import requests
from urllib.parse import urlencode
from auth import spotipy_oauth

USER_ID = 'br18lp7xinjotspsyry15qyrk'
PLAYLIST_NAME='all songs from apple'
redirect_uri = 'https://localhost:8888/callback'

def get_spotify_id(song_title, spotipy_client): #make this plural and send in array first
    params = {
        'q': f'track:{song_title}',
        'type': 'track',
        'limit': 1
    }
    data = spotipy_client.search(params)

    if 'tracks' in data and 'items' in data['tracks'] and data['tracks']['items']:
        track = data['tracks']['items'][0]
        return track['uri']
    else:
        return None

def add_tracks_to_playlist(track_uris, spotify_client): #need to. figure out if we need the track ids or what here
    spotify_client.playlist_add_items(PLAYLIST_ID, track_uris)


# Replace the list below with your array of song titles
song_titles = ['Cries in vein', 'Lemonade', 'Trapper']


spotify = spotipy_oauth()

# created_playlist = spotify.user_playlist_create(USER_ID, PLAYLIST_NAME, True, False, '')
PLAYLIST_ID = '47VW4a6XXezcUi9Ev2MZiP'

# playlist_id = create_playlist(api_token, user_id, PLAYLIST_NAME)
# print('playlist_id is')
# print(playlist_id)

# Store the results in an array
results = []

for song_title in song_titles: #only adding the first track for some reason
    spotify_id = get_spotify_id(song_title, spotify)
    if spotify_id:
        results.append(spotify_id)

print("Spotify URI's of the songs:")
print(results)

test = add_tracks_to_playlist(results, spotify)
print(test)


# spotify_uris = ['4RSpef8XeBACK6MNkfdVE7', '7hxHWCCAIIxFLCzvDgnQHX', '4XaW4jIud5YxwV4QRJOb40']