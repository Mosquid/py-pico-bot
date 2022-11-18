import socket
import network
import secrets
import time
from blink_dance import blink_dance
from machine import Pin
from motor import Motor

ledOn = False
led = Pin("LED", Pin.OUT)
motor = Motor(14, 15)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)

html = """<!DOCTYPE html>
<html>

    <head><title>Pico W</title><link rel="icon" href="data:;base64,iVBORw0KGgo="></head>
    <body> <h1>Pico W</h1>
    </body>
</html>
"""

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]  # type: ignore
s = socket.socket()  # type: ignore
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # type: ignore
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Listen for connections
while True:
    cl = None
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)

        if ledOn == True:
            motor.forward(100)
            ledOn = False
        else:
            motor.stop()
            ledOn = True

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
        cl.close()

    except OSError as e:
        blink_dance()
        print('connection closed')

        if cl:
            cl.close()
