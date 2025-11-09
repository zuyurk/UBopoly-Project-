class Property:
    color_table = {
        "Baird": "brown", "Clements": "brown",
        "Baldy": "light blue", "Jacobs": "light blue", "Park": "light blue",
        "O'Brian": "pink", "Norton": "pink", "Knox": "pink",
        "Bonner": "orange", "Talbert": "orange", "Hochstetter": "orange",
        "Cooke": "red", "Fronczak": "red", "NSC": "red",
        "Ketter": "yellow", "Slee": "yellow", "Furnas": "yellow",
        "The Commons": "green", "Center for the Arts": "green", "Alumni Arena": "green",
        "Davis": "dark blue", "Jarvis": "dark blue"
    }

    rent_table = {
        "Baird": {"house": [2, 10, 30, 90, 160], "hotel": 250},
        "Clements": {"house": [4, 20, 60, 180, 320], "hotel": 450},
        "Baldy": {"house": [6, 30, 90, 270, 400], "hotel": 550},
        "Jacobs": {"house": [6, 30, 90, 270, 400], "hotel": 550},
        "Park": {"house": [8, 40, 100, 300, 450], "hotel": 600},
        "O'Brian": {"house": [8, 40, 100, 300, 450], "hotel": 600},
        "Norton": {"house": [8, 40, 100, 300, 450], "hotel": 600},
        "Knox": {"house": [10, 50, 150, 450, 625], "hotel": 750},
        "Bonner": {"house": [10, 50, 150, 450, 625], "hotel": 750},
        "Talbert": {"house": [10, 50, 150, 450, 625], "hotel": 750},
        "Hochstetter": {"house": [12, 60, 180, 500, 700], "hotel": 750},
        "Cooke": {"house": [22, 110, 330, 800, 1000], "hotel": 900},
        "Fronczak": {"house": [22, 110, 330, 800, 1000], "hotel": 900},
        "NSC": {"house": [24, 120, 360, 850, 1050], "hotel": 950},
        "Ketter": {"house": [24, 120, 360, 850, 1050], "hotel": 950},
        "Slee": {"house": [26, 130, 390, 900, 1100], "hotel": 1000},
        "Furnas": {"house": [26, 130, 390, 900, 1100], "hotel": 1000},
        "The Commons": {"house": [28, 150, 450, 1000, 1200], "hotel": 1050},
        "Center for the Arts": {"house": [28, 150, 450, 1000, 1200], "hotel": 1050},
        "Alumni Arena": {"house": [30, 160, 500, 1100, 1300], "hotel": 1100},
        "Davis": {"house": [35, 175, 500, 1200, 1400], "hotel": 1200},
        "Jarvis": {"house": [50, 200, 600, 1400, 1700], "hotel": 1400}
    }

    purchase_prices = {
        "Baird": 60, "Clements": 60,
        "Baldy": 100, "Jacobs": 100, "Park": 120,
        "O'Brian": 140, "Norton": 140, "Knox": 160,
        "Bonner": 180, "Talbert": 180, "Hochstetter": 200,
        "Cooke": 220, "Fronczak": 220, "NSC": 240,
        "Ketter": 260, "Slee": 260, "Furnas": 280,
        "The Commons": 300, "Center for the Arts": 300, "Alumni Arena": 320,
        "Davis": 350, "Jarvis": 400
    }

    def __init__(self, name, buildings=0, owner=None):
        self.name = name
        self.color = Property.color_table[name]
        self.buildings = buildings
        self._owner = owner
        self._mortgaged = False
        self.state = "house"  # can be "house" or "hotel"

    def owner(self):
        return self._owner

    def transfer_owner(self, new_owner):
        self._owner = new_owner

    def mortgage(self):
        self._mortgaged = True

    def unmortgage(self):
        self._mortgaged = False

    def add_building(self):
        if self.buildings < 4:
            self.buildings += 1
        elif self.buildings == 4:
            self.state = "hotel"
            self.buildings = 1

    def rent(self):
        if self._mortgaged:
            return 0
        data = Property.rent_table[self.name]
        if self.state == "house":
            return data["house"][self.buildings]
        elif self.state == "hotel":
            return data["hotel"]
        return 0

    def purchase_price(self):
        return Property.purchase_prices[self.name]
