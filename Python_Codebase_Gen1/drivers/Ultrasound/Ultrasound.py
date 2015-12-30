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
sys.path.append(os.path.abspath(os.path.dirname(__file__)  + '/../..'))

#print(os.path.abspath(os.path.dirname(__file__)  + '/../../..'))

try:
	import lib.Python_lib as Pylib
except:

	sys.path.append('../../../')
	import lib.Python_lib as Pylib





import time, sys, os

Linux_Gpio = Pylib.PyGPIO()

usleep = lambda x: time.sleep(x/1000000.0)


led_pin = 0

TRIG_PIN	= 	'DIGI_IO4' #Output Pin
ECHO_PIN	=	'DIGI_IO7' #Input Pin


try:
	Linux_Gpio.pin_setup(TRIG_PIN,'out')


	#Linux_Gpio.set_digital_output(led_pin, '0')

	#led_pin = str(sys.argv[1])
#	print("Digital Pin :",led_pin )
except:

	#led_pin = 'DIGI_IO8'
	#
	#led_pin = 'GPIO_LED'
	#led_pin = 'DIGI_IO2'
	#led_pin = 'DIGI_IO4'
	#led_pin = 'DIGI_IO7'
	#led_pin = 'DIGI_IO8'
	led_pin = 'DIGI_IO12'
	#led_pin = 'DIGI_IO13'

	print("No input provided, setting default pin",led_pin )






print("Enter CTRL +C to stop Blinking")
try:


	while True:

		#Make TRIG to low
		Linux_Gpio.set_digital_output(TRIG_PIN, '0')
		time.sleep(2/1000000)

		#Make TRIG High
		Linux_Gpio.set_digital_output(TRIG_PIN, '1')
		time.sleep(10/1000000)

		#Make TRIG to low
		Linux_Gpio.set_digital_output(TRIG_PIN, '0')
		Linux_Gpio.pin_setup(ECHO_PIN,dir='in')
		print("ECHO Pin in the loop:",int(Linux_Gpio.digital_read(ECHO_PIN).rstrip('\n')))
		x = 1

#
#		while  x==1:
#
#			x = int(Linux_Gpio.digital_read(ECHO_PIN).rstrip('\n'))
#			print("ECHO Pin in the loop:",int(Linux_Gpio.digital_read(ECHO_PIN).rstrip('\n')),x)

		print("Echo Pin:",Linux_Gpio.digital_read(ECHO_PIN))

		time.sleep(1)



except KeyboardInterrupt:
	Linux_Gpio.pins_cleanup()


