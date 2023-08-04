from auth import spotipy_oauth
from excel_helper import extract_title_and_artist_from_excel, write_spotify_uri_to_excel, get_sheet_names, separate_valid_uris_and_invalid_uris, extract_uri_from_excel, remove_parentheses_from_column
import time
import os
from dotenv import load_dotenv

load_dotenv()

USER_ID = os.getenv("USER_ID")
og_path = './data/all songs from apple.xlsx'
updated_path = './data/all songs with uri.xlsx'
not_found_path = './data/all songs with not found uri.xlsx'
not_found_no_title_parentheses = './data/all songs not found no title parentheses.xlsx'

def create_playlists(playlist_names):
    playlist_metadata = []
    for name in playlist_names:
        id = spotify.user_playlist_create(USER_ID, name, True, False, '')['id']
        metadata = {'name': name, 'id': id}
        playlist_metadata.append(metadata)
    return playlist_metadata

def get_spotify_uri(title, artist):
    query = f'track:{title} artist:{artist}'
    data = spotify.search(query, limit=1)

    if 'tracks' in data and 'items' in data['tracks'] and data['tracks']['items']:
        track = data['tracks']['items'][0]
        return track['uri']
    else:
        return 'NOT FOUND'

def add_tracks_to_playlist(track_uris, playlist_id):
    print('Processing these tracks:', track_uris)
    spotify.playlist_add_items(playlist_id, track_uris) 

def grab_uris_and_append_to_excel(music_metadata, path, sheet_name): #look into speeding this up somehow 
    uris = []
    for metadata in music_metadata:
        spotify_uri = get_spotify_uri(metadata['title'], metadata['artist'])
        print('spotify uri for:', metadata['title'])
        print(spotify_uri)
        uris.append(spotify_uri)
        time.sleep(60/175)
    write_spotify_uri_to_excel(uris, path, sheet_name)
    try:
        while True:
            uris.remove('NOT FOUND')
    except ValueError:
        pass

def register_songs_to_playlist(uri_list, playlist_id):
  for i in range(0, len(uri_list), 75): #max amount of uris in one request is 100
      batch = uri_list[i:i + 75]
      add_tracks_to_playlist(batch, playlist_id)
      time.sleep(60/175)

def first_iteration(playlist_info):
    for entry in playlist_info:
        song_metadata = extract_title_and_artist_from_excel(og_path, entry['name'])
        print(song_metadata)
        grab_uris_and_append_to_excel(song_metadata, og_path, entry['name'])
        separate_valid_uris_and_invalid_uris(og_path, not_found_path, entry['name'])
        uris = extract_uri_from_excel(og_path, entry['name'])
        register_songs_to_playlist(uris, entry['id'])

test_second_uris = []
def second_iteration(playlist_info):
    for entry in playlist_info:
        remove_parentheses_from_column(not_found_path, not_found_no_title_parentheses, 1, entry['name'])
        second_song_metadata = extract_title_and_artist_from_excel(not_found_no_title_parentheses, entry['name'])
        print(second_song_metadata)
        grab_uris_and_append_to_excel(second_song_metadata, not_found_no_title_parentheses, entry['name'])
        separate_valid_uris_and_invalid_uris(not_found_no_title_parentheses, not_found_path, entry['name']) 
        second_uris = extract_uri_from_excel(not_found_no_title_parentheses, entry['name']) #bit janky here too, ideally wed be adding the new URIs from the og path, only grabbing newly added ones etc
        if second_uris:
            global test_second_uris
            test_second_uris = test_second_uris + second_uris
        register_songs_to_playlist(second_uris, entry['id'])

# for the second iteration, we want to go back through the all songs with not found and remove the ones that were found
spotify = spotipy_oauth()
my_playlist_names = get_sheet_names(og_path)

#my_playlist_names.pop(0)
playlist_metadata = create_playlists(['spice (pepper)'])

first_iteration(playlist_metadata)
second_iteration(playlist_metadata)

# print('all songs captured on the second attempt')
# print(len(test_second_uris))
# print(test_second_uris)
