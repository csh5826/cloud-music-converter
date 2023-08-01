import openpyxl

og_path = './data/all songs from apple.xlsx'
updated_path = './data/all songs with uri.xlsx'

def extract_title_and_artist_from_excel():
    data_list = []
    wb = openpyxl.load_workbook(og_path)
    sheet = wb.active

    # Assuming column 1 is 'title' and column 3 is 'artist'
    for row in sheet.iter_rows(min_row=2, values_only=True):
        title, _, artist, *_ = row  # Extract title and artist from the row
        data_list.append({'title': title, 'artist': artist})

    wb.close()
    return data_list

def extract_uid_from_excel():
    uid_list = []
    wb = openpyxl.load_workbook(updated_path)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        spotify_uid = row[5]  # Extract title and artist from the row
        if spotify_uid and spotify_uid != 'NOT FOUND':
            uid_list.append(spotify_uid)

    wb.close()
    return uid_list

def write_spotify_uid_to_excel(list):
    wb = openpyxl.load_workbook(og_path)
    sheet = wb.active

    # Start writing from the second row (skipping the header row)
    for i, spotify_uid in enumerate(list, start=2):
        sheet.cell(row=i, column=6, value=spotify_uid)

    wb.save(og_path)
    wb.close()