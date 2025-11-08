from player import Player
from board import Board
import random

class GameManager:
    def __init__(self):
        """Initialize the board, players, and starting turn."""
        self.board = Board()
        self.players = [Player("Alice"), Player("Bob")]
        self.current_turn = 0
        self.turn_count = 0

    def roll_and_move(self):
        """Roll dice, move the player, and update the game state."""
        player = self.players[self.current_turn]

        # Skip bankrupt players
        if player.bankrupt:
            print(f"{player.name} is bankrupt and skipped.")
            self.next_turn()
            return {"message": f"{player.name} is bankrupt and skipped.", "player": player.to_dict()}

        # Roll 2 dice
        dice = random.randint(1, 6) + random.randint(1, 6)
        print(f"{player.name} rolled a {dice}!")

        # Move player and get result message
        result_message = player.move(dice, self.board)
        self.turn_count += 1

        # Check for passing GO or other updates
        print(result_message)
        print(f"New position: {player.position} | Coordinates: {player.coordinates}")
        print(f"Balance: ${player.balance}")
        print("-" * 40)

        # Switch to the next player
        self.next_turn()

        return {"message": result_message, "player": player.to_dict()}

    def next_turn(self):
        """Rotate to the next player."""
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def is_game_over(self):
        """Check if the game is over (only one active player remains)."""
        active_players = [p for p in self.players if not p.bankrupt]
        return len(active_players) <= 1

    def get_winner(self):
        """Return the winner, if one exists."""
        active_players = [p for p in self.players if not p.bankrupt]
        if len(active_players) == 1:
            winner = active_players[0]
            return {"name": winner.name, "balance": winner.balance, "net_worth": winner.net_worth()}
        return None

    def get_state(self):
        """Return the full game state for frontend updates."""
        return {
            "turn": self.current_turn,
            "turn_count": self.turn_count,
            "players": [p.to_dict() for p in self.players],
            "is_game_over": self.is_game_over(),
            "winner": self.get_winner()
        }

    def print_state(self):
        """CLI helper to display current game status."""
        print("\n📊 Current Game State:")
        for p in self.players:
            print(f"- {p.name}: ${p.balance}, pos={p.position}, coords={p.coordinates}")
        print("-" * 40)
