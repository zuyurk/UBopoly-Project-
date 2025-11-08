class Player:
    GO_CASH = 200  # Money received when passing GO

    def __init__(self, name, starting_balance=1500, start_tile=0):
        self.name = name
        self.balance = starting_balance
        self.position = start_tile  # Board index
        self.coordinates = (0, 0)  # Optional: (x, y) for display
        self.properties = []  # List of Property objects
        self.in_jail = False
        self.jail_turns = 0
        self.bankrupt = False

    # ------------------------
    # Movement
    # ------------------------
    def move(self, steps, board):
        if self.in_jail:
            return f"{self.name} is in jail and can't move this turn."

        prev_position = self.position
        self.position = (self.position + steps) % len(board.tiles)

        # Check if passed GO
        passed_go = self.position < prev_position
        if passed_go:
            self.balance += Player.GO_CASH

        # Update coordinates (for UI purposes)
        self.coordinates = board.get_tile_coordinates(self.position)

        return (
            f"{self.name} passed GO! +${Player.GO_CASH}"
            if passed_go
            else f"{self.name} moved {steps} spaces to {board.tiles[self.position]['name']}."
        )

    # ------------------------
    # Property Management
    # ------------------------
    def buy_property(self, property):
        if self.balance >= property.purchase_price() and not property.owner():
            self.balance -= property.purchase_price()
            property.transfer_owner(self)
            self.properties.append(property)
            return f"{self.name} bought {property.name} for ${property.purchase_price()}."
        elif property.owner():
            return f"{property.name} is already owned by {property.owner().name}."
        else:
            return f"{self.name} doesn't have enough money to buy {property.name}."

    def pay_rent(self, property):
        if property.owner() and property.owner() != self:
            rent = property.rent()
            if self.balance >= rent:
                self.balance -= rent
                property.owner().balance += rent
                return f"{self.name} paid ${rent} rent to {property.owner().name}."
            else:
                self.go_bankrupt(property.owner())
                return f"{self.name} couldn't afford rent and went bankrupt!"

    def owns_full_color_set(self, color):
        """Check if player owns all properties of a specific color."""
        color_properties = [p for p in self.properties if p.color == color]
        # Compare count with total properties of that color
        total_color_count = sum(1 for p_name, c in Property.color_table.items() if c == color)
        return len(color_properties) == total_color_count

    # ------------------------
    # Bankruptcy
    # ------------------------
    def go_bankrupt(self, creditor=None):
        self.bankrupt = True
        for prop in self.properties:
            if creditor:
                prop.transfer_owner(creditor)
            else:
                prop.transfer_owner(None)
        self.properties.clear()
        self.balance = 0
        return f"{self.name} is bankrupt."

    # ------------------------
    # Money / Net Worth
    # ------------------------
    def net_worth(self):
        total_property_value = sum(p.purchase_price() for p in self.properties)
        return self.balance + total_property_value

    # ------------------------
    # Representation
    # ------------------------
    def __repr__(self):
        return f"<Player {self.name}: ${self.balance}, Pos={self.position}, Coords={self.coordinates}>"
