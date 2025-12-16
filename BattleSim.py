import math
from Arena import Arena
from cards import Troop, Spell

class BattleSimulation:
    def __init__(self):
        #inits
        self.arena = Arena()
        self.team1_troops = []
        self.team2_troops = []
        self.game_over = False
        self.time_elapsed = 0
        self.dt = 0.5
        
        # tower attack
        self.tower_cooldowns = {1: {}, 2: {}}
        
        # getting tower stats, to shoot arrows
        princess_data = self.arena.get_tower_data("TowerPrincess")
        self.tower_damage = princess_data["combat_stats"]["damage"]["11"]
        self.tower_hit_speed = princess_data["mechanics"]["hit_speed"]
        self.tower_range = princess_data["mechanics"]["range"]

    def spawn_unit(self, team, name, row, col):
        """Quite obvious, just spawns a troop in the sim"""
        data = self.arena.get_card_data(name)

        count = data["mechanics"]["count"]
        print(f"Spawning {count}x {name} for Team {team} at ({row}, {col})")
        
        for i in range(count):
            offset_c = (i - (count-1)/2) * 0.5

            #using troop class
            unit = Troop(data, [row, col + offset_c], team)
            
            if team == 1:
                self.team1_troops.append(unit)
            else:
                self.team2_troops.append(unit)
    
    def cast_spell(self, team, spell_name, row, col):
        """casts a spell to damage all the troops near it"""
        spell_data = self.arena.get_spell_data(spell_name)
        
        #using spell class 
        spell = Spell(spell_data, [row, col])
        print(f"[{self.time_elapsed:.1f}s] Team {team} casts {spell.name}")
        
        enemy_troops = self.team2_troops if team == 1 else self.team1_troops
        
        #logic to damage trools
        for troop in enemy_troops:
            if not troop.is_alive:
                continue
            dist = troop.get_distance_to_point([row, col])
            if dist <= spell.radius:
                print(f" Gets {troop.name}(T{troop.team}) for {spell.damage} dmg")
                troop.take_damage(spell.damage)
                if not troop.is_alive:
                    print(f"{troop.name}(T{troop.team}) is ded")

    def get_nearest_enemy(self, unit):
        """gets the nearest enemy troop"""
        enemies = self.team2_troops if unit.team == 1 else self.team1_troops
        alive_enemies = [e for e in enemies if e.is_alive]
        
        if not alive_enemies:
            return None, float('inf')
        
        nearest = None
        min_dist = float('inf')
        for enemy in alive_enemies:
            dist = unit.get_distance_to(enemy)
            if dist < min_dist:
                min_dist = dist
                nearest = enemy
        return nearest, min_dist
    
    def get_nearest_enemy_tower_pos(self, unit):
        """gets nearest enemy tower, especially useful for giant"""
        tower_positions = self.arena.get_enemy_tower_positions(unit.team)
        
        nearest_pos = None
        min_dist = float('inf')
        for pos in tower_positions:
            dist = unit.get_distance_to_point(pos)
            if dist < min_dist:
                min_dist = dist
                nearest_pos = pos
        return nearest_pos, min_dist
    
    def is_past_bridge(self, unit):
        """checks if bridge is crossed, which is crucial for having the tower actually shoot"""
        if unit.team == 1:
            return unit.location[0] < 15 
        else:
            return unit.location[0] > 16 
    
    def update_tower_attacks(self):
        """towers do damage"""
        # Team 1 towers shoot Team 2 troops
        self.tower_attacks(1, self.team2_troops)
        # Team 2 towers shoot Team 1 troops
        self.tower_attacks(2, self.team1_troops)
    
    def tower_attacks(self, tower_team, enemy_troops):
        """Process tower attacks for one team"""
        tower_positions = self.arena.tower_positions[tower_team]
        
        # sees if bridge crossed
        enemies_past_bridge = [t for t in enemy_troops if t.is_alive and self.is_past_bridge(t)]
        if not enemies_past_bridge:
            return
        
        for tower_name, tower_pos in tower_positions.items():

            if tower_name not in self.tower_cooldowns[tower_team]:
                self.tower_cooldowns[tower_team][tower_name] = 0
            
            if self.tower_cooldowns[tower_team][tower_name] > 0:
                self.tower_cooldowns[tower_team][tower_name] -= self.dt
                continue
            
            # Find closest enemy in range
            closest = None
            closest_dist = float('inf')
            for enemy in enemies_past_bridge:
                dist = math.sqrt((enemy.location[0] - tower_pos[0])**2 + 
                                (enemy.location[1] - tower_pos[1])**2)
                if dist <= self.tower_range and dist < closest_dist:
                    closest = enemy
                    closest_dist = dist
            
            if closest:
                print(f"[{self.time_elapsed:.1f}s] {tower_name}(T{tower_team}) shoots {closest.name}(T{closest.team}) for {self.tower_damage} dmg")
                closest.take_damage(self.tower_damage)
                self.tower_cooldowns[tower_team][tower_name] = self.tower_hit_speed
                
                if not closest.is_alive:
                    print(f"[{self.time_elapsed:.1f}s] {closest.name}(T{closest.team}) is also ded")

    def move_unit(self, unit, target_pos):
        """actual movement unit based on the path"""
        path = self.arena.find_path(unit.location, target_pos, unit.is_flying)
        if path:
            next_node = path[0]
            dx = next_node[0] - unit.location[0]
            dy = next_node[1] - unit.location[1]
            move_dist = (dx**2 + dy**2)**0.5
            
            if move_dist > 0:
                max_move = unit.speed * self.dt
                ratio = min(max_move, move_dist) / move_dist
                unit.location[0] += dx * ratio
                unit.location[1] += dy * ratio

    def update_game_state(self):
        #game loop updating
        all_units = self.team1_troops + self.team2_troops
        
        alive_t1 = [u for u in self.team1_troops if u.is_alive]
        alive_t2 = [u for u in self.team2_troops if u.is_alive]
        
        if not alive_t1 and not alive_t2:
            self.game_over = True
            return

        #tower attacks first
        self.update_tower_attacks()

        for unit in all_units:
            if not unit.is_alive:
                continue
            
            if unit.attack_cooldown > 0:
                unit.attack_cooldown -= self.dt

            # only for giant, because giant is different
            if unit.is_giant:
                tower_pos, distance = self.get_nearest_enemy_tower_pos(unit)
                if tower_pos:
                    if distance <= unit.range:
                        if unit.attack_cooldown <= 0:
                            print(f"[{self.time_elapsed:.1f}s] {unit.name}(T{unit.team}) attacks tower for {unit.damage_per_hit} dmg")
                            unit.attack_cooldown = unit.hit_speed
                    else:
                        self.move_unit(unit, tower_pos)
            
            # regular troops
            else:
                target, distance = self.get_nearest_enemy(unit)
                
                if target:
                    if distance <= unit.range:
                        if unit.attack_cooldown <= 0:
                            print(f"[{self.time_elapsed:.1f}s] {unit.name}(T{unit.team}) attacks {target.name}(T{target.team}) for {unit.damage_per_hit} dmg")
                            target.take_damage(unit.damage_per_hit)
                            unit.attack_cooldown = unit.hit_speed
                            
                            if not target.is_alive:
                                print(f"[{self.time_elapsed:.1f}s] {target.name}(T{target.team}) ded too")
                    else:
                        self.move_unit(unit, target.location)
                else:
                    # go to tower
                    tower_pos, _ = self.get_nearest_enemy_tower_pos(unit)
                    if tower_pos:
                        self.move_unit(unit, tower_pos)

        # finalized after run
        self.team1_troops = [u for u in self.team1_troops if u.is_alive]
        self.team2_troops = [u for u in self.team2_troops if u.is_alive]

    def run_scenario(self, scenario_name, max_time=60):
        #intiuitive demo

        print(f"Scenario: {scenario_name}")
        
        self.game_over = False
        self.time_elapsed = 0
        
        while not self.game_over and self.time_elapsed < max_time:
            self.update_game_state()
            self.time_elapsed += self.dt
            
        print(f" Game Over at {self.time_elapsed:.1f}s ")
        print("Surviving troops:")
        for u in self.team1_troops + self.team2_troops:
            print(f"  {u}")


if __name__ == "__main__":
    #  Giant ignores archers, paths to tower
    sim = BattleSimulation()
    sim.spawn_unit(1, "Giant", 20, 3)
    sim.spawn_unit(2, "Archers", 14, 3)
    sim.run_scenario("Giant vs Archers", max_time=30)
    
    # Tower shoots goblins that cross bridge
    print("\n")
    sim2 = BattleSimulation()
    sim2.spawn_unit(1, "Knight", 18, 3)
    sim2.spawn_unit(2, "Goblins", 10, 3)
    sim2.run_scenario("Knight vs Tower", max_time=20)
