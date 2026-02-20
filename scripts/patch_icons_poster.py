#!/usr/bin/env python3
"""Patch original mosque pages: replace emoji icons with mosque silhouette SVG, add poster link."""
import os, re

ROOT = 'G:/My Drive/Work/Prayer-times'
ORIGINALS = ['shahjalal', 'quba', 'Almahad', 'Tawakkulia', 'Salahadin',
             'abubakar', 'iyma', 'JamiaMasjid', 'taqwa', 'ibrahim']

# Mosque silhouette SVG template (use {c} for URL-encoded color like %23004d40)
MOSQUE_ICON = (
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

POSTER_LINK = (
    '            <span style="color: rgba(255,255,255,0.15);">|</span>\n'
    '            <a href="poster.html" target="_blank" style="color: rgba(255,255,255,0.5); '
    'text-decoration: none; margin: 0 10px; transition: color 0.2s;" '
    "onmouseover=\"this.style.color='white'\" onmouseout=\"this.style.color='rgba(255,255,255,0.5)'\">"
    '&#x1F5A8;&#xFE0F; Download QR Poster</a>'
)

for folder in ORIGINALS:
    fpath = os.path.join(ROOT, folder, 'index.html')
    if not os.path.exists(fpath):
        print(f"  SKIP {folder}/")
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    changes = []

    # 1. Replace favicon (emoji text SVG -> mosque silhouette)
    # Pattern: <link rel="icon" href="data:image/svg+xml,...emoji...">
    favicon_pattern = r'<link rel="icon" href="data:image/svg\+xml,[^"]*(?:🌙|🕌)[^"]*">'
    m = re.search(favicon_pattern, content)
    if m:
        # Extract color from apple-touch-icon (more reliable) or default
        color_match = re.search(r"apple-touch-icon.*?fill='(%23[0-9a-fA-F]{6})'", content)
        if color_match:
            color = color_match.group(1)
        else:
            color = '%23004d40'  # fallback
        new_favicon = f'<link rel="icon" href="data:image/svg+xml,{MOSQUE_ICON.format(c=color)}">'
        content = content[:m.start()] + new_favicon + content[m.end():]
        changes.append('favicon')

    # 2. Replace apple-touch-icon (emoji -> mosque silhouette)
    apple_pattern = r'<link rel="apple-touch-icon" href="data:image/svg\+xml,[^"]*(?:🌙|🕌)[^"]*">'
    m = re.search(apple_pattern, content)
    if m:
        color_match = re.search(r"fill='(%23[0-9a-fA-F]{6})'", m.group(0))
        color = color_match.group(1) if color_match else '%23004d40'
        new_apple = f'<link rel="apple-touch-icon" href="data:image/svg+xml,{MOSQUE_ICON.format(c=color)}">'
        content = content[:m.start()] + new_apple + content[m.end():]
        changes.append('apple-touch-icon')

    # 3. Add poster link if not already present
    if 'poster.html' not in content:
        # Find the Report an Error link's closing </a> followed by \n        </div>
        report_pattern = 'Report an Error</a>\n        </div>'
        idx = content.find(report_pattern)
        if idx >= 0:
            insert_at = idx + len('Report an Error</a>')
            content = content[:insert_at] + '\n' + POSTER_LINK + content[insert_at:]
            changes.append('poster-link')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  {folder}/index.html - {', '.join(changes)}")
    else:
        print(f"  {folder}/index.html - no changes needed")

print("\nDone.")
