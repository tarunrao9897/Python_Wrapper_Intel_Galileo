#!/usr/bin/env python

#-------------------------------------------------------#
#                                                       #
#	Name: 	Digital_Input_Working.py	        #
#       Author: Varada Tarun Rao 	                #
#	Desc: 	Program to test Galelio Digital Pins	#
#       Date: 	03/09/2015                              #
#       Vern: 	0.1                                     #
#                                                       #
#-------------------------------------------------------#
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)  + '/../../..'))

#print(os.path.abspath(os.path.dirname(__file__)  + '/../../..'))

try:
	import lib.Python_lib as Pylib
except:

	sys.path.append('../../../')
	import lib.Python_lib as Pylib


import time, sys, os

Linux_Gpio = Pylib.PyGPIO()

input_pin= 0

try:
	input_pin= str(sys.argv[1])
	print("Digital Pin :",input_pin)
except:

	input_pin= 'DIGI_IO8'
	#input_pin= 'GPIO_LED'
	#input_pin= 'DIGI_IO2'
	#input_pin= 'DIGI_IO4'
	#input_pin= 'DIGI_IO7'
	#input_pin= 'DIGI_IO8'
	#input_pin= 'DIGI_IO12'
	#led_pin = 'DIGI_IO13'

	print("No input provided, setting default pin",input_pin)


print("Press CTRL +C to stop the Test")
try:


	Linux_Gpio.pin_setup(input_pin, dir='in')
	while True:

		print(Linux_Gpio.digital_read(input_pin))





except KeyboardInterrupt:
	Linux_Gpio.pins_cleanup()
