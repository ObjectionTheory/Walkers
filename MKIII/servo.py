import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

class Servo:
    def __init__(self, identity, angle=90, offset=0):
        self.id = identity
        self.angle = angle
        self.offset = offset
    
    def update(self, angle):
        if angle > self.min anf angle < self.max:
            kit.servo[self.id].angle = angle-self.offset
            self.angle = angle-offset