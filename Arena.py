# This initializes the matrix as placeable for everything everywhere

rows = 32
col = 18
zeros_matrix = [[0 for _ in range(col)] for _ in range(rows)]

# Key for making the arena 
# 0: placeable for everything
# 1: only spells placeable 
# 2: unplaceable at all

#initalizing unplaceable places for different troop types 

# This is setting the areas on the rows next to the king tower as unplaceable
for i in range(0, 6):
    zeros_matrix[0][i] = 2
    zeros_matrix[31][i] =  2
    zeros_matrix[0][17-i] = 2
    zeros_matrix[31][17-i] = 2

# initalializing only spells 

# This is setting the king towers as unplaceable for troops
for i in range(4):
    for k in range(4):
        zeros_matrix[1+k][7+i] = 1
        zeros_matrix[27+k][7+i] = 1

# This sets the princess towers as unplaceable for troops
for i in range(3):
    for k in range(3):
        zeros_matrix[5+k][2+i] = 1
        zeros_matrix[24+k][2+i] = 1
        zeros_matrix[5+k][13+i] = 1
        zeros_matrix[24+k][13+i] = 1

# This sets the tile in the corner next to the bridge as unplaceable for troops
zeros_matrix[14][0] = 1
zeros_matrix[17][0] = 1
zeros_matrix[14][17] = 1
zeros_matrix[17][17] = 1 

# This sets the bridge as unplaceable for troops
for i in range(18):
    zeros_matrix[15][i] = 1
    zeros_matrix[16][i] = 1



# Enemy unit inputs
# First Number = Unit Type
#   0 = Troop
#   1 = Building
#   2 = Spell
# Second Number  = Row Index
# Third Number = Column Index
# EX : 1 2 2 
# This would get the information to initalize a building in the tile 2 , 2
# Later on when we make classes for each unit we will replace the first input with the unit name
loc = str(input())

lcsplit = loc.split(" ")

if((zeros_matrix[int(lcsplit[1])][int(lcsplit[2])] == 0) and (lcsplit[0] == '0' or lcsplit[0] == '1')):
    print("success")
else:
    print("invalid placement")

print(zeros_matrix)

