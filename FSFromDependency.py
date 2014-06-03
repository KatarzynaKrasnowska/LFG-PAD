# -*- coding: utf-8 -*-
'''
Created on 10-02-2014

@author: Katarzyna Krasnowska
'''
from DependencyInfo import DependencyType
from FSConstrs import SkladnicaConstrs

class DependencyNode:
    def __init__(self, base, dep, n_id):
        self.base = base
        self.dep = dep
        self.n_id = n_id
        self.children = []
    def __str__(self):
        return '*%d* %s' % (self.n_id, self.base)
    def __repr__(self):
        return '*%d* %s' % (self.n_id, self.base)

def tree_from_conll(conll):
    nodes, children = {}, {}
    for line in conll.split('\n'):
        print line
        n_id, _, base, _, _, _, parent_id, dep, _, _ = line.split()
        n_id, parent_id = int(n_id), int(parent_id)
        node = DependencyNode(base, dep, n_id)
        if not parent_id in children:
            children[parent_id] = []
        children[parent_id].append(node)
        nodes[n_id] = node
    nodes[0] = DependencyNode('ROOT', DependencyType.default, 0)
    print children
    for node_id, node in nodes.items():
        if node_id in children:
            nodes[node_id].children = children[node_id]
    return nodes[0]

def collect_constrs(tree, constrs=None):
    if constrs is None:
        constrs = {}
        collect_constrs(tree, constrs)
        return constrs
    else:
        constr = SkladnicaConstrs()
        for child in tree.children:
            constr.undef_cs.append(child.base)
        if not tree.base in constrs:
            constrs[tree.base] = {}
        constrs[tree.base][tree.n_id] = constr
        for child in tree.children:
            collect_constrs(child, constrs)

def fs_constrs_from_conll(conll):
    t = tree_from_conll(conll)
    return collect_constrs(t)

conll = '''1    Na    na    prep    prep    acc    4    adjunct    _    _
2    wszelki    wszelki    adj    adj    sg|acc|m3|pos    3    adjunct    _    _
3    wypadek    wypadek    subst    subst    sg|acc|m3    1    comp    _    _
4    weźmiemy    wziąć    verb    fin    pl|pri|perf    0    pred    _    _
5    cię    ty    subst    ppron12    sg|acc|m1|sec|nakc    4    obj    _    _
6    za    za    prep    prep    acc    4    comp    _    _
7    wielbłąda    wielbłąd    subst    subst    sg|acc|m2    6    comp    _    _
8    .    .    interp    interp    _    4    punct    _    _'''
constrs = fs_constrs_from_conll(conll)
print constrs
for pred, cs in constrs.items():
    print pred
    for n_id, c in cs.items():
        print '   ', c
    