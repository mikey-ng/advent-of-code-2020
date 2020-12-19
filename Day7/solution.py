from collections import defaultdict

# part 1
graph = defaultdict(list)
f = open('input')
for line in f.readlines():

    # construct directed graph from child bag to parent bag
    src, dsts = line.strip().split(' contain ')
    for dst in dsts.split(', '):
        graph['-'.join(dst.split(' ')[1:3])].append('-'.join(src.split(' ')[:2]))

f.close()
visited = set([])
stack = graph['shiny-gold']
count = 0

while stack:
    curr = stack.pop()
    if curr in visited:
        continue

    visited.add(curr)

    for bag in graph[curr]:        
        stack.append(bag)

print(len(visited))

# part 2
graph = defaultdict(list)
f = open('input')
for line in f.readlines():

    # construct directed graph from parent bag to child bag
    src, dsts = line.strip().split(' contain ')
    for dst in dsts.split(', '):
        if dst[0].isnumeric():
            count, color1, color2, _ = dst.split(' ')
            graph['-'.join(src.split(' ')[:2])].append(('{}-{}'.format(color1, color2), int(count)))
f.close()

total_count = -1
stack = [('shiny-gold', 1)]
while stack:
    curr, curr_count = stack.pop()
    total_count += curr_count

    for bag, bag_count in graph[curr]:
        stack.append((bag, curr_count * bag_count))

print(total_count)