from machine import PWM, Pin


class Motor:

    def __init__(self, forwardPin, reversePin, speedPin):

        self.speedPin = PWM(Pin(speedPin))
        self.forwardPin = Pin(forwardPin, Pin.OUT)
        self.reversePin = Pin(reversePin, Pin.OUT)

    def forward(self, speed):
        self.reversePin.off()
        self.forwardPin.on()
        self.speedPin.freq(50)
        self.speedPin.duty_u16(int(speed / 100 * 65536))

    def reverse(self, speed):
        self.forwardPin.off()
        self.reversePin.on()
        self.speedPin.freq(50)
        self.speedPin.duty_u16(int(speed / 100 * 65536))

    def stop(self):
        self.reversePin.off()
        self.forwardPin.off()
