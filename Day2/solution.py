# part 1
res = 0
f = open('input')

for line in f:
    line_items = line.split(' ')
    mn, mx = line_items[0].split('-')
    char = line_items[1][0]
    pwd = line_items[2]

    count = pwd.count(char)
    res += 1 if int(mn) <= count <= int(mx) else 0

print(res)

# part 2
res = 0
f = open('input')

for line in f:
    line_items = line.split(' ')
    first, second = list(map(int, line_items[0].split('-')))
    char = line_items[1][0]
    pwd = line_items[2]

    res += 1 if (pwd[first-1] == char) ^ (pwd[second-1] == char) else 0

print(res)