class Game:
    class Cup:
        """
        Treat cups as nodes in a linked list
        """
        def __init__(self, label):
            self.label = label
            self.next = None

    def __init__(self, input, part2=False):
        self.part2 = part2
        self.mx = max(input)
        if part2:
            input += list(range(10, 1000000 + 1))
            self.mx = 1000000

        # store Cup objects in dict with label as key
        self.cups = {}
        prev = None
        for label in input:
            cup = self.Cup(label)
            self.cups[label] = cup

            if prev is not None:
                prev.next = cup

            prev = cup

        # link first and last cups
        self.cups[input[-1]].next = self.cups[input[0]]

        self.first = input[0]

    def play(self):
        n = 100 if not self.part2 else 10000000
        curr_cup = self.cups[self.first]

        for i in range(n):
            # remove cups from circle
            first = curr_cup.next
            curr_cup.next = curr_cup.next.next.next.next

            # track labels of cups that were picked up    
            picked_up = set([])
            picked_up.add(first.label)
            picked_up.add(first.next.label)
            picked_up.add(first.next.next.label)

            # determine destination 
            dest = curr_cup.label - 1
            while dest in picked_up or dest == 0:
                dest = dest - 1 if dest > 0 else self.mx
            dest_cup = self.cups[dest]

            # place removed cups after destination
            first.next.next.next = dest_cup.next
            dest_cup.next = first

            # choose next cup
            curr_cup = curr_cup.next
        
        return self.results(self.part2)
    
    # return results
    def results(self, part2=False):
        if part2:
            cup = self.cups[1]
            return cup.next.label * cup.next.next.label
        else:
            cup = self.cups[1].next
            labels = []
            while cup.label != 1:
                labels.append(str(cup.label))
                cup = cup.next
            return ''.join(labels)

# problem input
input = list(map(int, list('135468729')))

# part 1
game = Game(input, part2=False)
print(game.play())

# part 2
game = Game(input, part2=True)
print(game.play())
