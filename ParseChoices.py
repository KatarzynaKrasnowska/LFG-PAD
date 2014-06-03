'''
Created on 11-01-2013

@author: Katarzyna Krasnowska
'''

import re

class Choice(object):
    def __init__(self, choices, conditions):
        self.conditions = conditions
        self.choices = choices
    def __str__(self):
        return 'choice: ' + ' | '.join(self.choices) + ' ; condition: ' + ' | '.join(self.conditions)
    def prolog(self):
        '''choice([B1,B2,B3], A6)'''
        if len(self.conditions) == 1:
            return '\tchoice([%s], %s)' % (','.join(self.choices), self.conditions[0])
        else:
            return '\tchoice([%s], or(%s))' % (','.join(self.choices), ','.join(self.conditions))

def parse_conditions(s, equivalences):
    conds_tmp = parse_conditions_2(s)[0]
    # replace CV_... with actual choices
    conds = []
    for c in conds_tmp:
        if (c in equivalences):
            conds += equivalences[c]
        else:
            conds.append(c)
    return conds

def parse_conditions_2(s):
    #print 'ParseChoices.parse_conditions', s
    if (s.startswith('or') or s.startswith(',or')):
        i = 3
        # or-clause within another or-clause, preceded by a comma
        if (s.startswith(',')):
                i = 4
        arg, rest = parse_conditions_2(s[i:])
        arg_list = arg
        while (not rest.startswith(')')):
            arg, rest = parse_conditions_2(rest)
            arg_list += arg
        return arg_list, rest[1:]
    else:
        #print 's:', s
        atom, rest = re.match(r',?(\w*\d)(.*)', s).group(1, 2)
        #print 'atom:', atom, "*"
        return [atom], rest#[s[0:2]], s[2:]

def parse_choice(s):
    #print 'ParseChoices.parse_choice', s
    ch, cond = re.match(r'\tchoice\(\[(.+)\], (.+)\)', s).group(1, 2)
    choices = ch.split(',')
    return Choice(choices, parse_conditions(cond, {}))

def parse_choice_probability(s):
    #print 'ParseChoices.parse_choice_probability', s
    choice, prob = re.match(r'\tprobability\((.+),(.+)\)', s).group(1, 2)
    return choice, float(prob)

def parse_choice_weight(s):
    #print 'ParseChoices.parse_choice_weight', s
    choice, weight = re.match(r'\tweight\((.+),(.+)\)', s).group(1, 2)
    return choice, float(weight)