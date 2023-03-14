import machine
# utime and time are the same - the time library just points to utime library
from utime import sleep

# on regular pico can use GP25 - on pico w use 'LED"
#  for regular pico use: internalLED = machine.Pin(25, machine.Pin.OUT)

# Blink the PicoW onboard LED (on the back of the Badger)
#internalLED = machine.Pin('LED', machine.Pin.OUT)

# Blink Badger LED (Front Lower left
internalLED = machine.Pin(22, machine.Pin.OUT)

while True:
    internalLED.value(1)
    sleep(1)
    internalLED.value(0)
    sleep(1)