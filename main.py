
import RPi.GPIO as GPIO
import Adafruit_DHT

#set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# RPi Pin numbers
humidifier = 18
heater = 23
freezer = 24
ambient_sensor = 20
chamber_sensor = 21


GPIO.setup(humidifier, GPIO.OUT)
GPIO.setup(heater, GPIO.OUT)
GPIO.setup(freezer, GPIO.OUT)

chamber_sen = Adafruit_DHT.DHT22
ambient_sen = Adafruit_DHT.DHT22

RUN = true


# Get Sensor Readings
amb_relhum, amb_temp = Adafruit_DHT.read_retry(ambient_sensor, ambient_pin)
cbm_relhum, cbm_temp = Adafruit_DHT.read_retry(chamber_sensor, chamber_pin)

# Print Sensor Readings
print('              Temp    RelHum\n'
print('           --------  --------\n'
print(' Ambient    %4.1f     %4.2f' % (amb_temp, amb_relhum))
print(' Chamber    %4.1f     %4.2f' % (cbm_temp, cbm_relhum))
	
