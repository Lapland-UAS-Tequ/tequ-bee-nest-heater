try:
    #blinkLED("white",250,1)
    import tempReading
    tr = tempReading.tempReading(pwrPin="P10",owPin="P9")
    data = data.DataStruct()
    mqtt = mqtt.MQTTConnection(config, data, relay)
    exp = handleException.HandleException(mqtt)
except Exception as e:
    print_exception(e)
    relay.setOFF()

# Main program loop, this is repeated while program is running
while 1:
    try:
        # Read initial values
        start = time.ticks_ms()
        cpu_t = ((machine.temperature() - 32) / 1.8)

        if wlan.isWlanConnected():
            log("WLAN connection OK...")
        else:
            log("Main: WLAN connection is not OK... Connecting WLAN..")
            setLED("blue")
            log("Main: Set relay OFF...")
            relay.setOFF()
            wlan.connectWlan(30)

        # Read temperature sensor
        try:
            temperature = tr.readSingleDS18B20Sensor()
            avg_t = tr.getAverageTemperature()
            data.updatePayloadValue("1","t", temperature)
            data.updatePayloadValue("1","avg_t", avg_t)

            if avg_t == 85:
                t_sensor_failure = 1
            elif avg_t == -0.0625:
                t_sensor_failure = 1
            else:
                t_sensor_failure = 0
        except Exception as e:
            exp.handleException(e, "Temperature sensor is not connected or not working...", True, True, True, True)
            t_sensor_failure = 1

        try:
            # Temperature Control
            SP = config.getSP()
            CTRL_T = temperature

            lowLimit = config.getSP() - config.getHysteresis() + config.getConfigValue("hysteresis_low_offset")
            highLimit = config.getSP() + config.getHysteresis() + config.getConfigValue("hysteresis_high_offset")
            control_mode = relay.getControl_mode()
            current_relay_state = relay.getRelayState()

            log("Main: T: %.1f C | AVG: %.1f C | Setpoint: %.2f <> %.2f C <> %.2f  | Relay state: %d | Manual control: %d | T_fail: %d | CTRL_SIG: %d"
                % (temperature, avg_t, lowLimit, SP, highLimit, current_relay_state, control_mode, t_sensor_failure, control_signal_ok()))

            if t_sensor_failure:
                log("Main: Temperature sensor failure detected => Switch OFF heating.")
                setLED("yellow")
                relay.setOFF()

            elif control_mode:
                log("Main: Manual control mode activated")
                setLED("blue")

            else:
                if CTRL_T >= highLimit:
                    if current_relay_state == 1:
                        log("Main: Temperature is too high => Switch OFF heating.")
                        setLED("green")
                        relay.setOFF()
                        publish_data = True

                elif CTRL_T <= lowLimit:
                    if current_relay_state == 0:
                        log("Main: Temperature is too low => Switch ON heating.")
                        setLED("red")
                        #relay.setON()
                        mqtt.publishRelayEvent()
                        publish_data = True

            data.updatePayloadValue("1", "sp", config.getSP())
            data.updatePayloadValue("1", "hyst",config.getHysteresis())
            data.updatePayloadValue("1", "relay", relay.getRelayState())
            data.updatePayloadValue("1", "mode", relay.getControl_mode())
            data.updatePayloadValue("1", "t_fail", t_sensor_failure)
            data.updatePayloadValue("1", "cpu_t", cpu_t)
            data.updatePayloadValue("1", "ctrl_ok", control_signal_ok())
            log("Main: Datavalues updated...")
        except Exception as e:
            exp.handleException(e, "Temperature control failed...", True, True, True, True)

        try:
            log("Main: Checking MQTT...")
            mqtt.checkNewMessages()
            mqtt.pingServer()
        except Exception as e:
            exp.handleException(e, "Checking MQTT messages failed...", True, True, True, False)


        # Do @start
        if publish_data:
            try:
                log("Main: Something changed => Publish data.")
                mqtt.publishDataEvent(data.createJSONDataPacket())
                publish_data = False
            except Exception as e:
                exp.handleException(e, "Error in publishing data to MQTT...", True, True, True, False)

        elif count == 5:
            try:
                log("Main: Publish data count == 5.")
                mqtt.publishDataEvent(data.createJSONDataPacket())
            except Exception as e:
                exp.handleException(e, "Error in publishing data to MQTT...", True, True, True, False)

        # Send data every 10 cycles
        elif count % 10 == 0:
            try:
                log("Main: Publish data count == 10.")
                mqtt.publishDataEvent(data.createJSONDataPacket())
            except Exception as e:
                exp.handleException(e, "Error in publishing data to MQTT...", True, True, True, False)

        if count % 10 == 0:
            # Scan Ruuvitag sensors
            try:
                TIMEOUT = config.getTagHarvestingTimeout()
                tagnames = config.getTagNames()
                rts = RuuviTagScanner(tagnames)
                log("Main: Scanning ruuvitag sensors... TIMEOUT: %d seconds" % TIMEOUT)
                ruuvitags = rts.find_ruuvitags(timeout=config.getTagHarvestingTimeout())
                for ruuvitag in ruuvitags:
                    index = config.getTagIndex(ruuvitag.mac)
                    try:
                        ruuvitag_payload = data.createRuuviTagPayload(ruuvitag, index)
                        mqtt.publishDataEvent(ruuvitag_payload)
                    except Exception as e:
                        exp.handleException(e, "Error in publishing data to MQTT...", True, True, True, False)
            except Exception as e:
                exp.handleException(e, "Error in reading Ruuvitags...", True, True, True, False)

        # Sync time every 60 cycles
        if count % 60 == 0:
            try:
                rtc.ntp_sync("pool.ntp.org")
            except Exception as e:
                exp.handleException(e, "Error in updating time...", True, True, True, True)

    except Exception as e:
        exp.handleException(e, "Error in main loop...", True, True, True, True)

    finally:
        try:
            if exp.getExceptionCount() < 30:
                log("Main: Feeding watchdog | Exception count: %d " % exp.getExceptionCount())
                wdt.feed()
            else:
                log("Main: Exception count: %d => Do not feed WatchDog" % exp.getExceptionCount())

            delta = time.ticks_diff(time.ticks_ms(), start)
            if delta > 5000:
                timeToSleep = 0.001
            else:
                timeToSleep = (5000 - delta) / 1000

            log("Main: Executing program took %.3f seconds. Sleeping %.3f seconds...\n\n" % (delta / 1000, timeToSleep))
            count = count + 1
            time.sleep(timeToSleep)
        except Exception as e:
            print_exception(e)
            log("Main: Error in finally... deepsleep 10 seconds to reset...")
            machine.deepsleep(10000)
