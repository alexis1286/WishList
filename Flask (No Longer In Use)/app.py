#from flask import Flask, request, jsonify
#from flask_cors import CORS  # Import CORS
#import json

#app = Flask(__name__)
#CORS(app, resources={r"/*": {"origins": "*"}})  
# Load wishlist from file
def load_wishlist():
    try:
        with open("christmas_list.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# API endpoint to get wishlist data
@app.route("/wishlist", methods=["GET"])
def get_wishlist():
    return jsonify(load_wishlist())

# API endpoint to add an item
@app.route("/wishlist/add", methods=["POST"])
def add_item():
    wishlist = load_wishlist()
    new_item = request.json
    new_item["id"] = len(wishlist) + 1
    wishlist.append(new_item)
    with open("christmas_list.json", "w") as file:
        json.dump(wishlist, file, indent=4)
    return jsonify({"message": "Item added!", "wishlist": wishlist})

# API endpoint to remove an item
@app.route("/wishlist/remove/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    wishlist = load_wishlist()
    wishlist = [item for item in wishlist if item["id"] != item_id]
    with open("christmas_list.json", "w") as file:
        json.dump(wishlist, file, indent=4)
    return jsonify({"message": "Item removed!", "wishlist": wishlist})

# Ensure the app runs on the correct port
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)