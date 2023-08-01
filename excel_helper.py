import openpyxl

path = './data/all songs from apple.xlsx'

def extract_data_from_excel():
    data_list = []
    wb = openpyxl.load_workbook(path)
    sheet = wb.active

    # Assuming column 1 is 'title' and column 3 is 'artist'
    for row in sheet.iter_rows(min_row=2, values_only=True):
        title, _, artist, *_ = row  # Extract title and artist from the row
        data_list.append({'title': title, 'artist': artist})

    wb.close()
    return data_list