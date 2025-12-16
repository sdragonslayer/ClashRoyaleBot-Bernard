import math

class Troop:
    def __init__(self, card_data, location, team):
        self.name = card_data["sc_key"]
        self.team = team
        self.elixir = card_data["elixir"]
        
        self.max_hp = card_data["combat_stats"]["hitpoints"]["11"]
        self.current_hp = self.max_hp
        self.damage_per_hit = card_data["combat_stats"]["damage"]["11"]
        self.hit_speed = card_data["mechanics"]["hit_speed"]
        self.dps = self.damage_per_hit / self.hit_speed
        
        self.attack_cooldown = 0.0
        self.speed = card_data["mechanics"]["speed"] / 60.0 
        self.range = card_data["mechanics"]["range"]
        self.is_flying = "Flying" in card_data.get("special_abilities", [])
        
        # necessary because giant targets buildings only
        self.is_giant = self.name.lower() == "giant"
        
        #tracking now done in objects
        self.location = list(location) 
        self.is_alive = True

    def take_damage(self, amount):
        """Simulates taking damage, so health tracking is now done within object"""
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0
            self.is_alive = False 
            
    def get_distance_to(self, target):
        """important because we need the actual distance between two troops"""
        if hasattr(target, 'location'):
            return math.sqrt((self.location[0] - target.location[0])**2 + 
                             (self.location[1] - target.location[1])**2)
        return float('inf')

    def get_distance_to_point(self, point):
        """used for pathing to points and such, especially for flying units"""
        return math.sqrt((self.location[0] - point[0])**2 + 
                         (self.location[1] - point[1])**2)



class Spell:
    def __init__(self, card_data, location):
        """normal init, same as before """
        self.name = card_data["sc_key"]
        self.elixir = card_data["elixir"]
        self.damage = card_data["combat_stats"]["damage"]["11"]
        self.radius = card_data["mechanics"]["radius"]
        self.location = list(location)

class Tower:
    # initating defaults here
    # as or right now, we are using direct damage 
    def __init__(self, card_data, location):
        self.hp = card_data["combat_stats"]["hitpoints"]["11"]
        self.dps = card_data["combat_stats"]["damage"]["11"] / card_data["mechanics"]["hit_speed"]["11"]
        self.range = card_data["mechanics"]["range"]["11"]
        self.tower_fallen = False 
        self.location = location


