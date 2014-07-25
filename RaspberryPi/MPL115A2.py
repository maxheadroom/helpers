#!/usr/bin/env python
# encoding: utf-8
"""
MPL115A2.py

Created by Falko Zurell on 2014-07-25.
Copyright (c) 2014 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import time

from smbus import SMBus


class MPL115A2:
	
	# select the SMBus channel (depends on RaspberryPI model)
	bus = SMBus(0)
	
	# the I2C address of the MPL115A2 sensor
	# default is 0x60
	MPL115A2_ADDRESS = (0x60)
	
	# the register addresses of the MPL115A2 sensor
	MPL115A2_REGISTER_PRESSURE_MSB = (0x00)
	MPL115A2_REGISTER_PRESSURE_LSB = (0x01)
	MPL115A2_REGISTER_TEMP_MSB = (0x02)
	MPL115A2_REGISTER_TEMP_LSB = (0x03)
	MPL115A2_REGISTER_A0_COEFF_MSB = (0x04)
	MPL115A2_REGISTER_A0_COEFF_LSB = (0x05)
	MPL115A2_REGISTER_B1_COEFF_MSB = (0x06)
	MPL115A2_REGISTER_B1_COEFF_LSB = (0x07)
	MPL115A2_REGISTER_B2_COEFF_MSB = (0x08)
	MPL115A2_REGISTER_B2_COEFF_LSB = (0x09)
	MPL115A2_REGISTER_C12_COEFF_MSB = (0x0A)
	MPL115A2_REGISTER_C12_COEFF_LSB = (0x0B)
	MPL115A2_REGISTER_STARTCONVERSION = (0x12)
    
    # some private variables
	a0_MSB = -1;
	a0_LSB = -1;
	b1_MSB = -1;
	b1_LSB = -1;
	b2_MSB = -1;
	b2_LSB = -1;
	c12_MSB = -1;
	c12_LSB = -1;
	 
	_mpl115a2_a0 = -1;
	_mpl115a2_b1 = -1;
	_mpl115a2_b2 = -1;
	_mpl115a2_c12 = -1;

	pressure_MSB = -1
	pressure_LSB = -1
	
	temp_MSB = -1
	temp_LSB = -1
	
	temperature = -1
	pressure = -1
	
	def __init__(self, address=0x60, smbus=0, debug=False):
		global MPL115A2_ADDRESS
		global bus
		self.bus = SMBus(smbus)
		self.MPL115A2_ADDRESS = address
		self.debug = debug
		
		# one time read factory calibrated coefficients from sensor
		# Read the calibration data
		self.readCoefficients()
		pass
	
	# initiate conversion inside the sensor before metrics reading
	def startConvert(self):
		# send conversion command needed for pressure reading
		self.bus.write_i2c_block_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_STARTCONVERSION,[0x12])
		#   
		# sleep until the conversion is certainly completed
		time.sleep(0.3);
		
	def readRawData(self):
		# prepare sensor for reading
		self.startConvert()
		# read pressure AGC units
		self.pressure_MSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_PRESSURE_MSB);
		self.pressure_LSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_PRESSURE_LSB);
		
		# read raw temperature AGC units
		self.temp_MSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_TEMP_MSB+0);
		self.temp_LSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_TEMP_LSB+0);
		
		# build 
		self.temperature = (self.temp_MSB<<8 | self.temp_LSB) >>6;
		self.pressure = (self.pressure_MSB<< 8 | self.pressure_LSB) >>6;

	def readRawTemperatur(self):
		# read raw temperature AGC units
		self.temp_MSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_TEMP_MSB+0);
		self.temp_LSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_TEMP_LSB+0);

		# build 
		self.temperature = (self.temp_MSB<<8 | self.temp_LSB) >>6;

	def readTemperature(self):
		self.readRawTemperature()
		return (self.temperature - 498.0) / -5.35 +25.0; 
		
	def readPressure(self):
		self.readRawData()
		pressureComp = self._mpl115a2_a0 + (self._mpl115a2_b1 + self._mpl115a2_c12 * self.temperature ) * self.pressure + self._mpl115a2_b2 * self.temperature;
		return ((65.0 / 1023.0) * pressureComp) + 50.0; 

	def readBoth(self):
		self.readRawData()
		pressureComp = self._mpl115a2_a0 + (self._mpl115a2_b1 + self._mpl115a2_c12 * self.temperature ) * self.pressure + self._mpl115a2_b2 * self.temperature;
		temp = (self.temperature - 498.0) / -5.35 +25.0; 
		press = ((65.0 / 1023.0) * pressureComp) + 50.0;
		tinydict = {'temperature': temp,'pressure':press}
		return tinydict
		
		
	# read the factory coefficients from the sensor
	def readCoefficients(self):
		
		self.a0_MSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_A0_COEFF_MSB+0);
		self.a0_LSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_A0_COEFF_LSB+0);

		self.b1_MSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_B1_COEFF_MSB+0);
		self.b1_LSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_B1_COEFF_LSB+0);

		self.b2_MSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_B2_COEFF_MSB+0);
		self.b2_LSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_B2_COEFF_LSB+0);
	   
		self.c12_MSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_C12_COEFF_MSB+0);
		self.c12_LSB = self.bus.read_byte_data(self.MPL115A2_ADDRESS,self.MPL115A2_REGISTER_C12_COEFF_LSB+0);
		# unpack to 10bits full scale
		self._mpl115a2_a0 = (float)( (self.a0_MSB<<8) | self.a0_LSB  ) / (2<<3)
		self._mpl115a2_b1 = (float)( (self.b1_MSB<<8) | self.b1_LSB  ) / (2<<13)
		self._mpl115a2_b2 = (float)( (self.b2_MSB<<8) | self.b2_LSB  ) / (2<<14)
		self._mpl115a2_c12 = (float)( (self.c12_MSB<<8) | (self.c12_LSB >>2) ) / (2<<13)


class MPL115A2Tests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	# unittest.main()
	sensor = MPL115A2();
	# print "Temperature: " + str(sensor.readTemperature())
	# print "Pressure: " + str(sensor.readPressure())
	both = sensor.readBoth()
	print "Temperature (Both): " + str(both['temperature'])
	print "Pressure (Both): " + str(both['pressure'])
