# part 1
ship = [0, 0]
direction = [1, 0]
f = open('input')
for line in f.readlines():
    action, val = line[0], int(line[1:].strip())

    if action == 'N':
        ship[1] += val
    elif action == 'S':
        ship[1] -= val
    elif action == 'E':
        ship[0] += val
    elif action == 'W':
        ship[0] -= val
    elif action == 'F':
        ship[0] += val * direction[0]
        ship[1] += val * direction[1]
    else:
        for i in range(val // 90):
            if action == 'L':
                direction = [-direction[1], direction[0]]
            else:
                direction = [direction[1], -direction[0]]

f.close()
print(abs(ship[0]) + abs(ship[1]))

# part 2
ship = [0, 0]
waypoint = [10, 1]

f = open('input')
for line in f.readlines():
    action, val = line[0], int(line[1:].strip())

    if action == 'N':
        waypoint[1] += val
    elif action == 'S':
        waypoint[1] -= val
    elif action == 'E':
        waypoint[0] += val
    elif action == 'W':
        waypoint[0] -= val
    elif action == 'F':
        ship[0] += val * waypoint[0]
        ship[1] += val * waypoint[1]
    else:
        for i in range(val // 90):
            x, y = waypoint[0], waypoint[1]
            if action == 'L':
                waypoint = [-y, x]
            else:
                waypoint = [y, -x]

f.close()
print(abs(ship[0]) + abs(ship[1]))