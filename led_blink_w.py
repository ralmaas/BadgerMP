import utime
from machine import Pin

led_onboard = Pin("LED", Pin.OUT)

while True:
    led_onboard.on()
    utime.sleep(5)
    led_onboard.off()
    utime.sleep(5)