# -*- coding: utf-8 -*-
'''
Created on 21-01-2014

@author: Katarzyna Krasnowska
'''

import os, re, sys, traceback

from ReadProlog import read_prolog_file
from FStructure import build_fs

sys.setrecursionlimit(1000)

sents_dir = '/home/kasia/Dokumenty/Robota/LFG/parses/FULL_20130917_newdict_Skladnica-131011_updated_map/'
sents_dir = '/home/kasia/Dokumenty/Robota/LFG/parses/Skladnica140410_FULL_prolog_POLFIE2v0.5_W-20140608/'

sents_file = '/home/kasia/Dokumenty/Robota/LFG/Iness/all-13012014.txt'
sents_file = '/home/kasia/Dokumenty/Robota/LFG/Iness/all-09062014.txt'
#sents_file = '/home/kasia/Dokumenty/Robota/LFG/Iness/test.txt'
ranked_dir = '/home/kasia/Dokumenty/Robota/LFG/parses/ranked/FULL_20130917_newdict_Skladnica-131011_updated_map/'
ranked_dir = '/home/kasia/Dokumenty/Robota/LFG/parses/ranked/Skladnica140410_FULL_prolog_POLFIE2v0.5_W-20140608/'

MAX_SOLUTIONS = 100000

sentences = []
with open (sents_file, 'r') as f:
    for l in f.readlines():
        if not (l.startswith('#')):
            s_name = re.match(r'.*(Skladnica.*-s).*', l).group(1)
            sentences.append(s_name)

solutions_full = dict()
solutions_sum = dict()
ranked_forests = dict()
i = 0
for s_name in sentences:
    i += 1
    if (i % 200 == 0):
        print i
    full_forest = sents_dir + s_name + '.pl'
    solutions = 0
    with open(full_forest, 'r') as forest:
        l = forest.readline()
        while l:
            if l.startswith('\t\'statistics'):
                solutions = int(l[15:l.find(' solutions')])
                break
            l = forest.readline()
    if solutions > 0:
        solutions_full[s_name] = solutions
        solutions_sum[s_name] = 0
        ranked_forests[s_name] = []

i = 0
rfs = sorted(os.listdir(ranked_dir))
n = len(rfs)
exceptions = dict()
exc_forests = dict()

print 'Checking solutions sums'
for ranked_forest in rfs:
    i += 1
    if (i % 250 == 0):
        print i, '/', n
    j = ranked_forest.find('-s-')
    s_name = ranked_forest[:(j + 2)]
    if not s_name in solutions_sum:
        #print ranked_forest
        continue
    ranked_forests[s_name].append(ranked_forest)
    #TYLKO NA RAZIE TU PRZERYWAMY, ZEBY BYLO SZYBCIEJ
    #continue
    prolog_data = read_prolog_file(ranked_dir + ranked_forest, quiet=True, max_solutions=1000000)
    if prolog_data is None:
        continue
    #print ranked_forest, len(prolog_data.opts)
    for o in prolog_data.opts:
        try:
            fs, eqs_dict = build_fs([c for c, l_no in prolog_data.constraint_list if c.cond.intersection(o)])
        except:
            if not s_name in exc_forests:
                print 'EXCEPTION'
                print o
                exc_forests[s_name] = set()
                raise
            exceptions[s_name] = traceback.format_exc()
            exc_forests[s_name].add(ranked_forest)
    solutions_sum[s_name] += len(prolog_data.opts)

i = 0
print 'Checking solutions'
for s_name, solutions in sorted(solutions_full.items()):
    if not ranked_forests[s_name]:
        #print s_name
        continue
    #print s_name, solutions
    i += 1
    if i % 500 == 0:
        print i, '/', len(solutions_full)
    if solutions > MAX_SOLUTIONS:
        continue
    full_prolog_data = read_prolog_file(sents_dir + s_name + '.pl', quiet=True)
    full_parses = []
    for o in full_prolog_data.opts:
        parse = [c for c, l_no in full_prolog_data.constraint_list if c.cond.intersection(o)]
        full_parses.append(parse)
    matched = set()
    for ranked_forest in ranked_forests[s_name]:
        #print ranked_forest
        ranked_prolog_data = read_prolog_file(ranked_dir + ranked_forest, quiet=True)
        for o in ranked_prolog_data.opts:
            parse = [c for c, l_no in ranked_prolog_data.constraint_list if c.cond.intersection(o)]
            #print 'num_constrs in parse:', len(parse)
            #print parse[:4]
            found_match = False
            for j in xrange(0, len(full_parses)):
                if not j in matched:
                    p = full_parses[j]
                    #print 'num_constrs in parse from full:', len(p)
                    #print p[:4]
                    if p == parse:
                        matched.add(j)
                        found_match = True
                        break
            if not found_match:
                print 'Oh noes!'
    if len(matched) != len(full_parses):
        print '!!!', s_name
        print 'solutions:', solutions
        raise RuntimeError

print 'DONE'
'''
for k, v in solutions_full.items():
    if v != solutions_sum[k] and ranked_forests[k]:
        print sents_dir + k
        print v, solutions_sum[k]
'''
for k, v in sorted(exceptions.items()):
    for f in sorted(exc_forests[k]):
        print f
    print v
    print '------------------------'
