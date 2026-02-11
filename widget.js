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

const BG = new Color("#000000");
const WHITE = Color.white();
const GREY = new Color("#8E8E93");
const HIGHLIGHT = new Color("#3A3A3C");

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
  todayEntry = loadCache(mosqueKey);
}

let widget;
if (todayEntry) {
  const nextIdx = getNextPrayerIndex(todayEntry, today);
  widget = buildWidget(mosque.name, todayEntry, nextIdx);
} else {
  widget = new ListWidget();
  widget.backgroundColor = BG;
  const t = widget.addText("No data available");
  t.textColor = WHITE;
}

Script.setWidget(widget);
if (!config.runsInWidget) await widget.presentMedium();
Script.complete();

// --- Build Widget ---

function buildWidget(mosqueName, entry, nextIdx) {
  const w = new ListWidget();
  w.backgroundColor = BG;
  w.setPadding(12, 16, 12, 16);

  // Title
  const title = w.addText(mosqueName);
  title.font = Font.boldSystemFont(16);
  title.textColor = WHITE;
  title.centerAlignText();

  w.addSpacer();

  // Header
  const hdr = w.addStack();
  hdr.setPadding(0, 8, 0, 0);
  addFixedCol(hdr, "Prayer", 90, Font.mediumSystemFont(13), GREY, "left");
  addFixedCol(hdr, "Begins", 80, Font.mediumSystemFont(13), GREY, "center");
  hdr.addSpacer();
  addFixedCol(hdr, "Iqamah", 80, Font.mediumSystemFont(13), GREY, "center");

  w.addSpacer();

  // Prayer rows
  for (let i = 0; i < PRAYERS.length; i++) {
    const p = PRAYERS[i];
    const isNext = i === nextIdx;
    const beginsRaw = entry[p.begins] || "";
    const iqamahRaw = p.iqamah ? (entry[p.iqamah] || "") : "";
    const begins24 = beginsRaw;
    const iqamah24 = p.iqamah ? iqamahRaw : "";

    const row = w.addStack();
    row.setPadding(6, 8, 6, 0);
    row.cornerRadius = 8;
    if (isNext) row.backgroundColor = HIGHLIGHT;

    const font = Font.boldSystemFont(15);

    addFixedCol(row, p.label, 90, font, WHITE, "left");
    addFixedCol(row, begins24, 80, font, WHITE, "center");
    row.addSpacer();
    addFixedCol(row, iqamah24, 80, font, WHITE, "center");

    if (i < PRAYERS.length - 1) w.addSpacer();
  }

  w.addSpacer(4);
  return w;
}

function addLabel(stack, text, font, color) {
  const t = stack.addText(text);
  t.font = font;
  t.textColor = color;
  t.lineLimit = 1;
}

function addFixedCol(stack, text, width, font, color, align) {
  const col = stack.addStack();
  col.size = new Size(width, 0);
  if (align === "center" || align === "right") col.addSpacer();
  addLabel(col, text || "", font, color);
  if (align === "center" || align === "left") col.addSpacer();
}

// --- Data ---

function parseTimetableData(html) {
  const match = html.match(
    /const\s+timetableData\s*=\s*\[([\s\S]*?)\];\s*\n/
  );
  if (!match) return [];

  let jsonStr = "[" + match[1] + "]";
  jsonStr = jsonStr.replace(/\/\/.*$/gm, "");
  jsonStr = jsonStr.replace(
    /date:\s*\[(\d+),\s*(\d+),\s*(\d+)\]/g,
    'date: "$1-$2-$3"'
  );
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

function to24mins(timeStr, isPm) {
  if (!timeStr) return 0;
  const [h, m] = timeStr.split(":").map(Number);
  if (isPm && h < 12) return (h + 12) * 60 + m;
  return h * 60 + m;
}

function to24str(timeStr, isPm) {
  if (!timeStr) return "";
  const [h, m] = timeStr.split(":").map(Number);
  let h24 = isPm && h < 12 ? h + 12 : h;
  return `${h24}:${String(m).padStart(2, "0")}`;
}

function getNextPrayerIndex(entry, now) {
  const nowMins = now.getHours() * 60 + now.getMinutes();
  for (let i = 0; i < PRAYERS.length; i++) {
    const p = PRAYERS[i];
    const field = p.iqamah || p.begins;
    const mins = to24mins(entry[field], p.pm);
    if (mins > nowMins) return i;
  }
  return -1;
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
