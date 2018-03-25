import servo_controller as servo
import time

servos = [servo.Servo(i) for i in range(12)]

for i in servos:
    i.set_angle(90)
    time.sleep(1)