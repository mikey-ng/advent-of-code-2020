f = open('input')
taken = [0] * (8 * 128)
mn = 8 * 128
mx = 0
for line in f.readlines():
    row_code = line[:7]
    col_code = line[7:10]
    
    row = 0
    for ch in row_code:
        row = (row << 1) + (1 if ch == 'B' else 0)

    col = 0
    for ch in col_code:
        col = (col << 1) + (1 if ch == 'R' else 0)

    taken[row * 8 + col] = 1
    mn = min(mn, row * 8 + col)
    mx = max(mx, row * 8 + col)

f.close()

# part 1
print(mx)

# part 2
for i in range(mn, mx + 1):
    if taken[i] == 0:
        print(i)
        



