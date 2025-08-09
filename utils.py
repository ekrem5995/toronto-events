import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_sheets_service():
    creds = Credentials.from_service_account_file(
        'credentials.json',
        scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=creds)
    return service

def load_settings(service, spreadsheet_id, sheet_name='Settings'):
    sheet = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{sheet_name}!A1:C'
    ).execute()

    rows = sheet.get('values', [])[1:]  # Skip header
    settings = {}

    for row in rows:
        if len(row) >= 3:
            attribute = row[0].strip()
            weight = float(row[1])
            active = row[2].strip().lower() == "true"
            settings[attribute] = {'weight': weight, 'active': active}
    
    return settings
