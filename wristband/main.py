from machine import Pin, Timer

led = Pin(19, Pin.OUT)
tim = Timer(0)

tim.init(period = 500, mode = Timer.PERIODIC, callback = lambda t: blink(led))

def blink(pin: Pin):
    if pin.value() == 0: pin.value(1)
    else: pin.value(0)