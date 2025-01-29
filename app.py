from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Connect to the database
def connect_db():
    return sqlite3.connect("christmas_list.db")

# Get all wishlist items
@app.route("/wishlist", methods=["GET"])
def get_wishlist():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, item, link, price, image, priority FROM wishlist")
    items = [{"id": row[0], "Category": row[1], "Item": row[2], "Link": row[3], "Price": row[4], "Image": row[5], "Priority": row[6]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(items)

# Add a new item to the wishlist
@app.route("/wishlist/add", methods=["POST"])
def add_item():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO wishlist (category, item, link, price, image, priority) VALUES (?, ?, ?, ?, ?, ?)",
                   (data["Category"], data["Item"], data["Link"], data["Price"], data["Image"], data["Priority"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item added successfully!"})

# Remove an item from the wishlist
@app.route("/wishlist/remove/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wishlist WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item removed successfully!"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
