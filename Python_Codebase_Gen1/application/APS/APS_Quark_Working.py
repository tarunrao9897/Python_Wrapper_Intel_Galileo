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
import time
import curses
sys.path.append(os.path.abspath(os.path.dirname(__file__)  + '/../..'))

#print(os.path.abspath(os.path.dirname(__file__)  + '/../..'))

try:
	import lib.Python_lib as Pylib
except:

	sys.path.append('../../')
	import lib.Python_lib as Pylib

import time, sys, os

Linux_Gpio = Pylib.PyGPIO()



# These are the input lines for CRB 1
CRB_SLP_S3_1 	= 'DIGI_IO2'
CRB_SLP_S4_1 	= 'DIGI_IO3'
CRB_SLP_S5_1 	= 'DIGI_IO4'
CRB_SLP_A_1 	= 'DIGI_IO5'

# These are the input lines for CRB 2
CRB_SLP_S3_2 	= 'DIGI_IO6'
CRB_SLP_S4_2 	= 'DIGI_IO7'
CRB_SLP_S5_2 	= 'DIGI_IO8'
CRB_SLP_A_2 	= 'DIGI_IO9'


pwm_pin_10	= 'PWM10'
pwm_pin_11	= 'PWM11'

IO_12_pin 	= 'DIGI_IO12'
IO_13_pin 	= 'DIGI_IO13'

SW_CRB_1 = 0
SW_CRB_2 = 1

ARRAY_SIZE = 2

SW_CRB = [0]*ARRAY_SIZE

class Printer():
    """
    Print things to stdout on one line dynamically
    """
 
    def __init__(self,data):
 
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()

#Initialze the APS
def APS_init():
	#These are the Input GPIO for CRB1
	Linux_Gpio.pin_setup(CRB_SLP_S3_1, dir='in')
	Linux_Gpio.pin_setup(CRB_SLP_S4_1, dir='in')
	Linux_Gpio.pin_setup(CRB_SLP_S5_1, dir='in')
	Linux_Gpio.pin_setup(CRB_SLP_A_1, dir='in')

	#These are the Input GPIO for CRB2
	Linux_Gpio.pin_setup(CRB_SLP_S3_2, dir='in')
	Linux_Gpio.pin_setup(CRB_SLP_S4_2, dir='in')
	Linux_Gpio.pin_setup(CRB_SLP_S5_2, dir='in')
	Linux_Gpio.pin_setup(CRB_SLP_A_2, dir='in')
	return 0


# This is to turnoff power.
# DDummy wrapper for now
def APS_PowerOff():
	SW_CRB[SW_CRB_1] = SW_CRB[SW_CRB_2] = 0
	#TODO add out GPIOs and set that to turn off platform
	return 0

def APS_GetPwrSts():
	#print "Do you have CRB1 connected to Galelio?"
	#Get user input for the CRB1 and CRB2 Set to On foor now
	SW_CRB[SW_CRB_1] = SW_CRB[SW_CRB_2] = 0
	SW_CRB[SW_CRB_2] =1
	TurnOff = SW_CRB[SW_CRB_1] | SW_CRB[SW_CRB_2]
	return

#########################
SCANNING_FREQUENCY = 0.10
#########################
ON	= '1'
OFF	= '0'

# Setup and Initialize Pins
def io_init():

	#Setting the output pins - default all off

	Linux_Gpio.setup_pwm(pwm_pin_10)
	Linux_Gpio.setup_pwm(pwm_pin_11)

	Linux_Gpio.pin_setup(IO_12_pin)
	Linux_Gpio.set_digital_output(IO_12_pin, OFF)

	Linux_Gpio.pin_setup(IO_13_pin)
	Linux_Gpio.set_digital_output(IO_13_pin, OFF)

	Linux_Gpio.pwm(pwm_pin_10, periodsec = '1', dutysec=OFF)
	Linux_Gpio.pwm(pwm_pin_11, periodsec = '1', dutysec=OFF )

#Set specific values to Digital Ouptut Pins
def io_set_value(pin_10_value,pin_11_value,pin_12_value,pin_13_value):

	Linux_Gpio.pwm(pwm_pin_10, periodsec = '1', dutysec=pin_10_value)
	Linux_Gpio.pwm(pwm_pin_11, periodsec = '1', dutysec=pin_11_value )
	Linux_Gpio.set_digital_output(IO_12_pin, pin_12_value)
	Linux_Gpio.set_digital_output(IO_13_pin, pin_13_value)


try:
	#Setting the pind for Digital output - PWM10,PWM11,IO12,IO13
	io_init()
	#Setting up the Analog Pins - IO2 -IO9
	APS_init()
	APS_GetPwrSts()

	print("SW_CRB_1 :", SW_CRB[SW_CRB_1])


	os.system('clear') 
	
	PROGRESS_SYMBOL = "%"
	refresh_paramater = 1
	#print("\n\n\n\n")
	print("  *************************************************************************")
	print("  *                       PLATFORM STATUS DASHBOARD                       *")
	print("  *************************************************************************")
        print "    SLP_S3        "  + "SLP_S4       " +"SLP_S5       " + "ME AWAKE     " + "PLATFORM STATE"+"\n"
        
        LINER = "***********************************************************************"
	while True:

		if(SW_CRB[SW_CRB_1]):

			#print "CRB 1 SLP_S3 = " + Linux_Gpio.digital_read(CRB_SLP_S3_1)\
			#+ "CRB 1 SLP_S4 = " + Linux_Gpio.digital_read(CRB_SLP_S4_1)\
			#+ "CRB 1 SLP_S5 = " + Linux_Gpio.digital_read(CRB_SLP_S5_1)\
			#+ "CRB 1 ME     = " + Linux_Gpio.digital_read(CRB_SLP_A_1)

			io_set_value(ON,ON,ON,ON)
			time.sleep(delay)

		if(SW_CRB[SW_CRB_2]):
			x = "CRB 100 SLP_S3 = "
			S3 = int(Linux_Gpio.digital_read(CRB_SLP_S3_2)) 
			S4 = int(Linux_Gpio.digital_read(CRB_SLP_S4_2))
			S5 = int(Linux_Gpio.digital_read(CRB_SLP_S5_2))
			ME_AWAKE = int(Linux_Gpio.digital_read(CRB_SLP_A_2))
			RESULT = "UNKNOWN STATE   " 
			
			if(not(S3)and S4 and S5 and ME_AWAKE):
				RESULT = "SLEEP M3        "
			elif (not(S3)and S4 and S5 and not(ME_AWAKE)):
				RESULT = "SLEEP MOFF      "
				
			elif (not(S3) and not(S4) and S5 and ME_AWAKE):
				RESULT = "HIBERNATION  M3"
			elif (not(S3) and not(S4) and S5 and not(ME_AWAKE)):
				RESULT = "HIBERNATION MOFF"

			elif (not(S3) and not(S4) and not(S5) and ME_AWAKE):
				RESULT = "SHUTDOWN  M3    "
			elif (not(S3) and not(S4) and not(S5) and not(ME_AWAKE)):
				RESULT = "SHUTDOWN MOFF   "
			
			elif (S3 and S4 and S5 and ME_AWAKE):
				RESULT = "ON M0           "
						
			
			if(refresh_paramater):
				#print("Hi")
				PROGRESS_SYMBOL = "  "
				refresh_paramater = 0
			elif(not(refresh_paramater)):
				#print("Hi")
				refresh_paramater = 1
				PROGRESS_SYMBOL = "%%"
			 
		        sys.stdout.write("\r       %d  " %S3)
		        sys.stdout.write("          %d  " %S4)
		        sys.stdout.write("          %d  " %S5)
		        sys.stdout.write("          %d" %ME_AWAKE)
		        sys.stdout.write("           %s" %RESULT)
		        sys.stdout.write(" %s" %PROGRESS_SYMBOL)
		        
		      
		        sys.stdout.flush()
		        
	
					
			

			
    		        #print(os.path.getsize(file_name)/1024+'KB / '+size+' KB downloaded!\r'),
			#printf ('\rCRB 1 SLP_S3 = %d',Linux_Gpio.digital_read(CRB_SLP_S3_2));
			#print "CRB 1 SLP_S4 = " + Linux_Gpio.digital_read(CRB_SLP_S4_2),
			#print "CRB 1 SLP_S5 = " + Linux_Gpio.digital_read(CRB_SLP_S5_2),
			#print "CRB 1 ME     = " + Linux_Gpio.digital_read(CRB_SLP_A_2)
			io_set_value(OFF,OFF,OFF,OFF)
			time.sleep(SCANNING_FREQUENCY)




except KeyboardInterrupt:
	Linux_Gpio.pins_cleanup()


