

from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

class Servo:
    def __init__(self, channel, servo_min = 150, servo_max = 600):
        # Configure min and max servo pulse lengths
        self.servo_min = servo_min  # Min pulse length out of 4096
        self.servo_max = servo_max  # Max pulse length out of 4096
        self.channel = channel

    def set_angle(self, degrees):
        value = int((self.servo_max - self.servo_min)/180 * degrees)
        pwm.set_pwm(self.channel, 0, self.servo_min + value)

Stukov = Servo(0)
Stukov.set_angle(90)