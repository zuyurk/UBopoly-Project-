class Board:
    def __init__(self):
        # Each tile has a name and coordinates (x%, y%)
        self.tiles = [
            {"name": "GO", "x": 90, "y": 90},
            {"name": "Mediterranean Ave", "x": 80, "y": 90},
            {"name": "Community Chest", "x": 70, "y": 90},
            {"name": "Baltic Ave", "x": 60, "y": 90},
            {"name": "Income Tax", "x": 50, "y": 90},
            {"name": "Reading Railroad", "x": 40, "y": 90},
            # ... continue defining all 40 tiles
        ]

    def get_tile_coordinates(self, tile_index):
        tile = self.tiles[tile_index % len(self.tiles)]
        return (tile["x"], tile["y"])
