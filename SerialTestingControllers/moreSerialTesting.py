#import libraries
import serial
import time
import itertools

#initialise and open serial
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM5'
ser.writeTimeout = 0
ser.open()

queue = []

#lists of commands
reset = [
        "090",
        "190",
        "290",
        "390",
        "450",
        "5130",
        "650",
        "7130"
        ]

squat = [
        "0150",
        "120",
        "2150",
        "320",
        ]

leg2 = [
        "130",
        "5170",
        "1110",
        "560",
        "130",
        "5130",
        "1100"
        ]

leg4 = [
        "330",
        "760",
        "3110",
        "7170",
        "330",
        "7130",
        "3100"
        ]

#send arduino message via serial to rotate
def changeValue(val):
        #command = str(leg) + "" + str(val) + "X"
        command = val + "X"
        print(command)
        ser.write(command.encode())

#cycle through commands in certain list
def cycle(positions, delay = 0.07):
        for command in positions:
                if command[0] == "X":
                        time.sleep(int(command[1:]))
                yield command
                

leg2cycle = cycle(leg2, 0.1)

leg4cycle = cycle(leg4, 0.1)

time.sleep(1)

while True:
        try:
                print("derP")
                time.sleep(0.5)

                changeValue(next(leg2cycle))
                changeValue(next(leg4cycle))

        except KeyboardInterrupt:
                break
        
cycle(reset, 0)
cycle(reset, 0)



#close serial port after use
time.sleep(1)
ser.close()
