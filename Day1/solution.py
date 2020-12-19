# part 1
f = open('input')
nums = set([])
for line in f:
    if 2020 - int(line) in nums:
        print ((2020 - int(line)) * int(line))
        break
    nums.add(int(line))

# part2
f = open('input')
nums = []
for line in f:
    nums.append(int(line))

n = len(nums)
two_sum = {}

for i in range(n):
    for j in range(i + 1, n):
        two_sum[nums[i] + nums[j]] = (i, j)

for num in nums:
    if 2020 - num in two_sum:
        i, j = two_sum[2020 - num]
        print(num * nums[i] * nums[j])
        break