import streamlit as st

def recommendation_card(song, artist, similarity, mood, genre, popularity, album_cover=None, spotify_url=None):
    
    if album_cover:
        st.image(album_cover, width=200)
    else:
        st.image("assets/default_album.jpg", width=200)

    st.markdown(f"### 🎵 {song}")
    st.markdown(f"🎤 **{artist}**")
    st.markdown(f"🎭 Mood: `{mood}`")
    st.markdown(f"🎸 Genre: `{genre}`")
    st.markdown(f"🔥 Popularity: `{popularity}`")
    st.markdown(f"✅ Similarity: `{similarity}%`")

    if spotify_url:
        st.markdown(f"[▶ Open in Spotify]({spotify_url})")