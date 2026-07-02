import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from user_history import load_history

st.title("📊 Music Analytics Dashboard")

df=pd.read_csv("data/cleaned_songs.csv")

history=load_history()

col1,col2,col3=st.columns(3)

with col1:
    st.metric(
        "Songs",
        len(df)
    )

with col2:
    st.metric(
        "Genres",
        df["track_genre"].nunique()
    )

with col3:
    st.metric(
        "Artists",
        df["artists"].nunique()
    )

st.divider()

st.subheader("👤 User Statistics")

col1,col2=st.columns(2)

with col1:
    st.metric(
        "Songs Searched",
        len(history)
    )

with col2:
    st.metric(
        "Unique Searches",
        len(set(history))
    )

st.subheader("🕒 Recent Searches")

if len(history) == 0:
    st.info("No searches yet")

else:
    for song in history[:10]:
        st.write("🎵", song)

st.divider()



# -------------------
# Genre Distribution
# -------------------

st.subheader("🎵 Top Genres")

genre_count=(
    df["track_genre"].value_counts().head(10)
)

fig,ax=plt.subplots(figsize=(8,5))

genre_count.plot(kind="bar",ax=ax,colormap="viridis")

plt.xticks(rotation=45)

st.pyplot(fig)

# -------------------
# Popularity
# -------------------

st.subheader("🔥 Popularity Distribution")

fig,ax=plt.subplots(figsize=(8,5))

ax.hist(df["popularity"],bins=20)

st.pyplot(fig)

# -------------------
# Energy vs Danceability
# -------------------

st.subheader("⚡ Energy vs Danceability")

sample = df.sample(3000)

fig, ax = plt.subplots(figsize=(8,5))

ax.scatter(
    sample["energy"],
    sample["danceability"],
    alpha=0.5
)

ax.set_xlabel("Energy")
ax.set_ylabel("Danceability")

st.pyplot(fig)

# -------------------
# Top Artists
# -------------------

st.subheader("🎤 Most Frequent Artists")

artist_count = (
    df["artists"]
    .value_counts()
    .head(10)
)

fig, ax = plt.subplots(figsize=(8,5))

artist_count.plot(
    kind="barh",
    ax=ax,
    colormap="viridis"
)

st.pyplot(fig)

st.divider()

st.subheader("🎤 Favorite Artists Based On Your Searches")

if len(history) > 0:
    searched_artists=[]

    for item in history:
        if "-" in item:
            artist=item.split(" - ")[1].strip()

            searched_artists.append(artist)
        
    if len(searched_artists) > 0:

        artist_count=(
            pd.Series(searched_artists)
            .value_counts()
            .head(10)
        )

        fig,ax=plt.subplots(figsize=(8,5))

        artist_count.plot(kind="bar",ax=ax,colormap="viridis")


        st.pyplot(fig)