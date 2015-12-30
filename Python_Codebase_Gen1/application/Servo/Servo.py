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
step_size = 0.009
pwm_duty_cycle = 0.3 #0.035
pwm_step = step_size

#Linux_Gpio.setup(pin)

pwm_pin= 0

try:
	pwm_pin= str(sys.argv[1])
	print("PWM Pin Selected:",pwm_pin)
except:

#	pwm_pin	= 'PWM3'
	pwm_pin1= 'PWM5'
	pwm_pin2= 'PWM6'
#	pwm_pin	= 'PWM9'
#	pwm_pin	= 'PWM10'
#	pwm_pin	= 'PWM11'

	print("No input provided, setting default pin",pwm_pin1,pwm_pin2)

def(pwm_pin)

try:
	#Setup pwm pin
	Linux_Gpio.setup_pwm(pwm_pin1)
	Linux_Gpio.pwm(pwm_pin1, periodsec = '3', dutysec='0.6')
#	
#	
#	time.sleep(0.2)
#	Linux_Gpio.pwm(pwm_pin, periodsec = '3', dutysec='0.0')

	
	
	frequency =0
	
	while frequency < 2:

		
		pwm_duty_cycle = pwm_duty_cycle + pwm_step
		final= math.sin(pwm_duty_cycle)
		print(final)

		Linux_Gpio.pwm(pwm_pin1, periodsec = '3', dutysec=str(final) )

		if final > 0.8:
			pwm_step =  - pwm_step
		elif final <= 0.31 :
			pwm_step = step_size
			frequency = frequency + 1


	Linux_Gpio.pwm(pwm_pin1, periodsec = '3', dutysec=str(0) )
	
	frequency =0
	while frequency < 2:
	
			
			pwm_duty_cycle = pwm_duty_cycle + pwm_step
			final= math.sin(pwm_duty_cycle)
			print(final)
	
			Linux_Gpio.pwm(pwm_pin2, periodsec = '3', dutysec=str(final) )
	
			if final > 0.8:
				pwm_step =  - pwm_step
			elif final <= 0.31 :
				pwm_step = step_size
				frequency = frequency + 1
	
	
	Linux_Gpio.pwm(pwm_pin2, periodsec = '3', dutysec=str(0) )




except KeyboardInterrupt:
	Linux_Gpio.pins_cleanup()

