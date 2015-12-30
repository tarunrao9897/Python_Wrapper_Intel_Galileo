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

#print(os.path.abspath(os.path.dirname(__file__)  + '/../..'))

try:
	import lib.Python_lib as Pylib
except:

	sys.path.append('../../')
	import lib.Python_lib as Pylib

import time, sys, os,math

Linux_Gpio= Pylib.PyGPIO()


step_size = 0.001
pwm_duty_cycle = 0 #0.035
pwm_step = step_size

#Define pins for motor

#ENABLE PINS for Motor - PWM
EA_PIN		= 'PWM9'	#Motor A

EB_PIN		= 'PWM10'	#Motor B

#IN PINS - Digital IO
IN_1	 	= 'DIGI_IO8'		#Motor A
IN_2	 	= 'PWM11'	#Motor A

IN_3 		= 'DIGI_IO13'	#Motor B
IN_4		= 'DIGI_IO12'	#Motor B


#led_pin		= 'IO3'
#Linux_Gpio.setup(led_pin)
#Linux_Gpio.set_digital_output(led_pin, '1')


delay = 2
step_size = 0.001
pwm_duty_cycle = 0.2 #0.035
pwm_step = step_size


ON	= '1.0'
OFF	= '0'
#IMPORTANT - Based on iput power vary this
motor_speed = 0.5 	# 1.0 - for AC power, 0.5-0.6 - for battery
#Linux_Gpio.setup(pin)



analog_pin_1	= 'ANG_A0'
analog_pin_2	= 'ANG_A1'
analog_pin_3	= 'ANG_A2'



counter_range = 20000
difference = 100

START_APPLICATION	= 1
STOP_APPLICATION	= 0

OBSTACLE_DETECTED 	= 0
INITIALIZE_ONCE 	= 1
a 	= 2
b	= 3
SURFACE_TYPE 	= 4
counter 	= 5


array_size = 6

var = [0]*array_size

OPTICAL_RANGE = 200

OBSTACLE_RANGE = 500


BLACK_SURFACE	=	1
WHITE_SURFACE	=	0

def scanning_optical_sensor(opt_pin_1,opt_pin_2,opt_pin_3):




	Sensor_pin_1_adc_value = int(Linux_Gpio.analog_read(opt_pin_1))
	Sensor_pin_2_adc_value = int(Linux_Gpio.analog_read(opt_pin_2))
	Sensor_pin_3_adc_value = int(Linux_Gpio.analog_read(opt_pin_3))

	#print(Sensor_pin_1_adc_value,Sensor_pin_2_adc_value)

	if Sensor_pin_3_adc_value <= OBSTACLE_RANGE:
		print("OBSTACLE DETECTED")
		#debounce time
		time.sleep(1)

		if var[OBSTACLE_DETECTED] == STOP_APPLICATION:
			var[OBSTACLE_DETECTED] = START_APPLICATION

		elif var[OBSTACLE_DETECTED] == START_APPLICATION:
			var[OBSTACLE_DETECTED] = STOP_APPLICATION


	if Sensor_pin_1_adc_value >= OPTICAL_RANGE or Sensor_pin_2_adc_value >= OPTICAL_RANGE :
		return BLACK_SURFACE
	else:
		return WHITE_SURFACE


def motor_init():
	#Setup ENABLE PINS as pwm
	Linux_Gpio.setup_pwm(EA_PIN)
	Linux_Gpio.setup_pwm(EB_PIN)

	#Setup IN PINS for Motor A
	Linux_Gpio.pin_setup(IN_1)
	Linux_Gpio.setup_pwm(IN_2)

	#Setup IN PINS for Motor B
	Linux_Gpio.pin_setup(IN_3)
	Linux_Gpio.pin_setup(IN_4)


	#Disable MotorA
	Linux_Gpio.pwm(EA_PIN, periodsec = '1', dutysec=OFF )
	#Disable MotorB
	Linux_Gpio.pwm(EB_PIN, periodsec = '1', dutysec=OFF )

	#Disable Motor Pin
	Linux_Gpio.pwm(IN_2, periodsec = '1', dutysec=OFF )

def motor_brake(motor):
	if motor == 'A':
		Linux_Gpio.set_digital_output(IN_1, '1')
		Linux_Gpio.pwm(IN_2, periodsec = '1', dutysec=ON )

	elif motor == 'B':
		Linux_Gpio.set_digital_output(IN_3, '1')
		Linux_Gpio.set_digital_output(IN_4, '1')
def motor_clockwise(motor):
	if motor == 'A':
		Linux_Gpio.set_digital_output(IN_1, '1')
		Linux_Gpio.pwm(IN_2, periodsec = '1', dutysec=OFF )

	elif motor == 'B':
		Linux_Gpio.set_digital_output(IN_3, '1')
		Linux_Gpio.set_digital_output(IN_4, '0')

def motor_anticlockwise(motor):
	if motor == 'A':
		Linux_Gpio.set_digital_output(IN_1, '0')
		Linux_Gpio.pwm(IN_2, periodsec = '1', dutysec=ON )

	elif motor == 'B':
		Linux_Gpio.set_digital_output(IN_3, '0')
		Linux_Gpio.set_digital_output(IN_4, '1')

def move_forward():
	#Turn Motor Anit-ClockWise
	motor_anticlockwise('A')
	motor_anticlockwise('B')

def stop_moving():

	#Break Motor
	motor_brake('A')
	motor_brake('B')

def turn_right():
	#Turn right/left reverse
	motor_clockwise('A')
	motor_anticlockwise('B')


try:
	motor_init()
	Linux_Gpio.pwm(EA_PIN, periodsec = '1', dutysec=str(motor_speed))
	Linux_Gpio.pwm(EB_PIN, periodsec = '1', dutysec=str(motor_speed))

	Linux_Gpio.pin_setup(analog_pin_1)
	Linux_Gpio.pin_setup(analog_pin_2)
	Linux_Gpio.pin_setup(analog_pin_3)




	while True:
		scanning_optical_sensor(analog_pin_1,analog_pin_2,analog_pin_3)
		if var[OBSTACLE_DETECTED] == START_APPLICATION:
		        #print("Starting application")
			if var[INITIALIZE_ONCE] == 0:
				print("Moving forward only once")
				var[INITIALIZE_ONCE] =1
				#Move the robot forward initially - Keep on white surface
				move_forward()


			if scanning_optical_sensor(analog_pin_1,analog_pin_2,analog_pin_3) == BLACK_SURFACE:
				print "Stop the Motor"
				stop_moving()
				time.sleep(1)
				turn_right()
				time.sleep(1)
				stop_moving()
				time.sleep(1)
				move_forward()

		elif var[INITIALIZE_ONCE] == 1:
			if var[OBSTACLE_DETECTED] == STOP_APPLICATION:
				print("Stopping Application")
				var[INITIALIZE_ONCE] = 0
				stop_moving()





except KeyboardInterrupt:
	Linux_Gpio.pins_cleanup()

