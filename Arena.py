import json
import heapq

class Arena:
    def __init__(self, rows=32, cols=18):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        with open('cards.json', 'r') as clash:
            self.cards_data = json.load(clash)
        
        self.set_unplaceable()
        self.set_unplaceable_spell()
        
        # towerp ositions for targeting
        # team 1 - bottom, team 2 - top
        self.tower_positions = {
            1: {
                "king": [28.5, 8.5],
                "princess_left": [25, 3],
                "princess_right": [25, 14]
            },
            2: {
                "king": [2.5, 8.5],
                "princess_left": [6, 3],
                "princess_right": [6, 14]
            }
        }

    def get_card_data(self, card_name):
        """Get troop card data from cards.json"""
        for card in self.cards_data.get("troops", []):
            if card["sc_key"].lower().replace(" ", "") == card_name.lower().replace(" ", ""):
                return card
        return None
    
    def get_spell_data(self, spell_name):
        """Get spell card data from cards.json"""
        for spell in self.cards_data.get("spells", []):
            if spell["sc_key"].lower().replace(" ", "") == spell_name.lower().replace(" ", ""):
                return spell
        return None
    
    def get_tower_data(self, tower_type):
        """Get tower stats from cards.json"""
        for tower in self.cards_data.get("towers", []):
            if tower["sc_key"].lower() == tower_type.lower():
                return tower
    
    def get_enemy_tower_positions(self, team):
        """Get list of enemy tower positions for a team"""
        enemy_team = 2 if team == 1 else 1
        positions = self.tower_positions[enemy_team]
        return [positions["princess_left"], positions["princess_right"], positions["king"]]

    def set_unplaceable(self):
        # pretty much not placeable 
        for i in range(0, 6):
            self.board[0][i] = 2
            self.board[31][i] = 2
            self.board[0][17 - i] = 2
            self.board[31][17 - i] = 2

    def set_unplaceable_spell(self):
        # Places the king towers
        for i in range(4):
            for k in range(4):
                self.board[1 + k][7 + i] = 1   
                self.board[27 + k][7 + i] = 1  

        # Places the princess towers
        for i in range(3):
            for k in range(3):
                self.board[5 + k][2 + i] = 1    
                self.board[24 + k][2 + i] = 1  
                self.board[5 + k][13 + i] = 1   
                self.board[24 + k][13 + i] = 1  

        # more blocks
        self.board[14][0] = 1
        self.board[17][0] = 1
        self.board[14][17] = 1
        self.board[17][17] = 1

        # the river
        for c in range(self.cols):
            self.board[15][c] = 1
            self.board[16][c] = 1
        
        # bridges
        for r in [15, 16]:
            for c in range(2, 5):
                self.board[r][c] = 0
            for c in range(13, 16):
                self.board[r][c] = 0

    def is_walkable(self, r, c, is_flying=False):
        """Checks if a tile can be used, mostly for pathfinding. Of course, flying units can just fly anywhere lol"""
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        if is_flying:
            return True
        return self.board[r][c] == 0

    def find_path(self, start, end, is_flying=False):
        """Pathfinding using A*, was hard and had to take inspiration from stackoverflow, etc."""
        start = (int(start[0]), int(start[1]))
        end = (int(end[0]), int(end[1]))
        
        if is_flying:
            return [end]

        if not self.is_walkable(end[0], end[1], is_flying):
            valid = False
            for rad in range(1, 10):
                if valid:
                    break
                for dr in range(-rad, rad + 1):
                    if valid:
                        break
                    for dc in range(-rad, rad + 1):
                        new_end = (end[0] + dr, end[1] + dc)
                        if self.is_walkable(new_end[0], new_end[1], is_flying):
                            end = new_end
                            valid = True
                            break

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        
        def h(a, b):
            return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            neighbors = [
                (0,1), (0,-1), (1,0), (-1,0),
                (1,1), (1,-1), (-1,1), (-1,-1)
            ]
            
            #yeah implementation is here, but theory wise I am not too sure. this was kind hard. 
            for dr, dc in neighbors:
                neighbor = (current[0] + dr, current[1] + dc)
                
                if self.is_walkable(neighbor[0], neighbor[1], is_flying):
                    move_cost = 1 if (dr == 0 or dc == 0) else 1.414
                    tentative_g_score = g_score[current] + move_cost

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + h(neighbor, end)
                        heapq.heappush(open_set, (f_score, neighbor))
        
        return []

    def display(self):
        """displays arena visually"""
        print("Arena Map:")
        print("  " + "".join(f"{c:2}" for c in range(self.cols)))
        
        #pretty much same as before
        for r in range(self.rows):
            row_str = ""
            for c in range(self.cols):
                val = self.board[r][c]
                if val == 0:
                    row_str += "0"  
                elif val == 1:
                    row_str += "1"  
                else:
                    row_str += "2"  
            print(row_str)