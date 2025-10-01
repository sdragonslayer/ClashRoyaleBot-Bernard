class Troop:
    def __init__(self, card_data, location):
        self.elixer = card_data["elixer"]
        self.hp = card_data["combat_stats"]["hitpoints"]["11"]
        self.dps = card_data["combat_stats"]["damage"]["11"] / card_data["mechanics"]["hit_speed"]["11"]        
        # tiles / second
        self.speed = card_data["mechanics"]["speed"] / 60
        self.location = location
        self.counters = card_data["counters"]
        self.synergies = card_data["synergies"]    

class Spell:
    def __init__(self, card_data, location):
        self.elixir = card_data["elixir"]
        self.damage = card_data["combat_stats"]["damage"]["11"]
        self.crown_tower_damage = card_data["combat_stats"]["crown_tower_damage"]["11"]
        self.radius = card_data["mechanics"]["radius"]
        self.location = location
        self.knockback = "Knockback" in card_data["special_abilities"]
        self.counters = card_data["counters"]
        self.synergies = card_data["synergies"]

class Tower:
    # initating defaults of everything
    def __init__(self, card_data, location):
        self.hp = card_data["combat_stats"]["hitpoints"]["11"]
        self.dps = card_data["combat_stats"]["damage"]["11"] / card_data["mechanics"]["hit_speed"]["11"]
        self.range = card_data["mechanics"]["range"]["11"]
        self.tower_fallen = False 
        self.location = location


