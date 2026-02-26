#!/usr/bin/env python3
"""
Add lat/lon coordinates to directory_clean.json using Postcodes.io bulk lookup.
Coordinates enable Google Maps directions even when address is missing.
"""

import json
import time
import urllib.request
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
INPUT_FILE = PROJECT_DIR / "directory_clean.json"
OUTPUT_FILE = PROJECT_DIR / "directory_clean.json"  # overwrite in place

def bulk_postcode_lookup(postcodes):
    """Lookup lat/lon for up to 100 postcodes via Postcodes.io."""
    results = {}
    data = json.dumps({"postcodes": postcodes}).encode()
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
                        results[item["query"]] = {
                            "lat": r["latitude"],
                            "lon": r["longitude"],
                        }
    except Exception as e:
        print(f"  Warning: batch lookup failed: {e}")
    return results


def main():
    with open(INPUT_FILE) as f:
        data = json.load(f)

    mosques = data["mosques"]
    print(f"Total mosques: {len(mosques)}")

    # Collect unique postcodes that need coordinates
    need_coords = [m for m in mosques if not m.get("lat") and m.get("postcode")]
    unique_postcodes = list(set(m["postcode"] for m in need_coords))
    print(f"Unique postcodes to look up: {len(unique_postcodes)}")

    # Bulk lookup (100 per request)
    all_results = {}
    for i in range(0, len(unique_postcodes), 100):
        batch = unique_postcodes[i:i+100]
        print(f"  Batch {i//100 + 1}: {len(batch)} postcodes...", end=" ", flush=True)
        results = bulk_postcode_lookup(batch)
        all_results.update(results)
        print(f"{len(results)} resolved")
        time.sleep(0.5)

    # Apply coordinates
    added = 0
    no_postcode = 0
    not_found = 0
    for m in mosques:
        if m.get("postcode") and m["postcode"] in all_results:
            coords = all_results[m["postcode"]]
            m["lat"] = round(coords["lat"], 6)
            m["lon"] = round(coords["lon"], 6)
            added += 1
        elif not m.get("postcode"):
            no_postcode += 1
        else:
            not_found += 1

    print(f"\nResults:")
    print(f"  Coordinates added: {added}")
    print(f"  No postcode (can't look up): {no_postcode}")
    print(f"  Postcode not found: {not_found}")

    # List mosques without coordinates
    missing = [m for m in mosques if not m.get("lat")]
    if missing:
        print(f"\nMosques still without coordinates ({len(missing)}):")
        for m in missing:
            print(f"  - {m['name']} ({m.get('city', 'no city')})")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nWritten to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
