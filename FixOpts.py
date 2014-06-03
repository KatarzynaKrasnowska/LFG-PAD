'''
Created on 21 sty 2014

@author: katarzyna krasnowska
'''

from ParseChoices import Choice

class Node:
    def __init__(self, choice):
        self.choice = choice
        self.children = []

def print_opts_tree(node, tab=''):
    print tab, node.choice
    for child in node.children:
        print_opts_tree(child, tab + '  ')

def init_opts_tree(opts):
    root = Node(opts[0])
    if len(opts) > 1:
        root.children.append(init_opts_tree(opts[1:]))
    return root

def update_opts_tree(node, opts):
    if not opts:
        return
    for child in node.children:
        if child.choice == opts[0]:
            update_opts_tree(child, opts[1:])
            return
    node.children.append(init_opts_tree(opts))

def collect_choices(node, choices, renaming):
    choice = node.choice
    choice_set = set()
    for child in node.children:
        collect_choices(child, choices, renaming)
        choice_set.add(child.choice)
    choice_t = tuple(sorted(choice_set))
    if choice in choices:
        if choices[choice] != choice_t:
            node.choice = 'AAAA' + str(len(renaming) + 1)
            renaming.append((choice, node.choice))
            choices[node.choice] = choice_t
    else:
        choices[choice] = choice_t

''' collect and collapse single-branching paths
    consisting of equivalent options.
    parents_map maps an option to all its parents in the tree
'''
def collect_equiv_opts_and_collapse(tree, parents_map):
    equivs = set()
    l = c_e_o(tree, equivs, parents_map)
    equivs.add(tuple(reversed(l)))
    return equivs

def c_e_o(node, equivs, parents_map):
    if not node.children:
        return [node.choice,]
    elif len(node.children) == 1:
        child = node.children[0]
        child_ch = child.choice
        l = c_e_o(child, equivs, parents_map)
        #print parents_map
        if len(parents_map[child_ch]) == 1:
            # expand current list and collapse single-branching path
            l.append(node.choice)
            node.children = child.children
            return l
        else:
            # l can no longer be expanded
            equivs.add(tuple(reversed(l)))
            return [node.choice,]
    else:
        for child in node.children:
            equivs.add(tuple(reversed(c_e_o(child, equivs, parents_map))))
        return [node.choice,]

def collect_sb_paths_and_collapse(tree):
    equivs = dict()
    rnm = set()
    l = c_sb_p(tree, equivs, rnm)
    if l != ['1']:
        raise RuntimeError
    #print l
    ret = set()
    for path, new_id in equivs.items():
        ret.add(tuple((new_id,) + path))
    return ret

def c_sb_p(node, equivs, rnm):
    if not node.children:
        return [node.choice,]
    elif len(node.children) == 1:
        child = node.children[0]
        l = c_sb_p(child, equivs, rnm)
        # expand current list and collapse single-branching path
        l.append(node.choice)
        node.children = child.children
        return l
    else:
        for child in node.children:
            l = c_sb_p(child, equivs, rnm)
            if len(l) > 1:
                # a path was collapsed - rename
                path = tuple(reversed(l))
                if not path in equivs:
                    new_id = 'BBBB%d' % (len(rnm) + 1)
                    equivs[path] = new_id
                    rnm.add(new_id)
                child.choice = equivs[path]
                #l.append(child.choice)
            #equivs.add(tuple(reversed(l)))
        return [node.choice,]

def sorted_opts(opts):
    s_opts = []
    buckets = dict()
    for o in opts:
        if not len(o) in buckets:
            buckets[len(o)] = set()
        buckets[len(o)].add(o)
    for _, b in sorted(buckets.items()):
        s_opts += sorted(b)
    return s_opts

def opts_tree(opts_list):
    tree = init_opts_tree(sorted_opts(opts_list[0]))
    for opts in opts_list[1:]:
        update_opts_tree(tree, sorted_opts(opts)[1:])
    return tree

def new_choices(opts_list):
    #for opts in opts_list:
    #    print ' '.join(sorted_opts(opts))
    tree = opts_tree(opts_list)
    #print '=== ORIGINAL TREE ==='
    #print_opts_tree(tree)
    choices = dict()
    renaming = []
    collect_choices(tree, choices, renaming)
    #print '=== AFTER RENAMING ==='
    #print_opts_tree(tree)
    # collect information about parents
    for cond in choices.keys():
        if choices[cond] == ():
            del choices[cond]
    parents_map = dict()
    for cond, chs in choices.items():
        for choice in chs:
            if not choice in parents_map:
                parents_map[choice] = set()
            parents_map[choice].add(cond)
    #print parents_map
    equiv = collect_equiv_opts_and_collapse(tree, parents_map)
    #print '=== AFTER COLLAPSING EQUIVALENT ==='
    #print_opts_tree(tree)
    merged = collect_sb_paths_and_collapse(tree)
    #print merged
    #print '=== AFTER COLLAPSING OTHER SINGLE PATHS ==='
    #print_opts_tree(tree)
    choices = dict()
    collect_choices(tree, choices, [])
    for cond in choices.keys():
        if choices[cond] == ():
            del choices[cond]
    ret = []
    known = ['1']
    while known:
        ch = known[0]
        known = known[1:]
        if ch in choices:
            ret.append(Choice(list(choices[ch]), [ch]))
            known += list(choices[ch])
            del choices[ch]
    rnm = dict()
    eqv = dict()
    mrg = dict()
    for o, n in renaming:
        #print o, '->', n
        if not o in rnm:
            rnm[o] = set()
        rnm[o].add(n)
    for t in equiv:
        for opt in t[1:]:
            eqv[opt] = t[0]
    #print '==================', merged
    for t in merged:
        for o in t[1:]:
            if not o in mrg:
                mrg[o] = set()
            mrg[o].add(t[0])
    #print '======================='
    '''Check whether some choice have the same alternatives - they should be merged
    with an 'or' of their conditions as the new condition.
    The choice should be rearranged so that all their conditions are introduced before.'''
    opts_conds = {}
    #opts_last_index = {}
    opts_uniq_list = []
    for i in xrange(0, len(ret)):
        ch = ret[i]
        opts = tuple(sorted(ch.choices))
        #print '  ', ch
        if not opts in opts_conds:
            opts_conds[opts] = []
            opts_uniq_list.append(opts)
        opts_conds[opts] += ch.conditions
        #opts_last_index[opts] = i
    ret2 = []
    '''Choices arranged so that all conditions are introduced before.'''
    ordered_opts = []
    '''Temporary list of choices whose conditions are not yet introduced.'''
    unknown_yet = []
    '''Set of introduced conditions.'''
    known_cond = set(['1',])
    for opts in opts_uniq_list:
        if known_cond.issuperset(set(opts_conds[opts])):
            #print 'add to ordered:', opts
            known_cond.update(opts)
            ordered_opts.append(opts)
            '''Maybe some choices conditions became known now.'''
            if unknown_yet:
                #print '  unknown:', unknown_yet
                introduced = [opts for opts in unknown_yet if known_cond.issuperset(set(opts_conds[opts]))]
                still_unknown = [opts for opts in unknown_yet if not known_cond.issuperset(set(opts_conds[opts]))]
                while introduced:
                    #print '  introduced:', introduced
                    #print '  still_unknown', still_unknown
                    ordered_opts += introduced
                    for opts in introduced:
                        known_cond.update(opts)
                    unknown_yet = still_unknown
                    introduced = [opts for opts in unknown_yet if known_cond.issuperset(set(opts_conds[opts]))]
                    still_unknown = [opts for opts in unknown_yet if not known_cond.issuperset(set(opts_conds[opts]))]
        else:
            #print 'add to unknown:', opts
            unknown_yet.append(opts)
    if unknown_yet:
        print unknown_yet
        raise RuntimeError
    #for i, opts in sorted([(i, opts) for opts, i in opts_last_index.items()]):
    for opts in ordered_opts:
        ret2.append(Choice(list(opts), opts_conds[opts]))
    return ret2, rnm, eqv, mrg

def fixed_conditions(conditions, active_opts, renamings, equivalences, merged):
    #print 'c:', conditions
    fixed = set()
    fixed_2 = set()
    for o in conditions:
        #if o in active_opts:
        #    fixed.add(o)
        #else:
        #    if o in equivalences:
        #        fixed.add(equivalences[o])
        #    if o in renamings:
        #        fixed.update(renamings[o])
        #    if o in merged:
        #        fixed.update(merged[o])
        fixed.add(o)
        if o in renamings:
            fixed.update(renamings[o])
    for o in fixed:
        fixed_2.add(o)
        if o in equivalences:
            fixed_2.add(equivalences[o])
    fixed = set()
    for o in fixed_2:
        fixed.add(o)
        if o in merged:
            fixed.update(merged[o])
    fixed = set([o for o in fixed if o in active_opts])
    return sorted(fixed)