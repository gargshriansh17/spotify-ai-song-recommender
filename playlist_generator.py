import pandas as pd
import random

df=pd.read_csv("data/spotify_tracks.csv")

def generate_playlist(mood,size=15):

    mood=mood.lower()

    if mood=="party":

        songs=df[
            (df["energy"] > 0.75)
            &
            (df["danceability"] > 0.70)
        ]

    elif mood=="happy":

        songs=df[
            df["valence"] > 0.70
        ]

    elif mood=="sad":

        songs=df[
            df["energy"] < 0.40
        ]

    elif mood=="relax":

        songs=df[
            df["acousticness"] > 0.70
        ]

    else:

        songs=df.sample(100)

    

    playlist=songs.sample(
        min(size,len(songs))
    )

    return playlist


def generate_playlist_name(mood):

    name={

        "Party":[
            "🔥 Weekend Chaos",
            "⚡ Adrenaline Rush",
            "🎉 Dance Floor Takeover",
            "🚀 Energy Boost",
            "💃 Party Starter"
        ],

        "Happy":[
            "☀️ Good Vibes Only",
            "😊 Smile Mode",
            "🌈 Feel Good Hits",
            "✨ Happy Place",
            "🎵 Sunshine Playlist"
        ],

        "Relax":[
            "🌙 Late Night Vibes",
            "☕ Coffee & Chill",
            "🌿 Peaceful Moments",
            "✨ Calm Waves",
            "🎧 Relax Mode"
        ],

        "Sad":[
            "💔 Broken Hearts Club",
            "🌧 Rainy Day Thoughts",
            "🌙 Midnight Therapy",
            "🥀 Melancholy Mix",
            "🎵 Emotional Escape"
        ]
    }

    return random.choice(
        name.get(
            mood,
            ["🎵 My Playlist"]
        )
    )

playlist = generate_playlist("Relax")

