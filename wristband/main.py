import time
import network
import espnow
import os
from machine import Pin
import re


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
        
        message = str(msg).strip("b'")
#        if bool(re.match('^[-. ]*$',message[1])):
#            for i in message:
#                if i==' ': 
#                    vibr.off()
#                    time.sleep(1.5)
#
#                elif i == '-':
#                    vibr.on()
#                    time.sleep(1.5)
#                    vibr.off()
#                elif i == '.':
#                    vibr.on()
#                    time.sleep(0.5)
#                    vibr.off()
#                if button.value() == 0: break
        if msg == b"ring":
            counter = 20
            while counter>0 :
                vibr.value(1)
                time.sleep(0.5)
                counter-=1
                if button.value() == 0: break
            vibr.value(0)
        elif msg == b"tone":
            counter = 10
            while counter>0:
                for x in range(1,3):
                    vibr.value(1)
                    time.sleep(1)
                    vibr.off()
                    time.sleep(0.5)
                    counter -=1
                    if button.value() == 0: break


        

#while True:
#    toggle(vibr)
#    time.sleep(1)