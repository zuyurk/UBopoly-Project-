class Player:
    def __init__(self, name, starting_balance=1500, start_tile=0):
        self.name = name  # Player name
        self.balance = starting_balance  # Money (Bear Bucks)
        self.position = start_tile  # Board tile index (0 = GO)
        self.coordinates = (0, 0)  # (x, y) board coordinates for display
        self.properties = []  # List of owned properties
        self.in_jail = False  # Jail flag
        self.jail_turns = 0  # Turns spent in jail
        self.bankrupt = False  # Status flag

    def move(self, steps, board):
        """Move player around the board and update coordinates."""
        if self.in_jail:
            return f"{self.name} is in jail and can't move this turn."

        prev_position = self.position
        self.position = (self.position + steps) % len(board.tiles)

        # Check if passed GO
        passed_go = self.position < prev_position
        if passed_go:
            self.balance += 200

        # Update the player's on-screen coordinates
        self.coordinates = board.get_tile_coordinates(self.position)

        return (
            f"{self.name} passed GO! +$200"
            if passed_go
            else f"{self.name} moved {steps} spaces to {board.tiles[self.position]['name']}."
        )

    def buy_property(self, property):
        """Attempt to buy a property."""
        if self.balance >= property.price and not property.owner:
            self.balance -= property.price
            property.owner = self
            self.properties.append(property)
            return f"{self.name} bought {property.name} for ${property.price}."
        elif property.owner:
            return f"{property.name} is already owned."
        else:
            return f"{self.name} doesn't have enough money to buy {property.name}."

    def pay_rent(self, property):
        """Pay rent if another player owns the property."""
        if property.owner and property.owner != self:
            rent = property.rent
            if self.balance >= rent:
                self.balance -= rent
                property.owner.balance += rent
                return f"{self.name} paid ${rent} rent to {property.owner.name}."
            else:
                self.go_bankrupt(property.owner)
                return f"{self.name} couldn't afford rent and went bankrupt!"

    def go_bankrupt(self, creditor=None):
        """Handle bankruptcy."""
        self.bankrupt = True
        for prop in self.properties:
            prop.owner = creditor  # Transfer ownership
        self.properties.clear()
        self.balance = 0
        return f"{self.name} is bankrupt."

    def net_worth(self):
        """Calculate total net worth (cash + properties)."""
        total_property_value = sum(p.price for p in self.properties)
        return self.balance + total_property_value

    def __repr__(self):
        return f"<Player {self.name}: ${self.balance}, Pos={self.position}, Coords={self.coordinates}>"
