class Utility:
    price = 150

    def __init__(self, name, owner=None, count_owned=1):
        self.name = name
        self._owner = owner
        self._mortgaged = False
        self.count_owned = count_owned

    def rent(self, dice_roll):
        if self._mortgaged:
            return 0
        multiplier = 4 if self.count_owned == 1 else 10
        return dice_roll * multiplier

    def purchase_price(self):
        return Utility.price
