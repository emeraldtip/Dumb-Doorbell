import struct
import asyncio
import network
import espnow
import os
import random
import json
from machine import Pin, I2S
from microdot import Microdot, send_file, Request
from utemplater import Template
import gc


#Webserver init variable
app = Microdot()
Request.max_content_length = 1024 * 1024

#Global variables
filename = "sound.wav"
volume = 0.5
pattern = 1.0
samplerate = 11025

#Button
button_pin = Pin(23,Pin.IN,Pin.PULL_UP)

#Audio
sck_pin = Pin(14)   # Serial clock output
ws_pin = Pin(13)    # Word clock output
sd_pin = Pin(12)    # Serial data output

#File opening logic
wav = open(filename, "rb")

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



#Load settings from previous session
if "settings.txt" in os.listdir():
    with open("settings.txt","r") as file:
        volume, settings = [float(i) for i in file.readlines()]
        print(volume,settings)
    print("read")


wav_samples_final = memoryview(bytearray(512))
#audio file playing logic
async def play_ringtone():
    #clear ram
    gc.collect()
   
    global wav
    global volume
    global wav_samples_final
    global samplerate
    global bits_per_sample

    await asyncio.sleep_ms(1)

    #Open I2S stream
    audio_out = I2S(0, sck=sck_pin, ws=ws_pin, sd=sd_pin,mode=I2S.TX, bits=16, format=I2S.MONO, rate=samplerate, ibuf=5120)
        

    #seek past the header of the file to the audio data
    pos = wav.seek(44)
    
    while True:
        
        read_bytes = ""
        try:
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
    global volume
    vol = int(volume*100)
    return Template("index.html").render(vol=vol), {'Content-Type': 'text/html'}

#static file routing
@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    if "ffmpeg" in path:
        return send_file('static/' + path, compressed=True)
    return send_file('static/' + path)

#updating parameters
@app.post('/update',)
async def updet(request):
    global volume
    global pattern
    
    print("update")
    if request.method == "POST":
        data = request.json
        print(data)
        if len(data) != 0:
            vol = int(data.get("volume"))
            patt = int(data.get("pattern"))
            reset = int(data.get("reset"))
            print(vol)
            print(patt)
            print(reset)
            if reset == 0:
                print("dontreset")
                volume = vol/100
                pattern = patt
            else:
                print("reset")
                volume = 0.5
                pattern = 1.0
            with open("settings.txt","w+") as file:
                file.write(str(volume)+"\n"+str(pattern))
    return json.dumps({"success":True,"message":"Successfully updated!"}), 200, {'ContentType':'application/json'}

#file upload bs
@app.post('/upload')
async def upload(request):
    # obtain the filename and size from request headers
    filename = request.headers['Content-Disposition'].split(
        'filename=')[1].strip('"')
    size = int(request.headers['Content-Length'])


    # write the file to the files directory in 1K chunks
    with open("sound.wav", 'wb') as f:
        while size > 0:
            chunk = await request.stream.read(min(size, 1024))
            f.write(chunk)
            size -= len(chunk)

    print('Successfully saved file: ' + filename)
    return ''







#mainloop
async def check_button():
    global wav
    global filename
    global interface
    global samplerate
    global bits_per_sample
    
    if button_pin.value() == 0:
        #(re)open file
        wav = open(filename, "rb")
        #seek to read the samplerate
        wav.seek(24)
        samplerate = int.from_bytes(wav.read(4),"little")
        print("Samplerate:",samplerate)
        #seek to beginning of data
        wav.seek(44)
        if pattern == 1.0:
            interface.send(peer, "ring")
        elif pattern == 2.0:
            interface.send(peer, "tone")
        print("registered")
        
        #wait before registering next button press
        await asyncio.sleep_ms(300)
        asyncio.create_task(play_ringtone())
    else:
        pass

asyncio.create_task(app.start_server(port=80))
while True:
    asyncio.run(check_button())