from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Step 1: Authenticate and authorize
scopes = ["https://www.googleapis.com/auth/youtube"]
flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes=scopes)
credentials = flow.run_local_server(port=0)

# Step 2: Initialize YouTube API client
youtube = build('youtube', 'v3', credentials=credentials)

# Step 3: Create a new playlist
request = youtube.playlists().insert(
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
response = request.execute()
playlist_id = response["id"]
print("Created playlist ID:", playlist_id)

# Step 4: Add videos to the playlist
video_ids = ["cUWhxke7E14"]
for video_id in video_ids:
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    print(f"Added video {video_id} to playlist.")
