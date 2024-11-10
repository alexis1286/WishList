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


# Optional: Endpoint to filter items by priority or category
@app.route('/api/items/filter', methods=['GET'])
def filter_items():
    priority = request.args.get('priority')
    category = request.args.get('category')
    query = 'SELECT * FROM items WHERE 1=1'
    params = []

    if priority:
        query += ' AND priority = ?'
        params.append(priority)
    if category:
        query += ' AND category = ?'
        params.append(category)

    conn = get_db_connection()
    cursor = conn.execute(query, params)
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(items)

# Serve index.html from the root route
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
