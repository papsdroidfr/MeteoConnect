from machine import Timer
from time import sleep
from lcd import LCD
from api_meteo import Meteo
from dht22 import Sensor
from sys import exit

INSEE = '78015'          # country insee code at https://public.opendatasoft.com/explore/dataset/correspondance-code-insee-code-postal/table/
PERIOD_METEOEXT = 5*60*1000   # period to get external meteo in ms: every 5mn
PERIOD_METEOINT = 5*1000      # period to get internal meteo in ms: every 5s

class Application:
    def __init__(self):
        ''' contructor'''
        print('démarrage application meteoConnect')
        
        #initiailze screen
        self.screen = LCD()
        self.screen.putstr('IN' +'\n' +'EX')
        
        #initialise DHT22 sensor
        self.sensor = Sensor() #default pin sensor = 3
        
        #initialize external meteo
        print('Connection en cours API météo ...')
        self.meteo = Meteo(insee=INSEE)
        self.h, self.buletin, self.temp, self.hum, self.probarain, self.wind = None, None, None, None, None, None
        self.tempIn, self.humIn = self.get_meteo_int()
        status = self.get_meteo_ext()
        if (status == 200): #connection is ok
            print('connection OK !')
        else :
            print("Echec de connection à l'API météo")    
                        
        #timers
        self.tim_meteo_ext = Timer(0)  # timer to get external meteo perdiodically
        self.tim_meteo_int = Timer(2)  # timer to get internal meteo periodically
        
        #start timers
        self.tim_meteo_ext.init(period=PERIOD_METEOEXT, mode=Timer.PERIODIC, callback=self.__callback_meteo_ext)
        self.tim_meteo_int.init(period=PERIOD_METEOINT, mode=Timer.PERIODIC, callback=self.__callback_meteo_int)
    
    def get_meteo_int(self) ->(int,int) :
        ''' get temp °C + hum % from sensor '''
        return self.sensor.get_data()
    
    def __callback_meteo_int(self, _t) ->None : 
        ''' callback method assiociated with timer self.tim_meteo_int '''
        self.tempIn, self.humIn = self.get_meteo_int()
        #print('capteur DHT22:', self.tempIn, '°C', self.humIn, '%')
        
    def get_meteo_ext(self)->int :
        ''' get foreacast from api meteo, return status '''
        status = self.meteo.get_forecast()   # forecast meteo
        if (status == 200) :                 # API return code 200 =  ok
            self.h, self.buletin, self.temp, self.hum, self.probarain, self.wind = self.meteo.decode_detail_meteo(id_forecast=0)
            #print('prévision météo', self.h, 'à', self.meteo.city, ':', self.buletin, ',',
            #      self.temp, '°C, humidité', self.hum,'%, proba pluie',self.probarain,'% , vent moyen', self.wind,'km/h' )
        return status
        
    def __callback_meteo_ext(self, _t) ->None :   #The callback must take one argument, which is passed the Timer object
        ''' callback method assiociated with timer self.tim_meteo_ext '''
        self.get_meteo_ext()
    
    def loop(self):
        ''' event loop application'''
        while True:
            #internal meteo data
            if self.tempIn is not None:
                self.screen.move_to(cursor_x=3,cursor_y=0)
                self.screen.putstr(self.screen.get_char('thermometre')+ '{:0>4.1f}'.format(self.tempIn) +chr(7)) #logo thermometre + temp xx.x + °C
                self.screen.putstr('  '+'{:0>4.1f}'.format(self.humIn)+'%') #humidity %
            else:
                self.screen.move_to(cursor_x=3,cursor_y=0)
                self.screen.putstr(self.screen.get_char('wifi') + ' connect...') #logo wifi + message connection API en cours
            #ext meteo data
            if self.temp is None:
                #data not ready: connection still in progress
                self.screen.move_to(cursor_x=3,cursor_y=1)
                self.screen.putstr(self.screen.get_char('wifi') + ' connect...') #logo wifi + message connection API en cours
                sleep(5)
            else:
                #screen1: temp + humidity
                self.screen.move_to(cursor_x=3,cursor_y=1)
                self.screen.putstr(self.screen.get_char('thermometre')+ '{:0>4.1f}'.format(self.temp) +chr(7)) #logo thermometre + temp xx.x + °C
                if (self.temp>-10):
                    self.screen.putstr('  ')
                else:
                    self.screen.putstr(' ')
                self.screen.putstr('{:0>4.1f}'.format(self.hum)+'%') #humidity %
                sleep(3)
                #screen2: wind + rain proba
                self.screen.move_to(cursor_x=3,cursor_y=1)
                self.screen.putstr(self.screen.get_char('pluie')+ '{:0>3.0f}'.format(self.wind) +'km/h') #logo pluie + wind xxxkm/h
                self.screen.putstr(' '+'{:0>3.0f}'.format(self.probarain)+'%') #proba rain xxx%
                sleep(3)
                #screen3: buletin scroll
                self.screen.move_to(cursor_x=3,cursor_y=1)
                l = [e.lower() for e in self.buletin.split()] # list of words in lower case
                if ('soleil' in l):
                    c = self.screen.get_char('soleil')
                elif ('nuageux' in l) or ('couvert' in l) or ('voile' in l):
                    c = self.screen.get_char('nuages')
                elif ('brouillard' in l):
                    c = self.screen.get_char('brouillard')
                elif ('neige' in l):
                    c = self.screen.get_char('neige')
                else:
                    c = self.screen.get_char('pluie')                  
                self.screen.putstr(c)
                self.screen.scroll(self.buletin, lig=1, col=4)             
    
    def destroy(self):
        """end of application"""
        # stop timers
        self.tim_meteo_ext.deinit() 
        self.tim_meteo_int.deinit()
        print('Bye!')     
            
if __name__ == '__main__':
    appl=Application()
    try:
        appl.loop()
    except KeyboardInterrupt:  # interruption clavier CTRL-C: appel à la méthode destroy() de appl.
        appl.destroy()         


