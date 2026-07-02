import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from user_history import load_history
from feedback import load_liked,load_disliked
import pickle



df = pd.read_csv("data/spotify_tracks.csv")

df = df.drop_duplicates(
    subset=["track_name", "artists"]
).reset_index(drop=True)

print("Dataset after removing duplicates:")
print(df.shape)

features = [
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "popularity",
    "loudness"
]

X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

genre_models = {}

for genre, group in df.groupby("track_genre"):

    indices = group.index.to_numpy()

    if len(indices) < 2:
        continue

    genre_vectors = X_scaled[indices]

    knn = NearestNeighbors(
        n_neighbors=min(100, len(indices)),
        metric="cosine"
    )

    knn.fit(genre_vectors)

    genre_models[genre] = {
        "knn": knn,
        "indices": indices
    }

print(f"Trained {len(genre_models)} genre models")

def find_matches(song_name, limit=10):

    matches = df[
        df["track_name"].str.contains(
            song_name,
            case=False,
            na=False
        )
    ]

    if matches.empty:
        return []

    matches = matches.sort_values(
        "popularity",
        ascending=False
    )

    results = []

    for idx, row in matches.head(limit).iterrows():

        results.append(
            {
                "index": idx,
                "song": row["track_name"],
                "artist": row["artists"],
                "genre": row["track_genre"],
                "popularity": row["popularity"]
            }
        )

    return results

def get_mood(song_index):
    row=df.iloc[song_index]

    if row["energy"] > 0.75 and row ["danceability"] > 0.7:
        return "Party"
    
    elif row["valence"] > 0.7:
        return "Happy"
    
    elif row["acousticness"] > 0.7:
        return "Relax"
    
    elif row["energy"] < 0.4:
        return "Sad"
    
    else:
        return "Chill"
    
def get_favorite_genres():

    history=load_history()

    genres=[]

    for item in history:
        if " - " not in item:
            continue

        song_name=item.split(" - ")[0].strip()

        match=df[
            df["track_name"]==song_name
        ]

        if not match.empty:
            genres.append(
                match.iloc[0]["track_genre"]
            )
    return genres


def get_music_personality():

    history=load_history()

    if len(history)==0:
        return None
    
    favorite_genres=get_favorite_genres()

    if len(favorite_genres)==0:
        return None
    
    favorite_genre=pd.Series(
        favorite_genres
    ).value_counts().idxmax()

    if favorite_genre in [
        "pop",
        "dance",
        "edm",
        "electro"
    ]:
        personality="Mainstream Pop Fan"

    elif favorite_genre in [
        "hip-hop",
        "rap",
        "trap"
    ]:
        personality="Hip-Hop Lover"

    elif favorite_genre in [
        "rock",
        "alt-rock",
        "metal"
    ]:
        personality="Rock Enthusiast"

    elif favorite_genre in [
        "acoustic",
        "folk",
        "singer-songwriter"
    ]:
        personality="Acoustic Explorer"

    else:
        personality="Music Explorer"

    return {
        "favorite_genre": favorite_genre,
        "personality": personality
    }

def get_favorite_artist():

    history=load_history()

    artists=[]

    for item in history:

        if " - " not in item:
            continue

        artist=item.split(" - ")[1].strip()

        artist=artist.split(";")[0]

        artists.append(artist)

    if len(artists)==0:
        return None
    
    return (
        pd.Series(artists)
        .value_counts().idxmax()
    )

def get_favorite_mood():
    
    history=load_history()

    moods=[]

    for item in history:

        if " - " not in item:
            continue

        song_name=item.split(" - ")[0].strip()

        match=df[df["track_name"]==song_name]

        if not match.empty:
            mood=get_mood(
                match.index[0]
            )

            moods.append(mood)

    if len(moods)==0:
        return None
    
    return (
        pd.Series(moods)
        .value_counts().idxmax()
    )

def get_top_artists(n=5):

    history=load_history()

    artists=[]

    for item in history:

        if " - " not in item:
            continue

        artist=item.split(" - ")[1].strip()
        artist=artist.split(";")[0]

        artists.append(artist)

    if len(artists)==0:
        return {}
    
    return (
        pd.Series(artists)
        .value_counts()
        .head().to_dict()
    )

def get_top_genres(n=5):
    genres=get_favorite_genres()

    if len(genres)==0:
        return {}
    
    return (
        pd.Series(genres)
        .value_counts()
        .head(n)
        .to_dict()
    )


def _recommend_from_index(song_index, n_results=6):

    selected_song = df.iloc[song_index]["track_name"]
    selected_artist = df.iloc[song_index]["artists"]
    selected_genre = df.iloc[song_index]["track_genre"]

    mood=get_mood(song_index)

    model_entry = genre_models.get(selected_genre)

    if model_entry is None:
        return [], selected_song, selected_artist, selected_genre

    knn = model_entry["knn"]
    genre_indices = model_entry["indices"]

    distances, positions = knn.kneighbors(
        [X_scaled[song_index]]
    )

    history=load_history()
    liked=load_liked()
    disliked=load_disliked()

    favorite_genres=get_favorite_genres()

    favorite_artists=[]

    for item in history:

        if " - " in item:

            favorite_artists.append(
                item.split(" - ")[1].strip()
            )
    seen = set()
    favorite_songs=set(history[-20:])
    recommendations=[]

    genre_avg_popularity=(
        df[df["track_genre"]==selected_genre]
        ["popularity"].mean()
    )

    for distance, pos in zip(
        distances[0],
        positions[0]
    ):

        idx = genre_indices[pos]

        if idx == song_index:
            continue

        row = df.iloc[idx]

        song = row["track_name"]
        artist = row["artists"]
        popularity = row["popularity"]


        if song in seen:
            continue

        seen.add(song)

        similarity = round(
            (1 - distance) * 100,
            2
        )

        artist_bonus = (
            25
            if artist == selected_artist
            else 0
        )

        genre_preference_bonus = (
            20
            if selected_genre in favorite_genres
            else 0
        )

        artist_history_bonus=(
            20
            if artist in favorite_artists
            else 0
        )

        song_history_bonus=(
            20
            if song in favorite_songs
            else 0
        )

        liked_bonus = (
            30
            if song in liked
            else 0
        )

        song = row["track_name"]
        artist = row["artists"]
        popularity = row["popularity"]

        if song in disliked:
            continue

        genre_score=(
            popularity/genre_avg_popularity
        )*15


        # liked_bonus=0

        # if song in liked:
        #     liked_bonus=30

        score = (
            similarity * 0.50
            +
            artist_bonus
            +
            artist_history_bonus
            +
            song_history_bonus
            +
            genre_preference_bonus
            +
            liked_bonus
            +
            genre_score
            +
            popularity * 0.10
        )

        explanations=[]

        if artist==selected_artist:
            explanations.append("Same artist")

        if selected_genre==row["track_genre"]:
            explanations.append("Same genre")

        if popularity > 70:
            explanations.append("Popular Track")

        if similarity > 85:
            explanations.append("Highly similar audio features ")

        if get_mood(idx)==mood:
            explanations.append("Same mood")

        recommendations.append(
            {
                "song": song,
                "artist": artist,
                "genre": selected_genre,
                "mood":get_mood(idx),
                "popularity": popularity,
                "similarity": similarity,
                "score": round(score, 2),
                "same_artist":artist==selected_artist,
                "explanations":explanations
            }
        )

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return (
        recommendations[:n_results],
        selected_song,
        selected_artist,
        selected_genre,
    )


def get_recommendations(song_name, song_index=None):

    if song_index is None:

        matches = df[
            df["track_name"].str.contains(
                song_name,
                case=False,
                na=False
            )
        ]

        if matches.empty:
            return []

        song_index = matches.index[0]

    recommendations, _, _, _ = _recommend_from_index(
        song_index,
        n_results=6
    )

    return recommendations

# REPLACE WITH THIS:
if __name__ == "__main__":
    import os
    os.makedirs("models", exist_ok=True)
    pickle.dump(genre_models, open("models/genre_models.pkl", "wb"))
    pickle.dump(scaler, open("models/scaler.pkl", "wb"))
    print("Models saved successfully")


