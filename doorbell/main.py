import os
import time
from machine import Pin, I2S

#button_pin = Pin(23,Pin.IN,Pin.PULL_UP)


#Audio
sck_pin = Pin(14)   # Serial clock output
ws_pin = Pin(13)    # Word clock output
sd_pin = Pin(12)    # Serial data output


audio_out = I2S(0, sck=sck_pin, ws=ws_pin, sd=sd_pin,mode=I2S.TX, bits=16, format=I2S.MONO, rate=11025, ibuf=20000)

# some code from from https://github.com/miketeachman/micropython-i2s-examples
# The MIT License (MIT)
# Copyright (c) 2022 Mike Teachman
# https://opensource.org/licenses/MIT
#
# Purpose:  Play a WAV audio file out of a speaker or headphones
#
wav = open("yee.wav", "rb")
pos = wav.seek(44)

wav_samples = bytearray(1000)
wav_samples_mv = memoryview(wav_samples)

#while True:
#	if button_pin.value() == 0:
#		buzzer_pin.duty(200)
#	else:
#		buzzer_pin.duty(0)

print("start playback")
try:
    while True:
        num_read = wav.readinto(wav_samples_mv)
        # end of WAV file?
        if num_read == 0:
            # end-of-file, advance to first byte of Data section
            #_ = wav.seek(44)
        else:
            _ = audio_out.write(wav_samples_mv[:num_read])

except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

# cleanup
wav.close()
audio_out.deinit()
print("Done")