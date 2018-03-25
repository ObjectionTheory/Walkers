import servo_controller as servo
import time

basePositions = [50, 20, 20, 50, 30, 180, 180, 30, 50, 130, 50, 130]

servos = [servo.Servo(i) for i in range(12)]

for i, j in servos, range(12):
    i.set_angle(basePositions[j])
    time.sleep(1)