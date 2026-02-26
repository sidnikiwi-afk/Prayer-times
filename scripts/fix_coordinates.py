#!/usr/bin/env python3
"""
Replace postcode-centroid coordinates with exact OSM building coordinates.

1. Re-queries Overpass API for all UK mosques (just coords + name)
2. Matches OSM results to directory entries by name or postcode
3. Updates lat/lon with exact building positions
4. Falls back to postcode centroid if no OSM match found
"""

import json
import re
import time
import urllib.request
import urllib.parse
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
DIRECTORY_FILE = PROJECT_DIR / "directory_clean.json"
RETRY_FILE = PROJECT_DIR / "scripts" / "retry_osm_data.json"
OUTPUT_FILE = PROJECT_DIR / "directory_clean.json"

# Same regions as build_directory.py but with smaller boxes for problem areas
UK_REGIONS = [
    # London split into 4
    ("London NW", (51.5, -0.5, 51.7, -0.1)),
    ("London NE", (51.5, -0.1, 51.7, 0.3)),
    ("London SW", (51.3, -0.5, 51.5, -0.1)),
    ("London SE", (51.3, -0.1, 51.5, 0.3)),
    ("SE England", (50.7, -1.5, 51.3, 1.5)),
    ("SW England", (50.0, -5.8, 51.3, -1.5)),
    ("East England", (51.7, 0.0, 52.8, 1.8)),
    # Birmingham area split
    ("Birmingham", (52.3, -2.1, 52.6, -1.6)),
    ("West Mids wider", (52.0, -2.5, 52.3, -1.2)),
    ("West Mids north", (52.6, -2.5, 52.8, -1.2)),
    ("East Midlands south", (52.0, -1.2, 52.5, 0.0)),
    ("East Midlands north", (52.5, -1.2, 53.0, 0.0)),
    ("NW England", (53.0, -3.2, 53.7, -1.8)),
    ("Greater Manchester", (53.3, -2.5, 53.7, -1.8)),
    ("Yorkshire South", (53.2, -1.8, 53.7, -0.5)),
    ("Yorkshire West", (53.6, -2.2, 54.0, -1.2)),
    ("Yorkshire North+East", (53.7, -1.2, 54.5, 0.0)),
    ("NE England south", (54.5, -2.5, 55.0, 0.0)),
    ("NE England north", (55.0, -2.5, 55.5, 0.0)),
    ("Lancashire", (53.6, -3.2, 54.2, -2.2)),
    ("South Wales", (51.3, -4.0, 51.8, -2.5)),
    ("North Wales", (52.5, -5.5, 53.5, -2.5)),
    ("Scotland South", (55.5, -5.5, 56.5, -2.0)),
    ("Scotland North", (56.5, -8.0, 61.0, -0.5)),
    ("Glasgow+Edinburgh", (55.8, -4.5, 56.1, -3.0)),
    ("N Ireland", (54.0, -8.5, 55.5, -5.0)),
    ("York+Hull", (53.7, -1.2, 54.2, 0.0)),
    ("Hampshire", (50.7, -1.5, 51.3, -0.5)),
    ("Kent", (51.0, 0.0, 51.5, 1.5)),
    ("Sussex+Surrey", (50.7, -0.8, 51.3, 0.2)),
]

OVERPASS_URLS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter",
]


def normalize(s):
    """Normalize string for matching."""
    return re.sub(r'[^a-z0-9]', '', s.lower())


def query_overpass_all():
    """Fetch all UK mosques from Overpass API with coordinates."""
    print("Querying OSM for exact mosque coordinates...")
    all_elements = []
    seen_ids = set()

    for region_name, (south, west, north, east) in UK_REGIONS:
        query = f"""
[out:json][timeout:60];
(
  node["amenity"="place_of_worship"]["religion"="muslim"]({south},{west},{north},{east});
  way["amenity"="place_of_worship"]["religion"="muslim"]({south},{west},{north},{east});
);
out center tags;
"""
        print(f"  {region_name}...", end=" ", flush=True)
        success = False
        for api_url in OVERPASS_URLS:
            data = urllib.parse.urlencode({"data": query}).encode()
            req = urllib.request.Request(api_url, data=data)
            try:
                with urllib.request.urlopen(req, timeout=90) as resp:
                    result = json.loads(resp.read())
                elements = result.get("elements", [])
                new = 0
                for el in elements:
                    eid = el.get("id")
                    if eid not in seen_ids:
                        seen_ids.add(eid)
                        all_elements.append(el)
                        new += 1
                print(f"{len(elements)} found ({new} new)")
                success = True
                break
            except Exception as e:
                continue
        if not success:
            print("FAILED")
        time.sleep(2)

    print(f"  Total unique: {len(all_elements)}")
    return all_elements


def extract_postcode(tags):
    """Extract postcode from OSM tags."""
    pc = tags.get("addr:postcode", "")
    if pc:
        return pc.upper().strip()
    full = tags.get("addr:full", "") + " " + tags.get("name", "")
    match = re.search(r'[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}', full.upper())
    return match.group(0) if match else ""


import math

def haversine(lat1, lon1, lat2, lon2):
    """Distance in km between two points."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def build_osm_entries(elements):
    """Build list of OSM entries with name, postcode, lat, lon."""
    entries = []
    for el in elements:
        tags = el.get("tags", {})
        name = tags.get("name", "").strip()
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if not lat or not lon or not name:
            continue
        pc = extract_postcode(tags)
        entries.append({
            "name": name,
            "norm_name": normalize(name),
            "postcode": pc,
            "norm_pc": pc.upper().replace(" ", "") if pc else "",
            "lat": lat,
            "lon": lon,
        })
    return entries


def find_best_match(mosque, osm_entries, pc_centroid_lat=None, pc_centroid_lon=None):
    """Find best OSM match for a directory mosque.

    Priority:
    1. Postcode match (same postcode = definitely same area)
    2. Name match + proximity check (within 5km of postcode centroid)
    3. None
    """
    norm_name = normalize(mosque["name"])
    norm_pc = mosque.get("postcode", "").upper().replace(" ", "")

    # 1. Try postcode match first - most reliable for location
    if norm_pc:
        pc_matches = [e for e in osm_entries if e["norm_pc"] == norm_pc]
        if len(pc_matches) == 1:
            return pc_matches[0], "postcode_exact"
        elif len(pc_matches) > 1:
            # Multiple mosques at same postcode - try name within those
            name_and_pc = [e for e in pc_matches if e["norm_name"] == norm_name]
            if name_and_pc:
                return name_and_pc[0], "postcode+name"
            # Return closest name match
            return pc_matches[0], "postcode_first"

    # 2. Try name match with proximity check
    name_matches = [e for e in osm_entries if e["norm_name"] == norm_name]
    if name_matches:
        if len(name_matches) == 1:
            # Only one mosque with this name - probably correct
            return name_matches[0], "name_unique"
        elif pc_centroid_lat and pc_centroid_lon:
            # Multiple matches - pick closest to postcode centroid
            closest = min(name_matches, key=lambda e: haversine(
                pc_centroid_lat, pc_centroid_lon, e["lat"], e["lon"]))
            dist = haversine(pc_centroid_lat, pc_centroid_lon,
                           closest["lat"], closest["lon"])
            if dist < 5:  # Within 5km of expected area
                return closest, f"name_nearest({dist:.1f}km)"

    return None, "no_match"


def main():
    # Load directory
    with open(DIRECTORY_FILE) as f:
        data = json.load(f)
    mosques = data["mosques"]
    print(f"Directory: {len(mosques)} mosques")

    # Load saved retry data first
    retry_elements = []
    if RETRY_FILE.exists():
        with open(RETRY_FILE) as f:
            retry_elements = json.load(f)
        print(f"Loaded {len(retry_elements)} elements from retry cache")

    # Query Overpass for fresh data
    fresh_elements = query_overpass_all()

    # Merge all OSM elements (retry + fresh)
    all_elements = retry_elements + fresh_elements
    # Deduplicate by ID
    seen = set()
    unique = []
    for el in all_elements:
        eid = el.get("id")
        if eid and eid not in seen:
            seen.add(eid)
            unique.append(el)
    all_elements = unique
    print(f"\nTotal unique OSM elements: {len(all_elements)}")

    # Build structured entries
    osm_entries = build_osm_entries(all_elements)
    print(f"OSM entries with name+coords: {len(osm_entries)}")

    # First pass: get postcode centroids for proximity checking
    # (use existing lat/lon which are centroids from Postcodes.io)
    existing_centroids = {}
    for m in mosques:
        pc = m.get("postcode", "").upper().replace(" ", "")
        if pc and m.get("lat"):
            existing_centroids[pc] = (m["lat"], m["lon"])

    # Match directory entries to OSM coordinates
    stats = {}
    for m in mosques:
        norm_pc = m.get("postcode", "").upper().replace(" ", "")
        centroid = existing_centroids.get(norm_pc, (None, None))

        match, method = find_best_match(m, osm_entries, centroid[0], centroid[1])

        if match:
            # Verify the match isn't wildly far from expected location
            if centroid[0] and centroid[1]:
                dist = haversine(centroid[0], centroid[1], match["lat"], match["lon"])
                if dist > 10:  # More than 10km away - suspicious
                    stats["rejected_far"] = stats.get("rejected_far", 0) + 1
                    # Keep existing centroid
                    continue

            m["lat"] = round(match["lat"], 6)
            m["lon"] = round(match["lon"], 6)
            stats[method] = stats.get(method, 0) + 1
        elif m.get("lat"):
            stats["kept_centroid"] = stats.get("kept_centroid", 0) + 1
        else:
            stats["no_coords"] = stats.get("no_coords", 0) + 1

    print(f"\nCoordinate matching results:")
    for method, count in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {method}: {count}")
    total_osm = sum(v for k, v in stats.items()
                    if k not in ("kept_centroid", "no_coords", "rejected_far"))
    print(f"  Total with exact OSM coords: {total_osm}")

    # Save
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nWritten to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
