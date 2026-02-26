#!/usr/bin/env python3
"""
Build a comprehensive UK mosque directory from OpenStreetMap data.
Merges with existing directory.json, excludes Shia and Ahmadiyya mosques.
"""

import json
import re
import time
import urllib.request
import urllib.parse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
DIRECTORY_FILE = PROJECT_DIR / "directory.json"
OUTPUT_FILE = PROJECT_DIR / "directory_new.json"

# --- Overpass API ---
# Use alternative Overpass endpoint (less congested)
OVERPASS_URLS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter",
]

# Split UK into smaller regional bounding boxes to avoid timeout
# Format: (south, west, north, east)
UK_REGIONS = [
    ("London", (51.3, -0.5, 51.7, 0.3)),
    ("SE England", (50.7, -1.5, 51.3, 1.5)),
    ("SW England", (50.0, -5.8, 51.3, -1.5)),
    ("East England", (51.7, 0.0, 52.8, 1.8)),
    ("West Midlands", (52.0, -2.5, 52.8, -1.2)),
    ("East Midlands", (52.0, -1.2, 53.0, 0.0)),
    ("NW England", (53.0, -3.2, 53.7, -1.8)),
    ("Greater Manchester", (53.3, -2.5, 53.7, -1.8)),
    ("Yorkshire South", (53.2, -1.8, 53.7, -0.5)),
    ("Yorkshire West", (53.6, -2.2, 54.0, -1.2)),
    ("Yorkshire North+East", (53.7, -1.2, 54.5, 0.0)),
    ("NE England", (54.5, -2.5, 55.5, 0.0)),
    ("Lancashire", (53.6, -3.2, 54.2, -2.2)),
    ("Wales", (51.3, -5.5, 53.5, -2.5)),
    ("Scotland South", (54.5, -5.5, 56.5, -2.0)),
    ("Scotland North", (56.5, -8.0, 61.0, -0.5)),
    ("N Ireland", (54.0, -8.5, 55.5, -5.0)),
]

# --- Exclusion filters ---
# Denomination tags to exclude
EXCLUDED_DENOMINATIONS = {"shia", "shi'a", "ahmadiyya", "ismaili"}

# Name keywords indicating Shia mosques
SHIA_KEYWORDS = [
    "hussainiya", "husainiya", "husainia", "hussainia",
    "imambargah", "imam bargah", "imam-bargah",
    "ja'fari", "jafari", "jaafari",
    "ithna ashari", "ithna-ashari",
    "khoei", "khoie",
    "idara-e-jaaferiya", "jaaferiya", "jaferiya",
    "shia", "shi'a",
    "mehfil-e-abbas", "mehfil e abbas",
    "al-abbas", "hussain foundation",
    "ahlulbayt", "ahlul bayt", "ahl ul bayt",
    "ahl-ul-bayt", "ahl al-bayt",
    "karbala", "kerbala",
    "hyderi", "haideri", "hayderi",
    "rasul al-adham", "rasul-al-adham",
]

# Name keywords indicating Ahmadiyya/Qadiani mosques
AHMADIYYA_KEYWORDS = [
    "ahmadiyya", "ahmadi muslim",
    "qadiani", "qadiany",
    "baitul futuh", "baitul ehsan", "baitul hamd",
    "baitul aman", "baitul afiyat", "baitul ahad",
    "baitul islam", "baitul noor", "baitul muqeet",
    "baitul ghafoor", "baitul ikram", "baitul huda",
    "nasir mosque", "fazl mosque",
    "ahmadiyya muslim association",
    "tahir mosque",
    "darul barakaat", "darul barakat",
    "noor mosque ahmadiyya",
    "mubarak mosque ahmadiyya",
]


def is_excluded(tags):
    """Check if a mosque should be excluded based on tags."""
    name = (tags.get("name", "") + " " + tags.get("name:en", "")).lower()
    denomination = tags.get("denomination", "").lower()
    description = tags.get("description", "").lower()
    operator = tags.get("operator", "").lower()

    # Check denomination tag
    for excl in EXCLUDED_DENOMINATIONS:
        if excl in denomination:
            return True

    # Check name/description/operator against keyword lists
    search_text = f"{name} {description} {operator}"
    for kw in SHIA_KEYWORDS:
        if kw in search_text:
            return True
    for kw in AHMADIYYA_KEYWORDS:
        if kw in search_text:
            return True

    return False


def extract_postcode(tags):
    """Try to extract a UK postcode from address tags."""
    postcode = tags.get("addr:postcode", "")
    if postcode:
        return postcode.upper().strip()
    # Try to find postcode in full address
    full = tags.get("addr:full", "") + " " + tags.get("name", "")
    match = re.search(r'[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}', full.upper())
    return match.group(0) if match else ""


def extract_address(tags):
    """Build address string from OSM tags."""
    parts = []
    housenumber = tags.get("addr:housenumber", "")
    street = tags.get("addr:street", "")
    if housenumber and street:
        parts.append(f"{housenumber} {street}")
    elif street:
        parts.append(street)
    elif housenumber:
        parts.append(housenumber)

    city = tags.get("addr:city", "")
    if city:
        parts.append(city)

    return ", ".join(parts)


def extract_city(tags, lat, lon):
    """Get city from OSM tags."""
    for key in ["addr:city", "addr:town", "addr:suburb"]:
        if tags.get(key):
            return tags[key]
    return ""


def reverse_geocode_batch(mosques_without_city):
    """Use Postcodes.io to get city for mosques with postcodes but no city."""
    postcodes = [m["postcode"] for m in mosques_without_city if m["postcode"]]
    if not postcodes:
        return

    # Deduplicate
    unique_postcodes = list(set(postcodes))
    results = {}

    # Batch lookup (100 per request)
    for i in range(0, len(unique_postcodes), 100):
        batch = unique_postcodes[i:i+100]
        data = json.dumps({"postcodes": batch}).encode()
        req = urllib.request.Request(
            "https://api.postcodes.io/postcodes",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read())
                if body.get("result"):
                    for item in body["result"]:
                        if item.get("result"):
                            r = item["result"]
                            # Use admin_district (e.g. "City of Bradford") or postal_town
                            city = r.get("admin_district", "") or r.get("parliamentary_constituency", "")
                            # Clean up "City of X" -> "X"
                            city = re.sub(r'^City of ', '', city)
                            results[item["query"]] = city
        except Exception as e:
            print(f"  Warning: Postcodes.io batch failed: {e}")
        time.sleep(0.5)  # Be nice to the API

    # Apply results
    for m in mosques_without_city:
        if m["postcode"] in results:
            m["city"] = results[m["postcode"]]


def reverse_geocode_coords(mosques_without_city):
    """Use Postcodes.io nearest postcode lookup for mosques without postcode."""
    for m in mosques_without_city:
        if m.get("city") or not m.get("_lat"):
            continue
        try:
            url = f"https://api.postcodes.io/postcodes?lon={m['_lon']}&lat={m['_lat']}&limit=1"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = json.loads(resp.read())
                if body.get("result") and len(body["result"]) > 0:
                    r = body["result"][0]
                    if not m["postcode"]:
                        m["postcode"] = r.get("postcode", "")
                    city = r.get("admin_district", "")
                    city = re.sub(r'^City of ', '', city)
                    m["city"] = city
        except Exception as e:
            pass
        time.sleep(0.3)


def query_overpass():
    """Fetch all UK mosques from Overpass API in regional batches."""
    print("Querying OpenStreetMap Overpass API for UK mosques...")
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
            print("FAILED (all endpoints)")
        time.sleep(3)

    print(f"  Total unique: {len(all_elements)}")
    return all_elements


def main():
    # Load existing directory
    with open(DIRECTORY_FILE) as f:
        existing = json.load(f)
    existing_mosques = existing["mosques"]
    existing_postcodes = {m["postcode"].upper().replace(" ", "") for m in existing_mosques if m["postcode"]}
    existing_names = {m["name"].lower() for m in existing_mosques}
    print(f"Existing directory: {len(existing_mosques)} mosques")

    # Query OSM
    elements = query_overpass()

    # Process results
    new_mosques = []
    excluded_count = 0
    no_name_count = 0
    duplicate_count = 0

    for el in elements:
        tags = el.get("tags", {})
        name = tags.get("name", "").strip()
        if not name:
            no_name_count += 1
            continue

        # Exclude Shia / Ahmadiyya
        if is_excluded(tags):
            excluded_count += 1
            continue

        # Get coordinates
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")

        postcode = extract_postcode(tags)
        address = extract_address(tags)
        city = extract_city(tags, lat, lon)

        # Check for duplicates against existing
        pc_normalized = postcode.upper().replace(" ", "") if postcode else ""
        name_lower = name.lower()
        if pc_normalized and pc_normalized in existing_postcodes:
            duplicate_count += 1
            continue
        if name_lower in existing_names:
            duplicate_count += 1
            continue

        # Also deduplicate within new results
        if pc_normalized and pc_normalized in {m["postcode"].upper().replace(" ", "") for m in new_mosques if m["postcode"]}:
            duplicate_count += 1
            continue

        new_mosques.append({
            "name": name,
            "address": address,
            "postcode": postcode,
            "city": city,
            "has_timetable": False,
            "slug": None,
            "color1": None,
            "color2": None,
            "tags": "",
            "_lat": lat,
            "_lon": lon,
        })

    print(f"\nFiltering results:")
    print(f"  Excluded (Shia/Ahmadiyya): {excluded_count}")
    print(f"  No name: {no_name_count}")
    print(f"  Duplicates with existing: {duplicate_count}")
    print(f"  New mosques to add: {len(new_mosques)}")

    # Resolve missing cities via Postcodes.io
    missing_city = [m for m in new_mosques if not m["city"]]
    if missing_city:
        print(f"\nResolving cities for {len(missing_city)} mosques via Postcodes.io...")

        # First try postcode lookup
        with_postcode = [m for m in missing_city if m["postcode"]]
        if with_postcode:
            print(f"  Batch postcode lookup for {len(with_postcode)} mosques...")
            reverse_geocode_batch(with_postcode)

        # Then try coordinate lookup for remaining
        still_missing = [m for m in new_mosques if not m.get("city")]
        if still_missing:
            print(f"  Coordinate lookup for {len(still_missing)} mosques...")
            reverse_geocode_coords(still_missing)

    # Final stats
    with_city = sum(1 for m in new_mosques if m.get("city"))
    with_postcode = sum(1 for m in new_mosques if m["postcode"])
    print(f"\nFinal data quality:")
    print(f"  With city: {with_city}/{len(new_mosques)}")
    print(f"  With postcode: {with_postcode}/{len(new_mosques)}")

    # Rename internal coordinate fields to public names
    for m in new_mosques:
        lat = m.pop("_lat", None)
        lon = m.pop("_lon", None)
        if lat and lon:
            m["lat"] = round(lat, 6)
            m["lon"] = round(lon, 6)

    # Merge: existing (unchanged) + new
    merged = existing_mosques + new_mosques
    output = {"mosques": merged}

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nOutput written to: {OUTPUT_FILE}")
    print(f"Total mosques: {len(merged)} ({len(existing_mosques)} existing + {len(new_mosques)} new)")

    # Show city breakdown
    city_counts = {}
    for m in merged:
        c = m.get("city") or "Unknown"
        city_counts[c] = city_counts.get(c, 0) + 1
    print(f"\nTop cities:")
    for city, count in sorted(city_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"  {city}: {count}")


if __name__ == "__main__":
    main()
