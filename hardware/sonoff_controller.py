import yaml
import time
from paho.mqtt import publish as mqtt_publish
from datetime import datetime

# Load config
with open("config/settings.yaml") as f:
    cfg = yaml.safe_load(f)

MQTT_HOST = cfg["sonoff"]["host"]
RELAY_MAP = cfg["sonoff"]["relays"]

_fan_state = None
_heater_state = None

# Validate configuration
VALID_RELAYS = {"fan", "heater"}
missing = VALID_RELAYS - set(RELAY_MAP.keys())
if missing:
    raise RuntimeError(f"Missing relay config(s): {missing}")


def control_relay(name: str, desired: str, force: bool = False):
    global _fan_state, _heater_state
    
    topic = RELAY_MAP.get(name)
    if not topic:
        raise ValueError(f"No topic defined for relay '{name}'")

    state_var = _fan_state if name == "fan" else _heater_state

    # Always re-send if forced or condition is still violated
    if force or desired != state_var:
        mqtt_publish.single(
            topic,
            desired,
            hostname=MQTT_HOST,
            port=1883,
            auth=None
        )
        print(f"{name.capitalize()} {desired} command sent")
        if name == "fan":
            _fan_state = desired
        else:
            _heater_state = desired
        time.sleep(0.3)

def is_night_time(): 
    hour = datetime.now().hour 
    return hour >= 19 or hour < 7

def fan_controller(humidity: float):
    global _fan_state

    if humidity > 54:
        desired = "ON"
    elif humidity <= 51:
        desired = "OFF"
    else:
        return

    # Redundancy: if humidity still wrong, force resend
    if humidity > 54 and _fan_state != "ON":
        control_relay("fan", "ON")
    elif humidity <= 51 and _fan_state != "OFF":
        control_relay("fan", "OFF")
    else:
        # Re-enforce every loop if out of bounds
        control_relay("fan", desired, force=True)


def heater_controller(temp: float):
    global _heater_state

    if is_night_time():
        min_temp, max_temp = 24, 26
    else:
        min_temp, max_temp = 26, 28

    if temp < min_temp:
        desired = "ON"
    elif min_temp < temp < max_temp:
        desired = "OFF"
    else:
        return

    if temp <= min_temp and _heater_state != "ON":
        control_relay("heater", "ON")
    elif min_temp <= temp < max_temp and _heater_state != "OFF":
        control_relay("heater", "OFF")
    else:
        # Re-enforce every loop if still not in correct range
        control_relay("heater", desired, force=True)
