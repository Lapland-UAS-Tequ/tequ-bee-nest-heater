import ujson
from utility import log
from utility import setLED
from sys import print_exception
from machine import Pin


class RelayControl:

    def __init__(self, controlPin):
        self.PIN_ID = controlPin
        log("RelayControl: Using PIN %s as relay control pin" % self.PIN_ID)
        self.ctrl_pin = Pin(self.PIN_ID, Pin.OUT, value=0, pull=Pin.PULL_DOWN)
        self.setAutomaticControl()
        self.setOFF()
        self.getRelayState()

    def setManualControl(self):
        log("RelayControl: Manual control mode activated..")
        self.control_mode = 1

    def setAutomaticControl(self):
        log("RelayControl: Automatic control mode activated..")
        self.control_mode = 0

    def getControl_mode(self):
        return self.control_mode

    def setON(self):
        log("RelayControl: Relay ON")
        self.ctrl_pin.value(1)

    def setOFF(self):
        log("RelayControl: Relay OFF")
        self.ctrl_pin.value(0)

    def getRelayState(self):
        relay_state = self.ctrl_pin.value()
        log("RelayControl: Relay state: %d" % relay_state)
        return relay_state
