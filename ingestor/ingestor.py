import paho.mqtt.client as mqtt
import json
from db import get_connection
from config import MQTT_HOST, MQTT_PORT


MEASURE_MSG_FIELDS_RULES = {
    "schema_version": {
        "type": str,
        "min_len": 1
    },
    "device_id": {
        "type": str,
        "min_len": 1
    },
    "sensor_type": {
        "type": str,
        "min_len": 1
    },
    "value": {
        "type": float,
    },
    "timestamp": {
        "type": int,
    },
    "message_seq": {
        "type": int,
        "optional": True
    },
    "unit": {
        "type": str,
        "optional": True
    }
}

STATUS_MSG_FIELDS_RULES = {
    "schema_version": {
        "type": str,
        "min_len": 1
    },
    "device_id": {
        "type": str,
        "min_len": 1
    },
    "sensor_type": {
        "type": str,
        "min_len": 1
    },
    "value": {
        "type": float,
    },
    "timestamp": {
        "type": int,
    },
    "message_seq": {
        "type": int,
        "optional": True
    },
    "unit": {
        "type": str,
        "optional": True
    }
}

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


def is_valid(data: dict, fields_rules: dict):

    for field, rules in fields_rules.items():
        is_optional = "optional" in rules.keys() and rules["optional"] == True

        # Sprawdzenie czy pole istnieje, pomiń jeśli jest opcjonalne
        if field not in data.keys() and not is_optional:
            return False
        
        # Sprawdzenie czy wartość pola posiada odpowiedni typ
        if field in data.keys() and not isinstance(data.get(field), rules["type"]):
            return False
        
    return True


def on_connect(client, userdata, flags, reason_code, props):
    print(f"Connected with result code {reason_code}")
    client.subscribe("lab/#")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
   
    if(is_valid(data, MEASURE_MSG_FIELDS_RULES)):
        store_measurement(msg.topic, data)    
    

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_HOST, MQTT_PORT)
mqtt_client.loop_forever()