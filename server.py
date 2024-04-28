import paho.mqtt.client as mqtt
import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from keras.models import load_model
import numpy as np
from MQTT import *
#MQTT
MQTT_TOPIC_AI = "/innovation/airmonitoring/AI"
mqtt=MQTTHelper()

# Google Sheets Receive Data
sheetGetData_id = '1A1V1pnv-MvBhynMW7rBfc0m5X6Cc3QmOssjgjzMl8j0'
countRows=2
isFirst=True
# API key
api_key = 'AIzaSyCGQxAPIFmR03S3CbNDtulHhxfdAQNmTbM'   # Lấy tại Google Cloud -->API_KEY
parameter_1='majorDimension=ROWS'
parameter_2='valueRenderOption=UNFORMATTED_VALUE'

X_test = np.zeros((1, 9, 9), dtype=np.float32)



#Google Sheet Send Data
# Khai báo client ID và client secret key
creds = service_account.Credentials.from_service_account_file('Token.json')
# Xác thực và đăng nhập vào tài khoản Google
service = build('sheets', 'v4', credentials=creds)
# Truy cập vào một bảng tính cụ thể
spreadsheet_id = '1qO1gqFsBra6mbL7lR1GeKLbJBeAL10zf1mfkAdoFPk0'

prediction_sheet= f'PredictionData!A:K'
real_sheet= f'RealData!A:K'
range_name_real_sheet='RealData'



message = {
  "station_id": "SENSOR_PREDICTION_0002",
  "station_name": "SENSOR PREDICTION 0002",  
  "sensor_predict": [
    {
      "temp_0001": 0,
      "humi_0001": 0,
      "temp_0002": 0,
      "humi_0002": 0,
      "ph_0002": 0,
      "EC_0002": 0,
      "Nito_0002": 0,
      "Photpho_0002": 0,
      "Kali_0002": 0
    }    
  ]
}
# Dữ liệu bạn muốn ghi lên Google Sheets
prediction_values = [
  [1713929117, "24/04/2024 10:25:17", 33, 62.6, 31.5, 24.4, 6.8, 23, 1, 2, 5]
]
real_values = [
  [1713929117, "24/04/2024 10:25:17", 33, 62.6, 31.5, 24.4, 6.8, 23, 1, 2, 5]
]

def storeDatabase(new_values,sheet_name):
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


def read_data():
  global countRows
  range_name=f'RealData!C{countRows}:K'
  response = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, 
    range=range_name,
    valueRenderOption='UNFORMATTED_VALUE',
    majorDimension='ROWS',
  ).execute()

  values = response.get('values', [])

  if(len(values)>9):
    countRows=countRows+len(values)-9
    read_data()
  else:
    array_values=values
    data_float32 = np.array(array_values, dtype=np.float32)
    print("Count Rows: ",countRows)
    X_test[0] = data_float32
    print("X_test",X_test)

def onMessage(data):
  global countPrediction  # Khai báo biến count là biến toàn cục
  index_value=2
  json_data = json.loads(data.payload.decode("utf-8"))
  print("Received: ",json_data )
  read_data()
  #lấy thoi gian hien tai
  current_time=datetime.now()
  prediction_values[0][1]=current_time.strftime("%d/%m/%Y %H:%M:%S")
  real_values[0][1]=prediction_values[0][1]
 
  # Chuyển đổi thành epoch time
  epoch_time = int(current_time.timestamp())
  prediction_values[0][0]=epoch_time
  real_values[0][0]=epoch_time   


  #Gan gia tri cam bien nhan duoc tu mqtt
  for sensor in json_data["sensors"]:
    if(index_value<11):
      real_values[0][index_value]=sensor["value"]
    index_value=index_value+1
  
  storeDatabase(real_values,real_sheet)
  
 # Load model Prediction, tinh gia tri du doan
  loaded_model = load_model('LSTM2k2.keras')
  yhat = loaded_model.predict(X_test, verbose=0)   
  
  # Làm tròn các giá trị trong y_hat[0][0] đến 2 chữ số thập phân
  rounded_values = [round(value, 2) for value in yhat[0][0].tolist()]

  # Gan gia tri du doan
  prediction_values[0][2:] = rounded_values
  
  
  message["sensor_predict"][0]["temp_0001"] = rounded_values[0]
  message["sensor_predict"][0]["humi_0001"] = rounded_values[1]
  message["sensor_predict"][0]["temp_0002"] = rounded_values[2]
  message["sensor_predict"][0]["humi_0002"] = rounded_values[3]
  message["sensor_predict"][0]["ph_0002"] = rounded_values[4]
  message["sensor_predict"][0]["EC_0002"] = rounded_values[5]
  message["sensor_predict"][0]["Nito_0002"] = rounded_values[6]
  message["sensor_predict"][0]["Photpho_0002"] =rounded_values[7]
  message["sensor_predict"][0]["Kali_0002"] = rounded_values[8]


  mqtt.publish(MQTT_TOPIC_AI, message)
  storeDatabase(prediction_values,prediction_sheet)




mqtt.setRecvCallBack(onMessage)
mqtt.start_loop()

# while (True):
#     pass

