import paho.mqtt.client as mqtt
import json
from db import get_connection
from config import MQTT_HOST, MQTT_PORT

def store_measurement(topic, data: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO measurements (group_id, device_id, sensor, value, unit, ts_ms, seq, topic)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    data.get("group_id"),
                    data.get("device_id"),
                    data.get("sensor_type"),
                    data.get("value"),
                    data.get("unit"),
                    data.get("timestamp"),
                    data.get("message_seq"),
                    topic
                ))
    conn.commit()
    cur.close()
    conn.close()


def is_valid(data: dict):
    req_fields = [
        "schema_version",
        "device_id",
        "sensor_type",
        "value",
        "timestamp",
        "message_seq"
    ]
    opt_fields = [
        "unit",
        "message_req"
    ]

    for key in req_fields:
        if key not in data.keys():
            return False
        
    return True


def on_connect(client, userdata, flags, reason_code, props):
    print(f"Connected with result code {reason_code}")
    client.subscribe("lab/#")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    store_measurement(msg.topic, data)
    

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_HOST, MQTT_PORT)
mqtt_client.loop_forever()