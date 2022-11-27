from machine import Pin
import server_new
import machine


led = Pin("LED", Pin.OUT)

try:
    led.on()
    server = server_new.Server()
except Exception as e:
    print(e)
    led.off()
    machine.reset()
