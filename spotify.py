from auth import spotipy_oauth
from excel_helper import extract_title_and_artist_from_excel, write_spotify_uid_to_excel, get_sheet_names, remove_rows_without_spotify_uid, extract_uid_from_excel
import time
import os
from dotenv import load_dotenv
# PROBABLY WORTH MAKING EXCEL_HELPER INTO ITS OWN CLASS
load_dotenv()

USER_ID = os.getenv("USER_ID")
PLAYLIST_NAME='all songs from apple'
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

def add_tracks_to_playlist(track_uris, playlist_id): # need a list of track URIs
    print('Processing these tracks:', track_uris)
    spotify.playlist_add_items(playlist_id, track_uris) 
    return f'Your playlist: {PLAYLIST_NAME} has been updated'

# created_playlist = spotify.user_playlist_create(USER_ID, PLAYLIST_NAME, True, False, '')
PLAYLIST_ID = '47VW4a6XXezcUi9Ev2MZiP'

def grab_uids_and_append_to_excel(music_metadata, path, sheet_name): #look into speeding this up somehow 
    results = []
    for metadata in music_metadata:
        spotify_uri = get_spotify_uri(metadata['title'], metadata['artist'])
        print('spotify uri for:', metadata['title'])
        print(spotify_uri)
        results.append(spotify_uri)
        time.sleep(60/175)
    write_spotify_uid_to_excel(results, path, sheet_name) #update this
    try:
        while True:
            results.remove('NOT FOUND')
    except ValueError:
        pass

def register_songs_to_playlist(uid_list, playlist_id):
  for i in range(0, len(uid_list), 75): #max amount of uris in one request is 100
      batch = uid_list[i:i + 75]
      add_tracks_to_playlist(batch, playlist_id)
      time.sleep(60/175)


spotify = spotipy_oauth()
my_playlist_names = get_sheet_names(og_path)
my_playlist_names.pop(0)
my_playlist_names = ['firework']

playlist_metadata = create_playlists(my_playlist_names)
# FOR LOOP HERE 
for entry in playlist_metadata:
    song_metadata = extract_title_and_artist_from_excel(og_path, entry['name'])
    print(song_metadata)
    grab_uids_and_append_to_excel(song_metadata, og_path, entry['name'])
    remove_rows_without_spotify_uid(og_path, not_found_path, entry['name'])
    uids = extract_uid_from_excel(og_path, entry['name'])
    register_songs_to_playlist(uids, entry['id'])

#list of dictionaries for artist and song
#apple_music_metadata = extract_title_and_artist_from_excel(og_path)
#quick note, spotify does not like feat.
# remove_parentheses_from_column(not_found_path, not_found_no_title_parentheses, 1)
# not_found_metadata = extract_title_and_artist_from_excel(not_found_path)
# print(not_found_metadata)
# grab_uids_and_append_to_excel(not_found_metadata, not_found_path)

# uid_list = extract_uid_from_excel(updated_path)

# uid_list = extract_uid_from_excel(not_found_path)
# print(uid_list)

# register_songs_to_playlist(uid_list)