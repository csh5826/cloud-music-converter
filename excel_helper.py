import openpyxl
import os

# og_path = './data/all songs from apple.xlsx'
#updated_path = './data/all songs with uri.xlsx'

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

# def extract_uid_from_excel(not_found, path):
#     uid_list = []
#     wb = openpyxl.load_workbook(path)
#     sheet = wb.active

#     for row in sheet.iter_rows(min_row=2, values_only=True):
#         spotify_uid = row[5]  # Extract title and artist from the row
#         if not_found is False:
#             if spotify_uid and spotify_uid != 'NOT FOUND': #can definitely clean this up
#                 uid_list.append(spotify_uid)
#         else:
#             if spotify_uid and spotify_uid is 'NOT FOUND':
#                 uid_list.append(spotify_uid)

#     wb.close()
#     return uid_list

def extract_uid_from_excel(path):
    uid_list = []
    wb = openpyxl.load_workbook(path)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        spotify_uid = row[5]  # Extract title and artist from the row
        if spotify_uid and spotify_uid != 'NOT FOUND':
            uid_list.append(spotify_uid)

    wb.close()
    return uid_list

def write_spotify_uid_to_excel(uid_list, path):
    wb = openpyxl.load_workbook(path)
    sheet = wb.active

    # Start writing from the second row (skipping the header row)
    for i, spotify_uid in enumerate(uid_list, start=2):
        sheet.cell(row=i, column=6, value=spotify_uid)

    wb.save(path)
    wb.close()

# def create_excel_sheet(name, columns):
#     workbook = openpyxl.Workbook()
#     sheet = workbook.active
#     sheet.title = name
#     # Write column headers to the sheet
#     for col_idx, column in enumerate(columns, start=1):
#         sheet.cell(row=1, column=col_idx, value=column)
#     # Save the workbook in the 'data' folder
#     data_folder = 'data'
#     os.makedirs(data_folder, exist_ok=True)
#     file_path = os.path.join(data_folder, f"{name}.xlsx")
#     workbook.save(file_path)
#     return file_path

# def copy_sheet_data(source_path, new_path): #source_sheet_name <-- may want to utilize this
#     source_wb = openpyxl.load_workbook(source_path)
#     source_sheet = source_wb.active

#     # Create or load the destination workbook and sheet
#     try:
#         destination_workbook = openpyxl.load_workbook(new_path)
#     except FileNotFoundError:
#         destination_workbook = openpyxl.Workbook()
#         destination_sheet = destination_workbook.create_sheet()

#     for row in source_sheet.iter_rows(values_only=True):
#         destination_sheet.append(row)

#     destination_workbook.save(new_path)

def remove_rows_without_spotify_uid(input_file, output_file):
    # Load the workbook and active sheet from the input file
    input_workbook = openpyxl.load_workbook(input_file)
    input_sheet = input_workbook.active #

    # Create a new workbook and sheet for the filtered data
    output_workbook = openpyxl.Workbook()
    output_sheet = output_workbook.active

    # Copy only the rows with a value of 'NOT FOUND' in the Spotify UID column
    for row in input_sheet.iter_rows(values_only=True):
        spotify_uid = row[5]  # Assuming column 6 is the 'Spotify UID' column
        if spotify_uid == 'NOT FOUND':
            output_sheet.append(row)

    # Save the new workbook to the output file
    output_workbook.save(output_file)

# def handle_not_found_uids(name, columns, existing_excel_path, new_path):
#     copy_sheet_data(existing_excel_path, new_path)

#     write_spotify_uid_to_excel(not_found_list, new_path)

 # we want to:
#  1. create a new excel sheet
 # 2. copy over the updated one with all uris
 # remove all rows that have do not have a row value of 'not found' for spotify UID

#flow is : create_excel_sheet -> extract_uid_from_excel(file_path, True) --> write_spotify_uid_to_excel
