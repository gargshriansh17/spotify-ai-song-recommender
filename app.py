import streamlit as st
from streamlit_option_menu import option_menu
from recommender import (
    get_recommendations, 
    find_matches,
    get_music_personality,
    get_favorite_artist,
    get_favorite_mood,
    get_top_artists,
    get_top_genres,
    df
)

from components.recommendation_card import recommendation_card
from spotify_api import get_track_info
from user_history import save_song,load_history
from playlist_generator import (
    generate_playlist,
    generate_playlist_name
    )

from feedback import (
    save_liked,
    save_disliked
)
from nlp_search import detect_mood
from music_assistant import ask_music_assistant
import pandas as pd
import plotly.express as px


all_songs=(
    df["track_name"]
    .dropna()
    .unique()
    .tolist()
)


st.set_page_config(
    page_title="Song system",
    page_icon="🎵",
    layout="wide"
)

with open("style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

with st.sidebar:

    st.markdown("# 🎵 Spotify AI")

    history = load_history()

    if history:
        st.markdown("### Recent Searches")

    for song in history:
        st.write("🎵", song)

    selected = option_menu(
        menu_title=None,
        options=[
            "Home",
            "Recommend",
            "Playlists",
            "Favorites",
            "History",
            "Analytics",
            "Assistant",
            "Settings"
        ],
        icons=[
            "house",
            "music-note",
            "bar-chart",
            "gear"
        ],
        default_index=0,

        styles={
        "container": {
            "padding": "8px",
            "background-color": "#020617",
            "border-radius": "16px"
        },

        "nav-link": {
            "font-size": "20px",
            "font-weight": "500",
            "text-align": "left",
            "margin": "6px 0",
            "padding": "14px",
            "border-radius": "12px",
            "transition": "all 0.3s ease"
        },

        "nav-link-selected": {
            "background": "linear-gradient(90deg,#8b5cf6,#3b82f6)",
            "color": "white",
            "font-weight": "700"
        }
        }
    )
    st.write(selected)

if selected=="Home":
    st.markdown(
        """
        <div class='main-title'>
        🎵 Song System
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
    """
    <div class='card'>
        <h2>🎧 Find Your Next Favorite Song</h2>
        <p>
        AI-powered recommendations from
        81,000+ tracks across 114 genres.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown(
        """
        <div class='subtitle'>
        Machine Learning Powered Song Discovery
        </div>
        """,
        unsafe_allow_html=True 
    )

    st.write("")

    col1,col2,col3=st.columns(3)

    with col1:
        st.metric(
            "Songs",
            "81,343"
        )

    with col2:
        st.metric(
            "Genres",
            "114"
        )

    st.write("")
    st.write("")

    st.markdown("---")

    st.markdown(
        """
        <div class='card'>
        <h2>Discover Music with AI</h2>
        <p>
        Search from 81,000+ songs and get
        recommendations powered by
        machine learning.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )
        
        
    st.markdown("---")

    st.subheader(
        "🤖 AI Music Search"
    )

    query=st.text_input(
        "Describe the music you want"
    )

    if query:

        detected_mood=detect_mood(query)

        st.write("Detected:", detected_mood)

        if detected_mood:
            st.success(
                f"Detected Mood:{detected_mood}"
            )

            playlist=generate_playlist(detected_mood)

            st.write(
                f"### Recommended {detected_mood} Playlist"
            )

            for _,row in playlist.iterrows():

                st.write(
                    f"🎵 {row['track_name']} - {row['artists']}"
                )

# ----------------------
# RECOMMEND PAGE
# ----------------------

elif selected=="Recommend":

    st.title("🎧 AI Song Recommender")

    history = load_history()

    if history:
        st.subheader("🕒 Recent Searches")

        for song in history:
            st.write("•", song)

        st.markdown("---")

    selected_song=st.selectbox(
        "🔍 Search Song",
        options=all_songs,
        index=None,
        placeholder="Start typing a song..."
    )

    if selected_song:

        if st.button("🎵 Get Recommendations"):

            save_song(selected_song)

            st.session_state["current_song"]=selected_song

            results=get_recommendations(selected_song)

            st.write("Recommendations found:",len(results))
            # print("Recommendations:",len(results))

            st.session_state["recommend_results"]=results

    # song=st.text_input("Enter Song Name")

    # matches=[]

    # if song:
    #     matches=find_matches(song)

    # if song and not matches: 
    #     st.error("Song Not Found")

    # if matches:
    #     options = [
    #         f"{m['song']} — {m['artist']} ({m['genre']})"
    #         for m in matches
    #     ]

    #     chosen_label = st.selectbox(
    #         "Did you mean:",
    #         options
    #     )
    #     chosen_position = options.index(chosen_label)
    #     chosen_match = matches[chosen_position]

        # if st.button("Get Recommendations"):

        #     save_song(
        #         f"{chosen_match['song']} - {chosen_match['artist']}"
        #     )

        #     st.session_state["current_song"]=chosen_match["song"]
            

        #     st.session_state["recommend_results"] = (get_recommendations(
        #         chosen_match["song"],
        #         song_index=chosen_match["index"]
        #         )
        #     )

    results = st.session_state.get("recommend_results")

    if results is not None:
        if len(results)==0:
            st.error("No recommendations found for this song's genre.")

        else:
            cols=st.columns(3)

            for i,result in enumerate(results):
                with cols[i%3]:

                    spotify_data = get_track_info(
                        result["song"]
                    )

                    if spotify_data is None:
                        album_cover = None
                        spotify_url = None
                    else:
                        album_cover = spotify_data["album_cover"]
                        spotify_url = spotify_data["spotify_url"]

                    st.caption(
                        f"🎭 Mood: {result['mood']}"
                    )
                    
                    recommendation_card(
                        result["song"],
                        result["artist"],
                        result["similarity"],
                        result["mood"],
                        result["genre"],
                        result["popularity"],
                        album_cover,
                        spotify_url
                    )

                    st.caption("Why Recommended:")

                    st.info(
                        "\n".join(result["explanations"])
                    )

                    col1,col2=st.columns(2)

                    with col1:
                        if st.button(
                            "👍 Like",
                            key=f"like_{i}"
                        ):
                            save_liked(result["song"])

                    with col2:
                        if st.button(
                            "👎 Dislike",
                            key=f"dislike_{i}"
                        ):
                            save_disliked(result["song"])

# ----------------------
# ANALYTICS PAGE
# ----------------------

elif selected=="Analytics":
    from user_history import load_history

    st.title("📊 User Analytics")

    history=load_history()

    from feedback import (
        load_liked,
        load_disliked
    )

    liked=load_liked()
    disliked=load_disliked()

    most_played_song=None

    if len(history) > 0:
        most_played_song=(
            pd.Series(history)
            .value_counts()
            .idxmax()
        )

    total_likes=len(liked)
    total_dislikes=len(disliked)

    st.metric(
        "Songs Searched",
        len(history)
    )

    personality=get_music_personality()

    favorite_artist=get_favorite_artist()

    favorite_mood=get_favorite_mood()

    top_artists=get_top_artists()

    top_genres=get_top_genres()

    if len(history) < 10:        
        level = "Beginner Listener"

    elif len(history) < 30:        
        level = "Music Explorer"

    elif len(history) < 60:        
        level = "Music Enthusiast"

    else:
        level = "Music Expert"

        st.metric(
            "🏆 Listener Level",
            level
        )
    if personality:
        st.markdown("---")

        st.subheader(
            "🎵 Spotify Wrapped 2026"
        )
        wrapped_data = {
        "artist": favorite_artist,
        "genre": personality["favorite_genre"],
        "mood": favorite_mood,
        "personality": personality["personality"],
        "songs": len(history),
        "level": level,
        "top_song": most_played_song,
        "likes": total_likes,
        "dislikes": total_dislikes
    }
        st.info(
        f"""
    🎤 Top Artist: {wrapped_data['artist']}

    🎶 Top Genre: {wrapped_data['genre']}

    😊 Favorite Mood: {wrapped_data['mood']}

    📈 Songs Searched: {wrapped_data['songs']}

    🧠 Music Personality: {wrapped_data['personality']}

    🏆 Listener Level: {wrapped_data['level']}

    🔥 Most Played Song: {wrapped_data['top_song']}

    👍 Total Likes: {wrapped_data['likes']}

    👎 Total Dislikes: {wrapped_data['dislikes']}
    """
    )
        
        st.markdown("---")

        st.subheader(
            "🎵 Your Music Personality"
        )

        st.info(
            f"""
        Favorite Artist:{favorite_artist}

        Favorite Genre: {personality['favorite_genre']}

        Favorite Mood:{favorite_mood}

        Listening Style: {personality['personality']}
        """
        )

        st.markdown("---")

        st.subheader("🎵 Your Spotify Wrapped")

        col1,col2=st.columns(2)

        with col1:
            st.write("### 🎤 Top Artists")

            for artist,count in top_artists.items():
                st.write(f"{artist} ({count})")

        with col2:
            st.write("### 🎵 Top Genres")

            for genre,count in top_genres.items():
                st.write(f"{genre} ({count})")

        
        st.markdown("---")


        st.markdown("---")
        st.subheader("📈 Listening Trends")

    if len(top_genres) > 0:
        genre_df=pd.DataFrame(
            list(top_genres.items()),
            columns=["Genre","Count"]
        )

        fig=px.bar(
            genre_df,
            x="Genre",
            y="Count",
            title="Favorite Genres"
        )

        st.plotly_chart(
            fig,
             width="stretch"
        )

    
    if len(top_artists) > 0:

        artist_df = pd.DataFrame(
            list(top_artists.items()),
            columns=["Artist", "Count"]
        )

        fig = px.pie(
            artist_df,
            names="Artist",
            values="Count",
            title="Top Artists"
        )

        st.plotly_chart(
            fig,
             width="stretch"
        )



    if history:
        st.subheader(
            "Recently Searched Songs"
        )

        for song in history[-10:][::-1]:
            st.write("🎵",song)


elif selected=="Playlists":
    st.title("🎵 Smart Playlist Generator")

    mood=st.selectbox(
        "Choose Mood",
        [
            "Party",
            "Happy",
            "Relax",
            "Sad"
        ]
    )

    if st.button("Generate PLaylist"):
        playlist=generate_playlist(mood)

        st.session_state["playlist"]=playlist

    playlist=st.session_state.get(
        "playlist"
    )

    if playlist is not None:
        playlist_name = generate_playlist_name(
            mood
        )

        st.markdown(
            f"##{playlist_name}"
        )
        st.markdown("---")

        st.subheader("📊 Playlist Insights")


        avg_popularity = round(
            playlist["popularity"].mean(),
            2
        )

        dominant_genre = (
            playlist["track_genre"]
            .mode()[0]
        )

        avg_energy = round(
            playlist["energy"].mean(),
            2
        )

        song_count = len(playlist)

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.metric(
                "Songs",
                song_count
            )

        with col2:
            st.metric(
                "Popularity",
                avg_popularity
            )

        with col3:
            st.metric(
                "Top Genre",
                dominant_genre
            )

        with col4:
            st.metric(
                "Energy",
                avg_energy
            )

        st.markdown("---")
        st.subheader("🎵 Genre Distribution")

        genre_counts = (
            playlist["track_genre"]
            .value_counts()
        )

        st.bar_chart(genre_counts)

        # ADD SECOND CHART HERE
        st.subheader("⚡ Energy Distribution")

        st.line_chart(
            playlist["energy"]
        )


        for _, row in playlist.iterrows():

            st.markdown(
            f"""
            <div style="
            padding:10px;
            border-radius:10px;
            margin-bottom:10px;
            background:#1e1e1e;">
            🎵 <b>{row['track_name']}</b><br>
            🎤 {row['artists']}
            </div>
            """,
            unsafe_allow_html=True
        )
                
        csv=playlist.to_csv(index=False)

        st.download_button(
            label="📥 Download Playlist",
            data=csv,
            file_name=f"{mood}_playlist.csv",
            mime="text/csv"
        )      

elif selected=="Favorites":

    from feedback import (
        load_liked,
        load_disliked
    )

    liked=load_liked()
    disliked=load_disliked()

    st.title("⭐ My Music Library")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "👍 Liked Songs",
            len(liked)
        )

    with col2:
        st.metric(
            "👎 Disliked Songs",
            len(disliked)
        )

    st.subheader("👍 Favorite Songs")

    for song in liked:
        st.write("🎵", song)

    st.markdown("---")

    st.subheader("👎 Blocked Songs")

    for song in disliked:
        st.write("🚫", song)



elif selected=="History":

    from user_history import load_history

    st.title("🎵 Your Listening History")

    history=load_history()

    from feedback import (
        load_liked,
        load_disliked
    )

    liked=load_liked()
    disliked=load_disliked()

    st.write("Liked songs loaded:", liked)
    st.write("Disliked songs loaded:", disliked)

    if len(history)==0:
        st.info("No History Yet")

    else:
        for song in reversed(history):
            st.write("🎧",song)

    st.markdown("---")
    st.subheader("👍 Liked Songs")

    if len(liked) == 0:
        st.info("No liked songs yet")

    else:
        for song in liked:
            st.write("👍", song)


    st.markdown("---")
    st.subheader("👎 Disliked Songs")

    if len(disliked) == 0:
        st.info("No disliked songs yet")

    else:
        for song in disliked:
            st.write("👎", song)


elif selected=="Assistant":

    st.title("🤖 Music Assistant")

    question=st.text_input(
        "Ask something about your music"
    )

    if question:

        answer=ask_music_assistant(question)

        st.success(answer)

# ----------------------
# SETTINGS PAGE
# ----------------------

elif selected=="Settings":
    st.title("⚙ Settings")
    st.write(
        "Theme Settings Coming Soon"
    )