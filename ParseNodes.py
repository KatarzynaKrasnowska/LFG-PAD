'''
Created on 11-01-2013

@author: Katarzyna Krasnowska
'''

import re

from ParseChoices import parse_conditions

class Node:
    def __init__(self, n_id, label):
        self.n_id = n_id
        self.label = label
        self.children = []
        self.children_ids = []
        #self.choices = set()
    def __str__(self):
        return self.string('')
    def string(self, tab):
        s = tab + self.label +'\n'
        for c in self.children:
            s += c.string(tab + ' ')
        return s
    def short(self):
        return '%d %s %s' % (self.n_id, self.label, self.children_ids)
    def tex(self, tab=None):
        if (tab is None):
            return '\\branchheight{20pt}\\synttree\n' + self.tex('')
        else:
            if self.children:
                s = tab + '[ %d %s' % (self.n_id, self.label) +'\n'
                for c in self.children:
                    s += c.tex(tab + '  ')
                return s + '%s]\n' % tab
            else:
                return tab + '[ \\textit{%d %s} ]\n' % (self.n_id, self.label)
    def __hash__(self):
        ret = self.n_id
        for ch in self.children:
            ret ^= hash(ch)
        return ret
    def __cmp__(self, other):
        if (self.n_id != other.n_id):
            return cmp(self.n_id, other.n_id)
        if (self.label != other.label):
            return cmp(self.label, other.label)
        if (len(self.children) != len(other.children)):
            return cmp(len(self.children), len(other.children))
        return cmp(self.children, other.children)

def parse_node(s, equivalences):
    #print 'ParseNodes.parse_node', s
    ret = None
    if (s.find('subtree') > -1):
        cond, node = re.match(r'\tcf\((.+),subtree\((.+)\)\)', s).group(1, 2)
        #n_id, label, ch1, ch2 = node.replace('-', '0').split(',')
        n_id, label, ch1, ch2 = node.split(',')
        ret = Node(int(n_id), label[1:-1])
        conditions = parse_conditions(cond, equivalences)
        # if (len(conditions) == 1 and conditions[0] in equivalences):
        #    conditions = equivalences[conditions[0]]
        choices = set(conditions)
        ret.children_ids = [(int(i), choices) for i in (ch1, ch2) if i != '-']
    if (s.find('terminal(') > -1):
        #cf(1,terminal(32,'w',[32])),
        cond, n_id, label = re.match(r'\tcf\((.+),terminal\((.+),\'(.+)\',.*\)\)', s).group(1, 2, 3)
        ret = Node(int(n_id), label)
    return ret