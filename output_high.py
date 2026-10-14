from machine import Pin
from utime import sleep_ms

pin = Pin("GP22", Pin.OUT)
while True:
    pin.on()
    #print("working?")
    sleep_ms(10)
    