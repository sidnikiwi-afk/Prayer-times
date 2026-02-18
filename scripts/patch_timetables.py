"""
patch_timetables.py — Apply Fixes 4 & 5 to the 10 original hand-crafted mosque pages.

Fix 4: Post-Isha highlight — after Isha Jamaah, Sehri (or Fajr) becomes NEXT (wrap to index 0).
Fix 5: Jamaat-based cutoff — highlight stays on current prayer until AFTER its Jamaah time.

Handles two patterns:
  A) Standard (quba, Almahad, Salahadin, abubakar*, iyma, JamiaMasjid, taqwa, ibrahim):
     Single-line prayers array, same pattern as abubakar template.
  B) Tawakkulia special case: Uses todayData.iftar (sunset) for Maghrib, has separate maghrib jamaah.
  C) Shahjalal: Multi-line format, two arrays (Ramadan + non-Ramadan).

* abubakar already patched directly — included here for verification only.
"""

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Standard replacements (applied to all except Tawakkulia) ---
STANDARD_REPLACEMENTS = [
    # Fix 5: Sehri card changes at Fajr Jamaah (was: sehri begin)
    (
        'eventTime: toDate24(todayData.sehri, false) },',
        'eventTime: toDate24(todayData.jFajr, false) },'
    ),
    # Fix 5: Zohar/Jumu'ah card changes at Zuhr Jamaah (was: zuhr begin)
    (
        'eventTime: toDate24(todayData.zuhr, false) },',
        'eventTime: toDate24(todayData.jZuhr, true) },'
    ),
    # Fix 5: Asr card changes at Asr Jamaah (was: asr begin)
    (
        'eventTime: toDate24(todayData.asr, true) },',
        'eventTime: toDate24(todayData.jAsr, true) },'
    ),
    # Fix 5: Isha card changes at Isha Jamaah (was: isha begin)
    (
        'eventTime: toDate24(todayData.isha, true) }',
        'eventTime: toDate24(todayData.jIsha, true) }'
    ),
]

# --- Shahjalal non-Ramadan Fajr card ---
SHAHJALAL_EXTRA = [
    # Non-Ramadan Fajr card: changes at Fajr Jamaah (was: fajr begin)
    (
        'eventTime: toDate24(todayData.fajr, false) },',
        'eventTime: toDate24(todayData.jFajr, false) },'
    ),
]

# --- Tawakkulia special replacements ---
# Uses todayData.iftar (sunset) for Maghrib mainTime — no jamaah for Maghrib, so eventTime unchanged.
# Only patch Sehri, Zuhr, Asr, Isha.
TAWAKKULIA_REPLACEMENTS = [
    (
        'eventTime: toDate24(todayData.sehri, false) },',
        'eventTime: toDate24(todayData.jFajr, false) },'
    ),
    (
        'eventTime: toDate24(todayData.zuhr, false) },',
        'eventTime: toDate24(todayData.jZuhr, true) },'
    ),
    (
        'eventTime: toDate24(todayData.asr, true) },',
        'eventTime: toDate24(todayData.jAsr, true) },'
    ),
    (
        'eventTime: toDate24(todayData.isha, true) }',
        'eventTime: toDate24(todayData.jIsha, true) }'
    ),
]

# --- Fix 4: Post-Isha wrap — single-line for loop pattern (most mosques) ---
OLD_WRAP_SINGLE = (
    'let nextIndex = -1;\n'
    '            for (let i = 0; i < prayers.length; i++) { if (now < prayers[i].eventTime) { nextIndex = i; break; } }\n'
    '            document.getElementById(\'todayCards\').innerHTML = prayers.map((p, i) => {\n'
    '                const isPassed = nextIndex === -1 || i < nextIndex;\n'
    '                const isNext = i === nextIndex;\n'
    '                let cls = \'prayer-card\';\n'
    '                if (isPassed && nextIndex !== -1) cls += \' passed\';\n'
    '                if (isNext) cls += \' active-prayer\';'
)
NEW_WRAP_SINGLE = (
    'let nextIndex = -1;\n'
    '            for (let i = 0; i < prayers.length; i++) { if (now < prayers[i].eventTime) { nextIndex = i; break; } }\n'
    '            const isWrapped = nextIndex === -1;\n'
    '            if (isWrapped) nextIndex = 0;\n'
    '            document.getElementById(\'todayCards\').innerHTML = prayers.map((p, i) => {\n'
    '                const isPassed = isWrapped ? (i !== 0) : (i < nextIndex);\n'
    '                const isNext = i === nextIndex;\n'
    '                let cls = \'prayer-card\';\n'
    '                if (isPassed) cls += \' passed\';\n'
    '                if (isNext) cls += \' active-prayer\';'
)

# Tawakkulia uses the same single-line for loop pattern
# Shahjalal uses a multi-line for loop:
OLD_WRAP_SHAHJALAL = (
    '            // Find next prayer\n'
    '            let nextIndex = -1;\n'
    '            for (let i = 0; i < prayers.length; i++) {\n'
    '                if (now < prayers[i].eventTime) { nextIndex = i; break; }\n'
    '            }\n'
    '\n'
    '            document.getElementById(\'todayCards\').innerHTML = prayers.map((p, i) => {\n'
    '                const isPassed = nextIndex === -1 || i < nextIndex;\n'
    '                const isNext = i === nextIndex;\n'
    '\n'
    '                let cls = \'prayer-card\';\n'
    '                if (isPassed && nextIndex !== -1) cls += \' passed\';\n'
    '                if (isNext) cls += \' active-prayer\';'
)
NEW_WRAP_SHAHJALAL = (
    '            // Find next prayer\n'
    '            let nextIndex = -1;\n'
    '            for (let i = 0; i < prayers.length; i++) {\n'
    '                if (now < prayers[i].eventTime) { nextIndex = i; break; }\n'
    '            }\n'
    '            const isWrapped = nextIndex === -1;\n'
    '            if (isWrapped) nextIndex = 0;\n'
    '\n'
    '            document.getElementById(\'todayCards\').innerHTML = prayers.map((p, i) => {\n'
    '                const isPassed = isWrapped ? (i !== 0) : (i < nextIndex);\n'
    '                const isNext = i === nextIndex;\n'
    '\n'
    '                let cls = \'prayer-card\';\n'
    '                if (isPassed) cls += \' passed\';\n'
    '                if (isNext) cls += \' active-prayer\';'
)


def patch_file(path, replacements, wrap_old, wrap_new, label=''):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    changes = []
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            changes.append(f'  eventTime fix: {old[:50]}...')
        else:
            print(f'  WARNING: Pattern not found in {label}: {old[:60]}')

    if wrap_old in content:
        content = content.replace(wrap_old, wrap_new)
        changes.append('  post-Isha wrap fix applied')
    else:
        print(f'  WARNING: Wrap pattern not found in {label}')

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'PATCHED: {label} ({len(changes)} changes)')
    else:
        print(f'NO CHANGE: {label} (already patched?)')


mosques = [
    ('quba/index.html',        STANDARD_REPLACEMENTS, OLD_WRAP_SINGLE, NEW_WRAP_SINGLE,       'quba'),
    ('Almahad/index.html',     STANDARD_REPLACEMENTS, OLD_WRAP_SINGLE, NEW_WRAP_SINGLE,       'Almahad'),
    ('Salahadin/index.html',   STANDARD_REPLACEMENTS, OLD_WRAP_SINGLE, NEW_WRAP_SINGLE,       'Salahadin'),
    ('iyma/index.html',        STANDARD_REPLACEMENTS, OLD_WRAP_SINGLE, NEW_WRAP_SINGLE,       'iyma'),
    ('JamiaMasjid/index.html', STANDARD_REPLACEMENTS, OLD_WRAP_SINGLE, NEW_WRAP_SINGLE,       'JamiaMasjid'),
    ('taqwa/index.html',       STANDARD_REPLACEMENTS, OLD_WRAP_SINGLE, NEW_WRAP_SINGLE,       'taqwa'),
    ('ibrahim/index.html',     STANDARD_REPLACEMENTS, OLD_WRAP_SINGLE, NEW_WRAP_SINGLE,       'ibrahim'),
    ('Tawakkulia/index.html',  TAWAKKULIA_REPLACEMENTS, OLD_WRAP_SINGLE, NEW_WRAP_SINGLE,     'Tawakkulia'),
    ('shahjalal/index.html',   STANDARD_REPLACEMENTS + SHAHJALAL_EXTRA, OLD_WRAP_SHAHJALAL, NEW_WRAP_SHAHJALAL, 'shahjalal'),
    # abubakar already patched — verify only
    ('abubakar/index.html',    [], OLD_WRAP_SINGLE, NEW_WRAP_SINGLE,                           'abubakar (verify)'),
]

print('Patching 10 original mosque files...\n')
for rel_path, replacements, wrap_old, wrap_new, label in mosques:
    full_path = os.path.join(BASE, rel_path)
    if not os.path.exists(full_path):
        print(f'MISSING: {full_path}')
        continue
    patch_file(full_path, replacements, wrap_old, wrap_new, label)

print('\nDone.')
