#!/usr/bin/env python3
"""Rename 'Jamaah' -> "Jama'ah" in user-visible text across all 10 original mosque pages.
Does NOT touch variable names (jFajr, jZuhr, jAsr, jIsha)."""

import os, sys

ROOT = 'G:/My Drive/Work/Prayer-times'
ORIGINALS = ['shahjalal', 'quba', 'Almahad', 'Tawakkulia', 'Salahadin',
             'abubakar', 'iyma', 'JamiaMasjid', 'taqwa', 'ibrahim']

# Replacements: (old, new) — order matters (longer matches first)
REPLACEMENTS = [
    ("Fajr Jamaah", "Fajr Jama\\'ah"),
    ("Zohar Jamaah", "Zohar Jama\\'ah"),
    ("Zuhr Jamaah", "Zuhr Jama\\'ah"),
    ("Asr Jamaah", "Asr Jama\\'ah"),
    ("Isha Jamaah", "Isha Jama\\'ah"),
    # Standalone label in single-quoted JS: {label:'Jamaah', or { label: 'Jamaah',
    ("{label:'Jamaah',", "{label:'Jama\\'ah',"),
    ("{ label: 'Jamaah',", "{ label: 'Jama\\'ah',"),
    # Template literal contexts (no escaping needed)
    ("Jamaah changes:", "Jama'ah changes:"),
    ("Jamaah changes tomorrow:", "Jama'ah changes tomorrow:"),
    # Comment text
    ("// After Isha Jamaah", "// After Isha Jama'ah"),
]

total_changes = 0

for folder in ORIGINALS:
    fpath = os.path.join(ROOT, folder, 'index.html')
    if not os.path.exists(fpath):
        print(f"  SKIP {folder}/ (not found)")
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)

    changes = 0
    for i, (a, b) in enumerate(zip(original, content)):
        if a != b:
            changes += 1

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        # Count actual replacements
        count = sum(original.count(old) for old, new in REPLACEMENTS)
        print(f"  {folder}/index.html - {count} replacements")
        total_changes += count
    else:
        print(f"  {folder}/index.html - no changes needed")

print(f"\nDone: {total_changes} total replacements across {len(ORIGINALS)} mosques")
