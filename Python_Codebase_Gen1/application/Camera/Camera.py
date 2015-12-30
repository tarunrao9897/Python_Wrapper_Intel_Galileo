#!/usr/bin/env python

#-------------------------------------------------------#
#                                                       #
#	Name: 	Digital_Working.py 		        #
#       Author: Varada Tarun Rao 	                #
#	Desc: 	Program to test Galelio Digital Pins	#
#       Date: 	08/18/2015                              #
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

import time, sys, os,math

Linux_Gpio= Pylib.PyGPIO()


BAUD = 38400
PORT = "COM1"      # change this to your com port!
TIMEOUT = 0.2

SERIALNUM = 0    # start with 0

COMMANDSEND = 0x56
COMMANDREPLY = 0x76
COMMANDEND = 0x00

CMD_GETVERSION = 0x11
CMD_RESET = 0x26
CMD_TAKEPHOTO = 0x36
CMD_READBUFF = 0x32
CMD_GETBUFFLEN = 0x34

FBUF_CURRENTFRAME = 0x00
FBUF_NEXTFRAME = 0x01
FBUF_STOPCURRENTFRAME = 0x00

getversioncommand = [COMMANDSEND, SERIALNUM, CMD_GETVERSION, COMMANDEND]
resetcommand = [COMMANDSEND, SERIALNUM, CMD_RESET, COMMANDEND]
takephotocommand = [COMMANDSEND, SERIALNUM, CMD_TAKEPHOTO, 0x01, FBUF_STOPCURRENTFRAME]
getbufflencommand = [COMMANDSEND, SERIALNUM, CMD_GETBUFFLEN, 0x01, FBUF_CURRENTFRAME]


def checkreply(r, b):
    r = map (ord, r)
    if (r[0] == 0x76 and r[1] == SERIALNUM and r[2] == b and r[3] == 0x00):
        return True
    return False

def reset():
	s = serial.Serial("/dev/ttyS0", baudrate=BAUD)
	cmd = ''.join( map( chr, resetcommand ) )
	s.write(cmd)
	#reply = s.read(100)
	#r = list(reply)
	s.close()
	time.sleep(2)
	#if checkreply( r, CMD_RESET ):
	#	return True
	#return False
        
def getversion():

    s = serial.Serial("/dev/ttyS0", baudrate=BAUD)
    cmd = ''.join (map (chr, getversioncommand))
    print cmd
    s.write(cmd)
    reply =  s.read(16)
    s.close()
    r = list(reply);
    if checkreply(r, CMD_GETVERSION):
        print r
        return True
    return False

def takephoto():
    s = serial.Serial("/dev/ttyS0", baudrate=BAUD)
    cmd = ''.join (map (chr, takephotocommand))
    s.write(cmd)
    reply =  s.read(5)
    s.close()
    r = list(reply);
    print r
    
    
    if (checkreply(r, CMD_TAKEPHOTO) and r[3] == chr(0x0)):
        return True
    return False   

def getbufferlength():
    s = serial.Serial("/dev/ttyS0", baudrate=BAUD)
    cmd = ''.join (map (chr, getbufflencommand))
    print cmd
    s.write(cmd)
    reply =  s.read(9)
    s.close()
    r = list(reply);
    print r
    if (checkreply(r, CMD_GETBUFFLEN) and r[4] == chr(0x4)):
        l = ord(r[5])
        l <<= 8
        l += ord(r[6])
        l <<= 8
        l += ord(r[7])
        l <<= 8
        l += ord(r[8])
        return l
               
    return 0

readphotocommand = [COMMANDSEND, SERIALNUM, CMD_READBUFF, 0x0c, FBUF_CURRENTFRAME, 0x0a]


def readbuffer(bytes):
	addr = 0   # the initial offset into the frame buffer
	photo = []

	# bytes to read each time (must be a mutiple of 4)
	inc = 8192
	s = serial.Serial("/dev/ttyS0", baudrate=BAUD)
	while( addr < bytes ):
 		# on the last read, we may need to read fewer bytes.
                chunk = min( bytes-addr, inc );

		# append 4 bytes that specify the offset into the frame buffer
		command = readphotocommand + [(addr >> 24) & 0xff, 
				(addr>>16) & 0xff, 
				(addr>>8 ) & 0xff, 
				addr & 0xff]

		# append 4 bytes that specify the data length to read
		command += [(chunk >> 24) & 0xff, 
				(chunk>>16) & 0xff, 
				(chunk>>8 ) & 0xff, 
				chunk & 0xff]

		# append the delay
		command += [1,0]

		# print map(hex, command)
		print "Reading", chunk, "bytes at", addr

		# make a string out of the command bytes.
		cmd = ''.join(map(chr, command))
	        s.write(cmd)

		# the reply is a 5-byte header, followed by the image data
		#   followed by the 5-byte header again.
		reply = s.read(5+chunk+5)

 		# convert the tuple reply into a list
		r = list(reply)
		if( len(r) != 5+chunk+5 ):
			# retry the read if we didn't get enough bytes back.
			print "Read", len(r), "Retrying."
			continue

		if( not checkreply(r, CMD_READBUFF)):
			print "ERROR READING PHOTO"
			return
		
		# append the data between the header data to photo
		photo += r[5:chunk+5]

		# advance the offset into the frame buffer
		addr += chunk
	s.close()
	print addr, "Bytes written"
	return photo




try:
	print("Setting up UART")
	#setup UART port
	Linux_Gpio.setup_uart()
	#s = serial.Serial("/dev/ttyS0", baudrate=BAUD)
	reset()
	
	if (not getversion()):
		print "Camera not found"
	else:
		print "VC0706 Camera found"
	#s.close()
	if takephoto():
    		print "Snap!"
	bytes = getbufferlength()

	print bytes, "bytes to read"
	
	photo = readbuffer(bytes)
	f = open("/media/mmcblk0p1/Python_Codebase_Gen1/application/Camera/photo.jpg", 'w')
	#print photo
	photodata = ''.join(photo)
	f.write(photodata)
	f.close()
	print ("Photo recorded")
	while(1):
		x =1


	#setup UART port
#	Linux_Gpio.setup_uart()
#	ser = serial.Serial("/dev/ttyS0", baudrate=9600)
#	demo_string = 'D0'+'\r\n'
#	test_string = 'W180' + '\r\n' + 'SHello there! My name is Galelio Bot! Lets start moving! ' + '\r\n'
#	ser.write(test_string);
#	ser.close()





except KeyboardInterrupt:
	Linux_Gpio.pins_cleanup()

