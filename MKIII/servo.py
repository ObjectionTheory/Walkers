import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

class Servo:
    def __init__(self, identity, angle=90, offset=0):
        self.id = identity
        self.angle = angle
        self.offset = offset
        self.min = 0
        self.max = 180
    
    def update(self, angle):
        angle = angle-self.offset
        if angle > self.min and angle < self.max:
            kit.servo[self.id].angle = angle
            self.angle = angle
