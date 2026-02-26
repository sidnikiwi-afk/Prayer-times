#!/usr/bin/env python3
"""
Enrich mosque directory using Serper.dev (Google Search API).
Fills in missing addresses, phone numbers, and websites.

Uses Google Places/Maps results via search to get:
- Full street address
- Phone number
- Website URL
- Postcode (if missing)

Rate: ~300 searches for mosques missing addresses.
Serper.dev free tier: 2,500 searches/month.
"""

import json
import os
import re
import time
import urllib.request
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
INPUT_FILE = PROJECT_DIR / "directory_clean.json"
OUTPUT_FILE = PROJECT_DIR / "directory_clean.json"
LOG_FILE = PROJECT_DIR / "scripts" / "enrich_log.json"

SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "")
SERPER_URL = "https://google.serper.dev/search"

# UK postcode regex
UK_POSTCODE_RE = re.compile(r'\b([A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})\b', re.IGNORECASE)

# Phone regex (UK landline/mobile)
UK_PHONE_RE = re.compile(r'\b(0\d{2,4}\s?\d{3,4}\s?\d{3,4})\b')


def search_serper(query):
    """Search Google via Serper.dev API."""
    data = json.dumps({
        "q": query,
        "gl": "gb",
        "hl": "en",
        "num": 5,
    }).encode()
    req = urllib.request.Request(
        SERPER_URL,
        data=data,
        headers={
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"    Search failed: {e}")
        return None


def extract_info_from_results(results, mosque_name, city):
    """Extract address, phone, website from search results."""
    info = {"address": "", "phone": "", "website": "", "postcode": ""}

    if not results:
        return info

    # Check Knowledge Graph first (most reliable)
    kg = results.get("knowledgeGraph", {})
    if kg:
        addr = kg.get("address", "")
        if addr:
            info["address"] = addr
        phone = kg.get("phone", "")
        if phone:
            info["phone"] = phone
        website = kg.get("website", "")
        if website:
            info["website"] = website

        # Try to extract postcode from address
        pc_match = UK_POSTCODE_RE.search(addr)
        if pc_match:
            info["postcode"] = pc_match.group(1).upper()

    # Check Places results
    places = results.get("places", [])
    if places:
        place = places[0]  # Top result
        if not info["address"]:
            addr = place.get("address", "")
            if addr:
                info["address"] = addr
                pc_match = UK_POSTCODE_RE.search(addr)
                if pc_match:
                    info["postcode"] = pc_match.group(1).upper()
        if not info["phone"]:
            info["phone"] = place.get("phone", "")

    # Check organic results for additional info
    organic = results.get("organic", [])
    for result in organic[:3]:
        snippet = result.get("snippet", "")
        title = result.get("title", "")
        link = result.get("link", "")

        # Extract postcode from snippets
        if not info["postcode"]:
            pc_match = UK_POSTCODE_RE.search(snippet)
            if pc_match:
                info["postcode"] = pc_match.group(1).upper()

        # Extract phone from snippets
        if not info["phone"]:
            phone_match = UK_PHONE_RE.search(snippet)
            if phone_match:
                info["phone"] = phone_match.group(1)

        # Get website (prefer mosque's own domain, not directories)
        if not info["website"] and link:
            skip_domains = ["facebook.com", "twitter.com", "instagram.com",
                           "google.com", "yelp.com", "tripadvisor",
                           "justdial", "yell.com", "192.com", "findamosque",
                           "wikipedia.org", "wikidata.org", "openstreetmap",
                           "salatomatic", "muslimdirectory", "halaltrip"]
            if not any(d in link.lower() for d in skip_domains):
                info["website"] = link

        # Try address from snippet
        if not info["address"]:
            # Look for street-like patterns in snippet
            addr_match = re.search(
                r'(\d+[A-Za-z]?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Street|Road|Lane|Avenue|Drive|Way|Terrace|Court|Place|Close|Crescent|Row|Square|Parade|Mount|Hill|Gardens|Park|Walk|Mews|Rise|Grove))',
                snippet
            )
            if addr_match:
                info["address"] = addr_match.group(1)

    return info


def clean_address(addr):
    """Clean up address string."""
    if not addr:
        return ""
    # Remove duplicate city/country info at end
    addr = re.sub(r',?\s*United Kingdom\s*$', '', addr, flags=re.IGNORECASE)
    addr = re.sub(r',?\s*UK\s*$', '', addr, flags=re.IGNORECASE)
    addr = re.sub(r',?\s*England\s*$', '', addr, flags=re.IGNORECASE)
    addr = re.sub(r',?\s*Scotland\s*$', '', addr, flags=re.IGNORECASE)
    addr = re.sub(r',?\s*Wales\s*$', '', addr, flags=re.IGNORECASE)
    return addr.strip().strip(',').strip()


def main():
    if not SERPER_API_KEY:
        print("ERROR: SERPER_API_KEY environment variable not set")
        return

    with open(INPUT_FILE) as f:
        data = json.load(f)

    mosques = data["mosques"]
    print(f"Total mosques: {len(mosques)}")

    # Find mosques needing enrichment (missing address)
    needs_enrichment = [m for m in mosques if not m.get("address")]
    print(f"Need enrichment (no address): {len(needs_enrichment)}")

    # Also enrich mosques missing postcode even if they have address
    needs_postcode = [m for m in mosques if not m.get("postcode") and m.get("address")]
    print(f"Have address but no postcode: {len(needs_postcode)}")

    # Combine
    to_enrich = needs_enrichment + [m for m in needs_postcode if m not in needs_enrichment]
    print(f"Total to search: {len(to_enrich)}")

    enriched = 0
    addresses_found = 0
    postcodes_found = 0
    phones_found = 0
    websites_found = 0
    log = []

    for i, m in enumerate(to_enrich):
        name = m["name"]
        city = m.get("city", "")
        pc = m.get("postcode", "")

        # Build search query
        query_parts = [name]
        if city:
            query_parts.append(city)
        elif pc:
            query_parts.append(pc)
        query_parts.append("mosque UK")
        query = " ".join(query_parts)

        print(f"  [{i+1}/{len(to_enrich)}] {name} ({city or pc})...", end=" ", flush=True)

        results = search_serper(query)
        if not results:
            print("FAILED")
            time.sleep(1)
            continue

        info = extract_info_from_results(results, name, city)

        # Apply enrichment
        updated = []
        if info["address"] and not m.get("address"):
            m["address"] = clean_address(info["address"])
            addresses_found += 1
            updated.append("addr")

        if info["postcode"] and not m.get("postcode"):
            m["postcode"] = info["postcode"]
            postcodes_found += 1
            updated.append("pc")

        if info["phone"] and not m.get("phone"):
            m["phone"] = info["phone"]
            phones_found += 1
            updated.append("tel")

        if info["website"] and not m.get("website"):
            m["website"] = info["website"]
            websites_found += 1
            updated.append("web")

        if updated:
            enriched += 1
            print(f"+ {', '.join(updated)}")
        else:
            print("no new data")

        log.append({
            "name": name,
            "city": city,
            "query": query,
            "found": info,
            "updated": updated,
        })

        # Rate limit: ~2 requests/sec to stay well within limits
        time.sleep(0.5)

    # Save enriched data
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Save log
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    print(f"\n--- Enrichment Summary ---")
    print(f"Searched: {len(to_enrich)}")
    print(f"Enriched: {enriched}")
    print(f"  Addresses found: {addresses_found}")
    print(f"  Postcodes found: {postcodes_found}")
    print(f"  Phones found: {phones_found}")
    print(f"  Websites found: {websites_found}")
    print(f"\nRemaining gaps:")
    print(f"  Still no address: {sum(1 for m in mosques if not m.get('address'))}")
    print(f"  Still no postcode: {sum(1 for m in mosques if not m.get('postcode'))}")
    print(f"\nWritten to: {OUTPUT_FILE}")
    print(f"Log: {LOG_FILE}")


if __name__ == "__main__":
    main()
