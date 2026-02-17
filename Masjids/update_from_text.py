#!/usr/bin/env python3
"""Parse the authoritative text file and update all data.json files."""
import re, json, os

TEXT_FILE = os.path.join(os.path.dirname(__file__), '1. Masjid_text.txt')
MASJIDS_DIR = os.path.dirname(__file__)

# Map text file section names to folder names
FOLDER_MAP = {
    "Masjid Namirah": "Masjid Namirah",
    "Iqra Masjid": "Iqra Masjid",
    "Al Abrar Academy": "Al Abrar Academy",
    "Imam Yusuf Motala Academy": None,  # Already on website (iyma/)
    "Jamia Abu Hanifa Madrassa": "Jamia Abu Hanifa Madrassa",
    "Madrasa Abbasiya": "Madrasa Abbasiya",
    "Masjid Ibraheem": "Masjid Ibraheem",
    "Jamiah Farooqiah": "Jamiah Farooqiah",
    "Al Hikmah": "Al Hikmah Learning Centre",
    "Masjid Usman": "Masjid Usman",
    "Masjid ~ E ~ Usman": "Masjid Usman",
    "Masjid Abu Bakar": None,  # Already on website (abubakar/)
    "PYC Masjid Ahle Bayt": "PTC Masjid Ahle Bayt",
    "PTC Masjid Ahle Bayt": "PTC Masjid Ahle Bayt",
    "Firdaws": "Firdaws Islamic Centre",
    "Salahaddin": "SALAHADIN_WEBSITE",  # Special: update website version
    "Salahadin": "SALAHADIN_WEBSITE",
    "Salahaddin Mosque": "SALAHADIN_WEBSITE",
    "Jamia Masjid": None,  # Already on website (JamiaMasjid/)
    "Muslim Association of Bradford": None,  # Already on website (JamiaMasjid/)
    "Shahjalal": None,  # Already on website
    "Al Mahadul Islami": None,  # Already on website (Almahad/)
    "Al-Mustaqeem": "Al-Mustaqeem Education Centre",
    "Madni Masjid": "Madni Masjid",
    "Markazi Masjid Darul Irfan": "Markazi Masjid Darul Irfan",
    "Masjid Ali": "Masjid Ali",
    "Masjid Umar Farooqa": "Masjid Umar Farooqa Canterbury",
    "Khanqah Naqshbandia": "Masjid Umar Farooqa Canterbury",
    "Wibsey Musalla": "Wibsey Musalla",
    "Wibsey/Buttershaw": "Wibsey Buttershaw Islamic Dawah Centre",
    "Wibsey Buttershaw": "Wibsey Buttershaw Islamic Dawah Centre",
    "Wibsey & Buttershaw": "Wibsey Buttershaw Islamic Dawah Centre",
    "Doha Mosque": "Doha Masjid",
    "Doha Masjid": "Doha Masjid",
    "Nusrat": "Masjid Nusratul Islam",
    "Masjid Nusratul Islam": "Masjid Nusratul Islam",
    "Azharul Madaaris": "Ashanul Madaaris",
    "Ashanul Madaaris": "Ashanul Madaaris",
    "Musalla Salaam": "Musalla Salaam Clayton",
    "Masjid Noorul Islam": "Masjid Noorul Islam",
    "Masjid Taqwa": "Masjid Taqwa",
    "Masjid Hamza": "Masjid Hamza",
    "Tawakkulia": None,  # Already on website
    "Masjid Quba": None,  # Already on website
    "Darul Mahmood": "Darul Mahmood",
    "Masjid Bilal": "Masjid Bilal",
    "Masjid Noor": "Masjid Noor",
    "Masjid Umar": "Masjid Umar",
    "Masjid E-Umar": "Masjid Umar",
    "Masjid Abdullah": "Masjid Abdullah bin Masood",
    "Shipley Islamic": "Shipley Islamic Education Centre",
    "Masjidur Raashideen": "Masjidur Raashideen",
    "Al Hidaya": "Al Hidaya Academy",
    "Masjid Husain": "Masjid Husain",
    "Masjid Ayesha": "Masjid Ayesha",
    "Al Amin": "Al Amin Islamic Society",
    "Al-Hidaayah": "Al-Hidaayah Foundation",
    "Baitul Ilm": "Baitul Ilm",
}

def normalize_time(t):
    """Normalize time string: dots to colons, strip leading zeros, 24h to 12h, strip quotes."""
    if not t or t == '""' or t == "''":
        return ""
    t = str(t).strip().strip('"').strip("'")
    # Handle AM/PM suffixes
    is_pm = 'pm' in t.lower()
    is_am = 'am' in t.lower()
    t = re.sub(r'\s*(AM|PM|am|pm)\s*', '', t).strip()
    t = t.replace('.', ':')
    # Strip leading zeros from hours: "05:39" -> "5:39"
    if ':' in t and t[0] == '0' and len(t.split(':')[0]) == 2:
        t = t.lstrip('0') or '0'
        if ':' not in t:
            t = '0:' + t  # edge case
    # Handle case where it's just a number
    if ':' not in t:
        return t
    # Convert PM times to 24h then back to 12h
    parts = t.split(':')
    if len(parts) == 2:
        h = int(parts[0])
        # If explicitly PM and hour < 12, add 12 first
        if is_pm and h < 12:
            h += 12
        # Convert 24-hour to 12-hour format (website uses 12h)
        if h >= 13:
            t = f"{h - 12}:{parts[1]}"
        elif h == 0:
            t = f"12:{parts[1]}"
        else:
            t = f"{h}:{parts[1]}"
    return t

def find_folder(section_title):
    """Find the matching folder for a section title."""
    for key, folder in FOLDER_MAP.items():
        if key.lower() in section_title.lower():
            return folder
    return None

def parse_timetable_rows(js_text):
    """Parse JavaScript array of timetable objects into Python list."""
    rows = []
    # Match each { ... } object
    pattern = r'\{([^}]+)\}'
    for match in re.finditer(pattern, js_text):
        obj_str = match.group(1)
        row = {}

        # Extract date array
        date_match = re.search(r'date:\s*\[(\d+),\s*(\d+),\s*(\d+)\]', obj_str)
        if date_match:
            row['date'] = [int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))]

        # Extract day
        day_match = re.search(r'day:\s*"(\w+)"', obj_str)
        if day_match:
            row['day'] = day_match.group(1)

        # Extract no
        no_match = re.search(r'no:\s*(\d+)', obj_str)
        if no_match:
            row['no'] = int(no_match.group(1))

        # Extract ALL time fields (various naming conventions across mosques)
        all_fields = re.findall(r'(\w+):\s*"([^"]*)"', obj_str)
        for fname, fval in all_fields:
            val = normalize_time(fval)
            if not val:
                continue
            # Map field name variants to standard names
            fl = fname.lower()
            if fl in ('sehri', 'sehr', 'sahoor', 'suhoor'):
                row.setdefault('sehri', val)
            elif fl in ('fajr', 'fajrb', 'bfajr', 'fajrbegin', 'fajr_begin'):
                row.setdefault('fajr', val)
            elif fl in ('zuhr', 'zuhrb', 'bzuhr', 'dhuhr', 'zohr'):
                row.setdefault('zuhr', val)
            elif fl in ('asr', 'asrb', 'basr'):
                row.setdefault('asr', val)
            elif fl in ('isha', 'ishab', 'bisha', 'esha'):
                row.setdefault('isha', val)
            elif fl == 'sunrise':
                row.setdefault('sunrise', val)
            elif fl in ('maghrib', 'iftar', 'iftaar'):
                row.setdefault('maghrib', val)
            elif fl in ('jfajr', 'fajrj', 'jamaatfajr'):
                row.setdefault('jFajr', val)
            elif fl in ('jzuhr', 'zuhrj', 'jamaatzuhr'):
                row.setdefault('jZuhr', val)
            elif fl in ('jasr', 'asrj', 'jamaatasr'):
                row.setdefault('jAsr', val)
            elif fl in ('jisha', 'ishaj', 'jamaatisha'):
                row.setdefault('jIsha', val)
            elif fl in ('jmaghrib', 'maghribj', 'jamaatmaghrib'):
                # Some mosques list jMaghrib separately; use as maghrib if not set
                row.setdefault('jMaghrib', val)

        if row.get('date'):
            # Derive day from date if missing
            if 'day' not in row or not row['day']:
                from datetime import date as dt_date
                d = dt_date(row['date'][0], row['date'][1], row['date'][2])
                row['day'] = d.strftime('%a')
            rows.append(row)

    return rows

def ensure_all_fields(rows):
    """Ensure each row has all required fields, using defaults if missing."""
    sunrise_defaults = {
        1:"7:22", 2:"7:20", 3:"7:17", 4:"7:15", 5:"7:13", 6:"7:11", 7:"7:09",
        8:"7:06", 9:"7:04", 10:"7:02", 11:"7:00", 12:"6:55", 13:"6:53", 14:"6:50",
        15:"6:48", 16:"6:45", 17:"6:43", 18:"6:41", 19:"6:38", 20:"6:36", 21:"6:34",
        22:"6:31", 23:"6:29", 24:"6:26", 25:"6:24", 26:"6:21", 27:"6:19", 28:"6:17",
        29:"6:14", 30:"6:12"
    }
    required = ['date', 'day', 'no', 'sehri', 'fajr', 'sunrise', 'zuhr', 'asr',
                'isha', 'jFajr', 'jZuhr', 'jAsr', 'maghrib', 'jIsha']

    for row in rows:
        no = row.get('no', 0)
        if 'sunrise' not in row or not row['sunrise']:
            row['sunrise'] = sunrise_defaults.get(no, "7:00")

        # Use jMaghrib as maghrib if maghrib missing
        if ('maghrib' not in row or not row['maghrib']) and row.get('jMaghrib'):
            row['maghrib'] = row['jMaghrib']

        # Derive beginning times from jamaah times if missing
        if 'fajr' not in row or not row['fajr']:
            row['fajr'] = row.get('jFajr', '5:30')
        if 'sehri' not in row or not row['sehri']:
            # Sehri ~10 min before fajr
            fajr = row.get('fajr', '')
            if fajr and ':' in fajr:
                h, m = int(fajr.split(':')[0]), int(fajr.split(':')[1])
                m -= 10
                if m < 0: m += 60; h -= 1
                row['sehri'] = f"{h}:{m:02d}"
            else:
                row['sehri'] = '5:30'
        if 'zuhr' not in row or not row['zuhr']:
            row['zuhr'] = '12:20'
        if 'asr' not in row or not row['asr']:
            row['asr'] = row.get('jAsr', '3:30')

        # Derive isha from jIsha or maghrib
        if 'isha' not in row or not row['isha']:
            row['isha'] = row.get('jIsha', '7:30')
        if 'maghrib' not in row or not row['maghrib']:
            row['maghrib'] = '5:30'

        # Derive jamaah times from beginning times if missing
        if 'jFajr' not in row or not row['jFajr']:
            row['jFajr'] = row.get('fajr', '')
        if 'jZuhr' not in row or not row['jZuhr']:
            row['jZuhr'] = '1:00'
        if 'jAsr' not in row or not row['jAsr']:
            row['jAsr'] = row.get('asr', '')
        if 'jIsha' not in row or not row['jIsha']:
            row['jIsha'] = row.get('isha', '')

        # Clean up temp field
        row.pop('jMaghrib', None)

    return rows

def parse_mosque_info(info_text):
    """Extract mosque info from the text between section header and timetable."""
    info = {}

    patterns = {
        'name': r'Name:\s*(.+?)(?:\n|$)',
        'address': r'Address:\s*(.+?)(?:\n|$)',
        'phone': r'Phone:\s*(.+?)(?:\n|$)',
        'email': r'Email:\s*(.+?)(?:\n|$)',
        'website': r'Website:\s*(.+?)(?:\n|$)',
        'eid_info': r'Eid Salah.*?:\s*(.+?)(?:\n|$)',
        'fitrana': r'(?:Sadaqatul Fitr|Fitrana).*?:\s*(.+?)(?:\n|$)',
        'donations': r'Donations?:\s*(.+?)(?:\n|$)',
        'note': r'Note:\s*(.+?)(?:\n|$)',
        'receiver': r'Receiver.*?:\s*(.+?)(?:\n|$)',
    }

    for key, pat in patterns.items():
        m = re.search(pat, info_text, re.IGNORECASE)
        if m:
            info[key] = m.group(1).strip()

    return info

def main():
    with open(TEXT_FILE, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split into sections by numbered headers like "1. Masjid Name" or "15. Salahaddin"
    # Pattern: start of line, number, dot, space, then the name
    sections = re.split(r'\n(?=\d+\.\s+)', text)

    updated = 0
    skipped = 0
    salahadin_data = None

    for section in sections:
        if not section.strip():
            continue

        # Get section header
        header_match = re.match(r'(\d+)\.\s+(.+?)(?:\n|$)', section)
        if not header_match:
            continue

        section_num = int(header_match.group(1))
        section_title = header_match.group(2).strip()

        # Find the JavaScript array
        js_match = re.search(r'const\s+\w+\s*=\s*\[(.*?)\];', section, re.DOTALL)
        if not js_match:
            print(f"  SKIP #{section_num} {section_title} - no timetable data")
            skipped += 1
            continue

        rows = parse_timetable_rows(js_match.group(0))
        if len(rows) != 30:
            print(f"  WARN #{section_num} {section_title} - got {len(rows)} rows (expected 30)")
            if len(rows) < 25:
                continue

        rows = ensure_all_fields(rows)

        # Find the matching folder
        folder = find_folder(section_title)

        if folder is None:
            print(f"  SKIP #{section_num} {section_title} - already on website")
            skipped += 1
            continue

        # Extract mosque info
        info_text = section[:section.find('const ')] if 'const ' in section else section
        info = parse_mosque_info(info_text)

        if folder == "SALAHADIN_WEBSITE":
            # Special handling for Salahadin - save for later
            salahadin_data = {'rows': rows, 'info': info, 'section_title': section_title}
            print(f"  SAVED #{section_num} {section_title} - for Salahadin website update")
            continue

        folder_path = os.path.join(MASJIDS_DIR, folder)
        data_path = os.path.join(folder_path, 'data.json')

        if not os.path.isdir(folder_path):
            print(f"  WARN #{section_num} {section_title} - folder not found: {folder}")
            continue

        # Load existing data.json if it exists (to preserve non-timetable fields)
        existing = {}
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                existing = json.load(f)

        # Update with correct data from text file
        if info.get('name'):
            existing['name'] = info['name']
        if info.get('address'):
            existing['address'] = info['address']
        if info.get('phone'):
            existing['phone'] = info['phone']
            existing['phone_display'] = info['phone']
        if info.get('eid_info'):
            existing['eid_info'] = info['eid_info']
        if info.get('fitrana'):
            existing['fitrana'] = info['fitrana']
        if info.get('donations'):
            existing['donation_info'] = info['donations']
        if info.get('note'):
            existing['notes'] = info['note']
        if info.get('receiver'):
            existing['receiver_freq'] = info['receiver']
        if info.get('website'):
            existing['website'] = info['website']

        # Replace timetable with authoritative data
        existing['timetable'] = rows

        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

        print(f"  UPDATED #{section_num} {section_title} -> {folder} ({len(rows)} rows)")
        updated += 1

    # Handle Salahadin
    if salahadin_data:
        sal_path = os.path.join(MASJIDS_DIR, 'salahadin_update.json')
        with open(sal_path, 'w', encoding='utf-8') as f:
            json.dump({
                'info': salahadin_data['info'],
                'timetable': salahadin_data['rows']
            }, f, indent=2, ensure_ascii=False)
        print(f"\n  Salahadin data saved to {sal_path}")

    print(f"\nDone! Updated: {updated}, Skipped: {skipped}")

if __name__ == '__main__':
    main()
