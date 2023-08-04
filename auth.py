import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET =os.getenv("CLIENT_SECRET")
SCOPE='playlist-modify-public'

def spotipy_oauth():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))