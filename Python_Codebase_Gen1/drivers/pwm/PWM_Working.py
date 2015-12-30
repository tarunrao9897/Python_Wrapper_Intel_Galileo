#!/usr/bin/env python

#-------------------------------------------------------#
#!/usr/bin/env python

#-------------------------------------------------------#
#                                                       #
#	Name: 	PWM_Working.py 			        #
#       Author: Varada Tarun Rao 	                #
#	Desc: 	Program to test Galelio PWM Pins	#
#       Date: 	03/09/2015                              #
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

import time, sys, os,math

Linux_Gpio = Pylib.PyGPIO()



delay = 0.02
step_size = 0.005
pwm_duty_cycle = 0 #0.035
pwm_step = step_size

#Linux_Gpio.setup(pin)

pwm_pin= 0

try:
	pwm_pin= str(sys.argv[1])
	print("PWM Pin Selected:",pwm_pin)
except:

#	pwm_pin	= 'PWM3'
	pwm_pin	= 'PWM5'
#	pwm_pin	= 'PWM6'
#	pwm_pin	= 'PWM9'
#	pwm_pin	= 'PWM10'
#	pwm_pin	= 'PWM11'

	print("No input provided, setting default pin",pwm_pin)



try:
	#Setup pwm pin
	Linux_Gpio.setup_pwm(pwm_pin)
	#Linux_Gpio.pwm(pwm_pin, periodsec = '3', dutysec='0.8' )

	while True:

		x =1
		pwm_duty_cycle = pwm_duty_cycle + pwm_step
		final= math.sin(pwm_duty_cycle)
		print(final)

		Linux_Gpio.pwm(pwm_pin, periodsec = '3', dutysec=str(final) )

		if final >= 0.9:
			pwm_step = pwm_step
		if final <= 0 :
			pwm_step = step_size







except KeyboardInterrupt:
	Linux_Gpio.pins_cleanup()

