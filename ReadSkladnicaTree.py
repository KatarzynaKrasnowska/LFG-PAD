# -*- coding: utf-8 -*-
'''
Created on 14-05-2013

@author: Katarzyna Krasnowska
'''

import sys, os
from xml.sax import handler, make_parser

from SkladnicaInfo import *
#import SkladnicaInfo
from FSFromSkladnica import find_pred

features = set([SkladnicaFs.rekcja, SkladnicaFs.tfw, SkladnicaFs.stopien,
                SkladnicaFs.dest, SkladnicaFs.neg, SkladnicaFs.czas,
                SkladnicaFs.przypadek, SkladnicaFs.przyim])

coord_rules = set([
    # zdania rownorzednie
    SkladnicaRules.r1, SkladnicaRules.r2, SkladnicaRules.r3,
    # zdania szeregowo
    SkladnicaRules.s1, SkladnicaRules.s2, SkladnicaRules.s3,
    # fzd rownorzednie
    SkladnicaRules.zdr1, SkladnicaRules.zdr2,
    # fzd szeregowo
    SkladnicaRules.zdsz1, SkladnicaRules.zdsz2, SkladnicaRules.zdsz3,
    # fwe rownorzednie
    SkladnicaRules.wer1,
    # fwe szeregowo
    SkladnicaRules.wes3,
    # fno rownorzednie
    SkladnicaRules.nor1, SkladnicaRules.nor2, SkladnicaRules.nor3,
    # fno szeregowo
    SkladnicaRules.nos1, SkladnicaRules.nos2, SkladnicaRules.nos3,
    # fpm rownorzednie
    SkladnicaRules.pmr1, SkladnicaRules.pmr2, SkladnicaRules.pmr3,
    # fpm szeregowo
    SkladnicaRules.pms1, SkladnicaRules.pms2, SkladnicaRules.pmsz3,
    # fps szeregowo
    SkladnicaRules.pss3,
    # przyimki
    SkladnicaRules.pimr1, SkladnicaRules.pimr2, SkladnicaRules.pims3,
    SkladnicaRules.ptsz3,
    
    SkladnicaRules.n_pt2
    ])

class HelperNode:

    def __init__(self):
        self._id = None
        self._children = []
        self._headChildren = []
        self._cat = ''
        self._orth = ''
        self._base = ''
        self._tag = ''
        self._fs = {}
        self._rule = ''
        self._parent = None
    
    def __str__(self):
        return '(%s)' % str(self._children)

class SkladnicaNode:
    def __init__(self, n_id, cat, tag, base, fs, rule):
        self.n_id = n_id
        self.cat = cat
        self.tag = tag
        self.base = base
        self.fs = fs
        self.rule = rule
        self.headChildren = []
        self.children = []
        # for coordination manipulations
        self.coord_path = False
    def __str__(self):
        return self.to_str('')
    def to_str(self, tab):
        ret = '%s ID: %d %s `%s` %s' % (tab, self.n_id, self.cat, self.base, self.fs)
        if self.coord_path:
            ret += ' (C) '
        if self.headChildren:
            ret += ' H: %s' % [ch.n_id for ch in self.headChildren]
        ret += '\n'
        for child in self.children:
            ret += child.to_str(tab + '  ')
        return ret
    def to_tex(self, head=False, tab=None):
        if tab is None:
            return '\\branchheight{80pt}\\synttree\n' + self.to_tex(True, '').replace('_', '\\_')
        h = ''
        if head:
            h = '$\\ast$'
        tex = tab + '[ \\begin{tabular}{ c }' + h + '\\textbf{' + self.cat + '}\\textit{' + self.base + '} \\\\ '
        tex += '\\textit{' + self.rule + '} \\\\'
        for k, v in self.fs.items():
            tex += k + ':' + v.replace('[', '(').replace(']', ')') + ' \\\\ '
        tex += '\\end{tabular}\n'
        for child in self.children:
            hd = child in self.headChildren
            tex += child.to_tex(hd, tab + '  ')
        return tex + tab + ']\n'
    def copy(self):
        node_copy = SkladnicaNode(self.n_id, self.cat, self.tag, self.base, self.fs, self.rule)
        node_copy.coord_path = self.coord_path
        for child in self.children:
            child_copy = child.copy()
            node_copy.children.append(child_copy)
            if child in self.headChildren:
                node_copy.headChildren.append(child_copy)
        return node_copy
        
class TreeHandler(handler.ContentHandler):

    def __init__(self, out = sys.stdout):
        handler.ContentHandler.__init__(self)
        self._out = out
        self._nodes = {}
        self._currNode = HelperNode()
        self._chosen = False
        self._chosenChildren = False
        self._cat = False
        self._orth = False
        self._base = False
        self._tag = False
        self._f = False
        self._curr_f = False
        self.success = False
        self._firstSeen = {}
        self._currId = None

    def skladnicaTree(self, node=None, parent_fl=False, parent_cat=None):
        if node is None:
            tree = self.skladnicaTree(self._nodes[0])
            #print tree.to_tex()
            splitCoord(tree)
            give_ids(tree)
            #print tree.to_tex()
            return tree
        else:
            root = SkladnicaNode(node._id, node._cat, node._tag, node._base, node._fs, node._rule)
            for ch_id in node._children:
                child = self.skladnicaTree(self._nodes[ch_id],
                                           root.cat == SkladnicaCats.fl or
                                           parent_fl and root.rule in coord_rules,
                                           root.cat)
                if (not child.cat in (SkladnicaCats.posilk, SkladnicaCats.przec)):
                    root.children.append(child)
                    if (ch_id in node._headChildren):
                        root.headChildren.append(child)
            '''fix'''
            if (len(root.children) == 1 and not root.headChildren):
                root.headChildren.append(root.children[0])
            '''(must test) fw fzd's head is zdanie (if there is one - could be coordination)'''
            if (not (parent_fl or parent_cat in (SkladnicaCats.zdanie,))
                and root.cat == SkladnicaCats.fzd):
                #old_ch = root.children
                #root.headChildren = []
                #root.children = []
                #for child in old_ch:
                #    if (child.cat == SkladnicaCats.zdanie):
                #        root.children.append(child)
                #        root.headChildren.append(child)
                old_ch = root.children
                zdanie_ch = []
                for child in old_ch:
                    if (child.cat == SkladnicaCats.zdanie):
                        zdanie_ch.append(child)
                if zdanie_ch:    
                    root.headChildren = zdanie_ch
                    root.children = zdanie_ch
            '''advp realised by prepnp changed to prepnp(_,_)
            to comply with Walenty'''
            if (root.cat == SkladnicaCats.fw and root.fs[SkladnicaFs.tfw] == 'advp'
                    and root.children[0].cat == SkladnicaCats.fpm):
                #print root
                fpm_child = root.children[0]
                prep, case = fpm_child.fs[SkladnicaFs.przyim], fpm_child.fs[SkladnicaFs.przypadek], 
                root.fs[SkladnicaFs.tfw] = 'prepnp(%s,%s)' % (prep, case)
                print root.fs[SkladnicaFs.tfw]
            '''(must test) fw fpm's head is fno'''
            #if (parent_fw and root.cat == SkladnicaCats.fpm):
            #    old_ch = root.children
            #    root.headChildren = []
            #    root.children = []
            #    for child in old_ch:
            #        if (child.cat == SkladnicaCats.fno):
            #            root.children.append(child)
            #            root.headChildren.append(child)
            if (root.cat == SkladnicaCats.fpm):
                if (len(root.children) == 2):
                    
                    if ((root.children[0].cat == SkladnicaCats.przyimek or
                         root.children[0].cat == SkladnicaCats.modpart) and
                            root.children[1].cat == SkladnicaCats.fno):
                        '''fpm -> przyimek fno'''
                        root.children = [root.children[1]]
                        root.headChildren = root.children
                    elif (root.children[0].cat == SkladnicaCats.fno and
                            root.children[1].cat == SkladnicaCats.przyimek):
                        '''fpm -> fno przyimek'''
                        root.children = [root.children[0]]
                        root.headChildren = root.children
            '''fpmpt's head is fpt'''
            if (root.cat == SkladnicaCats.fpmpt):
                root.children = [root.children[1]]
                root.headChildren = root.children
            '''zdanie zl. podrzednie'''
            if (root.rule == SkladnicaRules.p1):
                spojnik = root.children[1]
                zdanie = root.children[2]
                #new_child = SkladnicaNode(0, 'podrz', node._tag, node._base, node._fs, '_')
                #new_child.children = [spojnik, zdanie]
                #new_child.headChildren = [spojnik]
                #root.children = [root.children[0], root.children[1], new_child]
                #root.headChildren = [root.children[0]]
                fl = SkladnicaNode(0, 'fl', '', '', {}, '_')
                podrz = SkladnicaNode(0, 'podrz', '', '', {}, '_')
                podrz.children = [spojnik, zdanie]
                podrz.headChildren = [spojnik]
                fl.children = [podrz]
                fl.headChildren = [podrz]
                #root.headChildren = root.children[0].headChildren
                #root.children = root.children[0].children + [fl]
                root.headChildren = [root.children[0]]
                root.children = [root.children[0], fl]
            '''formarzecz - apozycja'''
            if (root.rule == SkladnicaRules.n_rz5):
                root.headChildren = [root.children[0]]
            '''n_cz11'''
            if (root.rule == SkladnicaRules.n_cz11):
                root.headChildren = root.children
            #'''wypowiedzenie'''
            #if (root.cat == SkladnicaCats.wypowiedzenie):
            #    root.children = [child for child in root.children if child.cat == SkladnicaCats.zdanie]
            #    root.headChildren = root.children
            '''przyszły złożony (będzie je finansować)'''
            if (root.cat == SkladnicaCats.zdanie):
                ffs = [child for child in root.children if child.cat == SkladnicaCats.ff]
                if ffs:
                    ff = ffs[0]
                    _, pred = find_pred(ff)
                    if (pred == u'być' and ff.fs[SkladnicaFs.rekcja].find('infp(nd)') != -1):
                        infp_fw = [child for child in root.children
                                   if SkladnicaFs.tfw in child.fs and child.fs[SkladnicaFs.tfw] == 'infp(nd)']
                        if infp_fw:
                            infp_child = infp_fw[0]
                            if (infp_child.fs['czas'] == 'przy'):
                                root.children.remove(ff)
                                root.children.remove(infp_child)
                                root.children += infp_child.children[0].children
                                root.headChildren = infp_child.children[0].headChildren
                                infp_child.children[0].headChildren[0].cat = SkladnicaCats.ff
                                #for child in root.children:
                                #    if (SkladnicaFs.tfw in child.fs and child.fs[SkladnicaFs.tfw] == 'infp(nd)'):
                                #        root.children.remove(child)
                                #        root.children += child.children[0].children
                                #        root.headChildren = child.children[0].headChildren
                                #        child.children[0].headChildren[0].cat = SkladnicaCats.ff
            '''korelat'''
            #TODO: kor2 i kor3 (nie wystepuja w Skladnicy - na razie...)
            if (root.rule == 'zdk1'):
                '''korelat is head'''
                root.headChildren = [root.children[0]]
            if (root.rule == 'kor1'):
                '''to is head'''
                root.children = [root.children[1]]
                root.headChildren = root.children
            '''6.30'''
            if (root.rule == 'n_pt6' and len(root.children) == 3):
                root.headChildren = root.children[:2]
                flicz = SkladnicaNode(0, 'flicz', '', '', {}, '_')
                flicz.children = flicz.headChildren = [root.children[2]]
                fno = SkladnicaNode(0, 'fno', '', '', {}, '_')
                fno.children = fno.headChildren = [flicz]
                root.children[2] = fno
                print root
            '''biało-czerwony'''
            if (root.rule == 'n_pt2'):
                fpm = SkladnicaNode(0, 'formaprzym', '', '', {}, '_')
                fpm.children = fpm.headChildren = root.children[:1]
                root.children = [fpm] + root.children[1:]
                root.headChildren = root.children[1]
            '''sie'''
            #ffs = [child for child in root.children if child.cat == SkladnicaCats.ff]
            #if ffs:
            #    ff = ffs[0]
            sie_fw = [child for child in root.children
                      if SkladnicaFs.tfw in child.fs and child.fs[SkladnicaFs.tfw] == 'sie']
            if sie_fw:
                sie_child = sie_fw[0]
                root.children.remove(sie_child)
                find_head_leaf(root).base += '_się'
            if not root.children and root.cat:
                root.cat = ''
            return root
    
    def startElement(self, name, attrs):
        if (name == 'base-answer' and attrs['type'] == 'FULL'):
            self.success = True
        elif (name == 'node'):
            self._currId = int(attrs['nid'])
            if (attrs['chosen'] == 'true'):
                self._chosen = True
                self._nodes[int(attrs['nid'])] = self._currNode
                self._currNode._id = int(attrs['nid'])
        elif (name == 'children'):
            self._chosenChildren = attrs.has_key('chosen')
            if (self._chosenChildren):
                self._currNode._rule = attrs['rule']
        elif (name == 'child' and self._chosenChildren):
            self._currNode._children.append(int(attrs['nid']))
            if (attrs['head'] == 'true'):
                self._currNode._headChildren.append(int(attrs['nid']))
        elif (name == 'f' and attrs['type'] in features):
            self._f = True
            self._curr_f = attrs['type']
        else:
            self._cat = (name == 'category')
            self._orth = (name == 'orth')
            self._base = (name == 'base')
            self._tag = (name == 'f' and attrs['type'] == 'tag')

    def endElement(self, name):
        if (name == 'node'):
            if (self._chosen) or True:
                self._currNode = HelperNode()
            self._chosen = False
            self._chosenChildren = False
        #if (name == 'category'):
        #    self._cat = False
        self._f = False
        self._cat = False
        self._orth = False
        self._base = False
        self._tag = False

    def characters(self, content):
        if (self._cat and content.strip()):
            self._currNode._cat += content
        if (self._orth and content.strip()):
            if (content.strip() not in self._firstSeen):
                self._firstSeen[content.strip()] = self._currId
        if (self._orth and self._chosen and content.strip()):
            self._currNode._orth += content
        if (self._base and self._chosen and content.strip()):
            self._currNode._base += content
        if (self._tag and self._chosen and content.strip()):
            self._currNode._tag += content
        if (self._f and self._chosen and content.strip()):
            if not self._curr_f in self._currNode._fs:
                self._currNode._fs[self._curr_f] = ''
            self._currNode._fs[self._curr_f] += content

def splitCoord(tree):
    print 'splitCoord'
    begin, end = findCoordPath(tree)
    while (end):
        print 'COORD PATH FOUND'
        print 'BEGINNING IN', begin.cat, begin.n_id, '- ENDING IN', end.cat, end.n_id
        #print tree
        conjuncts = []
        for child in end.children:
            if (child.cat == end.cat):
                conjuncts.append(child)
        print 'FOUND', len(conjuncts), 'CONJUNCTS'
        end.children = []
        begin_parent = findParent(begin, tree)
        if begin in begin_parent.headChildren:
            print 'splitCoord - begin in begin_parent.headChildren', begin_parent.cat, '->', begin.cat,
            #raise RuntimeError
        pre, post = [], []
        curr = pre
        for child in begin_parent.children:
            if (child == begin):
                curr = post
            else:
                curr.append(child)
        begin_parent.children = pre
        for conjunct in conjuncts:
            split = begin.copy()
            split_end = findCoordPathEnd(split)
            #TODO test this
            split_end.rule = '_coord'
            split_end.children = [conjunct]
            split_end.headChildren = [conjunct]
            begin_parent.children.append(split)
        begin_parent.children += post
        '''add a dummy head child if needed'''
        if (not begin_parent.headChildren[0] in begin_parent.children):
            dummy = SkladnicaNode(0, 'coord_head', '', 'coord_head', {}, '_')
            begin_parent.headChildren = [dummy]
        clearCoordMarking(tree)
        begin, end = findCoordPath(tree)
        #print tree.to_tex()
        
'''marks a path to coordination node that should be split'''
'''returns begin, end: the first and last node on the path'''
def findCoordPath(node):
    #print node.cat, 'r:', node.rule, node.rule in coord_rules
    #print node.children
    if (node.rule in coord_rules):
        print '          findCoordPath', node.rule
        node.coord_path = True
        return node, node
    for child in node.children:
        begin, end = findCoordPath(child)
        if end:
            '''extend path to node if necessary'''
            '''child.cat == node.cat: eg. fno -> fpt fno* where fno* contains coordination'''
            '''len(node.children == 1) - no other branches from node: eg. fl -> fpt'''
            if (((child.cat == node.cat and child in node.headChildren) or
                 len(node.children) == 1)
                and child.coord_path):
                print '          findCoordPath - will mark', node.cat
                print '            ->', (child.cat == node.cat), len(node.children) == 1 
                node.coord_path = True
                begin = node
            return begin, end
    return None, None

'''assuming node is on marked coord path!'''
def findCoordPathEnd(node):
    for child in node.children:
        if child.coord_path:
            return findCoordPathEnd(child)
    return node

def clearCoordMarking(node):
    node.coord_path = False
    for child in node.children:
        clearCoordMarking(child)

def findParent(child_node, node):
    if (child_node in node.children):
        return node
    for child in node.children:
        p = findParent(child_node, child)
        if p:
            return p
    return None

def has_pyza(node):
    if (SkladnicaFs.tfw in node.fs and node.fs[SkladnicaFs.tfw] == 'sentp(pz)'):
        return True
    for child in node.children:
        if has_pyza(child):
            return True
    return False

def has_on_prep(node):
    if (node.rule == 'pm1'):
        return node.children[0].children[0].children[0].tag.startswith('ppron')
    for child in node.children:
        if has_on_prep(child):
            return True
    return False

'''give unique ids to nodes (ids get messed up e.g. in coordination split)'''
def give_ids(node, i=None):
    if i is None:
        return give_ids(node, 1)
    else:
        node.n_id = i
        for child in node.children:
            i = give_ids(child, i)
        return i + 1

def find_head_leaf(node):
    if node.headChildren:
        return find_head_leaf(node.headChildren[0])
    return node