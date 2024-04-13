import sys
import time
import random
from Adafruit_IO import MQTTClient
from teachable_ai import get_ai_info

AIO_FEED_ID = ["humid_update", "light_update"]
AIO_USERNAME = "khoaphamce"
AIO_KEY = "aio_qpyz29sOGxoKjdJD4bjwn3iLrbpS"

GREEN = "00FF00"
RED = "FF0000"

def send_hum(client):
  hum = random.randint(0, 100) + random.random()
  client.publish("humidity", hum)

def send_light(client):
  light = random.randint(0, 100) + random.random()
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


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect ()
client.loop_background ()

delay_time = 8
counter = delay_time
while True:
    counter = counter - 1

    if (counter <= 0):
      counter = delay_time
      temp = random.randint(18, 35) + random.random()
      if (temp >= 27):
         client.publish("temperature_light", RED)
      else:
         client.publish("temperature_light", GREEN)
      client.publish("temperature", temp)
      client.publish("teachable", get_ai_info())
    
    time.sleep(2)
    pass