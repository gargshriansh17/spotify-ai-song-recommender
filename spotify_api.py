import os
import spotipy
import streamlit as st

from spotipy.oauth2 import SpotifyClientCredentials

def _get_credential(key):
    # Prefer Streamlit secrets (secrets.toml) when running inside Streamlit.
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        pass
    # Fall back to a plain environment variable (e.g. when running this
    # file directly with `python spotify_api.py`, outside Streamlit).
    return os.environ.get(key)

client_id = _get_credential("SPOTIFY_CLIENT_ID")
client_secret = _get_credential("SPOTIFY_CLIENT_SECRET")


if not client_id or not client_secret:
    raise RuntimeError(
        "Missing SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET. "
        "Add a .streamlit/secrets.toml file in your project folder with:\n"
        '  SPOTIFY_CLIENT_ID = "your_client_id"\n'
        '  SPOTIFY_CLIENT_SECRET = "your_client_secret"\n'
        "(see the comment at the bottom of this file for the exact steps)."
    )

auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)

sp=spotipy.Spotify(
    auth_manager=auth_manager
)


def get_track_info(song_name):
    try:
        result=sp.search(
            q=song_name,
            type="track",
            limit=1
        )

    except Exception:
        return None

    if len(result["tracks"]["items"])==0:
        return None
    
    track=result["tracks"]["items"][0]

    album_cover = None

    if track["album"]["images"]:
        album_cover = track["album"]["images"][0]["url"]
    return {
        "album_cover": album_cover,
        
        "spotify_url":
            track["external_urls"]["spotify"]
        
    }


