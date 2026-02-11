// Prayer Times Widget for Scriptable (iOS)
// Displays today's prayer times from waqt.uk
// Set mosque via widget parameter: shahjalal, quba, almahad

const MOSQUES = {
  shahjalal: { name: "Shahjalal Islamic Society", path: "shahjalal" },
  quba: { name: "Masjid Quba", path: "quba" },
  almahad: { name: "Al Mahad Ul Islami", path: "Almahad" },
};

const PRAYERS = [
  { label: "Fajr", begins: "fajr", iqamah: "jFajr", pm: false },
  { label: "Ishraq", begins: "sunrise", iqamah: null, pm: false },
  { label: "Dhuhr", begins: "zuhr", iqamah: "jZuhr", pm: true },
  { label: "Asr", begins: "asr", iqamah: "jAsr", pm: true },
  { label: "Maghrib", begins: "maghrib", iqamah: "maghrib", pm: true },
  { label: "Isha", begins: "isha", iqamah: "jIsha", pm: true },
];

const COLORS = {
  bg: new Color("#1C1C1E"),
  text: new Color("#FFFFFF"),
  dimText: new Color("#ABABAB"),
  highlight: new Color("#3A3A3C"),
  headerText: new Color("#8E8E93"),
};

// --- Main ---
const mosqueKey = (args.widgetParameter || "shahjalal").toLowerCase().trim();
const mosque = MOSQUES[mosqueKey] || MOSQUES.shahjalal;
const today = new Date();
let todayEntry = null;

try {
  const url = `https://waqt.uk/${mosque.path}/index.html`;
  const html = await new Request(url).loadString();
  const data = parseTimetableData(html);
  todayEntry = findToday(data, today);
  if (todayEntry) cacheData(mosqueKey, todayEntry);
} catch (e) {
  // Network failed — try cache
  todayEntry = loadCache(mosqueKey);
}

let widget;
if (todayEntry) {
  const nextIdx = getNextPrayerIndex(todayEntry, today);
  widget = buildWidget(mosque.name, todayEntry, nextIdx);
} else {
  widget = new ListWidget();
  widget.backgroundColor = COLORS.bg;
  const t = widget.addText("No data available");
  t.textColor = COLORS.text;
}

Script.setWidget(widget);
if (!config.runsInWidget) await widget.presentMedium();
Script.complete();

// --- Functions ---

function parseTimetableData(html) {
  const match = html.match(
    /const\s+timetableData\s*=\s*\[([\s\S]*?)\];\s*\n/
  );
  if (!match) return [];

  let jsonStr = "[" + match[1] + "]";
  // Strip JS comments
  jsonStr = jsonStr.replace(/\/\/.*$/gm, "");
  // Convert date arrays: date: [2026, 2, 18] → date: "2026-2-18"
  jsonStr = jsonStr.replace(
    /date:\s*\[(\d+),\s*(\d+),\s*(\d+)\]/g,
    'date: "$1-$2-$3"'
  );
  // Quote unquoted keys (only after { or , to avoid matching inside strings)
  jsonStr = jsonStr.replace(/([{,])\s*(\w+)\s*:/g, '$1"$2":');

  try {
    return JSON.parse(jsonStr);
  } catch (e) {
    return [];
  }
}

function findToday(data, now) {
  const key = `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}`;
  return data.find((d) => d.date === key) || null;
}

function to24(timeStr, isPm) {
  if (!timeStr) return 0;
  const [h, m] = timeStr.split(":").map(Number);
  if (isPm && h < 12) return (h + 12) * 60 + m;
  return h * 60 + m;
}

function getNextPrayerIndex(entry, now) {
  const nowMins = now.getHours() * 60 + now.getMinutes();
  for (let i = 0; i < PRAYERS.length; i++) {
    const p = PRAYERS[i];
    const field = p.iqamah || p.begins;
    const mins = to24(entry[field], p.pm);
    if (mins > nowMins) return i;
  }
  return -1; // All prayers passed
}

function buildWidget(mosqueName, entry, nextIdx) {
  const w = new ListWidget();
  w.backgroundColor = COLORS.bg;
  w.setPadding(10, 16, 10, 16);

  // Mosque name
  const title = w.addText(mosqueName);
  title.font = Font.boldSystemFont(16);
  title.textColor = COLORS.text;
  title.centerAlignText();

  w.addSpacer(6);

  // Header row
  addRow(w, "Prayer", "Begins", "Iqamah", COLORS.headerText, Font.semiboldSystemFont(12), false);

  w.addSpacer(2);

  // Prayer rows
  for (let i = 0; i < PRAYERS.length; i++) {
    const p = PRAYERS[i];
    const isNext = i === nextIdx;
    const textColor = isNext ? COLORS.text : COLORS.dimText;
    const font = isNext ? Font.semiboldSystemFont(14) : Font.regularSystemFont(14);
    const beginsVal = entry[p.begins] || "";
    const iqamahVal = p.iqamah ? (entry[p.iqamah] || "") : "";

    addRow(w, p.label, beginsVal, iqamahVal, textColor, font, isNext);

    if (i < PRAYERS.length - 1) w.addSpacer(0);
  }

  w.addSpacer();
  return w;
}

function addRow(w, col1, col2, col3, color, font, highlight) {
  const row = w.addStack();
  row.setPadding(5, 8, 5, 8);
  row.cornerRadius = 8;
  if (highlight) row.backgroundColor = COLORS.highlight;

  const c1 = row.addStack();
  c1.size = new Size(100, 0);
  const t1 = c1.addText(col1);
  t1.font = font;
  t1.textColor = color;
  t1.lineLimit = 1;

  row.addSpacer();

  const t2 = row.addText(col2);
  t2.font = font;
  t2.textColor = color;
  t2.lineLimit = 1;

  row.addSpacer();

  const c3 = row.addStack();
  c3.addSpacer();
  const t3 = c3.addText(col3);
  t3.font = font;
  t3.textColor = color;
  t3.lineLimit = 1;
}

// --- Cache ---
function cacheData(key, entry) {
  const fm = FileManager.local();
  const path = fm.joinPath(fm.documentsDirectory(), `prayer_${key}.json`);
  fm.writeString(path, JSON.stringify(entry));
}

function loadCache(key) {
  const fm = FileManager.local();
  const path = fm.joinPath(fm.documentsDirectory(), `prayer_${key}.json`);
  if (fm.fileExists(path)) {
    try {
      return JSON.parse(fm.readString(path));
    } catch (e) {
      return null;
    }
  }
  return null;
}
