# -*- coding: utf-8 -*-
'''
Created on 10-08-2013

@author: Katarzyna Krasnowska
'''

attrs_order = ('PRED', 'SUBJ', 'OBJ', 'OBL', 'OBL-STR', 'OBL-INST', 'OBL2', 'OBL3',
               'XCOMP', 'XCOMP-PRED', 'POSS', 'ADJUNCT', 'XADJUNCT')

val_attrs = set(['ACM', 'ASPECT', 'ATYPE', 'CASE', 'CLAUSE-TYPE', 'COMP-FORM', 'COORD-FORM', 'DEGREE',
                 'GEND', 'IMPERSONAL', 'MOOD', 'NEG', 'NUM', 'PASSIVE', 'PERS', 'PFORM', 'PRECOORD-FORM',
                 'PTYPE', 'REFLEXIVE', 'TENSE', 'TYPE'])

no_tex_attrs = val_attrs.union(set(['CHECK', 'TNS-ASP', 'NTYPE']))

fs_attrs = set(['ADJUNCT', 'APP', 'COMP', 'OBJ', 'OBJ-TH', 'OBL', 'OBL-COMPAR', 'OBL-GEN', 'OBL-INST', 'OBL-STR',
                'POSS', 'SUBJ', 'XADJUNCT', 'XCOMP', 'XCOMP-PRED'])

old2newid = {
'NKJP_1M_.' : 'NKJP_1M_7123900001',
'NKJP_1M_000500-GazetaPomorska' : 'NKJP_1M_GazetaPomorska',
'NKJP_1M_001000-DziennikPolski1980' : 'NKJP_1M_DP1980',
'NKJP_1M_012750-Rzeczpospolita' : 'NKJP_1M_Rzeczpospolita',
'NKJP_1M_010200-ZycieWarszawyPLUSZycie' : 'NKJP_1M_ZycieWarszawyPLUSZycie',
'NKJP_1M_031875-SuperExpress' : 'NKJP_1M_SuperExpress',
'NKJP_1M_012750-TrybunaPLUSTrybunaLudu' : 'NKJP_1M_TrybunaPLUSTrybunaLudu',
'NKJP_1M_1998' : 'NKJP_1M_DP1998',
'NKJP_1M_1999' : 'NKJP_1M_DP1999',
'NKJP_1M_2000' : 'NKJP_1M_DP2000',
'NKJP_1M_2001' : 'NKJP_1M_DP2001',
'NKJP_1M_2002' : 'NKJP_1M_DP2002',
'NKJP_1M_2003' : 'NKJP_1M_DP2003',
'NKJP_1M_2004' : 'NKJP_1M_DP2004',
}

path_diff = [('ZycieWarszawy_Zycie', 'ZycieWarszawyPLUSZycie'),
             ('TrybunaLudu_Trybuna', 'TrybunaPLUSTrybunaLudu'),
             ('Trybuna_TrybunaLudu', 'TrybunaPLUSTrybunaLudu'),
             ('NIE', '4scal-NIE'),
             ('KOT', '4scal-KOT')]

skip_sets = {'Skladnica_FULL_prolog_20130405' : 
             set(['Skladnica--FULL_2002000154_morph_7-p_morph_7.25-s',
                  'Skladnica--FULL_1302910000006_morph_84-p_morph_84.20-s',
                  'Skladnica--FULL_1305000000027_morph_1-p_morph_1.71-s',
                  #'Skladnica--FULL_NIE_morph_54-p_morph_54.49-s', #Ale-po-co-ogłaszać-przetarg-,-skoro-muszą-wygrać-partnerzy-biznesowi-Stanisława-K-.-?
                  'Skladnica--FULL_ZycieWarszawy_Zycie_morph_30-p_morph_30.23-s',
                  'Skladnica--FULL_SuperExpress_morph_507-p_morph_507.59-s',
                  'Skladnica--FULL_1302910000004_morph_6-p_morph_6.23-s',
                  'Skladnica--FULL_1204900000001_morph_146-p_morph_146.49-s',
                  'Skladnica--FULL_1204900008_morph_7-p_morph_7.21-s',
                  'Skladnica--FULL_3302000000028_morph_37-p_morph_37.43-s']),
             'FULL_16-09-2013' :
             set(['Skladnica--FULL_1305000000988_morph_1-p_morph_1.18-s',
                  'Skladnica--FULL_1305000001801_morph_1-p_morph_1.28-s',
                  'Skladnica--FULL_3202000000090_morph_1-p_morph_1.17-s',
                  'Skladnica--FULL_1305000000027_morph_1-p_morph_1.71-s',
                  'Skladnica--FULL_Rzeczpospolita_morph_139-p_morph_139.19-s',
                  'Skladnica--FULL_1303900001_morph_130-p_morph_130.21-s',
                  'Skladnica--FULL_NIE_morph_30-p_morph_30.55-s',
                  'Skladnica--FULL_1202000008_morph_11-p_morph_11.73-s',
                  'Skladnica--FULL_6203010000042_morph_3-p_morph_3.15-s',
                  'Skladnica--FULL_1202900001000_morph_24-p_morph_24.69-s',
                  'Skladnica--FULL_TrybunaLudu_Trybuna_morph_129-p_morph_129.35-s',
                  'Skladnica--FULL_6203010001855_morph_3-p_morph_3.60-s',
                  'Skladnica--FULL_1305000000109_morph_1-p_morph_1.10-s',
                  'Skladnica--FULL_1305000001266_morph_1-p_morph_1.51-s',
                  'Skladnica--FULL_3102000027_morph_3-p_morph_3.30-s']),
             'Skladnica_FULL_prolog_20130917_newdict' :
             set(['Skladnica--FULL_1305000000988_morph_1-p_morph_1.18-s',
                  'Skladnica--FULL_1305000001801_morph_1-p_morph_1.28-s',
                  'Skladnica--FULL_1303910001_morph_60-p_morph_60.49-s', #-1 solutions
                  'Skladnica--FULL_3202000000090_morph_1-p_morph_1.17-s',
                  'Skladnica--FULL_1305000000027_morph_1-p_morph_1.71-s',
                  'Skladnica--FULL_1102000010_morph_6-p_morph_6.82-s', #-1 solutions
                  'Skladnica--FULL_1303900001_morph_130-p_morph_130.21-s',
                  'Skladnica--FULL_NIE_morph_30-p_morph_30.55-s',
                  'Skladnica--FULL_1202000008_morph_11-p_morph_11.73-s',
                  'Skladnica--FULL_6203010000042_morph_3-p_morph_3.15-s',
                  'Skladnica--FULL_6203010001855_morph_3-p_morph_3.60-s',
                  'Skladnica--FULL_1202900094_morph_6-p_morph_6.52-s', #nowe
                  'Skladnica--FULL_3302000000027_morph_43-p_morph_43.61-s', #-1 solutions
                  'Skladnica--FULL_1305000000109_morph_1-p_morph_1.10-s',
                  'Skladnica--FULL_GazetaTczewska_morph_15-p_morph_15.42-s', #-1 solutions
                  'Skladnica--FULL_1305000001266_morph_1-p_morph_1.51-s',
                  'Skladnica--FULL_3102000027_morph_3-p_morph_3.30-s',
                  'Skladnica--FULL_1204900011_morph_40-p_morph_40.27-s', #0 solutions
                  'Skladnica--FULL_1102000008_morph_7-p_morph_7.41-s', #0 solutions
                  'Skladnica--FULL_2004000000507_morph_2-p_morph_2.50-s', #0 solutions
                  ]),
             'FULL_20130917_newdict_Skladnica-130925':
             set([#'Skladnica--FULL_1305000000988_morph_1-p_morph_1.18-s',
                  'Skladnica--FULL_1305000001801_morph_1-p_morph_1.28-s',
                  #'Skladnica--FULL_1303910001_morph_60-p_morph_60.49-s', #-1 solutions
                  'Skladnica--FULL_3202000000090_morph_1-p_morph_1.17-s',
                  'Skladnica--FULL_1305000000027_morph_1-p_morph_1.71-s',
                  #'Skladnica--FULL_1102000010_morph_6-p_morph_6.82-s', #-1 solutions
                  'Skladnica--FULL_1303900001_morph_130-p_morph_130.21-s',
                  'Skladnica--FULL_NIE_morph_30-p_morph_30.55-s',
                  'Skladnica--FULL_1202000008_morph_11-p_morph_11.73-s',
                  'Skladnica--FULL_6203010000042_morph_3-p_morph_3.15-s',
                  'Skladnica--FULL_6203010001855_morph_3-p_morph_3.60-s',
                  'Skladnica--FULL_1202900094_morph_6-p_morph_6.52-s', #nowe
                  #'Skladnica--FULL_3302000000027_morph_43-p_morph_43.61-s', #-1 solutions
                  'Skladnica--FULL_1305000000109_morph_1-p_morph_1.10-s',
                  #'Skladnica--FULL_GazetaTczewska_morph_15-p_morph_15.42-s', #-1 solutions
                  'Skladnica--FULL_1305000001266_morph_1-p_morph_1.51-s',
                  'Skladnica--FULL_3102000027_morph_3-p_morph_3.30-s',
                  #'Skladnica--FULL_1204900011_morph_40-p_morph_40.27-s', #0 solutions
                  #'Skladnica--FULL_1102000008_morph_7-p_morph_7.41-s', #0 solutions
                  #'Skladnica--FULL_2004000000507_morph_2-p_morph_2.50-s', #0 solutions
                  'Skladnica--FULL_1305000001381_morph_1-p_morph_1.17-s',
                  'Skladnica--FULL_1302910000004_morph_6-p_morph_6.23-s',
                  'Skladnica--FULL_Trybuna_TrybunaLudu_morph_129-p_morph_129.35-s',
                  ]),
             'FULL_20130917_newdict_Skladnica-131011':
             set([#'Skladnica--FULL_1305000000988_morph_1-p_morph_1.18-s',
                  'Skladnica--FULL_1305000001801_morph_1-p_morph_1.28-s',
                  #'Skladnica--FULL_1303910001_morph_60-p_morph_60.49-s', #-1 solutions
                  'Skladnica--FULL_3202000000090_morph_1-p_morph_1.17-s',
                  'Skladnica--FULL_1305000000027_morph_1-p_morph_1.71-s',
                  #'Skladnica--FULL_1102000010_morph_6-p_morph_6.82-s', #-1 solutions
                  'Skladnica--FULL_1303900001_morph_130-p_morph_130.21-s',
                  'Skladnica--FULL_NIE_morph_30-p_morph_30.55-s',
                  'Skladnica--FULL_1202000008_morph_11-p_morph_11.73-s',
                  'Skladnica--FULL_6203010000042_morph_3-p_morph_3.15-s',
                  'Skladnica--FULL_6203010001855_morph_3-p_morph_3.60-s',
                  'Skladnica--FULL_1202900094_morph_6-p_morph_6.52-s', #nowe
                  #'Skladnica--FULL_3302000000027_morph_43-p_morph_43.61-s', #-1 solutions
                  'Skladnica--FULL_1305000000109_morph_1-p_morph_1.10-s',
                  #'Skladnica--FULL_GazetaTczewska_morph_15-p_morph_15.42-s', #-1 solutions
                  'Skladnica--FULL_1305000001266_morph_1-p_morph_1.51-s',
                  'Skladnica--FULL_3102000027_morph_3-p_morph_3.30-s',
                  #'Skladnica--FULL_1204900011_morph_40-p_morph_40.27-s', #0 solutions
                  #'Skladnica--FULL_1102000008_morph_7-p_morph_7.41-s', #0 solutions
                  #'Skladnica--FULL_2004000000507_morph_2-p_morph_2.50-s', #0 solutions
                  'Skladnica--FULL_1305000001381_morph_1-p_morph_1.17-s',
                  'Skladnica--FULL_1302910000004_morph_6-p_morph_6.23-s',
                  'Skladnica--FULL_Trybuna_TrybunaLudu_morph_129-p_morph_129.35-s',
                  'Skladnica--FULL_3102000000212_morph_3-p_morph_3.72-s', #nowe
                  'Skladnica--FULL_NIE_morph_54-p_morph_54.49-s', #Ale-po-co-ogłaszać-przetarg-,-skoro-muszą-wygrać-partnerzy-biznesowi-Stanisława-K-.-?
                  'Skladnica--FULL_1303910001_morph_206-p_morph_206.16-s',
                  'Skladnica--FULL_forumowisko.pl_57_morph_7-p_morph_7.25-s',
                  ]),
             'FULL_20130917_newdict_Skladnica-131011_updated_map':
             set([
                  ]),
             'Skladnica140410_FULL_prolog_POLFIE2v0.5_W-20140529':
             set([
                  ]),
             'Skladnica140410_FULL_prolog_POLFIE2v0.5_W-20140608':
             set([
                  'Skladnica--FULL_1305000001881_morph_1-p_morph_1.40-s', # nie zgadza się num_solutions
                  ]),
             }