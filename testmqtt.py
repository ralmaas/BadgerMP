#=============================
# Based on this code: https://microcontrollerslab.com/raspberry-pi-pico-w-mqtt-client-publish-subscribe-messages/
# and modified for Badger
#=============================
import badger2040w as badger2040
from machine import Pin
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import gc
from badger2040w import WIDTH
from badger2040w import HEIGHT

gc.collect()


mqtt_server = '192.168.198.227'  #Replace with your MQTT Broker IP

display = badger2040.Badger2040W()
print("Try to connect")
display.connect() # Her benyttes informasjone fra WIFI_CONFIG.py til å koble opp mot nettverk

client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'rpi_pico_w/test_sub'


#while station.isconnected() == False:
#  pass

print('Connection successful')
# print("Set IP to: " + display.ifconfig())

def sub_cb(topic, msg):
    print ('Received Message %s from topic %s' %(msg, topic))

    display.clear()
    display.set_font("bitmap8_outline")
    display.set_pen(15)
    display.rectangle(0, 0, WIDTH, HEIGHT)
    display.set_pen(0)
    display.text(topic + ":", 3, 10, WIDTH, 3)
    display.text(msg, 10, 32, WIDTH, 3)
    display.update()

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()
  
while True:
  try:
       new_msg = client.check_msg()
     
  except OSError as e:
    restart_and_reconnect