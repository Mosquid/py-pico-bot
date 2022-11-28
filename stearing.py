from motor import Motor


class Stearing:
    def __init__(self):
        self.stearing = Motor(17, 18)

    def leftTurn(self, angle):
        print(angle)
        self.stearing.forward(angle)

    def rightTurn(self, angle):
        self.stearing.reverse(angle)

    def end(self):
        self.stearing.stop()

    def turn(self, dir, speed):
        if dir == 'left':
            self.leftTurn(speed)
        else:
            self.rightTurn(speed)
