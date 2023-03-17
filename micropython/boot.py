############################
# Connexion Wifi
############################
WIFI_SSID = 'xxxxx'
WIFI_PASSWORD = 'xxxxxxxxxxxxxxxxxxx'

MAX_ITERATION = 20

import time, network
from RGBLed import RGB_led

#RGB led setup
led = RGB_led()
led.color((0,0,64)) #blue color

#wifi setup
station = network.WLAN(network.STA_IF)
station.active(True)

print("Scanning for WiFi networks, please wait...")
authmodes = ['Open', 'WEP', 'WPA-PSK' 'WPA2-PSK4', 'WPA/WPA2-PSK']
for (ssid, bssid, channel, RSSI, authmode, hidden) in station.scan():
  print("* {:s}".format(ssid))

#try to connect to WiFi
nb_iteration=0
while not station.isconnected():
    # Try to connect to WiFi access point
    print("Connecting...")
    try:
        station.connect(WIFI_SSID, WIFI_PASSWORD)
    except:
        pass
    nb_iteration+=1
    if (nb_iteration==MAX_ITERATION):
        break
    time.sleep(0.5)
    led.blink((0,0,64))

led.color((0,0,64)) #blue color

# Display connection details
if station.isconnected():
    print("Connected!")
    print("My IP Address:", station.ifconfig()[0])
    led.color((64,0,0)) #green color
else:
    print("connection to wifi failed!")
    led.color((0,54,0)) #red color



