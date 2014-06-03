'''
Created on 14-01-2013

@author: Katarzyna Krasnowska
'''

import re

from ParseChoices import parse_conditions

class Phi(object):
    def __init__(self, n_id, var, choices):
        self.n_id = n_id
        self.var = var
        self.choices = choices
    def prolog(self):
        '''cf(1,phi(1563,var(0)))'''
        if (len(self.choices) == 1):
            ch = self.choices[0]
        else:
            ch = 'or(%s)' % ','.join(self.choices)
        return '\tcf(%s,phi(%s,var(%s)))' % (ch, self.n_id, self.var)

def parse_phi(s, equivalences):
    cond, n_id, var = re.match(r'\tcf\((.+),phi\((.+),var\((.+)\)\)\)', s).group(1, 2, 3)
    return Phi(int(n_id), int(var), parse_conditions(cond, equivalences))
