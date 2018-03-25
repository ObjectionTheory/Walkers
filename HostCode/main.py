from servo_controller import Servo

class Limb:
    def __init__(self, identity, servos):
        self.base = servos[0]
        self.middle = servos[1]
        self.tip = servos[2]

    def extend(self, dist)