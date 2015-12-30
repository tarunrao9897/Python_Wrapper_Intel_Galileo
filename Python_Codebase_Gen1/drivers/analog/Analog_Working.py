#!/usr/bin/env python

#-------------------------------------------------------#
#                                                       #
#	Name: 	Analog_Working.py 		        #
#       Author: Varada Tarun Rao 	                #
#	Desc: 	Program to test Galelio Analog Pins	#
#       Date: 	03/05/2015                              #
#       Vern: 	0.1                                     #
#                                                       #
#-------------------------------------------------------#
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)  + '/../..'))

#print(os.path.abspath(os.path.dirname(__file__)  + '/../..'))

try:
	import lib.Python_lib as Pylib
except:

	sys.path.append('../../')
	import lib.Python_lib as Pylib

import time, sys, os

Linux_Gpio = Pylib.PyGPIO()


led_pin = 0

analog_pin_1	= 0
analog_pin_2	= 0
try:
	analog_pin_1= str(sys.argv[1])
	analog_pin_2= str(sys.argv[2])

	print("Analog Pins :",analog_pin_1,analog_pin_2)
except:



	analog_pin_1	= 'ANG_A0'
	analog_pin_2	= 'ANG_A1'
	#analog_pin_1 	= 'ANG_A2'
	#analog_pin_2 	= 'ANG_A3'
	#analog_pin_1 	= 'ANG_A4'
	#analog_pin_2 	= 'ANG_A5'



	print("No input provided, setting default pins ",analog_pin_1,analog_pin_2)




print("Enter CTRL +C to stop Analog Operation")
try:

	Linux_Gpio.pin_setup(analog_pin_1)
	Linux_Gpio.pin_setup(analog_pin_2)



	while True:

		print (Linux_Gpio.analog_read(analog_pin_1), Linux_Gpio.analog_read(analog_pin_2))



except KeyboardInterrupt:
	Linux_Gpio.pins_cleanup()


