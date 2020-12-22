import re

# build dictionary of rules and track resolved rules  (i.e. don't reference another rule)
def build_rulebook(rule_defs):
    rulebook = {}
    resolved = set([])

    for line in rule_defs.split('\n'):
        idx, rule = line.split(': ')

        # handle explicit rules (ex. 1: 'a')
        if rule[0] == '"':
            rule = rule[1]
            resolved.add(idx)
        rulebook[idx] = rule
    
    return rulebook, resolved

# build regex pattern by resolving rule references recursively
def resolve_rule(key, rulebook, resolved, part):
    if key in resolved:
        return rulebook[key]

    # split rule by OR
    or_rules = []    
    for or_rule in rulebook[key].split(' | '):
        and_rules = []
        # split sub-rule by AND
        for and_rule in or_rule.split(' '):            
            rule = resolve_rule(and_rule, rulebook, resolved, part) 
            if '|' in rule:
                rule = '(' + rule + ')'

            # rule insertion for part 2
            if key == '8' and part == 2:
                rule = '(' + rule + '+)' 

            and_rules.append(rule)

        if key == '11' and part == 2:
            or_rules.append('(' + '|'.join([and_rules[0] + '{' + str(i) + '}' + and_rules[1] + '{'+ str(i) +'}' for i in range(1, 6)]) + ')')
        else:
            # wrap each AND rule in ()
            or_rules.append('(' + ''.join(and_rules) + ')')
    
    # separate OR rules by |
    rulebook[key] = '|'.join(or_rules)

    # track resolved rules
    resolved.add(key)

    return rulebook[key]

# load data
f = open('input')
rule_defs, messages = f.read().split('\n\n')

# part 1

# build rulebook
rulebook, resolved = build_rulebook(rule_defs)

# build pattern with modifiers to match start and end 
pattern = '^' + resolve_rule('0', rulebook, resolved, 1) + '$'
prog = re.compile(pattern)
messages = messages.split('\n')

# process each message and return 1 if valid
print(sum([1 for message in messages if prog.match(message)]))

# part 2
'''
Updated Rules for Part 2
8: 42 | 42 8 -> (Rule 42)+
11: 42 31 | 42 11 31 -> (Rule 41){n}(Rule 31){n}
'''

# build rulebook
rulebook, resolved = build_rulebook(rule_defs)

# build pattern with modifiers to match start and end 
pattern = '^' + resolve_rule('0', rulebook, resolved, 2) + '$'
prog = re.compile(pattern)

# process each message and return 1 if valid
print(sum([1 for message in messages if prog.match(message)]))
