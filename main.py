import requests
from urllib.parse import urlencode
from auth import spotipy_oauth

USER_ID = 'br18lp7xinjotspsyry15qyrk'
PLAYLIST_NAME='all songs from apple'
redirect_uri = 'https://localhost:8888/callback'

def get_spotify_uri(title, artist): #make this plural and send in array first
    query = f'track:{title} artist:{artist}'
    data = spotify.search(query, limit=1)

    if 'tracks' in data and 'items' in data['tracks'] and data['tracks']['items']:
        track = data['tracks']['items'][0]
        return track['uri'] #ideally we write this value to the csv
    else: #need to update this logic to note we weren't able to get that track (ideally we are writing to the csv here)
        return None

def add_tracks_to_playlist(track_uris, spotify_client): # need a list of track URIs
    spotify_client.playlist_add_items(PLAYLIST_ID, track_uris)

#list of dictionaries for artist and song
apple_music_metadata = [{'artist': 'zach bryan', 'title': 'oklahoma smokeshow'}]

spotify = spotipy_oauth()

# created_playlist = spotify.user_playlist_create(USER_ID, PLAYLIST_NAME, True, False, '')
PLAYLIST_ID = '47VW4a6XXezcUi9Ev2MZiP'

# playlist_id = create_playlist(api_token, user_id, PLAYLIST_NAME)

# Store the results in an array
results = []

for metadata in apple_music_metadata:
    spotify_id = get_spotify_uri(metadata['title'], metadata['artist'])
    if spotify_id:
        results.append(spotify_id)

print("Spotify URI's of the songs:")
print(results)

add_tracks_to_playlist(results, spotify)


# spotify_uris = ['4RSpef8XeBACK6MNkfdVE7', '7hxHWCCAIIxFLCzvDgnQHX', '4XaW4jIud5YxwV4QRJOb40']