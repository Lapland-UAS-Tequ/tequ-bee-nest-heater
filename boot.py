# boot.py -- run on boot-up
from machine import WDT
wdt = WDT(timeout=90000)
import relayControl
from machine import UART, Pin
#relay = relayControl.RelayControl("P11")
relay = relayControl.RelayControl("P11")
relay.setOFF()
control_signal_ok = Pin("P12", Pin.IN)
count = 1
t_sensor_failure = 0
temperature = 999
avg_t = 999
publish_data = False
start = 0
sync_loop = 0

from utility import log
import config
from utime import ticks_ms, ticks_diff, sleep_ms
from utility import log, releasePinHold, setPinHold, changePin, blinkLED, setPin, setLED, getYear
from pycom import heartbeat
from os import dupterm

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
log("Boot: Starting Bee-IoT-Heater-App-v1.0 (2022-06-10)...")

blinkLED("blue",250,1)

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
wlan.connectWlan(30)


log("Boot: Configuring RTC...")
rtc = machine.RTC()

while getYear() == 1970 and sync_loop < 5:
    log("Boot: Syncing RTC...")
    rtc.ntp_sync("pool.ntp.org")
    utime.sleep_ms(1000)
    sync_loop = sync_loop + 1

setToNVRAM("error",0)

#blinkLED("green",250,1)
