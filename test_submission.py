"""
Test the timetable submission pipeline manually.
Reads an image from the submissions folder, sends to Claude + OpenAI Vision,
validates both extractions, picks the best, and sends Telegram notification.
"""
import base64
import json
import os
import sys
import hashlib
import subprocess
import re

# Config
SUBMISSIONS_DIR = r"G:\My Drive\Prayer_submissions\Timetables"
TELEGRAM_BOT_TOKEN = "8238602157:AAG2fKf3kzOlK8RW51QVI2Oq02sq_aWnvJ8"
TELEGRAM_CHAT_ID = "1578762040"
SQL_WEBHOOK = "https://primary-production-64370.up.railway.app/webhook/sql-query"

def get_api_key(env_name):
    """Get API key from Windows user environment."""
    result = subprocess.run(
        ["powershell", "-Command", f'[System.Environment]::GetEnvironmentVariable("{env_name}", "User")'],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def call_claude(b64_data, mime_type, prompt):
    """Call Claude Vision API via curl."""
    api_key = get_api_key("ANTHROPIC_API_KEY")
    media_type = "image" if mime_type.startswith("image/") else "document"

    body = {
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 8000,
        "messages": [{
            "role": "user",
            "content": [
                {"type": media_type, "source": {"type": "base64", "media_type": mime_type, "data": b64_data}},
                {"type": "text", "text": prompt}
            ]
        }]
    }

    with open("_test_claude.json", "w") as f:
        json.dump(body, f)

    result = subprocess.run([
        "curl", "-s", "-X", "POST", "https://api.anthropic.com/v1/messages",
        "-H", f"x-api-key: {api_key}",
        "-H", "anthropic-version: 2023-06-01",
        "-H", "Content-Type: application/json",
        "-d", "@_test_claude.json"
    ], capture_output=True, text=True, timeout=120)

    os.remove("_test_claude.json")
    return json.loads(result.stdout)

def call_openai(b64_data, mime_type, prompt):
    """Call OpenAI Vision API via curl."""
    api_key = get_api_key("OPENAI_API_KEY")

    body = {
        "model": "gpt-4o",
        "max_tokens": 8000,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64_data}"}},
                {"type": "text", "text": prompt}
            ]
        }]
    }

    with open("_test_openai.json", "w") as f:
        json.dump(body, f)

    result = subprocess.run([
        "curl", "-s", "-X", "POST", "https://api.openai.com/v1/chat/completions",
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Content-Type: application/json",
        "-d", "@_test_openai.json"
    ], capture_output=True, text=True, timeout=120)

    os.remove("_test_openai.json")
    return json.loads(result.stdout)

def parse_ai_response(response, source):
    """Extract JSON from AI response."""
    try:
        if source == "claude":
            text = response["content"][0]["text"]
        else:
            text = response["choices"][0]["message"]["content"]

        clean = re.sub(r'^```json\n?', '', text.strip())
        clean = re.sub(r'\n?```$', '', clean).strip()
        return json.loads(clean), None
    except Exception as e:
        return None, str(e)

def validate(data):
    """Validate timetable data."""
    if not data:
        return 0, ["Failed to parse JSON"]

    errors = []
    if not data.get("name"):
        errors.append("Missing mosque name")

    tt = data.get("timetable", [])
    if not isinstance(tt, list):
        return 0, ["Missing or invalid timetable array"]

    if len(tt) < 28:
        errors.append(f"Only {len(tt)} days (need 30)")
    if len(tt) > 30:
        errors.append(f"{len(tt)} days (expected 30)")

    time_fields = ["sehri", "fajr", "sunrise", "zuhr", "asr", "maghrib", "isha", "jFajr", "jZuhr", "jAsr", "jIsha"]
    for i, d in enumerate(tt):
        if d.get("no") != i + 1:
            errors.append(f"Day {i+1}: wrong no={d.get('no')}")
        for f in time_fields:
            val = d.get(f, "")
            if val and not re.match(r'^\d{1,2}:\d{2}$', str(val)):
                errors.append(f"Day {i+1}: bad {f}={val}")
        date = d.get("date")
        if not isinstance(date, list) or len(date) != 3:
            errors.append(f"Day {i+1}: invalid date")

    score = max(0, 100 - len(errors) * 3)
    return score, errors

def send_telegram(text, drive_file_id="test"):
    """Send Telegram notification with approve/reject buttons."""
    body = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "reply_markup": {
            "inline_keyboard": [[
                {"text": "Approve", "callback_data": f"approve_{drive_file_id[:50]}"},
                {"text": "Reject", "callback_data": f"reject_{drive_file_id[:50]}"}
            ]]
        }
    }

    with open("_test_tg.json", "w") as f:
        json.dump(body, f, ensure_ascii=False)

    result = subprocess.run([
        "curl", "-s", "-X", "POST",
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        "-H", "Content-Type: application/json",
        "-d", "@_test_tg.json"
    ], capture_output=True, text=True)

    os.remove("_test_tg.json")
    return json.loads(result.stdout)

def store_submission(mosque_name, submitter, file_name, drive_file_id, claude_json, openai_json, final_json, notes):
    """Store in Postgres via sql-query webhook."""
    def esc(s):
        if s is None:
            return "NULL"
        return "'" + str(s).replace("'", "''") + "'"

    sql = f"""CREATE TABLE IF NOT EXISTS timetable_submissions (
        id SERIAL PRIMARY KEY, mosque_name TEXT, submitter TEXT, file_name TEXT,
        drive_file_id TEXT, claude_json JSONB, openai_json JSONB, final_json JSONB,
        validation_notes TEXT, status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT NOW()
    );
    INSERT INTO timetable_submissions (mosque_name, submitter, file_name, drive_file_id, claude_json, openai_json, final_json, validation_notes, status)
    VALUES ({esc(mosque_name)}, {esc(submitter)}, {esc(file_name)}, {esc(drive_file_id)},
    {esc(json.dumps(claude_json))}::jsonb, {esc(json.dumps(openai_json))}::jsonb,
    {esc(json.dumps(final_json))}::jsonb, {esc(notes)}, 'pending') RETURNING id"""

    body = {"query": sql}
    with open("_test_sql.json", "w") as f:
        json.dump(body, f)

    result = subprocess.run([
        "curl", "-s", "-X", "POST", SQL_WEBHOOK,
        "-H", "Content-Type: application/json",
        "-d", "@_test_sql.json"
    ], capture_output=True, text=True, timeout=30)

    os.remove("_test_sql.json")
    return result.stdout

PROMPT = """Extract the Ramadan timetable from this image into JSON. Return ONLY valid JSON, no markdown, no code blocks, no explanation.

Schema: {"name":"Mosque Name","short_name":"Short Name","address":"Full address with postcode","phone":"","notes":"","eid_info":"","fitrana":"","donation_info":"","timetable":[{"date":[2026,2,18],"no":1,"day":"Wed","sehri":"5:22","fajr":"5:44","sunrise":"7:20","zuhr":"12:35","asr":"3:45","maghrib":"5:26","isha":"7:30","jFajr":"6:00","jZuhr":"1:15","jAsr":"4:00","jIsha":"7:45"}]}

RULES:
- Ramadan 2026: Feb 18 (Wed) to Mar 19 (Thu) = 30 days
- no = Ramadan day number (1-30)
- Day names: Mon, Tue, Wed, Thu, Fri, Sat, Sun
- All times in H:MM or HH:MM format
- sehri = Suhoor end time
- fajr/zuhr/asr/isha = beginning/start times
- jFajr/jZuhr/jAsr/jIsha = jamaah/congregation times
- maghrib = Maghrib/Iftar time
- sunrise = sunrise time
- If a time column is not shown in the timetable, use empty string
- Extract ALL visible metadata (mosque name, address, phone, bank details, fitrana, eid times)
- Return ONLY the JSON object, nothing else"""

def main():
    # Pick test file
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "IMG-20260211-WA0083 - Shihab Uddin.jpg"

    filepath = os.path.join(SUBMISSIONS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    print(f"Processing: {filename}")

    # Extract submitter from filename (handle "PREFIX - Name.ext" format)
    m = re.search(r'\s+-\s+(.+)\.\w+$', filename)
    submitter = m.group(1).strip() if m else "Unknown"
    print(f"Submitter: {submitter}")

    # Read and encode file
    with open(filepath, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()

    ext = filename.lower().split(".")[-1]
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "pdf": "application/pdf"}
    mime = mime_map.get(ext, "image/jpeg")
    print(f"MIME: {mime}, Size: {len(data)} bytes")

    # Call both AIs in sequence
    print("\nCalling Claude Vision...")
    claude_resp = call_claude(b64, mime, PROMPT)
    claude_data, claude_err = parse_ai_response(claude_resp, "claude")

    print("Calling OpenAI Vision...")
    openai_resp = call_openai(b64, mime, PROMPT)
    openai_data, openai_err = parse_ai_response(openai_resp, "openai")

    # Validate
    claude_score, claude_errors = validate(claude_data)
    openai_score, openai_errors = validate(openai_data)

    print(f"\nClaude: score={claude_score}/100, errors={len(claude_errors)}")
    if claude_errors:
        for e in claude_errors[:5]:
            print(f"  - {e}")

    print(f"OpenAI: score={openai_score}/100, errors={len(openai_errors)}")
    if openai_errors:
        for e in openai_errors[:5]:
            print(f"  - {e}")

    # Pick best
    if claude_score >= openai_score:
        final = claude_data
        source = "claude"
    else:
        final = openai_data
        source = "openai"

    mosque_name = final.get("name", "Unknown") if final else "EXTRACTION FAILED"
    day_count = len(final.get("timetable", [])) if final else 0
    is_valid = final and (claude_score >= 70 or openai_score >= 70)

    print(f"\nBest: {source} | Mosque: {mosque_name} | Days: {day_count} | Valid: {is_valid}")

    # Preview
    if final and final.get("timetable"):
        d1 = final["timetable"][0]
        dL = final["timetable"][-1]
        print(f"Day 1: Fajr {d1.get('fajr','?')}, Maghrib {d1.get('maghrib','?')}, Isha {d1.get('isha','?')}")
        print(f"Day {dL.get('no','?')}: Fajr {dL.get('fajr','?')}, Maghrib {dL.get('maghrib','?')}, Isha {dL.get('isha','?')}")

    # Store in Postgres
    print("\nStoring in Postgres...")
    notes = f"Claude: {claude_score}/100, OpenAI: {openai_score}/100, Best: {source}"
    sql_result = store_submission(mosque_name, submitter, filename, "test_manual", claude_data, openai_data, final, notes)
    print(f"SQL result: {sql_result[:200] if sql_result else 'empty'}")

    # Send Telegram
    print("\nSending Telegram notification...")
    valid_icon = "YES" if is_valid else "NO"
    preview = ""
    if final and final.get("timetable"):
        d1 = final["timetable"][0]
        dL = final["timetable"][-1]
        preview = f"Day 1: Fajr {d1.get('fajr','?')}, Maghrib {d1.get('maghrib','?')}, Isha {d1.get('isha','?')}"
        preview += f"\nDay {dL.get('no','?')}: Fajr {dL.get('fajr','?')}, Maghrib {dL.get('maghrib','?')}, Isha {dL.get('isha','?')}"

    text = f"New Timetable Submission\n\n"
    text += f"Mosque: {mosque_name}\n"
    text += f"Submitter: {submitter}\n"
    text += f"File: {filename}\n"
    text += f"Validation: {valid_icon} ({day_count} days)\n"
    text += f"Best: {source} (Claude {claude_score}, OpenAI {openai_score})\n\n"
    text += preview
    if claude_errors:
        text += f"\n\nClaude issues: {'; '.join(claude_errors[:3])}"
    if openai_errors:
        text += f"\nOpenAI issues: {'; '.join(openai_errors[:3])}"

    tg_result = send_telegram(text)
    print(f"Telegram: {json.dumps(tg_result, indent=2)[:300]}")

    # Save final JSON for review
    if final:
        outpath = os.path.join(os.path.dirname(__file__), f"test_output_{submitter.replace(' ', '_')}.json")
        with open(outpath, "w") as f:
            json.dump(final, f, indent=2)
        print(f"\nFinal JSON saved to: {outpath}")

    print("\nDone!")

if __name__ == "__main__":
    main()
