from collections import defaultdict, Counter

class Tile:
    """
    Tile Object to hold image, borders and transformations

    Properties:
        id: Tile ID
        borders: binary hash of borders; list(4)
        mirrored_borders: binary has of mirrored borders; list(4)
        flipped: is the tile mirrored on verical axes
        rotation: number of clock-wise rotations
        img: original tile image

        border indices given rotation (r):
        normal tile:
            r = 0
                ___0___
                |      |
               3|      |1
                |______|
                   2
            r = 1
                ___3___
                |      |
               2|      |0
                |______|
                   1
            r = 2
                ___2___
                |      |
               1|      |3
                |______|
                   0
            r = 3
                ___1___
                |      |
               0|      |2
                |______|
                   3
        mirrored tile:
            r = 0
                ___0___
                |      |
               1|      |3
                |______|
                   2
            r = 1
                ___1___
                |      |
               2|      |0
                |______|
                   3
            r = 2
                ___2___
                |      |
               3|      |1
                |______|
                   0
            r = 3
                ___3___
                |      |
               0|      |2
                |______|
                   1

    """
    def __init__(self, id, borders, img):
        """
        Initialize Tile object

        Args:
            id (int): tile id
            borders (list): list of border hashes, even and odd indices represent forward and mirrored hashes 
            img (n x n list): tile image
        """
        self.id = id
        self.borders = [borders[x] for x in range(0, 7, 2)]
        self.mirrored_borders = [borders[x] for x in range(1, 8, 2)]
        self.mirrored_borders[1], self.mirrored_borders[3]  = self.mirrored_borders[3], self.mirrored_borders[1]
        self.flipped = False
        self.rotation = 0
        self.img = img

    def get_borders(self):
        """
        Generates and returns list of borders based on current transformation
        """
        borders = []
        if self.flipped:
            for i in range(4):
                borders.append(self.mirrored_borders[(-self.rotation + i) % 4])
        else:
            for i in range(4):
                borders.append(self.borders[(-self.rotation + i) % 4])

        return borders

    def get_img(self):
        def rotate(img):
            n = len(img)

            for i in range(n//2):
                for j in range(i, n-i-1):
                    temp = img[i][j]
                    img[i][j] = img[n - j - 1][i]
                    img[n - j - 1][i] = img[n - i - 1][n - j - 1]
                    img[n - i - 1][n - j - 1] = img[j][n - i - 1]
                    img[j][n - i - 1] = temp
        """
        Generates and returns img based on current transformation
        """
        if self.flipped:
            img = [list(reversed(line)) for line in self.img]
        else:
            img = [list(line) for line in self.img]

        for i in range(self.rotation):
            rotate(img)

        return img

    def reset(self):
        self.flipped = False
        self.rotation = 0

def hash(line):
    """
    Generate binary hashes where '#' and '.' represent '1' and '0'

    Ex. #.#. -> Forward Hash: 1010 = 10, Mirror Hash: 0101 = 5
    """
    n = len(line)
    hash_code = 0
    for ch in line:
        hash_code <<= 1
        if ch == '#':
            hash_code += 1

    rev_hash_code = 0
    for i in range(n):
        rev_hash_code <<= 1
        if line[n - i - 1] == '#':
            rev_hash_code += 1

    return [hash_code, rev_hash_code]

def place_tiles(i, j, puzzle, tiles, corners, edges, interiors, used, hashes, borders, unmatched):
    """
    Recusively places tiles

    Args:
        i (int): current row of puzzle
        j (int): current column of puzzle
        puzzle (n x n list): array of placements, -2 for position
        tiles (dict): dictionary of tile objects keyed by tile id
        corners (list): list of corner tile ids
        edges (list): list of edge tile ids
        interiors (list): list of interior tile ids
        used (set): set of used tiles
        hashes (dict): map border hashes from regular to mirrored and vice-versa, represents whether two borders line up 
        borders (dict): map borders hashes to tile ids
        unmatched (set): set of unmatched borders

    Returns:
        [bool]: flag to signify whether current tile is correctly placed
    """

    n = len(puzzle)

    # all border tiles have been placed
    if len(used) == n * n:
        return True

    # set source for tiles
    if (i, j) in ((0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)):
        src = corners
    elif i in (0, n - 1) or j in (0, n - 1):
        src = edges
    else:
        src = interiors

    # get list of adjacent pieces, -2 if none
    reqs = []
    for x, y in zip((-1, 0, 1, 0), (0, 1, 0, -1)):
            if 0 <= i + x < n and 0 <= j + y < n:
                reqs.append(puzzle[i + x][j + y])
            else:
                reqs.append(-2)
    
    # set border requirements according to adjacent tiles
    for x in range(4):
        if reqs[x] >= 0:
            reqs[x] = hashes[tiles[reqs[x]].get_borders()[(x + 2) % 4]]

    # set border requirement according puzzle border
    if i == 0:
        reqs[0] = -1
    if j == n - 1:
        reqs[1] = -1
    if i == n - 1:
        reqs[2] = -1
    if j == 0:
        reqs[3] = -1

    n_tiles = len(src)
    for idx in range(n_tiles):
        tile_id = src[idx]
        if tile_id not in used and tile_id != 'x':
            for id in (tile_id, -tile_id):
            
                valid = True
                tile = tiles[tile_id]

                # check if candidate tile has right borders
                for req in reqs:
                    if req >= 0 and (id not in borders[req]):
                        valid = False
                        break
                
                # check order of the borders on candidate tile
                if valid:       

                    # get candidate tile borders             
                    if id < 0:
                        tile.flipped = True
                    tile_borders = tile.get_borders()

                    # flag unmatched borders on candidate
                    for x in range(4):
                        if tile_borders[x] in unmatched:
                            tile_borders[x] = -1
                    
                    # check if border requirements can be fulfilled by rotating tile
                    valid = False
                    target = len([x for x in reqs if x >= -1])
                    for x in range(4):
                        m = 0
                        for y in range(4):
                            if reqs[(x + y) % 4] == tile_borders[y]:
                                m += 1                            
                            if m == target:
                                valid = True
                                tile.rotation = x
                                break
                        if valid:
                            break

                # place candidate tile and proceed to place next tile
                if valid:                
                    src[idx] = 'x'
                    used.add(tile_id)
                    
                    puzzle[i][j] = tile_id
                    
                    if j == n - 1:
                        next_loc = (i + 1, 0)
                    else:
                        next_loc = (i, j + 1)

                    placed = place_tiles(next_loc[0], next_loc[1], puzzle, tiles, corners, edges, interiors, used, hashes, borders, unmatched)

                    # next tile was placed successfully return
                    if placed:
                        return True

                    # candidate tile was wrong, undo placement and try another
                    puzzle[i][j] = -2
                    used.remove(tile_id)
                    src[idx] = tile_id

                # reset transformations done on candidate tile
                tile.reset()

    return False

def find_monster(photo, coords, n, m):
    """
    Counts number of '#' occupied by monster as defined by pattern in coords

    Args:
        photo (n x n list): photo
        coords (list(tuple)): monster pattern
        n (int): height of pattern
        m (int): width of pattern
    """

    locs = set([])
    n_photo = len(photo)

    for i in range(n_photo - n + 1):
        for j in range(n_photo - m + 1):
            curr_locs = set([])
            for (x, y) in coords:
                if photo[i + x][j + y] == '#':
                    curr_locs.add((i + x, j + y))

            if len(curr_locs) == len(coords):
                locs = locs.union(curr_locs)

    return len(locs)

def flip_coords(coords, n, m, axis):
    """
    Returns a list of coordinates rotated around a specified central axis

    Args:
        coords (list): list of original coordinates, left-top most point is (0,0)
        n (int): height range of coordinates
        m (int): width range of coordinates
        axis (0 or 1): central axis, 0 (horizonal), 1 (vertical)

    Returns:
        [list]: list of flipped coordinates
    """
    new_coords = []

    # flip around middle row
    if axis == 0:
        for (x, y) in coords:
            new_coords.append((x, m - y - 1))
    # flip around middle column
    elif axis == 1:
        for (x, y) in coords:
            new_coords.append((n - x - 1, y))
    return new_coords

f = open('input')
tiles_input = f.read().split('\n\n')
n_tiles = len(tiles_input)

borders = defaultdict(set)
hashes = {}
tiles = {}

# read input to create tile objects
for tile in tiles_input:
    lines = tile.split('\n')

    tile_id = int(lines[0][5:len(lines[0])-1])

    n = len(lines)

    # create list of clock-wise border hashes 
    # top:      read left->right
    # right:    read top->bottom
    # bottom:   read right->left
    # left:     read bottom->top
    # (opposite for mirrored )
    codes = []
    codes +=hash(lines[1][:])
    codes +=hash([lines[i][-1] for i in range(1, n)])
    codes +=hash([lines[-1][n - i - 2] for i in range(n - 1)])
    codes +=hash([lines[n - i - 1][0] for i in range(n - 1)])

    # create tile object
    tiles[tile_id] = Tile(tile_id, codes, lines[1:])
    
    for i in range(0, 7, 2):
        # map of hash-rev hash to match borders with
        hashes[codes[i]] = codes[i + 1]
        hashes[codes[i + 1]] = codes[i]

        # map of borders to tiles
        borders[codes[i]].add(tile_id)
        borders[codes[i + 1]].add(-tile_id)

# build sets of corner, edge, and interior tiles
unmatched = set([])
border_tiles = []
interiors = set([])
for border, tile_list in borders.items():
    if len(tile_list) == 1:
        tile_id = list(tile_list)[0]
        if tile_id >= 0:
            border_tiles.append(tile_id)
        unmatched.add(border)
    else:
        for tile_id in list(tile_list):
            if tile_id >= 0:
                interiors.add(tile_id)

c = Counter(border_tiles)
corners = []
edges = []
prod = 1
for tile_id, count in c.items():
    if count == 2:
        prod *= tile_id
        corners.append(tile_id)
    else:
        edges.append(tile_id)

# solution to part 1
print(prod)

for tile_id in corners:
    interiors.remove(tile_id)
for tile_id in edges:
    interiors.remove(tile_id)
interiors = list(interiors)

# solve puzzle to determine tile placements
n_border = int(n_tiles ** 0.5)
puzzle = [[-2] * n_border for i in range(n_border)]
place_tiles(0, 0, puzzle, tiles, corners, edges, interiors, set([]), hashes, borders, unmatched)

# get transformed images for each tile
images = {}
for tile_id in tiles:
    tile = tiles[tile_id]

    images[tile_id] = tile.get_img()

# build photo from transformed tiles
n_tile = len(images[tile_id]) - 2
n_photo = n_tile * n_border
photo = [['.'] * n_photo for i in range(n_photo)]
hash_count = 0
for i in range(n_photo):
    for j in range(n_photo):
        x = i // n_tile
        y = j // n_tile
        tile_id = puzzle[x][y]

        k = i % n_tile
        l = j % n_tile
        photo[i][j] = images[tile_id][k+1][l+1]

        if photo[i][j] == '#':
            hash_count += 1

"""
Generate possible orientations of the monster:
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""
# generate horizontal monster patterns by flipping around central axes
h_monster = [[
    (0,18),(1,0),(1,5),(1,6),(1,11),(1,12),(1,17),(1,18),(1,19),(2,1),(2,4),(2,7),(2,10),(2,13),(2,16)
]]
h_monster.append(flip_coords(h_monster[-1], 3, 20, 0))
h_monster.append(flip_coords(h_monster[-1], 3, 20, 1))
h_monster.append(flip_coords(h_monster[-1], 3, 20, 0))

# pivot horizontal monster pattern around diag(1,1) to generate first vertical monster pattern
# generate vertical monster patterns by flipping around central axes
v_monster = [[(y,x) for (x,y) in h_monster[0]]]
v_monster.append(flip_coords(v_monster[-1], 20, 3, 0))
v_monster.append(flip_coords(v_monster[-1], 20, 3, 1))
v_monster.append(flip_coords(v_monster[-1], 20, 3, 0))

# count hashes (#) occupied by monster
monster_hash_count = 0
for monster in v_monster:
    monster_hash_count = max(monster_hash_count, find_monster(photo, monster, 20, 3))
for monster in h_monster:
    monster_hash_count = max(monster_hash_count, find_monster(photo, monster, 3, 20))

# solution to part 2
print(hash_count - monster_hash_count)
