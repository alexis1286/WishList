from flask import Flask, send_from_directory, jsonify, request
import json
import os

app = Flask(__name__, static_folder="static", static_url_path="")

ITEMS_FILE = "christmas_list.json"


def load_items():
    if not os.path.exists(ITEMS_FILE):
        return []
    with open(ITEMS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_items(items):
    with open(ITEMS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)


@app.route("/")
def index():
    # serves static/index.html
    return app.send_static_file("index.html")


@app.route("/api/items", methods=["GET"])
def get_items():
    return jsonify(load_items())


@app.route("/api/items", methods=["POST"])
def add_item():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body"}), 400

    items = load_items()
    items.append({
        "Priority": int(data.get("Priority", 3)),
        "Category": data.get("Category", ""),
        "Item": data.get("Item", ""),
        "Link": data.get("Link", ""),
        "Price": data.get("Price", ""),
        "Image": data.get("Image", "")
    })
    save_items(items)
    return jsonify({"status": "ok"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
