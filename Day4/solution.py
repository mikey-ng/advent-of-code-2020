# part 1
f = open('input')

curr_fields = set(['cid'])
i = 0
res = 0

for line in f.readlines():
    
    if (line != '\n'):
        curr_fields.update([x.split(':')[0] for x in line.split(' ')])
    else:
        if len(curr_fields) == 8:
            res += 1
        curr_fields = set(['cid'])
        
print(res if len(curr_fields) < 8 else res + 1)
f.close()

# part 2
def is_valid_passport(fields):
    count = 0
    for key, val in fields.items():
        if key == 'byr':
            count += 1
            if not (val.isnumeric() and 1920 <= int(val) <= 2002):
                return False
        elif key == 'iyr':
            count += 1
            if not (val.isnumeric() and 2010 <= int(val) <= 2020):
                return False
        elif key == 'eyr':
            count += 1
            if not (val.isnumeric() and 2020 <= int(val) <= 2030):
                return False
        elif key == 'hgt':
            count += 1
            if not ((len(val) == 4 and val[2:] == 'in' and val[:2].isnumeric() and 59 <= int(val[:2]) <= 76) or (len(val) == 5 and val[3:] == 'cm' and val[:3].isnumeric() and 150 <= int(val[:3]) <= 193)):
                return False
        elif key == 'hcl':
            count += 1
            if not (len(val) == 7 and val[0] == '#' and sum([ord('a') <= ord(x) <= ord('z') or ord('0') <= ord(x) <= ord('9') for x in val[1:]]) == 6):
                return False
        elif key == 'ecl':
            count += 1
            if not val in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
                return False
        elif key == 'pid':
            count += 1
            if not (len(val) == 9 and val.isnumeric()):
                return False
    return count == 7

f = open('input')

curr_fields = {}
i = 0
res = 0

for line in f.readlines():
    
    if (line != '\n'):
        for x in line.split(' '):
            key, val = x.split(':')
            curr_fields[key] = val.strip()
    else:
        if is_valid_passport(curr_fields):
            res += 1
        curr_fields = {}

f.close()   
print(res + 1 if is_valid_passport(curr_fields) else res)



