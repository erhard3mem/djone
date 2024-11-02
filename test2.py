from google.oauth2 import service_account
from googleapiclient.discovery import build

# Pfad zur JSON-Datei mit dem privaten Schlüssel des Dienstkontos
SERVICE_ACCOUNT_FILE = 'djone-440513-9aa109a76e2f.json'

# Berechtigungs-Scopes festlegen (z. B. für Google Sheets)
SCOPES = ['https://www.googleapis.com/auth/youtube']

# Dienstkonto-Credentials laden
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Erstelle den Google Sheets-API-Service
service = build('youtube', 'v3', credentials=creds)


print("OK")