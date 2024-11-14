import struct
import asyncio
import network
import espnow
import os
import random
from machine import Pin, I2S
from microdot import Microdot
from utemplate import Template



#Webserver init variable
app = Microdot()

#Global variables
filename = "yee.wav"
volume = 1.0

#Button
button_pin = Pin(23,Pin.IN,Pin.PULL_UP)

#Audio
sck_pin = Pin(14)   # Serial clock output
ws_pin = Pin(13)    # Word clock output
sd_pin = Pin(12)    # Serial data output

#File opening logic
wav = open("yee.wav", "rb")

#WIFI init logic
ap = network.WLAN(network.AP_IF)
ap.active(True)

ssid, pw = "", ""
if "wifi.txt" in os.listdir():
    with open("wifi.txt","r") as file:
        ssid, pw = file.readlines()
else:
    ssid = "Dumb Doorbell"
    pw = "".join(random.choice(
    "QWERTYUIOPASDFGHJKLZXCVBNM1234567890qwertyuiopasdfghjklzxcvbnm_!+-"
    ) for i in range(8)) #random 8-chracter password generation
    with open("wifi.txt","w") as file:
        file.write(ssid+"\n"+pw)

print("SSID=",ssid)    
print("Password=",pw)
ap.config(essid=ssid, password=pw, security=3) #3 - WPA2_PSK authentication


#ESP-NOW init logic
interface = espnow.ESPNow()
interface.active(True)
peer = b"\xcc\x7b\x5c\x9a\xf1\xfc" # MAC address of wristband

#encryption keys
if "keys.txt" in os.listdir():
    with open("keys.txt","r") as file:
        pmk, lmk = file.readlines() #read primary and local master keys
        interface.set_pmk(pmk.strip()) #strip for whitespace removal just in case
        interface.add_peer(peer, ifidx=network.AP_IF, lmk=lmk.strip(), encrypt=True)
        print("Using encryption")    
else:
    #non-encrypted
    interface.add_peer(peer, ifidx=network.AP_IF)    
    print("Non-encrypted")






#audio file playing logic
async def play_ringtone():
    global wav
    global volume

    #Open I2S stream
    audio_out = I2S(0, sck=sck_pin, ws=ws_pin, sd=sd_pin,mode=I2S.TX, bits=16, format=I2S.MONO, rate=11025, ibuf=20000)
    
    #seek past the header of the file to the audio data
    pos = wav.seek(44)
    
    wav_samples_final = memoryview(bytearray(2048))
    
    while True:
        #read in 2048 bytes from the wav file
        read_bytes = wav.read(2048)
        if len(read_bytes) != 0:
            #convert bytes to integers, reduce amplitude, then multiply by volume and the put into bytearray
            e = 0
            for i in struct.unpack("B"*len(read_bytes),read_bytes):
                wav_samples_final[e] = int((i-128)*volume)
                e+=1
            print("writing")
            audio_out.write(wav_samples_final)
            await asyncio.sleep_ms(1)
        else:
            break

    wav.close()
    audio_out.deinit()








#web code:
@app.route("/")
async def index(request):
    return Template("index.html").render()














#mainloop
async def check_button():
    global wav
    global filename
    global interface
    
    
    if button_pin.value() == 0:
        # reopen file
        wav = open(filename, "rb")
        # seek to beginning of data
        wav.seek(44)
        interface.send(peer, "ring")
        
        print("registered")
        #wait before registering next button press
        host, msg = interface.recv()
        if msg:
            print(host.hex(),msg)
            
        await asyncio.sleep_ms(300)
        asyncio.create_task(play_ringtone())

        
    else:
        pass

server = asyncio.create_task(app.start_server(port=80))
while True:
    asyncio.run(check_button())