from machine import Pin
import time
from apa106 import APA106

class RGB_led:
    def __init__(self):
        ''' constructeur '''
        self.on = False #on/off status
        self.rgb_led = Pin(8, Pin.OUT)
        self.ap = APA106(self.rgb_led, 1)
        self.off()
        
    def off(self):
        ''' off led '''
        self.ap[0] = (0, 0, 0) # set the led to RGB
        self.ap.write()
        self.on = False
        
    def color(self, rgb=(64,64,64)):
        ''' switch on led to color rgb '''
        self.ap[0] = rgb # set the led to RGB
        self.ap.write()
        self.on = True
        
    def blink(self, rgb=(64,64,64)):
        ''' switch on/off led to color rgb/off '''
        if self.on:
            self.off()
        else:
            self.ap[0] = rgb # set the led to RGB
            self.on = True
        self.ap.write()
