import ujson
from utility import log
from sys import print_exception
from utility import isNaN
from utility import getUTCTimeStamp

class DataStruct:

    payload = {}

    def __init__(self):
        log("Initializing data object...")
        self.resetPayload()

    def resetPayload(self):
        self.payload = {
            "d": {
                "1":{
                    "avg_t": {"v": float('nan')},
                    "relay": {"v": float('nan')},
                    "sp": {"v": float('nan')},
                    "mode": {"v": float('nan')},
                    "hyst": {"v": float('nan')},
                    "t_fail": {"v": float('nan')},
                    "t": {"v": float('nan')},
                    "cpu_t": {"v": float('nan')},
                    "ctrl_ok":{"v": float('nan')}
                }
            },
            "ts": ""
        }

    def createJSONDataPacket(self):
        data = self.payload
        data["ts"] = getUTCTimeStamp()
        self.resetPayload()
        return ujson.dumps(data)

    def updatePayloadValue(self, group, key, value):
        if type(value) == int or type(value) == float:
            current_value = self.payload["d"][group][key]["v"]
            if isNaN(current_value):
                new_value = value
            else:
                new_value = value
            self.payload["d"][group][key]["v"] = new_value
        else:
            log('The variable is not a number')

    def getLatestValue(self, group, key):
        return self.payload["d"][group][key]["v"]

    def getData(self):
        return self.payload

    def createRuuviTagPayload(self, ruuvitag,index):
        #id = ruuvitag["mac"].replace(":","")
        tagID = "rt%d" % (index+1)
        payload = {}
        payload["d"] = {}
        payload["d"][tagID] = {
                               "1": {"v": ruuvitag.temperature},
                               "2": {"v": ruuvitag.humidity},
                               "3": {"v": ruuvitag.pressure},
                               "4": {"v": ruuvitag.battery_voltage},
                               "5": {"v": ruuvitag.rssi}
        }
        payload['ts'] = getUTCTimeStamp()
        print(ujson.dumps(payload))
        return ujson.dumps(payload)
