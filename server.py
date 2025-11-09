from flask import Flask, request, jsonify
from flask_cors import CORS
from Objects.board import Board
from Objects.player import Player
from Objects.property import Property
from Objects.railroad import Railroad
from Objects.utility import Utility
import random
import os

app = Flask(__name__)
CORS(app)

# === GAME STATE ===
board = Board()
players = [Player(f"Player {i + 1}") for i in range(4)]
active_player = 0

# Keep a lightweight piece map for UI tokens (filename relative to Images/)
player_pieces = {}  # index -> "busPiece.png", etc.

# Build ownables by name using your classes
properties = {name: Property(name) for name in Property.purchase_prices.keys()}
railroads = {name: Railroad(name) for name in ["North Bus", "South Bus", "Downtown Bus", "Shopping Bus"]}
utilities = {name: Utility(name) for name in ["SA Fees", "Textbook Fees"]}
ownables = {**properties, **railroads, **utilities}


def get_ownable(name):
    return ownables.get(name)


def get_state():
    """Return full state for the frontend UI."""
    return {
        "active_player": active_player,
        "players": [{
            "name": p.name,
            "balance": p.balance,
            "position": p.position,
            "coords": list(p.coordinates),  # (x, y) 0..100 from Board.get_tile_coordinates
            "piece": player_pieces.get(i),  # e.g., "busPiece.png"
            "properties": [prop.name for prop in p.properties],
            "bankrupt": p.bankrupt,
        } for i, p in enumerate(players)],
    }


# ========== ENDPOINTS ==========

@app.route("/init_players", methods=["POST"])
def init_players():
    """
    Initialize game with a custom set of players from page2.
    Payload:
      { "players": [ { "name": "...", "piece": "busPiece.png" }, ... ] }
    """
    global board, players, active_player, player_pieces, properties, railroads, utilities, ownables

    data = request.get_json() or {}
    incoming = data.get("players", [])
    if not isinstance(incoming, list) or len(incoming) == 0:
        return jsonify({"error": "players array required"}), 400

    # Reset everything
    board = Board()
    players = [Player(p.get("name", f"Player {i+1}")) for i, p in enumerate(incoming)]
    active_player = 0
    player_pieces = {i: (p.get("piece") or None) for i, p in enumerate(incoming)}

    properties = {name: Property(name) for name in Property.purchase_prices.keys()}
    railroads = {name: Railroad(name) for name in ["North Bus", "South Bus", "Downtown Bus", "Shopping Bus"]}
    utilities = {name: Utility(name) for name in ["SA Fees", "Textbook Fees"]}
    ownables = {**properties, **railroads, **utilities}

    return jsonify({"message": "Players initialized", **get_state()})


@app.route("/state", methods=["GET"])
def state():
    return jsonify(get_state())


@app.route("/roll", methods=["POST"])
def roll():
    """Roll dice, move active player using Board, handle passing GO and rent."""
    global active_player
    p = players[active_player]

    d = random.randint(1, 6) + random.randint(1, 6)
    move_msg = p.move(d, board)  # updates position, coordinates, balances on GO

    tile = board.get_tile(p.position)
    tile_name = tile["name"]
    msg = f"{move_msg} Landed on {tile_name}."

    # Rent if ownable and owned by someone else
    obj = get_ownable(tile_name)
    if obj and obj.owner() and obj.owner() != p:
        rent_msg = p.pay_rent(obj, dice_roll=d)
        if rent_msg:
            msg += f" {rent_msg}"

    return jsonify({"roll": d, "landed": tile_name, "message": msg, **get_state()})


@app.route("/buy", methods=["POST"])
def buy():
    """
    Buy the tile where the active player stands (no need to click). If 'property'
    is provided in payload, we respect it; otherwise infer from current position.
    """
    global active_player
    p = players[active_player]

    data = request.get_json() or {}
    prop_name = data.get("property")
    if not prop_name:
        prop_name = board.get_tile(p.position)["name"]

    obj = get_ownable(prop_name)
    if not obj:
        return jsonify({"error": f"{prop_name} is not purchasable."}), 400

    msg = p.buy_property(obj)
    return jsonify({"message": msg, "bought": prop_name, **get_state()})


@app.route("/end_turn", methods=["POST"])
def end_turn():
    global active_player
    active_player = (active_player + 1) % len(players)
    return jsonify({"next_player": players[active_player].name, **get_state()})


@app.route("/reset", methods=["POST"])
def reset():
    """Hard reset back to four default players."""
    global board, players, active_player, player_pieces, properties, railroads, utilities, ownables
    board = Board()
    players = [Player(f"Player {i + 1}") for i in range(4)]
    active_player = 0
    player_pieces = {}

    properties = {name: Property(name) for name in Property.purchase_prices.keys()}
    railroads = {name: Railroad(name) for name in ["North Bus", "South Bus", "Downtown Bus", "Shopping Bus"]}
    utilities = {name: Utility(name) for name in ["SA Fees", "Textbook Fees"]}
    ownables = {**properties, **railroads, **utilities}
    return jsonify({"message": "Game reset!", **get_state()})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
