# Import thư viện cần thiết
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

from MQTT import *
#MQTT
MQTT_TOPIC_AI = "/innovation/airmonitoring/AI"
mqtt=MQTTHelper()

#Google Sheet
# Khai báo client ID và client secret key
creds = service_account.Credentials.from_service_account_file('Token.json')
# Xác thực và đăng nhập vào tài khoản Google
service = build('sheets', 'v4', credentials=creds)
# Truy cập vào một bảng tính cụ thể
spreadsheet_id = '1qO1gqFsBra6mbL7lR1GeKLbJBeAL10zf1mfkAdoFPk0'
sheet_name = f'RealData!A:K'


# Định nghĩa một hàm xử lý để nhận các thông điệp từ máy chủ MQTT
def receive_callback(message):
    print("Received: ", message.payload.decode("utf-8"))
    if message.topic=="/innovation/airmonitoring/NBIOTs":
        mqtt.publish(MQTT_TOPIC_AI,"OK")
        # Dữ liệu bạn muốn ghi lên Google Sheets
        new_values = [
            [1713929117, "24/04/2024 10:25:17", 33, 62.6, 31.5, 24.4, 6.8, 23, 1, 2, 5]
        ]
        # Thực hiện việc cập nhật dữ liệu vào bảng tính
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

# Gọi phương thức setRecvCallBack để gán hàm xử lý cho việc nhận thông điệp
mqtt.setRecvCallBack(receive_callback)
mqtt.start_loop()

while True: 
    pass










# # Lấy dữ liệu từ bảng tính
# result = service.spreadsheets().values().get(
#     spreadsheetId=spreadsheet_id, range=range_name).execute()

# # In ra các giá trị trong bảng tính
# for row in result.get('values', []):
#     print(row)







