#!/usr/bin/env python

#-------------------------------------------------------#
#                                                       #
#	Name: 	Digital_Working.py 		        #
#       Author: Varada Tarun Rao 	                #
#	Desc: 	Program to test Galelio Digital Pins	#
#       Date: 	03/05/2015                              #
#       Vern: 	0.1                                     #
#                                                       #
#-------------------------------------------------------#
import os
import sys
import serial
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

try:
	led_pin = str(sys.argv[1])
	print("Digital Pin :",led_pin )
except:

	#led_pin = 'DIGI_IO8'
	#
	led_pin = 'GPIO_LED'
	#led_pin = 'DIGI_IO2'
	#led_pin = 'DIGI_IO4'
	#led_pin = 'DIGI_IO7'
	#led_pin = 'DIGI_IO8'
	#led_pin = 'DIGI_IO12'
	#led_pin = 'DIGI_IO13'

	print("No input provided, setting default pin",led_pin )



Linux_Gpio.pin_setup(led_pin,'out')
Linux_Gpio.set_digital_output(led_pin, '1')

#setup UART port
Linux_Gpio.setup_uart()
ser = serial.Serial("/dev/ttyS0", baudrate=9600)
demo_string = 'D0'+'\r\n'
test_string = 'W180' + '\r\n' + 'SHello there! My name is Galelio. Nice to meet you. ' + '\r\n'
ser.write(test_string);
ser.close()


print("Enter CTRL +C to stop Blinking")
try:


	while True:


		Linux_Gpio.set_digital_output(led_pin, '1')

		time.sleep(1)
		Linux_Gpio.set_digital_output(led_pin, '0')

		time.sleep(1)



except KeyboardInterrupt:
	Linux_Gpio.pins_cleanup()


