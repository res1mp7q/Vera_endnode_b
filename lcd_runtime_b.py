#!/usr/bin/env python
# Standalone EndNodeB runtime using I2C and MCP23008 on raspberry pi.
# Created by Jimmy Lamont for use with a Vera HAP and wunderground
# Dont forget to enter your vera address and api key/state/city!

import time
import requests
import Adafruit_CharLCD as LCD
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime


# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2


# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDBackpack()

# create some custom characters
lcd.create_char(1, [2, 3, 2, 2, 14, 30, 12, 0])
lcd.create_char(2, [0, 1, 3, 22, 28, 8, 0, 0])
lcd.create_char(3, [0, 14, 21, 23, 17, 14, 0, 0])
lcd.create_char(4, [31, 17, 10, 4, 10, 17, 31, 0])
lcd.create_char(5, [8, 12, 10, 9, 10, 12, 8, 0])
lcd.create_char(6, [2, 6, 10, 18, 10, 6, 2, 0])
lcd.create_char(7, [31, 17, 21, 21, 21, 21, 17, 31])


p = Popen('hostname -I', shell=True, stdout=PIPE)
IP = p.communicate()[0]


# Start routine, diplay relevant 411
lcd.set_backlight(0)
lcd.clear()
lcd.message('\n     Hello')

time.sleep(3.0)

#Show version and name
lcd.clear()
lcd.message('  Vera \n  endnode B')
time.sleep(2.0)
lcd.clear()
lcd.message('\n30DEC2017  v0.04')
time.sleep(2.0)
lcd.clear()
lcd.message(IP)
time.sleep(2.0)
lcd.clear()

#Bought the Pi some time, so startup is complete, setup weather request, run the loop

r = requests.get('http://api.wunderground.com/api/<API Key Here>/conditions/q/<State>/<City>.json')
data = r.json()


lastmessage = ""
while True:
        now = "{}\n{}".format(datetime.now().strftime('%b %d  %H:%M'), data['current_observation']['temperature_string'])
        if lastmessage != now:
                lcd.clear()
                lcd.set_backlight(0)
                lcd.message (now)
                lastmessage = now
