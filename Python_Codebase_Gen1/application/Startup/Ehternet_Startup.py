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



#setup ethernet
Linux_Gpio.setup_ehternet()

#setup UART port
Linux_Gpio.setup_uart()
ser = serial.Serial("/dev/ttyS0", baudrate=9600)
demo_string = 'D0'+'\r\n'
test_string = 'W180' + '\r\n' + 'SEthernet is setup with IP address 192.168.0.50, enjoy!' + '\r\n'
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


