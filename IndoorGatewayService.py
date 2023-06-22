from flask import Flask
import paho.mqtt.client as mqtt
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS
CORS(app)


if __name__ == '__main__':
    app.run()









