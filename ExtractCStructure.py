# -*- coding: utf-8 -*-
'''
Created on 07-04-2014

@author: Katarzyna Krasnowska
'''

import re

from ReadProlog import read_prolog_file

sents_dir = '/home/kasia/Dokumenty/Robota/LFG/parses/FULL_20130917_newdict_Skladnica-131011_updated_map/'
sents_file = '/home/kasia/Dokumenty/Robota/LFG/Iness/all-13012014.txt'
#ranked_dir = '/home/kasia/Dokumenty/Robota/LFG/parses/ranked/FULL_20130917_newdict_Skladnica-131011_updated_map/'

MAX_SOLUTIONS = 8

sentences = []
with open (sents_file, 'r') as f:
    for l in f.readlines():
        if not (l.startswith('#')):
            s_name = re.match(r'.*(Skladnica.*-s).*', l).group(1)
            sentences.append(s_name)

i = 0
for s_name in sentences[3917:3930]:
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
    if solutions > 7 and solutions <= MAX_SOLUTIONS:
        print full_forest
        prolog_data = read_prolog_file(full_forest, quiet=True, max_solutions=MAX_SOLUTIONS)
        print prolog_data.text
        for n_id, node in prolog_data.nodes.items():
            print node.short()
        print prolog_data.nodes