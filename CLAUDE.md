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
└── Almahad/
    ├── index.html          # Al Mahad Ul Islami timetable
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

### Donation Details
- **Shahjalal**: Not listed in timetable
- **Quba**: Madressa Islamia Talimuddin, Barclays, Sort: 20-11-81, Acc: 90803383
- **Almahad**: Al Mahadul Islami, Sort: 20-76-92, Acc: 13161595

### Contact / Radio
- **Quba**: Tel 01274 542027 | masjidquba.org | Receiver: 454.3500
- **Almahad**: Receiver: 456.62500

## Features (All Mosques)
- **Today View**: Card-based layout showing today's prayer times only, with pill toggle to switch to Full Timetable. Passed prayers dimmed with checkmark, next prayer highlighted with accent border + "NEXT" badge, tomorrow's Sehri/Iftar preview at bottom. Friday shows "Jumu'ah" instead of Zuhr. View preference saved to localStorage. Auto-refreshes every 60s. Defaults to "Today" during Ramadan, "Full Timetable" otherwise.
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

- **PWA**: manifest.json + sw.js for offline support, installable (all mosques)
- **OG image**: og-image.svg social preview (all mosques)
- **QR poster**: poster.html for A4 printing (all mosques)

### Shahjalal-Only Features
- **Demo mode**: DEMO button (bottom-left), date picker + time slider to test countdown at any date/time

### Unique Sections
- **Quba**: Programmes During Ramadan (Ml. Siraj Saleh, Ml. Ahmed Desai), live stream info
- **Almahad**: "Some Sunnah of Ramadan" 10-item grid (Sahoor, Iftar, Taraweeh, Quran, etc.)

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
- localStorage keys (use unique prefix, e.g. `newmosque-darkMode`, `newmosque-notifications`, `newmosque-viewMode`)
- WhatsApp share URL
- Today View: CSS accent colors, `renderTodayView()`, `setView()`, localStorage key, toggle HTML
- Footer content (Eid times, Fitrana, donation details, notices)
- Any unique sections (programmes, sunnah, etc.)
- Add `<script src="../nav.js"></script>` before `</body>`

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
| Mosque | Dark Mode Key | Notifications Key | View Mode Key |
|--------|--------------|-------------------|---------------|
| Shahjalal | `darkMode` | `notifications` | `viewMode` |
| Quba | `quba-darkMode` | `quba-notifications` | `quba-viewMode` |
| Almahad | `almahad-darkMode` | `almahad-notifications` | `almahad-viewMode` |

### nav.js
- Self-executing function that injects CSS, HTML, and event handlers
- Detects active mosque from URL path
- Search filter works on name + address
- Print media query hides nav
- Dark mode aware (`body.dark-mode .masjid-nav`)

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

### Git Config
- Repo: `sidnikiwi-afk/Prayer-times`
- Auth: `gh auth setup-git` (credential helper configured)
- Identity: sidnikiwi-afk
