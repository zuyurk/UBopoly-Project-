from flask import Flask, request, jsonify
from flask_cors import CORS
from GameManager import game  # uses the singleton 'game' defined in GameManager.py

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.get("/state")
def state():
    return jsonify(game.serialize())

@app.post("/init_players")
def init_players():
    body = request.get_json(force=True) or {}
    players = body.get("players", [])
    game.init_players(players)
    return jsonify(game.serialize())

@app.post("/roll")
def roll():
    out = game.roll()
    return jsonify(out)

@app.post("/buy")
def buy():
    out = game.buy()
    return jsonify(out)

@app.post("/use_card")
def use_card():
    body = request.get_json(force=True) or {}
    card_id = body.get("card_id")
    out = game.use_card(card_id)
    return jsonify(out)

@app.post("/end_turn")
def end_turn():
    out = game.end_turn()
    return jsonify(out)

@app.post("/reset")
def reset():
    game.reset()
    return jsonify(game.serialize())

if __name__ == "__main__":
    # Run on port 5050 and disable the reloader to prevent duplicate servers on the same port
    app.run(host="0.0.0.0", port=5050, debug=True, use_reloader=False)
