from machine import Pin
from motor import Motor
from wifi import connect_wifi
import _thread
import blink_dance
import socket
import time


class Server:
    timeLeft = 3
    idleThread = None

    def __init__(self):
        self.ledOn = False
        self.led = Pin("LED", Pin.OUT)
        self.motor = Motor(14, 15)
        connect_wifi()
        self.start_server()
        self.serve()

    def start_server(self):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]  # type: ignore
        self.socket = socket.socket()  # type: ignore
        self.socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # type: ignore
        self.socket.bind(addr)
        self.socket.listen(1)

        print('listening by new server on', addr)

    def idle(self):
        while self.timeLeft > 0:
            self.timeLeft -= 1
            time.sleep(1)
            print(self.timeLeft)

        self.motor.stop()

    def powerMotor(self, speed, direction):
        if direction == 'forw':
            method = 'forward'
        else:
            method = 'reverse'

        getattr(self.motor, method)(speed)

    def getMoveDirection(self, req):
        reqString = str(req)

        if reqString.find('/forw') >= 0:
            return 'forw'
        elif reqString.find('/back') >= 0:
            return 'back'

    def serve(self):
        while True:
            cl = None
            try:
                cl, addr = self.socket.accept()
                print('client connected from', addr)
                request = cl.recv(1024)
                self.timeLeft = 3
                dir = self.getMoveDirection(request)

                self.powerMotor(90, dir)

                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
                cl.close()

                if self.idleThread is None:
                    self.idleThread = _thread.start_new_thread(self.idle, ())

            except OSError:
                blink_dance.blink_dance()
                print('connection closed')

                if cl:
                    cl.close()
