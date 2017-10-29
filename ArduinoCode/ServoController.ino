
#include <Servo.h>

String input;
int servoCount = 8;

Servo servos[8];
int servoPins[] = {16, 5, 4, 0, 14, 12, 13, 15};
int startPositions[] = {80, 100, 80, 100, 50, 130, 50, 130};

void setup()
{
  Serial.begin(9600);
  
  for (int i = 0; i < servoCount; i++) {
    Servo newServo;
    servos[i] = newServo;
    servos[i].attach(servoPins[i]);
    servos[i].write(startPositions[i]);
  }
}

void loop() {
  if (Serial.available() > 0) {
    input = Serial.readStringUntil('X');
    int identity = input.substring(0, 1).toInt();
    int pos = map(input.substring(1).toInt(), 0, 180, 24, 170);
    servos[identity].write(pos);
    Serial.println(input);
  }
}

void record() {
  
}

