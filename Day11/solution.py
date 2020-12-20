# part 1
def adj_count(i, j, grid):
    n = len(grid)
    m = len(grid[0])
    count = 0
    for k in (-1, 0, 1):
        for l in (-1, 0, 1):
            if (k != 0 or l != 0) and 0 <= i + k < n and 0 <= j + l < m and grid[i + k][j + l] == '#':
                count += 1

    return count

f = open('input')

layout = []
for line in f.readlines():
    layout.append(list(line.strip()))

f.close()

cache = [[], []]
n = len(layout)
m = len(layout[0])
delta = 1

while delta > 0:
    delta = 0
    for i in range(n):
        for j in range(m):
            if layout[i][j] == 'L' and adj_count(i, j, layout) == 0:
                cache[1].append('#')
                delta += 1
            elif layout[i][j] == '#' and adj_count(i, j, layout) >= 4:
                cache[1].append('L')
                delta += 1
            else:
                cache[1].append(layout[i][j])

        if i >= 1:
            layout[i - 1] = cache[0].copy()

        cache[0], cache[1] = cache[1], []

    layout[-1] = cache[0].copy()

res = 0
for row in layout:
    for col in row:
        if col == '#':
            res += 1 

print(res)

# part 2
def vis_count(i, j, grid):
    n = len(grid)
    m = len(grid[0])
    count = 0
    for k in (-1, 0, 1):
        for l in (-1, 0, 1):
            if count == 5:
                return count

            r =  i + k
            c = j + l
            if k != 0 or l != 0:
                while 0 <= r < n and 0 <= c < m and grid[r][c] == '.':
                    r += k
                    c += l
                if 0 <= r < n and 0 <= c < m and grid[r][c] == '#':
                    count += 1

    return count 

f = open('input')

layout = []
for line in f.readlines():
    layout.append(list(line.strip()))

f.close()

n = len(layout)
m = len(layout[0])
cache = [['.']*m for i in range(n)]
delta = 3

while delta > 0:
    # delta -= 1
    delta = 0
    for i in range(n):
        for j in range(m):
            if layout[i][j] == 'L' and vis_count(i, j, layout) == 0:
                cache[i][j] = '#'
                delta += 1
            elif layout[i][j] == '#' and vis_count(i, j, layout) >= 5:
                cache[i][j] = 'L'
                delta += 1
            else:
                cache[i][j] = layout[i][j]

    layout = cache
    cache = [['.']*m for i in range(n)]

res = 0
for row in layout:
    for col in row:
        if col == '#':
            res += 1 

print(res)