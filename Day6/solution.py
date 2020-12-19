# part 1
f = open('input')
questions = set([])
res = 0

for line in f.readlines():
    if line != '\n':
        for ch in line.strip():            
            questions.add(ch)
    else:
        res += len(questions)
        questions = set([])

f.close()

res += len(questions)
print(res)

# part 2
from collections import defaultdict
f = open('input')
questions = defaultdict(int)
line_count = 0
res = 0

for line in f.readlines():
    if line != '\n':
        line_count += 1
        for ch in line.strip():            
            questions[ch] += 1
    else:
        for count in questions.values():
            if count == line_count:
                res += 1
        line_count = 0
        questions = defaultdict(int)

f.close()
for count in questions.values():
    if count == line_count:
        res += 1

print(res)
