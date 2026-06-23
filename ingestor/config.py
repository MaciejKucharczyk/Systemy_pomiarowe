import os

MQTT_HOST = os.getenv("MQTT_HOST", "127.0.0.1")
MQTT_PORT = os.getenv("MQTT_PORT", 1883)

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASS", "admin_pass1234")
DB_NAME = os.getenv("DB_NAME", "abcd_db")