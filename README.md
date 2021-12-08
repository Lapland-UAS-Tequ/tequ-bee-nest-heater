# tequ-bee-nest-heater
 
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


### 4. Find out WiPy board unique ID 

- Open Atom
- Connect WiPy with USB-cable
- Open terminal 
- Run following code

```
import machine
machine.unique_id()
```

Remove ':' from ID and save it.

### 5. Register device to Tequ´s IBM Cloud Watson IoT Platform

https://i5u4t3.internetofthings.ibmcloud.com/dashboard/

Device Type = bee-iot
Device ID = use unique id
mqtt_authtoken = generate randomly

Add generated token to config.json <MQTT AUTH TOKEN>
 
### 6. Update firmware


 
 






