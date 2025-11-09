from Objects.property import Property


class Player:
    GO_CASH = 200  # Money received when passing GO

    def __init__(self, name, starting_balance=1500, start_tile=0):
        self.name = name
        self.balance = starting_balance
        self.position = start_tile  # Board index
        self.coordinates = (0, 0)  # Optional: (x, y) for display
        self.properties = []  # List of Property/Railroad/Utility objects
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

        # Update coordinates (for UI)
        self.coordinates = board.get_tile_coordinates(self.position)

        return (
            f"{self.name} passed GO! +${Player.GO_CASH}"
            if passed_go
            else f"{self.name} moved {steps} spaces to {board.tiles[self.position]['name']}."
        )

    # ------------------------
    # Property Management
    # ------------------------
    def buy_property(self, prop):
        """Handles purchase for Property, Railroad, or Utility."""
        if prop.owner() is not None:
            return f"{prop.name} is already owned by {prop.owner().name}."
        if self.balance < prop.purchase_price():
            return f"{self.name} doesn't have enough money to buy {prop.name}."

        # Transaction
        self.balance -= prop.purchase_price()
        prop.transfer_owner(self)
        self.properties.append(prop)
        return f"{self.name} bought {prop.name} for ${prop.purchase_price()}."

    def pay_rent(self, prop, dice_roll=None):
        """Pays rent for any property type. Utility uses dice roll."""
        if not prop.owner() or prop.owner() == self:
            return None  # No rent to pay

        rent = prop.rent()
        # Utilities depend on dice roll
        if hasattr(prop, "rent") and "dice_roll" in prop.rent.__code__.co_varnames:
            rent = prop.rent(dice_roll)

        if self.balance >= rent:
            self.balance -= rent
            prop.owner().balance += rent
            return f"{self.name} paid ${rent} rent to {prop.owner().name} for {prop.name}."
        else:
            self.go_bankrupt(prop.owner())
            return f"{self.name} couldn't afford rent (${rent}) and went bankrupt!"

    def owns_full_color_set(self, color):
        """Check if player owns all properties of a specific color group."""
        color_properties = [p for p in self.properties if hasattr(p, "color") and p.color == color]
        total_color_count = sum(1 for c in Property.color_table.values() if c == color)
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
