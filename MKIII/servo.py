# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

class Servo:
    
    def __init__(self, channel, angle = 90):
        self.channel = channel
        # Configure min and max servo pulse lengths
        self.servo_min = 187  # Min pulse length out of 4096
        self.servo_max = 534  # Max pulse length out of 4096
        
        self.min = 0
        self.max = 180
        self.angle = angle
    
    # Helper function to make setting a servo pulse width simpler.
    def set_servo_pulse(self, pulse):
        pulse_length = 1000000    # 1,000,000 us per second
        pulse_length //= 60       # 60 Hz
        print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096     # 12 bits of resolution
        print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        pwm.set_pwm(self.channel, 0, int(pulse))

    def mapValues(self, x, min1, max1, min2, max2):
        return min2 + (max2 - min2) * x / (max1 - min1)
    
    def setServo(self, angle):
        self.angle = angle
        self.update()

    def update(self):
        pulse = self.mapValues(self.angle, 0, 180, self.servo_min, self.servo_max)
        self.set_servo_pulse(pulse)
