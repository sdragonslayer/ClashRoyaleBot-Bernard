from cards import *
import json

class Arena:
    def __init__(self, rows=32, cols=18):
        """
        Initializes the Arena by setting up the board with all its rules.
        """
        self.rows = rows
        self.cols = cols
        # Initialize the board as placeable for everything everywhere
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        #gets our cards list 
        with open('cards.json', 'r') as clash:
            self.cards = json.load(clash)
        
        # Call private methods to set up restricted areas
        self._set_unplaceable_tiles()
        self._set_spell_only_tiles()

    def _set_unplaceable_tiles(self):
        """Sets the areas on the board that are completely unplaceable (value 2)."""
        # This is setting the areas on the far sides next to the king tower
        for i in range(0, 6):
            self.board[0][i] = 2
            self.board[31][i] = 2
            self.board[0][17 - i] = 2
            self.board[31][17 - i] = 2

    def _set_spell_only_tiles(self):
        """Sets the areas where only spells can be placed (value 1)."""
        # This sets the king towers as unplaceable for troops
        for i in range(4):
            for k in range(4):
                self.board[1 + k][7 + i] = 1
                self.board[27 + k][7 + i] = 1

        # This sets the princess towers as unplaceable for troops
        for i in range(3):
            for k in range(3):
                self.board[5 + k][2 + i] = 1
                self.board[24 + k][2 + i] = 1
                self.board[5 + k][13 + i] = 1
                self.board[24 + k][13 + i] = 1

        # This sets the tile in the corner next to the bridge as unplaceable for troops
        self.board[14][0] = 1
        self.board[17][0] = 1
        self.board[14][17] = 1
        self.board[17][17] = 1

        # This sets the bridge as unplaceable for troops
        for i in range(self.cols):
            self.board[15][i] = 1
            self.board[16][i] = 1

    #checks for valid placement 
    def check_valid_placement(self, troop_type, row, col):
        if (troop_type == 3):
            if(self.board[row][col] == 1 or self.board[row][col] == 0):
                return True
            return False
        else:
            if(self.board[row][col] == 0):
                return True
            return False
        
    #simple movement
    #takes in speed (tiles/sec), input coords
    #ground trooops time to bridge, flying troops time to princess tower 
    #assume input coords are on our side
    def simple_movement(self, type, speed, row_i, col_i):

        self.check_valid_placement(type, row_i, col_i)

        distance = ((row_i - row_f) ** 2 + (col_i-col_f) **2) ** (1/2)

        time = distance/speed

        return time 

    #display the board
    def display(self):
        """Prints a string representation of the board to the console."""
        for row in self.board:
            print(" ".join(map(str, row)))
    
            

if __name__ == "__main__":
    game_arena = Arena()
    game_arena.display()


    # Enemy unit inputs
    # First String = Troop name
    # First Number = Unit Type
    #   0 = Troop
    #   1 = Flying Troop
    #   2 = Building
    #   3 = Spell
    # Second Number  = Row Index
    # Third Number = Column Index
    # EX : knight 0 2 2 
    # This would get the information to initalize a building in the tile 2 , 2
    loc = str(input())
    name, type, row, col = loc.split(" ")

