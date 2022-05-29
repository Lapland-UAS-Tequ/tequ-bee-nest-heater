#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Class for WLANConnection
"""

from utility import log
from utility import blinkLED
from utime import sleep_ms
from ubinascii import unhexlify, hexlify
from network import WLAN
import machine


class WLANConnection:

    def __init__(self, ssid, password):
        log('WLANConnection: Initializing...')
        self.wlan = WLAN(mode=WLAN.STA)
        log('WLANConnection: Setting auth...')
        self.SSID = ssid
        self.password = password
        self.mac = hexlify(machine.unique_id(), ':').decode()
        log('WLANConnection: MAC ADDRESS: %s' % self.mac)

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
        mac_string = mac_string.replace(':', '')
        return mac_string

    def connectWlan(self, times_to_try):
        i = 1
        times_to_try = times_to_try
        backup = False
        while 1:
            if i > 9 and i < 13:
                log('WLANConnection: Try backup connection...')
                self.wlan.connect(ssid='tequ-daq-2.4G',
                                  auth=(WLAN.WPA2, 'Tequwlan!'))
                backup = True
            else:
                self.wlan.connect(ssid=self.SSID, auth=(WLAN.WPA2,
                                  self.password))
                backup = False

            log('WLANConnection: Waiting 10 seconds for connection to establish...')
            sleep_ms(10000)

            if self.wlan.isconnected():
                log('WLANConnection: Connection...OK')
                break
            elif i >= times_to_try:
                log('WLANConnection: Connection...FAILED')
                break
            else:
                if backup:
                    log('WLANConnection: Connecting to backup SSID %s... %d / %d'
                        % ('tequ-daq-2.4G', i, times_to_try))
                    i = i + 1
                else:
                    log('WLANConnection: Connecting to %s... %d / %d'
                        % (self.SSID, i, times_to_try))
                    i = i + 1

    def isWlanConnected(self):
        return self.wlan.isconnected()
