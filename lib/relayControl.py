import ujson
from utility import log
from utility import setLED
from sys import print_exception
from machine import Pin


class RelayControl:

    def __init__(self, controlPin):
        self.PIN_ID = controlPin
        log("Using PIN %s as relay control pin" % self.PIN_ID)
        self.ctrl_pin = Pin(self.PIN_ID, Pin.OUT, value=0, pull=Pin.PULL_DOWN)
        self.control_mode = 0

    def setManualControl(self):
        log("Manual control mode activated..")
        self.control_mode = 1

    def setAutomaticControl(self):
        log("Automatic control mode activated..")
        self.control_mode = 0

    def getControl_mode(self):
        return self.control_mode

    def setON(self):
        log("Relay ON")
        self.ctrl_pin.value(1)

    def setOFF(self):
        log("Relay OFF")
        self.ctrl_pin.value(0)

    def getRelayState(self):
        relay_state = self.ctrl_pin.value()
        return relay_state
