from flask import Flask
import paho.mqtt.client as mqtt
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS
CORS(app)

#Setting up the username and password for the MQTT broker
mqtt_broker = "nam1.cloud.thethings.network"
mqtt_port = 1883
mqtt_username = "sensores-espe@ttn" #"rpfreire1@espe.edu.ec"
mqtt_password = "NNSXS.3JABFSPM25WQAW4FCASLBX4PICR75GMDDJNVXXA.3Y7ZIHJKDS7QUEG67WSFJF55DD7YAB3A5CCOZHW5RIX6ZEWBJLJQ" #"NNSXS.ZL4ZNNGP77E6YB73I7ZARXEUMSB2RESQWXAWEUA.HJDVR7SHXTEYCCQIWQDSPHHHNZWABA3NNNOJNHHFS3KJQ35UIE7Q"

#Setting up callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to broker MQTT with result code "+str(rc)+" using flags "+str(flags))
    client.subscribe("v3/sensores-espe@ttn/devices/eui-sensores-1/up")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(payload)

#Setting up the MQTT client
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(mqtt_username, mqtt_password)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

#Connecting to the MQTT broker on separate thread
def connect_mqtt():
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)
    mqtt_client.loop_start()

@app.route('/connect')
def connect():
    connect_mqtt()
    return "Connected to MQTT broker"

if __name__ == '__main__':
    app.run()









