# sensors/discovery.py

import json
from mqtt.publisher import publish

def publish_discovery(mqtt_conf: dict, base_topic: str = "mawe/growtent"):
    """
    Publish MQTT-Discovery config messages for DHT22 temperature & humidity sensors.
    Uses retained messages so Home Assistant will auto-create entities.
    """
    DISCOVERY_PREFIX = "homeassistant"

    # Temperature sensor config
    temp_cfg = {
        "name": "Grow Tent Temperature",
        "state_topic": f"{base_topic}/temp",
        "unit_of_measurement": "°C",
        "value_template": "{{ value | float }}",
        "unique_id": "mawe_growtent_temp",
    }
    publish(
        f"{DISCOVERY_PREFIX}/sensor/mawe_temp/config",
        json.dumps(temp_cfg),
        {**mqtt_conf, "retain": True}
    )

    # Humidity sensor config
    hum_cfg = {
        "name": "Grow Tent Humidity",
        "state_topic": f"{base_topic}/humidity",
        "unit_of_measurement": "%",
        "value_template": "{{ value | float }}",
        "unique_id": "mawe_growtent_hum",
    }
    publish(
        f"{DISCOVERY_PREFIX}/sensor/mawe_hum/config",
        json.dumps(hum_cfg),
        {**mqtt_conf, "retain": True}
    )
