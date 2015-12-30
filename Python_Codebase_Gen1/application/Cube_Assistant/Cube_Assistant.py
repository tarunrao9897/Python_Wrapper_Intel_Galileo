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
import serial
sys.path.append(os.path.abspath(os.path.dirname(__file__)  + '/../..'))

#print(os.path.abspath(os.path.dirname(__file__)  + '/../../..'))

try:
	import lib.Python_lib as Pylib
except:

	sys.path.append('../../')
	import lib.Python_lib as Pylib


import time, sys, os

Linux_Gpio = Pylib.PyGPIO()
prox_input_pin	=	'DIGI_IO7'
laser_input_pin	= 	'DIGI_IO8'
pwm_pin		=	'PWM5'






print("Press CTRL +C to stop the Test")
try:


	#setup UART port
	Linux_Gpio.setup_uart()
	ser = serial.Serial("/dev/ttyS0", baudrate=9600)
	demo_string = 'D0'+'\r\n'
	test_string = 'W180' + '\r\n' + 'SHello there! My name is Galelio. Nice to meet you. This is Cube Assist Demo ' + '\r\n'
	ser.write(test_string);
	ser.close()

	Linux_Gpio.pin_setup(prox_input_pin, dir='in')
	Linux_Gpio.pin_setup(laser_input_pin, dir='in')
	#Setup pwm pin
	Linux_Gpio.setup_pwm(pwm_pin)

	Linux_Gpio.pwm(pwm_pin, periodsec = '3', dutysec=str(0) )
	y = 1

	tarun_is_present = 0
	send_response= 0

	z= 1
	while True:
		prox_response = int(Linux_Gpio.digital_read(prox_input_pin))
		laser_response = int(Linux_Gpio.digital_read(laser_input_pin))
		if(laser_response):
			Linux_Gpio.pwm(pwm_pin, periodsec = '3', dutysec=str(0.8))





		if(prox_response ==0):


			if(y):
				print("Hello There")
				test_string = 'W180' + '\r\n' +'sHello There!' + '\r\n'
				y = 0

			else:
				print("Bye")
				test_string = 'W25' + '\r\n' +'sBye' + '\r\n'
				y = 1
				Linux_Gpio.pwm(pwm_pin, periodsec = '3', dutysec=str(0.0))

			ser = serial.Serial("/dev/ttyS0", baudrate=9600)

			ser.write(test_string);
			ser.close()
			time.sleep(2)


		#print(x)


#
#		if(x):





except KeyboardInterrupt:
	Linux_Gpio.pins_cleanup()
