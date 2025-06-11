import streamlit as st
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "526665e9160e4e04ba4dcef9427243c2"
CLIENT_SECRET = "aa7d7f522c5e4af5986e2e0090275d94"
REDIRECT_URI = "https://melodymatch.onrender.com/callback"
TOKEN_PATH = "token_store.json"

st.title("🎵 MelodyMatch - Spotify Dating")

if not os.path.exists(TOKEN_PATH):
    st.markdown("### Find your music soulmate")
    auth_url = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-top-read user-read-private",
        cache_path=None
    ).get_authorize_url()

    st.markdown(f"[Click here to login with Spotify]({auth_url})")
else:
    with open(TOKEN_PATH, "r") as f:
        token_info = json.load(f)

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user = sp.current_user()

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(user['images'][0]['url'] if user['images'] else "https://via.placeholder.com/150", width=150)

    with col2:
        st.header(f"Welcome, {user['display_name']}!")
        st.caption(f"Spotify ID: {user['id']}")

    st.subheader("Your Top Tracks")
    tracks = sp.current_user_top_tracks(limit=5)['items']
    for idx, track in enumerate(tracks, 1):
        st.write(f"{idx}. **{track['name']}** by {track['artists'][0]['name']}")

    if st.button("Logout"):
        os.remove(TOKEN_PATH)
        st.success("Logged out.")
        st.rerun()
