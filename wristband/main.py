from machine import Pin
import time

led = Pin(13, Pin.OUT)

def toggle(pin: Pin):
    pin.value(not pin.value())

while True:
    toggle(led)
    time.sleep(1)