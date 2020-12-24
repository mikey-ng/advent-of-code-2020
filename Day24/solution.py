f = open(r'C:\Users\michael\Desktop\Projects\adventOfCode2020\Day24\input')

travel = {
    'e':  (2, 0),
    'w':  (-2, 0),
    'se': (1,-1),
    'sw': (-1, -1),
    'ne': (1, 1),
    'nw': (-1, 1)
}

lines = f.read().split('\n')
black_tiles = set([])
for line in lines:
    coords = (0, 0)
    n = len(line)
    i = 0
    while i < n:
        if line[i] in ('n', 's'):
            direction = line[i:i + 2]
            i += 2
        else:
            direction = line[i]
            i += 1

        # travel to next coordinates
        delta = travel[direction]
        coords = (coords[0] + delta[0], coords[1] + delta[1])

    # if tile is white, flip it to black and vice-versa
    key = coords
    if key not in black_tiles:
        black_tiles.add(key)
    else:
        black_tiles.remove(key)

# answer to part 1
print(len(black_tiles))

# count number of neighbouring black tiles
def get_neighbour_count(coords, black_tiles):
    (i, j) = coords
    deltas = [(2, 0), (-2, 0), (1,-1), (-1, -1), (1, 1), (-1, 1)]
    count = 0
    for x, y in deltas:
        if (i + x, j + y) in black_tiles:
            count += 1

    return count

# flip results from part 1 for 100 days
for i in range(100):
    next_black_tiles = set([])
    for coords in black_tiles:

        # rule 1: if black tiles have zero or more than neighbouring two black tile they flip to white
        # in other words if the number of neighbouring black tile is 1 or 2 it stays black
        if get_neighbour_count(coords, black_tiles) in (1,2):
            next_black_tiles.add(coords)

        # only white tiles with neighbouring black tiles can be flipped
        # it suffices to check if a neighbour of a black tile is white and the number of neighbouring black tiles
        deltas = [(2, 0), (-2, 0), (1,-1), (-1, -1), (1, 1), (-1, 1)]        
        for i, j in deltas:
            # rule 2: if a white tile has 2 neighbouring black tiles it flips to black
            neighbour = (coords[0] + i, coords[1] + j)
            if neighbour not in black_tiles and get_neighbour_count(neighbour, black_tiles) == 2:
                next_black_tiles.add(neighbour)
    black_tiles = next_black_tiles
    
print(len(black_tiles))