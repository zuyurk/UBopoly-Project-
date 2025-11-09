from flask import Flask, request, jsonify
from flask_cors import CORS
import random

# ==== Your game objects ==================================

from Objects.player import Player
from Objects.property import Property
from Objects.board import Board
# (Railroad/Utility exist but are not yet placed on the board; you can wire them later.)

# ==== Chance deck ========================================

class ChanceDeck:
    """
    Very small example deck: some 'immediate' effects and one 'keepable' card.
    You can add many more!
    """
    def __init__(self):
        self._reset_deck()

    def _reset_deck(self):
        self.cards = [
            {"id": "advance_go", "text": "Advance to GO (collect $200)", "type": "immediate"},
            {"id": "bank_pays_50", "text": "Bank pays you dividend of $50", "type": "immediate"},
            {"id": "pay_each_50", "text": "Pay each player $50", "type": "immediate"},
            {"id": "go_to_jail", "text": "Go to Jail. Do not pass GO.", "type": "immediate"},
            {"id": "jail_free", "text": "Get Out of Jail Free (keep this card)", "type": "keepable"},
        ]
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            self._reset_deck()
        return self.cards.pop()

# ==== Game manager =======================================

class GameManager:
    def __init__(self, player_names=None, pieces=None):
        if player_names is None:
            player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
        self.board = Board()
        self.players = [Player(n) for n in player_names]
        # Optional: attach piece filenames from UI
        if pieces:
            for p, piece in zip(self.players, pieces):
                p.piece = piece

        self.active = 0
        # All purchasable properties we know about (by name)
        self.properties = {name: Property(name) for name in Property.purchase_prices.keys()}

        # Chance
        self.chance = ChanceDeck()
        # Keepable cards held by players: {player_index: [{"id","text"}]}
        self.held_cards = {i: [] for i in range(len(self.players))}

    # --- helpers
    def _tile_name(self, idx):
        return self.board.tile_names[idx % len(self.board.tile_names)]

    def _tile_coords_pct(self, idx):
        # Board uses 0..100 coords already → good for UI if you ever need it
        x, y = self.board.get_tile_coordinates(idx)
        return [x, y]

    def get_state(self):
        # Include each player's current tile name so the UI can place tokens EXACTLY on the DOM tile center
        return {
            "active_player": self.active,
            "players": [
                {
                    "name": p.name,
                    "balance": p.balance,
                    "position": p.position,
                    "tile": self._tile_name(p.position),
                    "coords": self._tile_coords_pct(p.position),
                    "in_jail": p.in_jail,
                    "cards": self.held_cards[i],
                    "piece": getattr(p, "piece", None),
                }
                for i, p in enumerate(self.players)
            ],
            "owned_properties": {
                nm: self.properties[nm].owner().name if self.properties[nm].owner() else None
                for nm in self.properties
            }
        }

    def next_turn(self):
        self.active = (self.active + 1) % len(self.players)

    # --- actions
    def roll(self):
        p = self.players[self.active]
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        roll = d1 + d2

        prev = p.position
        p.position = (p.position + roll) % len(self.board.tile_names)

        # Passed GO?
        if p.position < prev:
            p.balance += Player.GO_CASH

        landed = self._tile_name(p.position)

        result = {
            "roll": roll,
            "message": f"{p.name} rolled {roll} and moved to {landed}.",
            "landed": landed,
        }

        # If landed on CHANCE
        if landed == "Chance":
            card = self.chance.draw()
            result["chance_card"] = card

            if card["type"] == "immediate":
                self._apply_chance_immediate(p, card, result)
            else:
                # keepable
                self.held_cards[self.active].append({"id": card["id"], "text": card["text"]})
                result["message"] += f" Drew Chance: “{card['text']}” (kept)."

        # Sync payload with full state
        result.update(self.get_state())
        return result

    def _apply_chance_immediate(self, player, card, result_payload):
        if card["id"] == "advance_go":
            player.position = 0
            player.balance += Player.GO_CASH
            result_payload["landed"] = self._tile_name(player.position)
            result_payload["message"] += " Chance: Advance to GO (+$200)."
        elif card["id"] == "bank_pays_50":
            player.balance += 50
            result_payload["message"] += " Chance: Bank pays you $50."
        elif card["id"] == "pay_each_50":
            # Pay each other player 50
            pay = 50
            others = [pl for pl in self.players if pl is not player]
            total = pay * len(others)
            if player.balance >= total:
                player.balance -= total
                for pl in others: pl.balance += pay
            else:
                # if can't afford, go bankrupt to bank (simple behavior)
                player.balance = 0
            result_payload["message"] += " Chance: Pay each player $50."
        elif card["id"] == "go_to_jail":
            # Move to the Go To Academic Violation corner in our board list
            # That tile in your Board is named "Go to Academic Violation"
            jail_idx = self.board.tile_names.index("Go to Academic Violation")
            player.position = jail_idx
            player.in_jail = True
            result_payload["landed"] = self._tile_name(player.position)
            result_payload["message"] += " Chance: Go to Jail!"
        # else: ignore unknown ids

    def use_card(self, card_id):
        # Only current player can use their kept card (e.g., Get Out of Jail Free)
        lst = self.held_cards[self.active]
        i = next((i for i, c in enumerate(lst) if c["id"] == card_id), None)
        if i is None:
            return {"error": "Card not found."}

        p = self.players[self.active]
        card = lst.pop(i)

        # Implement just 'jail_free' for now
        if card_id == "jail_free":
            if p.in_jail:
                p.in_jail = False
                msg = f"{p.name} used Get Out of Jail Free."
            else:
                msg = f"{p.name} keeps the card for later (not in jail)."
                # Put it back if you prefer:
                # lst.append(card)
        else:
            msg = "Card effect not implemented."

        out = {"message": msg}
        out.update(self.get_state())
        return out

    def buy_current_tile(self):
        p = self.players[self.active]
        name = self._tile_name(p.position)
        if name not in self.properties:
            return {"error": f"{name} is not purchasable."}

        prop = self.properties[name]
        msg = p.buy_property(prop)
        out = {"message": msg}
        out.update(self.get_state())
        return out

    def reset(self):
        names = [p.name for p in self.players]
        pieces = [getattr(p, "piece", None) for p in self.players]
        self.__init__(names, pieces)  # reset same roster
        return {"message": "Game reset.", **self.get_state()}

# ==== Flask wiring =======================================

app = Flask(__name__)
CORS(app)

# In-memory game
GM = GameManager()

@app.route("/init_players", methods=["POST"])
def init_players():
    """
    Body:
      {
        "players": [
          {"name": "...", "piece": "busPiece.png"},
          ...
        ]
      }
    """
    data = request.get_json() or {}
    players = data.get("players") or []
    names = [p.get("name", f"Player {i+1}") for i, p in enumerate(players)]
    pieces = [p.get("piece") for p in players]
    global GM
    GM = GameManager(names, pieces)
    return jsonify({"message": "Players initialized.", **GM.get_state()})

@app.route("/state", methods=["GET"])
def state():
    return jsonify(GM.get_state())

@app.route("/roll", methods=["POST"])
def roll():
    return jsonify(GM.roll())

@app.route("/buy", methods=["POST"])
def buy():
    return jsonify(GM.buy_current_tile())

@app.route("/end_turn", methods=["POST"])
def end_turn():
    GM.next_turn()
    s = GM.get_state()
    s["next_player"] = s["players"][s["active_player"]]["name"]
    return jsonify(s)

@app.route("/use_card", methods=["POST"])
def use_card():
    data = request.get_json() or {}
    card_id = data.get("card_id")
    if not card_id:
        return jsonify({"error": "card_id required"}), 400
    return jsonify(GM.use_card(card_id))

@app.route("/reset", methods=["POST"])
def reset():
    return jsonify(GM.reset())

if __name__ == "__main__":
    app.run(debug=True)
