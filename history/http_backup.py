import serial
import time
import requests


serial_port = '/dev/ttyUSB2'
baud_rate = 115200
def read_gps_data():

    ser = serial.Serial(serial_port, baud_rate, timeout = 1)

    try:

            while True:
            
                command = "AT+CGPSINFO\r\n"
                ser.write(command.encode('utf-8'))
            
                response = ser.readline().decode('utf-8').strip()
                if response:
                    print(response)
                    #if "+CGPSINFO:" in response:
                        
                    parts = response.split(': ')
                    if len(parts) >=2:
                        #print(parts)
                        command = parts[0]
                        data = parts[1]
                        seperation = data.split(',')
                        #print(seperation)
                        if len(seperation) >=4:
                            dms_latitude = seperation[0]  # Latitude im Format "5327.770639"
                            dms_longitude = seperation[2]  # Longitude im Format "957.744034"
                            
                            string_dms_longitude = str(dms_longitude)
                            punkt_position = string_dms_longitude.find('.')
                            
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


                            #print(dms_latitude, dms_longitude, degrees_lat, degrees_long, minutes_lat, minutes_long, secconds_lat, secconds_long)

                            latitude = degrees_lat + minutes_lat + secconds_lat
                            longitude = degrees_long + minutes_long + secconds_long


                            print(f"LAT (DD): {latitude}, LON (DD): {longitude}")
                            
                            
                            
                            node_red_url = 'http://51.144.148.72:8080/api/v1/BJebdbC5PJXAsmXiQgjJ/telemetry'  # Passe die URL an
                            gps_data = {
                                'latitude': latitude,
                                'longitude': longitude
                            }
                            

                            response = requests.post(node_red_url, json=gps_data)
                            print("X")

                            if response.status_code == 200:
                                print("Daten erfolgreich gesendet!")
                            else:
                                print(f"Fehler beim Senden: {response.status_code}")
                            
                time.sleep(10)
            
        #ser.write(b'AT$GPSQ\r\n')
        #response = ser.readline().decode('utf-8').strip()
        #print(response)
        
    except KeyboardInterrupt:
        ser.close()

if __name__ == "__main__":
    read_gps_data()






