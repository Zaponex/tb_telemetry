# MQTT Subscriber

import paho.mqtt.client as mqtt

broker_address = "broker.emqx.io"
port = 1883
topic = "sensors/"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(topic)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, message):
    print(f"Received message on topic '{message.topic}': {str(message.payload)}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(broker_address, port)
    client.loop_forever()
except Exception as e:
    print(f"An error occurred: {e}")
