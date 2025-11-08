from player import Player
from board import Board
import random

def main():
    # Initialize game
    board = Board()
    players = [
        Player("Alice"),
        Player("Bob")
    ]

    turn = 0
    while True:
        player = players[turn % len(players)]
        if player.bankrupt:
            print(f"{player.name} is bankrupt and skipped.")
            turn += 1
            continue

        input(f"\n🎲 {player.name}'s turn! Press Enter to roll dice...")
        dice = random.randint(1, 6) + random.randint(1, 6)
        print(f"{player.name} rolled a {dice}!")

        result = player.move(dice, board)
        print(result)
        print(f"New position: {player.position} | Coordinates: {player.coordinates}")
        print(f"Balance: ${player.balance}")

        # Temporary stop condition for testing
        if turn > 10:
            print("\n🛑 Ending demo after 10 turns.")
            break

        turn += 1

if __name__ == "__main__":
    main()
