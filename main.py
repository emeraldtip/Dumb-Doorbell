from machine import Pin

button_pin = Pin(23,Pin.IN,Pin.PULL_UP)

while True:
	a = input(button_pin.value())
	if a == "EXIT":
		exit()