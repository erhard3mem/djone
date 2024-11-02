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
youtube = build('youtube', 'v3', credentials=creds)

api_request = youtube.playlists().insert(
    part="snippet,status",
    body={
    "snippet": {
        "title": "DJone playlist",
        "description": "Created with YouTube API",
        "tags": ["API", "YouTube"],
        "defaultLanguage": "en"
    },
    "status": {
        "privacyStatus": "public"
    }
    }
)
response = api_request.execute()
playlist_id = response["id"]
print("Created playlist ID:", playlist_id)

print("OK")