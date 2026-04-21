from flask import Flask, jsonify, render_template

import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

@app.route("/")
def hello_world():
    # Przykładowe dane (docelowo będą z bazy)
    pomiary = [
        {"uuid": "123", "name": "Sensor 1", "type": "Temp", "is_online": True},
        {"uuid": "456", "name": "Sensor 2", "type": "Wilgotność", "is_online": False}
    ]
    return render_template('index.html', data=pomiary)

""" Prosty health-check, weryfikacja dzialania przechodzenia miedzy endpoitami """
@app.route("/health", methods=["GET"])
def health():   
    return jsonify({"status": "ok"})

""" A tym sprawdzamy wartości pomiarów """
@app.route("/measurements", methods=["GET"])
def measurements():   
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
