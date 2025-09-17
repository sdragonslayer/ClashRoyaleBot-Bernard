rows = 32
col = 18
zeros_matrix = [[0 for _ in range(col)] for _ in range(rows)]

# 0: placeable for everything
# 1: only spells placeable 
# 2: unplaceable at all

#initalizing unplaceable places
for i in range(0, 6):
    zeros_matrix[0][i] = 2
    zeros_matrix[31][i] =  2
    zeros_matrix[0][17-i] = 2
    zeros_matrix[31][17-i] = 2

#initalializing only spells 

for i in range(4):
    for k in range(4):
        zeros_matrix[1+k][7+i] = 1
        zeros_matrix[27+k][7+i] = 1

for i in range(3):
    for k in range(3):
        zeros_matrix[5+k][2+i] = 1
        zeros_matrix[24+k][2+i] = 1
        zeros_matrix[5+k][13+i] = 1
        zeros_matrix[24+k][13+i] = 1

zeros_matrix[14][0] = 1
zeros_matrix[17][0] = 1
zeros_matrix[14][17] = 1
zeros_matrix[17][17] = 1 

for i in range(18):
    zeros_matrix[15][i] = 1
    zeros_matrix[16][i] = 1


print(zeros_matrix)

