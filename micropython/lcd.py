from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
from sys import exit

I2C_ADDR = 0x27
SDA_PIN = 0
SCL_PIN = 1
TOTAL_ROWS = 2
TOTAL_COLUMNS = 16

class LCD(I2cLcd):
    def __init__(self, sda_pin:int=SDA_PIN, scl_pin:int=SCL_PIN):
        """ constructor """
        self.i2c = self.get_i2c(sda_pin, scl_pin)
        if self.i2c is not None:
            I2cLcd.__init__(self, self.i2c, I2C_ADDR, TOTAL_ROWS, TOTAL_COLUMNS)
            self.clear()
            
            # generator custom character: https://maxpromer.github.io/LCD-Character-Creator/        
            self.dic_char={'wifi'       : (0, bytearray([0x0E, 0x11, 0x00, 0x1F, 0x00, 0x0E, 0x00, 0x04]) ),
                           'thermometre': (1, bytearray([0x04, 0x0B, 0x0A, 0x0B, 0x0A, 0x17, 0x1F, 0x0E]) ), 
                           'soleil'     : (2, bytearray([0x00, 0x15, 0x0E, 0x11, 0x11, 0x11, 0x0E, 0x15]) ),
                           'pluie'      : (3, bytearray([0x15, 0x00, 0x0E, 0x1F, 0x04, 0x04, 0x14, 0x08]) ),
                           'nuages'     : (4, bytearray([0x03, 0x0F, 0x1E, 0x1E, 0x0C, 0x00, 0x00, 0x00]) ),
                           'neige'      : (5, bytearray([0x10, 0x05, 0x02, 0x05, 0x00, 0x14, 0x08, 0x14]) ),
                           'brouillard' : (6, bytearray([0x0E, 0x1F, 0x0A, 0x15, 0x0A, 0x15, 0x0A, 0x15]) ),
                           'C'          : (7, bytearray([0x08, 0x14, 0x08, 0x03, 0x04, 0x04, 0x04, 0x03]) ),
                           #'papsdroid'  : (7, bytearray([0x0E, 0x1F, 0x15, 0x1F, 0x1F, 0x11, 0x1F, 0x0E]) ),
                           }
            for __cle, val in self.dic_char.items():
                self.custom_char(val[0], val[1])
            
        else:
            print('Revoir branchements écran LCD')
            exit(1)
          
    def get_char(self, name:str) ->chr :
        ''' return chr of named special char '''
        try:
            c = chr(self.dic_char[name][0])
        except:
            c =  chr(0)
        return c
    
    def scroll(self, s:str, lig:int, col:int):
        """ scroll string s rigth to left at (lig, col) """
        padding = ' ' * (16-col)
        padded_s = padding + s
        for i in range(len(padded_s)):
            lcd_text = padded_s[i:(i+16-col)]
            self.move_to(col,lig)
            self.putstr(lcd_text)
            sleep(0.3)
            self.move_to(col,lig)
            self.putstr(padding)
    
    def get_i2c(self, sda_pin:int, scl_pin:int) ->SoftI2C :
        ''' get i2c '''
        i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)
        devices =i2c.scan()      
        if len(devices) == 0:
             print("No i2c device !")
             return None
        else:
            print('i2c devices found:',len(devices))
            for device in devices:
                print("At address: ",hex(device))
            return i2c
        
if __name__ == '__main__':
    print('test lcd')            
    screen=LCD()
    screen.putstr(screen.get_char('papsdroid') + "  papsdroid  " + screen.get_char('papsdroid'))
    screen.move_to(0,1) #second line
    #print symbols
    screen.putstr(' '+screen.get_char('wifi'))
    screen.putstr(' '+screen.get_char('thermometre'))
    screen.putstr(' '+screen.get_char('soleil'))
    screen.putstr(' '+screen.get_char('nuages'))
    screen.putstr(' '+screen.get_char('pluie'))
    screen.putstr(' '+screen.get_char('neige'))
    screen.putstr(' '+screen.get_char('brouillard'))
    sleep(1)
    screen.scroll('https://papsdroidfr.github.io/', lig=0, col=2)
    screen.move_to(0,0)
    screen.putstr(screen.get_char('papsdroid') + "  papsdroid  " + screen.get_char('papsdroid'))
    

