import time
import network
import espnow
import os
from machine import Pin


vibr = Pin(13, Pin.OUT)
button = Pin(25 , Pin.IN, Pin.PULL_UP)

flag = False #Using the variable as
#if you just read the value of the pin from the ESP, it will always read 0
#as the vibration motor pulls too much current and pulls the voltage
#of the pin too low

#WIFI setup for ESP-NOW
net = network.WLAN(network.STA_IF)
net.active(True)

#ESP-NOW setup
interface = espnow.ESPNow()
interface.active(True)
peer = b'\x30\xae\xa4\x76\x23\x21' # MAC address of doorbell

#encryption keys
if "keys.txt" in os.listdir():
    with open("keys.txt","r") as file:
        print('using encryption')
        pmk, lmk = file.readlines() #read primary and local master keys
        interface.set_pmk(pmk.strip())
        interface.add_peer(peer, ifidx=network.STA_IF, lmk=lmk.strip(), encrypt=True)      
else:
    #non-encrypted
    interface.add_peer(peer, ifidx=network.STA_IF)    

def turnoff(pin:Pin):
    pin.value(1)
    counter = 10
    while button.value() ==0 and counter>0 :
        pin.value(1)
        time.sleep(1)
        counter-=1
    pin.value(0)


def toggle(pin: Pin):
    global flag

    pin.value(flag)
    print("toggled",flag)
    flag = not flag


while True:
    host, msg = interface.recv()
    if msg: #If no message is received then msg=None
        print(host.hex(), msg)
        interface.send(peer, "received")
        if msg == b"ring":
            counter = 20
            while counter>0 :
                vibr.value(1)
                time.sleep(0.5)
                counter-=1
                print(button.value())
                if button.value() == 0: break
            vibr.value(0)


        

#while True:
#    toggle(vibr)
#    time.sleep(1)