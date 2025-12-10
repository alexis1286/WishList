from flask import Flask, send_from_directory, jsonify, request, session
import json
import os

app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = "supersecretkey"

admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
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
@app.post("/api/login")
def login():
    data = request.get_json() or {}
    password = data.get("password", "")

    if password == admin_password:
        session["logged_in"] = True
        return jsonify({"status": "ok"}), 200
    else:
        # Make sure they are not logged in
        session.pop("logged_in", None)
        return jsonify({"status": "error", "message": "Invalid password"}), 401
@app.post("/api/logout")
def logout():
    session.pop("logged_in", None)
    return jsonify({"status": "ok"}), 200


@app.route("/api/items", methods=["GET"])
def get_items():
    return jsonify(load_items())

@app.route("/api/items", methods=["POST"])
def add_item():

    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized to add item"}), 401

    data = request.get_json() 
    if not data:
        return jsonify({"error": "No JSON body"}), 400

    items = load_items()
    manual_id = data.get("ID")

    if manual_id is not None:
        # Use the ID the user typed
        new_id = int(manual_id)

        # Shift existing items down if their id is >= the new one
        for item in items:
            current = item.get("id", 0)
            if current >= new_id:
                item["id"] = current + 1
    else:
        # No manual ID → append at the end
        max_id = max((item.get("id", 0) for item in items), default=0)
        new_id = max_id + 1

    items.append({
        "Priority": int(data.get("Priority", 3)),
        "Category": data.get("Category", ""),
        "Item": data.get("Item", ""),
        "Link": data.get("Link", ""),
        "Price": data.get("Price", ""),
        "Image": data.get("Image", ""),
        "id": new_id
    })
def remove_item():

    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized to add item"}), 401

    data = request.get_json() 
    if not data:
        return jsonify({"error": "No JSON body"}), 400

    items = load_items()
    name = data.get("Name")
    


    items.remove({
        "Name": name
    })

    items.sort(key=lambda x: (x["Priority"], x["id"]))
    save_items(items)
    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
