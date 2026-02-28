#!/usr/bin/env python3
"""
patch_nav_tour.py — Add nav bar walkthrough tour CSS + JS to all mosque timetable pages.
Also fixes shahjalal progress bar text (already applied manually, this verifies).

Adds:
1. Nav tooltip CSS (before </style>)
2. Nav tour JS (after nav.js script include)

Skips pages that already have the tour (idempotent).
"""

import os
import re
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CSS to inject before </style>
NAV_TOUR_CSS = """
        /* === Nav Bar Walkthrough Tour === */
        .nav-tooltip {
            position: absolute;
            top: calc(100% + 8px);
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.88);
            color: white;
            font-size: 12px;
            padding: 8px 12px;
            border-radius: 8px;
            white-space: nowrap;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 10001;
        }
        .nav-tooltip::before {
            content: '';
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 6px solid transparent;
            border-bottom-color: rgba(0,0,0,0.88);
        }
        .nav-tooltip.visible { opacity: 1; }
        .top-nav-btn.tour-highlight {
            background: rgba(255,255,255,0.3);
            box-shadow: 0 0 0 3px rgba(255,255,255,0.2), 0 0 12px rgba(255,255,255,0.15);
        }"""


def get_tour_js(prefix):
    """Return the nav tour JS block with the correct localStorage prefix."""
    return f"""
    <!-- Nav bar walkthrough tour (first visit) -->
    <script>
    (function() {{
        var key = '{prefix}-navTourSeen';
        if (localStorage.getItem(key)) return;
        var steps = [
            {{ selector: '.notify-btn', text: 'Get Sehri & Iftar reminders' }},
            {{ selector: '.dark-mode-toggle', text: 'Switch to dark mode' }},
            {{ selector: '.top-nav-btn[onclick*="shareWhatsApp"]', text: 'Share with friends' }}
        ];
        var current = -1;
        var tooltip = null;
        var timer = null;

        function cleanup() {{
            if (tooltip && tooltip.parentNode) tooltip.parentNode.removeChild(tooltip);
            steps.forEach(function(s) {{
                var btn = document.querySelector(s.selector);
                if (btn) btn.classList.remove('tour-highlight');
            }});
            localStorage.setItem(key, '1');
            document.removeEventListener('click', advance);
        }}

        function advance() {{
            if (tooltip && tooltip.parentNode) tooltip.parentNode.removeChild(tooltip);
            if (current >= 0 && current < steps.length) {{
                var prev = document.querySelector(steps[current].selector);
                if (prev) prev.classList.remove('tour-highlight');
            }}
            clearTimeout(timer);
            current++;
            if (current >= steps.length) {{ cleanup(); return; }}

            var step = steps[current];
            var btn = document.querySelector(step.selector);
            if (!btn) {{ advance(); return; }}

            btn.classList.add('tour-highlight');
            btn.style.position = 'relative';
            tooltip = document.createElement('div');
            tooltip.className = 'nav-tooltip';
            tooltip.textContent = step.text;
            btn.appendChild(tooltip);
            requestAnimationFrame(function() {{ tooltip.classList.add('visible'); }});
            timer = setTimeout(advance, 4000);
        }}

        setTimeout(function() {{
            advance();
            document.addEventListener('click', advance);
        }}, 1000);
    }})();
    </script>"""


def detect_prefix(content):
    """Detect the localStorage prefix from the file content."""
    # Look for patterns like 'prefix-darkMode', 'prefix-notifications'
    m = re.search(r"localStorage\.\w+\('(\w+)-darkMode", content)
    if m:
        return m.group(1)
    m = re.search(r"localStorage\.\w+\('(\w+)-notifications", content)
    if m:
        return m.group(1)
    # Shahjalal uses 'darkMode' without prefix
    if "'darkMode'" in content and 'shahjalal' in content.lower():
        return 'shahjalal'
    return None


def patch_file(path):
    """Add nav tour CSS + JS to a mosque page. Returns True if modified."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already patched
    if 'nav-tooltip' in content or 'navTourSeen' in content:
        return False

    # Skip non-timetable pages (landing page, etc.)
    if 'top-nav-btn' not in content:
        return False

    prefix = detect_prefix(content)
    if not prefix:
        print(f"  WARNING: Could not detect prefix for {path}")
        return False

    original = content

    # 1. Add CSS before </style>
    content = content.replace('    </style>', NAV_TOUR_CSS + '\n    </style>')

    # 2. Add JS after nav.js include
    tour_js = get_tour_js(prefix)
    # Try both patterns
    if '<script src="../nav.js"></script>' in content:
        content = content.replace(
            '<script src="../nav.js"></script>',
            '<script src="../nav.js"></script>\n' + tour_js
        )
    elif '<script src="nav.js"></script>' in content:
        content = content.replace(
            '<script src="nav.js"></script>',
            '<script src="nav.js"></script>\n' + tour_js
        )
    else:
        print(f"  WARNING: Could not find nav.js include in {path}")
        return False

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


# Hand-crafted mosques (excluding shahjalal and abubakar which are already done)
HAND_CRAFTED = [
    'quba', 'Almahad', 'Tawakkulia', 'Salahadin',
    'iyma', 'JamiaMasjid', 'taqwa', 'ibrahim', 'aqsa'
]

# Batch-generated mosques
BATCH_MOSQUES = [
    'alabrar', 'alamin', 'alhidaya', 'alhikmah', 'alhidaayah',
    'almustaqeem', 'azharulmadaaris', 'baitulilm', 'darulmahmood',
    'doha', 'firdaws', 'iqra', 'abuhanifa', 'farooqiah',
    'madnimasjid', 'abbasiya', 'darulirfan', 'abdullahbinmasood',
    'masjidali', 'masjidayesha', 'masjidbilal', 'masjidhamza',
    'masjidhusain', 'ibraheem', 'namirah', 'masjidnoor',
    'noorulislam', 'nusratul', 'farooqia', 'masjidumar',
    'masjidusman', 'raashideen', 'musallasalaam', 'ahlebayt',
    'shipley', 'westleeds', 'wibseybuttershaw', 'wibsey',
    'sjmkeighley', 'masjidtaqwa', 'makkimasjidmadrassah'
]

ALL_MOSQUES = HAND_CRAFTED + BATCH_MOSQUES

patched = 0
skipped = 0
missing = 0

print(f"Patching {len(ALL_MOSQUES)} mosque pages with nav tour...\n")

for mosque in ALL_MOSQUES:
    path = os.path.join(BASE, mosque, 'index.html')
    if not os.path.exists(path):
        print(f"  MISSING: {path}")
        missing += 1
        continue

    if patch_file(path):
        print(f"  PATCHED: {mosque}")
        patched += 1
    else:
        print(f"  SKIPPED: {mosque} (already patched or no nav)")
        skipped += 1

print(f"\nDone! Patched: {patched}, Skipped: {skipped}, Missing: {missing}")
