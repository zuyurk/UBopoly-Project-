from player import Player
from board import Board
import random

class GameManager:
    def __init__(self):
        self.board = Board()
        self.players = [Player("Alice"), Player("Bob")]
        self.current_turn = 0

    def roll_and_move(self):
        player = self.players[self.current_turn]
        dice = random.randint(1, 6) + random.randint(1, 6)
        message = player.move(dice, self.board)
        self.current_turn = (self.current_turn + 1) % len(self.players)
        return {"message": message, "player": player.to_dict()}

    def get_state(self):
        return {"players": [p.to_dict() for p in self.players]}
