print("Sensors and Actuators")

import time
import serial.tools.list_ports

from Adafruit_IO import MQTTClient
from teachable_ai import get_ai_info
import sys

AIO_FEED_ID = ["humid_update", "light_update"]
AIO_USERNAME = "khoaphamce"
AIO_KEY = "aio_qpyz29sOGxoKjdJD4bjwn3iLrbpS"

def send_hum(client,hum):
  print(f'Publishing  hum {hum}')
  client.publish("humidity", hum)

def send_light(client,light):
  print(f'Publishing light {light}')
  client.publish("light", light)

def connected(client):
    print("Connected ...")
    for topic in AIO_FEED_ID:
      client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribed ...")

def disconnected(client):
    print("Disconnected ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print(f"============== {feed_id}: {payload} ==============")
    if (feed_id == "humid_update"):
       send_hum(client)
    elif (feed_id == "light_update"):
       send_light(client)

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

portName = getPort()
print(portName)

try:
    ser = serial.Serial(port=portName, baudrate=9600)
    print("Open successfully")
except:
    print("Can not open the port")

relay1_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
relay1_OFF = [2, 6, 0, 0, 0, 0, 137, 249]

def setDevice1(state):
    if state == True:
        ser.write(relay1_ON)
    else:
        ser.write(relay1_OFF)
    time.sleep(1)
    print(serial_read_data(ser))


def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0

soil_temperature =[1, 3, 0, 6, 0, 1, 100, 11]
def readTemperature():
    serial_read_data(ser)
    ser.write(soil_temperature)
    time.sleep(1)
    return serial_read_data(ser)

soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]
def readMoisture():
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    return serial_read_data(ser)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect ()
client.loop_background ()

while True:
    print("TEST ACTUATOR")
    setDevice1(True)
    time.sleep(2)
    setDevice1(False)
    time.sleep(2)
    print("TEST SENSOR")
    # print(readMoisture())
    send_hum(readMoisture())
    time.sleep(2)
    send_light(readTemperature())
    # print(readTemperature())
    time.sleep(2)
