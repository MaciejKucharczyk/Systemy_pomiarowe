import os

MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_NAME = "abcd_db"
DB_USER = "admin"
DB_PASSWORD = "admin_pass1234"