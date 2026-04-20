from flask import Flask, jsonify
from db import get_connection

app = Flask(__name__)



@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/measurements", methods=["GET"])
def get_measurements():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT id, group_id, device_id, sensor, value, unit, ts_ms, seq, topic
    FROM measurements
    ORDER BY id DESC
    LIMIT 20
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "group_id": row[1],
            "device_id": row[2],
            "sensor": row[3],
            "value": row[4],
            "unit": row[5],
            "ts_ms": row[6],
            "seq": row[7],
            "topic": row[8]
        })
    return jsonify(result)

@app.route("/measurements/latest", methods=["GET"])
def get_latest_measurement():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT id, group_id, device_id, sensor, value, unit, ts_ms, seq, topic
    FROM measurements
    ORDER BY id DESC
    LIMIT 1
    """)
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row is None:
        return jsonify({"message": "Brak danych"}), 404
    
    return jsonify({
        "id": row[0],
        "group_id": row[1],
        "device_id": row[2],
        "sensor": row[3],
        "value": row[4],
        "unit": row[5],
        "ts_ms": row[6],
        "seq": row[7],
        "topic": row[8]
    })

if __name__ == "__main__":
    app.run()