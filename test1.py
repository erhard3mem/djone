from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ['https://www.googleapis.com/auth/youtube']

# Start OAuth flow
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secrets_render.json', SCOPES)
creds = flow.run_console()

# Speichere die Anmeldedaten in einer Datei, um sie später zu nutzen
with open('token.pickle', 'wb') as token:
    pickle.dump(creds, token)