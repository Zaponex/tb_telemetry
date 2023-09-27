import paho.mqtt.client as mqtt
import json
import time
import serial


serial_port = '/dev/ttyUSB2'
baud_rate = 115200

# ThingsBoard MQTT-Broker-Einstellungen 
from config import broker_address, broker_port, access_token, mqtt_topic

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

def start_gps():
    
    ser = serial.Serial(serial_port, baud_rate, timeout = 1)
    command = "AT+CGPS=1\r\n"
    ser.write(command.encode('utf-8'))
    time.sleep(5)
    response = ser.readline().decode('utf-8').strip()
    print(response)
    if response: 
        read_gps_data()

    else:
        print("Modul nicht erfolgreich gestartet.")


# GPS-Daten aus dem Modul
def read_gps_data():

    ser = serial.Serial(serial_port, baud_rate, timeout = 1)

    try:

            while True:
            
                command = "AT+CGPSINFO\r\n"
                ser.write(command.encode('utf-8'))
                response = ser.readline().decode('utf-8').strip()

                if response:

                    print(response)
                    parts = response.split(': ')

                    if len(parts) >=2:
                        
                        command = parts[0]
                        data = parts[1]
                        seperation = data.split(',')
                        
                        if len(seperation) >=4:
                            
                            dms_latitude = seperation[0]  # Latitude im Format "5327.770639"
                            dms_longitude = seperation[2]  # Longitude im Format "957.744034"
                            
                            # Finden des Punktes für Koordinatentrennung
                            string_dms_longitude = str(dms_longitude)
                            punkt_position = string_dms_longitude.find('.')
                            
                            #Überprüfung auf das Format der Koordinate
                            if punkt_position == 3:
                                degrees_long = float(dms_longitude[:1])
                                minutes_long = float(dms_longitude[1:3]) / 60  
                                secconds_long = float(dms_longitude[3:]) / 60

                            elif punkt_position == 4:
                                degrees_long = float(dms_longitude[:2])
                                minutes_long = float(dms_longitude[2:4]) / 60  
                                secconds_long = float(dms_longitude[4:]) / 60

                            elif punkt_position == 5:
                                degrees_long = float(dms_longitude[:3])
                                minutes_long = float(dms_longitude[3:5]) / 60  
                                secconds_long = float(dms_longitude[5:]) / 60

                            #Extrahieren der Degrees 
                            degrees_lat = float(dms_latitude[:2])
                            
                            # Extrahieren der Minuten 
                            minutes_lat = float(dms_latitude[2:4]) / 60
                            

                            #Extarahieren Sekunden aber nur 2 Stellen
                            secconds_lat = float(dms_latitude[4:]) / 60


                            latitude = degrees_lat + minutes_lat + secconds_lat
                            longitude = degrees_long + minutes_long + secconds_long


                            print(f"LAT (DD): {latitude}, LON (DD): {longitude}")
                            
                            payload = {
                              "latitude": latitude,
                              "longitude": longitude,
                              }
                            
                            client.publish(mqtt_topic, json.dumps(payload))
                            print("Datenpunkte gesendet!")
                            
                time.sleep(10)
        
    except KeyboardInterrupt:
        ser.close()

#Loop für den zyklischenn Transfer der Daten
while True:
    start_gps()
    time.sleep(10)

if __name__ == "__main__":
    read_gps_data()
