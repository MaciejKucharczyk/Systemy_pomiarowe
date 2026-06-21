MEASUREMENT_DICT_FIELDS = [
    "id",
    "group_id",
    "device_id",
    "sensor",
    "value",
    "unit",
    "ts_ms",
    "seq",
    "topic",
    "received_at"
]
SENSOR_DICT_FIELDS = [
    "uuid",
    "name",
    "type",
    "sensor",
    "is_online"
]

def row_to_dict(row: list, fields: list = None):

    if fields is None:
        fields = MEASUREMENT_DICT_FIELDS

    return {field: value for value, field in zip(row, fields)}