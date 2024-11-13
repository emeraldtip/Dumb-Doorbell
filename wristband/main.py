import time
import network
import espnow
from machine import Pin


vibr = Pin(13, Pin.OUT)

flag = False #Using the variable as
#if you just read the value of the pin from the ESP, it will always read 0
#as the vibration motor pulls too much current and pulls the voltage
#of the pin too low

#WIFI setup for ESP-NOW
net = network.WLAN(network.STA_IF)
net.active(True)

interface = espnow.ESPNow()
interface.active(True)


def toggle(pin: Pin):
    global flag

    pin.value(flag)
    print("toggled",flag)
    flag = not flag


while True:
    host, msg = interface.recv()
    if msg:             # msg == None if timeout in recv()
        print(host.hex(), msg)
        if msg == b"ring":
            vibr.value(1)
            time.sleep(10)
            vibr.value(0)
#while True:
#    toggle(vibr)
#    time.sleep(1)