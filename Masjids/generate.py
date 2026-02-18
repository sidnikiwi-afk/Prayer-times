#!/usr/bin/env python3
"""Generate mosque timetable HTML pages from JSON data files."""
import json, re, os, glob

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'abubakar', 'index.html')
MASJIDS_DIR = os.path.dirname(__file__)

def generate(config_path):
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        html = f.read()
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    name = config["name"]
    folder = os.path.dirname(config_path)
    prefix = config.get("prefix", re.sub(r'[^a-z0-9]', '', name.lower()))
    address = config["address"]
    short_name = config.get("short_name", name.split(" ")[-1] if len(name.split()) > 2 else name)
    phone = config.get("phone", "")
    phone_display = config.get("phone_display", phone)
    notes = config.get("notes", "Maghrib Salah commences after Iftar")
    eid_info = config.get("eid_info", "")
    fitrana = config.get("fitrana", "")
    donation_info = config.get("donation_info", "")
    website = config.get("website", "")
    receiver_freq = config.get("receiver_freq", "")
    timetable = config["timetable"]

    # === META / TITLE ===
    html = html.replace("Masjid Abu Bakar - Ramadhan 1447 Timetable", f"{name} - Ramadhan 1447 Timetable")
    html = html.replace("Ramadan 1447 prayer timetable for Masjid Abu Bakar, Bradford", f"Ramadan 1447 prayer timetable for {name}, Bradford")
    html = html.replace("Masjid Abu Bakar - Ramadan 1447 Prayer Timetable", f"{name} - Ramadan 1447 Prayer Timetable")
    html = html.replace("Masjid Abu Bakar, Bradford - Sehri, Iftar & prayer times with live countdown", f"{name}, Bradford - Sehri, Iftar & prayer times with live countdown")
    html = html.replace("Abu Bakar Times", f"{short_name} Times")

    # === URLS ===
    html = html.replace("https://waqt.uk/abubakar/", f"https://waqt.uk/{os.path.basename(folder)}/")

    # === HEADER CONTENT ===
    html = html.replace("MASJID ABU BAKAR", name.upper())
    html = html.replace("38 Steadman Terrace, Bradford, BD3 9NB", address)

    # === CONTACT INFO ===
    if phone:
        html = html.replace("tel:01274668343", f"tel:{phone.replace(' ', '')}")
        html = html.replace("01274 668343", phone_display)
    else:
        # Remove phone link entirely
        html = re.sub(r'<a href="tel:01274668343".*?</a>', '', html, flags=re.DOTALL)

    # === LOCALSTORAGE PREFIX ===
    html = html.replace("'abubakar-", f"'{prefix}-")

    # === TIMETABLE DATA ===
    timetable_js = "const timetableData = [\n"
    for row in timetable:
        timetable_js += "            { "
        timetable_js += f'date: [{row["date"][0]}, {row["date"][1]}, {row["date"][2]}], '
        timetable_js += f'day: "{row["day"]}", no: {row["no"]}, '
        timetable_js += f'sehri: "{row["sehri"]}", fajr: "{row["fajr"]}", '
        timetable_js += f'sunrise: "{row["sunrise"]}", zuhr: "{row["zuhr"]}", '
        timetable_js += f'asr: "{row["asr"]}", isha: "{row["isha"]}", '
        timetable_js += f'jFajr: "{row["jFajr"]}", jZuhr: "{row["jZuhr"]}", '
        timetable_js += f'jAsr: "{row["jAsr"]}", maghrib: "{row["maghrib"]}", '
        timetable_js += f'jIsha: "{row["jIsha"]}"'
        timetable_js += " },\n"
    timetable_js += "        ]"
    # Find the full timetableData block using line markers (not regex, to avoid matching nested brackets)
    start_marker = 'const timetableData = ['
    end_marker = '\n        ];'
    start_idx = html.index(start_marker)
    end_idx = html.index(end_marker, start_idx) + len(end_marker)
    html = html[:start_idx] + timetable_js + ';' + html[end_idx:]

    # === FOOTER ===
    # Replace footer content
    footer_html = '<div class="footer">\n'
    footer_html += f'            <div class="footer-section contact-box" style="flex: 1 1 100%;">\n'
    footer_html += f'                <em>{notes}</em>\n'
    footer_html += '            </div>\n'
    if eid_info:
        footer_html += f'            <div class="footer-section eid-info">\n'
        footer_html += f'                <strong>Eid Salah</strong><br>{eid_info}\n'
        footer_html += '            </div>\n'
    if fitrana:
        footer_html += f'            <div class="footer-section fitrana-box">\n'
        footer_html += f'                <strong>Sadaqatul Fitr</strong><br>{fitrana}\n'
        footer_html += '            </div>\n'
    footer_html += '        </div>'
    html = re.sub(r'<div class="footer">.*?</div>\s*</div>\s*</div>', footer_html + '\n        </div>', html, count=1, flags=re.DOTALL)

    # Actually, simpler: just replace the footer section only
    # The above regex is fragile. Let me use a marker approach instead.
    # For now, just replace the specific Abu Bakar footer text
    html = html.replace(
        "<em>Maghrib Salah to start 10 minutes after Iftar</em>",
        f"<em>{notes}</em>"
    )

    # Replace radio receiver section
    if not receiver_freq:
        html = re.sub(r'<div style="background: #2c2c6c.*?</div>', '', html, flags=re.DOTALL)
    else:
        html = html.replace("454.40625", receiver_freq)

    # Replace donation section
    if not donation_info:
        html = re.sub(r'<div style="background: #1a1a1a; color: white.*?</div>', '', html, flags=re.DOTALL)
    else:
        html = html.replace(
            '<strong>Cheques/Direct Debits:</strong>\n            Yorkshire Bank | Account No: <strong>18330977</strong> |\n            Sort Code: <strong>05-03-23</strong>',
            donation_info
        )

    # Write output
    out_path = os.path.join(folder, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated: {out_path}")

def main():
    data_files = glob.glob(os.path.join(MASJIDS_DIR, '*', 'data.json'))
    print(f"Found {len(data_files)} data files")
    for df in sorted(data_files):
        try:
            generate(df)
        except Exception as e:
            print(f"ERROR generating {df}: {e}")
    print("Done!")

if __name__ == '__main__':
    main()
