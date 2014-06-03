# -*- coding: utf-8 -*-
'''
Created on 10-02-2014

@author: Katarzyna Krasnowska
'''

class SkladnicaConstrs:
    def __init__(self):
        '''Constraints with defined attribute name.
        list of pairs (set(attr_name), pred)'''
        self.def_cs = []
        '''Constraints with no defined attribute name.
        list of preds'''
        self.undef_cs = []
        '''tells whether arguments must be checked'''
        self.check_args = False
    def __str__(self):
        ret = ''
        if self.check_args:
            ret += '  ARGUMENTY: '
            if self.def_cs:
                ret += (', '. join ('/'.join(arg_names) + ' - ' + arg for arg_names, arg in self.def_cs))
            else:
                ret += '-'
            #for arg_names, arg in self.def_cs:
            #    ret += '/'.join(arg_names) + ' - ' + arg + '  '
            ret += ' || MODYFIKATORY: '
            if self.undef_cs:
                ret += ', '.join(self.undef_cs)
            else:
                ret += '-'
        else:
            ret += '  ATRYBUTY: '
            if self.undef_cs:
                ret += ', '.join(self.undef_cs)
            else:
                ret += '-'
        return ret
    def __repr__(self):
        return str(self)
    def copy(self):
        c = SkladnicaConstrs()
        for dc in self.def_cs:
            c.def_cs.append((dc[0].copy(), dc[1]))
        c.undef_cs.extend(self.undef_cs)
        c.check_args = self.check_args
        return c