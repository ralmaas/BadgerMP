# =============================
#	Test Badger 2040W on MQTT
#	Programmet sender en MQTT-melding hvis man trykker på UP- eller DOWN-knappene
#	Monitorerer for data på en annen topic
#	2023-03-10/ralm
# =============================
import badger2040w as badger2040
import time
from umqtt.simple import MQTTClient
import badger_os
import utime
import network
import machine
from badger2040w import WIDTH
from badger2040w import HEIGHT
import jpegdec

APP_DIR = "/examples"
mqtt_server = '192.168.2.200'
client_id = 'bigles147'
topic_pub = b'lys/study'
topic_sub = b'han/kw'

button_a = machine.Pin(badger2040.BUTTON_A, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_b = machine.Pin(badger2040.BUTTON_B, machine.Pin.IN, machine.Pin.PULL_DOWN)
#button_c = machine.Pin(badger2040.BUTTON_C, machine.Pin.IN, machine.Pin.PULL_DOWN)
#button_down = machine.Pin(badger2040.BUTTON_DOWN, machine.Pin.IN, machine.Pin.PULL_DOWN)
#button_up = machine.Pin(badger2040.BUTTON_UP, machine.Pin.IN, machine.Pin.PULL_DOWN)

display = badger2040.Badger2040W()
display.connect() # Her benyttes informasjone fra WIFI_CONFIG.py til å koble opp mot nettverk

# Litt grafikk
def sub_ikoner():
    display.text("Light ON", 10, 110, WIDTH, 1)
    display.text("Light OFF", 110, 110, WIDTH, 1)
    icon = f"{APP_DIR}/light_on.jpg"
    jpeg.open_file(icon)
    jpeg.decode(20, 50)
    icon2 = f"{APP_DIR}/light_off.jpg"
    jpeg.open_file(icon2)
    jpeg.decode(120, 50)

# Noen subroutiner for MQTT
def sub_cb(topic, msg):
    print("New message on topic {}: ".format(topic.decode('utf-8')), end='')
    msg = msg.decode('utf-8')
    print(msg)
    display.set_pen(15)
    display.rectangle(200, 40, 65, 50)
    display.set_pen(0)
    display.text(topic, 200, 40, WIDTH, 2)
    display.text(msg, 210, 65, WIDTH, 2)
    display.update()
        
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

# Koble opp mot MQTT
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

# Håndter display'et
display.clear()
# display.set_font("bitmap8")
display.set_font("bitmap14_outline")
display.set_pen(15)
display.rectangle(0, 0, WIDTH, HEIGHT)
display.set_pen(0)
#display.text("Light On  ==>", 200, 30, WIDTH, 1)
#display.text("Light Off ==>", 200, 90, WIDTH, 1)
display.text("Study Light", 3, 4, WIDTH, 3)

jpeg = jpegdec.JPEG(display.display)

sub_ikoner()
display.update()

while True:
    client.subscribe(topic_sub)
    if button_a.value():
        client.publish(topic_pub, "1")
        utime.sleep(1)

    if button_b.value():
        client.publish(topic_pub, "0")
        utime.sleep(1)

