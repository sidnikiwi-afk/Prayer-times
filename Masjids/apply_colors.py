#!/usr/bin/env python3
"""Add color1/color2 to each mosque data.json and update generate.py to use them."""
import json, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')

# 37 unique color pairs per mosque prefix (dark primary, medium secondary)
MOSQUE_COLORS = {
    # Greens
    'alabrar':              ('#1a3a2e', '#2d6a4f'),
    'alhidaya':             ('#1b4a1e', '#2e7d32'),
    'firdaws':              ('#0f3d2e', '#1b6b4a'),
    'ibraheem':             ('#1f3d1a', '#3a7030'),
    'noorulislam':          ('#0a3d30', '#1a6b5a'),
    # Blues
    'alamin':               ('#0a2d6b', '#1a5ab0'),
    'iqra':                 ('#0d2747', '#1565c0'),
    'masjidumar':           ('#0d2045', '#1a3a85'),
    'ahlebayt':             ('#0a2a5e', '#1a4d9c'),
    'abdullahbinmasood':    ('#1a253d', '#2d4070'),
    # Teals/Cyans
    'azharulmadaaris':      ('#00363a', '#006064'),
    'farooqiah':            ('#1c3a47', '#2e6a7a'),
    'masjidnoor':           ('#003d4d', '#006b8a'),
    'shipley':              ('#003d3d', '#006b6b'),
    # Indigos/Deep purples
    'alhidaayah':           ('#1c2c5e', '#3949ab'),
    'masjidhusain':         ('#1a0f5e', '#3025a0'),
    'abbasiya':             ('#1a0f3d', '#332080'),
    'wibseybuttershaw':     ('#1a1530', '#2d2760'),
    'wibsey':               ('#2a1a3d', '#4a306b'),
    # Plums/Magentas
    'nusratul':             ('#3a0a55', '#6b1a9c'),
    'almustaqeem':          ('#4a0d2a', '#8b1a52'),
    'masjidayesha':         ('#4a1a35', '#8b3366'),
    # Reds/Burgundies
    'masjidali':            ('#5c0011', '#9c1928'),
    'raashideen':           ('#3d0a15', '#6d1a28'),
    'doha':                 ('#5c0a2e', '#991f5e'),
    # Oranges/Browns
    'alhikmah':             ('#3d1f00', '#7a3d00'),
    'abuhanifa':            ('#2a1800', '#5c3600'),
    'masjidhamza':          ('#3d1500', '#7a2d00'),
    'darulirfan':           ('#2e1500', '#5c2d00'),
    # Golds/Olives
    'madnimasjid':          ('#3d2800', '#7a5500'),
    'darulmahmood':         ('#2d3a0a', '#4f6b1a'),
    'farooqia':             ('#2a3a00', '#4f7000'),
    # Mauve/Mixed
    'namirah':              ('#3d1a40', '#7a3580'),
    'masjidusman':          ('#1a2020', '#2d4444'),
    'masjidbilal':          ('#0a2e35', '#1a5566'),
    # Remaining
    'baitulilm':            ('#0f2027', '#1a3a5c'),
    'musallasalaam':        ('#1a3020', '#2d5a3a'),
}

ROOT = 'G:/My Drive/Work/Prayer-times'
data_files = sorted(glob.glob(os.path.join(ROOT, 'Masjids', '*', 'data.json')))
updated = 0
skipped = 0

for df in data_files:
    d = json.load(open(df, encoding='utf-8'))
    prefix = d.get('prefix', '')
    if prefix not in MOSQUE_COLORS:
        print(f'  SKIP (no color defined): {prefix}')
        skipped += 1
        continue
    c1, c2 = MOSQUE_COLORS[prefix]
    d['color1'] = c1
    d['color2'] = c2
    with open(df, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    print(f'  {prefix}: {c1} / {c2}')
    updated += 1

print(f'\nDone: {updated} updated, {skipped} skipped')
