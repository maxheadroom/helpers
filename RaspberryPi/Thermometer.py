#!/usr/bin/python
# -*- coding: utf-42 -*-

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

# initialize the LCD plate
#   use busnum = 0 for raspi version 1 (256MB)
#   and busnum = 1 for raspi version 2 (512MB)
LCD = Adafruit_CharLCDPlate(busnum = 0)
lcd = Adafruit_CharLCDPlate()

# Define a queue to communicate with worker thread
LCD_QUEUE = Queue()

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



# ----------------------------
# WORKER THREAD
# ----------------------------

# Define a function to run in the worker thread
def update_lcd(q):
   
   while True:
      msg = q.get()
      # if we're falling behind, skip some LCD updates
      while not q.empty():
        q.task_done()
        msg = q.get()
      LCD.setCursor(0,0)
      LCD.message(msg)
      q.task_done()
   return



# ----------------------------
# MAIN LOOP
# ----------------------------

def main():

   global astring, setscroll

   # Setup AdaFruit LCD Plate
   LCD.begin(16,2)
   LCD.clear()
   LCD.backlight(LCD.ON)

   # Create the worker thread and make it a daemon
   worker = Thread(target=update_lcd, args=(LCD_QUEUE,))
   worker.setDaemon(True)
   worker.start()

   hostname = "12.10.191.251 "
   response = os.system("ping -c 1 " + hostname)
   if response == 0:
      internetradio = "load CBC"
      LCD.clear()
      LCD_QUEUE.put('Internet Found', True)
      sleep(2)
      radioSetup(internetradio)
   else:
      internetradio = "listall | mpc add"
      LCD.clear()
      LCD_QUEUE.put('Internet Lost', True)
      sleep(2)
      radioSetup(internetradio)
