import ujson
from utility import log
from sys import print_exception
from machine import Pin
from onewire import DS18X20, OneWire
from utime import sleep_ms
from ubinascii import unhexlify, hexlify
from utility import stddev
from utility import blinkLED

class tempReading:

    def __init__(self, pwrPin, owPin):
        self.times = 3
        self.convertTime = 1250
        self.sleepTimeIfFailed = 500
        self.pwrPin = pwrPin
        self.owPin = owPin
        log("tempReading: init: Using PIN %s as 1-wire power pin and PIN %s as 1-wire bus pin" % (self.pwrPin,self.owPin))
        self.ow = OneWire(Pin(self.owPin))
        self.powerCtrl = Pin(self.pwrPin, mode=Pin.OUT, pull=Pin.PULL_DOWN)
        self.sensorRom = ""
        self.sensorFound = False
        self.enable1WireBusPower()
        self.scanBus()
        self.temperatureList = []

    def scanBus(self):
        while 1:
            roms = self.ow.scan()

            if len(roms) == 0:
                log("tempReading: scanBus: Nothing found, trying again...")
                self.disable1WireBusPower()
                self.enable1WireBusPower()
                sleep_ms(750)
                blinkLED("red",50,3)

            else:
                log("tempReading: scanBus: Scanning 1-wire bus %s and found: %s" % (self.owPin,hexlify(roms[0])))
                self.sensorRom = roms[0]
                self.sensorFound = True
                break



    def enable1WireBusPower(self):
        log("tempReading: enable1WireBusPower: Enabling 1-wire bus power...")
        self.powerCtrl(1)

    def disable1WireBusPower(self):
        log("tempReading: disable1WireBusPower: Disabling 1-wire bus power...")
        self.powerCtrl(1)

    def getAverageTemperature(self):
        dev = stddev(self.temperatureList)
        #log("tempReading: Standard deviation: %.2f" % dev)
        if len(self.temperatureList) >= 3:
            if(dev > 3):
                log("tempReading: Standard deviation is high => Remove min and max values from list.")
                print(self.temperatureList)
                max_value = max(self.temperatureList)
                max_index = self.temperatureList.index(max_value)
                self.temperatureList.pop(max_index)

                min_value = min(self.temperatureList)
                min_index = self.temperatureList.index(min_value)
                self.temperatureList.pop(min_index)
                print(self.temperatureList)

        return sum(self.temperatureList) / len(self.temperatureList)

    def addToTemperatureValuesList(self,value):
        if( len(self.temperatureList) == 10):
            #log("tempReading: addToTemperatureValuesList: List == 10 Pop and append")
            self.temperatureList.pop(0)
            self.temperatureList.append(value)
        else:
            #log("tempReading: addToTemperatureValuesList: Append to list")
            self.temperatureList.append(value)

    def readSingleDS18B20Sensor(self):
        i=0
        while i<3:
            t = DS18X20(self.ow)
            #log("tempReading: readSingleDS18B20Sensor: Send ConvertT to 1-wire bus %s" %(self.owPin))
            t.start_conversion(self.sensorRom)
            sleep_ms(self.convertTime)
            temperature = t.read_temp_async(self.sensorRom)

            i=i+1

            if temperature >= 60:
                self.disable1WireBusPower()
                self.enable1WireBusPower()
            else:
                break


        self.addToTemperatureValuesList(temperature)
        return temperature
