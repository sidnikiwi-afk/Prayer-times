#!/usr/bin/env python3
import json, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = 'G:/My Drive/Work/Prayer-times'
MASJIDS_DIR = os.path.join(ROOT, 'Masjids')
EXISTING_ADDRESSES = {'807 Great Horton Road'}
EXISTING_PREFIXES = {'shahjalal','quba','almahad','tawakkulia','salahadin','abubakar','iyma','JamiaMasjid','taqwa'}
COLOR1 = '#4a148c'
COLOR2 = '#7b1fa2'

data_files = sorted(glob.glob(os.path.join(MASJIDS_DIR, '*', 'data.json')))
count = 0

for df in data_files:
    d = json.load(open(df, encoding='utf-8'))
    prefix = d.get('prefix', '')
    name = d['name']
    address = d.get('address', '')
    short_name = d.get('short_name', name)
    phone = d.get('phone', '')

    if prefix in EXISTING_PREFIXES or any(ea in address for ea in EXISTING_ADDRESSES):
        continue

    target_dir = os.path.join(ROOT, prefix)
    if not os.path.isdir(target_dir):
        continue

    # manifest.json
    manifest = {
        "name": f"{name} - Ramadan Timetable",
        "short_name": f"{short_name} Times",
        "description": f"Ramadan 1447 prayer timetable for {name}, Bradford",
        "start_url": f"/{prefix}/",
        "display": "standalone",
        "background_color": COLOR1,
        "theme_color": COLOR1,
        "icons": [{
            "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect fill='%234a148c' width='100' height='100' rx='20'/><text x='50' y='50' text-anchor='middle' dominant-baseline='central' font-size='60'>\U0001f319</text></svg>",
            "sizes": "any",
            "type": "image/svg+xml"
        }]
    }
    with open(os.path.join(target_dir, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # sw.js
    sw_lines = [
        f"const CACHE_NAME = 'ramadan-timetable-v5';",
        f"const ASSETS = [",
        f"  '/{prefix}/',",
        f"  '/{prefix}/index.html',",
        f"  '/{prefix}/manifest.json',",
        f"  'https://cdn.jsdelivr.net/npm/granim@2.0.0/dist/granim.min.js'",
        f"];",
        "",
        "self.addEventListener('install', event => {",
        "  event.waitUntil(",
        "    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))",
        "  );",
        "  self.skipWaiting();",
        "});",
        "",
        "self.addEventListener('activate', event => {",
        "  event.waitUntil(",
        "    caches.keys().then(keys =>",
        "      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))",
        "    )",
        "  );",
        "  self.clients.claim();",
        "});",
        "",
        "self.addEventListener('fetch', event => {",
        "  event.respondWith(",
        "    fetch(event.request)",
        "      .then(response => {",
        "        const clone = response.clone();",
        "        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));",
        "        return response;",
        "      })",
        "      .catch(() => caches.match(event.request))",
        "  );",
        "});",
    ]
    with open(os.path.join(target_dir, 'sw.js'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(sw_lines))

    # og-image.svg
    name_upper = name.upper().replace('&', '&amp;')
    addr_esc = address.replace('&', '&amp;')[:65]
    og_lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">',
        '  <defs>',
        '    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'      <stop offset="0%" style="stop-color:{COLOR1}"/>',
        f'      <stop offset="100%" style="stop-color:{COLOR2}"/>',
        '    </linearGradient>',
        '  </defs>',
        '  <rect width="1200" height="630" fill="url(#bg)"/>',
        '  <text x="600" y="200" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="100" fill="white">&#x1F54C;</text>',
        f'  <text x="600" y="320" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="40" font-weight="bold" fill="white" letter-spacing="2">{name_upper}</text>',
        f'  <text x="600" y="390" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="26" fill="white" opacity="0.9">{addr_esc}</text>',
        '  <text x="600" y="470" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="34" font-weight="600" fill="white">',
        '    <tspan fill="#ffc107">RAMADHAN 1447</tspan> | FEBRUARY - MARCH 2026',
        '  </text>',
        '  <text x="600" y="540" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="24" fill="white" opacity="0.8" font-style="italic">Prayer Timetable with Live Countdown</text>',
        '</svg>',
    ]
    with open(os.path.join(target_dir, 'og-image.svg'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(og_lines))

    # poster.html
    phone_line = f'<div class="contact">Tel: {phone}</div>' if phone else ''
    name_html = name.replace('&', '&amp;')
    addr_html = address.replace('&', '&amp;')
    poster_lines = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'    <title>{name_html} - QR Poster</title>',
        '    <style>',
        '        @page { size: A4; margin: 0; }',
        '        * { margin: 0; padding: 0; box-sizing: border-box; }',
        '        body { font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; width: 210mm; height: 297mm; margin: 0 auto; background: white; display: flex; flex-direction: column; align-items: center; }',
        '        .poster { width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; padding: 20mm 15mm; }',
        f'        .banner {{ width: 100%; background: linear-gradient(135deg, {COLOR1} 0%, {COLOR2} 100%); border-radius: 16px; padding: 25px 30px; text-align: center; color: white; margin-bottom: 15mm; }}',
        '        .mosque-icon { font-size: 60px; margin-bottom: 10px; }',
        '        .banner h1 { font-size: 24px; letter-spacing: 2px; margin-bottom: 6px; }',
        '        .banner .address { font-size: 13px; opacity: 0.9; margin-bottom: 10px; }',
        '        .banner .month { font-size: 20px; font-weight: 600; background: rgba(255,255,255,0.2); padding: 6px 20px; border-radius: 25px; display: inline-block; }',
        '        .scan-prompt { text-align: center; margin-bottom: 10mm; }',
        f'        .scan-prompt h2 {{ font-size: 32px; color: {COLOR1}; margin-bottom: 5px; }}',
        '        .scan-prompt p { font-size: 18px; color: #555; }',
        f'        .qr-wrapper {{ background: white; border: 4px solid {COLOR1}; border-radius: 20px; padding: 20px; margin-bottom: 10mm; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}',
        '        .qr-wrapper img, .qr-wrapper svg { width: 70mm; height: 70mm; }',
        '        .url-box { background: #f5f5f5; border: 2px solid #ddd; border-radius: 12px; padding: 12px 30px; margin-bottom: 10mm; }',
        f'        .url-box code {{ font-size: 14px; color: {COLOR1}; font-weight: 600; letter-spacing: 0.5px; }}',
        '        .features { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; margin-bottom: 12mm; }',
        '        .feature { text-align: center; padding: 12px 18px; background: #f3e5f5; border-radius: 12px; min-width: 130px; }',
        '        .feature-icon { font-size: 28px; margin-bottom: 5px; }',
        '        .feature-text { font-size: 12px; color: #333; font-weight: 500; }',
        '        .footer { margin-top: auto; text-align: center; width: 100%; }',
        f'        .footer-divider {{ width: 60%; height: 2px; background: linear-gradient(90deg, transparent, {COLOR1}, transparent); margin: 0 auto 15px; }}',
        '        .footer p { font-size: 13px; color: #888; }',
        '        .footer .contact { font-size: 15px; color: #1a1a1a; font-weight: 600; margin-top: 5px; }',
        '        @media print { body { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }',
        '    </style>',
        '</head>',
        '<body>',
        '    <div class="poster">',
        '        <div class="banner">',
        '            <div class="mosque-icon">&#x1F54C;</div>',
        f'            <h1>{name_html.upper()}</h1>',
        f'            <div class="address">{addr_html}</div>',
        '            <div class="month">RAMADHAN 1447 | FEBRUARY - MARCH 2026</div>',
        '        </div>',
        '        <div class="scan-prompt">',
        '            <h2>Scan for Prayer Timetable</h2>',
        '            <p>View Sehri &amp; Iftar times with live countdown on your phone</p>',
        '        </div>',
        '        <div class="qr-wrapper">',
        '            <div style="width:70mm;height:70mm;display:flex;align-items:center;justify-content:center;font-size:14px;color:#999;border:2px dashed #ccc;border-radius:10px;">QR code will be generated</div>',
        '        </div>',
        '        <div class="url-box">',
        f'            <code>waqt.uk/{prefix}</code>',
        '        </div>',
        '        <div class="features">',
        '            <div class="feature"><div class="feature-icon">&#x23F0;</div><div class="feature-text">Live Sehri &amp;<br>Iftar Countdown</div></div>',
        '            <div class="feature"><div class="feature-icon">&#x1F319;</div><div class="feature-text">Full Ramadan<br>Timetable</div></div>',
        '            <div class="feature"><div class="feature-icon">&#x1F514;</div><div class="feature-text">Sehri &amp; Iftar<br>Reminders</div></div>',
        '            <div class="feature"><div class="feature-icon">&#x1F4F1;</div><div class="feature-text">Works on<br>Any Phone</div></div>',
        '        </div>',
        '        <div class="footer">',
        '            <div class="footer-divider"></div>',
        f'            <p>{name_html} | {addr_html}</p>',
        f'            {phone_line}',
        '        </div>',
        '    </div>',
        '</body>',
        '</html>',
    ]
    with open(os.path.join(target_dir, 'poster.html'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(poster_lines))

    count += 1
    print(f'  {prefix}/')

print(f'\nDone: {count} mosques x 4 files = {count*4} files generated')
