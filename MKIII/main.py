from walker import Walker 
import remi.gui as gui
from remi import start, App

class application(App):
    def __init__(self, *args):
        super(application, self).__init__(*args)

        self.walker = Walker()
    
    def main(self):
        container = gui.VBox(width=250, height=800)
        self.servos = [Slider(i) for i in range(12)]
        for slider in self.servos:
            container.append(slider.container)
        # returning the root widget
        return container

    # listener function
    def on_button_pressed(self, widget):
        self.lbl.set_text('Button pressed!')
        self.bt.set_text('Hi!')
    
    def slider_changed(self, widget, value):
        self.lbl.set_text(str(value))

class Slider:
    def __init__(self, identity):
        self.id = identity
        self.container = gui.VBox(width=200, height=50)
        self.value = 90
        self.lbl = gui.Label("Servo " + str(self.id+1) + ":  " + str(self.value), width=80, height=20) 
        self.slider = gui.Slider(self.value, 0, 180, 2, width=200, height=20)
        self.slider.onchange.do(self.slider_changed)

        self.container.append(self.lbl)
        self.container.append(self.slider)

    def slider_changed(self, widget, value):
        self.lbl.set_text("Servo " + str(self.id+1) + ":  " + str(value))
        self.value = value
        self.walker.servos[self.id].update(value)
    
    def getComponent(self):
        return self.container
    
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
    
# starts the web server
start(application)