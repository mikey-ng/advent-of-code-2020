from collections import deque

f = open('input')
player1, player2 = f.read().split('\n\n')
player1 = deque(list(map(int, player1.split('\n')[1:])))
player2 = deque(list(map(int, player2.split('\n')[1:])))

while player1 and player2:
    card1 = player1.popleft()
    card2 = player2.popleft()

    if card1 > card2:
        player1.append(card1)
        player1.append(card2)
    else:
        player2.append(card2)
        player2.append(card1)

score = 0
winner = player1 if player1 else player2

n = len(winner)
for card in winner:
    score += n * card
    n -= 1

print(score)

f.seek(0)
player1, player2 = f.read().split('\n\n')
player1 = deque(list(map(int, player1.split('\n')[1:])))
player2 = deque(list(map(int, player2.split('\n')[1:])))

def game(player1, player2, other_rounds):
    def update_hash(hash, card, deck, event):
        """
        Update deck hash code by adding card values and shifting by 100 each time
        Ex. Deck = [13, 4, 5, 27] -> Hash Code: 13040527

        Adding Card to Deck Bottom : 
            Add '6' to end of [13, 4, 5, 27] -> [13, 4, 5, 27, 6]
            -> Hash Code = Hash Code * 100 + Added
                         = 13040527 * 100 + 6 
                         = 1304052706
        Removing Card from Deck Top: 
            Remove '13' from start of [13, 4, 5, 27, 6] -> [4, 5, 27, 6]
                -> Hash Code = Hash Code - 13 ^ 10 * (2n) where n is the new deck length
                             = 1304052706 - 13 * 10 ^ (2 * 4) 
                             = 1304052706 - 1300000000 
                             = 4052706
        Args:
            hash (int): current hash code
            card (int): event card value
            deck (list): current deck
            event (str): event

        Returns:
            int: updated hash
        """
        if event == 'draw':
            hash -= card * 10 ** (2 * len(deck))
        elif event == 'win':
            hash *= 100
            hash += card

        return hash

    player1_hash = 0
    player2_hash = 0
    prev_rounds = set({})

    for card in player1:
        player1_hash *= 100
        player1_hash += card
    for card in player2:
        player2_hash *= 100
        player2_hash += card

    while player1 and player2:
        if (player1_hash, player2_hash) in prev_rounds:
            return '1', []
        else:
            prev_rounds.add((player1_hash, player2_hash))

        card1 = player1.popleft()
        player1_hash = update_hash(player1_hash, card1, player1, 'draw')

        card2 = player2.popleft()
        player2_hash = update_hash(player2_hash, card2, player2, 'draw')

        if card1 <= len(player1) and card2 <= len(player2):
            player1_copy = deque([])
            for i in range(card1):
                player1_copy.append(player1[i])

            player2_copy = deque([])
            for i in range(card2):
                player2_copy.append(player2[i])

            winner = game(player1_copy, player2_copy, other_rounds)[0]
        else:
            winner = '1' if card1 > card2 else '2'

        if winner == '1':
            player1.append(card1)
            player1.append(card2)
            player1_hash = update_hash(player1_hash, card1, player1, 'win')
            player1_hash = update_hash(player1_hash, card2, player1, 'win')
        else:
            player2.append(card2)
            player2.append(card1)
            player2_hash = update_hash(player2_hash, card2, player2, 'win')
            player2_hash = update_hash(player2_hash, card1, player2, 'win')

    return ('1', player1) if player1 else ('2', player2)


score = 0
winner = game(player1, player2, {})[1]
n = len(winner)
for card in winner:
    score += n * card
    n -= 1
print(score)
