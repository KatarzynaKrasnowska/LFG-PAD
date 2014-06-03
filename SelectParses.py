# -*- coding: utf-8 -*-
'''
Created on 11-01-2013

@author: Katarzyna Krasnowska
'''

import os
import re
import sys
import traceback

from ReadProlog import read_prolog_file
from FStructure import build_fs, fs_to_tex, collect_fs_attrs, collect_attr_vals, collect_adj_attrs
from ParseConstraints import ConstraintType
from ParseNodes import Node
from ReadSkladnicaTree import make_parser, TreeHandler, has_pyza, has_on_prep
#from TextNormalizeFilter import text_normalize_filter
from FSFromSkladnica import fs_constrs_from_skladnica, check_with_skladnica_constrs_2
#from FSHelpers import get_from_fs, is_defined
from POLFIEInfo import old2newid, path_diff, skip_sets, val_attrs
from FixOpts import new_choices, fixed_conditions

#for debugging, default: 1000
sys.setrecursionlimit(1000)

labels = set()
adjacent_labels = set()
rules_set = set()

def choice_tree(node, choice):
    n = Node(node.n_id, node.label)
    for (ch, _) in ((ch, choices) for (ch, choices) in node.children if choices.intersection(choice)):
        n.children.append(choice_tree(ch, choice))
        n.children_ids.append(ch.n_id)
    if (n.children):
        labels.add(node.label)
        grandchildren = True
        for ch in n.children:
            if (ch.children):
                adjacent_labels.add((node.label, ch.label))
            if (not ch.children):
                grandchildren = False
        if grandchildren:
            rules_set.add(tuple([n.label] + [ch.label for ch in n.children]))
    return n

fs_attrs = set()
fs_attr_vals = set()
fs_adj_attrs = set()

def collect_fs_info(fs, eqs):
    fs_attrs.update(collect_fs_attrs(fs, eqs))
    fs_attr_vals.update(collect_attr_vals(fs, eqs))
    fs_adj_attrs.update(collect_adj_attrs(fs, eqs))

output_min_no_match, print_all_constrs, output_tex = False, False, False
output_min_no_match = True
#print_all_constrs = True
#output_tex = True

skladnica_v = '130301'
skladnica_v = '130718'
skladnica_v = '130909'
skladnica_v = '130925'
skladnica_v = '131011'
skladnica_v = '140410'
sentences = []
sents_file = ('/home/kasia/Dokumenty/Robota/LFG/Iness/agnieszka-gold-finished-30072013.txt')
sents_file = ('/home/kasia/Dokumenty/Robota/LFG/Iness/all.txt')
sents_file = ('/home/kasia/Dokumenty/Robota/LFG/Iness/all-16092013.txt')
sents_file = ('/home/kasia/Dokumenty/Robota/LFG/Iness/all-17092013.txt')
sents_file = ('/home/kasia/Dokumenty/Robota/LFG/Iness/all-11102013.txt')
sents_file = ('/home/kasia/Dokumenty/Robota/LFG/Iness/all-13012014.txt')
sents_file = ('/home/kasia/Dokumenty/Robota/LFG/Iness/all-02062014.txt')
#sents_file = ('/home/kasia/Dokumenty/Robota/LFG/Iness/test.txt')
with open (sents_file, 'r') as f:
    for l in f.readlines():
        if not (l.startswith('#')):
            s_name = re.match(r'.*(Skladnica.*-s).*', l).group(1)
            sentences.append(s_name)
sent_count = 0
success_count = 0
num_sents = len(sentences)
no_consistent = []
min_no_match = {}
sents_dir = 'disamb/30072013'
sents_dir = 'Skladnica_FULL_prolog_20130405'
sents_dir = 'FULL_16-09-2013'
sents_dir = 'FULL_20130917_newdict_Skladnica-130925'
sents_dir = 'FULL_20130917_newdict_Skladnica-131011'
sents_dir = 'FULL_20130917_newdict_Skladnica-131011_updated_map'
sents_dir = 'FULL_20130917_newdict_Skladnica-131011_updated_map'
sents_dir = 'Skladnica140410_FULL_prolog_POLFIE2v0.5_W-20140529'
#sents_dir = 'Skladnica_FULL_prolog_20130917_newdict'
#sents_dir = 'disamb/kasia-test'
file_suff = '-dis.pl'
file_suff = '.pl'
stats = 'SENT_ID,SOLUTIONS,NUM_BEST,PERCENTAGE_BEST\n'
sentences_solutions = {}
#sents_dir = 'agnieszka-disamb'
missing = []
os.system('rm /home/kasia/Dokumenty/Robota/LFG/parses/ranked/%s/*' % (sents_dir))
os.system('mkdir /home/kasia/Dokumenty/Robota/LFG/parses/ranked/%s' % (sents_dir))
tex_dir = '/home/kasia/Dokumenty/Robota/LFG/tex/' + sents_dir.replace('/', '_') + '/'
key_errors = set()
if output_tex:
    os.system('rm ' + tex_dir + '*')
    os.system('mkdir ' + tex_dir)
    os.system('cp /home/kasia/Dokumenty/Robota/LFG/parses/avm.sty ' + tex_dir)
processed = 0
for sent_name in sentences:
    sent_count += 1
    if sent_name in skip_sets[sents_dir]:
        #print 'SKIP:', sent_name
        continue
    print '-----', sent_count, '/',  num_sents, sent_name
    path = '/home/kasia/Dokumenty/Robota/LFG/parses/%s/' %  sents_dir + sent_name + file_suff #dla disamb trzeba dis
    try:
        open(path, 'r')
    except:
        print 'CAN\'T OPEN:', path
        continue
    prolog_data = read_prolog_file(path, max_solutions=10000)
    if prolog_data is None:
        continue
    num_solutions, text = prolog_data.num_solutions, prolog_data.text
    #num_solutions, text, constraint_list, phis, other_list, choices_list, nodes, root_id, opts, all_lines = read_prolog_file(path)
    sentences_solutions[sent_name] = num_solutions
    if (num_solutions < 1):
        continue
    processed += 1
    if (num_solutions > 10000):
        continue
    num_consistent = 0.0
    count = 0
    #====
    skladnica_path = '/home/kasia/Dokumenty/Robota/Świgrowe/zrobione%s/' % skladnica_v + \
                     sent_name.replace('Skladnica--FULL', 'NKJP_1M') \
                     .replace('_morph', '/morph') + '.xml'
    #for old, new in old2newid.items():
    #    skladnica_path = skladnica_path.replace(old + '/', new + '/')
    for s1, s2 in path_diff:
        skladnica_path = skladnica_path.replace(s1, s2)
    #downstream_handler = XMLGenerator()
    #parser = text_normalize_filter(make_parser(),  downstream_handler)
    parser = make_parser()
    parser.setContentHandler(TreeHandler())
    try:
        parser.parse(skladnica_path)
    except:
        missing.append((sent_name, text))
        continue
    if parser.getContentHandler().success:
        t = parser.getContentHandler().skladnicaTree()
        #print t
        skladnica_constrs = fs_constrs_from_skladnica(t)
        if u'być' in skladnica_constrs:
            print 'TODO: BYĆ'
            #continue
        #if u'I' in skladnica_constrs:
        #    print 'TODO: I'
        #    continue
        for pred, c_dict in skladnica_constrs.items():
            for n_id, cs in c_dict.items():
                if print_all_constrs:
                    print pred, n_id
                    print cs
    else:
        print 'Skladnica - no parse'
        continue
    known_problem = False#has_pyza(t) or has_on_prep(t)
    #====
    no_match = {}
    tex = {}
    print 'SOLUTIONS:', num_solutions
    tex_text = ('\\documentclass[8pt]{article}\n\\usepackage[utf8]{inputenc}\n' +
                '\\usepackage{polski}\n\usepackage{synttree}\n' +
                '\\usepackage[landscape, a4paper, top=20pt, bottom=20pt, left=20pt, right=20pt]{geometry}\n' +
                '\\usepackage{avm}\n\\avmoptions{bottom}\n\\avmfont{\\sc\\tiny}\n\n' +
                '\\usepackage[usenames,dvipsnames]{xcolor}\n' +
                '\\begin{document}\n\n\scriptsize{\n')
    for o in prolog_data.opts:
        #print o
        count += 1
        if (num_solutions > 20 and count % (num_solutions / 10) == 0):
            print count, '/', num_solutions
        #print 'tree', count, '====================================='
        try:
            fs, eqs_dict = build_fs([c for c, l_no in prolog_data.constraint_list if c.cond.intersection(o)]) #{}
            collect_fs_info(fs, eqs_dict)
            #t = fs_to_tex(fs[0], fs, eqs_dict).replace('_', '\\_')
            #print eqs_dict
            #for v, eq in sorted(eqs_dict.items()):
            #    print v, sorted(eq)
            #for c in [c for c in constraint_list if c.cond.intersection(o)]:
            #    print c
            #for k, v in sorted(fs.items()):
            #    print k, ':', v
            #print eqs_dict
        except KeyError as err:
            key_errors.add(sent_name)
            continue
        except:
            print 'f-structure problem'
            traceback.print_exc()
            #for c in [c for c in constraint_list if c.cond.intersection(o)]:
            #    print c.type, c.arg1, c.arg2
            #print len(fs)
            #for k, v in fs.items():
            #    print k, v
            raise
        try:
            n_m = check_with_skladnica_constrs_2(skladnica_constrs, fs, eqs_dict)
            if (known_problem and n_m == 1):
                n_m = 0
        except KeyError:
            raise
            #n_m = 0
        if not n_m in no_match:
            no_match[n_m] = []
            tex[n_m] = []
        no_match[n_m].append(o)
        consistent = n_m == 0
        #if sent_name == 'Skladnica--FULL_1202900101_morph_3-p_morph_3.17-s' and o == set(['1', 'I3', 'A9']):
        #    for c in [c for c in constraint_list if c.cond.intersection(o)]:
        #        print c.type, c.arg1, c.arg2
        #    for k, v in fs.items():
        #        print k, v
        #consistent = True
        t = '\\subsection*{%d %s}\n' % (count, o)
        t += choice_tree(prolog_data.nodes[prolog_data.root_id], o).tex() + '\\\\[30pt]\n'
        t += fs_to_tex(fs[0], fs, eqs_dict).replace('_', '\\_') + '\n'
        t += '\\newpage\n'
        tex[n_m].append(t)
        if consistent:
            num_consistent += 1
        #print_fs(fs[0], fs)
        #====min_n_m = sorted(no_match.items())[0][0]
        #====
    min_n_m = sorted(no_match.items())[0][0]
    for t in tex[min_n_m]:
        tex_text += t
    if output_tex:
        with open(tex_dir + sent_name + '.tex', 'w') as tex_file:
            tex_file.write(tex_text + '\n}\n\\end{document}')
    print sent_name, text
    if (count != num_solutions):
        print 'TREES != SOLUTIONS'
        #continue
        #break
    print 'CONSISTENT', int(num_consistent), '(%.1f' % (num_consistent * 100 / num_solutions) + '%)'
    num_best = len(sorted(no_match.items())[0][1]) * 1.0
    print 'BEST MATCH', int(num_best), '(%.1f' % (num_best * 100 / num_solutions) + '%)'
    stats += '%s,%d,%d,%f\n' % (sent_name, num_solutions, num_best, (num_best * 100 / num_solutions))
    if (not num_consistent):
        no_consistent.append((sent_name, text, skladnica_constrs))
    #min_n_m = sorted(no_match.items())[0][0]
    if not min_n_m in min_no_match:
        min_no_match[min_n_m] = []
    min_no_match[min_n_m].append((text, sent_name))
    check_solutions_sum = 0
    for num_no_match in no_match.keys():
        #print '\nprinting out for num_no_match:', num_no_match
        active_opts = set(['1',])
        #print no_match[min_n_m]
        #for opts in no_match[num_no_match]:
        #    print opts
        fixed_choices, renamings, equivalences, merged = new_choices(no_match[num_no_match])
        #    match_opts.update(opts)
        ranked_f = '/home/kasia/Dokumenty/Robota/LFG/parses/ranked/%s/%s-%d.pl' % (sents_dir, sent_name, num_no_match)
        with open(ranked_f, 'w') as mfile:
            mfile.write(''.join(prolog_data.all_lines[:15]))
            mfile.write('\t% Choices:\n\t[\n')
            ls = []
            opts_map = {}
            #for ch, l_no in prolog_data.choices_list:
            for ch in fixed_choices:
                #print ch
                active_opts.update(ch.conditions)
                active_opts.update(ch.choices)
                ls.append(ch.prolog())
                '''old_choices = ch.choices
                old_conditions = ch.conditions
                #ch.choices = [c for c in ch.choices if c in match_opts]
                #ch.conditions = [c for c in ch.conditions if c in match_opts]
                if (len(ch.choices) == len(ch.conditions) == 1):
                    o1, o2 = ch.choices[0], ch.conditions[0]
                    #if o2 in opts_map:
                    #    o2 = opts_map[o2]
                    #opts_map[o1] = o2
                    if not o1 in opts_map:
                        opts_map[o1] = set()
                    opts_map[o1].add(o2)
                for i in xrange(0, len(ch.choices)):
                    if ch.choices[i] in opts_map:
                        ch.choices[i] = opts_map[ch.choices[i]]
                for i in xrange(0, len(ch.conditions)):
                    if ch.conditions[i] in opts_map:
                        ch.conditions[i] = opts_map[ch.conditions[i]]
                if (ch.choices and ch.conditions and ch.choices != ch.conditions):
                    ls.append(ch.prolog())
                ch.choices = old_choices
                ch.conditions = old_conditions'''
            #for op in match_opts:
            #    if not op in opts_map:
            #        opts_map[op] = op
#             print opts_map
            #print 'ACTIVE:', active_opts
            mfile.write(',\n'.join(ls) + '\n')
            mfile.write('\t],\n\t% Equivalences:\n\t[\n\t\n\t],\n\t% Constraints:\n\t[\n')
            ls = []
            for constr, l_no in prolog_data.constraint_list:
                old_cond = constr.cond
                constr.cond = fixed_conditions(constr.cond, active_opts, renamings, equivalences, merged)#sorted(set([opts_map[c] for c in constr.cond if c in match_opts]))
                if (constr.cond):
                    ls.append(constr.prolog())
                constr.cond = old_cond
            mfile.write(',\n'.join(ls) + '\n')
            mfile.write('\t],\n\t% C-Structure:\n\t[\n')
            ls = []
            for phi, l_no in prolog_data.phis:
                old_choices = phi.choices
                phi.choices = fixed_conditions(phi.choices, active_opts, renamings, equivalences, merged)#sorted(set([opts_map[c] for c in phi.choices if c in active_opts]))
                if (phi.choices):
                    ls.append((l_no, phi.prolog()))
                phi.choices = old_choices
            for other, l_no in prolog_data.other_list:
                old_choices = other.choices
                other.choices = fixed_conditions(other.choices, active_opts, renamings, equivalences, merged)#sorted(set([opts_map[c] for c in other.choices if c in active_opts]))
                if (other.choices):
                    ls.append((l_no, other.prolog()))
                    #print type(other), other.prolog()
                other.choices = old_choices
            ls = [l for l_no, l in sorted(ls)]
            mfile.write(',\n'.join(ls) + '\n')
            mfile.write('\t]).\n')
        r_prolog_data = read_prolog_file(ranked_f, quiet=True, max_solutions=1000000)
        for o in r_prolog_data.opts:
            r_fs, r_eqs_dict = build_fs([c for c, l_no in r_prolog_data.constraint_list if c.cond.intersection(o)])
        check_solutions_sum += len(r_prolog_data.opts)
    if check_solutions_sum != num_solutions and not sent_name in key_errors:
        print key_errors
        raise RuntimeError
    success_count += 1
print 'SUCCESS:', success_count
print '\n\n'
for sent_name, text, constrs in sorted(no_consistent):
    print text.replace('-', ' '), '    - ' ,sent_name
    for pred, c_dict in constrs.items():
        for n_id, cs in c_dict.items():
            print pred
            print cs
    print '\n'
print len(no_consistent)
print
for sent_name, text, constrs in no_consistent:#sorted(no_consistent):
    print text, sent_name
print
for m, sents in min_no_match.items():
    print m, len(sents)
    #for _, sent_name, opts in sents:
    #    print sent_name
    #    print '    ', opts
with open('/home/kasia/Dokumenty/Robota/LFG/stochastic/sents-list', 'w') as f:
    ms = []
    for m, sents in min_no_match.items():
        ms += [s[1] + ' ' + s[1] + '-' + str(m) for s in sents if not s[1] in key_errors]
    for x in sorted(ms):
        f.write(x + '\n')
ms = []
print stats
if output_min_no_match:
    with open('/home/kasia/Dokumenty/Robota/LFG/parses/min-no-match-' + sents_dir.replace('/', '_') + '.csv', 'w') as matchfile:
        ms = []
        for m, sents in min_no_match.items():
            ms += [(s[1], s[0], m) for s in sents]
        for x in sorted(ms):
            matchfile.write('%s\t%s\t%d' % x + '\n')
    with open('/home/kasia/Dokumenty/Robota/LFG/parses/kolizje-' + sents_dir.replace('/', '_') + '.csv', 'w') as matchfile:
        ms = {}
        for m, sents in min_no_match.items():
            for s in sents:
                ms[s[1]] = (s[0], m)
        for s in sentences:
            if not s in ms:
                continue
            if ms[s][1] > 0:
                matchfile.write('%s\t%d\t%s\t%d' % (s, sentences_solutions[s], ms[s][0], ms[s][1]) + '\n')
    with open('/home/kasia/Dokumenty/Robota/LFG/parses/stats-' + sents_dir.replace('/', '_') + '.csv', 'w') as statsf:
        statsf.write(stats)
        for s, t in missing:
            print s, t
with open('/home/kasia/Dokumenty/Robota/LFG/features/' + sents_dir, 'w') as ffile:
    for l in sorted(labels):
        ffile.write('cs_label %s\n' % l)
    for p, c in sorted(adjacent_labels):
        ffile.write('cs_adjacent_label %s %s\n' % (p, c))
    for p in sorted(labels):
        for d in sorted(labels):
            ffile.write('cs_sub_label %s %s\n' % (p, d))
    for r in sorted(rules_set):
        ffile.write('cs_sub_rule %s\n' % ' '.join(r))
    for l in sorted(labels):
        ffile.write('cs_num_children %s\n' % l)
    for l in sorted(labels):
        for x in xrange(2, 5):
            ffile.write('cs_embedded %s %d\n' % (l, x))
    ffile.write('cs_right_branch\n')
    
    for a in sorted(fs_attrs):
        ffile.write('fs_attrs %s\n' % a)
    for a, v in sorted(fs_attr_vals):
        ffile.write('fs_attr_val %s %s\n' % (a , v))
    for p, c in sorted(fs_adj_attrs):
        ffile.write('fs_adj_attrs %s %s\n' % (p , c))
    
#fs_attrs    fs_attrs OBL-COMPAR
#fs_attr_val fs_attr_val COMP-FORM if
#fs_adj_attrs  fs_adj_attrs ADJUNCT SUBJs
#fs_auntsubattrs  fs_auntsubattrs 2 ADJUNCT NAME-MOD 6 OBJ OBJ-TH COMP-EX OBL COMP XCOMP 1 PRED
#verb_arg    pred arg    verb_arg read OBJ     counts the number of occurences of verb pred with argument arg     
#lex_subcat
    
print processed
for s in key_errors:
    print 'key error:', s
    os.system('rm /home/kasia/Dokumenty/Robota/LFG/parses/ranked/%s/%s*' % (sents_dir, s))