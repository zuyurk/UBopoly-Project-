from flask import Flask, request, jsonify
from flask_cors import CORS
from Objects.player import Player
from Objects.property import Property
import random

app = Flask(__name__)
CORS(app)

# === Game Setup ===
board_tiles = list(Property.purchase_prices.keys())
players = [Player(f"Player {i+1}") for i in range(4)]
active_player = 0
properties = {name: Property(name) for name in board_tiles}


@app.route("/roll", methods=["POST"])
def roll_dice():
    """Simulate rolling two dice and return their sum."""
    roll = random.randint(1, 6) + random.randint(1, 6)
    return jsonify({"roll": roll})


@app.route("/buy", methods=["POST"])
def buy_property():
    """Buy a property for the active player."""
    global active_player
    data = request.get_json() or {}
    prop_name = data.get("property")

    if prop_name not in properties:
        return jsonify({"error": f"Invalid property: {prop_name}"}), 400

    player = players[active_player]
    prop = properties[prop_name]
    message = player.buy_property(prop)
    return jsonify({
        "message": message,
        "new_balance": player.balance,
        "active_player": player.name
    })


@app.route("/state", methods=["GET"])
def get_state():
    """Return current players and balances."""
    return jsonify({
        "active_player": active_player,
        "players": [{"name": p.name, "balance": p.balance} for p in players],
        "properties_owned": {
            p.name: [prop.name for prop in p.properties] for p in players
        }
    })


@app.route("/end_turn", methods=["POST"])
def end_turn():
    """Advance to the next player's turn."""
    global active_player
    active_player = (active_player + 1) % len(players)
    next_player = players[active_player].name
    return jsonify({"next_player": next_player})


@app.route("/reset", methods=["POST"])
def reset_game():
    """Reset the game to starting state."""
    global players, active_player, properties
    players = [Player(f"Player {i+1}") for i in range(4)]
    active_player = 0
    properties = {name: Property(name) for name in board_tiles}
    return jsonify({"message": "Game reset.", "player_balance": 1500})


if __name__ == "__main__":
    app.run(debug=True)
