#plays bad apple when you press the button

import os
import time
import struct
import asyncio
from machine import Pin, I2S

#Button
button_pin = Pin(23,Pin.IN,Pin.PULL_UP)

#Audio
sck_pin = Pin(14)   # Serial clock output
ws_pin = Pin(13)    # Word clock output
sd_pin = Pin(12)    # Serial data output

#file opening logic
wav = open("badappe-2048.wav", "rb")

#audio file playing logic
async def play_ringtone():
    global wav
    
    #Open I2S stream
    #11025
    audio_out = I2S(0, sck=sck_pin, ws=ws_pin, sd=sd_pin,mode=I2S.TX, bits=16, format=I2S.MONO, rate=2048, ibuf=20000)
    
    #seek past the header of the file to the audio data
    pos = wav.seek(44)
    
    wav_samples_final = memoryview(bytearray(2052))
    
    while True:
        #read in 2048 bytes from the wav file
        try:
            read_bytes = wav.read(342)
        except:
            read_bytes = ""
        if len(read_bytes) != 0:
            #convert bytes to integers, reduce amplitude (-32) and the put into bytearray
            e = 0
            for i in struct.unpack("B"*len(read_bytes),read_bytes):
                wav_samples_final[e] = int((i-128))
                wav_samples_final[e+1] = int((i-128))
                wav_samples_final[e+2] = int((i-128))
                wav_samples_final[e+3] = int((i-128))
                wav_samples_final[e+4] = int((i-128))
                wav_samples_final[e+5] = int((i-128))
                e+=6
            print("writing")
            audio_out.write(wav_samples_final)
            await asyncio.sleep_ms(1)
        else:
            break
    
    wav.close()
    audio_out.deinit()


async def check_button():
    if button_pin.value() == 0:
        global wav
        # reopen file
        wav = open("badappe-2048.wav", "rb")
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