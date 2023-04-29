# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:24:07 2022

@author: Administrator

"""

import sys, os, collections
import lexer1
from lexer1 import get_word
sys.path.append(os.pardir)


sys.setrecursionlimit(4000)




class astNode():
    def __init__(self, _value = None, _type = None, _lineno = -1):
        self.nodeType = None # general astnode has no nodetype
        self.value = _value
        self.type = _type
        self.children = []
        self.lineno = _lineno
    def addchild(self,node):
        self.children.append(node)


class funcNode(astNode):
    def __init__(self, _value = None, _type = None,  _isconst = 0, _lineno = -1):
        super(funcNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'funcNode'
        self.isconst = _isconst
        self.isprotopyte = False #init funcprotopyte = False
        self.children = []
def test2():
    fnode = funcNode()
    print('fnodetest1111111111111111',fnode.isconst)

test2()