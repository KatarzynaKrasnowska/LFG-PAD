# -*- coding: utf-8 -*-
'''
Created on 10-08-2013

@author: Katarzyna Krasnowska
'''

class SkladnicaCats:
    #TODO: polish characters should have unicode! - add and check
    ff = 'ff'
    fw = 'fw'
    fl = 'fl'
    flicz = 'flicz'
    fno = 'fno'
    fpm = 'fpm'
    fpmpt = 'fpmpt'
    fps = 'fps'
    fpt = 'fpt'
    fzd = 'fzd'
    modpart = 'modpart'
    posilk = 'posiłk'
    przec = 'przec'
    przyimek = 'przyimek'
    spojnik = 'spójnik'
    wypowiedzenie = 'wypowiedzenie'
    zdanie = 'zdanie'

class SkladnicaFs:
    rekcja = 'rekcja'
    tfw = 'tfw'
    stopien = u'stopień'
    dest = 'dest'
    neg = 'neg'
    czas = 'czas'
    przypadek = 'przypadek'
    przyim = 'przyim'

class SkladnicaRules:
    int4 = 'int4'     # '. . .'
    int11 = 'int11'   # '. . . ?'
    n_cz6 = 'n_cz6'   # 'będzie miał'
    n_cz11 = 'n_cz11' # 'wracali śmy'
    n_cz12 = 'n_cz12' # formaczas -> morf condaglt
    n_cz29 = 'n_cz29' # trzeba będzie
    n_cz36 = 'n_cz36' # 'powinna m'
    n_rz5 = 'n_rz5'
    n_rz7 = 'n_rz7'   # ('Jan <S.>')
    n_rz6 = 'n_rz6'   # ('1920 <r.>')
    n_pt2 = 'n_pt2'   # 'ideowo - wychowawczej'
    to2 = 'to2'       # 'była to'
    to8 = 'to8'       # 'jest to'p2)
    
    n_pt2 = 'n_pt2'
    
    w5 = 'w5'
    w6 = 'w6'
    
    zdr1 = 'zdr1'
    zdr2 = 'zdr2'
    zdsz1 = 'zdsz1'
    zdsz2 = 'zdsz2'
    zdsz3 = 'zdsz3'
    
    wer1 = 'wer1'
    wes1 = 'wes1'
    wes3 = 'wes3'
    
    p1 = 'p1'         # zdanie -> zdanie przec spójnik zdanie
    
    r1 = 'r1'
    r2 = 'r2'
    r3 = 'r3'
    s1 = 's1'
    s2 = 's2'
    s3 = 's3'
    nor1 = 'nor1'
    nor2 = 'nor2'
    nor3 = 'nor3'
    nos1 = 'nos1'
    nos2 = 'nos2'
    nos3 = 'nos3'
    pmr1 = 'pmr1'
    pmr2 = 'pmr2'
    pmr3 = 'pmr3'
    pms1 = 'pms1'
    pms2 = 'pms2'
    pmsz3 = 'pmsz3'
    pss3 = 'pss3'
    pimr1 = 'pimr1'
    pimr2 = 'pimr2'
    pims3 = 'pims3'
    ptsz3 = 'ptsz3'

'''in which head element look for predicate'''    
multiple_heads = {
    1 : set([
    'sr2', 'sr14', 'sr51', 'sr52', 'spoj48', 'n_cz6', 'n_cza2', 'n_cz13',
    'n_cz17', 'n_cz21', 'n_cz28', 'n_cz30', 'n_cz33', 'n_cz34', 'to2', 'to6',
    'to8', 'po4', 'int5']),
    2 : set(['n_pt2', 'n_cz8', 'n_cz15', 'n_cz16', 'n_cz18', 'n_cz23',
             'n_cz37',  # nowe (zamiast n_cz16?)
             'to3']),
    3 : set(['int11', 'int7',]) }

mwe = set(['jel3a', 'jel3b', 'jel3c', 'jel3d', 'eps3', 'eps11', 'eps12', 'eps13',
           'mp5', 'mp5', 'mp6', 'sr2', 'sr4', 'sr6', 'sr11', 'sr13', 'sr14', 'sr24',
           'sr25', 'sr26', 'sr51', 'sr52', 'spoj25', 'spoj34', 'spoj40', 'spoj48'])




