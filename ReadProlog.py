# -*- coding: utf-8 -*-
'''
Created on 21-10-2013

@author: Katarzyna Krasnowska
'''

from ParseChoices import parse_choice, parse_choice_probability, parse_choice_weight
from ParseConstraints import parse_constraint, parse_equivalence
from ParseNodes import parse_node
from ParseOther import parse_other
from ParsePhis import parse_phi

class PrologData():
    def __init__(self, num_solutions, text, constraint_list, phis, other_list,
                  choices_list, choices_probs, choices_weights, nodes, root_id, opts, all_lines):
        self.num_solutions = num_solutions
        self.text = text
        self.constraint_list = constraint_list
        self.phis = phis
        self.other_list = other_list
        self.choices_list = choices_list
        self.choices_probs = choices_probs
        self.choices_weights = choices_weights
        self.nodes = nodes
        self.root_id = root_id
        self.opts = opts
        self.all_lines = all_lines

def options_combinations(choices):
    #print 'options_combinations', choices
    new, old = [], [[]]
    for choice_list in choices:
        for choice in choice_list:
            for old_combination in old:
                new.append(old_combination + [choice])
        old = new
        new = []
    #print 'result', old
    return old

def options_list(cond, cond_choices):
    if (cond_choices[cond]):
        ret = []
        for combination in options_combinations(cond_choices[cond]):
            new, old = [], [set([cond])]
            for choice in combination:
                for o in options_list(choice, cond_choices):
                    for old_option in old:
                        new.append(old_option.union(o))
                old = new
                new = []
            ret += old
            #for choice in combination:
            #    opts = options_list(choice, cond_choices)
            #    for o in opts:
            #        ret.append(set([cond]).union(o))
        return ret
    else:
        return [set([cond])]

def read_prolog_file(path, quiet=False, max_solutions=10000):
    with open(path, 'r') as f:
        choices, equivalences, constraints, structure = False, False, False, False
        choice_lines, probability_lines, weight_lines, equivalence_lines = [], [], [], []
        constraint_lines, structure_lines, phi_lines, other_lines = [], [], [], []
        lines = f.readlines()
        num_solutions = 0
        text = ''
        all_lines = []
        l_no = 0
        for l in lines:
            l_no += 1
            all_lines.append(l)
            if l.startswith('\t\'statistics'):
                num_solutions = int(l[15:l.find(' solutions')])
                if not quiet:
                    print l
            if l.startswith('fstructure'):
                text = l[12:-3].replace(' ', '-')
                while (text.startswith('-')):
                    text = text[1:]
                if not quiet:
                    print text
            if (l == '\t% Choices:\n'):
                choices = True
            if (l == '\t% Equivalences:\n'):
                choices = False
                equivalences = True
            if (l == '\t% Constraints:\n'):
                equivalences = False
                constraints = True
            if (l == '\t% C-Structure:\n'):
                constraints = False
                structure = True
            if (choices and l.startswith('\tchoice')):
                choice_lines.append((l, l_no))
            if (choices and l.startswith('\tprobability')):
                probability_lines.append((l, l_no))
            if (choices and l.startswith('\tweight')):
                weight_lines.append((l, l_no))
            if (equivalences and l.startswith('\tdefine')):
                equivalence_lines.append((l, l_no))
            if (constraints and l.startswith('\tcf')):
                constraint_lines.append((l, l_no))
            if (structure and l.startswith('\tcf')):
                if (l.find('subtree') + l.find('terminal') > -1):
                    structure_lines.append((l, l_no))
                    other_lines.append((l, l_no))
                elif (l.find('phi') > -1):
                    phi_lines.append((l, l_no))
                else:
                    other_lines.append((l, l_no))
        if (num_solutions > max_solutions):
            return None
        choices_list = [(parse_choice(l), l_no) for l, l_no in choice_lines]
        choices_probs = { choice : prob for choice, prob in (parse_choice_probability(l) for l, l_no in probability_lines) }
        choices_weights = { choice : weight for choice, weight in (parse_choice_weight(l) for l, l_no in weight_lines) }
        equivalence_dict = { alias : cond for alias, cond in (parse_equivalence(l) for l, l_no in equivalence_lines) }
        constraint_list = [(parse_constraint(l, equivalence_dict), l_no) for l, l_no in constraint_lines]
        other_list = [(parse_other(l, equivalence_dict), l_no) for l, l_no in other_lines]
        nodes_tmp = [(n.n_id, n) for n in [parse_node(l, equivalence_dict) for l, l_no in structure_lines] if n]
        nodes = {}
        root_id = None
        '''26.02.2014 - corrected way of collecting children - now the order used to get messed up;
        now will add children by buckets: first on the list, second etc. for each different
        children list conditional on options.
        NEW CODE STARTS HERE'''
        children_buckets = {}
        children_conds = {}
        for n_id, n in nodes_tmp:
            if not n_id in children_buckets:
                children_buckets[n_id] = {}
                children_conds[n_id] = {}
            if n_id == 497:
                print n_id, children_buckets[n_id]
            for i in xrange(0, len(n.children_ids)):
                ch_id, cond = n.children_ids[i]
                if not i in children_buckets[n_id]:
                    children_buckets[n_id][i] = set()
                children_buckets[n_id][i].add(ch_id)
                if not ch_id in children_conds[n_id]:
                    children_conds[n_id][ch_id] = set()
                children_conds[n_id][ch_id].update(cond)
        for n_id, buckets in sorted(children_buckets.items()):
            sum_from_buckets = 0
            sum_buckets = set()
            for b in buckets.values():
                sum_from_buckets += len(b)
                sum_buckets.update(b)
            #one node should not appear in more than one bucket
            if len(sum_buckets) != sum_from_buckets:
                raise RuntimeError
        for n_id, n in nodes_tmp:
            if (not nodes.has_key(n_id)):
                nodes[n_id] = n
        for n in nodes.values():
            children = []
            for bucket_no in sorted(children_buckets[n.n_id].keys()):
                for ch_id in children_buckets[n.n_id][bucket_no]:
                    children.append((nodes[ch_id], children_conds[n.n_id][ch_id]))
            n.children = children
        '''26.02.2014 NEW CODE ENDS HERE'''
        '''26.02.2014 OLD CODE STARTS HERE'''
        '''
        for n_id, n in nodes_tmp:
            if (not nodes.has_key(n_id)):
                nodes[n_id] = n
            else:
                nodes[n_id].children_ids += [ch_id for ch_id in n.children_ids if not ch_id in nodes[n_id].children_ids]
        for n in nodes.values():
            ch_ids = []
            ch_choices = {}
            for ch_id, choices in n.children_ids:
                if not ch_id in ch_ids:
                    ch_ids.append(ch_id)
                    ch_choices[ch_id] = set()
                ch_choices[ch_id] = ch_choices[ch_id].union(choices)
            n.children = [(nodes[c], ch_choices[c]) for c in ch_ids]
            #if (n.label == 'ROOT' and len(n.children) == 1):
            #    root_id = n.n_id
        '''
        '''26.02.2014 OLD CODE ENDS HERE'''
        '''26.02.2014 - corrected way of finding root_id'''
        '''nodes_tmp can be None in case of < 1 solutions'''
        if num_solutions > 0:
            if nodes_tmp[0][1].label != 'ROOT':
                raise RuntimeError
            root_id = nodes_tmp[0][1].n_id
        #root_id = int(re.match(r'\tcf\(1,subtree\((.+),\'ROOT\'.*', structure_lines[0]).group(1))
        phis = [(parse_phi(l, equivalence_dict), l_no) for l, l_no in phi_lines]
        cond_choices = { '1' : [] }
        for ch, l_no in choices_list:
            for choice in ch.choices:
                cond_choices[choice] = []
        for ch, l_no in choices_list:
            for cond in ch.conditions:
                cond_choices[cond].append(ch.choices)
        opts = options_list('1', cond_choices)
        return PrologData(num_solutions, text, constraint_list, phis, other_list,
                  choices_list, choices_probs, choices_weights, nodes, root_id, opts, all_lines)
