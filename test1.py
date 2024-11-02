from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ['https://www.googleapis.com/auth/youtube']

# Start OAuth flow
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secrets_desktop.json', SCOPES)
creds = flow.run_local_server(port=0)


print(creds)


# Speichere die Anmeldedaten in einer Datei, um sie später zu nutzen
with open('/home/erhard/token.pickle', 'wb') as token:
    pickle.dump(creds, token)