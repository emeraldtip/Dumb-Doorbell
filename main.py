from machine import Pin, PWM

button_pin = Pin(23,Pin.IN,Pin.PULL_UP)
buzzer_pin = PWM(Pin(22,Pin.OUT),1000)

while True:
	if button_pin.value() == 0:
		buzzer_pin.duty(200)
	else:
		buzzer_pin.duty(0)
		