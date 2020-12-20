# part 1
from collections import defaultdict, deque
f = open('input')
nums = deque([])
nums_set = defaultdict(int)
target = 0

for i in range(25):
    nums.append(int(f.readline().strip()))
    nums_set[nums[-1]] += 1

for line in f.readlines():
    target = int(line.strip())

    valid = False
    for num in nums:
        if target - num in nums_set and nums_set[target - num] > 0:
            valid = True
            break
    
    if not valid:        
        print(target)
        break

    nums_set[nums.popleft()] -= 1
    nums.append(target)
    nums_set[target] += 1

# part 2
f.seek(0)
rng = deque([])
total = 0

while total != target:
    if total > target:
        total -= rng.popleft()
    else:
        rng.append(int(f.readline().strip()))
        total += rng[-1]

print(max(rng) + min(rng))