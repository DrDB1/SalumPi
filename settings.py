# Program Settings
LOOPTIME = 30
UPLOAD = True
PRINTOUT = True
DEBUG = True
CONTROL = True
thingspeak_key = 'H3HJYAGBW2M3DDEX'

# Setpoints
Tset = 12.5 # C
Hset = 70.0 # %

# Heater Control
Heat_Kp  = 2.  
Heat_Ki  = .001
Heat_Kd  = .00
Heat_max = 10. # Limit max heater value X sec/loop

# Pinout
heater = 23
cooler = 24
fan    = 0
humid  = 18
