# Prayer-times Project

## Overview
Ramadan 1447 (Feb-Mar 2026) interactive prayer timetables for mosques in Bradford.
Hosted on GitHub Pages. Each mosque gets its own subfolder with a self-contained HTML page.

- **Repo**: https://github.com/sidnikiwi-afk/Prayer-times
- **Live**: https://waqt.uk/
- **Domain**: `waqt.uk` (Namecheap, DNS → GitHub Pages)
- **GitHub account**: sidnikiwi-afk

## File Structure
```
Prayer-times/
├── index.html              # Landing page - mosque selector (waqt.uk)
├── nav.js                  # Shared navigation dropdown (edit MASJIDS array here)
├── CNAME                   # Custom domain config (waqt.uk)
├── CLAUDE.md               # This file - project documentation
├── widget.js               # Scriptable iOS home screen widget
├── chat.js                 # AI prayer times chatbot + GA4 analytics (loaded on all pages)
├── .gitignore
├── shahjalal/
│   ├── index.html          # Shahjalal Islamic Society timetable
│   ├── manifest.json       # PWA manifest
│   ├── sw.js               # Service worker (offline support)
│   ├── og-image.svg        # Social preview image
│   ├── qr-code.svg         # QR code for poster
│   └── poster.html         # A4 printable QR poster
├── quba/
│   ├── index.html          # Masjid Quba timetable
│   ├── manifest.json       # PWA manifest
│   ├── sw.js               # Service worker (offline support)
│   ├── og-image.svg        # Social preview image
│   ├── qr-code.svg         # QR code for poster
│   └── poster.html         # A4 printable QR poster
├── Almahad/
│   ├── index.html          # Al Mahad Ul Islami timetable
│   ├── manifest.json       # PWA manifest
│   ├── sw.js               # Service worker (offline support)
│   ├── og-image.svg        # Social preview image
│   ├── qr-code.svg         # QR code for poster
│   └── poster.html         # A4 printable QR poster
├── Tawakkulia/
│   ├── index.html          # Tawakkulia Islamic Society timetable
│   ├── ramadan_timetable.json # Source timetable data (JSON)
│   ├── manifest.json       # PWA manifest
│   ├── sw.js               # Service worker (offline support)
│   ├── og-image.svg        # Social preview image
│   ├── qr-code.svg         # QR code for poster
│   └── poster.html         # A4 printable QR poster
├── Salahadin/
│   ├── index.html          # Salahadin Mosque timetable
│   ├── manifest.json       # PWA manifest
│   ├── sw.js               # Service worker (offline support)
│   ├── og-image.svg        # Social preview image
│   ├── qr-code.svg         # QR code for poster
│   └── poster.html         # A4 printable QR poster
├── abubakar/
│   ├── index.html          # Masjid Abu Bakar timetable
│   ├── manifest.json       # PWA manifest
│   ├── sw.js               # Service worker (offline support)
│   ├── og-image.svg        # Social preview image
│   ├── qr-code.svg         # QR code for poster
│   └── poster.html         # A4 printable QR poster
├── iyma/
│   ├── index.html          # IYMA timetable
│   ├── manifest.json       # PWA manifest
│   ├── sw.js               # Service worker (offline support)
│   ├── og-image.svg        # Social preview image
│   ├── qr-code.svg         # QR code for poster
│   └── poster.html         # A4 printable QR poster
├── JamiaMasjid/
│   ├── index.html          # Jamia Masjid timetable
│   ├── manifest.json       # PWA manifest
│   ├── sw.js               # Service worker (offline support)
│   ├── og-image.svg        # Social preview image
│   ├── qr-code.svg         # QR code for poster
│   └── poster.html         # A4 printable QR poster
└── taqwa/
    ├── index.html          # Masjid Taqwa timetable
    ├── manifest.json       # PWA manifest
    ├── sw.js               # Service worker (offline support)
    ├── og-image.svg        # Social preview image
    ├── qr-code.svg         # QR code for poster
    └── poster.html         # A4 printable QR poster
└── ibrahim/
    ├── index.html          # Masjid Ibraheem (Leeds) timetable
    ├── manifest.json       # PWA manifest
    ├── sw.js               # Service worker (offline support)
    ├── og-image.svg        # Social preview image
    ├── qr-code.svg         # QR code for poster
    └── poster.html         # A4 printable QR poster
# ... plus 38 batch-generated mosque folders (alabrar/, alamin/, alhidaya/, westleeds/, etc.)
# See "Batch Mosque Generation" section below for the full list and workflow.
scripts/
└── patch_timetables.py     # Applies Fixes 4 & 5 to 10 original hand-crafted mosque pages
Masjids/                    # Source data for batch-generated mosques
├── generate.py             # Batch HTML generator (uses abubakar/ as template, applies colors)
├── gen_pwa.py              # Batch PWA asset generator (manifest, sw, og-image, poster)
├── apply_colors.py         # Assigns color1/color2 to each data.json
├── update_landing.py       # Updates landing page card gradients to match mosque colors
├── validate.py             # Data validation script (row count, dates, times)
└── <Mosque Name>/
    └── data.json           # Per-mosque config, timetable data, and color1/color2
```

## Mosques

| Mosque | Folder | Address | Theme Colors | Eid Salah | Fitrana |
|--------|--------|---------|-------------|-----------|--------|
| Shahjalal Islamic Society | `shahjalal` | 149A Little Horton Lane, BD5 0HS | Teal `#004d40` / `#00796b` | 6:24am + 9:00am | £5.00 |
| Masjid Quba | `quba` | 20 Quba Court, BD8 7LA | Blue `#1a5a7e` / `#2a8ab5` | 8:00am | £5.00 |
| Al Mahad Ul Islami | `Almahad` | Dorset Street, BD5 0LT | Green `#1b5e20` / `#388e3c` | 9:00am | £5.00 |
| Tawakkulia Islamic Society | `Tawakkulia` | 48 Cornwall Road, BD8 7JN | Indigo `#1a237e` / `#3949ab` | 7:00am, 8:30am, 10:00am | £4.80 |
| Salahadin Mosque | `Salahadin` | 62 Little Horton Lane, BD5 0BS | Burgundy `#6a1b34` / `#9c2759` | TBA | £5.00 |
| Masjid Abu Bakar | `abubakar` | 38 Steadman Terrace, BD3 9NB | Purple `#4a148c` / `#7b1fa2` | — | — |
| IYMA | `iyma` | 68 Idle Road, BD2 4NH | Dark Cyan `#006064` / `#00838f` | 9:00am | £5.00 |
| Jamia Masjid | `JamiaMasjid` | 28-32 Howard St, BD5 0BP | Navy `#0d1b2a` / `#1b3a5c` | TBA | TBA |
| Masjid Taqwa | `taqwa` | 807 Great Horton Road, BD7 4AG | Cobalt Blue `#0d47a1` / `#1976d2` | 6:30am, 9:30am | £5.00 |
| Masjid Ibraheem | `ibrahim` | 4 Woodview Rd, Beeston, Leeds LS11 6LE | Deep Orange `#bf360c` / `#e64a19` | 9:00am (Men), 10:30am (Men & Women) | £5.00 |

### Donation Details
- **Shahjalal**: Not listed in timetable
- **Quba**: Madressa Islamia Talimuddin, Barclays, Sort: 20-11-81, Acc: 90803383
- **Almahad**: Al Mahadul Islami, Sort: 20-76-92, Acc: 13161595
- **Tawakkulia**: Tawakkulia Jami Masjid, Sort: 56-00-36, Acc: 42345499
- **Salahadin**: Barclays Bank, Sort: 20-11-88, Acc: 83561801
- **Abu Bakar**: Yorkshire Bank, Acc: 18330977, Sort: 05-03-23
- **IYMA**: Imam Yusuf Motala Academy, Yorkshire Bank, Sort: 05-03-03, Acc: 71398073
- **Jamia Masjid**: TBA
- **Masjid Taqwa**: Acc: 34495853, Sort: 40-13-15
- **Masjid Ibraheem**: Acc: 80015318, Sort: 40-27-41 | pay.easydonate.uk/masjidibraheem

### Contact / Radio
- **Quba**: Tel 01274 542027 | masjidquba.org | Receiver: 454.3500
- **Almahad**: Receiver: 456.62500
- **Tawakkulia**: Tel 01274 734563 | tawakkulia.com | tjmasjid@outlook.com | Receiver: 455-650
- **Abu Bakar**: Tel 01274 668343 | Receiver: 454.40625
- **IYMA**: Tel 07771 635 480 | info@iyma.org.uk | www.iyma.org.uk
- **Jamia Masjid**: Tel 01274 724 819
- **Masjid Taqwa**: www.masjidat-taqwa.co.uk | Receiver: 456.787
- **Masjid Ibraheem**: Tel 0113 270 9536 | masjidibraheemleeds.com | masjidibraheemleeds11@gmail.com
- **West Leeds Jamia Masjid**: Tel 07801 997 364 | westleedsjamiamasjid@gmail.com

### Batch-Generated Mosques (Ramadan 1447 – added Feb 2026)

These 38 mosques were added in bulk using the `Masjids/` batch generation workflow.
Each has a **unique color theme** stored in `color1`/`color2` fields of its `data.json` — all 10 purple shades from the abubakar template are fully replaced with per-mosque derived colors (dark, medium, light variants, tints).
Source data in `Masjids/<Name>/data.json`. Regenerate with `python Masjids/generate.py` then copy outputs.

| Mosque | Folder | Address | Theme |
|--------|--------|---------|-------|
| Al Abrar Academy | `alabrar` | 10-20 Heap Lane, Bradford, BD3 0DT | Emerald green |
| Al Amin Islamic Society / Jamia Masjid & Madrasa | `alamin` | Kensington Street, Keighley, BD21 1HZ | Royal blue |
| Al Hidaya Academy | `alhidaya` | Chapel Lane (Off Highgate Road), Queensbury, BD13 1EG | Forest green |
| Masjid Al Hikmah & Learning Centre | `alhikmah` | 181A Barkerend Rd, Bradford, BD3 9AP | Dark amber |
| Al-Hidaayah Foundation | `alhidaayah` | Bridge Street, Keighley, BD21 1AA | Slate indigo |
| Al-Mustaqeem Education and Community Centre | `almustaqeem` | 4 Central Avenue, Bradford, BD5 0PB | Deep magenta |
| Azharul Madaaris | `azharulmadaaris` | 102 Princeville Road, Lidget Green, Bradford, BD7 2AR | Dark teal |
| Madrasah Baitul Ilm | `baitulilm` | 4 St Johns Court, Square Street, Bradford, BD4 7NP | Midnight navy |
| Darul Mahmood | `darulmahmood` | 21 St. Mary's Road, Bradford, BD8 7LR | Olive |
| Doha Mosque | `doha` | 13-15 Claremont, Bradford, BD7 1BG | Qatar maroon |
| Firdaws Islamic Centre / Firdaws Mosque | `firdaws` | Males: Guy Street; Females: 75 Edward Street, Bradford, BD4 7BB | Jade green |
| Iqra Masjid | `iqra` | Off Farriers Croft, King's Road, Bradford, BD2 1ET | Sapphire blue |
| Jamia Abu Hanifa Madrassa | `abuhanifa` | 35 Hustler Street, Undercliffe, BD3 0PS | Dark tan |
| Jamiah Farooqiah | `farooqiah` | 432 Barkerend Road, Bradford, BD3 8QJ | Steel teal |
| Madni Masjid (West Bowling Islamic Society) | `madnimasjid` | 133 Newton Street, BD5 7BJ | Dark gold |
| Madrasa Abbasiya | `abbasiya` | 1D Moor Park Drive, Bradford, BD3 7ER | Deep violet |
| Markazi Masjid Darul Irfan | `darulirfan` | 1 Little Cross St, BD5 8AD | Rust |
| Masjid Abdullah-bin-Masood | `abdullahbinmasood` | 14 Lynthorne Road, Frizinghall, Bradford | Slate blue |
| Masjid Ali | `masjidali` | 228 Parkside Road, Bradford, BD5 8PW | Crimson |
| Masjid Ayesha | `masjidayesha` | 2 Thornacre Road, Manningham, BD18 1JY | Rose |
| Masjid Bilal | `masjidbilal` | 1-3 Drummond Rd, Bradford, BD8 8DA | Petrol |
| Masjid Hamza | `masjidhamza` | 42 Woodview Terrace, BD8 7AH | Burnt sienna |
| Masjid Husain | `masjidhusain` | 203 Allerton Road, BD15 7RD | Deep indigo |
| Masjid Ibraheem & Education Centre | `ibraheem` | Lower Rushton Road, Bradford, BD3 8PX | Sage green |
| Masjid Namirah / Madrasah Ta'limul Quran | `namirah` | 8-10 Hanover Square, Bradford, BD1 3BY | Dark mauve |
| Masjid Noor | `masjidnoor` | 62 Toller Lane, Bradford, BD8 9DA | Dark cyan |
| Masjid Noorul Islam | `noorulislam` | 58-62 St Margaret's Road, Bradford, BD7 3AE | Forest teal |
| Nusrat-ul-Islam Masjid | `nusratul` | Preston Street, Bradford, BD7 1DD | Plum |
| Khanqah Naqshbandia Masjid Farooqia | `farooqia` | 28 Gondal Court, Bradford, BD5 9JW | Dark olive |
| Masjid-e-Umar | `masjidumar` | 184 Durham Road, Bradford, BD8 9HU | Navy blue |
| Masjid-e-Usman / Madrassa Khaliliya | `masjidusman` | 57 Upper Seymour St, Bradford, BD3 9LJ | Slate |
| Masjidur Raashideen | `raashideen` | 14 Farfield Street, Bradford, BD9 5AS | Dark burgundy |
| Musalla Salaam | `musallasalaam` | 191 Pasture Lane, Clayton, Bradford, BD7 2SQ | Woodland |
| PYC Masjid Ahle Bayt | `ahlebayt` | Mount Street, Bradford, BD3 9SR | Islamic blue |
| Shipley Islamic & Education Centre | `shipley` | Aireville Road, Bradford, BD9 4HH | Teal |
| Wibsey & Buttershaw Islamic Learning Centre | `wibseybuttershaw` | The Cooperville Centre, Bellerby Brow, Bradford, BD6 3JY | Purple-navy |
| West Leeds Jamia Masjid | `westleeds` | Town Street, Armley, Leeds, LS12 3JG | Charcoal/Graphite |
| Wibsey Musalla | `wibsey` | 75 Odsal Road, Wibsey, BD6 1PN | Purple-grey |

**Note on Doha Mosque**: Timetable has 29 rows starting Feb 19 (their confirmed Ramadan start date differs by one day — moon sighted a day later).

## Features (All Mosques)

### Core Functionality
- **Today View**: Card-based layout showing today's prayer times only, with pill toggle to switch to Full Timetable. Passed prayers dimmed with checkmark, next prayer highlighted with accent border + "NEXT" badge. Highlight cutoff uses Jamaah times (e.g. Sehri stays highlighted until Fajr Jamaah, Zohar until Zuhr Jamaah, Asr until Asr Jamaah, Isha until Isha Jamaah). Post-Isha wrap: after Isha Jamaah passes, wraps to index 0 so Sehri/Fajr shows as NEXT instead of all prayers going grey (uses `isWrapped` variable). Tomorrow preview at bottom: during Ramadan shows Sehri/Iftar times + any jamaah changes; outside Ramadan shows jamaah changes only (hidden if none). Friday shows "Jumu'ah" instead of Zuhr. View preference saved to localStorage. Auto-refreshes every 60s. Defaults to "Today" view always (user can switch; preference saved to localStorage).
- Live prayer-by-prayer countdown (Sehri > Fajr Jamaah > Zuhr > Zuhr Jamaah > Asr > Asr Jamaah > Iftar > Isha > Isha Jamaah > next Sehri)
- Pre-Ramadan countdown with days display
- Post-Ramadan "Eid Mubarak" state
- Today's row auto-highlighted with pulse animation and "TODAY" badge (full timetable view)
- Friday rows highlighted in red
- Last 10 nights highlighted (gold border), odd nights marked with "ODD" badge
- Dark mode (toggle bottom-right, saved to localStorage)
- WhatsApp share button (green, bottom-right)
- Browser notifications (15 min before Sehri/Iftar)
- Shared nav dropdown (search + switch mosques)
- Submit timetable / report error links (Google Form) on all pages + landing page
- Responsive mobile layout
- Print-friendly (hides buttons, countdown, nav, today-view)
- Moon sighting disclaimer in header
- **iOS Widget (Scriptable)**: `widget.js` — medium home screen widget showing today's 6 prayers (Fajr, Ishraq, Dhuhr, Asr, Maghrib, Isha) with Begins/Iqamah columns. Ishraq time calculated as sunrise + 20 minutes (matching Shahjalal). Fetches timetableData from waqt.uk, highlights next prayer, caches for offline. Widget parameter selects mosque: `shahjalal` (default), `quba`, `almahad`.

### Visual Enhancements (All Mosques)
- **Granim.js animated header**: Async-loaded from CDN, smooth gradient animation behind header. Cached by service worker for offline. Each mosque has unique color palette.
- **Islamic geometric pattern overlay**: CSS `::after` on header with inline SVG data URI (star pattern / hexagonal / arabesque per mosque)
- **Mosque building SVG icon**: Unique hand-crafted mosque SVG in header per mosque (see Themes below)
- **Animated mosque icon**: Window glow pulse (`@keyframes`) + gentle float on the SVG
- **Glassmorphism prayer cards**: `backdrop-filter: blur` + semi-transparent backgrounds in Today View
- **Countdown flip animation**: 3D CSS flip on individual digits when they change
- **Entrance animations**: `@keyframes slideUp` with staggered delays on cards, countdown, footer
- **Enhanced table hover**: `translateX(2px)` + left-border accent + shadow lift
- **Floating button glass effect**: `backdrop-filter: blur(8px)` on fixed buttons
- **Custom themed scrollbar**: Per-mosque colors (WebKit + Firefox)
- **Skeleton shimmer**: Loading animation on header while Granim initializes

### Smart Features (All Mosques)
- **Ramadan progress bar**: Thin bar below header showing "Day X of 30" with gradient fill. Auto-calculated from timetableData. Hidden outside Ramadan.
- **Auto dark mode at Maghrib**: Automatically enables dark mode after Maghrib, disables after Fajr. Respects manual toggle (disables auto if user toggles manually). localStorage: `{prefix}-autoDark`
- **Eid confetti burst**: 150 themed particles burst when "Eid Mubarak" state triggers. Canvas overlay, self-removes after 5s.
- **Qibla compass**: Floating button (bottom-left) opens overlay with compass rose SVG. Arrow points 119.7° (Bradford → Ka'bah). Live compass on mobile via DeviceOrientationEvent (incl. `deviceorientationabsolute`), static bearing on desktop. **Standard implementation**: All mosques use the Shahjalal compass pattern (IIFE with `openQibla`/`closeQibla`/`closeQiblaOverlay` on window, `.qibla-overlay.open` toggle, `.qibla-compass`/`.qibla-compass-ring`/`.qibla-bearing-text` classes, `#qiblaSvg`/`#qiblaArrow`/`#qiblaKaaba` SVG IDs). New mosques should copy this pattern and only change theme colors.
- **AI Prayer Assistant**: `chat.js` — floating gold chat button (bottom-left, above Qibla compass) on all pages. Opens glassmorphism chat panel. Includes STATIC_INFO variable with mosque programmes/events (Quba tarawih, Tawakkulia daily programmes, IYMA donation appeal, Jamia Masjid maghrib notice) appended to timetable context. Sends questions + full context from all mosques to n8n webhook (`/webhook/prayer-chat`), which calls GPT-4o-mini via OpenAI API (system prompt includes spelling variations: jummah, jamaah, sehri, taraweeh, witr, asr, iftar; max_tokens=350). Suggestion chips: "Latest Isha Jamaah?", "Earliest Fajr Jamaah?". Header uses mosque's theme color. Mobile keyboard handling via `visualViewport` API. Session-only message history (not persisted). Context gathered by fetching each mosque's `index.html` and regex-extracting `timetableData`, cached per session.

### Progressive Enhancement
- All visual effects respect `prefers-reduced-motion: reduce`
- Print styles hide all interactive/decorative elements
- Granim falls back to CSS gradient if CDN/WebGL fails
- Qibla compass falls back to static bearing without device orientation
- All features work offline via service worker

### PWA & Assets
- **PWA**: manifest.json + sw.js for offline support, installable (all mosques)
- **OG image**: og-image.svg social preview (all mosques)
- **QR poster**: poster.html for A4 printing (all mosques)
- **Service worker**: Caches Granim.js CDN for offline (cache version: v6)

### Themes Per Mosque

| Mosque | SVG Icon | Pattern | Particle Effect | Card Accent | Confetti Colors |
|--------|----------|---------|-----------------|-------------|-----------------|
| Shahjalal | Grand mosque, 2 minarets (gold/amber) | Islamic star | Floating stars | Left border | Gold, teal, white, green |
| Quba | Modern mosque, 1 dome+minaret (silver/blue) | Hexagonal | Rising light orbs | Top border | Blue, silver, gold, white |
| Almahad | Triple-dome traditional (gold/green) | Arabesque floral | Golden fireflies | Bottom border | Green, gold, white, emerald |
| Tawakkulia | Dual-minaret with side domes (indigo) | Islamic star | Floating orbs | Left border | Indigo, light indigo, gold, white |
| Salahadin | Fortress-style, dual minarets, crenellations (burgundy) | Interlocking circles | Warm embers | Right border | Burgundy, rose, gold, white |
| Abu Bakar | Modern mosque, 1 dome+minaret (purple) | Hexagonal | Rising light orbs | Top border | Purple, lavender, gold, white |
| IYMA | Modern mosque, 1 dome+minaret (cyan) | Hexagonal | Rising light orbs | Top border | Cyan, teal, gold, white |
| Jamia Masjid | Modern mosque, 1 dome+minaret (navy) | Hexagonal | Rising light orbs | Top border | Navy, steel blue, gold, white |
| Masjid Ibraheem (Leeds) | Modern mosque, 1 dome+minaret (orange) | Hexagonal | Rising light orbs | Top border | Deep orange, amber, gold, white |

### Shahjalal-Only Features
- **Demo mode**: DEMO button (bottom-left), date picker + time slider to test countdown at any date/time

### Unique Sections
- **Quba**: Programmes During Ramadan (Ml. Siraj Saleh, Ml. Ahmed Desai), live stream info
- **Almahad**: "Some Sunnah of Ramadan" 10-item grid (Sahoor, Iftar, Taraweeh, Quran, etc.)
- **Tawakkulia**: Programmes During Ramadan (Taleem, Dars-e-Quran, Bangla Bayan, English Weekend Bayan, Quran Mashq, Late Night Taraweeh). Has separate `iftar` (sunset) and `maghrib` (jamaah) fields in timetableData — other mosques use `maghrib` for both. Source data in `ramadan_timetable.json`.
- **Salahadin**: Full February timetable (pre-Ramadan + Ramadan), Jumu'ah info (Khutba 12:30, Salah 12:50)
- **Abu Bakar**: No unique content sections
- **IYMA**: Donation appeal banner (Phase 3 extension building project), parking notice
- **Jamia Masjid**: No unique content sections (note: Maghrib Salah commences 2 min after Iftar)
- **Masjid Ibraheem**: No unique content sections. Friday Prayer: 1st Jummah 1pm / 2nd Jummah 3pm (in footer)

### Landing Page (waqt.uk)
- Granim.js animated background (deep blue/teal gradients)
- Card hover effects with per-mosque border glow colors
- Staggered entrance animations on cards
- Subtle Islamic geometric star/octagon pattern overlay
- Enhanced footer with "Ramadan 1447 | UK" context
- Custom scrollbar, skeleton shimmer

## How to Add a New Mosque

### 1. Create the timetable
```
mkdir NewMosque
```
Copy any existing `index.html` as a starting point, then update:
- `<title>` and meta tags (description, og:title, og:description, og:url, theme-color)
- Header content (mosque name, address, contact info)
- `timetableData` array with all 30 days of prayer times
- Theme colors throughout CSS (search/replace the old color hex values)
- localStorage keys (use unique prefix, e.g. `newmosque-darkMode`, `newmosque-notifications`, `newmosque-viewMode`, `newmosque-autoDark`)
- WhatsApp share URL
- Today View: CSS accent colors, `renderTodayView()`, `setView()`, localStorage key, toggle HTML
- Footer content (Eid times, Fitrana, donation details, notices)
- Any unique sections (programmes, sunnah, etc.)
- Mosque SVG icon in header (unique design per mosque)
- Granim.js color palettes (light + dark mode gradients)
- Islamic geometric pattern overlay (choose unique pattern)
- Particle effect canvas (choose unique style: stars/orbs/fireflies)
- Prayer card accent direction (left/top/bottom border)
- Confetti colors for Eid burst
- Scrollbar theme colors
- Add `<script src="../nav.js"></script>` and `<script src="../chat.js"></script>` before `</body>`

### 2. Add to nav.js
Add one line to the `MASJIDS` array:
```js
{ name: 'New Mosque Name', addr: 'Street, Postcode', folder: 'NewMosque' },
```
This automatically updates the nav dropdown on ALL timetable pages.

### 3. Add to landing page
Add a card to `index.html`:
```html
<a href="NewMosque/" class="masjid-card">
    <div class="card-colour" style="background: linear-gradient(to bottom, #COLOR1, #COLOR2);"></div>
    <div class="card-info">
        <div class="card-name">New Mosque Name</div>
        <div class="card-address">Street, Postcode</div>
    </div>
    <div class="card-arrow">&rsaquo;</div>
</a>
```

### 4. Commit and push
```bash
git add NewMosque/index.html nav.js index.html
git commit -m "Add New Mosque timetable"
git push
```

## Batch Mosque Generation (Masjids/ folder)

For adding many mosques at once without hand-coding each HTML file.

### Scripts
| Script | Purpose |
|--------|---------|
| `apply_colors.py` | Assigns `color1`/`color2` to each `data.json` from the curated palette |
| `generate.py` | Generates `index.html` per mosque from abubakar template |
| `gen_pwa.py` | Generates `manifest.json`, `sw.js`, `og-image.svg`, `poster.html` |
| `update_landing.py` | Updates landing page card gradients to match each mosque's `color1`/`color2` |
| `validate.py` | Data validation (row count, dates, day names, time format) |
| `scripts/patch_timetables.py` | Applies highlight fixes (Jamaah-based cutoff + post-Isha wrap) to the 10 original hand-crafted mosque pages |

### data.json schema
```json
{
  "name": "Mosque Full Name",
  "short_name": "Short Name",
  "prefix": "urlslug",
  "address": "Street, City, Postcode",
  "color1": "#1a3a2e",
  "color2": "#2d6a4f",
  "phone": "01274 123456",
  "phone_display": "01274 123 456",
  "notes": "Maghrib Salah commences after Iftar",
  "eid_info": "7:30am | 9:00am | 10:30am",
  "fitrana": "£5.00 per person",
  "donation_info": "Bank Name | Sort: 00-00-00 | Acc: 00000000",
  "website": "https://example.com",
  "receiver_freq": "454.40625",
  "timetable": [
    { "date": [2026, 2, 18], "day": "Wed", "no": 1,
      "sehri": "5:39", "fajr": "5:44", "sunrise": "7:20",
      "zuhr": "12:35", "asr": "3:45", "maghrib": "5:26",
      "isha": "7:30", "jFajr": "7:00", "jZuhr": "1:15",
      "jAsr": "4:00", "jIsha": "8:00" }
  ]
}
```

### Workflow
1. Create `Masjids/<Name>/data.json` with timetable data + `color1`/`color2`
2. Validate: `python Masjids/validate.py` (checks row count, dates, day names, time format)
3. Generate HTML: `python Masjids/generate.py` → writes `Masjids/<Name>/index.html`
4. Copy to root: copy each `Masjids/<Name>/index.html` → `<prefix>/index.html`
5. Generate PWA assets: `python Masjids/gen_pwa.py` → writes manifest.json, sw.js, og-image.svg, poster.html
6. Update landing cards: `python Masjids/update_landing.py` → updates card gradient colors in index.html
7. Update nav.js (MASJIDS array) if adding new mosques
8. Push all changes

### generate.py internals
- Uses `abubakar/index.html` as template
- Replaces: title/meta tags, URLs, header text, address, phone, localStorage prefix, timetableData, footer, **colors**
- **Color theming**: Reads `color1`/`color2` from data.json, derives a full 10-color palette (dark, medium, mid, deep, light secondary, very light, palest tint, medium-light, medium, bright accent) and replaces all 10 purple shades from the template. Palette derived using `blend()`, `lighten()`, `darken()` functions.
- **timetableData replacement**: Uses `str.index()` with markers `'const timetableData = ['` and `'\n        ];'` — NOT regex (regex with `.*?` was buggy: non-greedy match stopped at first `]` inside `date: [2026, 2, 18]`)
- Optional sections: receiver_freq, donation_info (removed if not present in data.json)

### Color palette (template purple → derived per-mosque)
| Template color | Role | Derived as |
|---------------|------|-----------|
| `#4a148c` | Primary dark | `color1` |
| `#7b1fa2` | Primary medium | `color2` |
| `#6a1b9a` | Mid dark | blend(color1, color2, 0.4) |
| `#311b92` | Deep dark | darken(color1, 0.15) |
| `#ce93d8` | Light secondary | lighten(color2, 0.55) |
| `#e8d5f5` | Very light primary | lighten(color1, 0.78) |
| `#f3e5f5` | Palest tint | lighten(color1, 0.88) |
| `#ba68c8` | Medium-light secondary | lighten(color2, 0.38) |
| `#ab47bc` | Medium secondary | lighten(color2, 0.22) |
| `#e040fb` | Bright accent | `color2` |

### Data validation checks
- 30 rows (29 acceptable for mosques with confirmed later Ramadan start)
- Date sequence: Feb 18 → Mar 19
- Day-of-week matches actual date
- Ramadan day numbers 1–30 sequential
- Time format uses `:` not `.`
- Time sanity ranges (sehri 4-6am, fajr 4-6am, maghrib 4-6pm, isha 6-9pm)
- Day names: Mon/Tue/Wed/Thu/Fri/Sat/Sun (not UPPERCASE, not Thur/Tues)

## Technical Notes

### Time Parsing
- Sehri/Fajr times are AM (stored as-is, e.g. "5:39")
- Maghrib/Isha times are PM (stored in 12hr format, e.g. "5:26")
- JS converts PM times: `isPM && h < 12 ? h + 12 : h`
- Countdown uses ms-precision Date diffs for live ticking seconds

### Countdown Sequence
```
Sehri ends → Fajr Jamaah → Zuhr begins → Zuhr Jamaah →
Asr begins → Asr Jamaah → Iftar → Maghrib Jamaah* → Isha begins → Isha Jamaah →
(next day's Sehri) → loop
```
After the last day's Isha Jamaah, shows "Eid Mubarak".

*Maghrib Jamaah step only on Tawakkulia (has separate iftar/sunset and maghrib jamaah times).

### localStorage Keys Per Mosque
| Mosque | Dark Mode | Notifications | View Mode | Auto Dark |
|--------|-----------|---------------|-----------|-----------|
| Shahjalal | `darkMode` | `notifications` | `viewMode` | `shahjalal-autoDark` |
| Quba | `quba-darkMode` | `quba-notifications` | `quba-viewMode` | `quba-autoDark` |
| Almahad | `almahad-darkMode` | `almahad-notifications` | `almahad-viewMode` | `almahad-autoDark` |
| Tawakkulia | `tawakkulia-darkMode` | `tawakkulia-notifications` | `tawakkulia-viewMode` | `tawakkulia-autoDark` |
| Salahadin | `salahadin-darkMode` | `salahadin-notifications` | `salahadin-viewMode` | `salahadin-autoDark` |
| Abu Bakar | `abubakar-darkMode` | `abubakar-notifications` | `abubakar-viewMode` | `abubakar-autoDark` |
| IYMA | `iyma-darkMode` | `iyma-notifications` | `iyma-viewMode` | `iyma-autoDark` |
| Jamia Masjid | `JamiaMasjid-darkMode` | `JamiaMasjid-notifications` | `JamiaMasjid-viewMode` | `JamiaMasjid-autoDark` |
| Masjid Taqwa | `taqwa-darkMode` | `taqwa-notifications` | `taqwa-viewMode` | `taqwa-autoDark` |
| Masjid Ibraheem | `ibrahim-darkMode` | `ibrahim-notifications` | `ibrahim-viewMode` | `ibrahim-autoDark` |

### nav.js
- Self-executing function that injects CSS, HTML, and event handlers
- Detects active mosque from URL path
- Search filter works on name + address (search is inside the dropdown, opened by clicking mosque name; magnifying glass icon on nav button)
- Print media query hides nav
- **Apostrophe escaping**: Mosque names/addresses containing apostrophes (Mary's, King's, Ta'limul, Margaret's) must use `\&#39;` in the MASJIDS array addr strings, otherwise unescaped quotes break the JS template literal and crash nav.js on every page
- Dark mode aware (`body.dark-mode .masjid-nav`)

### External Dependencies
- **Granim.js v2.0.0** (`cdn.jsdelivr.net/npm/granim@2.0.0/dist/granim.min.js`) - animated gradient backgrounds. Loaded async, cached by service worker, falls back to CSS gradient if unavailable.
- **OpenAI GPT-4o-mini** (via n8n webhook proxy on Railway) - AI prayer times chatbot. n8n workflow "Prayer AI Chat" (ID: `eZayWM5UAKhF8RWA`), webhook path `/webhook/prayer-chat`. Uses Header Auth credential for OpenAI API key.
- **Google Analytics 4** (`G-9DPJ6NR37M`) - injected dynamically via `chat.js` (covers all 48 pages). Dashboard: `analytics.google.com`.
- No other external JS libraries. All other effects are vanilla CSS/JS/SVG + Web Audio API.

### Data Source
- Timetables transcribed from printed/JPEG posters provided by each mosque
- Each mosque has slightly different Jamaah times
- Beginning times (Fajr, Zuhr, Asr, Isha) may also differ slightly between mosques

### Deployment
- GitHub Pages, deploy from branch (legacy mode), `master` branch
- Push to `master` triggers automatic rebuild
- Custom domain: `waqt.uk` (Namecheap)
- Old URL `sidnikiwi-afk.github.io/Prayer-times/` redirects to `waqt.uk`
- HTTPS enforced (SSL cert auto-provisioned by GitHub)

### Domain DNS (Namecheap)
```
A     @     185.199.108.153
A     @     185.199.109.153
A     @     185.199.110.153
A     @     185.199.111.153
CNAME www   sidnikiwi-afk.github.io
```

### URLs
**Original 9 mosques** (hand-crafted, unique themes):

| Page | URL |
|------|-----|
| Landing page | `waqt.uk` |
| Shahjalal | `waqt.uk/shahjalal/` |
| Masjid Quba | `waqt.uk/quba/` |
| Al Mahad Ul Islami | `waqt.uk/Almahad/` |
| Tawakkulia Islamic Society | `waqt.uk/Tawakkulia/` |
| Salahadin Mosque | `waqt.uk/Salahadin/` |
| Masjid Abu Bakar | `waqt.uk/abubakar/` |
| IYMA | `waqt.uk/iyma/` |
| Jamia Masjid | `waqt.uk/JamiaMasjid/` |
| Masjid Taqwa | `waqt.uk/taqwa/` |
| Masjid Ibraheem (Leeds) | `waqt.uk/ibrahim/` |

**Batch mosques** (38 total, all at `waqt.uk/<prefix>/`): alabrar, alamin, alhidaya, alhikmah, alhidaayah, almustaqeem, azharulmadaaris, baitulilm, darulmahmood, doha, firdaws, iqra, abuhanifa, farooqiah, madnimasjid, abbasiya, darulirfan, abdullahbinmasood, masjidali, masjidayesha, masjidbilal, masjidhamza, masjidhusain, ibraheem, namirah, masjidnoor, noorulislam, nusratul, farooqia, masjidumar, masjidusman, raashideen, musallasalaam, ahlebayt, shipley, westleeds, wibseybuttershaw, wibsey

### Git Config
- Repo: `sidnikiwi-afk/Prayer-times`
- Auth: `gh auth setup-git` (credential helper configured)
- Identity: sidnikiwi-afk
