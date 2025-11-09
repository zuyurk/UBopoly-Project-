class Board:
    def __init__(self):
        self.tile_names = [
            "GO", "Baird", "Community Chest", "Clements", "SA Fees", "North Bus",
            "Baldy", "Chance", "Jacobs", "Park",
            "Just Visiting", "O'Brian", "M & T Banks", "Norton", "Knox",
            "South Bus", "Bonner", "Community Chest", "Talbert", "Hochstetter",
            "Free Parking", "Cooke", "Chance", "Fronczak", "NSC",
            "Downtown Bus", "Ketter", "Slee", "Valmar", "Go to Academic Violation",
            "The Commons", "Center for the Arts", "Community Chest", "Alumni Arena",
            "Shopping Bus", "Chance", "Davis", "Textbook Fees", "Jarvis"
        ]

        self.tiles = []
        self._generate_coordinates()

        # Mapping JS HTML tile IDs -> Python tile names
        self.html_to_py = {
            # bottom row
            "go": "GO", "baird": "Baird", "community1": "Community Chest", "clements": "Clements",
            "saFees": "SA Fees", "northBus": "North Bus", "baldy": "Baldy", "chance1": "Chance",
            "jacobs": "Jacobs", "park": "Park", "justVisiting": "Just Visiting",
            # left column
            "obrian": "O'Brian", "mtBanks": "M & T Banks", "norton": "Norton", "knox": "Knox",
            "southBus": "South Bus", "bonner": "Bonner", "community2": "Community Chest",
            "talbert": "Talbert", "hochstetter": "Hochstetter",
            # top row
            "freeParking": "Free Parking", "cooke": "Cooke", "chance2": "Chance",
            "fronczak": "Fronczak", "nsc": "NSC", "downtownBus": "Downtown Bus", 
            "ketter": "Ketter", "slee": "Slee", "valmar": "Valmar", "furnas": "Go to Academic Violation",
            "goToJail": "Go to Academic Violation",
            # right column
            "theCommons": "The Commons", "centerArts": "Center for the Arts", "community3": "Community Chest",
            "alumniArena": "Alumni Arena", "shoppingBus": "Shopping Bus", "chance3": "Chance",
            "davis": "Davis", "textbookFees": "Textbook Fees", "jarvis": "Jarvis"
        }

    def _generate_coordinates(self):
        """Generate rectangular board coordinates for each tile."""
        size = 100  # Board width/height
        step = size // 10  # Approx 10 tiles per side

        # Bottom row: GO -> Park (index 0-9), Just Visiting (index 10)
        for i in range(0, 11):
            x = size - i * step
            y = size
            self.tiles.append({"name": self.tile_names[i], "x": x, "y": y})

        # Left column: Just Visiting -> Hochstetter (index 11-21)
        for i in range(11, 22):
            x = 0
            y = size - (i - 10) * step
            self.tiles.append({"name": self.tile_names[i], "x": x, "y": y})

        # Top row: Free Parking -> Go to Academic Violation (index 22-31)
        for i in range(22, 32):
            x = (i - 22) * step
            y = 0
            self.tiles.append({"name": self.tile_names[i], "x": x, "y": y})

        # Right column: The Commons -> Jarvis (index 32–end)
        for i in range(32, len(self.tile_names)):
            x = size
            y = (i - 32 + 1) * step
            self.tiles.append({"name": self.tile_names[i], "x": x, "y": y})

    def get_tile_coordinates(self, tile_index):
        tile = self.tiles[tile_index % len(self.tiles)]
        return (tile["x"], tile["y"])

    def get_tile(self, tile_index):
        return self.tiles[tile_index % len(self.tiles)]

    def get_coords_from_html_index(self, html_index):
        """Get Python coordinates using JS/HTML tile index from PATH array."""
        if html_index not in self.html_to_py:
            raise ValueError(f"No mapping for HTML tile ID '{html_index}'")
        py_name = self.html_to_py[html_index]
        py_index = next(i for i, t in enumerate(self.tiles) if t["name"] == py_name)
        return self.get_tile_coordinates(py_index)
