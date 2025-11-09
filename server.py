from flask import Flask, request, jsonify
from Objects.player import Player
from Objects.property import Property

app = Flask(__name__)

# Example setup
board_tiles = list(Property.purchase_prices.keys())
player = Player("Player 1")
properties = {name: Property(name) for name in board_tiles}


@app.route("/buy", methods=["POST"])
def buy_property():
    data = request.get_json()
    prop_name = data.get("property")

    if prop_name not in properties:
        return jsonify({"error": "Invalid property"}), 400

    prop = properties[prop_name]
    message = player.buy_property(prop)

    return jsonify({
        "message": message,
        "new_balance": player.balance
    })


if __name__ == "__main__":
    app.run(debug=True)
