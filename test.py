
import RPi.GPIO as GPIO
import Adafruit_DHT
import requests

#set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# RPi Pin numbers
humidifier = 18
heater = 23
freezer = 24
fan = 0
ambient_sensor = 21
chamber_sensor = 20

humidifier_status = 0
heat_status = 0
cool_status = 0
fan_status = 0

# Setup GPIO Pins
GPIO.setup(humidifier, GPIO.OUT)
GPIO.setup(heater, GPIO.OUT)
GPIO.setup(freezer, GPIO.OUT)

# Get Sensor Readings
amb_relhum, amb_temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, ambient_sensor)
cbm_relhum, cbm_temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, chamber_sensor)

thingspeak_key = 'H3HJYAGBW2M3DDEX'
'''
#r = requests.post('https://api.thingspeak.com/update.json', 
#	data = {'api_key':thingspeak_key, 
#	'field1':cbm_temp, 
#	'field2':cbm_relhum,
#	'field3':amb_temp,
#	'field4':amb_relhum,
#	'field5':cool_status,
#	'field6':heat_status,
	'field7':humidifier_status,
	'field8':fan_status
	})
'''

def checkval(inp):
    if inp:
        return inp
    return -999

# Print Sensor Readings
print('              Temp    RelHum')
print('           --------  --------')
print('  Ambient     %4.1f     %4.2f' % (checkval(amb_temp), checkval(amb_relhum)))
print('  Chamber     %4.1f     %4.2f' % (checkval(cbm_temp), checkval(cbm_relhum)))
	
GPIO.cleanup()
