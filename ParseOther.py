'''
Created on 11-06-2013

@author: Katarzyna Krasnowska
'''

import re

from ParseChoices import parse_conditions

class Other(object):
    def __init__(self, choices, text):
        self.choices = choices
        self.text = text
    def prolog(self):
        if (len(self.choices) == 1):
            ch = self.choices[0]
        else:
            ch = 'or(%s)' % ','.join(self.choices)
        return '\tcf(%s,%s)' % (ch, self.text)

def parse_other(s, equivalences):
    #cf(1,xyz(...)),
    i = 0
    rels = ('subtree(', 'terminal(', 'semform_data(', 'fspan(', 'surfaceform(')
    for r in rels:
        if (s.find(r) != -1):
            i = s.find(r)
            break
    cond, text = s[4:(i-1)], s[i:-1]
    if text.endswith(','):
        text = text[:-2]
    else:
        text = text[:-1]
    return Other(parse_conditions(cond, equivalences), text)
