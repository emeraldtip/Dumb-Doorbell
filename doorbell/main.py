import os
import time
import struct
import asyncio
from machine import Pin, I2S

#variables
filename = "yee.wav"
volume = 1.0

#Button
button_pin = Pin(23,Pin.IN,Pin.PULL_UP)

#Audio
sck_pin = Pin(14)   # Serial clock output
ws_pin = Pin(13)    # Word clock output
sd_pin = Pin(12)    # Serial data output

#file opening logic
wav = open("yee.wav", "rb")

#audio file playing logic
async def play_ringtone():
    global wav

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


async def check_button():
    global wav
    if button_pin.value() == 0:
        # reopen file
        wav = open("yee.wav", "rb")
        # seek to beginning of data
        wav.seek(44)
        
        print("registered")
        #wait before registering next button press
        await asyncio.sleep_ms(300)
        asyncio.create_task(play_ringtone())
        
    else:
        pass

while True:
    asyncio.run(check_button())