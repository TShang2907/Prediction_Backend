import paho.mqtt.client as mqtt
import json

from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

from MQTT import *
#MQTT
mqtt=MQTTHelper()

# Google Sheets Receive Data
sheetGetData_id = '1A1V1pnv-MvBhynMW7rBfc0m5X6Cc3QmOssjgjzMl8j0'
# API key
api_key = 'AIzaSyCGQxAPIFmR03S3CbNDtulHhxfdAQNmTbM'   # Lấy tại Google Cloud -->API_KEY
parameter_1='majorDimension=ROWS'
parameter_2='valueRenderOption=UNFORMATTED_VALUE'


#Google Sheet Send Data
# Khai báo client ID và client secret key
creds = service_account.Credentials.from_service_account_file('Token.json')
# Xác thực và đăng nhập vào tài khoản Google
service = build('sheets', 'v4', credentials=creds)
# Truy cập vào một bảng tính cụ thể
spreadsheet_id = '1qO1gqFsBra6mbL7lR1GeKLbJBeAL10zf1mfkAdoFPk0'

data_sheet= f'Data!A:K'

real_values = [
  [1713929117, "24/04/2024 10:25:17", 33, 62.6, 31.5, 24.4, 6.8, 23, 1, 2, 5]
]

def storeDatabase(new_values,sheet_name):
  try:
    if(sheet_name=='RealData!A:K'):
      print("Send real data to Google Sheet: ",new_values[0])
    else:
      print("Send prediction data to Google Sheet: ",new_values[0])


    request_body = {
              'values': new_values
          }
    response = service.spreadsheets().values().append(
      spreadsheetId=spreadsheet_id, 
      range=sheet_name,
      valueInputOption='USER_ENTERED',
      body=request_body,
      insertDataOption='INSERT_ROWS',
      responseDateTimeRenderOption='FORMATTED_STRING'
    ).execute()

    print(json.dumps(response, indent=4))
  except Exception as e:
    print("Đã xảy ra lỗi:", e)


def onMessage(data):
    index_value=2
    json_data = json.loads(data.payload.decode("utf-8"))
    print("Received: ",json_data )
  
    #lấy thoi gian hien tai
    current_time=datetime.now()
    epoch_time = int(current_time.timestamp())

    real_values[0][0]=epoch_time 
    real_values[0][1]=current_time.strftime("%d/%m/%Y %H:%M:%S")

    for sensor in json_data["sensors"]:
        if(index_value<11):
            real_values[0][index_value]=sensor["value"]
            index_value=index_value+1

    storeDatabase(real_values,data_sheet)
  
 
mqtt.setRecvCallBack(onMessage)
mqtt.start_loop()

# while (True):
#     pass

