from motor import Motor


class Stearing:
    def __init__(self):
        self.stearing = Motor(12, 11, 17)

    def leftTurn(self, angle):
        self.stearing.stop()
        self.stearing.forward(angle)

    def rightTurn(self, angle):
        self.stearing.stop()
        self.stearing.reverse(angle)

    def end(self):
        self.stearing.stop()
