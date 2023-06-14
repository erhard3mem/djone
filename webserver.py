from flask import Flask, render_template, request, jsonify
from lyricsgenius import Genius
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import webbrowser
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os

SECRET_KEY = os.urandom(32)
genius = Genius("API-TOKEN")
max_artists = 5
max_songs = 3 
lyrics = []
artists = []
artists_objects = []


app = Flask(__name__)
#app.debug = True

app.config['SECRET_KEY'] = SECRET_KEY

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
    submit = SubmitField('Order popular songs by similarity')


@csrf.exempt
@app.route('/', methods=['GET', 'POST'])
def submit():
    form = ArtistsForm()

   # print("before VALIDATE_ON_SUBMIT")


    if request.method == 'POST':
        # Action to be executed when the button is clicked
        artists = []
        if(form.name0.data != ""):
            artists.append(form.name0.data)
        if(form.name1.data != ""):
            artists.append(form.name1.data)
        if(form.name2.data != ""):
            artists.append(form.name2.data)
        if(form.name3.data != ""):
            artists.append(form.name3.data)
        if(form.name4.data != ""):
            artists.append(form.name4.data)
        print(artists)

        lyrics = [] #empty for next session
        artists_objects = []
        for a in artists: 
            artist = genius.search_artist(a, max_songs, sort='popularity')
            artists_objects.append(artist);
            for k in range(0,len(artist.songs)):
                lyrics.append(artist.songs[k].lyrics)                

        # Create a CountVectorizer instance to convert texts into vectors
        vectorizer = CountVectorizer()

        # Fit and transform the texts into vectors
        vectorized_text = vectorizer.fit_transform(lyrics)

        similarities = []
        indexes = []

        for i in range(0,len(lyrics)):   
            for k in range(0,len(lyrics)):
                # Calculate cosine similarity between the vectors
                cosine_sim = cosine_similarity(vectorized_text[i], vectorized_text[k])
                if(i != k):
                    try:
                        #print("Cosine Similarity:", i, k, cosine_sim[0][0])   
                        similarities.index(cosine_sim[0][0])                                      
                    except:
                        if(cosine_sim[0][0] < 0.9):
                            similarities.append([cosine_sim[0][0],i,k])   

        sorted_ = sorted(similarities,reverse=True)
        #print(sorted);

        song_indices = []

        index = 0
        for val in sorted_:
            if(index%2!=1):        
                song_left = val[1]
                song_right = val[2]
                try:
                    song_indices.index(song_left);
                except:
                    song_indices.append(song_left);
                try:
                    song_indices.index(song_right);
                except:
                    song_indices.append(song_right);
            index+=1;


        #print(song_indices);

        indices_value = []
        for i in song_indices:   
            if(i < len(lyrics)):        
                indices_value.append(i);

        songs_ordered = []
        for a in artists_objects:
            songs_len = len(a.songs)
            for i in range(0,songs_len):
                songs_ordered.append(a.name + " : " + a.songs[i].title)
        
        songs = []

        for i in indices_value:
            print(indices_value);
            print(songs_ordered[i]);
            songs.append(songs_ordered[i])
            
            #webbrowser.open("https://www.youtube.com/results?search_query="+songs_ordered[i])


        return jsonify(songs)  

    return render_template('index.html', form=form)


if __name__ == '__main__': 
    app.run(host="0.0.0.0")
