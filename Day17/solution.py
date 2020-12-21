# part 1
f = open('input')
lines = f.read().split('\n')
f.close()

n = len(lines[0])
cycles = 6

# initial space
def get_space(n, cycles):
    return [[['.'] * (n + (2 * cycles)) for i in range(n + (2 * cycles))] for i in range((2 * cycles) + 1)]

def count_active(z, x, y, space):
    delta = (-1, 0, 1)
    count = 0

    l = len(space)
    n = len(space[0])
    m = len(space[0][0])

    for k in delta:
        for i in delta:
            for j in delta:
                if not i == j == k == 0 and 0 <= z + k < l and 0 <= x + i < n and 0 <= y + j < m:
                    if space[z + k][x + i][y + j] == '#':
                        count += 1

    return count

space = get_space(n, cycles)

# boards of active zone (z, x, y)
bounds = [cycles, cycles, cycles, cycles + n - 1, cycles, cycles + n - 1]

z = bounds[0]
x = bounds[2]
y = bounds[4]

for line in lines:
    for ch in line:
        space[z][x][y] = ch
        y += 1
    x += 1
    y = bounds[4]

for t in range(cycles):
    temp_space = get_space(n, cycles)
    temp_bounds = bounds.copy()
    for k in range(bounds[0] - 1, bounds[1] + 1 + 1):
        for i in range(bounds[2] - 1, bounds[3] + 1 + 1):
            for j in range(bounds[4] - 1, bounds[5] + 1 + 1):
                neighbours = count_active(k, i, j, space)
                if space[k][i][j] == '#' and neighbours in (2, 3):
                    temp_space[k][i][j] = '#'
                elif space[k][i][j] == '.' and neighbours == 3:
                    temp_space[k][i][j] = '#' 

                    # update bounds since new activation could be outside current bounds
                    temp_bounds[0] = min(temp_bounds[0], k)
                    temp_bounds[1] = max(temp_bounds[1], k)
                    temp_bounds[2] = min(temp_bounds[2], i)
                    temp_bounds[3] = max(temp_bounds[3], i)
                    temp_bounds[4] = min(temp_bounds[4], j)
                    temp_bounds[5] = max(temp_bounds[5], j)

    space = temp_space
    bounds = temp_bounds

count = 0
for k in range(bounds[0], bounds[1] + 1):
    for i in range(bounds[2], bounds[3] + 1):
        for j in range(bounds[4], bounds[5] + 1):
            if space[k][i][j] == '#':
                count += 1

print(count)

# part 2 - add one dimension
f = open('input')
lines = f.read().split('\n')
f.close()

n = len(lines[0])
cycles = 6

# initial space
def get_space(n, cycles):
    return [[[['.'] * (n + (2 * cycles)) for i in range(n + (2 * cycles))] for i in range((2 * cycles) + 1)] for i in range((2 * cycles) + 1)]

def count_active(w, z, x, y, space):
    delta = (-1, 0, 1)
    count = 0

    a = len(space)
    b = len(space[0])
    c = len(space[0][0])
    d = len(space[0][0][0])

    for l in delta:
        for k in delta:
            for i in delta:
                for j in delta:
                    if not i == j == k == l == 0 and 0 <= w + l < a and 0 <= z + k < b and 0 <= x + i < c and 0 <= y + j < d:
                        if space[w + l][z + k][x + i][y + j] == '#':
                            count += 1

    return count

space = get_space(n, cycles)

# boards of active zone (w,z, x, y)
bounds = [cycles, cycles, cycles, cycles, cycles, cycles + n - 1, cycles, cycles + n - 1]

w = bounds[0]
z = bounds[2]
x = bounds[4]
y = bounds[6]

for line in lines:
    for ch in line:
        space[w][z][x][y] = ch
        y += 1
    x += 1
    y = bounds[6]

for t in range(cycles):
    temp_space = get_space(n, cycles)
    temp_bounds = bounds.copy()
    for l in range(bounds[0] - 1, bounds[1] + 1 + 1):
    #for l in range(bounds[0], bounds[0] + 1):
        for k in range(bounds[2] - 1, bounds[3] + 1 + 1):
            for i in range(bounds[4] - 1, bounds[5] + 1 + 1):
                for j in range(bounds[6] - 1, bounds[7] + 1 + 1):
                    neighbours = count_active(l, k, i, j, space)
                    if space[l][k][i][j] == '#' and neighbours in (2, 3):
                        temp_space[l][k][i][j] = '#'
                    elif space[l][k][i][j] == '.' and neighbours == 3:
                        temp_space[l][k][i][j] = '#' 

                        # update bounds since new activation could be outside current bounds
                        temp_bounds[0] = min(temp_bounds[0], l)
                        temp_bounds[1] = max(temp_bounds[1], l)
                        temp_bounds[2] = min(temp_bounds[2], k)
                        temp_bounds[3] = max(temp_bounds[3], k)
                        temp_bounds[4] = min(temp_bounds[4], i)
                        temp_bounds[5] = max(temp_bounds[5], i)
                        temp_bounds[6] = min(temp_bounds[6], j)
                        temp_bounds[7] = max(temp_bounds[7], j)

    space = temp_space
    bounds = temp_bounds      

count = 0
for l in range(bounds[0], bounds[1] + 1):
    for k in range(bounds[2], bounds[3] + 1):
        for i in range(bounds[4], bounds[5] + 1):
            for j in range(bounds[6], bounds[7] + 1):
                if space[l][k][i][j] == '#':
                    count += 1

print(count)