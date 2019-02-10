
import RPi.GPIO as GPIO
import Adafruit_DHT
import requests
import time
import salumipi


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

ambient = salumipi.TH_Sensor(21)
chamber = salumipi.TH_Sensor(20)

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
        ambient.get_data()
	chamber.get_data()

        # Only run control if temp is valid
        if CONTROL:
            if DEBUG: print('Valid Temp')
            if chamber.T < Tset-Tband:
                heat_status = 1
                if DEBUG: print('Turning Heater On')
            if heat_status and chamber.T > Tset:
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
                'field1':chamber.T, 
                'field2':chamber.RH,
                'field3':ambient.T,
                'field4':ambient.RH,
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
            print('  Ambient     %4.1f     %4.2f' % (ambient.T, ambient.RH))
            print('  Chamber     %4.1f     %4.2f' % (chamber.T, chamber.RH))
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
