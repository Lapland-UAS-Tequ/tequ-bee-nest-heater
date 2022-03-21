"""
Class for WLANConnection
"""
from utility import log
from utime import sleep_ms
from ubinascii import unhexlify, hexlify
from network import WLAN
import machine

class WLANConnection:
    def __init__(self, ssid, password):
        log("WLANConnection: Initializing...")
        self.wlan = WLAN(mode=WLAN.STA)
        log("WLANConnection: Setting auth...")
        self.SSID = ssid
        self.password = password
        self.mac = hexlify(machine.unique_id(),':').decode()
        log("WLANConnection: MAC ADDRESS: %s" % self.mac)
        self.connectWlan()

    def closeWlan(self):
        try:
            self.wlan.disconnect()
            self.wlan.deinit()
        except:
            pass

    def getMAC(self):
        return self.mac

    def getMACFlatten(self):
        mac_string = self.mac
        mac_string = mac_string.replace(":","")
        return mac_string

    def connectWlan(self):
        i = 1
        times_to_try = 5

        while 1:
            log("WLANConnection: Connecting to %s... %d / %d" % (self.SSID, i, times_to_try))
            self.wlan.connect(ssid=self.SSID, auth=(WLAN.WPA2, self.password))
            sleep_ms(10000)

            if self.wlan.isconnected():
                log("WLANConnection: Connection...OK")
                break
            elif i >= times_to_try:
                log("WLANConnection: Connection...FAILED")
                break
            else:
                i = i +1
