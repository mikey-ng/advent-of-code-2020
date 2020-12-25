f = open('input')
card, door = list(map(int, f.read().split('\n')))

mod = 20201227
loops = 1
curr = 1

while True:
    curr *= 7
    curr %= mod

    # card loop size found, tranform door public key
    if curr == card:
        key = 1
        for j in range(i):
            key *= door
            key %= mod
        print(key)
        break
    # door loop size found, tranform loop public key
    elif curr == door:
        key = 1
        for j in range(i):
            key *= card
            key %= mod
        print(key)
        break

    loops += 1