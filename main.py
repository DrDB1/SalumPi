
import RPi.GPIO as GPIO
import Adafruit_DHT
import requests
import time
import salumipi
import numpy as np

from simple_pid import PID

from settings import *

ambient = salumipi.TH_Sensor(21)
chamber = salumipi.TH_Sensor(20)

# PID setup
heat_pid = PID(Heat_Kp, Heat_Ki, Heat_Kp, setpoint=Tset)

t0 = time.time()
def setup():
    #set up GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Setup GPIO Pins
    GPIO.setup(humid,  GPIO.OUT)
    GPIO.setup(heater, GPIO.OUT)
    GPIO.setup(cooler, GPIO.OUT)

def loop():

    humidifier_status = 0
    heat = 0
    cool = 0
    fan_status = 0
        
    while True:
        ts = time.time()

        # Update settings
        
        # Get Sensor Readings
        ambient.get_data()
	chamber.get_data()

        if chamber.T > 35.0 or chamber.T < 0.0:
            destroy();
            break

	# Set heat time
	if Tset > ambient.T:
            heat_pid.setpoint = Tset
            heat_pid.tunings = (Heat_Kp, Heat_Ki, Heat_Kp)
            heat_pid.output_limits = (0, Heat_max)	
            heat = heat_pid(chamber.T)
        else:
            heat = 0    

        # Only run control if temp is valid
        if CONTROL:
            GPIO.output(heater, GPIO.HIGH)
            time.sleep(heat)
            
        GPIO.output(heater, GPIO.LOW)

        buffer = 1
        if chamber.T > Tset+buffer:
            cool = 1
            GPIO.output(cooler, GPIO.HIGH)

        if cool and chamber.T < Tset-buffer:
            cool = 0;
            GPIO.output(cooler, GPIO.LOW)
        
        fan_status = 0

        if UPLOAD:
            r = requests.post('https://api.thingspeak.com/update.json', 
                data = {'api_key':thingspeak_key, 
                'field1':chamber.T, 
                'field2':chamber.RH,
                'field3':ambient.T,
                'field4':ambient.RH,
                'field5':cool,
                'field6':heat,
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
            print('  Heater: %.2f' % heat)
            print('  Cooler: %.2f' % cool)
            print(' ')
            print('  Looptime : %.1f seconds' % (time.time()-ts))

        if time.time()-ts < LOOPTIME:
            time.sleep( LOOPTIME - ((time.time()-t0) % LOOPTIME))

def destroy():
    GPIO.output(humid, GPIO.LOW)
    GPIO.output(heater, GPIO.LOW)
    GPIO.output(cooler, GPIO.LOW)
    GPIO.cleanup()                     # Release resource
    
if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
