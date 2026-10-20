import adafruit_dht
import board

# Single DHT22 on BCM21
dht_device = adafruit_dht.DHT22(board.D21, use_pulseio=False)

def read_dht():
    try:
        temp = dht_device.temperature
        humidity = dht_device.humidity
        if temp is not None and humidity is not None:
            return round(temp, 1), round(humidity, 1)
    except RuntimeError as e:
        print(f"Sensor read error: {e}")
    return None, None
