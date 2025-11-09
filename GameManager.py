# GameManager.py
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# --- Board layout (clockwise from GO) must match page3.html tile IDs ---
TILES: List[str] = [
    "go",
    "baird", "community1", "clements", "saFees", "northBus",
    "baldy", "chance1", "jacobs", "park",
    "justVisiting",
    "obrian", "mtBanks", "norton", "knox", "southBus",
    "bonner", "community2", "talbert", "hochstetter",
    "freeParking",
    "cooke", "chance2", "fronczak", "nsc", "downtownBus",
    "ketter", "slee", "valmar", "furnas",
    "goToJail",
    "theCommons", "centerArts", "community3", "alumniArena", "shoppingBus",
    "chance3", "davis", "textbookFees", "jarvis",
]

# Buyable properties (simplified for gameplay)
BUYABLE = {
    "baird": 60, "clements": 60,
    "baldy": 100, "jacobs": 100, "park": 120,
    "obrian": 140, "norton": 140, "knox": 160,
    "bonner": 180, "talbert": 180, "hochstetter": 200,
    "cooke": 220, "fronczak": 220, "nsc": 240,
    "ketter": 260, "slee": 260, "furnas": 280,
    "theCommons": 300, "centerArts": 300, "alumniArena": 320,
    "davis": 350, "jarvis": 400,
}

RAILROADS = {"northBus", "southBus", "downtownBus", "shoppingBus"}  # treat as railroads
UTILS = set()  # add later if you introduce utilities

FEES = {"saFees": 200, "textbookFees": 100}

CHANCE = {"chance1", "chance2", "chance3"}
COMM = {"community1", "community2", "community3"}

CORNER_EVENTS = {
    "go": "collect_200",
    "justVisiting": "noop",
    "freeParking": "noop",
    "goToJail": "go_jail"
}

# Precompute ring coordinates (percent) for the 40 positions.
def _ring_coords() -> List[List[float]]:
    coords = []
    # Bottom row (GO at 100,100 to justVisiting at 0,100)
    for i in range(0, 11):  # 0..10
        x = 100 - (i * 10)
        y = 100
        coords.append([x, y])
    # Left column (0,100 to 0,0)
    for i in range(1, 11):  # 1..10
        x = 0
        y = 100 - (i * 10)
        coords.append([x, y])
    # Top row (0,0 to 100,0)
    for i in range(1, 11):
        x = i * 10
        y = 0
        coords.append([x, y])
    # Right column (100,0 to 100,100)
    for i in range(1, 11):
        x = 100
        y = i * 10
        coords.append([x, y])
    return coords[:40]  # drop duplicate GO

RING = _ring_coords()
ID_TO_INDEX: Dict[str, int] = {tid: i for i, tid in enumerate(TILES)}

def pos_to_coords(pos: int) -> List[float]:
    return RING[pos % 40]

@dataclass
class Player:
    name: str
    piece: Optional[str] = None
    balance: int = 1500
    position: int = 0
    in_jail: bool = False
    jail_turns: int = 0
    properties: List[str] = field(default_factory=list)
    cards: List[Dict] = field(default_factory=list)  # e.g., [{"id":"jail_free"}]

    def coords(self) -> List[float]:
        return pos_to_coords(self.position)

class Game:
    def __init__(self):
        self.players: List[Player] = []
        self.active: int = 0
        self.owners: Dict[str, int] = {}  # tile_id -> player index
        self.started: bool = False

    def _current(self) -> Player:
        return self.players[self.active]

    def _advance_turn(self):
        if self.players:
            self.active = (self.active + 1) % len(self.players)

    def _pass_go(self, old_pos: int, new_pos: int, p: Player):
        if (new_pos % 40) < (old_pos % 40):
            p.balance += 200

    def _land(self, p: Player, tile_id: str) -> str:
        if tile_id in CORNER_EVENTS:
            evt = CORNER_EVENTS[tile_id]
            if evt == "go_jail":
                p.in_jail = True
                p.jail_turns = 3
                p.position = ID_TO_INDEX["justVisiting"]
                return f"{p.name} was sent to Jail!"
            if evt == "collect_200":
                return f"{p.name} landed on GO."
            return f"{p.name} is just visiting."

        if tile_id in FEES:
            fee = FEES[tile_id]
            p.balance -= fee
            return f"{p.name} paid a fee of ${fee}."

        if tile_id in CHANCE:
            r = random.random()
            if r < 0.1:
                p.cards.append({"id": "jail_free", "name": "Get Out of Jail Free"})
                return f"{p.name} drew 'Get Out of Jail Free'!"
            elif r < 0.5:
                p.balance += 100
                return f"{p.name} received $100 from Chance."
            else:
                p.balance -= 100
                return f"{p.name} paid $100 from Chance."

        if tile_id in COMM:
            p.balance += 50
            return f"{p.name} received $50 from Community Chest."

        if tile_id in BUYABLE or tile_id in RAILROADS or tile_id in UTILS:
            if tile_id in self.owners:
                owner_idx = self.owners[tile_id]
                if owner_idx != self.active:
                    rent = self._calc_rent(tile_id, owner_idx)
                    p.balance -= rent
                    self.players[owner_idx].balance += rent
                    return f"{p.name} paid ${rent} rent to {self.players[owner_idx].name}."
                else:
                    return f"{p.name} landed on their own property."
            else:
                return f"{p.name} may buy {tile_id}."

        return f"{p.name} is taking a breather."

    def _calc_rent(self, tile_id: str, owner_idx: int) -> int:
        if tile_id in RAILROADS:
            owner = self.players[owner_idx]
            count = sum(1 for t in owner.properties if t in RAILROADS)
            return [25, 50, 100, 200][max(0, min(count - 1, 3))]
        price = BUYABLE.get(tile_id, 100)
        return max(10, (price // 10))

    # ---- API actions ----
    def init_players(self, player_specs: List[Dict]):
        self.players = []
        self.owners = {}
        self.active = 0
        for spec in player_specs:
            name = spec.get("name", "Player")
            piece = spec.get("piece")
            self.players.append(Player(name=name, piece=piece))
        self.started = True if self.players else False

    def roll(self) -> Dict:
        if not self.players:
            return {**self.serialize(), "error": "No players in game."}
        p = self._current()
        if p.in_jail:
            card_idx = next((i for i, c in enumerate(p.cards) if c.get("id") in {"jail_free", "cc_jail_free"}), None)
            if card_idx is not None:
                p.cards.pop(card_idx)
                p.in_jail = False
                p.jail_turns = 0
                msg = f"{p.name} used a Get Out of Jail Free card!"
                return {**self.serialize(), "roll": 0, "message": msg}
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            if d1 == d2:
                p.in_jail = False
                p.jail_turns = 0
                move = d1 + d2
                old = p.position
                p.position = (p.position + move) % 40
                self._pass_go(old, p.position, p)
                tile_id = TILES[p.position]
                msg = f"{p.name} rolled doubles {d1}+{d2} and left Jail. {self._land(p, tile_id)}"
                return {**self.serialize(), "roll": move, "message": msg}
            else:
                p.jail_turns -= 1
                if p.jail_turns <= 0:
                    p.balance -= 50
                    p.in_jail = False
                    p.jail_turns = 0
                    msg = f"{p.name} paid $50 jail fine and is free next turn."
                else:
                    msg = f"{p.name} failed to roll doubles ({d1}+{d2}). {p.jail_turns} turns left in Jail."
                return {**self.serialize(), "roll": d1 + d2, "message": msg}

        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        move = d1 + d2
        old = p.position
        p.position = (p.position + move) % 40
        self._pass_go(old, p.position, p)
        tile_id = TILES[p.position]
        msg = f"{p.name} rolled {d1}+{d2}. {self._land(p, tile_id)}"
        return {**self.serialize(), "roll": move, "message": msg}

    def buy(self) -> Dict:
        if not self.players:
            return {**self.serialize(), "error": "No players in game."}
        p = self._current()
        tile_id = TILES[p.position]
        if tile_id in self.owners:
            return {**self.serialize(), "error": "Already owned."}
        price = None
        if tile_id in BUYABLE:
            price = BUYABLE[tile_id]
        elif tile_id in RAILROADS:
            price = 200
        elif tile_id in UTILS:
            price = 150
        else:
            return {**self.serialize(), "error": "This tile is not buyable."}
        if p.balance < price:
            return {**self.serialize(), "error": "Insufficient funds."}
        p.balance -= price
        p.properties.append(tile_id)
        self.owners[tile_id] = self.active
        msg = f"{p.name} bought {tile_id} for ${price}."
        return {**self.serialize(), "message": msg}

    def use_card(self, card_id: Optional[str]) -> Dict:
        if not self.players:
            return {**self.serialize(), "error": "No players in game."}
        p = self._current()
        idx = next((i for i, c in enumerate(p.cards) if c.get("id") == card_id), None)
        if idx is None:
            return {**self.serialize(), "error": "You don't have that card."}
        card = p.cards.pop(idx)
        if card.get("id") in {"jail_free", "cc_jail_free"}:
            p.in_jail = False
            p.jail_turns = 0
            msg = f"{p.name} used Get Out of Jail Free."
            return {**self.serialize(), "message": msg}
        return {**self.serialize(), "error": "Unsupported card."}

    def end_turn(self) -> Dict:
        self._advance_turn()
        return {**self.serialize(), "next_player": self._current().name}

    def reset(self):
        for p in self.players:
            p.balance = 1500
            p.position = 0
            p.in_jail = False
            p.jail_turns = 0
            p.properties.clear()
            p.cards.clear()
        self.owners.clear()
        self.active = 0

    def serialize(self) -> Dict:
        return {
            "players": [
                {
                    "name": p.name,
                    "piece": p.piece,
                    "balance": p.balance,
                    "position": p.position,
                    "coords": p.coords(),  # [x%, y%]
                    "in_jail": p.in_jail,
                    "properties": list(p.properties),
                    "cards": list(p.cards),
                } for p in self.players
            ],
            "active_player": self.active,
        }

# Global singleton used by server.py
game = Game()
