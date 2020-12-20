# part 1
f = open('input')
arr = int(f.readline().strip())
buses = []
for id in f.readline().strip().split(','):
    if id != 'x':
        buses.append(int(id))
n = len(buses)

times = [0]*n
for i in range(n):
    while times[i] < arr:
        times[i] += buses[i]

mn = float('inf')
idx = -1

for i in range(n):
    if times[i] < mn:
        mn = times[i]
        idx = i

print((mn - arr) * buses[idx])

# part 2
# http://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
from functools import reduce
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

x = 0
buses = []
gaps = []

f = open('input')
f.readline()

for id in f.readline().strip().split(','):
    if id != 'x':
        buses.append(int(id))
        gaps.append(x)
    x += 1
f.close()

n = len(buses)

for i in range(1, n):
    gaps[i] = buses[i] - gaps[i]

print(chinese_remainder(buses, gaps)) 
