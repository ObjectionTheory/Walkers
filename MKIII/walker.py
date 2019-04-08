from servo import Servo
import math
import numpy as np

#the small boi
class Leg:
    def __init__(self, identity):
        self.id = identity

        #make sum servos
        self.joints = [Servo(i*4+self.id) for i in range(3)]
        self.joints[0].angle = 90
        self.joints[1].angle = 90
        self.joints[2].angle = 90

        

        #set servos to base position
        for servo in self.joints:
            servo.update(servo.angle)

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
        # print(d)
        a = (r1**2 - r2**2 + d**2) / (2*d)
        #print(a)
        #print(r1,a)
        h = math.sqrt(r1**2 - a**2) 
        P = p1 + a*(p2 - p1)/d
        vect1 = np.array([P[0] + h*(p2[1]-p1[1])/d, P[1] - h*(p2[0]-p1[0])/d]) #nope nope nooope
        vect2 = np.array([P[0] - h*(p2[1]-p1[1])/d, P[1] + h*(p2[0]-p1[0])/d])

        return vect1, vect2
    
    def findP2(self):
        vect1, vect2 = self.findIntersect(self.p1, self.p6, self.L1, self.L4)
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
        length = self.L4
        # print(length)
        dx = (self.p6[0]-self.p2[0])/length
        dy = (self.p6[1]-self.p2[1])/length
        self.p5[0] = self.p2[0] - self.L3 * dx
        self.p5[1] = self.p2[1] - self.L3 * dy

        return self.p5

    def findP4(self):
        vect1, vect2 = self.findIntersect(self.p5, self.p3, self.B, self.A)
        if vect1[1] > vect2[1]:
            self.p4 = vect1
            return vect1
        else:
            self.p4 = vect2
            return vect2
    
    def findP3angle(self):
        angle = math.degrees(math.acos((self.p4[1]-self.p3[1])/self.A))
        return angle
    
    def calculateValues(self):
        self.findP2()
        self.findP5()
        self.findP4()
        return self.p2, self.p5, self.p4

    def findAngles(self, x, y):
        self.p6 = np.array([x, y])
        self.calculateValues()

        hipAngle = self.findP1angle()
        kneeAngle = self.findP3angle()
        if self.id % 2 == 0:
            hipAngle = 180 - hipAngle
            kneeAngle = 180 - kneeAngle

        self.joints[1].angle = hipAngle
        self.joints[2].angle = kneeAngle

        return hipAngle, kneeAngle
    
            

#The Big Boi
class Walker:
    def __init__(self):
        self.legs = [Leg(i) for i in range(4)]
        self.servos = self.legs[0].joints + self.legs[1].joints + self.legs[2].joints + self.legs[3].joints 
        self.height = 90
        self.offset = 90
        self.servoOffsets = [-10, -14, 10,
                             -34, -18, 0,
                             -6, -14, -14,
                             -28, -12, -2]

        for servo in range(12):
            self.servos[servo].offset = self.servoOffsets[servo]

    def update(self):
        for leg in self.legs:
            leg.findAngles(self.offset, -self.height)

    def lift(self):
        self.height += 1
        self.update()
    
    def lower(self):
        self.height -= 1
        self.update()
    
    def setHeight(self, height):
        self.height = height
        self.update()
    
    
    
        
