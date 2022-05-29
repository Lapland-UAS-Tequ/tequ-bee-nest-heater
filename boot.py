# boot.py -- run on boot-up
from machine import WDT
wdt = WDT(timeout=90000)

from utility import log
import config
from utime import ticks_ms, ticks_diff, sleep_ms
from utility import log, releasePinHold, setPinHold, changePin, blinkLED, setPin, setLED, getYear
from pycom import heartbeat
from os import dupterm
from machine import UART, Pin
import WLANConnection
from sys import print_exception
from machine import reset_cause, wake_reason
from utility import setToNVRAM, getFromNVRAM, getBootCountFromNVRAM, setBootCountToNVRAM
import machine
import mqtt
import handleException
import data
import time
import utime
from ruuvitag.scanner import RuuviTagScanner
from machine import RTC

#import gc
#gc.enable()

config = config.config()
heartbeat(False)
uart = UART(0, 115200)
dupterm(uart)
log("Boot: Starting Bee-IoT-Heater-App-v1.0 (2022-05-27)...")

log("Set PIN P11 as relay control pin")
relay_pin = Pin("P11", Pin.IN)
log("Relay pin state: %d" % relay_pin())

#blinkLED("blue",250,1)

try:
    start = getFromNVRAM("error")
    bootCount = getBootCountFromNVRAM() + 1
    reset_cause = reset_cause()
    wake_reason = wake_reason()

    log("Boot: Reset cause: %s" % (reset_cause))
    log("Boot: Wake up reason: %s %s" % (wake_reason[0],wake_reason[1]))

    if(reset_cause == machine.PWRON_RESET):
        log("Boot: Forced system reset..(PWRON_RESET).")
        forced_reset = True
        bootCount = 1
    elif(reset_cause == machine.HARD_RESET):
        log("Boot: Forced system reset (HARD_RESET)....")
        forced_reset = True
        bootCount = 1
    elif(reset_cause == machine.WDT_RESET):
        log("Boot: Forced system reset (WDT_RESET)...")
        forced_reset = True
    elif(reset_cause == machine.DEEPSLEEP_RESET):
        log("Boot: Deepsleep reset, this is expected behaviour")
        forced_reset = False
    elif(reset_cause == machine.SOFT_RESET):
        log("Boot: SOFT Reset...")
    elif(reset_cause == machine.BROWN_OUT_RESET):
        log("Boot: Brown out reset...")
        forced_reset = True

    if wake_reason[0] == machine.PWRON_WAKE:
        log("Boot: Woke up by reset button")
    elif wake_reason[0] == machine.PIN_WAKE:
        log("Boot: Woke up by external pin (external interrupt)")
        read_sensors = True
    elif wake_reason[0] == machine.RTC_WAKE:
        log("Boot: Woke up by RTC (timer ran out)")
    elif wake_reason[0] == machine.ULP_WAKE:
        log("Boot: Woke up by ULP (capacitive touch)")
except Exception as e:
    print_exception(e)


log("Boot: bootCount: %d" % (bootCount))
setBootCountToNVRAM(bootCount)

start = start + 1
setToNVRAM("error",start)

if start >= 2:
    setToNVRAM("error",0)
    machine.deepsleep(5000)


wlan = WLANConnection.WLANConnection(config.getSSID(), config.getPassword())
log("Boot: Setting MAC address")
config.updateConfigValue("mqtt_device_id",wlan.getMACFlatten())
log("Boot: Configuring RTC...")
rtc = machine.RTC()

while getYear() == 1970:
    log("Boot: Syncing RTC...")
    rtc.ntp_sync("pool.ntp.org")
    utime.sleep_ms(1000)

setToNVRAM("error",0)

#blinkLED("green",250,1)
