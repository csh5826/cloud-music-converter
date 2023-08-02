from auth import spotipy_oauth
from excel_helper import extract_title_and_artist_from_excel, write_spotify_uid_to_excel, extract_uid_from_excel
import time

USER_ID = 'br18lp7xinjotspsyry15qyrk'
PLAYLIST_NAME='all songs from apple'
og_path = './data/all songs from apple.xlsx'
updated_path = './data/all songs with uri.xlsx'

def get_spotify_uri(title, artist): #make this plural and send in array first
    query = f'track:{title} artist:{artist}'
    data = spotify.search(query, limit=1)

    if 'tracks' in data and 'items' in data['tracks'] and data['tracks']['items']:
        track = data['tracks']['items'][0]
        return track['uri'] #ideally we write this value to the csv
    else: #lets return 'NOT FOUND'
        return 'NOT FOUND'

def add_tracks_to_playlist(track_uris): # need a list of track URIs
    print('Processing these tracks:', track_uris)
    spotify.playlist_add_items(PLAYLIST_ID, track_uris)
    return f'Your playlist: {PLAYLIST_NAME} has been updated'

#list of dictionaries for artist and song
apple_music_metadata = extract_title_and_artist_from_excel()
#quick note, spotify does not like feat.

spotify = spotipy_oauth()

# created_playlist = spotify.user_playlist_create(USER_ID, PLAYLIST_NAME, True, False, '')
PLAYLIST_ID = '47VW4a6XXezcUi9Ev2MZiP'

def grab_uids_and_append_to_excel():
    results = []
    for metadata in apple_music_metadata: #apple_music_metadata
        spotify_uri = get_spotify_uri(metadata['title'], metadata['artist'])
        print('spotify uri for:', metadata['title'])
        print(spotify_uri)
        #if spotify_id is not 'NOT FOUND':
        results.append(spotify_uri)
        time.sleep(60/175) #adding this bc spotify has governor limits of around 180 requests per minute (this will be about 175)
   #write the spotify id to excel here
    write_spotify_uid_to_excel(results, og_path)
    try:
        while True:
            results.remove('NOT FOUND')
    except ValueError:
        pass

uid_list = extract_uid_from_excel(updated_path)

def register_songs_to_playlist(uid_list):
  for i in range(0, len(uid_list), 75): #max amount of uris in one request is 100
      batch = uid_list[i:i + 75]
      add_tracks_to_playlist(batch)
      time.sleep(60/175)

register_songs_to_playlist(uid_list)