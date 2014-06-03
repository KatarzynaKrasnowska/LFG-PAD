'''
Created on 14-01-2013

@author: Katarzyna Krasnowska
'''

import re

from ParseChoices import parse_conditions

class ConstraintType:
    eq = 'eq'
    in_set = 'in_set'
    subsume = 'subsume'

class Constraint(object):
    def __init__(self, t, cond, arg1, arg2):
        self.type = t
        self.cond = set(cond)
        self.arg1 = arg1
        self.arg2 = arg2
    def __eq__(self, other):
        if type(other) != Constraint:
            return False
        return self.type == other.type and self.arg1 == other.arg1 and self.arg2 == other.arg2
    def __str__(self):
        return 'constraint: %s; cond: %s, arg1: %s, arg2: %s' % (self.type, self.cond, self.arg1, self.arg2)
    def __repr__(self):
        return '%s, arg1: %s, arg2: %s' % (self.type, self.arg1, self.arg2)
    def prolog(self):
        if len(self.cond) == 1:
            c = ''.join(self.cond)
        else:
            c = 'or(%s)' % ','.join(sorted(self.cond))
        return '\tcf(%s,%s(%s,%s))' % (c, self.type, self.arg1.prolog(), self.arg2.prolog())

class FSPathVar(object):
    def __init__(self, var):
        self.var = var
    def __str__(self):
        return 'v_%d' % self.var
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        if type(other) != FSPathVar:
            return False
        return self.var == other.var
    def prolog(self):
        return 'var(%d)' % self.var

class FSPathAttr(object):
    def __init__(self, fstr, attr):
        self.fstr = fstr
        self.attr = attr
    def __str__(self):
        return '%s.%s' % (self.fstr, self.attr)
    def __eq__(self, other):
        if type(other) != FSPathAttr:
            return False
        return self.fstr == other.fstr and self.attr == other.attr
    def prolog(self):
        return 'attr(%s,\'%s\')' % (self.fstr.prolog(), self.attr)

class FSPathVal(object):
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return 'val(%s)' % self.val
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        if type(other) != FSPathVal:
            return False
        return self.val == other.val
    def prolog(self):
        return '\'%s\'' % self.val

class FSPathSemform(object):
    def __init__(self, sem, i, arg_list, arg_list_2):
        self.sem = sem
        self.i = i 
        self.arg_list = arg_list
        self.arg_list_2 = arg_list_2
    def __str__(self):
        return 'sem(%s)' % self.sem
    def __eq__(self, other):
        if type(other) != FSPathSemform:
            return False
        return self.sem == other.sem and self.i == other.i and \
               self.arg_list == other.arg_list and self.arg_list_2 == other.arg_list_2
    def prolog(self):
        aa = [a.prolog() for a in self.arg_list]
        aa_2 = [a.prolog() for a in self.arg_list_2]
        return 'semform(\'%s\',%s,[%s],[%s])' % (self.sem, self.i, ','.join(aa), ','.join(aa_2))

def parse_fs_path(s):
    if (s.startswith('var')):
        i = s.find('(') + 1
        j = s.find(')')
        return FSPathVar(int(s[i:j])), s[(j + 1):]
    elif (s.startswith('attr')):
        fstr, rest = parse_fs_path(s[5:])
        i = rest.find('\'') + 1
        j = rest.find('\'', i)
        attr = rest[i:j]
        return FSPathAttr(fstr, attr), rest[(j + 2):] 
    elif (s.startswith('semform')):
        #semform('DO',5,[var(8)],[]))),
        sem, i, var_list, var_list_2, rest = re.match(r'semform\(\'(.+)\',(.+),\[(.*)\],\[(.*)\]\)(.*)', s).group(1,2,3,4,5)
        var_list = var_list.split(',')
        if (var_list != ['']):
            var_list = [parse_fs_path(v)[0] for v in var_list]
        else:
            var_list = []
        var_list_2 = var_list_2.split(',')
        if (var_list_2 != ['']):
            var_list_2 = [parse_fs_path(v)[0] for v in var_list_2]
        else:
            var_list_2 = []
        return FSPathSemform(sem, i, var_list, var_list_2), rest
    elif (s.startswith('\'')):
        i = 1
        j = (s.find('\'', i))
        return FSPathVal(s[i:j]), s[(j + 1):]
    else:
        print 'parse_fs_path - can\'t parse: *%s*' % s
    return '', s

def parse_constraint(s, equivalences):
    #print 'ParseConstraints.parse_constraint', s
    cond, constr_type, constr_args = re.match('\tcf\((.+),(eq|in_set|subsume)\((.+)\)', s).group(1,2,3)
    #print cond, constr_type, constr_args
    arg1, rest = parse_fs_path(constr_args)
    arg2, _ = parse_fs_path(rest[1:])
    conditions = parse_conditions(cond, equivalences)
    #if (len(conditions) == 1 and conditions[0] in equivalences):
    #    conditions = equivalences[conditions[0]]
    return Constraint(constr_type, conditions, arg1, arg2)

def parse_equivalence(s):
    alias, cond = re.match('\tdefine\((.+), (.+)\)', s).group(1,2)
    #print alias, cond
    cond = parse_conditions(cond, {})#tuple(parse_conditions(cond)[0])
    #print alias, cond
    return alias, cond