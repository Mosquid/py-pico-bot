from machine import Pin
from time import sleep

ledOn = True
led = Pin("LED", Pin.OUT)

def blink_dance():
    loops = 5
    while loops > 0:
        loops -= 1
        led.on()
        sleep(.1)
        led.off()
        sleep(.1)
        led.on()
        sleep(.1)
        led.off()