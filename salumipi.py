import Adafruit_DHT
import time
import numpy as np
import RPi.GPIO as GPIO


class Chamber:
	def __init__(self):
		self.R = 287.058 # J/kg-K
		self.cp_air = 1.005 # kJ/kg-K
		self.cp_h20 = 1.996 # kJ/kg-K
		# Chamber Properties
		
		self.V = 0.4 # m3 Chamber Volume
		self.A = 3.6 # m2 Chamber Area
		self.t = .05 # m  Chamber insulation thickness
		self.k = 0.026 # [W/m-K] Chamber insulation conductivity
		
		# Air Properties
		self.T = None # Temperature in K
		self.RH = None # Relative Humidity
		self.p = 101325. # [Pa] Standard Pressure
		self.Q = None # [kJ] Thermal Energy 
		
		self.rho_air = 0. # [kg/m3] Density of Air
		self.rho_h20 = 0. # Water vapor density
		
		self.p_sat = 0. # Saturation Pressure of Water
		self.rho_sat = 0. # Saturation Water vapor density
		self.m_air = 0. # mass of air
		self.m_h20 = 0. # mass of water
	
	def update(self,T,RH):
		# Air Conditions
		self.T = T+273.15
		self.rho_air = self.p/(self.R*self.T)
		
		# Water Conditions
		self.RH = RH/100.
		self.p_sat = np.exp(77.3450 + 0.0057*self.T - 7235/self.T) / (self.T**8.2) 
		self.rho_sat = 0.0022 * self.p_sat / self.T
		self.rho_h20 = self.RH*self.rho_sat
		
		self.m_air = self.rho_air*self.V
		self.m_h20 = self.rho_h20*self.V
		
		# Energy
		self.Q = self.cp_air * self.m_air * self.T + self.cp_h20 * self.m_h20 * self.T
		
class Heater:
	def __init__(self, pin=None):
		self.pin = pin 
		self.P = None # Heater Power in Watts


class TH_Sensor:
	def __init__(self, pin=None):		
		self.pin = pin # 
		self.T  = 0. # [C] Reporting Temperature		
		self.RH = 0. # Relative Humidity
		
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
				self.last_reading = time.time()
				if self.VERBOSE: print('Valid Reading')
			else:
				if self.VERBOSE: print('Invalid Reading, Loop %.0f' % n)
			n+=1
			
if __name__ == '__main__':
	ref = Chamber()
	test = Chamber()

	ref.update(15,50)
	test.update(14,50)

	print(ref.Q)
	print(test.Q)
	print((ref.Q-test.Q)/0.0185)
