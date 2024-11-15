import struct
import asyncio
import network
import espnow
import os
import random
import json
from machine import Pin, I2S
from microdot import Microdot, send_file
from utemplater import Template
import gc



#Webserver init variable
app = Microdot()

#Global variables
filename = "yee.wav"
volume = 0.5
pattern = 1

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






def set_volume(voe):
    global volume
    volume = voe


wav_samples_final = memoryview(bytearray(512))
#audio file playing logic
async def play_ringtone():
    #clear ram
    gc.collect()
   
    global wav
    global volume
    global wav_samples_final

    await asyncio.sleep_ms(1)

    #Open I2S stream
    audio_out = I2S(0, sck=sck_pin, ws=ws_pin, sd=sd_pin,mode=I2S.TX, bits=16, format=I2S.MONO, rate=11025, ibuf=5000)
        

    #seek past the header of the file to the audio data
    pos = wav.seek(44)
    
    while True:
        
        read_bytes = ""
        try:
            #read in 2048 bytes from the wav file
            read_bytes = wav.read(512)
        except:
            pass
            
        if len(read_bytes) != 0:
            #convert bytes to integers, reduce amplitude, then multiply by volume and the put into bytearray
            e = 0
            for i in struct.unpack("B"*len(read_bytes),read_bytes):
                wav_samples_final[e] = int((i-128)*volume*2)
                e+=1
            #print("writing")
            audio_out.write(wav_samples_final)
            await asyncio.sleep_ms(1)
        else:
            break

    wav.close()
    audio_out.deinit()








#web code:
@app.route("/")
async def index(request):
    vol = int(volume*100)
    return Template("index.html").render(vol=vol), {'Content-Type': 'text/html'}



#static file routing
@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)

#updating parameters
@app.post('/update',)
async def updet(request):
    #global volume
    #global pattern
    
    print("update")
    if request.method == "POST":
        data = request.json
        print(data)
        if len(data) != 0:
            vol = int(data.get("volume"))
            pattern = int(data.get("pattern"))
            resee = int(data.get("reset"))
            print(vol)
            print(pattern)
            print(resee)
            if resee == 0:
                print("dontreset")
                set_volume(float(vol/100))
                pattern = pattern

    return json.dumps({"success":True,"message":"Successfully updated!"}), 200, {'ContentType':'application/json'}








#mainloop
async def check_button():
    global wav
    global filename
    global interface
    
    if button_pin.value() == 0:
        #(re)open file
        wav = open(filename, "rb")
        #seek to beginning of data
        wav.seek(44)
        interface.send(peer, "ring")
        
        print("registered")
        
        #wait before registering next button press
        await asyncio.sleep_ms(300)
        asyncio.create_task(play_ringtone())
    else:
        pass

asyncio.create_task(app.start_server(port=80))
while True:
    asyncio.run(check_button())