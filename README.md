# tequ-bee-nest-heater

Add Description here


## Hardware and connections

| Hardware               | Model         | Link          |
| -------------          |:-------------:| :-------------:| 
| Board                  | WiPy 3.0      | <a href="https://docs.pycom.io/datasheets/development/wipy3/">Link</a>|
| Power                  | 12 VDC 2A     | |
| Heater                 | 12 V 10 W     | <a href="https://www.partco.fi/fi/mekaniikka/kotelointi/kotelotarvikkeet/23244-lk12v-12w.html">Link</a>|
| DC/DC 4.5 -24 => 5 VDC | MEZD71202A-G  | <a href="https://www.mouser.fi/datasheet/2/277/mEZD71202A-1384003.pdf">Data sheet</a>|
| Heater control         | COM-12959     | <a href="https://www.sparkfun.com/products/12959">Link</a>|
| Temperature sensor     | DS18B20       | <a href="https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf">Data sheet</a>|
| Overheat protection    | 80-OHD5R-40B  | <a href="https://content.kemet.com/datasheets/KEM_SE0202_OHD.pdf">Data sheet</a>|

Connections

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

### 3. Install development environment

https://docs.pycom.io/gettingstarted/software/atom/

### 4 Open folder cloned from Git

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

### 8. Upload project to Wipy and test its working
 
### 9. Start developing!
 
