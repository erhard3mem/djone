# This is a automatic Disc Jockey written in Python

from lyricsgenius import Genius
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

genius = Genius("API TOKEN")
max_artists = 4
max_songs = 2 
lyrics = []
artists = []
artists_objects = []

for i in range(0,max_artists):
    artist_input = input("Give me an artist:");    
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

for i in range(1,max_songs*max_artists):   
    for k in range(1,max_songs*max_artists):
        # Calculate cosine similarity between the vectors
        cosine_sim = cosine_similarity(vectorized_text[i-1], vectorized_text[k-1])
        if(i != k):
            #print("Cosine Similarity:", i, k, cosine_sim[0][0])
            similarities.append(cosine_sim[0][0])   
            indexes.append([i-1,k-1])                 


similarities = list(set(similarities))

for i in range(0,len(similarities)):
    for k in range(0,len(indexes)-1):
        if(indexes[k][0] == indexes[i][1] and indexes[k][1] == indexes[i][0]):
            indexes.pop(k);

# Sorting example from OpenAI ChatGPT:
# Create a list of tuples with original values and indices
indexed_nums = [(value, index) for index, value in enumerate(similarities)]

# Sort the indexed_nums list based on values
sorted_nums = sorted(indexed_nums, reverse=True)

# Extract the sorted values and indices
sorted_values = [value for value, _ in sorted_nums]
sorted_indices = [index for _, index in sorted_nums]

print(sorted_values)
#print(sorted_indices)

indices_value = []
for i in sorted_indices:   
    if(i < len(lyrics)):        
        indices_value.append(i);

songs_ordered = []
for a in artists_objects:
    songs_len = len(a.songs)
    for i in range(0,songs_len):
        songs_ordered.append(a.name + " : " + a.songs[i].title)
        
for i in indices_value:
    print(songs_ordered[i]);

