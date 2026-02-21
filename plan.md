# Timetable Submission Automation — Implementation Plan

## Overview
Two n8n workflows that automate processing of timetable submissions from Google Drive, using AI vision to extract data, validating it, and sending Telegram notifications for approval.

## Architecture

```
Google Form → Drive folder → n8n Workflow 1 → AI extract → Validate → Telegram notify
                                                                         ↓
Telegram approve button → n8n Workflow 2 → GitHub commit data.json → Notify done
```

## Prerequisites (manual setup needed)

1. **Google Drive folder ID** — need the folder ID for `G:\My Drive\Prayer_submissions\Timetables` (from the URL when viewing in browser)
2. **n8n credentials to create**:
   - **Telegram Bot API** — using existing bot token (`TELEGRAM_BOT_TOKEN` env var from Flight_scraper)
   - **Google Drive OAuth2** — may already exist if Google Sheets OAuth is configured (same Google account)
   - **Anthropic API** — for Claude vision extraction (HTTP Header Auth with API key)
   - **GitHub API** — for committing data.json (Personal Access Token, HTTP Header Auth)

## Workflow 1: "Timetable Submission Processor"

### Nodes:

1. **Google Drive Trigger** (poll every 5 min)
   - Watch folder: `Prayer_submissions/Timetables`
   - Event: `fileCreated`
   - Returns file metadata (name, id, mimeType)

2. **Google Drive Download**
   - Download the file by ID from trigger output
   - Returns binary data (image/PDF)

3. **Code Node — Prepare AI Request**
   - Convert binary to base64
   - Build Claude API request body with vision prompt
   - Prompt instructs Claude to extract timetable into exact data.json schema (30 days, all time fields)

4. **HTTP Request — Claude Vision API**
   - POST `https://api.anthropic.com/v1/messages`
   - Send image with extraction prompt
   - Claude returns structured JSON matching data.json schema

5. **Code Node — Validate Extracted Data**
   - Check 30 days present
   - Date sequence Feb 18 → Mar 19
   - All time fields in HH:MM format
   - Jamaah times after beginning times
   - Time sanity ranges (sehri 4-6am, maghrib 4-7pm, etc.)
   - Day names match dates
   - Returns validation result + cleaned JSON

6. **IF Node — Valid?**
   - Branch on validation pass/fail

7. **Code Node — Format Telegram Message**
   - Build summary: mosque name, submitter, date range, sample times
   - If validation failed: include error list
   - Build inline keyboard: `[Approve ✓] [Reject ✗]`
   - Store extracted JSON in workflow static data (keyed by callback ID)

8. **Telegram — Send Notification**
   - Send to chat ID `1578762040`
   - Parse mode: HTML
   - Include inline keyboard for approve/reject
   - Message includes: mosque name, submitter name (from filename), validation status, first/last day preview

### Telegram Message Format:
```
📋 New Timetable Submission

Mosque: Shahjalal Jami Masjid
Submitter: Saarah Islam
File: sjm-ramadan-2026.pdf
Validation: ✅ PASSED (30 days, all times valid)

Day 1 (Feb 18): Fajr 5:44, Zuhr 12:35, Asr 3:45, Maghrib 5:26, Isha 7:30
Day 30 (Mar 19): Fajr 4:48, Zuhr 12:19, Asr 4:12, Maghrib 6:06, Isha 7:52

Jamaah: jFajr 6:00, jZuhr 1:15, jAsr varies, jIsha varies
```

## Workflow 2: "Timetable Approval Handler"

### Nodes:

1. **Telegram Trigger**
   - Trigger on: `callback_query` (inline keyboard button clicks)

2. **Code Node — Parse Callback**
   - Extract callback data (approve/reject + submission ID)
   - Retrieve stored JSON from Workflow 1's static data (via n8n API or shared storage)

3. **IF Node — Approve or Reject?**

4. **On Approve path:**
   a. **Code Node — Build data.json**
      - Format the validated JSON into proper data.json structure
      - Generate prefix from mosque name

   b. **HTTP Request — GitHub API**
      - PUT `https://api.github.com/repos/sidnikiwi-afk/Prayer-times/contents/Masjids/{name}/data.json`
      - Creates/updates the file in the repo
      - Commit message: "Add timetable for {mosque name} via automation"

   c. **Telegram — Answer Callback + Confirm**
      - Answer callback query (removes loading spinner)
      - Send confirmation: "✅ data.json committed to GitHub. Run generation pipeline locally to deploy."

5. **On Reject path:**
   a. **Telegram — Answer Callback + Confirm**
      - Send: "❌ Submission rejected. No changes made."

## Shared Data Between Workflows

The extracted JSON needs to pass from Workflow 1 → Workflow 2. Options:
- **Option A (simplest)**: Store in a Google Sheet row (submission_id, mosque_name, json_data, status)
- **Option B**: Use n8n static data API
- **Option C**: Store in Postgres leads DB (new `timetable_submissions` table)

**Recommendation: Option A** — Google Sheet as a simple queue. Workflow 1 writes, Workflow 2 reads by ID.

## Implementation Steps

1. Get Google Drive folder ID from user
2. Create n8n credentials (Telegram Bot, Anthropic API, GitHub PAT)
3. Create a "Timetable Submissions" Google Sheet (columns: id, mosque_name, submitter, file_name, extracted_json, validation_status, approval_status, created_at)
4. Build Workflow 1 (Google Drive Trigger → AI → Validate → Telegram)
5. Build Workflow 2 (Telegram Trigger → GitHub commit)
6. Test with one of the existing submission files
7. Activate both workflows

## Post-Approval Manual Steps (for now)
After data.json is committed to GitHub:
1. `git pull` in Prayer-times repo
2. `python Masjids/generate.py`
3. Copy HTML to prefix folder
4. `python Masjids/gen_pwa.py`
5. `python Masjids/update_landing.py`
6. Update nav.js
7. Commit and push

(Future: GitHub Actions could automate steps 2-7)
