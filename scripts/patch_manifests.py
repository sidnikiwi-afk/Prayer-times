#!/usr/bin/env python3
"""Update manifest.json icons for original mosques to use mosque silhouette SVG."""
import json, os

ROOT = 'G:/My Drive/Work/Prayer-times'

# Original mosques with their theme colors
ORIGINALS = {
    'shahjalal': '#004d40',
    'quba': '#1a5a7e',
    'Almahad': '#1b5e20',
    'Tawakkulia': '#1a237e',
    'Salahadin': '#6a1b34',
    'abubakar': '#4a148c',
    'iyma': '#006064',
    'JamiaMasjid': '#0d1b2a',
    'taqwa': '#0d47a1',
    'ibrahim': '#bf360c',
}

MOSQUE_ICON_TEMPLATE = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
    "<rect fill='{c}' width='100' height='100' rx='20'/>"
    "<path d='M30 55 Q50 20 70 55 Z' fill='white' opacity='0.95'/>"
    "<rect x='22' y='35' width='6' height='40' rx='1' fill='white' opacity='0.9'/>"
    "<polygon points='22,35 25,25 28,35' fill='white' opacity='0.9'/>"
    "<rect x='72' y='35' width='6' height='40' rx='1' fill='white' opacity='0.9'/>"
    "<polygon points='72,35 75,25 78,35' fill='white' opacity='0.9'/>"
    "<rect x='30' y='55' width='40' height='20' fill='white' opacity='0.9'/>"
    "<path d='M44 75 L44 62 Q50 56 56 62 L56 75 Z' fill='{c}' opacity='0.8'/>"
    "<circle cx='50' cy='28' r='5' fill='white'/>"
    "<circle cx='52' cy='27' r='4' fill='{c}'/>"
    "</svg>"
)

for folder, color in ORIGINALS.items():
    mpath = os.path.join(ROOT, folder, 'manifest.json')
    if not os.path.exists(mpath):
        print(f"  SKIP {folder}/ (no manifest.json)")
        continue

    with open(mpath, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    c_uri = color.replace('#', '%23')
    icon_svg = MOSQUE_ICON_TEMPLATE.format(c=c_uri)
    new_icon_src = f"data:image/svg+xml,{icon_svg}"

    if manifest.get('icons') and manifest['icons'][0].get('src') != new_icon_src:
        manifest['icons'] = [{
            "src": new_icon_src,
            "sizes": "any",
            "type": "image/svg+xml"
        }]
        with open(mpath, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"  {folder}/manifest.json - updated")
    else:
        print(f"  {folder}/manifest.json - no change needed")

print("\nDone.")
