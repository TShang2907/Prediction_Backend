import paho.mqtt.client as mqtt
import time
# username: servermonitoring
# Pass: ServerMonitoring_wQ1Z3Q5n64
# Topic: /server/monitoring/
# host: mqttserver.tk
# port: 1883
MQTT_SERVER = "mqttserver.tk"
MQTT_PORT = 1883
MQTT_USERNAME = "innovation"
MQTT_PASSWORD = "Innovation_RgPQAZoA5N"
MQTT_TOPIC_SUB_AIR = "/innovation/airmonitoring/NBIOTs"
MQTT_TOPIC_AI = "/innovation/valvecontroller/ai" #"/innovation/airmonitoring/NBIOTs/AI"
# Import thư viện cần thiết
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

#Google Sheet
# Khai báo client ID và client secret key
creds = service_account.Credentials.from_service_account_file('Token.json')
# Xác thực và đăng nhập vào tài khoản Google
service = build('sheets', 'v4', credentials=creds)
# Truy cập vào một bảng tính cụ thể
spreadsheet_id = '1qO1gqFsBra6mbL7lR1GeKLbJBeAL10zf1mfkAdoFPk0'
sheet_name = f'RealData!A:K'

class MQTTHelper:
   
    def mqtt_connected(self, client, userdata, flags, rc):
        print("Connected succesfully!!")
        client.subscribe(MQTT_TOPIC_SUB_AIR)
                
    def mqtt_subscribed(self, client, userdata, mid, granted_qos):
        print("Subscribed to Topic!!!")


    def mqtt_recv_message(self, client, userdata, message):
        #self.recvCallBack(message)
        print("Topic",message.topic)
        print("Received: ", message.payload.decode("utf-8"))
        # if message.topic=="/innovation/airmonitoring/NBIOTs":
        #     # Dữ liệu bạn muốn ghi lên Google Sheets
        #     new_values = [
        #         [1713929117, "24/04/2024 10:25:17", 33, 62.6, 31.5, 24.4, 6.8, 23, 1, 2, 5]
        #     ]
        #     # Thực hiện việc cập nhật dữ liệu vào bảng tính
        #     request_body = {
        #         'values': new_values
        #     }

        #     response = service.spreadsheets().values().append(
        #         spreadsheetId=spreadsheet_id, 
        #         range=sheet_name,
        #         valueInputOption='USER_ENTERED',
        #         body=request_body,
        #         insertDataOption='INSERT_ROWS',
        #         responseDateTimeRenderOption='FORMATTED_STRING'

        #     ).execute()

        #     print(json.dumps(response, indent=4))


    def setRecvCallBack(self, func):
        self.recvCallBack = func
        
    def __init__(self):
        self.mqttClient = mqtt.Client()
        self.mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)

        # Register mqtt events
        self.mqttClient.on_connect = self.mqtt_connected
        self.mqttClient.on_subscribe = self.mqtt_subscribed
        self.mqttClient.on_message = self.mqtt_recv_message
        self.mqttClient.loop_start()
    
    def publish(self, topic, message):
        self.mqttClient.publish(topic, str(message), retain=True)
    
mqtt=MQTTHelper()

while True:
    # mqtt.publish(MQTT_TOPIC_AI,"hello")
    # time.sleep(3)
   pass