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

    def __init__(self, name, state, buildings):
        self.name = name
        self.state = state  # "house", "hotel", or "railroad"
        self.buildings = buildings
        self.color = Property.color_table.get(name, "unknown")

    def rent(self):
        if self.state == "railroad":
            if self.buildings == 1:
                return 25
            elif self.buildings == 2:
                return 50
            elif self.buildings == 3:
                return 100
            elif self.buildings == 4:
                return 200
            else:
                return 0
        data = Property.rent_table.get(self.name)
        if not data:
            return 0
        if self.state == "house":
            if 0 <= self.buildings < len(data["house"]):
                return data["house"][self.buildings]
            else:
                return 0
        elif self.state == "hotel":
            return data["hotel"]
        return 0