f = open('input', 'r')
pos = 3
trees = 0

n = len(f.readline()) - 1
for line in f.readlines():
    if line[pos % n] == '#':
        trees += 1
    pos += 3

f.close()
print(trees)


def count_trees(right, down):
    f = open('input', 'r')
    pos = right
    trees = 0
    downCount = 0
    
    n = len(f.readline()) - 1
    for line in f.readlines():
        downCount += 1
        if downCount < down:
            continue
        else:
            downCount = 0

        if line[pos % n] == '#':
            trees += 1
        pos += right

    f.close()

    return trees

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
res = 1

for right, down in slopes:
    res *= count_trees(right, down)

print (res)

