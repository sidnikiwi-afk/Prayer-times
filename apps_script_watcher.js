/**
 * Google Apps Script - Timetable Submission Watcher
 *
 * Watches the Prayer Submissions folder for new files and sends
 * the file ID to the n8n webhook for processing.
 *
 * SETUP:
 * 1. Go to https://script.google.com
 * 2. Create new project, paste this code
 * 3. Run setup() once (will ask for Drive permissions)
 * 4. Done! The trigger runs every minute automatically.
 *
 * The script stores processed file IDs in Script Properties
 * so it never processes the same file twice.
 */

const FOLDER_ID = '1khMM9ZH_J7HH7Dcx4uRMdNP-S2mPoOAN8Xy52iwQz7pmqYEg0XXSAPppxCGn9novB2rPBmVc';
const WEBHOOK_URL = 'https://primary-production-64370.up.railway.app/webhook/timetable-submission';

/**
 * Run this ONCE to set up the trigger.
 */
function setup() {
  // Remove any existing triggers
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));

  // Create time-based trigger: check every minute
  ScriptApp.newTrigger('checkForNewFiles')
    .timeBased()
    .everyMinutes(1)
    .create();

  // Store current file IDs so we don't process existing files
  const folder = DriveApp.getFolderById(FOLDER_ID);
  const files = folder.getFiles();
  const existing = {};
  while (files.hasNext()) {
    const file = files.next();
    existing[file.getId()] = true;
  }
  PropertiesService.getScriptProperties().setProperty('processedFiles', JSON.stringify(existing));

  Logger.log('Setup complete. ' + Object.keys(existing).length + ' existing files tracked. Trigger created.');
}

/**
 * Runs every minute. Checks for new files and sends to n8n webhook.
 */
function checkForNewFiles() {
  const folder = DriveApp.getFolderById(FOLDER_ID);
  const props = PropertiesService.getScriptProperties();

  // Load processed file IDs
  let processed = {};
  try {
    processed = JSON.parse(props.getProperty('processedFiles') || '{}');
  } catch (e) {
    processed = {};
  }

  // Check all files in folder
  const files = folder.getFiles();
  let newCount = 0;

  while (files.hasNext()) {
    const file = files.next();
    const fileId = file.getId();

    // Skip already processed files
    if (processed[fileId]) continue;

    // Skip files with "TEST" in name (test files)
    const fileName = file.getName();
    if (fileName.toUpperCase().startsWith('TEST')) continue;

    // New file found! Send to webhook
    Logger.log('New file: ' + fileName + ' (' + fileId + ')');

    try {
      const response = UrlFetchApp.fetch(WEBHOOK_URL, {
        method: 'post',
        contentType: 'application/json',
        payload: JSON.stringify({
          fileId: fileId,
          fileName: fileName,
          mimeType: file.getMimeType(),
          createdDate: file.getDateCreated().toISOString()
        }),
        muteHttpExceptions: true
      });

      const code = response.getResponseCode();
      Logger.log('Webhook response: ' + code + ' - ' + response.getContentText().substring(0, 200));

      // Mark as processed regardless of response (avoid infinite retries)
      processed[fileId] = true;
      newCount++;

    } catch (e) {
      Logger.log('Error sending to webhook: ' + e.message);
      // Don't mark as processed - will retry next minute
    }
  }

  // Save updated processed list
  if (newCount > 0) {
    props.setProperty('processedFiles', JSON.stringify(processed));
    Logger.log('Processed ' + newCount + ' new file(s)');
  }
}

/**
 * Manual test: processes the most recent file in the folder.
 */
function testWithLatestFile() {
  const folder = DriveApp.getFolderById(FOLDER_ID);
  const files = folder.getFiles();

  let latest = null;
  let latestDate = new Date(0);

  while (files.hasNext()) {
    const file = files.next();
    if (file.getDateCreated() > latestDate) {
      latest = file;
      latestDate = file.getDateCreated();
    }
  }

  if (!latest) {
    Logger.log('No files found');
    return;
  }

  Logger.log('Testing with: ' + latest.getName() + ' (' + latest.getId() + ')');

  const response = UrlFetchApp.fetch(WEBHOOK_URL, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({
      fileId: latest.getId(),
      fileName: latest.getName(),
      mimeType: latest.getMimeType(),
      createdDate: latest.getDateCreated().toISOString()
    }),
    muteHttpExceptions: true
  });

  Logger.log('Response: ' + response.getResponseCode());
  Logger.log('Body: ' + response.getContentText().substring(0, 500));
}

/**
 * Reset: clears all tracked files so everything gets reprocessed.
 */
function resetTracking() {
  PropertiesService.getScriptProperties().deleteProperty('processedFiles');
  Logger.log('Tracking reset. All files will be treated as new on next run.');
}
