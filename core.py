import time
import yaml
from sensors.temp_humidity import read_dht
from sensors.discovery import publish_discovery
from mqtt.publisher import publish
from hardware.sonoff_controller import fan_controller, heater_controller


def run():
    """
    Core MAWE loop: load config, publish discovery, and start sensor loop.
    """
    # Load config
    with open("config/settings.yaml") as f:
        cfg = yaml.safe_load(f)
    mqtt_conf = cfg["mqtt"]

    # 1) Publish Home Assistant Discovery configs once
    publish_discovery(mqtt_conf, base_topic="mawe/growtent")

    # 2) Main loop: read sensors, publish data, control fan
    while True:
        temp, hum = read_dht()
        if temp is not None and hum is not None:
            print(f"Temp: {temp} °C, Humidity: {hum}%")

            # Publish to HA
            publish("mawe/growtent/temp", temp, mqtt_conf)
            publish("mawe/growtent/humidity", hum, mqtt_conf)

            # Optional: control your Sonoff fan
            try:
                fan_controller(hum)
                heater_controller(temp)
            except Exception as e:
                print(f"Fan control error: {e}")
        else:
            print("Sensor read failed.")

        time.sleep(2)
