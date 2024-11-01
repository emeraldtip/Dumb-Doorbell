from machine import Pin, PWM, I2S

button_pin = Pin(23,Pin.IN,Pin.PULL_UP)
buzzer_pin = PWM(Pin(22,Pin.OUT),1000)


#Audio
sck_pin = Pin(14)   # Serial clock output
ws_pin = Pin(13)    # Word clock output
sd_pin = Pin(12)    # Serial data output


audio_out = I2S(2,
                sck=sck_pin, ws=ws_pin, sd=sd_pin,
                mode=I2S.TX,
                bits=16,
                format=I2S.MONO,
                rate=44100,
                ibuf=20000)



#while True:
#	if button_pin.value() == 0:
#		buzzer_pin.duty(200)
#	else:
#		buzzer_pin.duty(0)