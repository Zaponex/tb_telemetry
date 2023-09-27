import paho.mqtt.client as mqtt
import json
import time

# ThingsBoard MQTT-Broker-Einstellungen (Anpassen)
broker_address = "51.144.148.72"
broker_port = 1883
access_token = "hm12Dp0Hob9Lzw8yX9e2"
mqtt_topic = "v1/devices/roboter/telemetry"



# MQTT Callback-Funktion, die aufgerufen wird, wenn die Verbindung hergestellt ist
def on_connect(client, userdata, flags, rc):
    print("Verbunden mit ThingsBoard MQTT-Broker")

# MQTT Client erstellen
client = mqtt.Client()
client.on_connect = on_connect

# Mit dem MQTT-Broker verbinden
client.username_pw_set(access_token, password=None)
client.connect(broker_address, broker_port, 60)

# Schleife für die MQTT-Kommunikation aufrechterhalten
client.loop_start()

# GPS-Daten aus dem Modul
latitude = 53.229443  # Beispiel-Latitude-Wert
longitude = 10.404726  # Beispiel-Longitude-Wert
speed = 3.5

longitude_increment = -0.00003

def send_data(client):
    global longitude
    longitude += longitude_increment
    # Erstelle ein JSON-Payload mit den GPS-Daten
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "speed": speed
    }
    client.publish(mqtt_topic, json.dumps(payload))
    print("Datenpunkte gesendet!", longitude)

#Loop für den zyklischenn Transfer der Daten
while True:
    send_data(client)
    time.sleep(10)





