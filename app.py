from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load wishlist from file
def load_wishlist():
    try:
        with open("christmas_list.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save wishlist to file
def save_wishlist(wishlist):
    with open("christmas_list.json", "w") as file:
        json.dump(wishlist, file, indent=4)

# API endpoint to get wishlist data
@app.route("/wishlist", methods=["GET"])
def get_wishlist():
    return jsonify(load_wishlist())

# API endpoint to add an item
@app.route("/wishlist/add", methods=["POST"])
def add_item():
    wishlist = load_wishlist()
    new_item = request.json
    new_item["id"] = len(wishlist) + 1  # Auto-increment ID
    wishlist.append(new_item)
    save_wishlist(wishlist)
    return jsonify({"message": "Item added!", "wishlist": wishlist})

# API endpoint to remove an item
@app.route("/wishlist/remove/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    wishlist = load_wishlist()
    wishlist = [item for item in wishlist if item["id"] != item_id]
    save_wishlist(wishlist)
    return jsonify({"message": "Item removed!", "wishlist": wishlist})

if __name__ == "__main__":
    app.run(debug=True)
