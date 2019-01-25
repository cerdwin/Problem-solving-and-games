def value_count(data, value):
    counter = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == value:
                counter = counter + 1
    return counter
 
 
def value_positions(data, value):
    placement = []
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == value:
                placement.append((i, j))
    return placement
 
#value = -1
#data = [[0, -1, 1], [-1, 0, -1], [1, 0, -1]]
#count = value_count(data, value)
#print(count)
 
#value = 0
#data = [[0, -1, 1], [-1, 0, -1], [1, 0, -1]]
#positions = value_positions(data, value)
#print(positions)
