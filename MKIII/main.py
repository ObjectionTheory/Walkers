#from servo import Servo
import math
import numpy as np

#the small boi
class Leg:
    def __init__(self, id):
        self.id = id

        #make sum servos
        #self.joints = [Servo(i*4+id) for i in range(3)]
        #self.joints[2].angle = 30

        #set servos to base position
        #for servo in self.joints:
        #    servo.setServo(servo.angle)

        #loving those constants                             
        self.L1 = 88    #upper leg                            
        self.L2 = 91    #lower leg
        self.L3 = 47    #leg joint controller
        self.L4 = 90    #lower leg straight
        self.A = 28     #arm
        self.B = 103    #beam
        self.D = 25     #distance between servos
        self.Dang = 23.6#angle between servos
    
        #points in space for dem pivots
        self.p1 = np.array([0,0])           #SHOULD ALWAYS BE CONSTANT
        self.p2 = np.array([0,0])
        self.p3 = np.array([-10, 23.5])
        self.p4 = np.array([0,0])
        self.p5 = np.array([0,0])
        self.p6 = np.array([0,0])
        
    
    def findP2f(self, angle):
        self.p2[0] = self.L1 * math.cos(math.radians(angle)) + self.p1[0]
        self.p2[1] = self.L1 * math.sin(math.radians(angle)) + self.p1[1]

        return self.p2

    def findP4f(self, angle):
        self.p4[0] = self.A * math.cos(math.radians(angle)) + self.p3[0]
        self.p4[1] = self.A * math.sin(math.radians(angle)) + self.p3[1]

        return self.p4

    def findIntersect(self, p1, p2, r1, r2):
        #literally no chance of me commenting this
        d = np.linalg.norm(p2-p1)
        #print(d)
        a = (r1**2 - r2**2 + d**2) / (2*d)
        #print(a)
        #print(r1,a)
        h = math.sqrt(r1**2 - a**2) 
        P = p1 + ((p2 - p1)*a)/d
        vect1 = np.array([P[0] + h*(p2[1]-p1[1])/d, P[1] - h*(p2[0]-p1[0])/d]) #nope nope nooope
        vect2 = np.array([P[0] - h*(p2[1]-p1[1])/d, P[1] + h*(p2[0]-p1[0])/d])

        return vect1, vect2
    
    def findP2(self):
        vect1, vect2 = self.findIntersect(self.p1, self.p6, self.L1, self.L2)
        if vect1[1] > vect2[1]:
            self.p2 = vect1
            return vect1
        else:
            self.p2 = vect2
            return vect2
    
    def findP1angle(self):
        #print(self.p2)
        angle = math.degrees(math.asin(self.p2[1]/self.L1))
        return angle

    def findP5(self):
        length = np.linalg.norm(self.p6-self.p2)
        dx = (self.p6[0]-self.p2[0])/length
        dy = (self.p6[1]-self.p2[1])/length
        self.p5[0] = self.p2[0] - self.L3 * dx
        self.p5[1] = self.p2[1] - self.L3 * dy

        return self.p5

    def findP4(self):
        print(self.p5)
        vect1, vect2 = self.findIntersect(self.p5, self.p3, self.B, self.A)
        if vect1[1] > vect2[1]:
            self.p4 = vect1
            return vect1
        else:
            self.p4 = vect2
            return vect2
    
    def findP3angle(self):
        angle = math.degrees(math.acos((self.p3[1]-self.p4[1])/self.A))
        return angle
    
    def calculateValues(self):
        self.findP2()
        self.findP5()
        self.findP4()
        return self.p2, self.p5, self.p4

    def setAngles(self, x, y):
        self.p6 = np.array([x, y])
        self.calculateValues()

        hipAngle = self.findP1angle()
        self.joints[1].angle = hipAngle

        kneeAngle = self.findP3angle()
        self.joints[2].angle = kneeAngle

        return hipAngle, kneeAngle

#The Big Boi
class Walker:
    def __init__(self):
        legs = [Leg(i) for i in range(4)]
        self.height = 90
        self.offset = 90


    def update(self):
        for leg in self.legs:
            leg.setAngles(self.offset, self.height)


daddy = Walker()

while True:
    daddy.update()
    if input() == "w":
        daddy.height += 1
    else:
        daddy.height -= 1