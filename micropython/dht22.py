from machine import Pin
from time import sleep
from dht import DHT22 

PIN_SENSOR = 3 # pin sensor relié au DHT22
QUALIBRATION = True #True: T = Tdht #False: T = r*Tdht + T0
T_DHT1 = 21.7 # mesure 1 temp DHT22
T_R1   = 20.2 # mesure 1 temp thermometre de référence
T_DHT2 = 14.5 # mesure 2 temp DHT22
T_R2   = 14.0 # mesure 2 temp thermometre de référence

if QUALIBRATION:
    R = (T_R2 - T_R1)/(T_DHT2 - T_DHT1)
    T0 = T_R2 - R*T_DHT2
else:
    R  = 1
    T0 = 0

class Sensor():
    ''' DHT22 sensor class'''
    def __init__(self, pin:int=PIN_SENSOR):
        ''' constructor '''
        self.__sensor = DHT22(Pin(pin))
    
    def get_data(self) -> (int, int) :
        ''' get temp and humidity'''
        try:
            self.__sensor.measure()
            return( R*self.__sensor.temperature()+T0, self.__sensor.humidity() )
        except OSError as e:
            print('Failed to read sensor.')
            return (None, None)
        
if __name__ == "__main__":
    sensor = Sensor()
    while True:
        temp, hum = sensor.get_data()
        if (temp is not None):
            print('Température: {}°C, humidié: {}%'.format(temp, hum) )
        sleep(2)

