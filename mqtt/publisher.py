# mqtt/publisher.py

import paho.mqtt.client as mqtt

def publish(topic: str, payload, config: dict):
    """
    Connects to the broker, publishes one message, then disconnects.
    Expects config keys: host (str), port (int), optional username (str) and password (str).
    """
    client = mqtt.Client()
    user = config.get("username", "")
    pwd  = config.get("password", "")
    if user:
        client.username_pw_set(user, pwd)

    # This will raise if it can’t connect
    client.connect(config["host"], config["port"])
    # You might want to set QoS, retain, etc. here
    client.publish(topic, payload)
    client.disconnect()
