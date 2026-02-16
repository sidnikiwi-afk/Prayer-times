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
├── chat.js                 # AI prayer times chatbot (loaded on all pages)
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
└── JamiaMasjid/
    ├── index.html          # Jamia Masjid timetable
    ├── manifest.json       # PWA manifest
    ├── sw.js               # Service worker (offline support)
    ├── og-image.svg        # Social preview image
    ├── qr-code.svg         # QR code for poster
    └── poster.html         # A4 printable QR poster
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
| Jamia Masjid | `JamiaMasjid` | 28-32 Howard St, BD5 0BP | Brown/Amber `#4e342e` / `#795548` | TBA | TBA |

### Donation Details
- **Shahjalal**: Not listed in timetable
- **Quba**: Madressa Islamia Talimuddin, Barclays, Sort: 20-11-81, Acc: 90803383
- **Almahad**: Al Mahadul Islami, Sort: 20-76-92, Acc: 13161595
- **Tawakkulia**: Tawakkulia Jami Masjid, Sort: 56-00-36, Acc: 42345499
- **Salahadin**: Barclays Bank, Sort: 20-11-88, Acc: 83561801
- **Abu Bakar**: Yorkshire Bank, Acc: 18330977, Sort: 05-03-23
- **IYMA**: Imam Yusuf Motala Academy, Yorkshire Bank, Sort: 05-03-03, Acc: 71398073
- **Jamia Masjid**: TBA

### Contact / Radio
- **Quba**: Tel 01274 542027 | masjidquba.org | Receiver: 454.3500
- **Almahad**: Receiver: 456.62500
- **Tawakkulia**: Tel 01274 734563 | tawakkulia.com | tjmasjid@outlook.com | Receiver: 455-650
- **Abu Bakar**: Tel 01274 668343 | Receiver: 454.40625
- **IYMA**: Tel 07771 635 480 | info@iyma.org.uk | www.iyma.org.uk
- **Jamia Masjid**: Tel 01274 724 819

## Features (All Mosques)

### Core Functionality
- **Today View**: Card-based layout showing today's prayer times only, with pill toggle to switch to Full Timetable. Passed prayers dimmed with checkmark, next prayer highlighted with accent border + "NEXT" badge. Tomorrow preview at bottom: during Ramadan shows Sehri/Iftar times + any jamaah changes; outside Ramadan shows jamaah changes only (hidden if none). Friday shows "Jumu'ah" instead of Zuhr. View preference saved to localStorage. Auto-refreshes every 60s. Defaults to "Today" during Ramadan, "Full Timetable" otherwise.
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
- **AI Prayer Assistant**: `chat.js` — floating gold chat button (bottom-left, above Qibla compass) on all pages. Opens glassmorphism chat panel. Sends questions + today's timetable context from all 8 mosques to n8n webhook (`/webhook/prayer-chat`), which calls GPT-4o-mini via OpenAI API. Suggestion chips: "Latest Isha Jamaah?", "Earliest Fajr Jamaah?". Header uses mosque's theme color. Mobile keyboard handling via `visualViewport` API. Session-only message history (not persisted). Context gathered by fetching each mosque's `index.html` and regex-extracting `timetableData`, cached per session.

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
- **Service worker**: Caches Granim.js CDN for offline (cache version: v5)

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
| Jamia Masjid | Modern mosque, 1 dome+minaret (brown) | Hexagonal | Rising light orbs | Top border | Brown, tan, gold, white |

### Shahjalal-Only Features
- **Demo mode**: DEMO button (bottom-left), date picker + time slider to test countdown at any date/time

### Unique Sections
- **Quba**: Programmes During Ramadan (Ml. Siraj Saleh, Ml. Ahmed Desai), live stream info
- **Almahad**: "Some Sunnah of Ramadan" 10-item grid (Sahoor, Iftar, Taraweeh, Quran, etc.)
- **Tawakkulia**: Programmes During Ramadan (Taleem, Dars-e-Quran, Bangla Bayan, English Weekend Bayan, Quran Mashq, Late Night Taraweeh)
- **Salahadin**: Full February timetable (pre-Ramadan + Ramadan), Jumu'ah info (Khutba 12:30, Salah 12:50)
- **Abu Bakar**: No unique content sections
- **IYMA**: Donation appeal banner (Phase 3 extension building project), parking notice
- **Jamia Masjid**: No unique content sections (note: Maghrib Salah commences 2 min after Iftar)

### Landing Page (waqt.uk)
- Granim.js animated background (deep blue/teal gradients)
- Card hover effects with per-mosque border glow colors
- Staggered entrance animations on cards
- Subtle Islamic geometric star/octagon pattern overlay
- Enhanced footer with "Ramadan 1447 | Bradford" context
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

## Technical Notes

### Time Parsing
- Sehri/Fajr times are AM (stored as-is, e.g. "5:39")
- Maghrib/Isha times are PM (stored in 12hr format, e.g. "5:26")
- JS converts PM times: `isPM && h < 12 ? h + 12 : h`
- Countdown uses ms-precision Date diffs for live ticking seconds

### Countdown Sequence
```
Sehri ends → Fajr Jamaah → Zuhr begins → Zuhr Jamaah →
Asr begins → Asr Jamaah → Iftar → Isha begins → Isha Jamaah →
(next day's Sehri) → loop
```
After the last day's Isha Jamaah, shows "Eid Mubarak".

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

### nav.js
- Self-executing function that injects CSS, HTML, and event handlers
- Detects active mosque from URL path
- Search filter works on name + address
- Print media query hides nav
- Dark mode aware (`body.dark-mode .masjid-nav`)

### External Dependencies
- **Granim.js v2.0.0** (`cdn.jsdelivr.net/npm/granim@2.0.0/dist/granim.min.js`) - animated gradient backgrounds. Loaded async, cached by service worker, falls back to CSS gradient if unavailable.
- **OpenAI GPT-4o-mini** (via n8n webhook proxy on Railway) - AI prayer times chatbot. n8n workflow "Prayer AI Chat" (ID: `eZayWM5UAKhF8RWA`), webhook path `/webhook/prayer-chat`. Uses Header Auth credential for OpenAI API key.
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

### Git Config
- Repo: `sidnikiwi-afk/Prayer-times`
- Auth: `gh auth setup-git` (credential helper configured)
- Identity: sidnikiwi-afk
