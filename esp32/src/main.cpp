#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "secrets.h"
#include <map>
#include <DallasTemperature.h>

#define TEMP_DS18B20_PIN 4

WiFiClient espClient;
PubSubClient mqttClient(espClient);

OneWire oneWire(TEMP_DS18B20_PIN);
DallasTemperature sensors(&oneWire);

String deviceId;
String topic;

int tempCounter = 0;
int humCounter = 0; 
int pressCounter = 0;

String generateDeviceIdFromEfuse()
{
  uint64_t chipId = ESP.getEfuseMac();
  char id[32];
  snprintf(id, sizeof(id), "esp32-%04X%08X",
           (uint16_t)(chipId >> 32),
           (uint32_t)chipId);
  return String(id);
}

float get_temperature()
{
  sensors.requestTemperatures();
  float temp_c = sensors.getTempCByIndex(0);
 
  if(temp_c == DEVICE_DISCONNECTED_C) {
     Serial.print("[ERROR] Brak odczytu temperatury");
    return NAN;
  }
  Serial.print("Odczyt temperatury: ");
  Serial.print(temp_c);
  Serial.println(" C");
  return temp_c;
}

void connectWiFi()
{
  Serial.print("Laczenie z Wi-Fi: ");
  Serial.println(WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Polaczono z Wi-Fi");
  Serial.print("Adres IP: ");
  Serial.println(WiFi.localIP());
}
void connectMQTT()
{
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);
  while (!mqttClient.connected())
  {
    Serial.print("Laczenie z MQTT...");
    if (mqttClient.connect(deviceId.c_str()))
    {
      Serial.println("OK");
    }
    else
    {
      Serial.print("blad, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" - ponowna proba za 2 s");
      delay(2000);
    }
  }
}

void publishMeasurement(String topic, String label, float value, int precision, String unit, int counter)
{
  JsonDocument doc;
  doc["schema_version"] = "1.0";
  doc["device_id"] = deviceId;
  doc["sensor_type"] = label;
  doc["value"] = value;
  doc["unit"] = unit;
  doc["timestamp"] = millis();
  doc["message_seq"] = counter;
  char payload[256];
  serializeJson(doc, payload);
  mqttClient.publish(topic.c_str(), payload);
  Serial.print("Publikacja na topic: ");
  Serial.println(topic.c_str());
  Serial.println(payload);
}

void publishStatus(String sensor_type, String status, String message)
{ 
  JsonDocument doc;
  doc["schema_version"] = "1.0";
  doc["device_id"] = deviceId;
  doc["sensor_type"] = sensor_type;
  doc["status"] = status;
  doc["message"] = message;
  doc["code"] = 123;
  doc["timestamp"] = millis();

  String topic = topic + "/status/" + status;
  char payload[256];
  serializeJson(doc, payload);
  mqttClient.publish(topic.c_str(), payload);
  Serial.print("Publikacja na topic: ");
  Serial.println(topic);
  Serial.println(payload);
}

void processMeasurement(float temp, float hum, float pres)
{ 
  String errorType = "Nan value";
  // Walidacja
  if(!isnan(temp))
  {
    tempCounter+=1;
    publishMeasurement("lab/g2/esp/temperature", "temperature", temp, 2, " C", tempCounter);
    // publishStatus("temperature", "SUCCESS", "");
  }
  else 
  {
    // publishStatus("temperature", "ERROR: " + errorType, "[ERROR] Blad odczytu danych z czujnika");
  }

  return;
  if(!isnan(hum))
  {
    humCounter+=1;
    publishMeasurement(topic + "/humidity",  "humidity",    hum, 1, " %", humCounter);
    publishStatus("humidity", "SUCCESS", "");
  }
  else
  {
    publishStatus("humidity", "ERROR: " + errorType, "[ERROR] Blad odczytu danych z czujnika");
  }

  if(!isnan(pres))
  {
    pressCounter+=1;
    publishMeasurement(topic + "/pressure", "pressure",    pres, 0, " hPa", pressCounter);
    publishStatus("pressure", "SUCCESS", "");
  }
  else
  {
    publishStatus("pressure", "ERROR: " + errorType, "[ERROR] Blad odczytu danych z czujnika");
  }
  
}

void setup()
{
  Serial.begin(115200);
  delay(1000);
  deviceId = generateDeviceIdFromEfuse();
  // topic = "lab/" + String(MQTT_GROUP) + "/" + deviceId + "/temperature";
  topic = "lab/" + String(MQTT_GROUP) + "/" + deviceId;
  Serial.print("Device ID: ");
  Serial.println(deviceId);
  connectWiFi();
  connectMQTT();
}

void loop()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    connectWiFi();
  }
  if (!mqttClient.connected())
  {
    connectMQTT();
  }
  float temp_raw = get_temperature();
  mqttClient.loop();
  processMeasurement(temp_raw, 0, 0);
  delay(5000);
}