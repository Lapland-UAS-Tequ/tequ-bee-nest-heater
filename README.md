# tequ-bee-nest-heater

This is repository of bee nest heater prototype developed in Arctic Beekeeping project. Prototype is developed for Pycom WiPy 3.0 development board and each prototype can control 12 V heating of single bee nest. Heating plate is equipped with 2 x 10 W @12 VDC heating elements, thermal guard and temperature sensor for thermostat control. Each prototype uses WLAN to connect to internet. Prototype connects to Tequ´s Watson IoT Platform via MQTT and sensor data is delivered to cloud in real-time. Each unit is also remote controllable via MQTT connection. It is possible to connect three Ruuvitag sensors to each unit. Ruuvitag data is collected and forwarded to Watson IoT. Collected sensor data can be found and accessed using Datatool, Databrowser or Tequ-AI found from https://dash.tequ.fi.

## Hardware 
List of the hardware used in prototype

| Hardware               | Model         | Placement       | Link          |
| -------------          |:-------------:| :-------------: | :-------------:| 
| Board                  | WiPy 3.0      | Control box     | <a href="https://docs.pycom.io/datasheets/development/wipy3/">Link</a>|
| Solar power system     | 12 VDC 20A    | External        | |
| Heater                 | 12 V 10 W     | Heater unit     | <a href="https://www.partco.fi/fi/mekaniikka/kotelointi/kotelotarvikkeet/23244-lk12v-12w.html">Link</a>|
| DC/DC 4.5 -24 => 5 VDC | MEZD71202A-G  | Control box     | <a href="https://www.mouser.fi/datasheet/2/277/mEZD71202A-1384003.pdf">Data sheet</a>|
| Heater control         | COM-12959     | Control box     | <a href="https://www.sparkfun.com/products/12959">Link</a>|
| Temperature sensor     | DS18B20       | Heater unit     | <a href="https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf">Data sheet</a>|
| Thermal guard          | 80-OHD5R-40B  | Heater unit     | <a href="https://content.kemet.com/datasheets/KEM_SE0202_OHD.pdf">Data sheet</a>|
| Power input            | CA 3 GS       | Control box     | <a href="https://catalog.belden.com/techdata/EN/CA3GS_techdata.pdf">Data sheet</a>|
| Power output           | CA 3 GD       | Control box     | <a href="https://catalog.belden.com/techdata/EN/CA3GD_techdata.pdf">Data sheet</a>|
| Heater input           | CA 6 GD       | Control box     | <a href="https://catalog.belden.com/techdata/EN/CA6GD_techdata.pdf">Data sheet</a>|

## Connections 
Connections of the hardware used in prototype.
| Device                 | PIN           | Device         | PIN            |
| -------------          |:-------------:| :-------------:| :-------------:| 
| WiPy 3.0               | Vin           |  DC/DC         | Vout           |
| WiPy 3.0               | GND           |  POWER         | GND            |
| WiPy 3.0               | P9            |  DS18B20       | Data           |
| WiPy 3.0               | P10           |  DS18B20       | 5V             |
| WiPy 3.0               | P11           |  80-OHD5R-40B  | INPUT          |
| WiPy 3.0               | P12           |  COM-12959     | GATE           |
| 80-OHD5R-40B           | OUTPUT        |  COM-12959     | GATE           |
| COM-12959              | DRAIN         |  HEATER        | GND            |
| COM-12959              | SOURCE        |  POWER         | GND            |
| HEATER                 | 12 VDC        |  POWER         | 12 VDC         | 
| DCDC                   | Vin           |  POWER         | 12 VDC         | 

## Connectors pin order

**7-PIN connector CA 6**

This connector is for connecting heating element to control box.

Use cable with 7 x 0.5 mm2 conductors.

| PIN #                  | PIN                  | PIN                        | 
| -------------          |:-------------:       |:-------------:             |
| PIN 1                  | 12 V                 | 12 V for heating           | 
| PIN 2                  | HEATER GND           | GND thermostat controlled  | 
| PIN 3                  | DS18B20 5V           | 1-wire bus 5V line         |  
| PIN 4                  | DS18B20 GND          | 1-wire bus ground          |  
| PIN 5                  | DS18B20 DATA         | 1-wire bus data line       |  
| PÍN 6                  | 80-OHD5R-40B INPUT   | heating control signal in  |  
| PIN 7                  | 80-OHD5R-40B OUTPUT  | heating control signal out |  

**4-PIN connector CA 3**

This connector is used to deliver external power to system. External power can be sourced for example from 12 VDC solar power system.

Use cable with 4 x 1.5 mm2 or 4 x 2.5 mm2 to allow multiple heating units to be chained.

| PIN #                  | PIN                  | PIN           | 
| -------------          |:-------------:       |:-------------:|
| PIN 1                  | 12 V                 | 12 V input    | 
| PIN 2                  | GND                  | GND           | 
| PIN 3                  | 12 V                 | 12 V input    |  
| PIN 4                  | GND                  | GND           |  



## Remote control via MQTT commands and topics
Unit regularly checks following MQTT topics for incoming commands.
  
| TOPIC / COMMAND                         | Purpose                                          | Example payload   | 
| -------------                           |:-------------:                                   | :-------------:   | 
| iot-2/cmd/configure/fmt/json            | Change one or multiple config value              |  {"setpoint":25, "hysteresis":1} | 
| iot-2/cmd/relay_control/fmt/json        | Set relay ON/OFF (works only if manual mode)     |  0 or 1  | 
| iot-2/cmd/send_config/fmt/json          | Request current config from unit                 |  {}      | 
| iot-2/cmd/default_config/fmt/json       | Reverts back to default config                   |  {}      | 
| iot-2/cmd/control_mode/fmt/json         | Change control mode (automatic=0, manual=1)      |  0 or 1  | 
| iot-2/cmd/softreboot/fmt/json           | Reset device                                     |  {}      | 
| iot-2/cmd/deepsleep/fmt/json            | Activate deepsleep for 30 seconds                |  {}      | 
  
Example MQTT control & monitoring application is available at https://tequ.dy.fi/#!/6 & https://tequ.dy.fi/red

## Development

### 1. Clone this repository
```
git clone https://github.com/Lapland-UAS-Tequ/tequ-bee-nest-heater.git
```

### 2. Create config.json file to local directory

```
{
  "ssid": "eyesonhives",
  "password": "beewatch"
  "ruuvitags": ["ed:08:70:12:55:9d","f8:28:d4:94:6d:22", "f8:28:d4:94:6d:22"],
  "setpoint": 30,
  "hysteresis": 0.25,
  "hysteresis_low_offset": 0.25,
  "hysteresis_high_offset": 0.0,
  "ruuvitag_timeout": 5,
  "control_parameter_key":"t",
  "control_parameter_group":"1",
  "mqtt_user":"use-token-auth",
  "mqtt_authtoken":"<MQTT AUTH TOKEN>",
  "mqtt_port":1883,
  "mqtt_url":"i5u4t3.messaging.internetofthings.ibmcloud.com",
  "mqtt_org":"i5u4t3",
  "mqtt_device_id":"MAC",
  "mqtt_device_type":"bee-iot",
  "mqtt_data_topic":"iot-2/evt/data/fmt/json",
  "mqtt_error_topic":"iot-2/evt/error/fmt/json",
  "mqtt_config_topic":"iot-2/evt/config/fmt/json"
}
```
- ssid = SSID of local Wifi access point
- password = wifi password
- ruuvitags = list of ruuvitag sensors which data should be collected and forwarded to Watson IoT (max 3)
- setpoint = Target temperature for thermostat control
- hysteresis = allowed fluctuation of temperature during control
- hysteresis_low_offset = offset for more precise control of lower level hysteresis 
- hysteresis_high_offset = offset for more precise control of high level hysteresis 
- ruuvitag_timeout = seconds how long to listen incoming ruuvitag broadcasts
- control_parameter_key = t (do not change, for future purposes)
- control_parameter_group = 1 (do not change, for future purposes)
- mqtt_user = user name for MQTT  
- mqtt_authtoken = auth token for MQTT
- mqtt_port = MQTT server port
- mqtt_url = MQTT server url
- mqtt_device_id = automatically detected from Pycom board, must match registered device in MQTT server
- mqtt_device_type = registered device type 
- mqtt_data_topic = topic to send data events (sensor data)
- mqtt_error_topic = topic to send error messages
- mqtt_config_topic = topic to send device config

### 3. Install development environment

https://docs.pycom.io/gettingstarted/software/atom/

### 4 Open folder cloned from Git in development environment

### 5. Find out WiPy board unique ID 

- Connect WiPy with USB-cable
- Open terminal 
- Run following code

```
import machine
machine.unique_id()
```

Remove ':' from ID and save it.

### 6. Register device to Tequ´s IBM Cloud Watson IoT Platform

https://i5u4t3.internetofthings.ibmcloud.com/dashboard/

Device Type = bee-iot
Device ID = use unique id
mqtt_authtoken = generate randomly

Add generated token to config.json <MQTT AUTH TOKEN>
 
### 7. Update WiPy firmware

https://docs.pycom.io/updatefirmware/

### 8. Build connections
  
### 9. Upload project to Wipy and test its working
   
### 10. Start developing!
