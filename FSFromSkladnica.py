# -*- coding: utf-8 -*-
'''
Created on 14-05-2013

@author: Katarzyna Krasnowska
'''

from ReadSkladnicaTree import SkladnicaCats, SkladnicaFs, SkladnicaRules
from FStructure import AttributeStructure, Semform
from SkladnicaInfo import multiple_heads
from FSHelpers import get_from_fs
from FSConstrs import SkladnicaConstrs
from PrepnpToObl import get_prepnp_sem_obls
from AdvpToObl import get_advp_sem_obls

class Special:
    advp = 'advp'
    sentp = 'sentp'
    infp = 'infp'

czy_list = (u'CZY', u'CZYŻ', u'CZYŻBY', u'AZALI', u'AZALIŻ', u'LI')
czy_list = [czy.lower() for czy in czy_list]

arg_attrs = ('SUBJ', 'OBJ', 'OBJ-TH', 'OBL-GEN', 'OBL-INST', 'OBL-STR',
             'OBL', 'OBL2', 'OBL3',
             'OBL-AG', 'OBL-COMPAR', 'OBL-ABL', 'OBL-ADL', 'OBL-DUR',
             'OBL-LOCAT', 'OBL-MOD', 'OBL-PERL', 'OBL-TEMP',
             'OBL-ADV',
             'COMP', 'XCOMP', 'XCOMP-PRED') # TODO complete the list

OPT = '-opt'
BARDZO = 'bardzo'
SIE = '_się'

# TODO - udawać_się, udać_się może mieć SUBJ w znaczeniu 'iść'!
no_subj = set([
    #u'chcieć_się', u'czas', u'można', u'należeć', u'pora', u'udawać_się', u'udać_się',
    #u'warto', u'żal', u'szkoda', u'trzeba', u'wolno', u'wstyd'
    u'brak', u'brakować', u'bywać', u'być', u'chcieć_się', u'chodzić', u'czas',
    u'czuć', u'dochodzić', u'dojść', u'iść', u'jechać', u'mieć_się', u'można',
    u'należeć', u'odbijać_się', u'odchodzić', u'odejść', u'odrzucać', u'pachnieć',
    u'pora', u'przybywać', u'przybyć', u'pójść', u'robić_się', u'skręcać',
    u'skręcić', u'stać', u'stać_się', u'szkoda', u'słychać', u'trudno', u'trzeba',
    u'uczynić_się', u'udawać_się', u'udać_się', u'warto', u'wiadomo', u'widać',
    u'wieść_się', u'wolno', u'wstyd', u'wystarczyć', u'zabraknąć', u'zależeć',
    u'zanieść', u'zanieść_się', u'zanosić', u'zanosić_się', u'zbierać_się',
    u'zebrać_się', u'zemrzeć_się', u'znać', u'zrobić_się', u'śpieszyć_się', u'żal'
])

#opt_subj = set([u'udawać_się', u'udać_się'])
opt_subj = set([
    u'bywać', u'być', u'chodzić', u'czuć', u'dochodzić', u'dojść', u'iść',
    u'jechać', u'mieć_się', u'należeć', u'odbijać_się', u'odchodzić', u'odejść',
    u'odrzucać', u'pachnieć', u'przybywać', u'przybyć', u'pójść', u'robić_się',
    u'skręcać', u'skręcić', u'stać', u'stać_się', u'uczynić_się', u'udawać_się',
    u'udać_się', u'wystarczyć', u'zależeć', u'zanieść', u'zanieść_się', u'zanosić',
    u'zanosić_się', u'zbierać_się', u'zebrać_się', u'znać', u'zrobić_się',
    u'śpieszyć_się'
])

obj_th_pro = set([
    u'bronić', u'chcieć_się', u'dawać', u'dawać_się', u'dać', u'dać_się', u'doradzić', u'dozwolić',
    u'kazać', u'kłaść', u'nauczyć', u'obiecać', u'obiecywać', u'pomagać', u'pomóc', u'poradzić',
    u'postawić', u'pozwalać', u'pozwolić', u'położyć', u'proponować', u'przeszkadzać', u'radzić',
    u'szkoda', u'trzeba', u'udawać_się', u'udać_się', u'uczyć', u'układać', u'ułożyć',
    u'wolno', u'wstyd', u'zabraniać', u'zaproponować', u'życzyć'
])

obj_pro = set([
    u'kłaść', u'nauczyć', u'położyć', u'uczyć', u'układać', u'ułożyć', u'czynić', u'mieć', u'nazwać',
    u'ogłosić', u'ogłoszać', u'pamiętać', u'robić', u'uczynić', u'widzieć', u'znajdować', u'znaleźć'
])

comp_classes = {
                u'że' : set([u'że', u'iż']),
                u'żeby' : set([u'żeby', u'iżby', u'by', u'aby', u'ażeby']),
                u'dopóty' : set([u'dopóty', u'póty']),
                u'wówczas' : set([u'wówczas', u'wtedy']),
                u'to_jednak' : set([u'jednak', u'to_jednak']),
                u'to' : set([u'to']),
                u'dopóki' : set([u'dopóki', u'póki']),
                u'choćby' : set([u'choćby', u'chociażby']),
                u'gdyby' : set([u'gdyby', u'jeśliby', u'jeżeliby']),
                u'bo' : set([u'albowiem', u'bo', u'gdyż']),
                u'więc' : set([u'przeto', u'więc', u'zatem', u'toteż']),
                u'chociaż' : set([u'chociaż', u'choć', u'mimo_że']),
                u'gdy' : set([u'gdy', u'kiedy']),
                u'jeśli' : set([u'jeśli', u'jeżeli']),
                u'ponieważ' : set([u'ponieważ', u'skoro']),
                u'zanim' : set([u'zanim', u'nim'])
                }

tfw_to_attr_dict = {
                    'adjp(mian)' : set(['XCOMP-PRED']),
                    'adjp(narz)' : set(['XCOMP-PRED']), #TODO skonsultować
                    #'advp' : set([Special.advp]), # problem zgłoszony przez Witka (not needed anymore?)
                    #'infp(dk)' : set(['XCOMP']),
                    #'infp(nd)' : set(['XCOMP']), # Postanowili-śmy-iść-za-tym-pomysłem-.
                    'np(bier)' : set(['OBJ', 'OBL-STR', 'OBL-DUR']),
                    'np(cel)' : set(['OBJ', 'OBJ-TH']),
                    'np(dop)' : set(['OBJ', 'OBL-GEN', 'OBL-STR', 'OBL-TEMP']),
                    'np(mian)' : set(['XCOMP-PRED', 'OBL-STR']),
                    'np(narz)' : set(['XCOMP-PRED', 'OBJ', 'OBL-INST', 'OBL-DUR', 'OBL-PERL']),
                    'np(part)' : set(['OBJ']),
                    'subj' : set(['SUBJ']),
                    }

special_tfw_to_attr = {
                       Special.sentp : set(['COMP']),
                       Special.infp : set(['XCOMP'])
                       }

def tfw_to_attr(node):
    tfw = node.fs[SkladnicaFs.tfw]
    if tfw in tfw_to_attr_dict:
        return tfw_to_attr_dict[tfw].copy()
    '''prepnp lub advp przerobione na prepnp'''
    if (tfw.startswith('prepnp')):
        return set(['OBL', 'OBL2', 'OBL3', 'OBL-AG']).union(get_prepnp_sem_obls(tfw))
    '''advp przysłówkowe'''
    if (tfw.startswith('advp')):
        return get_advp_sem_obls(tfw).copy()
    '''fzd z korelatem'''
    if (tfw.startswith('sentp(o,') or tfw.startswith('sentp(do,')):
        return set(['OBL'])
    for s in special_tfw_to_attr.keys():
        if (tfw.startswith(s)):
            '''to be handled later'''
            return set([s])
    if (tfw.startswith('prepadjp')):
        return set(['XCOMP-PRED'])
    print '***', tfw
    raise RuntimeError

'''
Returns a pair (pred, id).
id is the corresponding leaf's id
Returns None if there's no pred (interpunction).
'''
def find_pred(node):
    if (node.base != ''):
        if (node.tag == 'interp'):
            return None
        else:
            if node.base == u'ubiegły rok':
                return node.n_id, u'ubiegły_rok'
            if node.base == u'bieżący rok':
                return node.n_id, u'bieżący_rok'
            pred = node.base.replace("'", "\\'")#.upper()
            if node.tag in ('conj', 'comp'):
                for c_class, comps in comp_classes.items():
                    if pred in comps:
                        pred = c_class
            return node.n_id, pred.strip()#.encode('utf8')
    else:
        if (False and node.cat == SkladnicaCats.fzd):
            pass
        else:
            if node.rule == 'eps10':
                return node.n_id, u'na_pewno'
            if node.rule == 'eps11':
                return node.n_id, u'i_tak'
            if node.rule == 'eps12':
                return node.n_id, u'na_zewnątrz'
            if node.rule == 'eps13':
                return node.n_id, u'jak_zwykle'
            if node.rule == 'mp5':
                if (node.children[1].base == 'wysoko'):
                    return node.n_id, u'co_najwyżej'
                if (node.children[1].base == 'mało'):
                    return node.n_id, u'co_najmniej'
            if node.rule == 'mp6':
                return node.n_id, u'co_więcej'
            if node.rule == 'spoj25':
                return node.n_id, u'to_jednak'
            if node.rule == 'spoj34':
                return node.n_id, u'chociaż'
            if node.rule == 'spoj40':
                return node.n_id, u'podczas_gdy'
            if (len(node.headChildren) > 1):
                for index, rules in multiple_heads.items():
                    if node.rule in rules:
                        return find_pred(node.headChildren[index])
            for head in node.headChildren:
                p = find_pred(head)
                if p:
                    return p
        return None

def find_tag(node):
    if (node.base != ''):
        return node.tag
    else:
        for head in node.headChildren:
            p = find_pred(head)
            if p:
                return find_tag(head)
    return None

def fs_is_prep(val, fs, eqs):
    v = get_from_fs(val, fs, eqs)
    #print 'fs_is_prep:', v
    if (type(v) == AttributeStructure and 'CHECK' in v.attrs):
        check = get_from_fs(v.attrs['CHECK'], fs, eqs)#fs[v.attrs['CHECK']]
        if not '_CAT' in check.attrs:
            return False
        #print 'fs_is_prep - check:', check
        return (get_from_fs(check.attrs['_CAT'], fs, eqs)) == 'prep'
    return False

def find_fs_pred(val, fs, eqs):
    #print '    !!!! find_fs_pred - val:', val
    if (type(val) == int):
        try:
            val = fs[val]
        except KeyError:
            #print 'find_fs_pred - KeyError'
            return None
    if (type(val) == Semform):
        return val.sem
    elif (fs_is_prep(val, fs, eqs)):
        #print val.attrs['PRED'], val.attrs.keys()
        #print '    !!!! find_fs_pred - preposition'
        return find_fs_pred(val.attrs['OBJ'], fs, eqs)
    elif (type(val) == AttributeStructure and 'PRED' in val.attrs):
        #print 'pred in struct'
        pred = val.attrs['PRED']
        #print pred
        #TODO: test
        '''if type(pred) == int:
            pred = fs[pred].sem
        else:
            pred = pred.sem'''
        pred = get_from_fs(pred, fs, eqs).sem
        #print 'will return:', pred
        return pred
    return None

def find_fs_struct(val, fs, eqs):
    if (type(val) == AttributeStructure):
        return val
    elif (type(val) == int and type(get_from_fs(val, fs, eqs)) == AttributeStructure):
        return get_from_fs(val, fs, eqs)

'''returns the list of all predicates in this structure
possibly looking at set elements'''
def collect_preds(val, fs, eqs):
    '''prep's OBJ may be a set'''
    if fs_is_prep(val, fs, eqs):
        return collect_preds(get_from_fs(val, fs, eqs).attrs['OBJ'], fs, eqs)
    p = find_fs_pred(val, fs, eqs)
    if p:
        return [p]
    elif (type(val) == int and type(get_from_fs(val, fs, eqs)) == AttributeStructure):
        preds = []
        for e in get_from_fs(val, fs, eqs).set_elements:
            preds += collect_preds(e, fs, eqs)
        return preds
    return []

'''returns the list of all structures in this attribute
possibly looking at set elements'''
def collect_attr_structs(val, fs, eqs):
    #print 'collect_attr_structs:', val
    '''prep's OBJ may be a set'''
    if fs_is_prep(val, fs, eqs):
        return collect_attr_structs(get_from_fs(val, fs, eqs).attrs['OBJ'], fs, eqs)
    v = find_fs_struct(val, fs, eqs)
    #print v
    if find_fs_pred(v, fs, eqs):
        return [v]
    elif (type(v) == AttributeStructure):
        structs = []
        for e in v.set_elements:
            structs += collect_attr_structs(e, fs, eqs)
        return structs
    return []

'''returns the list of all structure vars in this attribute
possibly looking at set elements'''
def collect_struct_vars(val, fs, eqs):
    #print 'collect_attr_structs:', val
    '''prep's OBJ may be a set'''
    if fs_is_prep(val, fs, eqs):
        return collect_struct_vars(get_from_fs(val, fs, eqs).attrs['OBJ'], fs, eqs)
    if find_fs_pred(val, fs, eqs):
        return [val]
    v = get_from_fs(val, fs, eqs)
    if (type(v) == AttributeStructure):
        structs = []
        for e in v.set_elements:
            structs += collect_struct_vars(e, fs, eqs)
        return structs
    return []

'''returns a list of pairs: (attribute name, predicate)'''
def collect_attr_preds(struct, fs, eqs):
    #print 'collect_attr_preds for', struct
    attr_preds = []
    for attr, val in struct.attrs.items():
        #print attr
        if (attr == 'PRED'):
            continue
        else:
            #print '    collect_attr_preds:', attr, val
            attr_preds += [(attr, p) for p in collect_preds(val, fs, eqs)]
    return attr_preds

'''returns true if the node has its rection'''
def rekcja(node):
    if (node.cat == SkladnicaCats.zdanie):
        return True
    for child in node.children:
        if (child.cat in (SkladnicaCats.fw, SkladnicaCats.fl)):
            return True
    return False

def is_conjunction(node):
    spojnik = False
    cat_the_same = True
    if (node.rule in ('w5',)):
        return False
    for child in node.children:
        if (child.cat == SkladnicaCats.spojnik):
            spojnik = True
        elif (child.cat != node.cat):
            cat_the_same = False
    ret = spojnik and cat_the_same
    if ret:
        print 'FsFromSkladnica.is_conjunction: conjunction found'
        print node.cat, node.rule, node
        raise RuntimeError
    return spojnik and cat_the_same

def conjunction_children(node):
    ret = []
    for child in node.children:
        if (child.cat == node.cat):
            ret.append(child)
    return ret

'''modifies the collected constraints to handle special cases'''
def handle_special_cases(constrs):
    for predicate, constr_dict in constrs.items():
        '''sentp(...) may be either a SUBJ or a COMP if there's no SUBJ other than `pro`'''
        for special, attr_names in special_tfw_to_attr.items():
            special_constrs = []
            for n_id, constr in constr_dict.items():
                has_special = False
                #has_subj = False
                for c in constr.def_cs:
                    if special in c[0]:
                        has_special = True
                    #if c[0] == set(['SUBJ']) and c[1] != 'pro':
                    #    has_subj = True
                if (has_special):# and not has_subj):
                    special_constrs.append((n_id, constr))
            for n_id, constr in special_constrs:
                constr_copy = constr.copy()
                n_id_copy = str(n_id) + '-' + special
                for c in constr.def_cs:
                    if special in c[0]:
                        c[0].remove(special)
                        c[0].update(attr_names)
                for c in constr_copy.def_cs:
                    if special in c[0]:
                        c[0].remove(special)
                        c[0].add('SUBJ')
                '''if special is a SUBJ, no SUBJ `pro` is needed'''
                #constr_copy.def_cs.remove((set(['SUBJ']), 'pro'))
                constr_dict[n_id_copy] = constr_copy
        '''advp may be either an OBL or undef'''
        advp_constrs = []
        for n_id, constr in constr_dict.items():
            has_advp = False
            for c in constr.def_cs:
                if Special.advp in c[0]:
                    has_advp = True
            if (has_advp):
                advp_constrs.append((n_id, constr))
        for n_id, constr in advp_constrs:
            constr_copy = constr.copy()
            n_id_copy = str(n_id) + '-advp'
            for c in constr.def_cs:
                if Special.advp in c[0]:
                    c[0].remove(Special.advp)
                    c[0].add('OBL')
                    c[0].add('XCOMP-PRED')
            for c in constr_copy.def_cs:
                if Special.advp in c[0]:
                    c[0].remove(Special.advp)
                    '''attr pred goes to undef'''
                    constr_copy.undef_cs.append(c[1])
            '''remove attr pred from def'''
            constr_copy.def_cs = [c for c in constr_copy.def_cs if c[0] != set()]
            constr_dict[n_id_copy] = constr_copy
        '''handle optional attributes'''
        opt_constrs = []
        for n_id, constr in constr_dict.items():
            has_opt = False
            for pred in constr.undef_cs:
                if pred.endswith(OPT):
                    has_opt = True
            if (has_opt):
                opt_constrs.append((n_id, constr))
        for n_id, constr in opt_constrs:
            constr_copy = constr.copy()
            n_id_copy = str(n_id) + OPT
            constr.undef_cs  = [c.replace(OPT, '') for c in constr.undef_cs]
            constr_copy.undef_cs = [c for c in constr_copy.undef_cs if not c.endswith(OPT)]
            constr_dict[n_id_copy] = constr_copy
        '''remove unnecessary SUBJ pro's'''
        opt_subj_constrs = []
        for n_id, constr in constr_dict.items():
            subj_preds = set([p for a, p in constr.def_cs if 'SUBJ' in a])
            max_pro_count = 0
            if (subj_preds == set(['pro']) and not predicate in no_subj):
                max_pro_count = 1
            '''can't have more than max_pro_count SUBJ pro's'''
            while (constr.def_cs.count((set(['SUBJ']), 'pro')) > max_pro_count):
                constr.def_cs.remove((set(['SUBJ']), 'pro'))
            if (predicate in opt_subj and not set([p for a, p in constr.def_cs if 'SUBJ' in a])):
                opt_subj_constrs.append((n_id, constr))
        for n_id, constr in opt_subj_constrs:
            constr_copy = constr.copy()
            n_id_copy = str(n_id) + '-opt-subj'
            constr_copy.def_cs.append((set(['SUBJ']), 'pro'))
            constr_dict[n_id_copy] = constr_copy
        obj_pro_constrs = [(n_id, constr) for n_id, constr in constr_dict.items()
                if predicate in obj_pro and not set([p for a, p in constr.def_cs if 'OBJ' in a])]
        for n_id, constr in obj_pro_constrs:
            constr_copy = constr.copy()
            n_id_copy = str(n_id) + '-obj-pro'
            constr_copy.def_cs.append((set(['OBJ']), 'pro'))
            constr_dict[n_id_copy] = constr_copy
        obj_th_pro_constrs = [(n_id, constr) for n_id, constr in constr_dict.items()
                if predicate in obj_th_pro and not set([p for a, p in constr.def_cs if 'OBJ-TH' in a])]
        for n_id, constr in obj_th_pro_constrs:
            constr_copy = constr.copy()
            n_id_copy = str(n_id) + '-obj-th-pro'
            constr_copy.def_cs.append((set(['OBJ-TH']), 'pro'))
            constr_dict[n_id_copy] = constr_copy

'''
Returns a dictionary: { pred : constr_dict }.
constr_dict's keys are ids of leaves corresponding to the predicate
(there may be more than one such occurrence of a pred in the sentence).
constr_dict' values are SkladnicaConstrs objects for each occurrence of the predicate.

mod_preds - predicates that needed modification (e.g. appending 'SIĘ')
'''
def fs_constrs_from_skladnica(node, constrs=None, mod_preds=None):
    v = False
    if constrs is None:
        constrs = {}
        mod = {}
        fs_constrs_from_skladnica(node, constrs, mod)
        #for pred, constr_dict in constrs.items():
        #    for n_id, constr in constr_dict.items():
        #        pass
        handle_special_cases(constrs)
        return constrs
    else:
        if v:
            print node.n_id, node.cat, node.fs
        p = find_pred(node)
        if p:
            #print p
            n_id, pred = p
            if p in mod_preds:
                n_id, pred = mod_preds[p]
            if v:
                print '    pred:', n_id, pred
            def_constrs = []
            undef_constrs = []
            check_args = False
            if rekcja(node):#(node.cat == SkladnicaCats.zdanie):
                if v:
                    print 'rekcja'
                # rekcja
                check_args = True
                r = set()
                subj_pred = 'pro'
                for child in node.children:
                    cp = find_pred(child)
                    '''may be interpunction'''
                    if not cp:
                        continue
                    child_id, child_pred = cp
                    if (child.cat == SkladnicaCats.fw):
                        tf = child.fs[SkladnicaFs.tfw]
                        if (child_pred != 'się'):
                            if (is_conjunction(child.headChildren[0])):
                                for grandchild in conjunction_children(child.headChildren[0]):
                                    gcp = find_pred(grandchild)
                                    if not gcp:
                                        continue
                                    def_constrs.append((tfw_to_attr(child), gcp[1]))
                            else:
                                def_constrs.append((tfw_to_attr(child), child_pred))
                            r.add(tf)
                        if (child.fs[SkladnicaFs.tfw] == 'subj'):
                            subj_pred = child_pred
                            if (child_pred == 'się'):
                                subj_pred = 'pro'
                    if (child.cat == SkladnicaCats.fl):
                        if (not child_pred in czy_list) or (not child.fs[SkladnicaFs.dest] in ('pyt', 'pz')):
                            undef_constrs.append(child_pred)
                if (not u'subj' in r):
                    tag = find_tag(node)
                    '''this is better handled by no_subj.
                    'trudno' is a pred, but has subj!'''
                    #'''no subject in this case'''
                    #if (tag != 'pred'):
                    #    def_constrs.append((set([u'SUBJ']), 'pro'))
                    if (not tag.startswith('subst') and not tag.startswith('adj')):
                        def_constrs.append((set([u'SUBJ']), 'pro'))
                '''special case: infp(...)'''
                for child in node.children:
                    if (child.cat == SkladnicaCats.fw and
                        child.fs[SkladnicaFs.tfw].startswith('infp(')):
                        child_id, child_pred = find_pred(child)
                        if not child_pred in constrs:
                            constrs[child_pred] = {}
                        if not child_id in constrs[child_pred]:
                            constrs[child_pred][child_id] = SkladnicaConstrs()
                        constrs[child_pred][child_id].def_cs.append((set(['SUBJ']), 'pro'))#subj_pred))
                        constrs[child_pred][child_id].check_args = True
            '''look through all children, omit fl and fw
            if no rection, this is equivalent to the else version;
            otherwise, it will catch non-fl/fw children'''
            #else:
            if True:
                if v:
                    print 'bez rekcji'
                attr_children = []
                opt_children = []
                for child in node.children:
                    if (not child in node.headChildren and child.cat != 'partykuła'
                        and not child.cat in (SkladnicaCats.fl, SkladnicaCats.fw)):
                        if (is_conjunction(child)):
                            '''special case - take `grandchildren`'''
                            #print '*** conjunction:', child.cat
                            #print len(conjunction_children(child))
                            attr_children += conjunction_children(child)
                        #elif (child.cat == SkladnicaCats.fzd):
                        #    '''special case - fzd: zdanie is the attribute'''
                        #    for ch in child.children:
                        #        if (ch.cat == SkladnicaCats.zdanie):
                        #            attr_children.append(ch)
                        elif (node.cat == SkladnicaCats.fpm and
                              not child.cat in (SkladnicaCats.fpm, SkladnicaCats.fno)):
                            '''special case - modifier for a prep that has been removed
                            may modify the noun in OBL'''
                            opt_children.append(child)
                        else:
                            attr_children.append(child)
                for child in attr_children:
                    child_pred = find_pred(child)
                    if v:
                        print 'ch:', child_pred
                    if child_pred:
                        #print pred, ('?', child_pred)
                        undef_constrs.append(child_pred[1])
                for child in opt_children:
                    child_pred = find_pred(child)
                    #print 'ch:', child_pred
                    if child_pred:
                        #print pred, ('?', child_pred)
                        undef_constrs.append(child_pred[1] + OPT)
                '''special case - degree'''
                if (node.cat in (SkladnicaCats.fpt, SkladnicaCats.fps) and
                    SkladnicaFs.stopien in node.fs and
                    node.fs[SkladnicaFs.stopien] in ('wyz', 'naj') and pred != 'bardzo'):
                    undef_constrs.append(BARDZO)
                '''special case - fno -> flicz - numeral needs an OBJ pro'''
                if (node.cat == SkladnicaCats.fno and len(node.children) == 1 and
                    node.children[0].cat == SkladnicaCats.flicz):
                    undef_constrs.append('pro')
                if v:
                    print ' ==== ', attr_children
            if not pred in constrs:
                constrs[pred] = {}
            if v:
                print '    constrs[pred].keys():', constrs[pred].keys()
                print '    constrs[pred]', constrs[pred]
            if not n_id in constrs[pred]:
                if v:
                    print 'ADDING constrs[pred][n_id] for', pred, n_id
                constrs[pred][n_id] = SkladnicaConstrs()
            else:
                if v:
                    print '    -> already in constrs,',  constrs[pred][n_id]
            if (check_args):
                constrs[pred][n_id].check_args = True
            '''if found a SUBJ which used to be pro, remove pro'''
            subj_preds = set([p for n, p in def_constrs if n == set(['SUBJ'])])
            if (subj_preds and
                #not 'pro' in subj_preds and
                (set(['SUBJ']), 'pro') in constrs[pred][n_id].def_cs):
                constrs[pred][n_id].def_cs.remove((set(['SUBJ']), 'pro'))
            constrs[pred][n_id].def_cs += def_constrs
            '''dont't add BARDZO more than once'''
            if (BARDZO in constrs[pred][n_id].undef_cs and BARDZO in undef_constrs):
                undef_constrs.remove(BARDZO)
            constrs[pred][n_id].undef_cs += undef_constrs
            if v:
                print '      ', def_constrs, undef_constrs
                print pred, '***', constrs[pred][n_id]
            for child in node.children:
                if (child.cat != 'partykuła'):
                    if is_conjunction(child):
                        for c_child in conjunction_children(child):
                            fs_constrs_from_skladnica(c_child, constrs, mod_preds)
                    else:
                        fs_constrs_from_skladnica(child, constrs, mod_preds)

def check_with_skladnica_constrs(constrs, fs, eqs):
    # set of ids of already matched constrs sets. can't be used again.
    v = False
    matched = set([])
    checked = set([])
    for fs_id, struct in fs.items():
        if (eqs[fs_id].intersection(checked)):
            continue
        if (fs_is_prep(struct, fs)):
            continue
        checked.add(fs_id)
        fs_pred = u'%s' % find_fs_pred(struct, fs)
        if (type(struct) == AttributeStructure and fs_pred):
            if v:
                print '================= fs_pred:', fs_pred
            if (not fs_pred in constrs):
                #print '!!!', fs_pred, 'not in constrs - TODO !!!'
                continue
            attr_preds = collect_attr_preds(struct, fs)
            '''for attr, val in struct.attrs.items():
                #print attr
                if (attr == 'PRED'):
                    continue
                else:
                    if (type(val) == int and type(fs[val]) == AttributeStructure):
                        for e in fs[val].set_elements:
                            p = find_fs_pred(e, fs)
                            if p:
                                #print 'set element:', p
                                attr_preds.append((attr, p))
                    p = find_fs_pred(val, fs)
                    if p:
                        #print 'val pred:', p
                        attr_preds.append((attr, p))'''
            if v:
                print 'this pred_fs\'s attrs:', attr_preds
                print 'constrs for this fs_pred:', constrs[fs_pred]
            m = False
            for k, skladnica_cs in constrs[fs_pred].items():
                #print ' *** checking constr:', skladnica_cs
                if (k in matched):
                    continue
                #print skladnica_cs
                if (skladnica_cs.check_args):
                    ''''preds for attributes which are arguments must match the constraints'''
                    #print ' *** checking args'
                    attr_arg_preds = [ap for ap in attr_preds if ap[0] in arg_attrs]
                    #print ' *** arg attrs are:', attr_arg_preds
                    matched_arg_indices = []
                    for attr_set, pred in skladnica_cs.def_cs:
                        #print '     * checking for arg consistent with', attr_set, pred
                        found = False
                        for i in xrange(0, len(attr_arg_preds)):#attr, a_pred in attr_arg_preds:
                            attr, a_pred = attr_arg_preds[i]
                            #print '      -> comparing with', attr, a_pred
                            '''once something was matched, it can't be matched to other attr'''
                            if (i in matched_arg_indices):#((attr, a_pred)) in matched_arg_preds:
                                continue
                            if (a_pred == pred and attr in attr_set):
                                #print '      ---> match found', attr, a_pred
                                matched_arg_indices.append(i)#((attr, a_pred))
                                found = True
                                break
                        ''''no matching attribute found'''
                        if not found:
                            #print ' === no match found in arg attrs'
                            break
                    ''''not all arg attributes were matched - go to next constrs set'''
                    if len(matched_arg_indices) != len(attr_arg_preds):#matched_arg_preds != attr_arg_preds:
                        continue
                    '''don't check those in the next step'''
                    #attr_preds.difference_update(matched_arg_preds)
                    for attr in attr_arg_preds:
                        attr_preds.remove(attr) 
                '''now check whether attributes' preds are the same'''
                #print sorted(skladnica_cs.undef_cs), sorted([p for attr, p in attr_preds])
                if sorted(skladnica_cs.undef_cs) == sorted([p for attr, p in attr_preds]):
                    m = True
                    matched.add(k)
                    '''no need to look at other constraint sets for this fs_pred'''
                    break
            '''none of the constraint sets for this fs_pred was matched'''
            if not m:
                return False
    return True

'''some structures are not comparable, e.g. imiesłów'''
def compatible_with_skladnica(struct, fs, eqs_dict):
    if ('CHECK' in struct.attrs):
        check = get_from_fs(struct.attrs['CHECK'], fs, eqs_dict)
        #print check
        try:
            cat = get_from_fs(check.attrs['_CAT'], fs, eqs_dict)
        except KeyError:
            cat = '_'
        #print cat
        if cat in ('prep',):#('pact', 'ppas', 'pcon', 'pant', 'prep', 'inf'):
            #print '        ---->    IMIESŁÓW'
            return False
    else:
        '''bardzo'''
        p = get_from_fs(struct.attrs['PRED'], fs, eqs_dict)
        if (p and p.sem == 'bardzo'):
            return False
    return True

def attr_pred_lists(struct, fs, eqs_dict, used_vars=None):
    v = False
    if (used_vars is None):
        return attr_pred_lists(struct, fs, eqs_dict, set())
    else:
        ret = []
        if v:
            print '\nattr_pred_lists start', struct
        '''PREPOSITION'''
        if fs_is_prep(struct, fs, eqs_dict):
            if v:
                print '    -> PREP'
            return attr_pred_lists(get_from_fs(struct, fs, eqs_dict).attrs['OBJ'], fs, eqs_dict, used_vars)
        if (type(struct) == AttributeStructure and not struct.set_elements):
            fs_pred = find_fs_pred(struct, fs, eqs_dict)
            if (not fs_pred):
                return []
            for attr, value in struct.attrs.items():
                if attr == 'REFLEXIVE':
                    #print fs_pred, '***************REFLEXIVE'
                    fs_pred += u'_się'
                val = value
                if (type(val) == int):
                    '''may be a prep'''
                    if (fs_is_prep(val, fs, eqs_dict)):
                        val = get_from_fs(val, fs, eqs_dict).attrs['OBJ']
                    if v:
                        print '-> attr of', fs_pred, ':', attr, val
                    if (val in fs):
                        #used_vars.add(val)
                        #structs = collect_struct_vars(val, fs, eqs_dict)#collect_attr_structs(val, fs, eqs_dict)
                        vs = collect_struct_vars(val, fs, eqs_dict)
                        if v:
                            #print 'structs:', structs
                            print 'vs:', vs
                        #for s in structs:
                        #    ret += attr_pred_lists(s, fs, eqs_dict, used_vars)
                        for var in vs:
                            v_used = False
                            if v:
                                print '  EQ:', eqs_dict[val], used_vars
                            if (not var in eqs_dict):
                                eqs_dict[var] = set([var])
                            for eq_val in eqs_dict[var]:
                                if (eq_val in used_vars):
                                    v_used = True
                                    if v:
                                        print '  USED:', var, eqs_dict[val]
                            if (not v_used):
                                if (not var in fs):
                                    for eq_val in eqs_dict[var]:
                                        if (eq_val in fs):
                                            var = eq_val
                                            break
                                used_vars.add(var)
                                s = get_from_fs(var, fs, eqs_dict)
                                ret += attr_pred_lists(s, fs, eqs_dict, used_vars)
                    else:
                        print 'UNKNOWN VAR:', val
            if v:
                print 'getting attr_pred_lists for:', fs_pred
            if (compatible_with_skladnica(struct, fs, eqs_dict)):
                #print 'attr_pred_lists - COMPATIBLE:', struct
                ret.append((fs_pred, collect_attr_preds(struct, fs, eqs_dict)))
            if v:
                print 'ret is now:', ret
        elif type(struct) == AttributeStructure and struct.set_elements:
            for s in struct.set_elements:#collect_attr_structs(struct, fs):
                elem = get_from_fs(s, fs, eqs_dict)
                ret += attr_pred_lists(elem, fs, eqs_dict, used_vars)
                '''for val in struct.set_elements:
                    v_used = False
                    if (not val in eqs_dict):
                        eqs_dict[val] = set([val])
                    for eq_val in eqs_dict[val]:
                        if (eq_val in used_vars):
                            v_used = True
                    if (not v_used):
                        if (not val in fs):
                            for eq_val in eqs_dict[val]:
                                if (eq_val in fs):
                                    val = eq_val
                                    break
                        if (val in fs):
                            used_vars.add(val)
                            ret += attr_pred_lists(fs[val], fs, eqs_dict, used_vars)
                        else:
                            print 'UNKNOWN VAR:', val'''
        else:
            pass
            #print struct
            #print type(struct)
            #raise RuntimeError()
        return ret

def check_attrs_with_constr(a_preds, skladnica_cs):
    v = False
    # make a copy
    attr_preds = [x for x in a_preds]
    if (skladnica_cs.check_args):
        ''''preds for attributes which are arguments must match the constraints'''
        #print ' *** checking args', attr_preds
        attr_arg_preds = [ap for ap in attr_preds if ap[0] in arg_attrs]
        #print ' *** arg attrs are:', attr_arg_preds
        matched_arg_indices = []
        for attr_set, pred in skladnica_cs.def_cs:
            if v:
                print '     * checking for arg consistent with', attr_set, '"%s"' % pred
            found = False
            for i in xrange(0, len(attr_arg_preds)):#attr, a_pred in attr_arg_preds:
                attr, a_pred = attr_arg_preds[i]
                '''once something was matched, it can't be matched to other attr'''
                if (i in matched_arg_indices):#((attr, a_pred)) in matched_arg_preds:
                    continue
                if v:
                    print '      -> comparing with', attr, a_pred
                '''may be reflexive in LFG'''
                '''we may be expecting SUBJ pro, but find a predicate instead
                (cases not handled in Swigra)'''
                if ((a_pred in (pred, pred + SIE) or pred == 'pro') and attr in attr_set):
                    if v:
                        print '      ---> match found for', attr, pred, ':', a_pred
                    matched_arg_indices.append(i)#((attr, a_pred))
                    found = True
                    '''there may be more than one predicate instead of pro (coordination)'''
                    if (pred != 'pro'):
                        break
            ''''no matching attribute found'''
            if not found:
                if v:
                    print '        -> no match found in arg attrs'
                # there was a 'break' before. From old code?
                return False
        '''there may be an unexpected SUBJ'''
        if (not [attr_set for attr_set, pred in skladnica_cs.def_cs if 'SUBJ' in attr_set]):
            for i in xrange(0, len(attr_arg_preds)):
                if (not i in matched_arg_indices and attr_arg_preds[i][0] == 'SUBJ'):
                    matched_arg_indices.append(i)
        ''''not all arg attributes were matched - go to next constrs set'''
        if len(matched_arg_indices) != len(attr_arg_preds):#matched_arg_preds != attr_arg_preds:
            if v:
                print '      -', 'wrong lengths', matched_arg_indices, attr_arg_preds
            return False
        '''don't check those in the next step'''
        #attr_preds.difference_update(matched_arg_preds)
        for attr in attr_arg_preds:
            attr_preds.remove(attr) 
        '''now check whether attributes' preds are the same'''
    #print sorted(skladnica_cs.undef_cs), sorted([p for attr, p in attr_preds])
    #return sorted(skladnica_cs.undef_cs) == sorted([p for attr, p in attr_preds])
    #'''check for unexpected SUBJ'''
    #if v and [p for a, p in attr_preds if a == 'SUBJ']:
    #    print '      unexpected SUBJ found'
    #attr_preds = [(a, p) for a, p in attr_preds if a != 'SUBJ']
    if (len(skladnica_cs.undef_cs) != len(attr_preds)):
        if v:
            print '      wrong mod number'
        '''check for unexpected SUBJ'''
        unexpected_SUBJ = (len(attr_preds) - len(skladnica_cs.undef_cs)) == \
                          len([p for a, p in attr_preds if a == 'SUBJ'])
        if not unexpected_SUBJ:
            return False
        else:
            if v:
                print '      but unexpected SUBJ found'
    ps = [p for attr, p in attr_preds]
    '''must check for SIE'''
    for p in skladnica_cs.undef_cs:
        if not (p in ps or (p + SIE) in ps):
            return False
    return True

def check_with_skladnica_constrs_2(constrs, fs, eqs):
    v = True
    no_match = 0
    if v:
        print '========= check_with_skladnica_constrs_2\n\n'
    matched = set()
    pred_lists = attr_pred_lists(fs[0], fs, eqs)
    if v:
        print '\n\n'
    for pred, attr_list in pred_lists:
        p = u'%s' % pred
        if v:
            print '   check_with_skladnica_constrs_2: checking for:', p
            print '    -> attrs are:', attr_list
        if p in constrs:
            cs = constrs[p].items()
            '''first check constrs with predicate SUBJ, then others'''
            pred_subj_cs, other_cs = [], []
            for i, c in cs:
                s_p = set([p for a, p in c.def_cs if a == set(['SUBJ'])])
                if (s_p and s_p != set(['pro'])):
                    pred_subj_cs.append((i, c))
                else:
                    other_cs.append((i,c))
            cs = pred_subj_cs + other_cs
            match_found = False
            for i, c in cs:
                if i in matched:
                    continue
                if v:
                    print '     * ', i, c
                if (check_attrs_with_constr(attr_list, c)):
                    if v:
                        print '    MATCH'
                    match_found = True
                    matched.add(i)
                    '''stop looking - there may be identical constrs for other
                    occurrence of this pred, we want to use it then!'''
                    break
            if not match_found:
                no_match += 1
        else:
            '''a verb reflexive is Skladnica, but not in f-structure'''
            if p + '_się' in constrs:
                no_match += 1
    if v:
        print 'NO MATCH', no_match
    return no_match