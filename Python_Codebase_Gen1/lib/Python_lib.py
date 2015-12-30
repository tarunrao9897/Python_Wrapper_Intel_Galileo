#!/usr/bin/env python

#-------------------------------------------------------#
#                                                       #
#	Name: 	Python_lib.py 		                #
#       Author: Varada Tarun Rao 	                #
#	Desc: 	Python library to interface with Galileo#
#	 	GPIO					#
#       Date: 	03/05/2015                              # 	#
#       Ver: 	0.1                                     #
#                                                       #
#-------------------------------------------------------#


import time, sys, os
import shutil

Board_Pins = {

"GPIO_LED":	3,
"DIGI_IO2":  	32,
"DIGI_IO3":     18,	#do not set as digital output
"DIGI_IO4":  	28,
"DIGI_IO5":  	17,	#do not set as digital output
"DIGI_IO6":  	24,	#do not set as digital output
"DIGI_IO7":  	27,
"DIGI_IO8":  	26,
"DIGI_IO9":  	19,	#do not set as digital output
"DIGI_IO10":  	16,	#do not set as digital output
"DIGI_IO11":  	25,	#do not set as digital output
"DIGI_IO12": 	38,
"DIGI_IO13": 	39,
"ANG_A0":   	(37,'in_voltage0_raw'),
"ANG_A1":   	(36,'in_voltage1_raw'),
"ANG_A2":   	(23,'in_voltage2_raw'),
"ANG_A3":   	(22,'in_voltage3_raw'),
"ANG_A4":   	(21,'in_voltage4_raw'),
"ANG_A5":   	(20,'in_voltage5_raw'),
"PWM3": 	3,
"PWM5": 	5,
"PWM6": 	6,
"PWM9": 	1,
"PWM10":	7,
"PWM11":	4
}

Board_Pins_Enabled = {
"GPIO_LED":	False,
"DIGI_IO2":	False,
"DIGI_IO3":  	False,
"DIGI_IO4":  	False,
"DIGI_IO5":  	False,
"DIGI_IO6":  	False,
"DIGI_IO7":  	False,
"DIGI_IO8":  	False,
"DIGI_IO9":  	False,
"DIGI_IO10":  	False,
"DIGI_IO11":  	False,
"DIGI_IO12": 	False,
"DIGI_IO13": 	False,
"ANG_A0":   	False,
"ANG_A1":   	False,
"ANG_A2":   	False,
"ANG_A3":   	False,
"ANG_A4":   	False,
"ANG_A5":   	False,
"PWM3": 	False,
"PWM5": 	False,
"PWM6": 	False,
"PWM9": 	False,
"PWM10":	False,
"PWM11":	False
}


#----------------------------------------------------#
#	Python GPIO Interface Class	     	     #
#----------------------------------------------------#
class PyGPIO:


	def __init__(self):
		#print "Initial Setup."
		return

	#----------------------------------------------------#
	#	File Operation Functions	     	     #
	#----------------------------------------------------#

	def cmd(self, value, file):
		#print(file)
		with open(file, 'w') as File:
			File.write(str(value))
		return
	#use this function which required cat command from linux
	def cmd_cat(self, value, file):
		f = open(file, "r")
		return f.read()


	#----------------------------------------------------#
	#	Pin Setup Operation Functions	     	     #
	#----------------------------------------------------#
	def pin_setup(self, pin, dir='out'):
		#print("Pin Selected",pin)
		if pin[:2] == 'DI' or pin[:2] == 'PW' or pin[:2] == 'GP':
			linux_pin = Board_Pins[pin]
		elif pin[:2] == 'AN':
			linux_pin = Board_Pins[pin][0]
		#print("Pin Value",linux_pin)
		self.cmd(linux_pin , '/sys/class/gpio/unexport')
		self.cmd(linux_pin , '/sys/class/gpio/export')
		self.cmd('0', '/sys/class/gpio/gpio{}/value'.format(linux_pin))
		self.cmd(dir, '/sys/class/gpio/gpio{}/direction'.format(linux_pin))
		if dir == 'out':
			print("Setting to Strong for output pin")
			self.cmd('strong', '/sys/class/gpio/gpio{}/drive'.format(linux_pin))
		if dir == 'in':
			print("Setting to Open Drain for input pin")
			self.cmd('hiz', '/sys/class/gpio/gpio{}/drive'.format(linux_pin))
		Board_Pins_Enabled [pin] = True

		#print("Pin Selected",Board_Pins_Enabled [pin])
		return 1
	#----------------------------------------------------#
	#	Digital IO Operation Functions	     	     #
	#----------------------------------------------------#

	def set_digital_output(self, pin, value='1'):
		linux_pin = Board_Pins[pin]
                #print(actpin)
		if Board_Pins_Enabled [pin]:
			#print("Ouput Pin:",actpin)
			#self.pullup(pin)
			self.cmd(value, '/sys/class/gpio/gpio{}/value'.format(linux_pin))
			return 1
		else:
			print "{} has not been set to output.".format(pin)
			return 0

	#use this function which required cat command from linux
	def digital_read(self,pin):
		linux_pin = Board_Pins[pin]
		#print("Input Pin:", actpin)
		file = '/sys/class/gpio/gpio{}/value'.format(linux_pin)
		f = open(file, "r")
		return f.read()


	def setup_uart(self):
		level_shifter = 4
		rx = 40
		tx = 41

		#unexport the pin setup
		self.cmd(level_shifter , '/sys/class/gpio/unexport')
		self.cmd(rx , '/sys/class/gpio/unexport')
		self.cmd(tx , '/sys/class/gpio/unexport')

		#setup the pins for UART config.
		self.cmd(level_shifter , '/sys/class/gpio/export')
		self.cmd(rx , '/sys/class/gpio/export')
		self.cmd(tx , '/sys/class/gpio/export')

		self.cmd('out', '/sys/class/gpio/gpio{}/direction'.format(level_shifter))
		self.cmd('out', '/sys/class/gpio/gpio{}/direction'.format(rx))
		self.cmd('out', '/sys/class/gpio/gpio{}/direction'.format(tx))

		self.cmd('strong', '/sys/class/gpio/gpio{}/drive'.format(rx))
		self.cmd('strong', '/sys/class/gpio/gpio{}/drive'.format(tx))

		self.cmd('1', '/sys/class/gpio/gpio{}/value'.format(level_shifter))
		self.cmd('0', '/sys/class/gpio/gpio{}/value'.format(rx))
		self.cmd('0', '/sys/class/gpio/gpio{}/value'.format(tx))

	def setup_ehternet(self):
		#Start telnet server
		os.system("telnetd -l /bin/sh")
		os.system("ifconfig eth0 192.168.0.50 netmask 255.255.0.0 up")
	#----------------------------------------------------#
	#	Analog IO Operation Functions	     	     #
	#----------------------------------------------------#

	def analog_read(self,pin):
		linux_pin = Board_Pins[pin][1]
		#print(linux_pin )
		command = '/sys/bus/iio/devices/iio:device0/' + linux_pin
		return self.cmd_cat('cat',command)


	#----------------------------------------------------#
	#	PWM IO Operation Functions	     	     #
	#----------------------------------------------------#

	def setup_pwm(self,pin):
		linux_pin = Board_Pins[pin]
		print(linux_pin)
		self.cmd(linux_pin, '/sys/class/pwm/pwmchip0/unexport')
		self.cmd(linux_pin, '/sys/class/pwm/pwmchip0/export')
		self.cmd('1', '/sys/class/pwm/pwmchip0/pwm{}/enable'.format(linux_pin))
		Board_Pins_Enabled [pin] = True


	def pwm(self, pin, periodsec=0.02, dutysec=0.01):
		linux_pin = Board_Pins[pin]
		#self.cmd(actpin, '/sys/class/pwm/pwmchip0/unexport')
		#self.cmd(actpin, '/sys/class/pwm/pwmchip0/export')
		periodnano = int(float(periodsec) * 1000000)	# Should translate it from 0.02 Seconds to the value in Nano seconds
		#print("Period for pin", periodnano)
		dutynano = int(float(dutysec) * periodnano)	# Not accurate enough yet for Servo control. This Linux =/= Realtime OS + Python 'Garbage Collection'

		self.cmd(periodnano, '/sys/class/pwm/pwmchip0/pwm{}/period'.format(linux_pin))
		self.cmd(dutynano, '/sys/class/pwm/pwmchip0/pwm{}/duty_cycle'.format(linux_pin))

		return 1

	def pwm_shutdown(self, pin):
		linux_pin = Board_Pins[pin]
		self.cmd('0', '/sys/class/pwm/pwmchip0/pwm{}/enable'.format(linux_pin))
		return 1


	#----------------------------------------------------#
	#	Clean up Operation Functions	     	     #
	#----------------------------------------------------#


	def pins_cleanup(self):
		for Pin in Board_Pins:
			#print(Pin)
			if Pin[:2] == 'DI' and Board_Pins_Enabled [Pin]:
				linux_pin = Board_Pins[Pin]
				print("Cleaning the following IO pin", linux_pin)
				self.cmd('0', '/sys/class/gpio/gpio{}/value'.format(linux_pin))
				self.cmd(linux_pin, '/sys/class/gpio/unexport')
			elif  Pin[:1] == 'G' and Board_Pins_Enabled [Pin]:
				linux_pin = Board_Pins[Pin]
				print("Cleaning the following IO pin", linux_pin)
				self.cmd('0', '/sys/class/gpio/gpio{}/value'.format(linux_pin))
				self.cmd(linux_pin, '/sys/class/gpio/unexport')
			elif Pin[:2] == 'AN' and Board_Pins_Enabled [Pin]:
				linux_pin = Board_Pins[Pin][0]
				print("Cleaning the following IO pin", linux_pin)
				self.cmd('0', '/sys/class/gpio/gpio{}/value'.format(linux_pin))
				self.cmd(linux_pin, '/sys/class/gpio/unexport')

			elif Pin[:3] == 'PWM' and Board_Pins_Enabled [Pin]:
				linux_pin = Board_Pins[Pin]
				print("Cleaning the following PWM pin", linux_pin)
				self.cmd('0', '/sys/class/pwm/pwmchip0/pwm{}/duty_cycle'.format(linux_pin))
				#self.cmd('0', '/sys/class/pwm/pwmchip0/pwm{}/enable'.format(actpin))
				self.cmd(linux_pin, '/sys/class/pwm/pwmchip0/unexport')

