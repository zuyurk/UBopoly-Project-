import random
from Objects.player import Player
from Objects.property import Property


class GameManager:
    def __init__(self, player_names=None):
        # Default setup with 4 players if none provided
        if player_names is None:
            player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]

        self.players = [Player(name) for name in player_names]
        self.active_player_index = 0
        self.board_tiles = list(Property.purchase_prices.keys())
        self.properties = {name: Property(name) for name in self.board_tiles}

    # === STATE HELPERS ===
    def get_state(self):
        """Return the current game state in JSON-friendly format."""
        return {
            "active_player": self.active_player_index,
            "active_player_name": self.players[self.active_player_index].name,
            "players": [
                {
                    "name": p.name,
                    "balance": p.balance,
                    "position": p.position,
                    "bankrupt": p.bankrupt,
                    "properties": [prop.name for prop in p.properties]
                }
                for p in self.players
            ],
            "owned_properties": {
                name: prop._owner.name if prop._owner else None
                for name, prop in self.properties.items()
            }
        }

    def get_active_player(self):
        """Return the Player object for the current active player."""
        return self.players[self.active_player_index]

    # === CORE GAME LOGIC ===
    def roll_dice(self):
        """Simulate rolling two dice."""
        r
