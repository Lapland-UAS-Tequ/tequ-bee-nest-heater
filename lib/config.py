import ujson
from utility import log
from sys import print_exception


class config:
    settings = {}

    def __init__(self):
        log("Initializing configuration file")
        self.loadConfig()

    def loadConfig(self):
        try:
            log("Loading config file...")
            file = open('config.json')
            self.settings = ujson.loads(file.read())
            file.close()
        except Exception as e:
            log("Loading config file... FAILED.. Creating default config..")
            print_exception(e)
            self.createDefaultConfig()
        finally:
            log(self.settings)

    def updateConfig(self):
        try:
            log("Updating config file...")
            file = open('config.json', mode='w')
            file.write(ujson.dumps(self.settings))
            file.close()
        except Exception as e:
            log("Updating config file... FAILED..")
            print_exception(e)
            self.createDefaultConfig()
        finally:
            log(self.settings)

    def createDefaultConfig(self):
        # original values
        log("Falling back to default config...")
        value = {
          "ssid": "eyesonhives",
          "password": "beewatch",
          "ruuvitags": ["ed:08:70:12:55:9d","f8:28:d4:94:6d:22", "f8:28:d4:94:6d:22"],
          "setpoint": 30,
          "hysteresis": 0.25,
          "hysteresis_low_offset": 0.25,
          "hysteresis_high_offset": 0.0,
          "ruuvitag_timeout": 5000,
          "control_parameter_key":"t",
          "control_parameter_group":"1",
          "mqtt_user":"use-token-auth",
          "mqtt_authtoken":"",
          "mqtt_port":1883,
          "mqtt_url":"i5u4t3.messaging.internetofthings.ibmcloud.com",
          "mqtt_org":"i5u4t3",
          "mqtt_device_id":"MAC",
          "mqtt_device_type":"bee-iot",
          "mqtt_data_topic":"iot-2/evt/data/fmt/json",
          "mqtt_error_topic":"iot-2/evt/error/fmt/json",
          "mqtt_config_topic":"iot-2/evt/config/fmt/json"
        }

        self.settings = value
        file = open('config.json', mode='w')
        file.write(ujson.dumps(value))
        file.close()

    def updateConfigValue(self, parameter, value):
        log("Parameter %s and value: %s => Updating parameter..." % (parameter, value))
        self.settings[parameter.lower()] = value

    def getConfigValue(self, name):
        return self.settings[name]

    def getSSID(self):
        return self.settings["ssid"]

    def getPassword(self):
        return self.settings["password"]

    def getTagNames(self):
        encoded_tag_names = []
        for ruuvitag in self.settings["ruuvitags"]:
            print(ruuvitag)
            encoded_tag_names.append(ruuvitag.encode('UTF-8'))
        return encoded_tag_names

    def getTagIndex(self,tag):
        return self.settings["ruuvitags"].index(tag)

    def getTagHarvestingTimeout(self):
        return self.settings["ruuvitag_timeout"]

    def getCurrentConfigAsJSON(self):
        return ujson.dumps(self.settings)

    def getSP(self):
        return self.settings["setpoint"]

    def getHysteresis(self):
        return self.settings["hysteresis"]

    def getControlParameterKey(self):
        return self.settings["control_parameter_key"]

    def getControlParameterGroup(self):
        return self.settings["control_parameter_group"]
