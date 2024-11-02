from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from lyricsgenius import Genius
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import webbrowser
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from google.oauth2.credentials import Credentials
#from google_auth_oauthlib.flow import InstalledAppFlow
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from flask_cors import CORS, cross_origin
import requests
import json
import secrets


SECRET_KEY = os.urandom(32)
genius = Genius("N_HS0PvD1iTh5NbeWa7PIk5Y3jr0MsDBT4c4QCSaQiUg6140-i4_D0-dFTDuLHxm")
max_artists = 5
max_songs = 3 
lyrics = []
artists = []
artists_objects = []



# YouTube v3 API
CLIENT_ID = '945610874524-40pmbovkr6lch4cvvg0i8983v2njc5un.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'https://djone-mslf.onrender.com/oauth2callback'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
API_KEY = 'AIzaSyCgNSh4urTC7iAxLssLJw8YceEtdPApdcI'




app = Flask(__name__)
#app.debug = True

app.config['SECRET_KEY'] = SECRET_KEY

#CORS(app)
CORS(app, resources={r"/api/*": {"origins": "https://djone-mslf.onrender.com"}})


csrf = CSRFProtect(app)


@app.after_request
def add_referrer_policy(response):
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

class ArtistsForm(FlaskForm):
    name0 = StringField('Artist 1', validators=[DataRequired()])
    name1 = StringField('Artist 2')
    name2 = StringField('Artist 3')
    name3 = StringField('Artist 4')
    name4 = StringField('Artist 5')
    submit = SubmitField('Generate playlist')


@csrf.exempt
#@cross_origin(origins=['https://djone-mslf.onrender.com/'])
@app.route('/', methods=['GET', 'POST'])
def submit():
    
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secrets_render.json',
        scopes=['https://www.googleapis.com/auth/youtube'],
        state=None)
        
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    creds = flow.credentials

    # Step 2: Initialize YouTube API client
    youtube = build('youtube', 'v3', credentials=creds, scopes=scps)

    # Step 3: Create a new playlist
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

  
    return render_template('index.html', form=form)


@app.route('/login')
def login():
    auth_url = (
        'https://accounts.google.com/o/oauth2/auth?'
        f'client_id={CLIENT_ID}&'
        f'redirect_uri={REDIRECT_URI}&'
        'response_type=code&'
        'scope=https://www.googleapis.com/auth/youtube'
    )
    return redirect(auth_url)

"""@app.route('/oauth2callback')
def oauth2callback():
    code = request.args.get('code')
    if code:
        token_response = requests.post(TOKEN_URL, data={
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code',
        })
        token_json = token_response.json()
        session['credentials'] = token_json  # Speichern der Credentials in der Session
        return redirect(url_for('submit'))
    return 'Fehler beim Anmelden.'
"""
from datetime import datetime, timedelta

@app.route('/oauth2callback')
def oauth2callback():
    code = request.args.get('code')
    if code:
        token_response = requests.post(TOKEN_URL, data={
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code',
        })
        
        token_json = token_response.json()

        print(token_json)

        # Calculate the expiration time
        expires_in = token_json.get('expires_in')
        expiry_time = datetime.utcnow() + timedelta(seconds=expires_in)

        # Save credentials in session
        session['credentials'] = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': token_json.get('refresh_token'),
            'access_token': token_json.get('access_token'),
            'token_uri': TOKEN_URL,
            'scopes': token_json.get('scope').split(),
            'expiry': expiry_time.isoformat() + 'Z'  # Save as ISO 8601 string
        }

        return redirect(url_for('submit'))
    return 'Error during authentication.'



@app.route('/profile')
def profile():
    credentials = session.get('credentials')
    if credentials:
        return f'Du bist angemeldet! {json.dumps(credentials)}'
    return redirect(url_for('submit'))

@app.route('/api/subscriptions')
def subscriptions():
    credentials = session.get('credentials')
    if credentials:
        access_token = credentials['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://www.googleapis.com/youtube/v3/subscriptions', headers=headers)
        return response.json()
    return {'error': 'Unauthorized'}, 401




if __name__ == '__main__': 
    #app.run(host="0.0.0.0")
    app.run(ssl_context=('cert.pem', 'key.pem'))
