from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# Load JSON data once and store it in a variable
with open('christmas_list.json') as f:
    items_data = json.load(f)

# Endpoint to fetch all items or filter by category
@app.route('/api/items', methods=['GET'])
def get_items():
    category = request.args.get('category')
    if category:
        filtered_items = [item for item in items_data if item['Category'] == category]
        return jsonify(filtered_items)
    return jsonify(items_data)

# Price scraping endpoint
@app.route('/api/get_price', methods=['POST'])
def get_price():
    url = request.json.get('url')
    item_id = request.json.get('item_id')  # Assumes item_id is passed for fallback price
    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Try to scrape the price from the URL
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Common selectors for price data
        price = None
        selectors = ['.price', '.product-price', '#price', '.current-price', '.price__current', '.price-final']
        for selector in selectors:
            price_tag = soup.select_one(selector)
            if price_tag:
                price = price_tag.get_text(strip=True)
                break

        if not price:
            # Fallback to the price in the JSON data if scraping fails
            for item in items_data:
                if item['id'] == item_id:
                    price = item['Price']
                    break

        return jsonify({"price": price})
    except requests.exceptions.RequestException as e:
        print(f"Error accessing URL {url}: {e}")
        return jsonify({"error": "Failed to retrieve page"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An error occurred"}), 500

# Serve index.html from the root directory
@app.route('/')
def serve_index():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
