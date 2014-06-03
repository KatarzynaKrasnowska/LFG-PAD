# -*- coding: utf-8 -*-
'''
Created on 21-10-2013

@author: Katarzyna Krasnowska
'''

import sys
import subprocess
#sys.path.insert(0, '/home/kasia/Dokumenty/Robota/LFG/stochastic/')
from conf import *

from ReadProlog import read_prolog_file
from FStructure import build_fs, fs_to_tex

sys.setrecursionlimit(1000)

parse_list = 'dev-list'
parse_dir = 'dev-parses%s/' % FEATURES_SUFFIX
tex_dir = LFG_DIR + 'stochastic/' + parse_dir + 'tex/'

output_overall = True
output_individual = True
#EPS = 0.00001
rs = (800, 600, 400, 300, 250, 200, 150, 100, 80, 60, 40, 20, 10, 8, 6, 4, 2, 1)
adds = (50,)
print 'rm %s*' % tex_dir
subprocess.call('rm %s*' % tex_dir, shell=True)
print tex_dir
subprocess.call('cp %s/parses/avm.sty %s' % (LFG_DIR, tex_dir), shell=True)
sentences, sentences_0, wfs = [], [], []
results_overall = {}
results_individual = {}
with open(LFG_DIR + '/stochastic/' + parse_list, 'r') as sfile:
    sentences = tuple(l.replace('\n', '').split() for l in sfile.readlines())
with open(LFG_DIR + '/stochastic/' + parse_list + '-0', 'r') as sfile:
    sentences_0 = tuple(l.replace('\n', '').split() for l in sfile.readlines())
with open(WEIGHTS_FILES_LIST + FEATURES_SUFFIX, 'r') as wf_list:
    active_wfs = tuple(l.replace('\n', '') for l in wf_list.readlines() if not l.startswith('#'))
    #active_wfs = tuple((int(wf.replace('-0', '').replace('weights-file_r', '')), wf) for wf in wfs)
wfs = {}
for a in adds:
    wfs[a] = []
    for r in rs:
        for list_0 in (True,):#, False):
            s = '-0' if list_0 else ''
            wf = 'step-%d%s/weights-file%s_r%d' % (a, FEATURES_SUFFIX, s, r)
            if wf in active_wfs:
                wfs[a].append((r, wf))
print active_wfs
for sents, list_0 in ((sentences, False),):#, (sentences_0, True)):
    for a in adds:
        for r, wf in sorted(wfs[a]):
            print r, wf, list_0
            individual = []
            sentences_ranks = {}
            #avg_first_rank = 0.0
            c = 0
            j = 0.0
            correct = 0.0
            half_correct = 0.0
            all_correct = 0.0
            cutoff = 0.0
            for s_full, s_disamb in sents:
                c += 1
                if c % 100 == 0:
                    print c, '/', len(sentences)
                s_name = s_full.replace(LFG_DIR + 'parses/' + PARSES_VERSION + '/', '')
                s_prob = LFG_DIR + 'stochastic/' + parse_dir + wf + '/' + s_name[:-3] + PROB_SUFFIX
                data = None
                try:
                    data = read_prolog_file(s_prob, True)
                except IOError:
                    #print 'IOError'
                    continue
                if not data.text:
                    #print 'Oh noes!'
                    continue
                text = data.text
                solutions = data.num_solutions
                #print '*', len(data.opts), data.num_solutions
                weighted_constrs = {}
                for opts in data.opts:
                    weight = 0
                    for o in opts:
                        if o in data.choices_weights:
                            weight -= data.choices_weights[o]
                    constrs = tuple(c for c, l_no in data.constraint_list if c.cond.intersection(opts))
                    if not weight in weighted_constrs:
                        weighted_constrs[weight] = set()
                    weighted_constrs[weight].add((constrs, tuple(opts)))
                #print '***', len(data.opts)
                disamb_constrs = []
                data = read_prolog_file(s_disamb, True)
                num_disamb = len(data.opts)
                for opts in data.opts:
                    constrs = tuple(c for c, l_no in data.constraint_list if c.cond.intersection(opts))
                    disamb_constrs.append((tuple(sorted(opts)), constrs))
                #print '*****', len(data.opts)
                i = 0
                j += len(weighted_constrs)
                tex_fs = []
                #found_first = False
                num_first = 0
                opts_found = set()
                sentences_ranks[s_name] = set()
                for w, cs_set in sorted(weighted_constrs.items()):
                    i += 1
                    for cs, opts in cs_set:
                        found = False
                        for d_opts, d_cs in disamb_constrs:
                            if (cs == d_cs):
                                found = True
                                opts_found.add(d_opts)
                                if i == 1:
                                    #found_first = True
                                    num_first += 1
                            #fs, eqs = build_fs(cs)
                            #tex_fs.append((w, fs_to_tex(fs[0], fs, eqs)))
                        if found:
                            sentences_ranks[s_name].add(i)
                            #avg_first_rank += i
                if (len(opts_found) != num_disamb):
                    print '======================================'
                    print len(opts_found), num_disamb
                    print opts_found
                    print data.opts
                    raise RuntimeError
                half_disamb = float(num_disamb) / 2
                if not half_disamb:
                    half_disamb = 1.0
                #print num_first, num_disamb / 2, bool(num_first), num_first >= num_disamb / 2
                if num_first:
                    correct += 1
                if num_first >= half_disamb:
                    half_correct += 1
                if half_correct > correct:
                    print half_correct, correct
                    raise RuntimeError
                if sentences_ranks[s_name] == set([1]):
                    all_correct += 1
                coff = 1.0 - float(len(sorted(weighted_constrs.items()[0][1]))) / solutions
                cutoff += coff
                individual.append((s_name, solutions, num_first, coff))
                #tex_text = ('\\documentclass[8pt]{article}\n\\usepackage[utf8]{inputenc}\n' +
                #            '\\usepackage{polski}\n\usepackage{synttree}\n' +
                #            '\\usepackage[landscape, a4paper, top=20pt, bottom=20pt, left=20pt, right=20pt]{geometry}\n' +
                #            '\\usepackage{avm}\n\\avmoptions{bottom}\n\\avmfont{\\sc\\tiny}\n\n' +
                #            '\\usepackage[usenames,dvipsnames]{xcolor}\n' +
                #            '\\begin{document}\n\n\scriptsize{\n')
                #with open(tex_dir + s_name[:-3] + '.tex', 'w') as tf:
                #    tf.write(tex_text)
                #    for w, t in tex_fs:
                #        tf.write('\\subsection*{%.2f}' % w)
                #        tf.write('\\subsubsection*{\\textit{%s}}' % text.replace('-', ' '))
                #        tf.write(t + '\n')
                #        tf.write('\\newpage\n')
                #    tf.write('\\end{document}\n')
            avg_first_rank = 0.0
            avg_last_rank = 0.0
            avg_avg_rank = 0.0
            for s, ranks in sentences_ranks.items():
                avg_first_rank += sorted(ranks)[0]
                avg_last_rank += sorted(ranks)[-1]
                avg_avg_rank += sum(ranks) / len(ranks)
            avg_first_rank = avg_first_rank / len(sentences_ranks)
            avg_last_rank = avg_last_rank / len(sentences_ranks)
            avg_avg_rank = avg_avg_rank / len(sentences_ranks)
            print avg_first_rank, len(sentences_ranks), j, len(sentences_ranks)
            if sentences_ranks:
                accuracy = correct / len(sentences_ranks)
                half_accuracy = half_correct / len(sentences_ranks)
                all_accuracy = all_correct / len(sentences_ranks)
                cutoff = cutoff / len(sentences_ranks)
                results_overall[(a, wf, list_0)] = (accuracy, half_accuracy, all_accuracy, cutoff,
                                                    avg_first_rank, avg_last_rank, avg_avg_rank,
                                                    j / len(sentences_ranks))
                results_individual[(a, wf, list_0)] = tuple(sorted(individual))
            print

for a in adds:
    if output_overall:
        print LFG_DIR + 'stochastic/results%s/results_overall-n-step-%d.csv' % (FEATURES_SUFFIX, a)
        with open(LFG_DIR + 'stochastic/results%s/results_overall-n-step-%d.csv' % (FEATURES_SUFFIX, a), 'w') as f:
            f.write('TRAIN,R,ACCURACY,HALF.ACCURACY,ALL.ACCURACY,CUTOFF,AVG.F.RANK,AVG.L.RANK,AVG.A.RANK,AVGRANKS,TEST\n')
            for list_0 in (False, True):
                test = 'only0' if list_0 else 'all'
                for r, wf in sorted(wfs[a]):
                    if (a, wf, list_0) in results_overall:
                        wf_tmp = wf.replace('step-%d%s/' % (a, FEATURES_SUFFIX), '').replace('weights-file', '').replace('-0_r', 'only0,').replace('_r', 'all,')
                        form = (wf_tmp,) + results_overall[(a, wf, list_0)] + (test,)
                        f.write('%s,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%s\n' % form)
    if output_individual:
        for list_0 in (False, True):
            test = 'only0' if list_0 else 'all'
            for r, wf in sorted(wfs[a]):
                if (a, wf, list_0) in results_individual:
                    train = wf.replace('weights-file', '').replace('-0_r', 'only0') \
                              .replace('_r', 'all').replace('step-%d/' % a, '') \
                              .replace('%d' % r, '')
                    fname = 'results-step-%s-r-%d-train-%s-test-%s.csv' % (a, r, train, test)
                    with open(LFG_DIR + 'stochastic/results%s/%s' % (FEATURES_SUFFIX, fname), 'w') as f:
                        f.write('ID,SOLUTIONS,ACCURACY,CUTOFF\n')
                        for row in results_individual[(a, wf, list_0)]:
                            f.write('%s,%d,%d,%.3f\n' % row)