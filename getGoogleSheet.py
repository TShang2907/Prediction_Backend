import requests
import time
# Đường dẫn đến Google Sheets
sheetGetData_id = '1A1V1pnv-MvBhynMW7rBfc0m5X6Cc3QmOssjgjzMl8j0'
countRows=2850
# API key
api_key = 'AIzaSyCGQxAPIFmR03S3CbNDtulHhxfdAQNmTbM'   # Lấy tại Google Cloud -->API_KEY
parameter_1='majorDimension=ROWS'
parameter_2='valueRenderOption=FORMULA'

# URL để truy cập Google Sheets API
# Test tại Google Developer -->Sheet

def getHistoryData():
    global countRows
    sheet_range = f'Trang tính2!C{countRows}:K'
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheetGetData_id}/values/{sheet_range}?key={api_key}&{parameter_1}&{parameter_2}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if(len(data["values"])>9):
            countRows=countRows+len(data["values"])-9
            getHistoryData()
        else:
            array_values=data["values"]
            print("Count Rows: ",countRows)
            print(array_values)
    else:
        print('Error:', response.status_code)


#getHistoryData()

while True:
    time.sleep(3)
    pass

