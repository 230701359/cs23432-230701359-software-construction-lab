from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

DB_PATH = "fraud_detection.db"

# Database connection

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Serve HTML and static files directly from root folder
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

# API: View all data
@app.route("/view", methods=["GET"])
def view():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM fraud_data").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# API: Save phone number
@app.route("/save_phone", methods=["POST"])
def save_phone():
    phone = request.json.get("phone")
    if not phone:
        return jsonify({"error": "Phone is required"}), 400
    conn = get_db_connection()
    conn.execute("INSERT INTO fraud_data (value, type, flagged) VALUES (?, ?, ?)", (phone, 'phone', 0))
    conn.commit()
    conn.close()
    return jsonify({"message": "Phone number saved!"})

# API: Save OTP
@app.route("/save_otp", methods=["POST"])
def save_otp():
    otp = request.json.get("otp")
    if not otp:
        return jsonify({"error": "OTP is required"}), 400
    conn = get_db_connection()
    conn.execute("INSERT INTO fraud_data (value, type, flagged) VALUES (?, ?, ?)", (otp, 'otp', 0))
    conn.commit()
    conn.close()
    return jsonify({"message": "OTP saved!"})

# API: Check for fraud
@app.route("/check_fraud", methods=["POST"])
def check_fraud():
    input_data = request.json.get("input")
    conn = get_db_connection()
    match = conn.execute("SELECT * FROM fraud_data WHERE value = ?", (input_data,)).fetchone()
    conn.close()
    return jsonify({"fraud": bool(match and match['flagged'])})

# API: Flag or unflag data
@app.route("/flag", methods=["POST"])
def flag_data():
    data_id = request.json.get("id")
    flagged = request.json.get("flagged")
    conn = get_db_connection()
    conn.execute("UPDATE fraud_data SET flagged = ? WHERE id = ?", (flagged, data_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Data flagged successfully"})

if __name__ == '__main__':
    app.run(debug=True)