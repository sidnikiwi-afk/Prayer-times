#!/usr/bin/env python3
"""
Clean up directory_new.json:
- Remove duplicates (existing-vs-new and new-vs-new)
- Remove non-UK entries
- Tag non-mosque entries (prayer rooms, community centres) with type field
- Fix city name inconsistencies and typos
- Fix generic/incomplete names
- Add lat/lon back for Google Maps fallback
- Remove missed Shia/sectarian entries
"""

import json
import re
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
INPUT_FILE = PROJECT_DIR / "directory_new.json"
OUTPUT_FILE = PROJECT_DIR / "directory_clean.json"

# ---- 1. DUPLICATE REMOVAL ----
# OSM entries that duplicate existing mosques (matched by postcode or clear name match)
REMOVE_EXACT = {
    # name substring to match (lowercased) -> reason
    # These are new entries whose postcode matches an existing mosque
}

# Postcodes of existing mosques that got re-added from OSM with slightly different names
DUPLICATE_POSTCODES_OF_EXISTING = {
    "BD50HS",   # Shahjalal Masjid (duplicate of Shahjalal Islamic Society)
    "BD50LT",   # Al Mahadul Islami (duplicate of Al Mahad Ul Islami)
    "BD24NH",   # Imam Yusuf Motala Academy (duplicate of IYMA)
    "BD57BJ",   # Madni Masjid (duplicate of existing Madni Masjid)
    "BD71BG",   # Masjid Doha (duplicate of Doha Mosque)
    "BD157RD",  # Hussain Islamic Academy (duplicate of Masjid Husain)
    "BD38PX",   # Masjid Ibraheem Education Center (duplicate of Masjid Ibraheem & Ed Centre)
    "BD39AP",   # Al Hikmah / Jamiyat Tabligh-ul-Islam (duplicate of Al Hikmah)
}

# New-vs-new exact duplicates (keep first, remove second by postcode)
NEW_DUPLICATE_POSTCODES = {
    "M130TA",   # Makki Masjid appears twice
    "M80PN",    # Khizra Mosque near-duplicate (keep M8 0PH version)
}

# Near-duplicate postcodes of existing mosques (different name, adjacent postcode)
NEAR_DUPLICATE_NAMES = {
    "al abrar academy masjid",    # duplicate of Al Abrar Academy (BD3 0DT vs BD3 0BE)
    "madrassah jamiah farooqiah",  # duplicate of Jamiah Farooqiah (BD3 8QH vs BD3 8QJ)
}

# ---- 2. NON-UK ENTRIES ----
REMOVE_NON_UK = {
    "dundalk islamic culture centre",  # Republic of Ireland
}

# ---- 3. MISSED SHIA/SECTARIAN ----
REMOVE_SHIA = {
    "jaffria islamic centre",  # Jafari = Shia
}

# ---- 4. PRAYER ROOMS / NON-MOSQUE TAGGING ----
PRAYER_ROOM_KEYWORDS = [
    "prayer room", "prayer rooms", "prayer hall",
    "university mosque", "university islamic",
    "uon prayer room", "qmc prayer room",
    "dmu prayer room", "ntu prayer room",
    "cavendish prayer", "cemetery lodge prayer",
    "islamic prayer rooms",
]

COMMUNITY_CENTRE_KEYWORDS = [
    "community centre", "community center",
    "islamic mission college",
]

# ---- 5. CITY NAME FIXES ----
CITY_FIXES = {
    # Typos
    "Midlesbrough": "Middlesbrough",
    # Council names -> cleaner versions
    "Glasgow City": "Glasgow",
    "Aberdeen City": "Aberdeen",
    "Bristol, City of": "Bristol",
    "Bournemouth, Christchurch and Poole": "Bournemouth",
    "Oadby and Wigston": "Oadby",
    # Standardise Blackburn
    "Blackburn with Darwen": "Blackburn",
}

# ---- 6. GENERIC NAME FIXES ----
NAME_FIXES = {
    "Masjid": "Masjid (Long Eaton)",      # NG10 4QP - Long Eaton area
    "Jame": "Jame Masjid (Leicester)",      # LE5 3QJ - Leicester
    "Prayer Room": "Prayer Room (Liverpool)", # L69 7ZG
}


def normalize_postcode(pc):
    """Remove spaces and uppercase for comparison."""
    return pc.upper().replace(" ", "") if pc else ""


def is_prayer_room(name_lower):
    """Check if entry is a prayer room, not a mosque."""
    for kw in PRAYER_ROOM_KEYWORDS:
        if kw in name_lower:
            return True
    return False


def is_community_centre(name_lower):
    """Check if entry is primarily a community centre."""
    for kw in COMMUNITY_CENTRE_KEYWORDS:
        if kw in name_lower:
            # But if it also says "mosque" or "masjid", it's a mosque with a community centre
            if "mosque" in name_lower or "masjid" in name_lower:
                return False
            return True
    return False


def main():
    with open(INPUT_FILE) as f:
        data = json.load(f)

    mosques = data["mosques"]
    print(f"Input: {len(mosques)} mosques")

    # Separate existing (has_timetable=True) from new
    existing = [m for m in mosques if m.get("has_timetable")]
    new = [m for m in mosques if not m.get("has_timetable")]
    print(f"  Existing (with timetable): {len(existing)}")
    print(f"  New (from OSM): {len(new)}")

    # Track removals
    removed = {"duplicate_existing": 0, "duplicate_new": 0, "non_uk": 0, "shia": 0, "near_dup": 0}
    tagged = {"prayer_room": 0, "community_centre": 0}
    fixed = {"city": 0, "name": 0}

    cleaned_new = []
    seen_postcodes = set()

    for m in new:
        name = m["name"]
        name_lower = name.lower().strip()
        pc_norm = normalize_postcode(m.get("postcode", ""))

        # ---- Remove non-UK ----
        if name_lower in REMOVE_NON_UK:
            removed["non_uk"] += 1
            print(f"  REMOVED (non-UK): {name}")
            continue

        # ---- Remove missed Shia ----
        if name_lower in REMOVE_SHIA:
            removed["shia"] += 1
            print(f"  REMOVED (Shia): {name}")
            continue

        # ---- Remove duplicates of existing mosques ----
        if pc_norm and pc_norm in DUPLICATE_POSTCODES_OF_EXISTING:
            removed["duplicate_existing"] += 1
            print(f"  REMOVED (dup of existing): {name} [{m.get('postcode', '')}]")
            continue

        # ---- Remove near-duplicates ----
        if name_lower in NEAR_DUPLICATE_NAMES:
            removed["near_dup"] += 1
            print(f"  REMOVED (near-dup): {name}")
            continue

        # ---- Remove new-vs-new duplicates ----
        if pc_norm and pc_norm in NEW_DUPLICATE_POSTCODES:
            if pc_norm in seen_postcodes:
                removed["duplicate_new"] += 1
                print(f"  REMOVED (dup new-vs-new): {name} [{m.get('postcode', '')}]")
                continue

        # Track seen postcodes
        if pc_norm:
            seen_postcodes.add(pc_norm)

        # ---- Tag non-mosque entries ----
        if is_prayer_room(name_lower):
            m["type"] = "prayer_room"
            tagged["prayer_room"] += 1
        elif is_community_centre(name_lower):
            m["type"] = "community_centre"
            tagged["community_centre"] += 1
        else:
            m["type"] = "mosque"

        # ---- Fix city names ----
        city = m.get("city", "")
        if city in CITY_FIXES:
            m["city"] = CITY_FIXES[city]
            fixed["city"] += 1

        # ---- Fix generic names ----
        if name in NAME_FIXES:
            m["name"] = NAME_FIXES[name]
            fixed["name"] += 1

        cleaned_new.append(m)

    # Add type field to existing mosques too
    for m in existing:
        m["type"] = "mosque"

    # Merge
    merged = existing + cleaned_new
    output = {"mosques": merged}

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n--- Summary ---")
    print(f"Removed:")
    for reason, count in removed.items():
        if count:
            print(f"  {reason}: {count}")
    print(f"  Total removed: {sum(removed.values())}")
    print(f"\nTagged:")
    for tag, count in tagged.items():
        if count:
            print(f"  {tag}: {count}")
    print(f"\nFixed:")
    for fix, count in fixed.items():
        if count:
            print(f"  {fix}: {count}")
    print(f"\nOutput: {len(merged)} mosques ({len(existing)} existing + {len(cleaned_new)} new)")
    print(f"Written to: {OUTPUT_FILE}")

    # Show type breakdown
    type_counts = {}
    for m in merged:
        t = m.get("type", "mosque")
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"\nBy type:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
