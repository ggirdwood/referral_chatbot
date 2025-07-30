import gspread
import json
import re
from oauth2client.service_account import ServiceAccountCredentials

# === CONFIGURE ===
SPREADSHEET_ID = "1_xqgUyAc3vbKc5vWZXLtccVkhweC8R-4nHZhivB_xu0"  # your Google Sheet ID
WORKSHEET_NAME = "Hospital Referral Mapping"
CREDS_FILE = "google-sheets-creds.json"  # path to your creds JSON file

def clean_key(key):
    """Clean column names to make them safe for JSON keys"""
    return re.sub(r'\s+', '_', key.strip().lower())

def clean_value(value):
    """Convert all line endings to \\n so they show as line breaks in HTML"""
    if isinstance(value, str):
        return value.replace('\r\n', '\n').replace('\r', '\n')
    return value

def main():
    print("🔌 Connecting to Google Sheets...")

    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
    client = gspread.authorize(creds)

    print("📄 Opening worksheet...")
    sheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.worksheet(WORKSHEET_NAME)

    print("📥 Fetching all rows...")
    rows = worksheet.get_all_records()

    print("🧼 Cleaning data...")
    cleaned_data = []
    for row in rows:
        cleaned_row = {
            clean_key(k): clean_value(v)
            for k, v in row.items()
        }
        cleaned_data.append(cleaned_row)

    print(f"💾 Saving to referral_data.json")
    with open("referral_data.json", "w") as f:
        json.dump(cleaned_data, f, indent=2)

    print("✅ Done!")

if __name__ == "__main__":
    main()
