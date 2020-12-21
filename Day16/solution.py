from collections import defaultdict

f = open('input')

fields, ticket, nearby = f.read().split('\n\n')

aggr_range = None
rules = {}

for line in fields.split('\n'):
    field, field_range = line.split(': ')

    # rule format: [min1, max1, min2, max2]
    rules[field] = list(map(int, field_range.replace(' or ', '-').split('-')))

    # since ranges in the input overlap, create an overall range
    if aggr_range is None:
        aggr_range = rules[field].copy()
    else:
        aggr_range[0] = min(aggr_range[0], rules[field][0])
        aggr_range[1] = max(aggr_range[1], rules[field][1])
        aggr_range[2] = min(aggr_range[2], rules[field][2])
        aggr_range[3] = max(aggr_range[3], rules[field][3])

ticket = list(map(int, ticket.split('\n')[1].split(',')))

# ticket validity check
tickets = []
invalid_sum = 0
for line in nearby.split('\n')[1:]:
    values = list(map(int, line.strip().split(',')))

    valid = True
    for val in values:
        if not (aggr_range[0] <= val <= aggr_range[1] or aggr_range[2] <= val <= aggr_range[3]):
            # sum values that don't fit in any valid ranges
            invalid_sum += val
            valid = False

    # keep tickets that contain all valid values
    if valid:
        tickets.append(values)

# ans to part 1
print(invalid_sum)

m = len(ticket)
n = len(tickets)

valid_positions = defaultdict(list)

# for each rule determine a list of valid ticket indices
# ex. 'arrival track':[0, 3, 5] -> all ticket values in indices 0, 3, 5 are meet the 'arrival track' range rules
for field in rules:    
    for j in range(m):
        valid = True
        for i in range(n):
            if not (rules[field][0] <= tickets[i][j] <= rules[field][1] or rules[field][2] <= tickets[i][j] <= rules[field][3]):
                valid = False
                break

        if valid:
            valid_positions[field].append(j)

# sort by increasing number of possible indices
positions = []
fields = list(valid_positions.keys())
fields.sort(key=lambda x: len(valid_positions[x]))

# recursively set the indices for each field
def set_position(curr, fields, valid_positions, used, positions):
    if curr == len(fields):
        return True

    field = fields[curr]
    for idx in valid_positions[field]:
        if idx not in used:
            used.add(idx)
            positions.append((field, idx))

            if set_position(curr + 1, fields, valid_positions, used, positions):
                return True

            used.remove(idx)
            positions.pop()

    return False

set_position(0, fields, valid_positions, set([]), positions)

# print product of departure field values
prd = 1
for field, idx in positions:
    if field.startswith('departure'):
        prd *= ticket[idx]

print(prd)
