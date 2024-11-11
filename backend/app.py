from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder="static")
CORS(app)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('christmas_list.db')
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint to fetch all items from the database
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

# Endpoint to filter items by category
@app.route('/api/items/filter', methods=['GET'])
def filter_items():
    category = request.args.get('category')
    query = 'SELECT * FROM items WHERE 1=1'
    params = []

    if category:
        query += ' AND Category = ?'
        params.append(category)

    conn = get_db_connection()
    cursor = conn.execute(query, params)
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(items)

# Price scraping endpoint
@app.route('/api/get_price', methods=['POST'])
def get_price():
    url = request.json.get('url')
    item_id = request.json.get('item_id')  # Assuming you pass the item ID for fallback price
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Attempt to find the price using various common selectors
        price = None
        selectors = ['.price', '.product-price', '#price', '.current-price', '.price__current', '.price-final']

        for selector in selectors:
            price_tag = soup.select_one(selector)
            if price_tag:
                price = price_tag.get_text(strip=True)
                break

        if not price:
            # Fallback to the price in the database if scraping fails
            conn = get_db_connection()
            cursor = conn.execute('SELECT Price FROM items WHERE id = ?', (item_id,))
            db_price = cursor.fetchone()
            conn.close()

            if db_price:
                price = db_price['Price']  # Fallback to database price
            else:
                return jsonify({"error": "Price not found in the database"}), 404

        return jsonify({"price": price})
    except requests.exceptions.RequestException as e:
        print(f"Error accessing URL {url}: {e}")
        return jsonify({"error": "Failed to retrieve page"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An error occurred"}), 500


# Serve the index.html file at the root
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
