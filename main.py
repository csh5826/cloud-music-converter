import requests
import base64
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

load_dotenv()


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET =os.getenv("CLIENT_SECRET")
# Replace 'USER_ID' with the user ID of your Spotify account
USER_ID='' #need this
# Replace 'AUTHORIZATION_CODE' with the authorization code you obtain after the user logs in and grants access
AUTHORIZATION_CODE = 'YOUR_AUTHORIZATION_CODE'

user_id = 'YOUR_USER_ID'
PLAYLIST_NAME='all songs from apple'

def get_api_token(client_id, client_secret):
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}
    data = {'grant_type': 'client_credentials'}

    response = requests.post(token_url, headers=headers, data=data)
    access_token = response.json().get('access_token')

    return access_token


def get_user_token(client_id, client_secret, code): #redirect_uri
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': ''#redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=data)
    access_token = response.json().get('access_token')

    return access_token


def get_spotify_id(song_title, access_token):
    base_url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {
        'q': f'track:{song_title}',
        'type': 'track',
        'limit': 1
    }

    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()
    print(data)

    if 'tracks' in data and 'items' in data['tracks'] and data['tracks']['items']:
        track = data['tracks']['items'][0]
        return track['id']
    else:
        return None

def create_playlist(access_token, user_id, playlist_name):
    create_playlist_url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    data = {'name': playlist_name, 'public': False}

    response = requests.post(create_playlist_url, headers=headers, json=data)
    playlist_id = response.json().get('id')

    return playlist_id

def add_tracks_to_playlist(access_token, playlist_id, track_uris):
    add_tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    data = {'uris': track_uris}

    response = requests.post(add_tracks_url, headers=headers, json=data)

    return response.status_code == 201

# Replace the list below with your array of song titles
song_titles = ['Cries in vein', 'Lemonade', 'Trapper']


# Get the access token using the client credentials flow
api_token = get_api_token(CLIENT_ID, CLIENT_SECRET)

user_token = get_user_token(CLIENT_ID, CLIENT_SECRET)

playlist_id = create_playlist(user_token, user_id, playlist_name)
print('playlist_id is')
print(playlist_id)

# Store the results in an array
results = []

for song_title in song_titles:
    spotify_id = get_spotify_id(song_title, api_token)
    if spotify_id:
        results.append(spotify_id)

print("Spotify IDs of the songs:")
print(results)


spotify_ids = ['4RSpef8XeBACK6MNkfdVE7', '7hxHWCCAIIxFLCzvDgnQHX', '4XaW4jIud5YxwV4QRJOb40']