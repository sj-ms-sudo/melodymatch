from flask import Flask, request, redirect
import json
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

CLIENT_ID = "526665e9160e4e04ba4dcef9427243c2"
CLIENT_SECRET = "aa7d7f522c5e4af5986e2e0090275d94"
REDIRECT_URI = "https://melodymatch.onrender.com/callback"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-top-read user-read-private",
    cache_path=None
)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    
    with open("token_store.json", "w") as f:
        json.dump(token_info, f)

    return redirect("https://melodymatch.onrender.com")  # go back to Streamlit

@app.route("/")
def home():
    return "Flask is running for MelodyMatch."

if __name__ == "__main__":
    app.run()
