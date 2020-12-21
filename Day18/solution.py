# part 1

f = open('input')
lines = f.read().split('\n')

def solve(s):
    # perform operation and return result
    def operate(op, curr, res):
        if op == '+':
                res += curr
        else:
            res *= curr  
        
        return res, 0

    n = len(s)

    res = 0
    op = '+'
    curr = 0
    i = 0
    while i < n:
        if s[i].isnumeric():
            # build number
            while i < n and s[i].isnumeric():
                curr = curr * 10 + int(s[i])
                i += 1
            res, curr = operate(op, curr, res)
        elif s[i] in ('+', '*'):
            op = s[i]
            i += 1
        # determine line inside brackets and solve recursively
        elif s[i] == '(':
            start = i + 1
            l = 1
            i += 1
            while l > 0:
                if s[i] == '(':
                    l += 1
                elif s[i] == ')':
                    l -= 1
                i += 1

            curr = solve(s[start:i - 1])
            res, curr = operate(op, curr, res)
        else:
            i += 1
    return res

total = 0
for line in lines:
    total += solve(line)

print(total)

# part 2

def advanced_solve(s):
    # perform operation
    def operate(op, curr, num, res):
        if op == '+':
                curr += num
        else:
            res *= curr   
            curr = num
        num = 0
        return curr, num, res


    n = len(s)

    res = 1
    op = '+'
    num = 0
    curr = 0
    i = 0
    while i < n:
        # build number
        if s[i].isnumeric():
            while i < n and s[i].isnumeric():
                num = num * 10 + int(s[i])
                i += 1
            curr, num, res = operate(op, curr, num, res)
        elif s[i] in ('+', '*'):
            op = s[i]
            i += 1
        # determine line inside brackets and solve recursively
        elif s[i] == '(':
            start = i + 1
            l = 1
            i += 1
            while l > 0:
                if s[i] == '(':
                    l += 1
                elif s[i] == ')':
                    l -= 1
                i += 1

            num = advanced_solve(s[start:i - 1])
            curr, num, res = operate(op, curr, num, res)
        else:
            i += 1
    return res * curr

total = 0
for line in lines:
    total += advanced_solve(line)

print(total)



        
        


