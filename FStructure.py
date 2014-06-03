'''
Created on 14-01-2013

@author: Katarzyna Krasnowska
'''

from ParseConstraints import ConstraintType, FSPathAttr, FSPathSemform, FSPathVal, FSPathVar
from FSHelpers import get_from_fs, is_defined
from POLFIEInfo import attrs_order, no_tex_attrs, val_attrs, fs_attrs
#from FSFromSkladnica import get_from_fs
#from FSFromSkladnica import get_from_fs

class AttributeStructure(object):
    def __init__(self, var):
        self.var = var
        self.attrs = {}
        self.set_elements = set()#[]
    def __str__(self):
        return str(self.attrs) + ' ' + str(self.set_elements)
    def __repr__(self):
        return str(self)

class Semform(object):
    def __init__(self, sem, arg_list, arg_list_2):
        self.sem = sem
        self.arg_list = arg_list
        self.arg_list_2 = arg_list_2
    def __str__(self):
        return '\'%s\'' % self.sem.upper()
    def __repr__(self):
        return self.__str__()

class Atom(object):
    def __init__(self, val):
        self.val = val

#compare two sub-structures of fs
def fs_equal(fs1, fs2, fs, eqs):
    if (type (fs1) == int or type(fs2) == int):
        if (type (fs1) != int or type(fs2) != int):
            if (type(fs1) == int):
                fsi, fss = fs1, fs2
            else:
                fsi, fss = fs2, fs1
            return fs_equal(get_from_fs(fsi, fs, eqs), fss, fs, eqs)
    if type(fs1) != type(fs2):
        return False
    if (type(fs1) == int):
        return eqs[fs1] == eqs[fs2]
    if (type(fs1) == str):
        return fs1 == fs2
    if type(fs1) == Atom:
        return fs1.val == fs2.val
    #TODO arglists
    if type(fs1) == Semform:
        #print fs1.sem, fs1.arg_list, fs1.arg_list_2
        #print fs2.sem, fs2.arg_list, fs2.arg_list_2
        return ((fs1.sem == fs2.sem) and
                (fs1.arg_list == fs2.arg_list) and
                (fs1.arg_list_2 == fs2.arg_list_2))
    if type(fs1) == AttributeStructure:
        if (fs1.attrs.keys() != fs2.attrs.keys()):
            return False
        for a in fs1.attrs.keys():
            if (not fs_equal(fs1.attrs[a], fs2.attrs[a], fs, eqs)):
                #print '      a', a, fs1.attrs[a], fs2.attrs[a]
                return False
        e1, e2 = set(), set()
        for e in fs1.set_elements:
            e1.update(eqs[e])
        for e in fs2.set_elements:
            e2.update(eqs[e])
        if (e1 != e2):#(fs1.set_elements != fs2.set_elements):
            #print 'set'
            return False
        return True
    raise RuntimeError
        
# returns True if the constraint not an equality between vars
def apply_constraint_to_fs(constraint, fs, eqs):
    #if (constraint.type == ConstraintType.subsume):
    #        print 'SUBSUME', constraint
    if (constraint.type == ConstraintType.subsume):
        if (((type(constraint.arg1) == FSPathVar and type(constraint.arg2) == FSPathVar)) or
            ((type(constraint.arg1) != FSPathVar and type(constraint.arg2) != FSPathVar))):
            #print 'SUBSUME nope'
            return False
            #pass
    if (constraint.type in (ConstraintType.eq, ConstraintType.subsume)):
        #if (constraint.type == ConstraintType.subsume):
        #    print 'SUBSUME', constraint
        #print constraint.type, constraint.arg1, constraint.arg2
        path = constraint.arg1
        val = constraint.arg2
        #if (constraint.type == ConstraintType.subsume):
        #    print 'SUBSUME blabla'
        if (type(val) == FSPathVal):
            v = val.val
        elif (type(val) == FSPathVar):
            v = val.var
        elif (type(val) == FSPathSemform):
            #print val.sem, val.arg_list
            arg = []
            for a in val.arg_list:
                if (type(a) == FSPathVar):
                    arg.append(a.var)
                elif (type(a) == FSPathVal and a.val == 'NULL'):
                    arg.append(None)
                else:
                    print a
                    1 / 0
            arg_2 = []
            for a in val.arg_list_2:
                if (type(a) == FSPathVar):
                    arg_2.append(a.var)
                elif (type(a) == FSPathVal and a.val == 'NULL'):
                    arg_2.append(None)
                else:
                    print a
                    1 / 0
            v = Semform(val.sem, arg, arg_2)
        else:
            print 'apply_constraint_to_fs - can\'t handle val type:', type(val)
        #if (constraint.type == ConstraintType.subsume):
        #    print 'SUBSUME bleble'
        if (type(path) == FSPathAttr):
            #if (constraint.type == ConstraintType.subsume):
            #    print 'SUBSUME attr'
            if (not fs.has_key(path.fstr.var)):
                fs[path.fstr.var] = AttributeStructure(path.fstr.var)
            #print path, path.fstr.var
            #print 'fs:', fs[path.fstr.var]
            fs[path.fstr.var].attrs[path.attr] = v
        elif (type(path) == FSPathVar):
            #if (constraint.type == ConstraintType.subsume):
            #    print 'SUBSUME var'
            if (type(val) == FSPathVar):
                # remember that the vars are equal
                # TODO - what about subsumption?
                found = False
                for eq_set in eqs:
                    if (path.var in eq_set):
                        found = True
                        eq_set.add(v)
                    if (v in eq_set):
                        found = True
                        eq_set.add(path.var)
                if not found:
                    eqs.append(set([path.var, v]))
                #TODO: test this - apply all eqs later by unifying structures
                return False
                # may be both undefined yet
                if (v in fs):
                    if path.var in fs:
                        print fs[path.var]
                        print fs[v]
                        print
                    fs[path.var] = fs[v]
                # EXPERIMENT: else leave this constraint for later
                else:
                    return False
                #elif (path.var in fs):
                #    fs[v] = fs[path.var]
                #else:
                #    print 'FStructure.apply_constraint_to_fs', path.var, v
                #    # TODO
            else:
                #if (constraint.type == ConstraintType.subsume):
                #    print 'SUBSUME - apply', constraint
                fs[path.var] = v
        else:
            print 'apply_constraint_to_fs - can\'t handle path type:', type(val)
    if (constraint.type == ConstraintType.in_set):
        if (not fs.has_key(constraint.arg2.var)):
            fs[constraint.arg2.var] = AttributeStructure(constraint.arg2.var)
        #print '    **** apply_constraint_to_fs', type(constraint.arg1), constraint.arg1
        #print '    **** apply_constraint_to_fs', constraint
        if type(constraint.arg1) == FSPathVar:
            fs[constraint.arg2.var].set_elements.add(constraint.arg1.var)
        else:
            '''may be an immediate value'''
            fs[constraint.arg2.var].set_elements.add(constraint.arg1.val)
    #if 61 in fs:
    #    print 'apply_constraint_to_fs', constraint
    #    print '   ***', fs[61]
    return True

def apply_eqs_to_fs(fs, eqs_dict):
    done = set()
    for var, eq_vars in eqs_dict.items():
        if not var in done:
            done.update(eq_vars)
            if len(eq_vars) > 1:
                #print '    ', 'apply_eqs_to_fs', eq_vars
                structs = [fs[v] for v in eq_vars if v in fs and type(fs[v]) == AttributeStructure]
                if structs:
                    new_attrs = {}
                    new_set_elements = set()
                    for s in structs:
                        for attr, val in s.attrs.items():
                            if not attr in new_attrs:
                                '''no such attr found before - can add safely'''
                                new_attrs[attr] = val
                            elif type(new_attrs[attr]) == int:
                                '''can overwrite'''
                                if (type(val) == int and val < new_attrs[attr]) or (type(val) != int):
                                    new_attrs[attr] = val
                        #'''can safely overwrite'''
                        #if not new_set_elements:
                        #    new_set_elements = s.set_elements
                        '''workaround for the stupid _CAT problem in adj-adj'''
                        for e in s.set_elements:
                            if e in eqs_dict:
                                new_set_elements.add(sorted(eqs_dict[e])[0])
                            else:
                                new_set_elements.add(e)
                    for v in eq_vars:
                        if not v in fs:
                            fs[v] = AttributeStructure(v)
                        fs[v].attrs = new_attrs
                        fs[v].set_elements = new_set_elements
                else:
                    vals =  [fs[v] for v in eq_vars if v in fs]
                    if vals:
                        new_val = vals[0]
                        for val in vals[1:]:
                            if type(val) != int:
                                new_val = val
                            elif (type(new_val) == int and val < new_val):
                                new_val = val
                        for v in eq_vars:
                            fs[v] = new_val 

'''inner - a call from within this function in case a Semform
is a value in AttributeStructure's attrs'''
def apply_eq_to_fs(fs, v1, v2, inner=False):
    #print 'APPLY', v1, v2
    if v1 < v2:
        old_v, new_v = v2, v1
    else:
        old_v, new_v = v1, v2
    if not inner:
        '''one of the vars be not be in fs yet'''
        if not new_v in fs:
            fs[new_v] = fs[old_v]
        if not old_v in fs:
            fs[old_v] = fs[new_v]
    for struct in fs.values():
        if (type(struct) == Semform):
            #print '              ', struct
            for i in xrange(0, len(struct.arg_list)):
                if (struct.arg_list[i] == old_v):
                    struct.arg_list[i] = new_v
            for i in xrange(0, len(struct.arg_list_2)):
                if (struct.arg_list_2[i] == old_v):
                    struct.arg_list_2[i] = new_v
        if (type(struct) == AttributeStructure):
            if (struct.var == old_v):
                struct.var = new_v
            for a in struct.attrs.keys():
                if (struct.attrs[a] == old_v):
                    struct.attrs[a] = new_v
                if (type(struct.attrs[a]) == Semform):
                    '''an inner call'''
                    apply_eq_to_fs({-1 : struct.attrs[a]}, v1, v2, True)
            if old_v in struct.set_elements:
                struct.set_elements.remove(old_v)
                struct.set_elements.add(new_v)

def check_sets(fs, eqs):
    for v in fs.values():
        if (type(v) == AttributeStructure):
            if v.set_elements:
                set_elems = []
                for e in v.set_elements:
                    duplicate = False
                    for ee in set_elems:
                        if eqs[e] == eqs[ee]:
                            duplicate = True
                    if not duplicate:
                        set_elems.append(e)
                v.set_elements = set_elems

def print_fs(struct, fs, tab='', set=False):
    if (type(struct) == AttributeStructure):
        if set:
            s = '(in_set)'
        else:
            s = ''
        for attr, val in struct.attrs.items():
            if (type(val) == str):
                print tab + s, attr, val
            elif (type(val) == Semform):
                print tab + s, attr, val.sem
            else:
                print tab + s, attr, '[%d]' % val
                print_fs(fs[val], fs, tab + ' ')
        for val in struct.set_elements:
            print_fs(fs[val], fs, tab + ' ', True)

# return the lowest from equivalent vars
def lowest_eq(var, eqs_dict):
    return var
    if not var in eqs_dict:
        eqs_dict[var] = set([var])
    return sorted(eqs_dict[var])[0]

def var_box_str(var):
    return '{\color{Green}\\fbox{%s}}' % str(var)

def semform_to_str(semform, eqs_dict):
    #print 'LIST:', semform.arg_list
    arg = [var_box_str(lowest_eq(var, eqs_dict)) for var in semform.arg_list]
    arg_2 = [var_box_str(lowest_eq(var, eqs_dict)) for var in semform.arg_list_2]
    #print '***', arg
    if arg or arg_2:
        return'`%s<%s>%s\'' % (semform.sem, ','.join(arg), ','.join(arg_2))
    else:
        return'`%s\'' % semform.sem

# used_vars is for stopping in case of recursive f-structure
#eqs_dict - we always take the smallest var from the set of equal ones
def fs_to_tex(struct, fs, eqs_dict, tab=None, used_vars=set(), used_preds=set()):
    #print used_preds
    #print 'struct:', struct
    if (tab is None):
        return '\\begin{avm}\n' + fs_to_tex(struct, fs, eqs_dict, '', set(), set()) + '\\end{avm}\n'
    else:
        ret = ''
        if (type(struct) == AttributeStructure):
            # sort attrs
            sorted_attrs = []
            all_attrs = set(struct.attrs.keys())
            for a in attrs_order:
                if (a in all_attrs):
                    sorted_attrs.append(a)
                    all_attrs.remove(a)
            sorted_attrs += sorted(all_attrs)
            ret += tab + var_box_str(lowest_eq(struct.var, eqs_dict)) + '\\[\n'
            #ret += tab + var_box_str(str(eqs_dict[struct.var])) + '\\[\n'
            for attr in sorted_attrs:
                if attr in no_tex_attrs:
                    #pass
                    continue
                val = struct.attrs[attr]#, val in struct.attrs.items():
                if (type(val) == str):
                    ret += (tab + ' ' + attr + ' & ' + val)
                elif (type(val) == Semform):
                    sem_str = semform_to_str(val, eqs_dict)
                    ret += (tab + ' ' + attr + ' & ' + sem_str)
                    if (sem_str in used_preds):
                        pass
                        #print 'already used:', sem_str
                        #print used_preds
                        #1 / 0
                    if (sem_str != '\'PRO\''):
                        used_preds.add(sem_str)
                else:
                    ret += (tab + ' ' + attr + ' &\n')
                    v_used = False
                    if (not val in eqs_dict):
                        eqs_dict[val] = set([val])
                    for eq_val in eqs_dict[val]:
                        if (eq_val in used_vars):
                            ret += var_box_str(str(lowest_eq(eq_val, eqs_dict)) + '*')
                            v_used = True
                    #if (val in used_vars):
                    #    ret += '\\fbox{%d ***}' % val
                    if (not v_used):
                        # some other equal var may be used
                        if (not val in fs):
                            for eq_val in eqs_dict[val]:
                                if (eq_val in fs):
                                    val = eq_val
                                    break
                        if (val in fs):
                            #used = set([val]).union(used_vars)
                            used_vars.add(val)
                            ret += fs_to_tex(fs[val], fs, eqs_dict, tab + ' ', used_vars, used_preds)
                        else:
                            raise RuntimeError
                            print 'UNKNOWN VAR:', val
                            ret += var_box_str(lowest_eq(val, eqs_dict)) + '\\large{\\color{red}\\textbf{?}}'
                ret += ' \\\\\n'
            if struct.set_elements:
                ret += '\\{'
                elems = []
                for val in struct.set_elements:
                    v_used = False
                    if (not val in eqs_dict):
                        eqs_dict[val] = set([val])
                    for eq_val in eqs_dict[val]:
                        if (eq_val in used_vars):
                            elems.append(var_box_str(str(lowest_eq(eq_val, eqs_dict)) + '*'))
                            v_used = True
                    #if (val in used_vars):
                    #    ret += '\\fbox{%d ***}' % val
                    if (not v_used):
                        # some other equal var may be used
                        if (not val in fs):
                            for eq_val in eqs_dict[val]:
                                if (eq_val in fs):
                                    val = eq_val
                                    break
                        if (val in fs):
                            #used = set([val]).union(used_vars)
                            used_vars.add(val)
                            elems.append(fs_to_tex(fs[val], fs, eqs_dict, tab + ' ', used_vars, used_preds))
                        else:
                            raise RuntimeError
                            print 'UNKNOWN VAR:', val
                            elems.append(var_box_str(lowest_eq(val, eqs_dict)) + '\\large{\\color{red}\\textbf{?}}')
                ret += ' {\\color{red}\\large{,}} '.join(elems)
                ret += '\\}'
            ret += tab + '\\]\n'
        elif (type(struct) == Semform):
            sem_str = semform_to_str(struct, eqs_dict)
            ret += sem_str  #'`%s\'\n' % struct.sem
            if (sem_str in used_preds):
                pass
                #print 'already used:', sem_str
                #1 / 0
            if (sem_str != '\'PRO\''):
                used_preds.add(sem_str)
        elif (type(struct) == str):
            ret += (struct + '\n')
        else:
            print struct
            print type(struct)
            raise RuntimeError()
        return ret

def collect_fs_attrs(fs, eqs):
    fs_attrs = set()
    for f in fs.values():
        if (type(f) == AttributeStructure):
            fs_attrs.update(f.attrs.keys())
    return fs_attrs

def collect_attr_vals(fs, eqs):
    attr_vals = set()
    for f in fs.values():
        if (type(f) == AttributeStructure):
            for k, v in f.attrs.items():
                if k in val_attrs:
                    attr_vals.add((k, get_from_fs(v, fs, eqs)))
    return attr_vals
    
def collect_adj_attrs(fs, eqs):
    adj_attrs = set()
    for f in fs.values():
        if (type(f) == AttributeStructure):
            for k, v in f.attrs.items():
                if k in fs_attrs:
                    attr_f = get_from_fs(v, fs, eqs)
                    adj_attrs.update([(k, kk) for kk in attr_f.attrs.keys() if kk in fs_attrs])
    return adj_attrs

# returns a pair: f-stfucture and a dictionary of equal variables
def build_fs(constrs):
    fs = {}
    eqs = []
    c_count = 0
    applied = 0
    eq_constrs = []
    subsume = []
    for c in constrs:
        if (apply_constraint_to_fs(c, fs, eqs)):
            c_count += 1
            applied += 1
        else:
            eq_constrs.append(c)
            if (c.type == ConstraintType.subsume):
                subsume.append(c)
    eqs_dict = {}
    '''make sure eq sets are OK'''
    ''''for eq_set in eqs:
        print eq_set
        for var in eq_set:
            if (not var in eqs_dict):
                eqs_dict[var] = set()
            for eq_var in eq_set:
                eqs_dict[var].add(eq_var)'''
    overlap = [(i, j) for i in xrange(0, len(eqs))
                      for j in xrange(0, len(eqs))
                      if i != j and eqs[i].intersection(eqs[j])]
    while overlap:
        i, j = overlap[0]
        eqs[i].update(eqs[j])
        del eqs[j]
        overlap = [(i, j) for i in xrange(0, len(eqs))
                      for j in xrange(0, len(eqs))
                      if i != j and eqs[i].intersection(eqs[j])]
    for eq_set in eqs:
        for var in eq_set:
            eqs_dict[var] = eq_set
    for var in fs.keys():
        if (not var in eqs_dict):
            eqs_dict[var] = set([var])
    '''now apply eqs between vars'''
    apply_eqs_to_fs(fs, eqs_dict)
    #for k, v in fs.items():
    #    print k, v
    while True:
        #print '    ### subsumptions:', len(subsume)
        eq = None
        for c in subsume:
            #print '-----------', c
            #print eqs_dict
            #for k, v in fs.items():
            #    print k, ':', v
            #if (c.arg1.var in eqs_dict and c.arg2.var in eqs_dict):
            def1, def2 = is_defined(c.arg1.var, fs, eqs_dict), is_defined(c.arg2.var, fs, eqs_dict)
            if (def1 or def2):
                if (def1 and def2):
                    #print c.arg1, c.arg2
                    v1, v2 = get_from_fs(c.arg1.var, fs, eqs_dict), get_from_fs(c.arg2.var, fs, eqs_dict)
                    #print '\n', v1, '\n', v2, '\n'
                    if fs_equal(v1, v2, fs, eqs_dict):
                        subsume.remove(c)
                        eq = (c.arg1.var, c.arg2.var)
                        break
                else:
                    subsume.remove(c)
                    eq = (c.arg1.var, c.arg2.var)
                    break
        if not eq:
            break
        #print '       ===================        ', eq
        for var in eq:
            if not var in eqs_dict:
                eqs_dict[var] = set([var])
        eqs_dict[eq[0]].update(eqs_dict[eq[1]])
        for v in eqs_dict[eq[0]]:
            eqs_dict[v] = eqs_dict[eq[0]]
        #print eqs_dict
        #print 'apply'
        apply_eq_to_fs(fs, c.arg1.var, c.arg2.var)
    #for c in subsume:
        #print '======================', c
        #if (c.arg1.var in eqs_dict and c.arg2.var in eqs_dict):
        #    v1, v2 = get_from_fs(c.arg1.var, fs, eqs_dict), get_from_fs(c.arg2.var, fs, eqs_dict)
        #    if v1 != v2:
        #        print '                 **************', v1
        #        print '                               ', v2
    '''check for duplicates in set elements'''
    check_sets(fs, eqs_dict)
    return fs, eqs_dict