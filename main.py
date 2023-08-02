from excel_helper import remove_rows_without_spotify_uid

new_excel = './data/all songs with not found uri.xlsx'
# columns = ['Title', 'Time', 'Artist', 'Album', 'Genre', 'Spotify URI']
existing_excel = './data/all songs not found no title parentheses.xlsx'
# handle_not_found_uids(excel_name, columns, existing_excel)
# def start():

remove_rows_without_spotify_uid(existing_excel, new_excel)



