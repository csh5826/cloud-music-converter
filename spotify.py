from auth import spotipy_oauth
from excel_helper import extract_data_from_excel, write_spotify_uid_to_excel

USER_ID = 'br18lp7xinjotspsyry15qyrk'
PLAYLIST_NAME='all songs from apple'

def get_spotify_uri(metadata): #make this plural and send in array first
    query = f'track:{metadata.title} artist:{metadata.artist}'
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
test = [apple_music_metadata[0], apple_music_metadata[1], {'title': 'blahasdf', 'artist': 'notrealfakeartist'}]

spotify = spotipy_oauth()

# created_playlist = spotify.user_playlist_create(USER_ID, PLAYLIST_NAME, True, False, '')
PLAYLIST_ID = '47VW4a6XXezcUi9Ev2MZiP'

# playlist_id = create_playlist(api_token, user_id, PLAYLIST_NAME)

# Store the results in an array
results = [] #update this name


# need to wrap this logic in a function
for metadata in test: #apple_music_metadata
    spotify_id = get_spotify_uri(metadata)
    #if spotify_id is not 'NOT FOUND':
    results.append(spotify_id)
   #write the spotify id to excel here
write_spotify_uid_to_excel(results)

print("Spotify URI's of the songs:")
print(results)

add_tracks_to_playlist(results, spotify)