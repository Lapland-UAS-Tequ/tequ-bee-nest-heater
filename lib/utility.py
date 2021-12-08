from utime import sleep_ms
from utime import localtime
from utime import ticks_ms
from pycom import rgbled
from machine import deepsleep, Pin
from ubinascii import unhexlify, hexlify
from pycom import nvs_set,nvs_get
from struct import pack,unpack
from sys import print_exception
from math import sqrt

def log(string):
	dateArray = localtime()
	ts = "%02d-%02d-%02d %02d:%02d:%02d" % (dateArray[0],dateArray[1],dateArray[2],dateArray[3],dateArray[4],dateArray[5])
	print("%s : %s" % (ts,string))

def getYear():
	dateArray = localtime()
	return dateArray[0]

def log2(string):
	print("%.3f: %s" % (ticks_ms()/1000,string))

def blinkLED(color,time_ms, times=1):
	for x in range(times):
		if color == "blue":
			rgbled(0x00007f)
		elif color == "aqua":
			rgbled(0x00ffff)
		elif color == "red":
			rgbled(0x7f0000)
		elif color == "green":
			rgbled(0x007f00)
		elif color == "magenta":
			rgbled(0xff00ff)
		elif color == "yellow":
			rgbled(0xffff00)
		elif color == "white":
			rgbled(0xffffff)
		else:
			rgbled(0x000000)

		sleep_ms(time_ms)
		rgbled(0x000000)
		sleep_ms(time_ms)


def changeLED(color,time_ms):
	if color == "blue":
		rgbled(0x00007f)
	elif color == "aqua":
		rgbled(0x00ffff)
	elif color == "red":
		rgbled(0x7f0000)
	elif color == "green":
		rgbled(0x007f00)
	elif color == "magenta":
		rgbled(0xff00ff)
	elif color == "yellow":
		rgbled(0xffff00)
	elif color == "white":
		rgbled(0xffffff)
	else:
		rgbled(0x000000)

	sleep_ms(time_ms)


def setLED(color):
	if color == "blue":
		rgbled(0x00007f)
	elif color == "aqua":
		rgbled(0x00ffff)
	elif color == "red":
		rgbled(0x7f0000)
	elif color == "green":
		rgbled(0x007f00)
	elif color == "magenta":
		rgbled(0xff00ff)
	elif color == "yellow":
		rgbled(0xffff00)
	elif color == "white":
		rgbled(0xffffff)
	else:
		rgbled(0x000000)

# x = input value
# a = input range min
# b = input range max
# c = output range min
# d = output range max
def mapValueToRange(x, a, b, c, d):
	if x < a:
   		x = a
 	elif x > b:
   		x = b
 	value = (x-a) / (b-a) * (d-c) +c
 	return value

def getFromNVRAM(name):
	value = 0
	try:
	    value = nvs_get(name)
	except Exception as e:
	    print_exception(e)
	finally:
		return value

def setToNVRAM(name, value):
	try:
		nvs_set(name,value)
	except Exception as e:
		log("Utility: Writing value %d %s to NVRAM...FAILED" %(value, name))
		print_exception(e)
	else:
		log("Utility: Writing value %d %s to NVRAM...OK" %(value, name))


def setBootCountToNVRAM(value):
	try:
		nvs_set("bootcount",value)
	except Exception as e:
		log("Utility: Writing bootCount value %d to NVRAM...FAILED" %(value))
		print_exception(e)
	else:
		log("Utility: Writing bootCount value %d to NVRAM...OK" %(value))

def getBootCountFromNVRAM():
	try:
	    value = int(nvs_get("bootcount"))
	except Exception as e:
		print_exception(e)
		value = 0
	finally:
		return value

def setPin(pin,value):
	try:
		p_out = Pin(pin, mode=Pin.OUT)
		p_out.value(value)
		sleep_ms(100)
	except Exception as e:
		log("Utility: Pin %s state changing to %d failed" % (pin,value))
		print_exception(e)
	else:
		log("Utility: Pin %s state: %d " % (pin,value))

def changePin(pin,value):
	try:
		pin.value(value)
		sleep_ms(250)
	except Exception as e:
		log("Utility: Pin %s state changing to %d failed" % (pin,value))
		print_exception(e)
	else:
		log("Utility: Pin %s state: %d " % (pin,value))

def setPinHold(pin):
	try:
		pin.hold(True)
		sleep_ms(250)
	except Exception as e:
		log("Utility: Pin %s hold set failed" % pin)
		print_exception(e)
	else:
		log("Utility: Pin %s hold set" % pin)

def releasePinHold(pin):
	try:
		pin.hold(False)
		sleep_ms(250)
	except Exception as e:
		log("Utility: Pin %s hold release failed" % pin)
		print_exception(e)
	else:
		log("Utility: Pin %s hold released" % pin)

def getTime():
	dateArray = localtime()
	return "%02d-%02d-%02d %02d:%02d:%02d" % (dateArray[0],dateArray[1],dateArray[2],dateArray[3],dateArray[4],dateArray[5])

def getUTCTimeStamp():
	dateArray = localtime()
	return "%02d-%02d-%02dT%02d:%02d:%02dZ" % (dateArray[0],dateArray[1],dateArray[2],dateArray[3],dateArray[4],dateArray[5])

def isNaN(num):
    return num != num

def stddev(lst):
	mean = float(sum(lst)) / len(lst)
	return sqrt(sum((x - mean)**2 for x in lst) / len(lst))
