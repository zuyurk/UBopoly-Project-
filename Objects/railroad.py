class Railroad:
    rent_scale = [25, 50, 100, 200]
    price = 200

    def __init__(self, name, owner=None, count_owned=1):
        self.name = name
        self._owner = owner
        self._mortgaged = False
        self.count_owned = count_owned  # number of railroads owned

    def rent(self):
        if self._mortgaged:
            return 0
        return Railroad.rent_scale[min(self.count_owned, 4) - 1]

    def purchase_price(self):
        return Railroad.price
