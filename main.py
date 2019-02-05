
import RPi.GPIO as GPIO
import Adafruit_DHT
import requests
import time

# Program Settings
UPLOAD = True
PRINTOUT = True
LOOPTIME = 30
DEBUG = True
CONTROL = False

Tset = 15.0
Tband = 1.0

Hset = 70.0 
Hband = 5.0
    
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

t0 = time.time()

def setup():
    #set up GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Setup GPIO Pins
    GPIO.setup(humidifier, GPIO.OUT)
    GPIO.setup(heater, GPIO.OUT)
    GPIO.setup(freezer, GPIO.OUT)

def loop():
    heat_status = 0
    RUN=True
    while RUN:
        ts = time.time()
        # Get Sensor Readings
        valid = False
        amb_relhum, amb_temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, ambient_sensor)
        cbm_relhum, cbm_temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, chamber_sensor)

        # Confirm valid readings
        if cbm_temp > -10. and cbm_temp < 50:
            valid = True

        # Only run control if temp is valid
        if valid and CONTROL:
            if DEBUG: print('Valid Temp')
            if cbm_temp < Tset-Tband:
                heat_status = 1
                if DEBUG: print('Turning Heater On')
            if heat_status and cbm_temp > Tset:
                heat_status = 0
                if DEBUG: print('Turning Heater Off')

            if heat_status:
                GPIO.output(heater, GPIO.HIGH)
            else:
                GPIO.output(heater, GPIO.LOW)
                

        
        GPIO.output(freezer, GPIO.LOW)
        cool_status = 0
        
        fan_status = 0


        

        if UPLOAD:
            thingspeak_key = 'H3HJYAGBW2M3DDEX'
            r = requests.post('https://api.thingspeak.com/update.json', 
                data = {'api_key':thingspeak_key, 
                'field1':cbm_temp, 
                'field2':cbm_relhum,
                'field3':amb_temp,
                'field4':amb_relhum,
                'field5':cool_status,
                'field6':heat_status,
                'field7':humidifier_status,
                'field8':fan_status
                })

        if PRINTOUT:
            # Print Sensor Readings
            print(' ---------t= %.0f --------------' % (time.time()-t0))
            print('              Temp    RelHum')
            print('           --------  --------')
            print('  Ambient     %4.1f     %4.2f' % (amb_temp, amb_relhum))
            print('  Chamber     %4.1f     %4.2f' % (cbm_temp, cbm_relhum))
            print(' ')
            print('  Heater: %.0f' % heat_status)
            print('  Cooler: %.0f' % cool_status)
            print(' ')
            print('  Looptime : %.1f seconds' % (time.time()-ts))

        if time.time()-ts < LOOPTIME:
            time.sleep( LOOPTIME - ((time.time()-t0) % LOOPTIME))

def destroy():
    GPIO.output(humidifier, GPIO.LOW)
    GPIO.output(heater, GPIO.LOW)
    GPIO.output(freezer, GPIO.LOW)
    GPIO.cleanup()                     # Release resource
    
if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
