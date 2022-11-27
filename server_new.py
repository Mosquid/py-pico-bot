from motor import Motor
from wifi import connect_wifi
import _thread
import socket
import time

timer = 3
lock = _thread.allocate_lock()


def secondThread():
    global timer
    motor = Motor(14, 15)

    while True:
        lock.acquire()

        if timer > 0:
            timer -= 1

        lock.release()
        time.sleep(.33)

        if timer == 0:
            motor.stop()


_thread.start_new_thread(secondThread, ())


class Server:

    def resetTimer(self):
        global timer
        global lock

        lock.acquire()
        timer = 3
        lock.release()

    def __init__(self):

        self.motor = Motor(14, 15)
        self.motor.stop()
        connect_wifi()
        self.start_server()
        self.serve()

    def start_server(self):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]  # type: ignore
        self.socket = socket.socket()  # type: ignore
        self.socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # type: ignore
        self.socket.bind(addr)
        self.socket.listen(5)

        print('listening by new server on', addr)

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
                self.resetTimer()
                dir = self.getMoveDirection(request)

                self.powerMotor(90, dir)

                cl.send(
                    'HTTP/1.0 200 OK\r\nContent-type: text/plain\r\nAccess-Control-Allow-Origin: * \r\n\r\n')

                cl.close()

            except Exception as e:
                print(e)
                # blink_dance.blink_dance()
                print('connection closed')

                if cl:
                    cl.close()
