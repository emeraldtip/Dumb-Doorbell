import os
import time
import struct
from machine import Pin, I2S

#button_pin = Pin(23,Pin.IN,Pin.PULL_UP)


#Audio
sck_pin = Pin(14)   # Serial clock output
ws_pin = Pin(13)    # Word clock output
sd_pin = Pin(12)    # Serial data output


audio_out = I2S(0, sck=sck_pin, ws=ws_pin, sd=sd_pin,mode=I2S.TX, bits=16, format=I2S.MONO, rate=11025, ibuf=20000)


wav = open("yee.wav", "rb")
pos = wav.seek(44)

wav_samples_final = memoryview(bytearray(2048))

#while True:
#	if button_pin.value() == 0:
#		buzzer_pin.duty(200)
#	else:
#		buzzer_pin.duty(0)
print("start playback")

while True:
    #read in 2048 bytes from the wav file
    read_bytes = wav.read(2048)
    if len(read_bytes) != 0:
        #convert bytes to integers, reduce amplitude (-64) and the put into bytearray
        #wav_samples = memoryview(byt
        e = 0
        for i in struct.unpack("B"*len(read_bytes),read_bytes):
            #print(i)
            wav_samples_final[e] = int(i-64)
            #print(wav_samples_final[e])
            e+=1

        audio_out.write(wav_samples_final)
    else:
        break


wav.close()
audio_out.deinit()
print("Done")