#!/usr/bin/env python3
"""Update landing page card colors to match each mosque's theme color."""
import json, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = 'G:/My Drive/Work/Prayer-times'
landing = os.path.join(ROOT, 'index.html')
SKIP = {'masjidtaqwa'}

with open(landing, encoding='utf-8') as f:
    html = f.read()

data_files = sorted(glob.glob(os.path.join(ROOT, 'Masjids', '*', 'data.json')))
updated = 0

for df in data_files:
    d = json.load(open(df, encoding='utf-8'))
    prefix = d.get('prefix', '')
    c1 = d.get('color1', '')
    c2 = d.get('color2', '')
    if not prefix or not c1 or prefix in SKIP:
        continue

    # Find the card for this prefix and update its gradient
    # Card format: href="{prefix}/" ... background: linear-gradient(to bottom, #XXXXXX, #XXXXXX)
    import re
    # Match the card's color div for this specific mosque
    pattern = rf'(<a href="{re.escape(prefix)}/"[^>]*>.*?<div class="card-colour" style="background: linear-gradient\(to bottom, )#[0-9a-fA-F]{{6}}(, )#[0-9a-fA-F]{{6}}(\);)'
    replacement = rf'\g<1>{c1}\g<2>{c2}\g<3>'
    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    if new_html != html:
        html = new_html
        updated += 1
    else:
        print(f'  WARNING: card not found for {prefix}')

with open(landing, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Updated {updated} card colors in index.html')
