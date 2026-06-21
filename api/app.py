from flask import Flask, jsonify, render_template


from flask import Flask, jsonify, request
from db import get_connection
from models import row_to_dict, SENSOR_DICT_FIELDS
import math

app = Flask(__name__)

state = {
    "step": 0,
    "amplitude": 10.0,
    "frequency": 0.1,  # Jak gęsto próbkowany jest sinus
    "offset": 20.0     # Np. bazowa temperatura
}

@app.route("/")
def hello_world():
    # Przykładowe dane (docelowo będą z bazy)
    pomiary = [
        {"uuid": "123", "name": "Sensor 1", "type": "Temp", "is_online": True},
        {"uuid": "456", "name": "Sensor 2", "type": "Wilgotność", "is_online": False}
    ]
    return render_template('index.html', data=pomiary)

# """ Prosty health-check, weryfikacja dzialania przechodzenia miedzy endpoitami """
# @app.route("/health", methods=["GET"])
# def health():   
#     return jsonify({"status": "ok"})

# """ A tym sprawdzamy wartości pomiarów """
# @app.route("/measurements", methods=["GET"])
# def measurements():   
#     return jsonify({"status": "ok"})

# app = Flask(__name__)

def get_results_from_db(query, one_result = False, params = None, fields = None):

    if params is None:
        params = []

    if fields is None:
        fields = SENSOR_DICT_FIELDS

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)

    if one_result:
        result = cur.fetchone()
    else:
        result = cur.fetchall()

    cur.close()
    conn.close()

    return result

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/measurements", methods=["GET"])
def get_measurements():
    rows = get_results_from_db(
        """
        SELECT id, group_id, device_id, sensor, value, unit, ts_ms, seq, topic
        FROM measurements
        ORDER BY id DESC
        LIMIT 20
        """
    )

    result = [row_to_dict(row) for row in rows]
    return jsonify(result)

@app.route("/measurements/latest", methods=["GET"])
def get_latest_measurement():
    row = get_results_from_db(
        """
        SELECT id, group_id, device_id, sensor, value, unit, ts_ms, seq, topic
        FROM measurements
        ORDER BY id DESC
        LIMIT 1
        """,
        True
    )
    if row is None:
        return jsonify({"message": "Brak danych"}), 404
    
    val = state["offset"] + state["amplitude"] * math.sin(state["step"] * state["frequency"])
    
    # Inkrementujemy krok dla kolejnego zapytania
    state["step"] += 1

    data = row_to_dict(row)
    data["value"] = val

    return jsonify(data)

@app.route("/measurements/history", methods=["GET"])
def get_measurements_history():
    device_id = request.args.get("device_id")
    sensor = request.args.get("sensor")
    limit = request.args.get("limit", 20, type=int)

    query = """
    SELECT id, group_id, device_id, sensor, value, unit, ts_ms, seq, topic
    FROM measurements 
    WHERE 1=1 
    """

    params = []

    if device_id:
        query += f" AND device_id = %s"
        params.append(device_id)

    if sensor:
        query += f" AND sensor = %s"
        params.append(sensor)

    params.append(limit)
    query += " ORDER BY id DESC LIMIT %s"

    rows = get_results_from_db(query, False, params)

    result = [row_to_dict(row) for row in rows]
    return jsonify(result)

@app.route("/sensors", methods=["GET"])
def get_sensors():
    rows = get_results_from_db(
        """
        SELECT uuid, name, type, sensor, is_online
        FROM sensor
        WHERE 1=1
        """,
        False
    )

    result = [row_to_dict(row, SENSOR_DICT_FIELDS) for row in rows]
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)