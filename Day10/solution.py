# part 1
f = open('input')
jolts = []
for line in f.readlines():
    jolts.append(int(line.strip()))

jolts.sort()
prev = 0
ones = 0
threes = 1

for jolt in jolts:
    if jolt - prev == 1:
        ones += 1
    elif jolt - prev == 3:
        threes += 1
    prev = jolt

print(ones * threes)

# part2

# no duplicates in input
jolts = set(jolts)
jolts.add(0)

def dfs(curr, jolts, memo, mx):
    if curr == mx:
        return 1
    elif curr in memo:
        return memo[curr]
    elif curr not in jolts:
        return 0

    memo[curr] = dfs(curr + 1, jolts, memo, mx) + dfs(curr + 2, jolts, memo, mx) + dfs(curr + 3, jolts, memo, mx)

    return memo[curr]

print(dfs(0, jolts, {}, max(jolts)))

