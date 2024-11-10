from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder="static")
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('christmas_list.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    try:
        cursor = conn.execute('SELECT * FROM items')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(items)
    except sqlite3.OperationalError as e:
        print(f"Error fetching items: {e}")
        return jsonify({"error": "Error fetching items, please try again later"}), 500

# Serve index.html from the root route
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
