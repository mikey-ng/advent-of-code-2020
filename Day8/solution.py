f = open('input')
offsets = [0]
for line in f.readlines():
    offsets.append(len(line)+offsets[-1] + 1)

def process_instr(line):
    instr, val = line.strip().split(' ')
    val = int(val[1:]) if val[0] == '+' else -int(val[1:])
    return instr, val

# part 1
curr = 0
acc = 0
visited = set([])

while True:
    if curr in visited:
        break

    visited.add(curr)

    f.seek(offsets[curr])
    line = f.readline()
    instr, val = process_instr(line)

    if instr == 'acc':
        acc += val
        curr += 1
    elif instr == 'jmp':
        curr += val
    else:
        curr += 1

print(acc)

# part 2
def dfs(curr, pivoted, visited, acc, f, offsets):
    if curr in visited:
        return 0

    if curr == len(offsets) - 1:
        return acc

    f.seek(offsets[curr])
    instr, val = process_instr(f.readline())
    visited.add(curr)

    if instr == 'acc':
        res = dfs(curr + 1, pivoted, visited, acc + val, f, offsets)
    elif instr == 'jmp':
        if pivoted:
            res = dfs(curr + val, pivoted, visited, acc, f, offsets)
        else:
            res = dfs(curr + val, False, visited, acc, f, offsets) + dfs(curr + 1, True, visited, acc, f, offsets)
    else:
        if pivoted:
            res = dfs(curr + 1, pivoted, visited, acc, f, offsets)
        else:
            res = dfs(curr + 1, False, visited, acc, f, offsets) + dfs(curr + val, True, visited, acc, f, offsets)

    visited.remove(curr)

    return res

print(dfs(0, False, set([]), 0, f, offsets))
f.close()