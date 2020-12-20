# part 1
f = open('input')

mem = {}
negate = 0
force = 0
for line in f.readlines():
    op, _, val = line.strip().split(' ')
    if op[:4] == 'mask':
        negate = 0
        force = 0

        for ch in val:
            force <<= 1
            negate <<= 1
            if ch == '1':
                force += 1
                negate += 1
            elif ch == 'X':
                negate += 1

    else:
        loc = int(op[4:len(op) - 1])
        val = int(val)
        val |= force
        val &= negate
        mem[loc] = val

f.close()
print(sum(mem.values()))

# part 2
f = open('input')

mem = {}
mask = ''

for line in f.readlines():
    op, _, val = line.strip().split(' ')
    if op[:4] == 'mask':
        mask = val
    else:
        locs = [int(op[4:len(op) - 1])]

        for i in range(len(mask)):
            if mask[i] == '1':
                for j in range(len(locs)):
                    locs[j] |= 2 ** (35 - i)
            elif mask[i] == 'X':
                locs *= 2
                for j in range(len(locs)//2):
                    locs[j] |= 2 ** (35 - i)
                for j in range(len(locs)//2, len(locs)):
                    locs[j] &= ((2 ** 36 - 1) ^ (2 ** (35 - i)))

        for loc in locs:
            mem[loc] = int(val)

f.close()
print(sum(mem.values()))