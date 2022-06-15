import ujson
from utility import log
from sys import print_exception
from pycomMQTT import MQTTClient
import time
from machine import reset, deepsleep

class MQTTConnection:

    def __init__(self, config, data, relay):
        log("Initializing MQTT Connection...")
        # MQTT settings
        self.config = config
        self.data = data
        self.relay = relay

        self.deviceID = config.getConfigValue("mqtt_device_id")
        self.deviceType = config.getConfigValue("mqtt_device_type")
        self.orgID = config.getConfigValue("mqtt_org")
        self.url = config.getConfigValue("mqtt_url")
        self.dataTopic = config.getConfigValue("mqtt_data_topic")
        self.errorTopic = config.getConfigValue("mqtt_error_topic")
        self.configTopic = config.getConfigValue("mqtt_config_topic")

        self.user = config.getConfigValue("mqtt_user")
        self.authToken = config.getConfigValue("mqtt_authtoken")
        self.port = config.getConfigValue("mqtt_port")

        self.clientID = "d" + ":" + self.orgID + ":" + self.deviceType + ":" + self.deviceID

        print(self.deviceID)
        print(self.deviceType)
        print(self.orgID)
        print(self.url)
        print(self.dataTopic)
        print(self.errorTopic)
        print(self.configTopic)
        print(self.user)
        print(self.authToken)
        print(self.port)
        print(self.clientID)

        self.client = MQTTClient(client_id=self.clientID, server=self.url, user=self.user, password=self.authToken, port=self.port, keepalive=0,ssl=False, ssl_params={}, timeout=30)
        #client_id, server, port=0, user=None, password=None, keepalive=0,
        #                 ssl=False, ssl_params={}, timeout=30
        self.connected = False

        self.connect()

    def connect(self):
        log("Set MQTT message callback function...")
        self.client.set_callback(self.process_MQTT_command)
        log("Connecting MQTT client...")
        self.client.connect()

        topics = ["iot-2/cmd/configure/fmt/json",
                  "iot-2/cmd/relay_control/fmt/json",
                  "iot-2/cmd/send_config/fmt/json",
                  "iot-2/cmd/default_config/fmt/json",
                  "iot-2/cmd/control_mode/fmt/json",
                  "iot-2/cmd/softreboot/fmt/json",
                  "iot-2/cmd/deepsleep/fmt/json"
                  ]

        for value in topics:
            log("Subscribing to topic '%s'... " % value)
            self.client.subscribe(value)

        self.connected = True

    def checkNewMessages(self):
        self.client.check_msg()

    def pingServer(self):
        self.client.ping()

    def publishDataEvent(self, JSONMessage):
        #log("Publishing data message %s to topic: %s" % (JSONMessage, self.dataTopic))
        log("Publishing data message to topic: %s" % self.dataTopic)
        self.client.publish(topic=self.dataTopic, msg=JSONMessage, qos=1)

    def publishErrorEvent(self, JSONMessage):
        #log("Publishing error message %s to topic: %s" % (JSONMessage, self.errorTopic))
        log("Publishing error message to topic: %s" % self.errorTopic)
        self.client.publish(topic=self.errorTopic, msg=JSONMessage, qos=1)

    def publishConfigEvent(self, JSONMessage):
        #log("Publishing config message %s to topic: %s" % (JSONMessage, self.configTopic))
        log("Publishing config message to topic: %s" % self.configTopic)
        self.client.publish(topic=self.configTopic, msg=JSONMessage, qos=1)

    def publishRelayEvent(self):
        #log("Publishing config message %s to topic: %s" % (JSONMessage, self.configTopic))
        JSONMessage = ujson.dumps({"relay":1})
        log("Publishing event message to topic: %s" % "iot-2/evt/relay/fmt/json")
        self.client.publish(topic="iot-2/evt/relay/fmt/json", msg=JSONMessage, qos=1)

    def process_MQTT_command(self, topic, msg):
        message_value = msg.decode("utf-8")
        topic_name = topic.decode("utf-8")

        log("Message received!")
        log("Topic: %s | Value: %s" % (topic_name, message_value))

        values = topic_name.split("/")
        mqtt_command = values[2]

        if mqtt_command == "softreboot":
            log("Rebooting device...")
            reset()

        elif mqtt_command == "deepsleep":
            log("Going to deepsleep for 30 seconds...")
            deepsleep(30000)

        elif mqtt_command == "configure":
            json_message = ujson.loads(message_value)
            for key in json_message:
                log(key)
                log(json_message[key])
                self.config.updateConfigValue(key, json_message[key])
            self.config.updateConfig()
            self.publishConfigEvent(self.config.getCurrentConfigAsJSON())

        elif mqtt_command == "relay_control":
            log("Control value: %s" % message_value)

            if message_value == 1 or message_value == "1" or message_value == "ON" or message_value == "on" or message_value == "true":
                self.relay.setON()
            else:
                self.relay.setOFF()

        elif mqtt_command == "control_mode":
            log("Control value: %s" % message_value)

            if message_value == 1 or message_value == "1" or message_value == "ON" or message_value == "on" or message_value == "true":
                self.relay.setManualControl()
            else:
                self.relay.setAutomaticControl()

        elif mqtt_command == "send_config":
            self.publishConfigEvent(self.config.getCurrentConfigAsJSON())

        elif mqtt_command == "default_config":
            self.publishConfigEvent(self.config.getCurrentConfigAsJSON())
            time.sleep(1)
            self.config.createDefaultConfig()
            time.sleep(1)
            self.publishConfigEvent(self.config.getCurrentConfigAsJSON())
