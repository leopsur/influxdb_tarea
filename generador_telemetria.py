import time
import random
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

URL = "http://localhost:8181"
TOKEN = "admin" # No importa el token con --without-auth
ORG = "IABD"
DATABASE = "trafico_raw"

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

print(" Generador enviando datos a InfluxDB 3.0 (Puerto 8181)...")

dispositivos = [{"name": "router1", "base_lat": 15.0}, {"name": "router2", "base_lat": 25.0}]

try:
    while True:
        for dev in dispositivos:
            traffic_in = round(random.uniform(50.0, 500.0), 2)
            traffic_out = round(random.uniform(20.0, 300.0), 2)
            latency = round(random.gauss(dev["base_lat"], 4.0), 2)
            
            if random.random() < 0.08: # Anomalía de latencia
                latency += round(random.uniform(35.0, 75.0), 2)

            point = Point("red") \
                .tag("device", dev["name"]) \
                .field("traffic_in", traffic_in) \
                .field("traffic_out", traffic_out) \
                .field("latency", latency)

            write_api.write(bucket=DATABASE, record=point)
            print(f"[{dev['name']}] IN={traffic_in} | OUT={traffic_out} | Latencia={latency}")
        time.sleep(2)
except KeyboardInterrupt:
    client.close()
