from motor import Motor
from request_parser import RequestParser
from stearing import Stearing
from wifi import connect_wifi
import _thread
import socket
import time


stearing = Stearing()
engineTimer = 3
stearingTimer = 1
lock = _thread.allocate_lock()
motor = Motor(14, 15)


def mainLoop():
    global engineTimer, stearingTimer, motor

    while True:
        lock.acquire()

        if stearingTimer > 0:
            stearingTimer -= 1

        if engineTimer > 0:
            engineTimer -= 1

        lock.release()
        time.sleep(.33)

        if stearingTimer == 0:
            stearing.end()

        if engineTimer == 0:
            motor.stop()


_thread.start_new_thread(mainLoop, ())


class Server:

    def resetTimers(self):
        global stearingTimer, lock, engineTimer

        lock.acquire()
        engineTimer = 3
        stearingTimer = 1
        lock.release()

    def __init__(self):
        global motor, stearing

        self.stearing = stearing
        self.motor = motor
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
                raw_request = cl.recv(1024)
                self.resetTimers()

                p = RequestParser(raw_request.decode("utf-8"))
                print(p.json['pid'])
                # dir = self.getMoveDirection(request)

                # self.powerMotor(90, dir)

                # if dir == 'forw':
                #     self.stearing.leftTurn(90)
                # else:
                #     self.stearing.rightTurn(90)

                cl.send(
                    'HTTP/1.0 200 OK\r\nContent-type: text/plain\r\nAccess-Control-Allow-Origin: * \r\n\r\n')

                cl.close()

            except Exception as e:
                print(e)
                # blink_dance.blink_dance()
                print('connection closed')

                if cl:
                    cl.close()
