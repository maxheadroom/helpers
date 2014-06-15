#!/usr/bin/python
# -*- coding: utf-8 -*-
# radio.py, version 3.4 (RGB LCD Pi Plate version)
# September 14.3, 2013
# Edited by Dylan Leite
# Written by Sheldon Hartling for Usual Panic
# BSD license, all text above must be included in any redistribution
#

#
# based on code from Kyle Prier (http://wwww.youtube.com/meistervision)
# and AdaFruit Industries (https://www.adafruit.com)
# Kyle Prier - https://www.dropbox.com/s/w2y8xx7t6gkq8yz/radio.py
# AdaFruit   - https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git, Adafruit_CharLCDPlate
#

#dependancies
from Adafruit_I2C          import Adafruit_I2C
from Adafruit_MCP230xx     import Adafruit_MCP230XX
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from datetime              import datetime
from subprocess            import *
from time                  import sleep, strftime
from Queue                 import Queue
from threading             import Thread

import smbus
import os
import time
import subprocess


#standard python libs
import logging
import time

#third party libs
from daemon import runner

class DisplayIPAddressDaemon:
	# initialize the LCD plate
	#   use busnum = 0 for raspi version 1 (256MB)
	#   and busnum = 1 for raspi version 2 (512MB)
	LCD = ""
#	lcd = ""

	# Define a queue to communicate with worker thread
	LCD_QUEUE = ""

	# Globals
	astring = ""
	setscroll = ""

	# Buttons
	NONE           = 0x00
	SELECT         = 0x01
	RIGHT          = 0x02
	DOWN           = 0x04
	UP             = 0x08
	LEFT           = 0x10
	UP_AND_DOWN    = 0x0C
	LEFT_AND_RIGHT = 0x12

	def __init__(self):
		self.LCD = Adafruit_CharLCDPlate(busnum = 0)
#		self.lcd = Adafruit_CharLCDPlate()
		self.LCD_QUEUE = Queue()
		
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/tty'
		self.stderr_path = '/dev/tty'
		self.pidfile_path =  '/var/run/testdaemon.pid'
		self.pidfile_timeout = 5

	# ----------------------------
	# WORKER THREAD
	# ----------------------------

	# Define a function to run in the worker thread
	def update_lcd(self,q):
   
	   while True:
	      msg = q.get()
	      # if we're falling behind, skip some LCD updates
	      while not q.empty():
	        q.task_done()
	        msg = q.get()
	      self.LCD.setCursor(0,0)
	      self.LCD.message(msg)
	      q.task_done()
	   return



	# ----------------------------
	# MAIN LOOP
	# ----------------------------

	def run(self):

	   global astring, setscroll

	   # Setup AdaFruit LCD Plate
	   self.LCD.begin(16,2)
	   self.LCD.clear()
	   self.LCD.backlight(self.LCD.ON)

	   # Create the worker thread and make it a daemon
	   worker = Thread(target=self.update_lcd, args=(self.LCD_QUEUE,))
	   worker.setDaemon(True)
	   worker.start()
	
	   self.display_ipaddr()

	def delay_milliseconds(self, milliseconds):
	   seconds = milliseconds / float(1000)   # divide milliseconds by 1000 for seconds
	   sleep(seconds)

	# ----------------------------
	# DISPLAY TIME AND IP ADDRESS
	# ----------------------------

	def display_ipaddr(self):
	   show_eth0 = "ip addr show eth0  | cut -d/ -f1 | awk '/inet/ {printf \"e%15.15s\", $2}'"
	   ipaddr = self.run_cmd(show_eth0)

	   self.LCD.backlight(self.LCD.ON)
	   i = 29
	   muting = False
	   keep_looping = True
	   while (keep_looping):

	      # Every 1/2 second, update the time display
	      i += 1
	      #if(i % 10 == 0):
	      if(i % 5 == 0):
	         self.LCD_QUEUE.put(datetime.now().strftime('%b %d  %H:%M:%S\n')+ ipaddr, True)

	      # Every 3 seconds, update ethernet or wi-fi IP address
	      if(i == 60):
	         ipaddr = self.run_cmd(show_eth0)
	         i = 0

	      self.delay_milliseconds(99)

	# ----------------------------

	def run_cmd(self,cmd):
	   p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
	   output = p.communicate()[0]
	   return output


app = DisplayIPAddressDaemon()
logger = logging.getLogger("DisplayIPAddressDaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()


if __name__ == "__main__":
	app = DisplayIPAddressDaemon()
	app.run()
