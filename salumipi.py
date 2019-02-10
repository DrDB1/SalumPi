import Adafruit_DHT
import time

class TH_Sensor:
	def __init__(self, pin=None):
		units = 'C'
		
		self.pin = pin # 
		self.T  = 0. # [C] Reporting Temperature
		self.Tk = 0. # Temperature in Kelvin
		self.RH = 0. # Relative Humidity
		self.p_air = 101325. # [Pa] Air Pressure 
		self.rho_air = 0. # [kg/m3] Density of Air
		self.pp_h20 = 0. # Partial Pressure of Water 
		
		self.last_reading = 0.
		self.TMIN = -20. # [C] Minimum valid temperature 
		self.TMAX = 50.  # [C] Maximum valid temperature
		self.RHMIN = 0. # [C] Minimum relative humidity 
		self.RHMAX = 110.  # [C] Maximum relative humidity
		self.NMAX = 10 # Max number of reading attempts'
		self.VERBOSE = 0;
		
	def get_data(self):
		VALID = False
		n = 0
		while not VALID and n<self.NMAX:
			RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self.pin)
			if self.VERBOSE: print('%.1f C, %.1f%%RH' % (T, RH))
			
			# test for valid temp RH ranges
			if RH <= self.RHMAX and RH >= self.RHMIN and T >= self.TMIN and T <= self.TMAX:
				VALID = True
				self.T = T
				self.RH = RH
				self.Tk = T+273.15
				if self.VERBOSE: print('Valid Reading')
			else:
				if self.VERBOSE: print('Invalid Reading, Loop %.0f' % n)
			n+=1
			
			
if __name__ == '__main__':
	test = TH_Sensor(20)
	test.VERBOSE = True
	test.get_data()
