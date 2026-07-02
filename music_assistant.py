from recommender import(
    get_music_personality,
    get_favorite_artist,
    get_favorite_mood,
    get_top_genres
)

from user_history import load_history


def ask_music_assistant(query):

    query=query.lower()

    history=load_history()

    personality=get_music_personality()

    favorite_artist=get_favorite_artist()

    favorite_mood=get_favorite_mood()

    genres=get_top_genres()

    if "favorite artist" in query:
        return f"🎤 Your favorite artist is {favorite_artist}"
    
    elif "favorite genre" in query:
        if len(genres) > 0:

            genre=list(genres.keys())[0]
            return f"🎵 Your favorite genre is {genre}"
        
    elif "personlity" in query:
        return (
            f"🧠 Your music personality is "
            f"{personality['personality']}"
        )
    
    elif "songs" in query or "searched" in query:
        return (
            f"📈 You have searched "
            f"{len(history)} songs"
        )
    
    return (
        "I can answer questions about "
        "your music history, favorite "
        "artists, genres, moods and personality."
    )
