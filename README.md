# 🎵 Spotify AI Song Recommender

An AI-powered music recommendation platform built using Python, Machine Learning, NLP, Spotify API, and Streamlit.

The system analyzes song audio features, user listening behavior, genres, moods, and feedback to generate personalized music recommendations.

---

## 🚀 Features

### 🎧 Smart Song Recommendation
- Recommends similar songs using Machine Learning
- Uses K-Nearest Neighbors (KNN)
- Genre-aware recommendation engine
- Audio feature similarity matching

### 🔍 Intelligent Song Search
- Search from 81,000+ songs
- Autocomplete suggestions
- Fast song matching

### 😊 Mood-Based Music Discovery
- Detect user mood using NLP
- Generate mood-specific playlists
- Supports:
  - Happy
  - Relax
  - Party
  - Sad

### 🎵 Smart Playlist Generator
- AI-generated playlists
- Playlist analytics
- Playlist export as CSV

### 📊 Music Analytics Dashboard
- Listening history analysis
- Favorite genres
- Favorite artists
- Music personality detection
- Spotify Wrapped-style insights

### 👍 Feedback Learning
- Like songs
- Dislike songs
- Personalized recommendation ranking

### 🤖 Music Assistant
- Natural language music queries
- Personalized music insights

### 🎨 Modern UI
- Glassmorphism design
- Neon hover effects
- Responsive Streamlit interface

---

## 🧠 Machine Learning Pipeline

### Data Processing
- Duplicate removal
- Feature selection
- Data normalization using StandardScaler

### Recommendation Engine
- K-Nearest Neighbors (KNN)
- Cosine Similarity
- Genre-specific recommendation models

### Features Used

- Danceability
- Energy
- Speechiness
- Acousticness
- Instrumentalness
- Liveness
- Valence
- Tempo
- Popularity
- Loudness

---

## 📂 Project Structure

```text
song-system/
│
├── app.py
├── recommender.py
├── spotify_api.py
├── playlist_generator.py
├── music_assistant.py
├── nlp_search.py
├── feedback.py
├── user_history.py
│
├── components/
│   └── recommendation_card.py
│
├── assets/
│   └── default_album.jpg
│
├── data/
│   ├── spotify_tracks.csv
│   └── cleaned_songs.csv
│
└── style.css
