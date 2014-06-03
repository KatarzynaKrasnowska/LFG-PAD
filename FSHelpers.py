# -*- coding: utf-8 -*-
'''
Created on 30 wrz 2013

@author: kasia
'''

'''safe way to get value from fs'''
def get_from_fs(val, fs, eqs):
    if (type(val) == int):
        for v in sorted(eqs[val]):
            try:
                return fs[v]
            except:
                pass
        print val
        raise KeyError
    return val

'''safe way to get value from fs'''
def is_defined(val, fs, eqs):
    if not val in eqs:
        return False
    if (type(val) == int):
        for v in sorted(eqs[val]):
            if v in fs:
                return True
    return False