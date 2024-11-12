from machine import Pin
import time

vibr = Pin(13, Pin.OUT)

flag = False #Using the variable as
#if you just read the value of the pin from the ESP, it will always read 0
#as the vibration motor pulls too much current and pulls the voltage
#of the pin too low


def toggle(pin: Pin):
    global flag

    pin.value(flag)
    print("toggled",flag)
    flag = not flag

while True:
    toggle(vibr)
    time.sleep(1)