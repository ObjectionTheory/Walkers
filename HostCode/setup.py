import servo_controller as servo
import time

basePositions = [70, 140, 140, 70, 30, 180, 180, 30, 50, 130, 50,     130]

servos = [servo.Servo(i) for i in range(12)]

for i in range(12):
    servos[i].set_angle(basePositions[i])
    time.sleep(1.5) 