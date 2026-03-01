#!/usr/bin/env python3
"""
Import mosques from Muslims in Britain (muslimsInBritain.org) CSV.
- Parses the MiB GPS CSV format
- Filters out Shia and multi-faith entries
- Reverse geocodes lat/lon to postcodes via Postcodes.io
- Deduplicates against existing directory.json (postcode + fuzzy name)
- Outputs merged directory_new.json for clean_directory.py pipeline
"""

import csv
import json
import re
import time
import urllib.request
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
MIB_CSV = Path(__file__).parent / "MosquesMar26.csv"
EXISTING_DIR = PROJECT_DIR / "directory.json"
OUTPUT_FILE = PROJECT_DIR / "directory_new.json"

# Batch size for Postcodes.io (max 100 per request)
GEOCODE_BATCH = 100


def parse_mib_csv(filepath):
    """Parse the MiB GPS CSV format.

    Format: lon,lat,"*[codes]Name. Address. Phone"
    Codes: capacity + W/NoW + denomination + management
    """
    mosques = []
    with open(filepath, encoding="latin-1") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Split: lon,lat,"description"
            parts = line.split(",", 2)
            if len(parts) < 3:
                continue

            try:
                lon = float(parts[0])
                lat = float(parts[1])
            except ValueError:
                continue

            desc = parts[2].strip().strip('"').strip()

            # Parse: [*?][codes]Name. Address. Phone
            match = re.match(r"([*?]?)\[(.+?)\](.*)", desc)
            if not match:
                continue

            precision = match.group(1)
            codes = match.group(2)
            rest = match.group(3).strip()

            # Split rest by ". " — Name. Address. Phone
            segments = rest.split(". ")
            name = segments[0].strip() if segments else ""
            address = segments[1].strip().rstrip(".") if len(segments) > 1 else ""
            phone = segments[2].strip().rstrip(".") if len(segments) > 2 else ""

            # Extra segments go into address (some addresses have periods)
            if len(segments) > 3:
                # Last segment with digits is likely phone
                last = segments[-1].strip().rstrip(".")
                if re.search(r"\d{5,}", last.replace(" ", "")):
                    phone = last
                    address = ", ".join(s.strip().rstrip(".") for s in segments[1:-1])
                else:
                    phone = ""
                    address = ", ".join(s.strip().rstrip(".") for s in segments[1:])

            # Parse denomination from codes
            denomination = ""
            if "Shia" in codes:
                denomination = "shia"
            elif "Brel" in codes:
                denomination = "barelvi"
            elif "Deob" in codes:
                denomination = "deobandi"
            elif "Salf" in codes:
                denomination = "salafi"
            elif "Maud" in codes:
                denomination = "maudoodi"
            elif "Sufi" in codes:
                denomination = "sufi"
            elif "Arab" in codes:
                denomination = "arab"

            # Check multi-faith
            is_multi = "multi" in codes.lower()

            # Women's facilities
            has_women = "W" in codes and "NoW" not in codes

            # Usage flags
            is_jumuah_only = "J" in codes and "NJ" not in codes
            is_irregular = "Irreg" in codes

            # Capacity
            cap_match = re.match(r"(\d+)", codes)
            capacity = int(cap_match.group(1)) if cap_match else None

            mosques.append({
                "name": name,
                "address": address,
                "phone": phone,
                "lat": lat,
                "lon": lon,
                "denomination": denomination,
                "is_multi": is_multi,
                "capacity": capacity,
                "has_women": has_women,
                "is_jumuah_only": is_jumuah_only,
                "is_irregular": is_irregular,
                "precision": precision,
            })

    return mosques


def batch_reverse_geocode(mosques):
    """Add postcodes and cities via Postcodes.io batch reverse geocode."""
    total = len(mosques)
    print(f"Reverse geocoding {total} mosques...")

    for i in range(0, total, GEOCODE_BATCH):
        batch = mosques[i : i + GEOCODE_BATCH]
        geolocations = [
            {"longitude": m["lon"], "latitude": m["lat"]} for m in batch
        ]

        payload = json.dumps({"geolocations": geolocations}).encode()
        req = urllib.request.Request(
            "https://api.postcodes.io/postcodes",
            data=payload,
            headers={"Content-Type": "application/json"},
        )

        try:
            resp = urllib.request.urlopen(req)
            data = json.loads(resp.read())

            for j, result in enumerate(data.get("result", [])):
                if result and result.get("result"):
                    best = result["result"][0]
                    mosques[i + j]["postcode"] = best.get("postcode", "")
                    mosques[i + j]["city"] = best.get("admin_district", "")
                else:
                    mosques[i + j]["postcode"] = ""
                    mosques[i + j]["city"] = ""
        except Exception as e:
            print(f"  Geocode error at batch {i}: {e}")
            for j in range(len(batch)):
                mosques[i + j]["postcode"] = ""
                mosques[i + j]["city"] = ""

        if (i + GEOCODE_BATCH) % 500 == 0 or i + GEOCODE_BATCH >= total:
            print(f"  {min(i + GEOCODE_BATCH, total)}/{total} geocoded")

        # Rate limit: be nice to the free API
        time.sleep(0.2)

    return mosques


def normalize_postcode(pc):
    """Remove spaces and uppercase for comparison."""
    return pc.upper().replace(" ", "") if pc else ""


def normalize_name(name):
    """Normalize mosque name for fuzzy matching."""
    name = name.lower().strip()
    # Remove common prefixes/suffixes
    for word in [
        "the ", "masjid ", "mosque ", "islamic centre ",
        "islamic center ", "jamia ", "jami ", "jamme ",
        " mosque", " masjid", " islamic centre", " islamic center",
        " and islamic centre", " & islamic centre",
        " community centre", " education centre",
    ]:
        name = name.replace(word, " ")
    # Remove punctuation
    name = re.sub(r"[^a-z0-9\s]", "", name)
    # Collapse whitespace
    name = re.sub(r"\s+", " ", name).strip()
    return name


def deduplicate(mib_mosques, existing_mosques):
    """Remove MiB mosques that already exist in directory.json.

    Strategy:
    1. Exact postcode match (primary)
    2. Fuzzy name match within same postcode area (outward code)
    3. Coordinate proximity (within ~100m)
    """
    # Build lookup sets from existing
    existing_postcodes = set()
    existing_outward_names = {}  # outward_code -> set of normalized names
    existing_coords = []  # [(lat, lon)]

    for m in existing_mosques:
        pc = normalize_postcode(m.get("postcode", ""))
        if pc:
            existing_postcodes.add(pc)
            # Outward code (first half of postcode)
            outward = pc.split()[0] if " " in m.get("postcode", "") else pc[:-3]
            norm_name = normalize_name(m["name"])
            if outward not in existing_outward_names:
                existing_outward_names[outward] = set()
            existing_outward_names[outward].add(norm_name)

        if m.get("lat") and m.get("lon"):
            existing_coords.append((m["lat"], m["lon"]))

    new_mosques = []
    dupes = {"postcode": 0, "name": 0, "coord": 0}

    for m in mib_mosques:
        pc = normalize_postcode(m.get("postcode", ""))

        # 1. Exact postcode match
        if pc and pc in existing_postcodes:
            dupes["postcode"] += 1
            continue

        # 2. Fuzzy name match in same outward code area
        if pc:
            outward = pc[:-3] if len(pc) > 3 else pc
            norm = normalize_name(m["name"])
            if outward in existing_outward_names:
                matched = False
                for existing_name in existing_outward_names[outward]:
                    # Check if names share significant words
                    e_words = set(existing_name.split())
                    n_words = set(norm.split())
                    common = e_words & n_words
                    # If they share 2+ meaningful words (not "al", "ul", etc.)
                    meaningful = {w for w in common if len(w) > 2}
                    if len(meaningful) >= 2:
                        dupes["name"] += 1
                        matched = True
                        break
                if matched:
                    continue

        # 3. Coordinate proximity (~100m = 0.001 degrees)
        close = False
        for elat, elon in existing_coords:
            if abs(m["lat"] - elat) < 0.001 and abs(m["lon"] - elon) < 0.001:
                dupes["coord"] += 1
                close = True
                break
        if close:
            continue

        new_mosques.append(m)

    return new_mosques, dupes


def to_directory_entry(m):
    """Convert MiB mosque to directory.json schema."""
    entry = {
        "name": m["name"],
        "address": m.get("address", ""),
        "postcode": m.get("postcode", ""),
        "city": m.get("city", ""),
        "has_timetable": False,
        "slug": None,
        "color1": None,
        "color2": None,
        "tags": "",
        "type": "mosque",
        "lat": round(m["lat"], 6),
        "lon": round(m["lon"], 6),
    }

    if m.get("phone"):
        entry["phone"] = m["phone"]

    # Tag type based on name/usage
    name_lower = m["name"].lower()
    if any(kw in name_lower for kw in ["prayer room", "prayer hall", "musallah", "musalla"]):
        entry["type"] = "prayer_room"
    elif m.get("is_jumuah_only"):
        entry["type"] = "prayer_room"  # Jumu'ah-only venues are effectively prayer rooms
    elif any(kw in name_lower for kw in ["community centre", "community center"]):
        if "mosque" not in name_lower and "masjid" not in name_lower:
            entry["type"] = "community_centre"

    return entry


def main():
    # 1. Parse MiB CSV
    print("Parsing MiB CSV...")
    all_mib = parse_mib_csv(MIB_CSV)
    print(f"  Total entries: {len(all_mib)}")

    # 2. Filter Shia and multi-faith
    filtered = [
        m for m in all_mib
        if m["denomination"] != "shia" and not m["is_multi"]
    ]
    shia_count = sum(1 for m in all_mib if m["denomination"] == "shia")
    multi_count = sum(1 for m in all_mib if m["is_multi"])
    print(f"  Filtered out: {shia_count} Shia, {multi_count} multi-faith")
    print(f"  After filtering: {len(filtered)}")

    # 3. Reverse geocode to get postcodes and cities
    filtered = batch_reverse_geocode(filtered)
    with_pc = sum(1 for m in filtered if m.get("postcode"))
    print(f"  With postcode: {with_pc}/{len(filtered)}")

    # 4. Load existing directory
    print("\nLoading existing directory...")
    with open(EXISTING_DIR) as f:
        existing_data = json.load(f)
    existing = existing_data["mosques"]
    print(f"  Existing mosques: {len(existing)}")

    # 5. Deduplicate
    print("\nDeduplicating...")
    new_mosques, dupes = deduplicate(filtered, existing)
    print(f"  Duplicates removed:")
    for reason, count in dupes.items():
        if count:
            print(f"    {reason}: {count}")
    print(f"  Total duplicates: {sum(dupes.values())}")
    print(f"  New unique mosques: {len(new_mosques)}")

    # 6. Convert to directory format
    new_entries = [to_directory_entry(m) for m in new_mosques]

    # 7. Merge with existing
    merged = existing + new_entries
    output = {"mosques": merged}

    # 8. Write output
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nOutput: {len(merged)} mosques ({len(existing)} existing + {len(new_entries)} new)")
    print(f"Written to: {OUTPUT_FILE}")

    # Type breakdown
    types = {}
    for m in merged:
        t = m.get("type", "mosque")
        types[t] = types.get(t, 0) + 1
    print(f"\nBy type:")
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
