# Prayer-times Project

## Overview
Prayer timetable web app for UK mosques (51 with timetables, 2100+ in directory).
Ramadan 1447 (Feb-Mar 2026) + year-round prayer times. Cities: Bradford, Leeds, Keighley, Oldham, and more.
Hosted on GitHub Pages. Each mosque gets its own subfolder with a self-contained HTML page.

- **Repo**: https://github.com/sidnikiwi-afk/Prayer-times
- **Live**: https://waqt.uk/
- **Domain**: `waqt.uk` (Namecheap, DNS → GitHub Pages)
- **GitHub account**: sidnikiwi-afk

## File Structure
```
Prayer-times/
├── index.html              # Landing page - mosque selector (waqt.uk), JS-rendered from directory.json
├── directory.json          # Single source of truth for all mosques (name, address, postcode, city, slug, colors, has_timetable)
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
├── aqsa/
│   ├── index.html          # Masjid-Ul-Aqsa & Islamic Centre timetable (Oldham)
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
# ... plus 39 batch-generated mosque folders (alabrar/, alamin/, alhidaya/, westleeds/, makkimasjidmadrassah/, etc.)
# See "Batch Mosque Generation" section below for the full list and workflow.
scripts/
├── patch_timetables.py     # Applies Fixes 4 & 5 to 10 original hand-crafted mosque pages
├── build_directory.py      # Queries OSM Overpass API for UK mosques → merges with directory.json
├── clean_directory.py      # Deduplicates, removes non-UK, tags types, fixes city names
├── enrich_directory.py     # Fills missing data (address, phone, website) via Serper.dev
├── import_mib.py           # Imports Muslims in Britain CSV, filters Shia/multi-faith, deduplicates
├── add_coordinates.py      # Adds lat/lon via Postcodes.io batch API
├── fix_coordinates.py      # Corrects bad lat/lon values
└── MosquesMar26.csv        # Muslims in Britain raw data (2,191 entries)
Masjids/                    # Source data for batch-generated mosques
├── generate.py             # Batch HTML generator (uses abubakar/ as template, applies colors)
├── gen_pwa.py              # Batch PWA asset generator (manifest, sw, og-image, poster)
├── apply_colors.py         # Assigns color1/color2 to each data.json
├── update_landing.py       # LEGACY - no longer needed (homepage reads from directory.json)
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
| Jamia Masjid | `JamiaMasjid` | 28-32 Howard St, BD5 0BP | Navy `#0d1b2a` / `#1b3a5c` | 6:30am, 9:30am | £4.00 |
| Masjid Taqwa | `taqwa` | 807 Great Horton Road, BD7 4AG | Cobalt Blue `#0d47a1` / `#1976d2` | 6:30am, 9:30am | £5.00 |
| Masjid Ibraheem | `ibrahim` | 4 Woodview Rd, Beeston, Leeds LS11 6LE | Deep Orange `#bf360c` / `#e64a19` | 9:00am (Men), 10:30am (Men & Women) | £5.00 |
| Masjid-Ul-Aqsa & Islamic Centre | `aqsa` | 135 Windsor Road, Coppice, Oldham OL8 1RG | Wine Red `#5d1020` / `#8b2040` | TBA | £5.00 |

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
- **Masjid-Ul-Aqsa**: Barclays Bank, Sort: 20-26-20, Acc: 70626694, Charity Reg: 1179403

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
- **Makki Masjid & Madrassah**: Tel 0113 245 6501 | www.makkimasjid.co.uk | Queries: 07827 295201
- **Masjid-Ul-Aqsa**: Tel 0161 633 0327 | www.masjidulaqsa.org.uk

### Batch-Generated Mosques (Ramadan 1447 – added Feb 2026)

These 41 mosques were added in bulk using the `Masjids/` batch generation workflow.
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
| Shahjalal Jami Masjid & Jamia Qurania | `sjmkeighley` | Temple Row, Keighley, BD21 2AH | Dark gold/Goldenrod |
| Jamia Masjid - Howard Street | `JamiaMasjid` | 28-32 Howard St, BD5 0BP | (shares JamiaMasjid page) |
| Makki Masjid & Madrassah | `makkimasjidmadrassah` | 1 Vicarage Road, Leeds, LS6 1NX | Dark green `#1a3a2e` / `#2d6a4f` |

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
- **Data-driven**: All mosque cards rendered from `directory.json` via JS (no hardcoded HTML cards)
- **Timetables / Directory toggle**: Pill-shaped glassmorphism switch. Timetables view (default) shows mosques with prayer times. Directory view shows all mosques including those without timetables.
- **Location sorting**: Pin icon in search bar → requests browser geolocation → geocodes postcodes via Postcodes.io bulk API (free, no key) → sorts by nearest → shows distance badges (e.g. "0.3 mi"). Coordinates cached in localStorage (30-day TTL). States: grey (default), teal+pulse (active), red (error/denied).
- **City sections**: Mosques grouped under collapsible city headers (Bradford, Keighley, Leeds, Oldham). First/nearest city expanded, rest collapsed. Reorders by proximity when location active.
- **Directory cards**: Pin icon opens Google Maps directions. Timetable cards link to timetable page + show pin icon in directory view.
- **Search**: Filters across both views and city sections, hides empty sections, updates city counts.
- Granim.js animated background (deep blue/teal gradients)
- Staggered entrance animations on first load only
- Subtle Islamic geometric star/octagon pattern overlay
- Enhanced footer with "Ramadan 1447 | UK" context
- Custom scrollbar, skeleton shimmer
- Accessible: aria-labels, aria-expanded, role=button on city headers, 44px touch targets

## Timetable Submission Automation

Automated workflow to extract prayer times from mosque submissions via AI vision, validate data, and commit to repo.

### Architecture

**Flow**: Google Drive → Apps Script Watcher → n8n Processor → Dual AI Vision → Postgres → Telegram Approval → GitHub Commit

### Components

#### 1. Google Apps Script Watcher
- **Script**: `apps_script_watcher.js` (also saved at `G:\My Drive\Work\apps-script-watcher/`)
- **Script ID**: `1l2m3vt8sZOTPCGII3C5b3AGx-jdcWm1RHghWIIJRfY8j_4P66KmFb4fd`
- **Trigger**: Every 1 minute (time-driven)
- **Watches**: Drive folder `1khMM9ZH_J7HH7Dcx4uRMdNP-S2mPoOAN8Xy52iwQz7pmqYEg0XXSAPppxCGn9novB2rPBmVc`
- **Purpose**: Sends new file IDs to n8n webhook (workaround for Railway's broken Google Drive polling trigger)
- **Deduplication**: Marks files as processed in Script Properties BEFORE sending webhook (prevents duplicates since webhook takes ~3 min but trigger runs every 1 min)
- **Setup**: Run `setup()` once in Apps Script editor to create trigger
- **Deploy via CLI**: `cd apps-script-watcher && clasp push` (logged in as `sidni.kiwi@gmail.com`)
- **Local clasp project**: `G:\My Drive\Work\apps-script-watcher/` (Code.js + appsscript.json + .clasp.json)

#### 2. n8n Workflow: "Timetable Submission Processor"
- **ID**: `If9GquKXNqlINPMn` (ACTIVE)
- **Webhook**: POST `https://primary-production-64370.up.railway.app/webhook/timetable-submission`
- **Payload**: `{fileId: string, fileName: string, mimeType: string, createdDate: string}`
- **Steps**:
  1. Webhook trigger receives file metadata
  2. Google Drive Download (using n8n credential `IIwzOJaw01epsSRq`)
  3. Dual AI extraction (parallel):
     - Claude Vision via Anthropic API (credential `pBI2VZprhG0vSJ60`)
     - OpenAI Vision via GPT-4o (credential `MkQvVYaqpmHI70cs`)
  4. Validation: JSON parse, row count (variable by period: 30 for Ramadan, 28-31 for monthly, 360+ for annual), required fields
  5. Best score selection (Claude typically 100/100, OpenAI unreliable)
  6. Postgres INSERT to `timetable_submissions` (credential `pSxR0FEFIyRJHnfX`)
  7. Telegram notification with Approve/Reject inline keyboard buttons (timetable submissions) or Acknowledged button (non-timetable submissions)
  8. Webhook response: `{success: true, id: uuid}`
- **Submission types**: AI classifies each submission as: `timetable` (with period: ramadan/monthly/annual/custom), `error_report`, `jumuah`, `eid`, `event`, `other`
- **Non-timetable handling**: Error reports, Eid info, Jumu'ah times, events get type-specific Telegram notifications and are stored in Postgres for manual review

#### 3. n8n Workflow: "Timetable Approval Handler" (ACTIVE)
- **ID**: `yAenh4XW0VfJPPW0` (20 nodes)
- **Trigger**: Telegram callback query (inline keyboard button press)
- **Approve path** (13 nodes):
  1. Telegram Callback → Parse Callback → Route Action (IF)
  2. Fetch Submission (Postgres by ID) → Prepare GitHub Commit (Code: builds filePath, base64Content, validates data)
  3. Check Valid (IF: routes errors to notification path)
  4. Get File SHA (HTTP GET to GitHub Contents API, continueOnFail) → Build Commit Body (Code: includes SHA if file exists, for updates vs creates)
  5. Commit to GitHub (HTTP PUT) → Update DB Status → Prepare Approve Msg → Answer Approve Callback + Send Approve Confirm
- **Reject path**: Prepare Reject Msg → Update DB Rejected → Answer Reject Callback + Send Reject Confirm
- **Error path** (from Check Valid false): Prepare Error Msg → Answer Error Callback + Send Error Telegram
- **Key fixes**: Handles existing files (gets SHA first), validates data before commit attempt, error notifications on invalid data

#### 4. Postgres Table: `timetable_submissions`
```sql
CREATE TABLE IF NOT EXISTS timetable_submissions (
  id UUID PRIMARY KEY,
  mosque_name TEXT,
  submitter TEXT,
  file_name TEXT,
  drive_file_id TEXT,
  claude_json JSONB,
  openai_json JSONB,
  final_json JSONB,
  validation_notes TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### 5. Telegram Bot
- **Name**: `Waqt_timetable_bot`
- **Token**: `8238602157:AAG2fKf3kzOlK8RW51QVI2Oq02sq_aWnvJ8`
- **Chat ID**: `1578762040`
- **Message format**:
  ```
  New timetable submitted: [Mosque Name]
  File: [filename.jpg]
  Claude score: [X/100]
  OpenAI score: [Y/100]
  Validation: [notes]
  ```

#### 6. Manual Test Script
- **Path**: `test_submission.py`
- **Usage**: `python test_submission.py path/to/timetable.jpg`
- **Steps**: Read image → Claude Vision → OpenAI Vision → Validate → Postgres INSERT → Telegram notify
- **Test results** (2026-02-22):
  - Claude Vision: 100/100 (perfect JSON extraction)
  - OpenAI Vision: 0/100 (failed JSON parse)

### AI Vision Prompts

**System**: Extract prayer timetable from image. Classify submission type (timetable with period ramadan/monthly/annual/custom, error_report, jumuah, eid, event, other). Return JSON only.

**Expected schema**:
```json
{
  "name": "Full Mosque Name",
  "short_name": "Short Name",
  "prefix": "urlslug",
  "address": "Street, City, Postcode",
  "color1": "#1a3a2e",
  "color2": "#2d6a4f",
  "timetable": [
    {
      "date": [2026, 2, 18],
      "day": "Wed",
      "no": 1,
      "sehri": "5:39",
      "fajr": "5:44",
      "sunrise": "7:20",
      "zuhr": "12:35",
      "asr": "3:45",
      "maghrib": "5:26",
      "isha": "7:30",
      "jFajr": "7:00",
      "jZuhr": "1:15",
      "jAsr": "4:00",
      "jIsha": "8:00"
    }
  ]
}
```

### Validation Rules

- Row count: Variable by period — 29-30 for Ramadan, 28-31 for monthly, 360+ for annual, flexible for custom
- Date sequence: Validated as sequential (not hardcoded to specific dates)
- Time format: `HH:MM` (colon, not dot)
- Required fields: mosque name, prefix, address, timetable array (for timetable type); identifier field (for non-timetable types)
- Scoring: +10 per field populated, max 100. Non-timetable submissions score 90 if identifier present, 50 if not

### Status: FULLY WORKING (tested 2026-02-27)

End-to-end test passed: Submission Processor (11 nodes) + Approval Handler (20 nodes) both working. Tested with Jamia Masjid Howard Street submission — AI extracted, validated, stored in Postgres, Telegram Approve button pressed, GitHub commit succeeded (including SHA lookup for existing file update). Also tested non-timetable submission (Eid info image) — correctly classified and notified.

**Fixes applied:**
- **Google Drive credential**: Authenticated as `sidni@localcardoctor.com`. Submissions folder shared with this account (Viewer access) to fix 404 download error.
- **Binary data**: n8n Code node `bin.data` returns a reference ID in newer n8n versions. Fixed to `await this.helpers.getBinaryDataBuffer(0, binaryKey)` then `.toString('base64')` for actual image data.
- **Telegram expression**: `Send Telegram` node was reading `$json.telegramBody` which was null (upstream `Store Submission` Postgres INSERT only returns `{id}`). Fixed to `$node["Prepare Store & Notify"].json.telegramBody`.
- **$input fix**: `Prepare AI Requests` node had `\.first()` instead of `$input.first()` (bash `$` escaping artifact).
- **Duplicate submissions**: Apps Script marked files as processed AFTER the webhook response (which takes ~3 min). During that time, 3 more 1-minute triggers fired sending the same file. Fixed by marking files as processed BEFORE the `UrlFetchApp.fetch()` call.
- **Empty drive_file_id**: Submission Processor used `item.json.id` for Drive file ID, but the Google Drive download node doesn't return `id` in json output. Fixed to `$('Webhook').first().json.body.fileId` to get it from the original webhook payload.
- **Approval Handler 404 on empty filePath**: When final_json had no valid timetable data, Prepare GitHub Commit returned error but workflow continued to Commit node with empty URL. Fixed by adding Check Valid IF node that routes errors to Telegram notification path.
- **Approval Handler 422 "sha wasn't supplied"**: When file already existed on GitHub, PUT without SHA failed. Fixed by adding Get File SHA (HTTP GET, continueOnFail) before commit, and Build Commit Body that includes SHA if file exists.

**Design decisions:**
- Telegram inline keyboard with Approve/Reject buttons for timetable submissions. Approve commits data.json to GitHub repo via API. Non-timetable submissions (Eid, Jumu'ah, etc.) get an Acknowledged button.
- After approval, still run `/add-mosque` manually to generate full HTML page, PWA assets, and update nav/directory.

### Post-Approval Workflow

After Telegram approval commits data.json to GitHub, generate the full page:

```bash
cd Prayer-times
git pull
python Masjids/generate.py          # Generates index.html from data.json
# Copy Masjids/<Name>/index.html to <prefix>/index.html
python Masjids/gen_pwa.py           # Generates manifest, sw, og-image, poster
# Edit nav.js MASJIDS array if new mosque
# Add entry to directory.json (name, address, postcode, city, slug, colors, has_timetable, tags)
git add .
git commit -m "Add [Mosque Name] timetable (automated submission)"
git push
```

### Credentials Created (n8n)

| Name | Type | ID | Purpose |
|------|------|-----|---------|
| Waqt Timetable Bot | telegramApi | `0g52BTf7dqjmIV2Y` | Telegram notifications |
| Anthropic API Key | httpHeaderAuth | `pBI2VZprhG0vSJ60` | Claude Vision API |
| GitHub PAT | httpHeaderAuth | `35rydgNWU8PRT4oH` | Commit to repo |
| Google Drive account | googleDrive | `IIwzOJaw01epsSRq` | Download submissions (auth: `sidni@localcardoctor.com`) |
| OpenAi account | openAi | `MkQvVYaqpmHI70cs` | OpenAI Vision API |
| Postgres account | postgres | `pSxR0FEFIyRJHnfX` | Database storage |

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

### 3. Add to directory.json
Add an entry to the `mosques` array in `directory.json`:
```json
{
  "name": "New Mosque Name",
  "address": "Street Address",
  "postcode": "BD5 0XX",
  "city": "Bradford",
  "has_timetable": true,
  "slug": "newmosque",
  "color1": "#COLOR1",
  "color2": "#COLOR2",
  "tags": "Area Name"
}
```
For directory-only mosques (no timetable page), set `"has_timetable": false` and `"slug": null`.

### 4. Commit and push
```bash
git add NewMosque/index.html nav.js directory.json
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
| `update_landing.py` | LEGACY - no longer needed (homepage reads from `directory.json`) |
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
6. Add entry to `directory.json` (name, address, postcode, city, slug, colors, has_timetable, tags)
7. Update nav.js (MASJIDS array) if adding new mosques
8. Push all changes

**Note:** `update_landing.py` is no longer needed — the homepage reads from `directory.json` directly.

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
| Masjid-Ul-Aqsa | `aqsa-darkMode` | `aqsa-notifications` | `aqsa-viewMode` | `aqsa-autoDark` |

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
- **Google Analytics 4** (`G-9DPJ6NR37M`) - injected dynamically via `chat.js` (covers all timetable pages). Dashboard: `analytics.google.com`.
- No other external JS libraries. All other effects are vanilla CSS/JS/SVG + Web Audio API.

### Data Sources
- **Timetables**: Transcribed from printed/JPEG posters provided by each mosque
- **Directory (OSM)**: ~1,034 mosques from OpenStreetMap Overpass API (via `build_directory.py`)
- **Directory (MiB)**: ~1,084 mosques from Muslims in Britain (muslimsInBritain.org) GPS CSV (via `import_mib.py`, added Mar 2026). Filtered Shia (148), multi-faith (75), non-UK (8). Deduplicated by postcode + coordinate proximity.
- **Enrichment**: Addresses, phones, websites filled via Serper.dev Google Search API
- **Geocoding**: Postcodes and cities via Postcodes.io free batch reverse geocode API
- Each mosque has slightly different Jamaah times
- Beginning times (Fajr, Zuhr, Asr, Isha) may also differ slightly between mosques

### Directory Stats (Mar 2026)
- **Total**: 2,113 mosques (51 with timetables, 2,062 directory-only)
- **Types**: 2,002 mosques, 57 prayer rooms, 54 community centres
- **Coverage**: 91% addresses, 99% postcodes, 50% phones, 24% websites
- **Top cities**: London (425), Birmingham (174), Bradford (138), Huddersfield (74), Leicester (69)

### Directory Update Pipeline
```
1. build_directory.py    → directory_new.json  (OSM import)
   import_mib.py         → directory_new.json  (MiB import, alternative source)
2. clean_directory.py    → directory_clean.json (dedup, tag types, fix cities)
3. enrich_directory.py   → directory_clean.json (Serper.dev search enrichment)
4. cp directory_clean.json directory.json → commit & push
```

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
**Original 12 mosques** (hand-crafted, unique themes):

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
| Masjid-Ul-Aqsa (Oldham) | `waqt.uk/aqsa/` |

**Batch mosques** (41 total, all at `waqt.uk/<prefix>/`): alabrar, alamin, alhidaya, alhikmah, alhidaayah, almustaqeem, azharulmadaaris, baitulilm, darulmahmood, doha, firdaws, iqra, abuhanifa, farooqiah, madnimasjid, abbasiya, darulirfan, abdullahbinmasood, masjidali, masjidayesha, masjidbilal, masjidhamza, masjidhusain, ibraheem, namirah, masjidnoor, noorulislam, nusratul, farooqia, masjidumar, masjidusman, raashideen, musallasalaam, ahlebayt, shipley, westleeds, wibseybuttershaw, wibsey, sjmkeighley, masjidtaqwa, makkimasjidmadrassah

### Git Config
- Repo: `sidnikiwi-afk/Prayer-times`
- Auth: `gh auth setup-git` (credential helper configured)
- Identity: sidnikiwi-afk
