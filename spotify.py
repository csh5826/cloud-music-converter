from auth import spotipy_oauth
from excel_helper import extract_data_from_excel, write_spotify_uid_to_excel
import time

USER_ID = 'br18lp7xinjotspsyry15qyrk'
PLAYLIST_NAME='all songs from apple'

def get_spotify_uri(title, artist): #make this plural and send in array first
    query = f'track:{title} artist:{artist}'
    data = spotify.search(query, limit=1)

    if 'tracks' in data and 'items' in data['tracks'] and data['tracks']['items']:
        track = data['tracks']['items'][0]
        return track['uri'] #ideally we write this value to the csv
    else: #lets return 'NOT FOUND'
        return 'NOT FOUND'

def add_tracks_to_playlist(track_uris, spotify_client): # need a list of track URIs
    spotify_client.playlist_add_items(PLAYLIST_ID, track_uris)
    return f'Your playlist: {PLAYLIST_NAME} has been updated'

#list of dictionaries for artist and song
apple_music_metadata = extract_data_from_excel()
test = [apple_music_metadata[0], {'title': 'A-Town (feat. Marlo)', 'artist': 'Lil Baby'}, {'title': 'blahasdf', 'artist': 'notrealfakeartist'}]
#quick note, spotify does not like feat.


spotify = spotipy_oauth()

# created_playlist = spotify.user_playlist_create(USER_ID, PLAYLIST_NAME, True, False, '')
PLAYLIST_ID = '47VW4a6XXezcUi9Ev2MZiP'

# playlist_id = create_playlist(api_token, user_id, PLAYLIST_NAME)

# Store the results in an array
results = [] #update this name


# need to wrap this logic in a function
for metadata in apple_music_metadata: #apple_music_metadata
    spotify_uri = get_spotify_uri(metadata['title'], metadata['artist'])
    print('spotify uri for:', metadata['title'])
    print(spotify_uri)
    #if spotify_id is not 'NOT FOUND':
    results.append(spotify_uri)
    time.sleep(60/175) #adding this bc spotify has governor limits of around 180 requests per minute (this will be about 175)
   #write the spotify id to excel here
write_spotify_uid_to_excel(results)

print("Spotify URI's of the songs:")
print(results)
try:
    while True:
        results.remove('NOT FOUND')
except ValueError:
    pass
print(results)

add_tracks_to_playlist(results, spotify)