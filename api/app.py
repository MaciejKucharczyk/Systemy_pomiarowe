from flask import Flask, jsonify, render_template, request, Response
from db import get_connection
from models import row_to_dict, SENSOR_DICT_FIELDS
import math
import json
import time

app = Flask(__name__)

state = {
    "step": 0,
    "amplitude": 10.0,
    "frequency": 0.1,  # Jak gęsto próbkowany jest sinus
    "offset": 20.0     # Np. bazowa temperatura
}


def fetch_sensors():
    return fetch_results_from_db(
        """
        SELECT uuid, name, type, sensor, is_online
        FROM sensor
        WHERE 1=1
        """,
        False
    )


def fetch_results_from_db(query, one_result = False, params = None, fields = None):

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


@app.route("/")
def view_sensors():
    results = [row_to_dict(row, SENSOR_DICT_FIELDS) for row in fetch_sensors()]
    return render_template('index.html', data=results)

@app.route("/<device_id>/measurements/")
def view_measurements(device_id: str):
    limit = request.args.get("limit", 20, type=int)

    measurements = fetch_results_from_db(
        """
        SELECT id, group_id, device_id, sensor, value, unit, ts_ms, seq, topic, received_at
        FROM measurements WHERE device_id = %s
        ORDER BY id DESC
        LIMIT %s
        """,
        False,
        [device_id, limit]
    )
    sensor = row_to_dict(
        fetch_results_from_db(
            """
            SELECT *
            FROM sensor
            WHERE uuid = %s
            """, True, [device_id]
        ),
        SENSOR_DICT_FIELDS
    )
    results = [row_to_dict(row) for row in measurements]
    
    chart_data = {
        'labels': [],
        'values': [],
        'y_label': ""
    }
    if len(results) > 0:
        chart_data['labels'] = [int(r.get('received_at').timestamp() * 1000) for r in results]
        chart_data['values'] = [r.get('value') for r in results]
        chart_data["y_label"] = f"{sensor.get('type')} ({results[0].get('unit')})"

    return render_template('measurements.html', data=results, sensor=sensor, chart_data=json.dumps(chart_data))


@app.route("/live")
def view_live_measurements():
    device_id = request.args.get('device_id', fetch_sensors()[0][0]);
    sensors = [row_to_dict(row, SENSOR_DICT_FIELDS) for row in fetch_results_from_db(
        """
        SELECT uuid, name, type, sensor, is_online
        FROM sensor
        ORDER BY CASE WHEN uuid = %s THEN 0 ELSE 1 END, uuid DESC
        """,
        False,
        [device_id]
    )]

    return render_template('live_measurements.html', sensors=sensors, device_id=device_id)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/measurements", methods=["GET"])
def get_measurements():
    rows = fetch_results_from_db(
        """
        SELECT id, group_id, device_id, sensor, value, unit, ts_ms, seq, topic, received_at
        FROM measurements
        ORDER BY id DESC
        LIMIT 20
        """
    )

    result = [row_to_dict(row) for row in rows]
    return jsonify(result)

@app.route("/measurements/latest", methods=["GET"])
def get_latest_measurement():
    row = fetch_results_from_db(
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

@app.route('/measurements/fake-latest', methods=['GET'])
def get_fake_latest_measurement():
    val = state["offset"] + state["amplitude"] * math.sin(state["step"] * state["frequency"])
    
    state["step"] += 1
    
    return jsonify({
        "device_id": "esp-gt3l13324",
        "sensor": "temperature",
        "value": round(val, 3),
        "unit": "C",
        "ts_ms": 2345633663,
        "seq": state["step"]
    })

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

    rows = fetch_results_from_db(query, False, params)

    result = [row_to_dict(row) for row in rows]
    return jsonify(result)


@app.route("/sensors", methods=["GET"])
def get_sensors():
    result = fetch_sensors()
    return jsonify([row_to_dict(row, SENSOR_DICT_FIELDS) for row in result])


def measurement_stream(device_id: str):
    while True:
        result = fetch_results_from_db(
                """
                SELECT id, group_id, device_id, sensor, value, unit, ts_ms, seq, topic, received_at
                FROM measurements WHERE device_id = %s
                ORDER BY id DESC
                LIMIT 1
                """,
                True,
                [device_id]
        )
        data = row_to_dict(result)

        val = state["offset"] + state["amplitude"] * math.sin(state["step"] * state["frequency"])
        state["step"] += 1

        data["value"] = val;
        data["timestamp"] = int(data["received_at"].timestamp() * 1000)
        data["received_at"] = data["received_at"].strftime('%Y-%m-%d %H:%M:%S')

        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(1)
        

@app.route("/stream/device/<device_id>")
def get_measurements_stream(device_id: str):
    response = Response(measurement_stream(device_id), mimetype="text/event-stream")
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    response.headers['X-Accel-Buffering'] = 'no'
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, threaded=True)