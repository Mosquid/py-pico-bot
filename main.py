import server_new
from machine import Pin
led = Pin("LED", Pin.OUT)

led.on()

server = server_new.Server()
