input = [6,4,12,1,20,0,16]

history = {}
for i in range(len(input)):
    history[input[i]] = (-1, i + 1)

time = len(input) + 1
prev = input[-1]
while time <= 2020: # 30000000 for part 2
    if prev in history and history[prev][0] >= 0:
        curr = history[prev][1] - history[prev][0]
    else:
        curr = 0

    if curr in history:
        history[curr] = (history[curr][1], time)
    else:
        history[curr] = (-1, time)

    prev = curr
    time += 1
print(prev)