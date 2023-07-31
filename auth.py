import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import base64
import requests

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET =os.getenv("CLIENT_SECRET")
SCOPE='playlist-modify-public'

def get_api_token():
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}
    data = {'grant_type': 'client_credentials'}

    response = requests.post(token_url, headers=headers, data=data)
    access_token = response.json().get('access_token')

    return access_token


def get_user_token(code): #redirect_uri
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': ''#redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=data)
    access_token = response.json().get('access_token')

    return access_token

def create_spotify_oauth():
    # Create a Spotify OAuth object
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri='http://localhost:8888/callback', scope=SCOPE)

    # Get the authorization URL and prompt the user to log in or grant permissions
    auth_url = sp_oauth.get_authorize_url()
    print("Please visit the following URL and log in or grant permissions:")
    print(auth_url)

    # Get the authorization code from the user after they grant permissions
    authorization_code = input("Enter the authorization code from the URL: ")

    # Get the access token using the authorization code
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    return sp_oauth.get_access_token(authorization_code)['access_token']