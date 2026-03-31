# Struktura topiców
## Wiadomości pomiarowe
```lab/<group_id>/<device_id>/<sensor_type>``` 

### Pola
```lab``` - obszar główny projektu

```group_id``` - numer grupy laboratoryjnej

``` device_id``` - ciąg identyfikacyjny urządzenia (UUID)

```sensor_type``` - rodzaj sensora (wielkość mierzona)

### Przykłady
```
lab/g03/esp-gt3l13324/temperature
lab/g03/esp-gt3l13324/humidity
lab/g03/esp-gt3l13324/pressure
```
## Wiadomości statusowe
```lab/<group_id>/<device_id>/status/<status_type>``` 

### Pola
```lab``` - obszar główny projektu

```group_id``` - numer grupy laboratoryjnej

``` device_id``` - ciąg identyfikacyjny urządzenia (UUID)

```status_type``` - status (success, error, info)
s
### Przykłady
```
lab/g03/esp-gt3l13324/status/success
lab/g03/esp-gt3l13324/status/error
```

# Struktura JSON
## Wiadomości pomiarowe
```json
{
    "schema_version": "1.0",
    "device_id": "esp-gt3l13324",
    "sensor_type": "temperature",
    "value": 23.5,
    "unit": "C",
    "timestamp": 2345633663,
    "message_seq": 12
}
```

### Pola wymagane
```schema_version``` - wersja struktury JSON

```device_id``` - ciąg identyfikacyjny urządzenia (UUID)

```sensor_type``` - rodzaj sensora (wielkość mierzona)

```value``` - wartość pomiaru

```timestamp``` - znacznik czasu

### Pola opcjonalne
```unit``` - jednostka mierzonej wielkości

```message_seq``` - numer sekwencyjny wiadomości

### Reguły walidacji
#### Pola wymagane
```schema_version``` - musi być nie pustym ciągiem znaków

```device_id``` - musi być nie pustym ciągiem znaków

```sensor_type``` - musi być nie pustym ciągiem znaków

```value``` - musi być liczbą zmiennoprzecinkową

```timestamp``` - musi być dodatnią liczbą całkowitą

#### Pola opcjonalne

```unit``` - musi być ciągiem znaków odpowiednim dla danego sensora

```message_seq``` - musi być dodatnią liczbą całkowitą

### Przykłady
#### Wiadomość poprawna
```json
{
    "schema_version": "1.0",
    "device_id": "esp-gt3l13324",
    "sensor_type": "temperature",
    "value": 23.5,
    "unit": "C",
    "timestamp": 2345633663,
    "message_seq": 12
}
```

#### Wiadomości błędne
```json
{
    "schema_version": "1.0",
    "device_id": "esp-gt3l13324",
    "sensor_type": "temperature",
    "value": 23.5,
    "timestamp": 2345633663,
    "message_seq": 12
}
```
    Błąd: Brak pola 'unit' przy pomiarze wielkości z jednostką

---
```json
{
    "schema_version": "1.0",
    "device_id": "esp-gt3l13324",
    "sensor_type": "",
    "value": 23.5,
    "timestamp": 2345633663,
    "message_seq": 12
}
```
    Błąd: Pole 'sensor_type' jest puste

## Wiadomości statusowe
```json
{
    "schema_version": "1.0",
    "device_id": "esp-gt3l13324",
    "sensor_type": "temperature",
    "status": "error",
    "message": "Błąd odczytu danych z czujnika",
    "code": 123,
    "timestamp": 7672839
}
```

### Pola wymagane
```schema_version``` - wersja struktury JSON

```device_id``` - ciąg identyfikacyjny urządzenia (UUID)

```sensor_type``` - rodzaj sensora (wielkość mierzona)

```status``` - status urządzenia (success, error, info)

```message``` - dokładna treść statusu

```code``` - kod statusu

```timestamp``` - znacznik czasu

### Pola opcjonalne 
```message``` - dokładna treść statusu

### Reguły walidacji
#### Pola wymagane
```schema_version``` - musi być nie pustym ciągiem znaków

```device_id``` - musi być nie pustym ciągiem znaków

```sensor_type``` - musi być nie pustym ciągiem znaków

```status``` - musi być nie pustym ciągiem znaków

```code``` - musi być dodatnią liczbą całkowitą

```timestamp``` - musi być dodatnią liczbą całkowitą

#### Pola opcjonalne

```message``` - musi być nie pustym ciągiem znaków

### Przykłady
#### Wiadomość poprawna
```json
{
    "schema_version": "1.0",
    "device_id": "esp-gt3l13324",
    "sensor_type": "temperature",
    "status": "error",
    "message": "Błąd odczytu danych z czujnika",
    "code": 123,
    "timestamp": 7672839
}
```

#### Wiadomości błędne
```json
{
    "schema_version": "1.0",
    "device_id": "esp-gt3l13324",
    "sensor_type": "temperature",
    "status": "",
    "message": "Błąd odczytu danych z czujnika",
    "code": 123,
    "timestamp": 7672839
}
```
    Błąd: Pole 'status' jest puste

---
```json
{
    "schema_version": "1.0",
    "device_id": "esp-gt3l13324",
    "sensor_type": "temperature",
    "status": "error",
    "message": "Błąd odczytu danych z czujnika",
    "timestamp": 7672839
}
```
    Błąd: Brak pola 'code'
