import serial
import tkinter as tk

ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM5'
ser.writeTimeout = 0
ser.open()


class Servo(tk.Frame):
    def __init__(self, master, identity):
        self.master = master
        self.identity = identity
        self.val = 90

        tk.Frame.__init__(self, self.master)

        self.configureView()
        self.createWidgets()

    def configureView(self):
        self.master.geometry("100x100")
        pass
        
    def createWidgets(self):
        self.label = tk.Label(self.master, text='Servo {}'.format(self.identity + 1))
        self.label.grid(row = 0, column = self.identity * 2, columnspan = 2)
        self.scale = tk.Scale(self.master, from_=0, to=180, orient='horizontal', command = self.getScaleValue, tickinterval = 90, length = 100)
        self.scale.grid(row = 1, column = self.identity * 2, columnspan = 2)
        self.scale.set(self.val)
        self.entry = tk.Entry(self.master, width = 3)
        self.entry.grid(row = 2, column = self.identity * 2)
        self.button = tk.Button(self.master, text = 'Set', width = 5, command = self.setValue)
        self.button.grid(row = 2, column = self.identity * 2 + 1)

    def setValue(self):
        value = self.entry.get()
        if value != "":
            self.scale.set(value)

    def getScaleValue(self, val):
        self.val = val
        self.changeValue()

    def changeValue(self):
        command = str(self.identity) + "" + str(self.val) + "X"
        #print(command)
        ser.write(command.encode())

    
            
        

class App(tk.Frame):
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.entries = {}
        self.buttons = {}
        self.servos = {}

        self.step = 2;
        
        self.configureView()
        self.createWidgets()

    def configureView(self):
        self.master.title("Arduino Controller")
        self.master.geometry("500x500")

    def createWidgets(self):
        for i in range(8):
            servo = Servo(self.master, i)
            self.servos[i] = servo

        for i in range(6):
            self.entries[i] = tk.Entry(self.master, width = 2)
            self.entries[i].grid(row = 4, column = i * 2)
            self.buttons[i] = tk.Button(self.master, text = 'Set servos', command = lambda i = i: self.setServos(i))
            self.buttons[i].grid(row = 4, column = i * 2 + 1)

        walk = tk.Button(self.master, command = self.step)
        walk.grid(row = 5, column = 0)
                    

    def setServos(self, n):
        val = self.entries[n].get()
        if n < 2:
            for i in range(n * 4, n * 4 + 4):

                self.servos[i].getScaleValue(val)
        elif n == 2:
            for i in range(0, 4, 2):
                self.servos[i].getScaleValue(val)
        elif n == 3:
            for i in range(1, 4, 2):
                self.servos[i].getScaleValue(val)
        elif n == 4:
            for i in range(4, 8, 2):
                self.servos[i].getScaleValue(val)
        elif n == 5:
            for i in range(5, 8, 2):
                self.servos[i].getScaleValue(val)

    def lerpRotate(self, leg, angleStart, angleEnd, progress=0):
        if progress >= 1:
            return True

        progress += 0.02
        difference = angleEnd - angleStart if angleEnd > angleStart else angleStart - angleEnd
            
        baseServo = self.servos[leg - 1]

        baseServo.getScaleValue(angleStart + (difference * progress))
        
        self.master.after(2, lambda: self.lerpRotate(leg, angleStart, angleEnd, progress))

    def step(self):
        baseServo = self.servos[0]
        jointServo = self.servos[5]

        baseServo.getScaleValue(150)

        self.master.after(500, lambda: jointServo.getScaleValue(90))

if __name__ == '__main__':
   root = tk.Tk()
   main_app =  App(root)
   root.geometry("850x150")
   root.mainloop()

ser.close()
print('Done')
