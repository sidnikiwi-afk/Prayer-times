// Prayer Times Widget for Scriptable (iOS)
// Displays today's prayer times from waqt.uk
// Set mosque via widget parameter: shahjalal, quba, almahad

const MOSQUES = {
  shahjalal: { name: "Shahjalal Islamic Society", path: "shahjalal" },
  quba: { name: "Masjid Quba", path: "quba" },
  almahad: { name: "Al Mahad Ul Islami", path: "Almahad" },
};

const PRAYERS = [
  { label: "Fajr", adhan: "fajr", iqamah: "jFajr", pm: false },
  { label: "Dhuhr", adhan: "zuhr", iqamah: "jZuhr", pm: true },
  { label: "Asr", adhan: "asr", iqamah: "jAsr", pm: true },
  { label: "Maghrib", adhan: "maghrib", iqamah: "maghrib", pm: true },
  { label: "Isha", adhan: "isha", iqamah: "jIsha", pm: true },
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

if (todayEntry) {
  const nextIdx = getNextPrayerIndex(todayEntry, today);
  const widget = buildWidget(mosque.name, todayEntry, nextIdx);
  Script.setWidget(widget);
} else {
  const w = new ListWidget();
  w.backgroundColor = COLORS.bg;
  const t = w.addText("No data available");
  t.textColor = COLORS.text;
  Script.setWidget(w);
}
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
    const iqamahMins = to24(entry[p.iqamah], p.pm);
    if (iqamahMins > nowMins) return i;
  }
  return -1; // All prayers passed
}

function buildWidget(mosqueName, entry, nextIdx) {
  const w = new ListWidget();
  w.backgroundColor = COLORS.bg;
  w.setPadding(12, 14, 12, 14);

  // Mosque name
  const title = w.addText(mosqueName);
  title.font = Font.semiboldSystemFont(14);
  title.textColor = COLORS.text;
  title.centerAlignText();

  w.addSpacer(8);

  // Header row
  const header = w.addStack();
  header.setPadding(0, 4, 4, 4);
  addCell(header, "Prayer", 80, COLORS.headerText, Font.semiboldSystemFont(11), "left");
  addCell(header, "Adhan", 65, COLORS.headerText, Font.semiboldSystemFont(11), "center");
  addCell(header, "Iqamah", 65, COLORS.headerText, Font.semiboldSystemFont(11), "center");

  // Prayer rows
  for (let i = 0; i < PRAYERS.length; i++) {
    const p = PRAYERS[i];
    const isNext = i === nextIdx;

    const row = w.addStack();
    row.setPadding(4, 4, 4, 4);
    row.cornerRadius = 6;
    if (isNext) row.backgroundColor = COLORS.highlight;

    const textColor = isNext ? COLORS.text : COLORS.dimText;
    const font = isNext
      ? Font.semiboldSystemFont(13)
      : Font.regularSystemFont(13);

    addCell(row, p.label, 80, textColor, font, "left");
    addCell(row, entry[p.adhan] || "-", 65, textColor, font, "center");
    addCell(row, entry[p.iqamah] || "-", 65, textColor, font, "center");
  }

  return w;
}

function addCell(stack, text, width, color, font, align) {
  const cell = stack.addStack();
  cell.size = new Size(width, 0);
  if (align === "center") cell.addSpacer();
  const t = cell.addText(text);
  t.font = font;
  t.textColor = color;
  t.lineLimit = 1;
  if (align === "center" || align === "right") cell.addSpacer();
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
