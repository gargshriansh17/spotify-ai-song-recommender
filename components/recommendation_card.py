import streamlit as st

def recommendation_card(
    song,
    artist,
    similarity,
    mood,
    genre,
    popularity,
    image_url,
    spotify_url
):

    st.markdown(
        "<div class='song-card'>",
        unsafe_allow_html=True
    )

    st.image(
        image_url,
        width=150
    )

    st.markdown(
        f"### {song}"
    )

    st.caption(
        artist
    )

    st.caption(f"Genre: {genre}")
    st.caption(f"Mood:{mood}")
    st.caption(f"Popularity: {popularity}")

    st.progress(
        similarity / 100
    )

    st.write(
        f"🎯 {similarity}% Match"
    )

    st.link_button(
        "🎵 Open in Spotify",
        spotify_url
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )