from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


# Helper function to connect to the database
def get_db_connection():
    try:
        conn = sqlite3.connect('christmas_list.db')
        conn.row_factory = sqlite3.Row
        print("Database connection successful")  # Debug message
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")  # Error message
        return None

# Endpoint to get all items
@app.route('/api/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.execute('SELECT * FROM items')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        print("Data retrieval successful")  # Debug message
        return jsonify(items)
    except sqlite3.OperationalError as e:
        print(f"Error fetching items: {e}")  # Error message
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

if __name__ == '__main__':
    app.run(debug=True)
