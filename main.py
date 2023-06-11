# DJone.py: This is a automatic Disc Jockey written in Python

from lyricsgenius import Genius
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import webbrowser

genius = Genius("3NTZjDyL0g5Y8_Q0Ok8JFUbwFraC16PxqZEfG6222t5rkKt5b51yn0-NBPrd8K6L")
max_artists = 3
max_songs = 3 
lyrics = []
artists = []
artists_objects = []

def play(indices):
    index = 0
    for a in artists_objects:
        for s in a.songs:
            i = indices[index][0]           
            if(index == i):
                print(s.title);
            index += 1;


for i in range(0,max_artists):
    artist_input = input("Give me an artist: ");    
    artists.append(artist_input);


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
                print("Cosine Similarity:", i, k, cosine_sim[0][0])   
                similarities.index(cosine_sim[0][0])                                      
            except:
                if(cosine_sim[0][0] < 0.9):
                    similarities.append([cosine_sim[0][0],i,k])   

sorted = sorted(similarities,reverse=True)
print(sorted);

song_indices = []

index = 0
for val in sorted:
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


print(song_indices);

indices_value = []
for i in song_indices:   
    if(i < len(lyrics)):        
        indices_value.append(i);

songs_ordered = []
for a in artists_objects:
    songs_len = len(a.songs)
    for i in range(0,songs_len):
        songs_ordered.append(a.name + " : " + a.songs[i].title)
        
for i in indices_value:
    print(songs_ordered[i]);
    webbrowser.open("https://www.youtube.com/results?search_query="+songs_ordered[i])



