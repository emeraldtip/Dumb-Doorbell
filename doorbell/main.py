import os
import time
import struct
import asyncio
from machine import Pin, I2S

button_pin = Pin(23,Pin.IN,Pin.PULL_UP)


#Audio
sck_pin = Pin(14)   # Serial clock output
ws_pin = Pin(13)    # Word clock output
sd_pin = Pin(12)    # Serial data output

wav = open("yee.wav", "rb")


async def play_ringtone():
    audio_out = I2S(0, sck=sck_pin, ws=ws_pin, sd=sd_pin,mode=I2S.TX, bits=16, format=I2S.MONO, rate=11025, ibuf=20000)
    
    pos = wav.seek(44)
    
    wav_samples_final = memoryview(bytearray(2048))
    
    while True:
        #read in 2048 bytes from the wav file
        read_bytes = wav.read(2048)
        if len(read_bytes) != 0:
            #convert bytes to integers, reduce amplitude (-64) and the put into bytearray
            e = 0
            for i in struct.unpack("B"*len(read_bytes),read_bytes):
                wav_samples_final[e] = int(i-120)
                e+=1
            print("writing")
            audio_out.write(wav_samples_final)
            await asyncio.sleep_ms(1)
        else:
            break

    wav.close()
    audio_out.deinit()


async def check_button():
    if button_pin.value() == 0:
        wav = open("yee.wav", "rb")
        wav.seek(44)
        await asyncio.sleep(1)
        asyncio.create_task(play_ringtone())
        print("gaming")
    else:
        print("no")

while True:
    asyncio.run(check_button())