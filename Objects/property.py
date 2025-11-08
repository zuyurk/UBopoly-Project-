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

    def __init__(self, name, state="house", buildings=0, owner=None):
        self.name = name
        self.state = state  # "house", "hotel", or "railroad"
        self.buildings = buildings
        self.color = Property.color_table[name]
        self._owner = owner
        self._mortgaged = False

    # ------------------------
    # Ownership / Mortgage
    # ------------------------
    def owner(self):
        return self._owner

    def transfer_owner(self, new_owner):
        self._owner = new_owner

    def is_mortgaged(self):
        return self._mortgaged

    def mortgage(self):
        if self._mortgaged:
            return "Already mortgaged"
        self._mortgaged = True
        return f"{self.name} is now mortgaged"

    def unmortgage(self):
        if not self._mortgaged:
            return "Property is not mortgaged"
        self._mortgaged = False
        return f"{self.name} is no longer mortgaged"

    # ------------------------
    # Buildings / State
    # ------------------------
    def add_building(self):
        if self.state != "house":
            return "Cannot add houses/hotel on this property"
        if self.buildings < 4:
            self.buildings += 1
            return f"House added! Total houses: {self.buildings}"
        else:
            return "Max houses reached (consider building a hotel)"

    def remove_building(self):
        if self.state != "house":
            return "No houses to remove"
        if self.buildings > 0:
            self.buildings -= 1
            return f"House removed. Total houses: {self.buildings}"
        return "No houses to remove"

    def build_hotel(self):
        if self.state == "hotel":
            return "Already have a hotel"
        elif self.buildings == 4:
            self.state = "hotel"
            self.buildings = 1  # Represents hotel
            return "Hotel built!"
        else:
            return "Need 4 houses to build a hotel"

    def remove_hotel(self):
        if self.state != "hotel":
            return "No hotel to remove"
        self.state = "house"
        self.buildings = 4
        return "Hotel removed, 4 houses restored"

    def number_of_buildings(self):
        return self.buildings

    def current_state(self):
        return self.state

    # ------------------------
    # Rent / Price
    # ------------------------
    def rent(self):
        if self._mortgaged:
            return 0
        if self.state == "railroad":
            railroad_rent = [25, 50, 100, 200]
            if 1 <= self.buildings <= 4:
                return railroad_rent[self.buildings - 1]
            return 0
        data = Property.rent_table.get(self.name)
        if not data:
            return 0
        if self.state == "house":
            if 0 <= self.buildings < len(data["house"]):
                return data["house"][self.buildings]
            return 0
        elif self.state == "hotel":
            return data["hotel"]
        return 0

    def purchase_price(self):
        return Property.purchase_prices.get(self.name, 0)

    # ------------------------
    # Display / Info
    # ------------------------
    def display_info(self):
        info = f"Property: {self.name}\n" \
               f"Color: {self.color}\n" \
               f"State: {self.state}\n" \
               f"Buildings: {self.buildings}\n" \
               f"Owner: {self._owner}\n" \
               f"Mortgaged: {self._mortgaged}\n" \
               f"Rent: {self.rent()}\n" \
               f"Purchase Price: {self.purchase_price()}"
        return info
