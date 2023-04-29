# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:24:07 2022

@author: Administrator

"""


import sys, os, collections

#from psutil import cpu_count
import lexer2
from lexer2 import get_word
sys.path.append(os.pardir)


sys.setrecursionlimit(100)
# null is ε
#grammer
#ambicious grammer
grammars = {
    'program':[['vardec','program'], ['funcprototype','program'], ['funcdef','program'],['structdef','program'],['null']],
    'vardec':[['const','typename','idents',';'],['typename','const','idents',';'],['typename','idents',';']],
    #'vardecs':[['vardec'],['vardec','vardecs']],
    'idents':[['id'],['id','[','int_val',']'], ['id','[','int_val',']',',','idents'],['id',',','idents']],
    'typename':[['void'], ['char'], ['int'], ['float']],
    'funcprototype':[['funcdec',';']],
    'funcdec':[['typename','id','(',')'],['typename','id','(','params',')']],
    'param':[['typename','id'], ['typename','id','[',']']],
    'params':[['param',',','params'], ['param']],
    #'funcdef':[['funcdec','{','}'], ['funcdec','{','vardecs','stmts','}'], ['funcdec','{','vardecs','}'], ['funcdec','{','stmts','}']],
    'funcbody':[['{','}'], ['{','vardecs','stmts','}'], ['{','vardecs','}'], ['{','stmts','}']],
    'structdef':[['struct','id','{','}',';'],['struct','id','{','vardecs','}',';'],['struct','id','id','{','vardecs','}',';'],['struct','id','id','{','}',';']],
    'stmt':[[';'], ['expr',';'], ['break',';'], ['continue',';'], ['return',';'], ['return','expr',';'], ['ifstmt'],['forstmt'],['whilestmt'],['dowhilestmt']],
    'stmts':[['stmt','stmts'], ['stmt']],
    'stmtblock':[['{','}'], ['{','stmts','}']],
    'ifstmt':[['if','(','expr',')','stmt'], ['if','(','expr',')','stmtblock'], ['if','(','expr',')','stmt','else','stmt'],\
              ['if','(','expr',')','stmt','else','stmtblock'], ['if','(','expr',')','stmtblock','else','stmt'], ['if','(','expr',')','stmtblock','else','stmtblock']],
    'forstmt':[['for','(','optexpr',';','optexpr',';','optexpr',')','stmtblock'], ['for','(','optexpr',';','optexpr',';','optexpr',')','stmt']],
    'whilestmt':[['while','(','expr',')','stmtblock'],['while','(','expr',')','stmt']],
    'dowhile':[['do','stmt','while','(','expr',')',';'], ['do','stmtblock','while','(','expr',')',';']],
    'optexpr':[['null'], ['expr']],
    'expr': [['constval'],['id','(','exprlst',')'], ['lval'], ['lval','assignoperator','expr'], ['++','lval'], ['lval','++'], ['--','lval'], ['lval','--'], \
             ['uoperator','expr'], ['expr','bioperator','expr'], ['expr','?','expr',':','expr'],['(','typename',')','expr'], ['(','expr',')']],
    'constval':[['char_lit'],['int_lit'],['real_lit'],['str_lit']],
    'exprlst':[['expr'], ['expr',',','exprlst']],
    'assignoperator':[['='], ['+='], ['-='], ['*='], ['/=']],
    'uoperator':[['-'], ['!'], ['~']],
    'bioperator':[['=='],['!='],['>'],['>='],['<'],['<='],['+'],['-'],['*'],['/'],['%'],['|'],['&'],['||'],['&&']],
    'lval':[['id'], ['id','(','expr',')'], ['lval','.','id'], ['lval','.','id','(','expr',')']]
    }


#program:
#null is not terminal
terminals =  [
    '!','%','&','(',')','*','+',',','-','.','/', ':', ';','<','=','>','?','[',']','{','}', '|','==','!=',
    '>=','<=','++','--','||','&&','+=','-=','*=','/=','const', 'struct','for','while','do','if','else',
    'break','continue','return','switch','case','default','type', 'void','char','int','float','char_lit','int_lit','real_lit','str_lit','id'
]
nonterminals = ['program', 'vardec', 'funcprototype','funcdec','funcdef','structdef','typename','idents','vardecs',
                'params','param','stmts','stmt','stmtblock','ifstmt','forstmt','whilestmt','dowhile','expr',
                'optexpr','exprlst','assignoperator','uoperator','bioperator','lval','constval'
    ]

class parser():
    def __init__(self, filename = 'test.c'):
        self.tokenlst = []
        self.filename = filename    
    
    
    def getToken(self):
        get_word(self.filename, self.tokenlst)
        return self.tokenlst
    def getFileName(self):
        return self.filename
    
    #def parse_file():




#tokenlst  = []
#fname = 'test4_part4.c'
#fname = 'extra4_part4.c'
fname = sys.argv[2]#
#lexer1.get_word(fname,tokenlst)
tokenlst = parser(filename = fname).getToken()
#fname = parser(filename = 'test1_part4.c').getFileName()
#tokenlst = parser(filename = 'test.c').getToken()
#print(tokenlst)
index = 0
#'program':[['vardec','program'], ['funcprototype','program'], ['funcdef','program'],['structdef','program'],['null']],


def test():
    i = 10 
    for j in range(len(tokenlst)):
        if tokenlst[j].value == 'return':
            return tokenlst
        else:
            print(tokenlst[j].value)
    return False



class astNode():
    def __init__(self, _value = None, _type = None, _lineno = -1):
        self.nodeType = 'rootNode' # general astnode has no nodetype
        self.value = _value
        self.type = _type
        self.children = []
        self.lineno = _lineno
    def addchild(self,node):
        self.children.append(node)
'''
testnode = astNode()
testnode.lineno = 100
print(testnode.lineno)
'''
class structNode(astNode):
    def __init__(self, _value = None, _type = None, _isconst = 0, _lineno = -1,  _fathername = None, _isglobal = 0, _ancester = None):
        super(structNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'structNode'
        self.isconst = _isconst
        self.children = []
        self.member = {}
        self.ancester = _ancester
        self.isglobal = _isglobal


class funcNode(astNode):
    def __init__(self, _value = None, _type = None,  _isconst = 0, _lineno = -1):
        super(funcNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'funcNode'
        self.isconst = _isconst
        self.isprototype = 0 #init funcprotopyte = False
        self.children = []

class funcbodyNode(astNode):
    def __init__(self, _value = None, _type = None,  _isconst = 0, _lineno = -1):
        super(funcbodyNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'funcbodyNode'
        self.isconst = _isconst  # affect return 
        self.isprotopyte = False #init funcprotopyte = False
        self.children = [] #parameter, vardec is local

#could be in structdef or funcdef
class vardecNode(astNode):
    def __init__(self, _value = None, _type = None,  _isconst = 0, _lineno = -1, _isglobal = 0, _ancester = None):
        super(vardecNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'vardecNode'
        self.isconst = _isconst
        self.isglobal = _isglobal
        self.children = []
        self.ancester = _ancester

class identNode(astNode):
    def __init__(self, _value = None, _type = None,  _isconst = 0, _lineno = -1, _islist = -1, _isglobal = 0, _initvalue = None, _ancester = None):
        super(identNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'identNode'
        self.isconst = _isconst
        self.isglobal = _isglobal
        self.listsize = _islist # id []
        self.initvalue = _initvalue
        self.children = []
        self.ancester = _ancester
    def setvalue(self, value):
        self.initvalue = value


class identsNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None):
        super(identsNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'identsNode'
        self.children = []
        self.ancester = _ancester

class stmtNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None):
        super(stmtNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'stmtNode'
        self.children = []
        self.ancester = _ancester
'''     
class stmtNode():
    def __init__(self, _value = None, _type = None, _lineno = -1):
        self.nodeType = 'stmtNode' # general astnode has no nodetype
        self.value = _value
        self.type = _type
        self.children = []
        self.lineno = _lineno
    def addchild(self,node):
        self.children.append(node)
'''

class stmtsNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None):
        super(stmtsNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'stmtsNode'
        self.children = []
        self.ancester = _ancester
class stmtblockNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None):
        super(stmtblockNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'stmtblockNode'
        self.children = []
        self.ancester = _ancester

class expr1Node(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None, _isconst = 0):
        super(expr1Node, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'expr1Node'
        #self.isfunc = _isfunc
        #self.isstruct = _isstruct
        self.children = []
        self.ancester = _ancester
        self.isconst = _isconst

class expr2Node(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None, _isconst = 0):
        super(expr2Node, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'expr2Node'
        self.children = []
        self.ancester = _ancester
        self.isconst = _isconst

class exprNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None, _isconst = 0):
        super(exprNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'exprNode'
        self.children = []
        self.ancester = _ancester
        self.isconst = _isconst

class exprlstNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None, _isconst = 0):
        super(exprlstNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'exprlstNode'
        self.children = []
        self.ancester = _ancester
        self.isconst = _isconst

class lvalNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None, _isconst = 0):
        super(lvalNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'lvalNode'
        self.children = []
        self.ancester = _ancester
        self.isconst = _isconst

class paramNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _islist = 0, _isdefined = 0, _isconst = 0, _ancester = None):
        super(paramNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'expr1Node'
        self.islist = _islist
        self.isdefined = _isdefined
        self.isconst = _isconst
        self.children = []
        self.ancester = _ancester
class paramsNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None):
        super(paramsNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'paramsNode'
        self.children = []
        self.ancester = _ancester

class ifstmtNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None):
        super(ifstmtNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'ifstmtNode'
        self.children = []
        self.ancester = _ancester

class forstmtNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None):
        super(forstmtNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'forstmtNode'
        self.children = []
        self.ancester = _ancester
class whilestmtNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None):
        super(whilestmtNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'whilestmtNode'
        self.children = []
        self.ancester = _ancester
class dowhilestmtNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1, _ancester = None):
        super(dowhilestmtNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'dowhilestmtNode'
        self.children = []
        self.ancester = _ancester
class assignoperatorNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1):
        super(assignoperatorNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'assignoperatorNode'
        self.children = []

class uoperatorNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1):
        super(uoperatorNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'uoperatorNode'
        self.children = []
class bioperatorNode(astNode):
    def __init__(self, _value = None, _type = None,  _lineno = -1):
        super(bioperatorNode, self).__init__(_value = None, _type = None, _lineno = -1)
        self.nodeType = 'bioperatorNode'
        self.children = []


nodelst = [] #save all the nonterminal node in this nodelst. when get a nonterminal node, save to this lst at once
root = astNode()
root.lineno = tokenlst[0].lineno # root lineno

globalStructs = {} #{structname:{member name:member type}}
globalVars = {} #varname:[type,islist,] or not if is not, -1, else give the size of list
funcs = {} #func name: [type, isfuncprotopyte, [params name, params num], params type]]
error_log = [] #store error msg

def parse_program():
    global index
    global tokenlst
    global root
    global nodelst
    global globalStructs
    global globalVars
    global funcs

    #programNode = astNode()
    #root.addchild(programNode)
    #empty file
    if len(tokenlst) == 0:
        print('empty file, syntax correct')
        return root
    #LL(K) check, NO UPDATE index
    

    if index >= len(tokenlst):
        print('syntax correct')
        return root
    else:
        #'vardec':[['const','typename','idents',';'],['typename','const','idents',';'],['typename','idents',';']],
        #'vardecs':[['vardec'],['vardec','vardecs']],
        #'funcprototype':[['funcdec',';']],
        #'funcdec':[['typename','id','(',')'],['typename','id','(','params',')']],
        #'funcdef':[['funcdec','{','}'], ['funcdec','{','vardecs','stmts','}'], ['funcdec','{','vardecs','}'], ['funcdec','{','stmts','}']],
        #'structdef':[['struct','id','{','}',';'],['struct','id','{','vardecs','}',';'],['struct','id','id','{','vardecs','}',';'],['struct','id','id','{','}',';']],
        #print(index)
        while index < len(tokenlst):
            #print('index is ', index, ' length of code is ', len(tokenlst) )
            #print('tokenvalue is ', tokenlst[index].value, ' line is ', tokenlst[index].lineno)
            #funcdec
            if parse_funcdec():
                #add child node 
                #programNode.addchild(nodelst[-1])
                #params num and type
                fparams = []
                typeparam = []
                #print(nodelst[-1].children[0].children[0].value)
                #print(len(nodelst[-1].children))
                if len(nodelst[-1].children) > 0 and nodelst[-1].children[0].nodeType == 'paramsNode': #there are param
                    for c in nodelst[-1].children[0].children:
                        fparams.append(c.value)
                        typeparam.append(c.type)
                fparams.append(len(fparams))
                #print(fparams)

                root.addchild(nodelst[-1])
                funcs[nodelst[-1].value] = [nodelst[-1].type, 0,fparams,typeparam]# save func name: type, funcpotopyte = 0 
                #funcprotopyte
                if tokenlst[index].value == ';':
                    index+=1
                    funcs[nodelst[-1].value][1] = 1 #set func name protopyte = 1, true. 
                    root.children[-1].isprototype = 1 # mark funcnode is funcprotopyte
                    #root.addchild(nodelst[-1])
                    #print(len(root.children))
                    return parse_program()
                #funcdef
                #funcbody type set during dfs tree
                elif parse_funcbody():
                    #add child
                    #programNode.addchild(nodelst[-1]) #add child
                    root.children[-1].addchild(nodelst[-1]) # funcbody is child of funcdec, not root now

                    #print(len(root.children))
                    return parse_program()
            #vardec
            elif parse_vardec():
                #programNode.addchild(nodelst[-1]) #add child
                nodelst[-1].isglobal = 1 # update vardec node to global
                for ids in nodelst[-1].children: #idents nodes
                    #print('2asadsssssssssssssssssssssss',ids.value)
                    for id1 in ids.children: #ident nodes
                        #print('2asadsssssssssssssssssssssss',id1.value)
                        globalVars[id1.value] = [nodelst[-1].type,id1.listsize] #vardec tuple, record the global value
                root.addchild(nodelst[-1])
                #print(len(root.children))
                return parse_program()
            elif parse_strcutdef():
                #programNode.addchild(nodelst[-1]) #add child
                nodelst[-1].isglobal = 1 # update vardec node to global
                root.addchild(nodelst[-1])

                globalStructs[nodelst[-1].value] = nodelst[-1].member #{name:type}
                #print(len(root.children))
                return parse_program()
            else:
                #print(index)
                print('syntax error, should start with vardec or funcdec or structdec in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                print('Parser error in file ', fname ,' in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value, '\n\t Expected with )')
                return False
        #print('syntax correct, end of file')
        return root
#'structdef':[['struct','id','{','}',';'],['struct','id','{','vardecs','}',';'],['struct','id','{','vardecs','}',';'], not all rules
#id : 306

# not allow multiple objects in one struct declareation
def parse_strcutdef():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    structNodes = structNode()
    

    while index < len(tokenlst):
        #struct
        if tokenlst[index].value == 'struct' or (tokenlst[index].value == 'const' and tokenlst[index +1].value == 'struct'):
            structNodes.nodeType = 'structNode'
            structNodes.lineno = tokenlst[index].lineno

            if tokenlst[index].value == 'const' and tokenlst[index +1].value == 'struct':
                
                structNodes.isconst = 1 #const struct
                index += 2
            else:
                index += 1
            #struct id, this id is a struct type
            if index < len(tokenlst) and tokenlst[index].type == 306 :
                structNodes.value =  tokenlst[index].value
                index += 1

                # struct could be list, check id[], id[int]
                if index < len(tokenlst) -1 and tokenlst[index].value == '[' and tokenlst[index+1].value == ']':
                    structNodes.value += '[]'
                    index += 2
                elif index < len(tokenlst) -2 and tokenlst[index].value == '[' and tokenlst[index+1].type == 303 and tokenlst[index+2].value == ']':
                    structNodes.value += '['+ tokenlst[index+1].value + ']'
                    index += 3

                #struct id id also work
                if index < len(tokenlst) and tokenlst[index].type == 306:
                    structNodes.type = structNodes.value
                    structNodes.value = tokenlst[index].value
                    index += 1
                    # struct could be list, check id[], id[int]
                    if index < len(tokenlst) -1 and tokenlst[index].value == '[' and tokenlst[index+1].value == ']':
                        structNodes.value += '[]'
                        index += 2
                    elif index < len(tokenlst) -2 and tokenlst[index].value == '[' and tokenlst[index+1].type == 303 and tokenlst[index+2].value == ']':
                        structNodes.value += '['+ tokenlst[index+1].value + ']'
                        index += 3

                #struct id  {
                if index < len(tokenlst) and tokenlst[index].value == '{':
                    index += 1
                    #struct id  { }
                    if index < len(tokenlst) and tokenlst[index].value == '}':
                        index += 1
                        if index < len(tokenlst) and tokenlst[index].value == ';':
                            index += 1
                            nodelst.append(structNodes) #add structnode to nodelst
                            return structNodes
                        else:
                            print('syntax error, expect "}" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                            return False
                    elif parse_vardec() or parse_strcutdef():
                        #
                        #add to struct member
                        if len(nodelst[-1].children) > 0: #struct could vardec or structdec as children
                            for cs in nodelst[-1].children:
                                if cs.nodeType == 'vardecNode':
                                    for ids in cs: #idents nodes
                                        for id1 in ids.children: #ident node
                                            structNodes.member[id1.value] = cs.type

                                elif cs.nodeType == 'structNode':
                                    structNodes.member[cs.value] = cs.type
                                    
                        structNodes.addchild(nodelst[-1])
                        
                        while parse_vardec() or parse_strcutdef():

                            #add to struct member
                            if len(nodelst[-1].children) > 0: #struct could vardec or structdec as children
                                for cs in nodelst[-1].children:
                                    if cs.nodeType == 'vardecNode':
                                        for ids in cs.children: #idents nodes
                                            for id1 in ids.children: #ident node
                                                structNodes.member[id1.value] = cs.type

                                    elif cs.nodeType == 'structNode':
                                        structNodes.member[cs.value] = cs.type

                            structNodes.addchild(nodelst[-1])
                            continue
                        if index < len(tokenlst) and tokenlst[index].value == '}':
                            index += 1
                            if index < len(tokenlst) and tokenlst[index].value == ';':
                                index += 1
                                nodelst.append(structNodes) #add structnode to nodelst
                                return structNodes
                            else:
                                print('syntax error, expect ";" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                return False
                        else:
                            print('syntax error, expect "}" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                            return False

                    else:
                        #print('syntax error, expect "}" or vardec or structdec in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                        return False
                # struct id id ;
                elif index < len(tokenlst) and tokenlst[index].value == ';':
                    index += 1
                    nodelst.append(structNodes) #add structnode to nodelst
                    return structNodes
                
                else:
                    #print('syntax error, expect "}" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect identifier in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        else:
            #not struct
            return False
    return root
#'vardec':[['const','typename','idents',';'],['typename','const','idents',';'],['typename','idents',';']],
def parse_vardec():
    global index
    global tokenlst
    global root
    global nodelst
    global globalVars

    #varnode: nodetype, isconst, type, varlst, isglobal(global or local variables)
    varNode = vardecNode()
    while index < len(tokenlst) :
        #globalvar or local var will be decided by its parents node , update in its parents node
        #const type or type const + idents + ;
        if index < len(tokenlst) - 2 and ((tokenlst[index].value == 'const' and tokenlst[index+1].type == 301) or \
            (tokenlst[index+1].value == 'const' and tokenlst[index].type == 301)):
            varNode.lineno = tokenlst[index].lineno #update lineno
            
            varNode.isconst = 1
            #varNode.nodeType = 'vardec'
            
            
            if tokenlst[index].type == 301:
                varNode.type = tokenlst[index].value
            elif tokenlst[index + 1].type == 301:
                varNode.type = tokenlst[index+1].value

            index += 2

            #print('const vardec type',varNode.type)

            '''
            temp  = index
            while temp < len(tokenlst):
                if tokenlst[temp].value != ';' or tokenlst[temp].value != '{' or tokenlst[temp].value != '(':
                    temp += 1
                else:
                    if tokenlst[temp].value == ';':
                            parse_idents()
                            if index < len(tokenlst) and tokenlst[index].value == ';':
                                index += 1
                                varNode.addchild(nodelst[-1])
                                nodelst.append(varNode)
                                return varNode
                    else :
                        return parse_funcdec()
            '''
            templist = nodelst
            tempindex = index
            if parse_idents():
                if index < len(tokenlst) and tokenlst[index].value == ';':
                    #print('vardec in line', tokenlst[index].lineno)
                    index += 1
                    varNode.addchild(nodelst[-1]) # varnode variables = identsNode.varables
                    #print(nodelst[-1].type) #check
                    nodelst.append(varNode) #add to nodelst
                    return varNode
                elif index < len(tokenlst)  and tokenlst[index].value == '{' or tokenlst[index].value == '(':
                    #index -= 2
                    # const type id ( or {
                    index = tempindex
                    nodelst = templist
                    return parse_funcdec()
                else:
                    print('syntax error, expect ; in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            
            else:
                print('syntax error, expect idents in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
            
        
        #type + idents + ;
        elif tokenlst[index].type == 301:
            varNode.lineno = tokenlst[index].lineno #update lineno
            varNode.type = tokenlst[index].value
            #print('vardec type',varNode.type)
            index += 1

            templist = nodelst
            tempindex = index
            if parse_idents():
                if index < len(tokenlst) and tokenlst[index].value == ';':
                    
                    #print('vardec in line', tokenlst[index].lineno)
                    index += 1
                    varNode.addchild(nodelst[-1]) # varnode variables = identsNode.varables
                    #print(nodelst[-1].nodeType) #check
                    nodelst.append(varNode)
                    return varNode
                elif tokenlst[index].value == '{' or tokenlst[index].value == '(':
                    #index -= 1
                    index = tempindex
                    nodelst = templist
                    return parse_funcdec()
                else:
                    #print("index is",index)
                    print('syntax error, expect ; in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect idents in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        #??? not vardec
        else:
            #print('syntax error, expect vardec; in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    #end of file, true?
    return varNode
    
#indents,'id':306, ',':44,   '[':91, ']':93, 'int_lit':303,
#'idents':[['id'],['id','[','int_val',']'], ['id','[','int_val',']',',','idents'],['id',',','idents']],

def parse_ident():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    idNode = identNode()
    while index < len(tokenlst):
        # id + [ ]  continue parse_idents
        if index < len(tokenlst) -3 and tokenlst[index].type == 306 and tokenlst[index+1].type == 91 and tokenlst[index + 2].type == 93:
            idNode.lineno = tokenlst[index].lineno #update lineno
            idNode.value = tokenlst[index].value + tokenlst[index+1].value +tokenlst[index+2].value
            idNode.listsize = 1 #default is 0
            index += 3
            nodelst.append(idNode)
            return idNode
        # id + [int_val ]  continue parse_idents
        elif index < len(tokenlst) -4 and tokenlst[index].type == 306 and tokenlst[index+1].type == 91 and tokenlst[index + 2].type == 303 and tokenlst[index + 3].type == 93:
            idNode.lineno = tokenlst[index].lineno #update lineno
            idNode.value = tokenlst[index].value + tokenlst[index+1].value +tokenlst[index+2].value +tokenlst[index+3].value
            #idNode.islist = 1
            idNode.listsize = tokenlst[index + 2].value #list size
            index += 4
            nodelst.append(idNode)            
            return idNode
        # id
        elif tokenlst[index].type == 306:
            idNode.lineno = tokenlst[index].lineno #update lineno
            idNode.value = tokenlst[index].value
            index += 1
            nodelst.append(idNode)
            return idNode
        else :
            #print('syntax error, expect ident in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    #end of file, true
    return idNode

#   'char_lit':302,
#   'int':303,
#   'real':304,
#   'str_lit':305,
#vardec include init
'''
def parse_idents():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    idsNode = identsNode()
    while index < len(tokenlst):
        idflag = 0 #record ident num
        while True:
            if parse_ident():
                idsNode.lineno = tokenlst[index].lineno #update lineno
                idflag += 1
                idsNode.addchild(nodelst[-1])
                #print(idsNode.children[-1].value) #check
                # , = 44
                if index < len(tokenlst) and tokenlst[index].type == 44:
                    index += 1
                
                #return parse_idents()
                #ident initlize
                elif index < len(tokenlst) and tokenlst[index].value == '=':
                    index += 1
                    if index < len(tokenlst) and  tokenlst[index].type == 302 or tokenlst[index].type == 303 or tokenlst[index].type == 304 or tokenlst[index].type == 305 or tokenlst[index].type == 306:
                        index += 1
                        idsNode.children[-1].setvalue(tokenlst[index].value) #init value 
                        #return True
                    # , = 44
                    if index < len(tokenlst) and tokenlst[index].type == 44:
                        index += 1
                    else:
                        break
                #check
                #for c in idsNode.children:
                #    print('check idents child ',c.value)
            else:
                break
        if idflag == 0:
            return False
        nodelst.append(idsNode)
        return idsNode
    return idsNode
'''

def parse_idents():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    idsNode = identsNode()
    while index < len(tokenlst):
        idflag = 0 #record ident num
        while True:
            if parse_ident():
                idsNode.lineno = tokenlst[index].lineno #update lineno
                idflag += 1
                idsNode.addchild(nodelst[-1])
                #print(idsNode.children[-1].value) #check
                # , = 44
                if index < len(tokenlst) and tokenlst[index].type == 44:
                    index += 1
                
                #return parse_idents()
                #ident initlize
                elif index < len(tokenlst) and tokenlst[index].value == '=':
                    index += 1
                    '''
                    if index < len(tokenlst) and  tokenlst[index].type == 302 or tokenlst[index].type == 303 or tokenlst[index].type == 304 or tokenlst[index].type == 305 or tokenlst[index].type == 306:
                        index += 1
                        idsNode.children[-1].setvalue(tokenlst[index].value) #init value 
                        #return True
                    '''
                    if parse_expr():
                        #expr is ident children
                        idsNode.children[-1].addchild(nodelst[-1])
                    # , = 44
                    if index < len(tokenlst) and tokenlst[index].type == 44:
                        index += 1
                    else:
                        break
                #check
                #for c in idsNode.children:
                #    print('check idents child ',c.value)
            else:
                break
        if idflag == 0:
            return False
        nodelst.append(idsNode)
        return idsNode
    return idsNode
    
#     'id':306, ',':44,   '[':91, ']':93, 'int_lit':303, type 301, const 401, { 123,  }125
#    'funcprototype':[['funcdec',';']],
#    'funcdec':[['typename','id','(',')'],['typename','id','(','params',')']],[['typename','const','id','(',')'],['const','typename','id','(','params',')']]
#    'param':[['typename','id'], ['typename','id','[',']']],
#    'params':[['param',',','params'], ['param']],
#    'funcdef':[['funcdec','{','}'], ['funcdec','{','vardecs','stmts','}'], ['funcdec','{','vardecs','}'], ['funcdec','{','stmts','}']],
#    'funcbody':[['{','}'], ['{','vardecs','stmts','}'], ['{','vardecs','}'], ['{','stmts','}']],
#     funcdef = funcdec + funcbody, no funcdef, divide it to two parts




def test2():
    fnode = funcNode()
    #print('fnodetest1111111111111111',fnode.isconst)


def parse_funcdec():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs
    #funcNode = astNode()
    fNode = funcNode()
    
    # have trouble to exactly pos the error with all conditions in one line
    while index < len(tokenlst):
        # const typename id (, or typename const id (
        if index < len(tokenlst) -5 and ((tokenlst[index].type == 401 and tokenlst[index + 1].type == 301 and tokenlst[index + 2].type == 306 and tokenlst[index+3].value == '(')\
            or (tokenlst[index].type == 301 and tokenlst[index + 1].type == 401 and tokenlst[index + 2].type == 306 and tokenlst[index+3].value == '(')):
            #
            fNode.isconst = 1
            if tokenlst[index].type == 301:
                fNode.type = tokenlst[index].value

            else:
                fNode.type = tokenlst[index+1].value

            fNode.value = tokenlst[index+2].value # funcname
            fNode.lineno = tokenlst[index].lineno #update lineno
            # check if not defined or  is funcprotopyte
            if fNode.value not in funcs.keys() or funcs[fNode.value][1] == 1:
                funcs[fNode.value] = [fNode.type, 0] # now fNode.value is func with type  fNode.type, not funcprotopyte any more if was
            else:
                error_log.append('Type checking error in file ', fname, ' in line ', tokenlst[index].lineno , )

            #no params 
            if tokenlst[index+4].value == ')':
                index += 5
                nodelst.append(fNode)
                return fNode
            else:
                index += 4
                if parse_params():
                    fNode.addchild(nodelst[-1]) #add params node to child
                    if tokenlst[index].value == ')':
                        index+=1
                        nodelst.append(fNode)
                        return fNode
                    else:
                        print('syntax error in funcdec, expect ) in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)  
                        return False
                else:
                    #print('syntax error in funcdec, expect params in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    #return False
                    nodelst.append(fNode)
                    return fNode

       # typename id (
        elif index < len(tokenlst) -4 and tokenlst[index].type == 301 and tokenlst[index + 1].type == 306 and tokenlst[index+2].value == '(':
            #
            fNode.lineno = tokenlst[index].lineno #update lineno
            fNode.type = tokenlst[index].value
            fNode.value = tokenlst[index+1].value

            if tokenlst[index+3].value == ')':
                index += 4
                nodelst.append(fNode)
                return fNode
            else:
                index += 3
                if parse_params():
                    fNode.addchild(nodelst[-1])
                    if tokenlst[index].value == ')':
                        index+=1
                        nodelst.append(fNode)
                        return fNode
                    else:
                        print('syntax error in funcdec, expect ) in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)  
                        return False
                else:
                    #print('syntax error in funcdec, expect params in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    nodelst.append(fNode)
                    return fNode
        else:
            return False
    #print('end of file')    
    exit
    return fNode     

#    'funcbody':[['{','}'], ['{','vardecs','stmts','}'], ['{','vardecs','}'], ['{','stmts','}']],
#    'stmt':[[';'], ['expr',';'], ['break',';'], ['continue',';'], ['return',';'], ['return','expr',';'], ['ifstmt'],['forstmt'],
#    ['whilestmt'],['dowhilestmt']],

#countf = 0

def parse_param():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs
    #could also have const type parameter
    paramNodes = paramNode()
    while index < len(tokenlst):
        #typename 
        if index < len(tokenlst) and tokenlst[index].type == 301:
            paramNodes.lineno = tokenlst[index].lineno
            paramNodes.type = tokenlst[index].value #
            #print('111111111111111111111',paramNodes.type)
            index += 1
            # const
            if index < len(tokenlst) and tokenlst[index].value == 'const':
                index += 1
                paramNodes.isconst = 1
            #typename id
            if index < len(tokenlst) and tokenlst[index].type == 306:
                index += 1
                
                #typename id [
                if index < len(tokenlst) and tokenlst[index].value == '[':
                    index += 1
                    #typename id [ ]
                    if index < len(tokenlst) and tokenlst[index].value == ']':
                        index += 1
                        paramNodes.value = tokenlst[index-3].value + '[]'
                        paramNodes.islist = 1
                        nodelst.append(paramNodes)
                        return paramNodes
                    else:
                        print('syntax error, expect "]" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value) 
                        return False
                #just type id

                else:
                    paramNodes.value = tokenlst[index-1].value
                    nodelst.append(paramNodes)
                    return paramNodes
            else:
                print('syntax error, expect identifier in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value) 
                return False
        else:
            # not type id, not param
            return False
    return paramNodes

def parse_params():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs
    paramsNodes = paramsNode()
    if parse_param():
        paramsNodes.lineno = nodelst[-1].lineno
        paramsNodes.addchild(nodelst[-1])
        if index < len(tokenlst) and tokenlst[index].value == ',':
            index += 1
            while parse_param():
                paramsNodes.addchild(nodelst[-1])
                if index < len(tokenlst) and tokenlst[index].value == ',':
                    index += 1
                else:
                    nodelst.append(paramsNodes)
                    return paramsNodes
            nodelst.append(paramsNodes)
            return paramsNodes
        else:
            #param
            nodelst.append(paramsNodes)
            return paramsNodes
            #return True
    else:
        # not params
        return False

def parse_funcbody():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs
    funcbodyNodes = funcbodyNode()
    while index < len(tokenlst):
        if tokenlst[index].value == '{':
            funcbodyNodes.lineno = tokenlst[index].lineno #update lineno
            index += 1
            #{ }
            if tokenlst[index].value == '}':
                index += 1
                nodelst.append(funcbodyNodes)
                return funcbodyNodes #empty body
            elif parse_vardec() or parse_stmts() or parse_strcutdef():
                    funcbodyNodes.addchild(nodelst[-1]) #add to child
                    while  parse_vardec() or parse_stmts() or parse_strcutdef():
                        funcbodyNodes.addchild(nodelst[-1])
                        if tokenlst[index].value == '}':
                            #print('funcbody } in ',tokenlst[index].lineno )
                            index += 1
                            #countf += 1
                            #print('countf',countf)
                            nodelst.append(funcbodyNodes)
                            return funcbodyNodes
                    if tokenlst[index].value == '}':
                        #print('11111funcbody } in ',tokenlst[index].lineno )
                        index += 1
                        #countf += 1
                        #print('countf',countf)
                        nodelst.append(funcbodyNodes)
                        return funcbodyNodes
                    else:
                        #print('syntax error, expect } in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                        return False
            else:
                print('syntax error, expect vardec or stmts or structdec in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
            
        else:
            #print('syntax error, expect { in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    #end of file
    return funcbodyNodes
                    
#    'stmt':[[';'], ['expr',';'], ['break',';'], ['continue',';'], ['return',';'], ['return','expr',';'], ['ifstmt'],['forstmt'],
#    ['whilestmt'],['dowhilestmt']],
def parse_stmt():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    stmtNodes = stmtNode()
    while index < len(tokenlst):
        # ;
        if tokenlst[index].value == ';':
            stmtNodes.lineno = tokenlst[index].lineno #update lineno
            index += 1
            nodelst.append(stmtNodes)
            return stmtNodes
        # break ;
        elif index < len(tokenlst) - 1 and tokenlst[index].value == 'break' and tokenlst[index+1].value == ';':
            stmtNodes.lineno = tokenlst[index].lineno #update lineno
            index += 2
            stmtNodes.value = 'break'
            nodelst.append(stmtNodes)
            return stmtNodes
        # continue ;
        elif index < len(tokenlst) - 1 and tokenlst[index].value == 'continue' and tokenlst[index+1].value == ';':
            stmtNodes.lineno = tokenlst[index].lineno #update lineno
            index += 2
            stmtNodes.value = 'continue'
            nodelst.append(stmtNodes)
            return stmtNodes
        #return ;
        elif index < len(tokenlst) - 1 and tokenlst[index].value == 'return' and tokenlst[index+1].value == ';':
            stmtNodes.lineno = tokenlst[index].lineno #update lineno
            index += 2
            #print('test return ;',tokenlst[index].value)
            stmtNodes.value = 'return'
            nodelst.append(stmtNodes)
            return stmtNodes
        # if 
        elif tokenlst[index].value == 'if':
            stmtNodes.lineno = tokenlst[index].lineno #update lineno

            if parse_ifstmt():
                stmtNodes.value = 'if'
                stmtNodes.addchild(nodelst[-1])
                nodelst.append(stmtNodes)
                return stmtNodes
            #    return True
            #else:
            #    print('syntax error in if stmts in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            #    return False
        #for 
        elif tokenlst[index].value == 'for':
            stmtNodes.lineno = tokenlst[index].lineno #update lineno
            if parse_forstmt():
                stmtNodes.value = 'for'
                stmtNodes.addchild(nodelst[-1])
                nodelst.append(stmtNodes)
                return stmtNodes
            #    return True   
            #else:
            #    print('syntax error in for stmts in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            #    return False
        #while
        elif tokenlst[index].value == 'while':
            stmtNodes.lineno = tokenlst[index].lineno #update lineno
            if parse_whilestmt():
                stmtNodes.value = 'while'
                stmtNodes.addchild(nodelst[-1])
                nodelst.append(stmtNodes)
                return stmtNodes
            #    return True   
            #else:
            #    print('syntax error in while stmts in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            #    return False
        # do while
        elif tokenlst[index].value == 'do':
            stmtNodes.lineno = tokenlst[index].lineno #update lineno
            if parse_dowhilestmt():
                stmtNodes.value = 'do'
                stmtNodes.addchild(nodelst[-1])
                nodelst.append(stmtNodes)
                return stmtNodes
            #    return True   
            #else:
            #    print('syntax error in dowhile stmts in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            #    return False
        #return expr ;
        elif tokenlst[index].value == 'return':
            stmtNodes.lineno = tokenlst[index].lineno #update lineno
            #print('11111111111111111111111111111111111111111111111test return ',tokenlst[index].value)
            #print(tokenlst[index].lineno, 'lineno and index ', index)
            stmtNodes.value = 'return'
          
            index += 1
            if parse_expr():
                if tokenlst[index].value == ';':
                    index += 1
                    stmtNodes.addchild(nodelst[-1])
                    nodelst.append(stmtNodes)
                    return stmtNodes
                else:
                    print('syntax error, expect ";" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        #expr ; 
        elif parse_expr():
            stmtNodes.lineno = nodelst[-1].lineno #update lineno
            if tokenlst[index].value == ';':
                index += 1
                stmtNodes.value = 'expr'
                stmtNodes.addchild(nodelst[-1])
                nodelst.append(stmtNodes)
                return stmtNodes
            else:
                print('syntax error, expect ";" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False   
        else:
            #not stmt
            #print(tokenlst[index].lineno, tokenlst[index].value)
            #print('stm loop test 1')
            return False     
    #print('stm loop test 2')
    return stmtNodes

#    'stmts':[['stmt','stmts'], ['stmt']],

def parse_stmts():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    stmtsNodes = stmtsNode()
    while index < len(tokenlst):
        if parse_stmt():
            stmtsNodes.lineno = nodelst[-1].lineno #update lineno
            stmtsNodes.addchild(nodelst[-1])
            while parse_stmt():
                stmtsNodes.addchild(nodelst[-1])
                #print(index, tokenlst[index].value)
                #continue
            nodelst.append(stmtsNodes)
            return stmtsNodes
        else:
            #print('111syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    return stmtsNodes
#stmtblock':[['{','}'], ['{','stmts','}']],

def parse_stmtblock():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    stmtblockNodes = stmtblockNode()

    while index < len(tokenlst):
        if tokenlst[index].value == '{':
            stmtblockNodes.lineno = tokenlst[index].lineno #update lineno
            #print('stmtblock { in ',tokenlst[index].lineno,' with value ', tokenlst[index].value )
            index += 1
            if index < len(tokenlst) and tokenlst[index].value == '}':
                #print('stmtblock } in ',tokenlst[index].lineno ,' with value ', tokenlst[index].value )
                #print('stmtblock } in ',tokenlst[index].lineno )
                index += 1
                nodelst.append(stmtblockNodes)
                return stmtblockNodes

            elif parse_stmts():
                stmtblockNodes.addchild(nodelst[-1]) #
                if index < len(tokenlst) and tokenlst[index].value == '}':
                    index += 1
                    #print('2222222stmtblock } in ',tokenlst[index].lineno,' with value ', tokenlst[index].value  )
                    #index += 1
                    return stmtblockNodes
                else:
                    print('syntax error, expect } in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect } or statements in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        else:
            return False
    return stmtblockNodes
#expr     
def parse_expr():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    
    #basic 
    #constval

    exprNodes = exprNode()
    while index < len(tokenlst):
        if parse_expr1():
            exprNodes.lineno = nodelst[-1].lineno #update lineno
            exprNodes.addchild(nodelst[-1])
            if parse_expr2():
                exprNodes.addchild(nodelst[-1])
                nodelst.append(exprNodes)
                return exprNodes
            #no expr2
            nodelst.append(exprNodes)
            return exprNodes
        else:
            return False
    return exprNodes

#'expr': [['constval'],['id','(','exprlst',')'], ['lval'], ['lval','assignoperator','expr'], ['++','lval'], ['lval','++'], 
# ['--','lval'], ['lval','--'], ['uoperator','expr'], ['expr','bioperator','expr'], ['expr','?','expr',':','expr'],['(','typename',')','expr'], ['(','expr',')']],
def parse_expr1():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs  # a dict, save the name and type

    expr1Nodes = expr1Node()
    #basic 
    #constval
    while index < len(tokenlst):
        expr1Nodes.lineno = tokenlst[index].lineno
        #constval,    'char_lit':302, 'int_lit':303, 'real_lit':304,'str_lit':305,
        if tokenlst[index].type == 302 or tokenlst[index].type == 303 or tokenlst[index].type == 304 or tokenlst[index].type == 305:
            
            #index +=1
            if tokenlst[index].type == 302:
                expr1Nodes.type = 'char'
            elif tokenlst[index].type == 303:
                expr1Nodes.type = 'int'
            elif tokenlst[index].type == 304:
                expr1Nodes.type = 'float'
            elif tokenlst[index].type == 305:
                expr1Nodes.type = 'char[]'    

            expr1Nodes.value = tokenlst[index].value
            expr1Nodes.isconst = 1
            expr1Nodes.lineno = tokenlst[index].lineno
            index += 1
            if parse_expr2():
                expr1Nodes.addchild(nodelst[-1])
                nodelst.append(expr1Nodes)
                return expr1Nodes
            else:
                return expr1Nodes
        # id','(','exprlst',')'
        #id
        elif tokenlst[index].type == 306 and tokenlst[index + 1].value == '(':
            #index += 2
            expr1Nodes.value = tokenlst[index].value
            index += 2
            # id ( )
            if index < len(tokenlst) and tokenlst[index].value == ')':
                index += 1
                nodelst.append(expr1Nodes)
                return expr1Nodes
            #id ( exprlst
            elif parse_exprlst():
                #id ( exprlst )
                expr1Nodes.addchild(nodelst[-1])
                if index < len(tokenlst) and tokenlst[index].value == ')':
                    index += 1
                    nodelst.append(expr1Nodes)
                    return expr1Nodes
                else:
                    print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect ")" or exprlst in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False

        #++ or -- or uoperator
        elif tokenlst[index].value == '++' or tokenlst[index].value == '--' or tokenlst[index].value == '-' or tokenlst[index].value == '!' or tokenlst[index].value == '~':
            expr1Nodes.lineno = tokenlst[index].lineno #update lineno
            index += 1
            expr1Nodes.addchild(tokenlst[index].value) # add ++ or -- to childrenlist
            if parse_lval():
                expr1Nodes.addchild(nodelst[-1])
                nodelst.append(expr1Nodes)
                return expr1Nodes
            else:
                print('syntax error, expect lval in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        #['(','typename',')','expr'], ['(','expr',')']],
        #(
        elif tokenlst[index].value == '(':
            index += 1
            # type 301
            #( typename 
            if index < len(tokenlst) and tokenlst[index].type == 301:
                expr1Nodes.lineno = tokenlst[index].lineno
                index += 1
                expr1Nodes.type = tokenlst[index].value # enforce the type to (typename)
                #( typename )
                if  index < len(tokenlst) and tokenlst[index].value == ')':
                    index += 1
                    if parse_expr():
                        expr1Nodes.addchild(nodelst[-1])
                        expr1Nodes.children[-1].type = expr1Nodes.type # widden the children type to parents type
                        nodelst.append(expr1Nodes)
                        return expr1Nodes
                    else:
                        print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                else:
                    print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            # ( expr         
            elif parse_expr():
                expr1Nodes.lineno = nodelst[-1].lineno
                expr1Nodes.addchild(nodelst[-1])
                
                # ( expr )
                if index < len(tokenlst) and tokenlst[index].value == ')':
                    index += 1
                    return expr1Nodes
                else:
                    print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect expr or typename in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        #['lval','assignoperator','expr']
        #lval, lval ++, lval --, 
        elif tokenlst[index].type == 306 and parse_lval():
            expr1Nodes.lineno = nodelst[-1].lineno
            expr1Nodes.addchild(nodelst[-1])
            if index < len(tokenlst) and (tokenlst[index].value == '++' or tokenlst[index].value == '--'):
                
                expr1Nodes.addchild(tokenlst[index].value)
                index += 1
                nodelst.append(expr1Nodes)
                return expr1Nodes
            #'assignoperator':[['='], ['+='], ['-='], ['*='], ['/=']],
            #lval assignmentoperator expr
            elif index < len(tokenlst) and (tokenlst[index].value == '+=' or tokenlst[index].value == '-=' or tokenlst[index].value == '*=' or tokenlst[index].value == '/=' or  tokenlst[index].value == '='):
                
                expr1Nodes.addchild(tokenlst[index].value)
                index += 1 
                if parse_expr():
                    expr1Nodes.addchild(nodelst[-1])
                    nodelst.append(expr1Nodes)
                    return expr1Nodes
                else:
                    print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                nodelst.append(expr1Nodes)
                return expr1Nodes

        else:
            # not expr
            return False
    return expr1Nodes

def parse_expr2():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    expr2Nodes = expr2Node()
    #basic 
    #constval
    while index < len(tokenlst):
            # ['expr','bioperator','expr'], ['expr','?','expr',':','expr']
        #expr bioperator expr ,left recursion,套娃，change to bioperator expr
        #elif parse_expr() and (parse_bioperator() or tokenlst[index].value == '?'):

        ################################should apply the Associativity Precedence, now take all bioperator as same precedence
        if parse_bioperator():
            expr2Nodes.lineno = tokenlst[index-1].lineno
            expr2Nodes.addchild(nodelst[-1])
            if parse_expr1():
                expr2Nodes.addchild(nodelst[-1])
                nodelst.append(expr2Nodes)


                while parse_bioperator():
                    #expr2Nodes.lineno = tokenlst[index-1].lineno
                    expr2Nodes.addchild(nodelst[-1])
                    if parse_expr1():
                        expr2Nodes.addchild(nodelst[-1])
                nodelst.append(expr2Nodes)
                return expr2Nodes
            else:
                print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
        elif tokenlst[index].value == '?':
            expr2Nodes.lineno = tokenlst[index].lineno
            expr2Nodes.addchild('?')
            index += 1
            if parse_expr1():
                expr2Nodes.addchild(nodelst[-1])
                if index < len(tokenlst) and tokenlst[index].value == ':':
                    index += 1
                    if parse_expr1():
                        expr2Nodes.addchild(nodelst[-1])
                        nodelst.append(expr2Nodes)
                        return expr2Nodes
                    else:
                        print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                        return False
                else:
                    print('syntax error, expect ":" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                #print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        else:
            #print('syntax error, expect bioperator or "?" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    return expr2Nodes
#'expr': [['constval'],['id','(','exprlst',')'], ['lval'], ['lval','assignoperator','expr'], ['++','lval'], ['lval','++'], 
# ['--','lval'], ['lval','--'], ['uoperator','expr'], ['expr','bioperator','expr'], ['expr','?','expr',':','expr'],['(','typename',')','expr'], ['(','expr',')']],

#'bioperator':[['=='],['!='],['>'],['>='],['<'],['<='],['+'],['-'],['*'],['/'],['%'],['|'],['&'],['||'],['&&']],
def parse_bioperator():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs
    bioperatorNodes = bioperatorNode()#
    if index >= len(tokenlst):
        return bioperatorNodes
    if tokenlst[index].value == '==' or tokenlst[index].value == '!=' or tokenlst[index].value == '>' or tokenlst[index].value == '>=' or \
        tokenlst[index].value == '<' or tokenlst[index].value == '<=' or tokenlst[index].value == '+' or tokenlst[index].value == '-' or \
            tokenlst[index].value == '*' or tokenlst[index].value == '/' or tokenlst[index].value == '%' or tokenlst[index].value == '|' or \
                tokenlst[index].value == '&' or tokenlst[index].value == '||' or tokenlst[index].value == '&&':
                bioperatorNodes.lineno = tokenlst[index].lineno # set lineno
                index += 1
                bioperatorNodes.value = tokenlst[index].value
                bioperatorNodes.addchild(tokenlst[index].value)
                nodelst.append(bioperatorNodes)
                return bioperatorNodes
    else:
        #print('syntax error, expect bi operator in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
        return False
#'ifstmt':[['if','(','expr',')','stmt'], ['if','(','expr',')','stmtblock'], ['if','(','expr',')','stmt','else','stmt'],\
#              ['if','(','expr',')','stmt','else','stmtblock'], ['if','(','expr',')','stmtblock','else','stmt'],
#               ['if','(','expr',')','stmtblock','else','stmtblock']],
def parse_ifstmt():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    ifNode = ifstmtNode()

    while index < len(tokenlst):
        if tokenlst[index].value == 'if':
            ifNode.lineno = tokenlst[index].lineno
            index += 1
            if index < len(tokenlst) and tokenlst[index].value == '(':
                index += 1
                #if ( expr 
                if parse_expr():
                    ifNode.addchild(nodelst[-1])# expr child for if 
                    if index < len(tokenlst) and tokenlst[index].value == ')':
                        index += 1
                        #if ( expr ) stmt
                        if parse_stmt():
                            ifNode.addchild(nodelst[-1])
                            if tokenlst[index].value == 'else':
                                ifNode.addchild('else')
                                index += 1
                                if parse_stmt():
                                    ifNode.addchild(nodelst[-1])
                                    nodelst.append(ifNode)
                                    return ifNode
                                elif parse_stmtblock():
                                    ifNode.addchild(nodelst[-1])
                                    nodelst.append(ifNode)
                                    return ifNode
                                else:
                                    print('syntax error, expect stmt or stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            else:
                                nodelst.append(ifNode)
                                return ifNode  
                        elif parse_stmtblock():
                            ifNode.addchild(nodelst[-1])
                            if tokenlst[index].value == 'else':
                                ifNode.addchild('else')
                                index += 1
                                if parse_stmt():
                                    ifNode.addchild(nodelst[-1])
                                    nodelst.append(ifNode)
                                    return ifNode
                                elif parse_stmtblock():
                                    ifNode.addchild(nodelst[-1])
                                    nodelst.append(ifNode)
                                    return ifNode
                                else:
                                    print('syntax error, expect stmt or stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            else:
                                nodelst.append(ifNode)
                                return ifNode
                        else:
                            print('syntax error, expect stmt ot stmts in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                            return False
                    else:
                        print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                        return False
                else:
                    print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect "(" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False               
        else:
            print('syntax error, expect if in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    return ifNode

#'forstmt':[['for','(','optexpr',';','optexpr',';','optexpr',')','stmtblock'], ['for','(','optexpr',';','optexpr',';','optexpr',')','stmt']],
def parse_forstmt():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    forNode = forstmtNode()
    while index < len(tokenlst):
        if tokenlst[index].value == 'for':
            forNode.lineno = tokenlst[index].lineno
            #print('start for stmt at line ', tokenlst[index].lineno)
            index += 1
            if index < len(tokenlst) and tokenlst[index].value == '(':
                index += 1
                #(; ; ) stmt or stmtblock
                #(; ; expr) stmt or stmtblock
                #(; expr ; ) stmt or stmtblock
                #(; expr ; expr )stmt or stmtblock
                if index < len(tokenlst) and tokenlst[index].value == ';':
                    index += 1
                    
                    if index < len(tokenlst) and tokenlst[index].value == ';':
                        index += 1
                        if index < len(tokenlst) and tokenlst[index].value == ')':
                            index += 1
                            if index < len(tokenlst) and tokenlst[index].value == '{':
                                if parse_stmtblock():
                                    forNode.addchild(nodelst[-1])
                                    nodelst.append(forNode)
                                    return forNode
                                else:
                                    print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            elif parse_stmt():
                                forNode.addchild(nodelst[-1])
                                nodelst.append(forNode)
                                return forNode
                            else:
                                print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                return False
                        elif parse_expr():
                            forNode.addchild(nodelst[-1])
                            if index < len(tokenlst) and tokenlst[index].value == ')':
                                index += 1
                                if index < len(tokenlst) and tokenlst[index].value == '{':
                                    if parse_stmtblock():
                                        forNode.addchild(nodelst[-1])
                                        nodelst.append(forNode)
                                        return forNode
                                    else:
                                        print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                        return False
                                elif parse_stmt():
                                    forNode.addchild(nodelst[-1])
                                    nodelst.append(forNode)
                                    return forNode
                                else:
                                    print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                        else:
                            print('syntax error, expect expr or ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                            return False
                    
                    # expr ; ) stmtblock or stmt
                    # expr ; expr ) stmtblock or stmt
                    elif parse_expr():
                        forNode.addchild(nodelst[-1])
                        if index < len(tokenlst) and tokenlst[index].value == ';':
                            index += 1
                            if index < len(tokenlst) and tokenlst[index].value == ')':
                                index += 1
                                if index < len(tokenlst) and tokenlst[index].value == '{':
                                    if parse_stmtblock():
                                        forNode.addchild(nodelst[-1])
                                        nodelst.append(forNode)
                                        return forNode
                                    else:
                                        print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                        return False
                                elif parse_stmt():
                                    forNode.addchild(nodelst[-1])
                                    nodelst.append(forNode)
                                    return forNode
                                else:
                                    print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            elif parse_expr():
                                forNode.addchild(nodelst[-1])
                                if index < len(tokenlst) and tokenlst[index].value == ')':
                                    index += 1
                                    if index < len(tokenlst) and tokenlst[index].value == '{':
                                        if parse_stmtblock():
                                            forNode.addchild(nodelst[-1])
                                            nodelst.append(forNode)
                                            return forNode
                                        else:
                                            print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                            return False
                                    elif parse_stmt():
                                        forNode.addchild(nodelst[-1])
                                        nodelst.append(forNode)
                                        return forNode
                                    else:
                                        print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                        return False
                                else:
                                    print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            else:
                                print('syntax error, expect expr or ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                return False
                        else:
                            print('syntax error, expect  ";" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                            return False
                    else:
                        print('syntax error, expect  ";" or expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                        return False
                elif parse_expr():
                    forNode.addchild(nodelst[-1])
                    if index < len(tokenlst) and tokenlst[index].value == ';':
                        index += 1
                        if index < len(tokenlst) and tokenlst[index].value == ';':
                            index += 1
                            if index < len(tokenlst) and tokenlst[index].value == ')':
                                index += 1
                                if index < len(tokenlst) and tokenlst[index].value == '{':
                                    if parse_stmtblock:
                                        forNode.addchild(nodelst[-1])
                                        nodelst.append(forNode)
                                        return forNode
                                    else:
                                        print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                        return False
                                elif parse_stmt():
                                    forNode.addchild(nodelst[-1])
                                    nodelst.append(forNode)
                                    return forNode
                                else:
                                    print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            elif parse_expr():
                                forNode.addchild(nodelst[-1])

                                if index < len(tokenlst) and tokenlst[index].value == ')':
                                    index += 1
                                    if index < len(tokenlst) and tokenlst[index].value == '{':
                                        if parse_stmtblock():
                                            forNode.addchild(nodelst[-1])
                                            nodelst.append(forNode)
                                            return forNode
                                        else:
                                            print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                            return False
                                    elif parse_stmt():
                                        forNode.addchild(nodelst[-1])
                                        nodelst.append(forNode)
                                        return forNode
                                    else:
                                        print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                        return False
                                else:
                                    print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            else:
                                print('syntax error, expect expr or ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                return False
                        
                        # expr ; ) stmtblock or stmt
                        # expr ; expr ) stmtblock or stmt
                        elif parse_expr():
                            forNode.addchild(nodelst[-1])
                            if index < len(tokenlst) and tokenlst[index].value == ';':
                                index += 1
                                if index < len(tokenlst) and tokenlst[index].value == ')':
                                    index += 1
                                    if index < len(tokenlst) and tokenlst[index].value == '{':
                                        if parse_stmtblock:
                                            forNode.addchild(nodelst[-1])
                                            nodelst.append(forNode)
                                            return forNode
                                        else:
                                            print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                            return False
                                    elif parse_stmt():
                                        forNode.addchild(nodelst[-1])
                                        nodelst.append(forNode)
                                        return forNode
                                    else:
                                        print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                        return False
                                elif parse_expr():
                                    forNode.addchild(nodelst[-1])
                                    if index < len(tokenlst) and tokenlst[index].value == ')':
                                        index += 1
                                        if index < len(tokenlst) and tokenlst[index].value == '{':
                                            if parse_stmtblock():
                                                forNode.addchild(nodelst[-1])
                                                nodelst.append(forNode)
                                                return forNode
                                                
                                            else:
                                                print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                                return False
                                        elif parse_stmt():
                                            forNode.addchild(nodelst[-1])
                                            nodelst.append(forNode)
                                            return forNode
                                        else:
                                            print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                            return False
                                else:
                                    print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            else:
                                print('1111syntax error, expect  ";" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                return False
                        else:
                            print('syntax error, expect  ";" or expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                            return False
                    else:
                        print('syntax error, expect  ";" or expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                        return False
                else:
                    print('syntax error, expect  ";" or expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect  "(" or expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False          
        else:
            #no need print error, this is just not forstmt 
            return False
    return forNode
#'whilestmt':[['while','(','expr',')','stmtblock'],['while','(','expr',')','stmt']],
def parse_whilestmt():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    whileNode = whilestmtNode()
    while index < len(tokenlst):
        if tokenlst[index].value == 'while':
            #print('whilestmt in ',tokenlst[index].lineno )
            whileNode.lineno = tokenlst[index].lineno
            index += 1
            if index < len(tokenlst) and tokenlst[index].value == '(':
                index += 1
                if parse_expr():
                    whileNode.addchild(nodelst[-1])
                    if index < len(tokenlst) and tokenlst[index].value == ')':
                        index += 1
                        if index < len(tokenlst) and tokenlst[index].value == '{':
                            #print('whilestmt block { in line ', tokenlst[index].lineno)
                            if parse_stmtblock():
                                whileNode.addchild(nodelst[-1])
                                nodelst.append(whileNode)
                                return whileNode
                            else:
                                #print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                return False
                        elif parse_stmt():
                            whileNode.addchild(nodelst[-1])
                            nodelst.append(whileNode)
                            return whileNode
                        else:
                            print('syntax error, expect stmtblock or stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                            return False
                    else:
                        print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                else:
                    print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect  "(" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        else:
            return False
    return whileNode
# 'dowhile':[['do','stmt','while','(','expr',')',';'], ['do','stmtblock','while','(','expr',')',';']],    
def parse_dowhilestmt():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    dowhileNode = dowhilestmtNode()
    while index < len(tokenlst):
        if tokenlst[index].value == 'do':
            dowhileNode.lineno = tokenlst[index].lineno
            index += 1
            if index < len(tokenlst) and tokenlst[index].value == '{':
                if parse_stmtblock():
                    dowhileNode.addchile(nodelst[-1])
                    if index < len(tokenlst) and tokenlst[index].value == 'while':
                        index += 1
                        if index < len(tokenlst) and tokenlst[index].value == '(':
                            if parse_expr():
                                dowhileNode.addchile(nodelst[-1])
                                if index < len(tokenlst) and tokenlst[index].value == ')':
                                    index += 1
                                    if index < len(tokenlst) and tokenlst[index].value == ';':
                                        index += 1
                                        nodelst.append(dowhileNode)
                                        return dowhileNode
                                    else:
                                        print('syntax error, expect ";" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                        return False
                                else:
                                    print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            else:
                                print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                return False
                        else:
                            print('syntax error, expect "(" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                            return False
                    else:
                        print('syntax error, expect while in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                        return False
                else:
                    print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            elif parse_stmt():
                dowhileNode.addchile(nodelst[-1])
                if index < len(tokenlst) and tokenlst[index].value == 'while':
                    index += 1
                    if index < len(tokenlst) and tokenlst[index].value == '(':
                        if parse_expr():
                            dowhileNode.addchile(nodelst[-1])
                            if index < len(tokenlst) and tokenlst[index].value == ')':
                                index += 1
                                if index < len(tokenlst) and tokenlst[index].value == ';':
                                    index += 1
                                    nodelst.append(dowhileNode)
                                    return dowhileNode
                                else:
                                    print('syntax error, expect ";" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            else:
                                print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                return False
                        else:
                            print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                            return False
                    else:
                        print('syntax error, expect "(" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                        return False
                else:
                    print('syntax error, expect while in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect stmtblock or stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False     
        # not start with do, not do while stmt          
        else:
            return False
    #end of file
    return dowhileNode
#    'exprlst':[['expr'], ['expr',',','exprlst']],

#    'uoperator':[['-'], ['!'], ['~']],

#    'lval':[['id'], ['id','(','expr',')'], ['lval','.','id'], ['lval','.','id','(','expr',')']]
def parse_exprlst():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs
    exprlstNodes = exprlstNode()
    while index < len(tokenlst):
        if parse_expr():
            exprlstNodes.lineno = nodelst[-1].lineno
            exprlstNodes.addchild(nodelst[-1])
            if tokenlst[index].value == ',':
                index += 1
            else:
                nodelst.append(exprlstNodes)
                return exprlstNodes
            while parse_expr():
                exprlstNodes.addchild(nodelst[-1])
                if tokenlst[index].value == ',':
                    index += 1
                else:
                    nodelst.append(exprlstNodes)
                    return exprlstNodes           
        else:
            print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    return exprlstNodes

#    'assignoperator':[['='], ['+='], ['-='], ['*='], ['/=']],
def parse_assignoperator():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs
    assignoperatorNodes = assignoperatorNode()
    while index < len(tokenlst):
        if tokenlst[index].value == '=' or tokenlst[index].value == '+=' or tokenlst[index].value == '-=' or tokenlst[index].value == '*=' or tokenlst[index].value == '/=':
            assignoperatorNodes.lineno = tokenlst[index].lineno
            index += 1
            assignoperatorNodes.value = tokenlst[index].value
            assignoperatorNodes.addchild(tokenlst[index].value)
            nodelst.append(assignoperatorNodes)
            return assignoperatorNodes
        else:
            print('syntax error, expect assignoperator in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    return assignoperatorNodes

#    'uoperator':[['-'], ['!'], ['~']],
def parse_uoperator():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs
    uoperatorNodes = uoperatorNode()
    while index < len(tokenlst):
        if tokenlst[index].value == '-' or tokenlst[index].value == '!' or tokenlst[index].value == '~' :
            uoperatorNodes.lineno = tokenlst[index].lineno
            index += 1
            uoperatorNodes.value = tokenlst[index].value
            uoperatorNodes.addchild(tokenlst[index].value)
            return uoperatorNodes
        else:
            print('syntax error, expect uoperator in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    return uoperatorNodes

#    'bioperator':[['=='],['!='],['>'],['>='],['<'],['<='],['+'],['-'],['*'],['/'],['%'],['|'],['&'],['||'],['&&']],
""" bioperatorlst = ['==','!=','>','>=','<','<=','+','-','*','/','%','|','&','||','&&']
def parse_bioperator():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs
    bioperatorNode = bioperatorNode()
    while index < len(tokenlst):
        if tokenlst[index].value in bioperatorlst:
            bioperatorNode.name = tokenlst[index].value
            bioperatorNode.addchild(tokenlst[index].value)
            index += 1
            return bioperatorNode
        else:
            #print('syntax error, expect bioperator in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    return bioperatorNode 
"""
#'lval':[['id'], ['id','[','expr',']'], ['lval','.','id'], ['lval','.','id','[','expr',']']], left recursion, elimilate left recursion
##'lval':[['id'], ['id','[','expr',']'], ['id','.','lval'], left recursion, elimilate left recursion
#'id':306, ',':44,   '[':91, ']':93, 'int_lit':303, type 301, const 401, { 123,  }125
def parse_lval():
    global index
    global tokenlst

    global root
    global nodelst

    global globalStructs
    global globalVars
    global funcs

    lvalNodes = lvalNode()

    while index < len(tokenlst):
        #print(index, 'tokenvalue is', tokenlst[index].value)
        # id 
        if tokenlst[index].type == 306:
            #print("lval index is ", tokenlst[index].value, ' with token num ',index, ' in line ', tokenlst[index].lineno)
            
            lvalNodes.lineno = tokenlst[index].lineno
            lvalNodes.value = tokenlst[index].value #
            #print('lval test',lvalNodes.value,lvalNodes.lineno )


            #typechecking need its type
            # if they are global var or struct, direct set its type, else set type in expr or funcdec
            # id is global var
            if tokenlst[index].value in globalVars:
                lvalNodes.type = globalVars[tokenlst[index].value][0] 
            elif tokenlst[index].value in globalStructs:
                lvalNodes.type = globalStructs[tokenlst[index].value][0] 

            index += 1
            # id []
            if index < len(tokenlst) and tokenlst[index].value == '[':
                index += 1
                if index < len(tokenlst) and tokenlst[index].value == ']':
                    index += 1
                    lvalNodes.value += '[]' 
                    #lval finished
                    nodelst.append(lvalNodes)
                    return lvalNodes
                elif parse_expr():

                    '''
                    #check expr type
                    if nodelst[-1].type != 'int' or 'char':
                        #print('check 11111',nodelst[-1].lineno)
                        #print(nodelst[-1].type)
                        if nodelst[-1].value != None:
                            emsg = 'Type checking error in file ' + fname +  ' line ' + chr(nodelst[-1].lineno) + ' wrong type for expr ' + nodelst[-1].value + ', expect type int or char'
                            error_log.append(emsg)
                    '''

                    lvalNodes.addchild(nodelst[-1]) #

                    if index < len(tokenlst) and tokenlst[index].value == ']':
                        index += 1
                        #not deal with struct 
                        if index < len(tokenlst) and tokenlst[index].value == '.':
                            index += 1
                            '''
                            # globalstructs = {structname:{members name: type}}
                            if tokenlst[index].value in globalStructs[lvalNodes.value]:
                                lvalNodes.type = globalStructs[lvalNodes.value][tokenlst[index].value]
                                lvalNodes.value = lvalNodes.value + '.' + tokenlst[index].value # lval value = struct.member
                                index += 1
                            '''
                            
                            if parse_lval():
                                lvalNodes.addchild(nodelst[-1])
                                nodelst.append(lvalNodes)
                                return lvalNodes
                        else:
                            # not . , lval finished
                            nodelst.append(lvalNodes)
                            return lvalNodes
                    else:
                        print('syntax error, expect ) in lval, in line ', tokenlst[index].lineno, ' near ', tokenlst[index].value)
                        return False
                else:
                    print('syntax error, expect expr in lval, in line ', tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            # id .
            elif index < len(tokenlst) and tokenlst[index].value == '.':
                index += 1

                
                if parse_lval():
                    lvalNodes.addchild(nodelst[-1]) #
                    nodelst.append(lvalNodes)
                    return lvalNodes
                

            # just id
            else:
                nodelst.append(lvalNodes)
                return lvalNodes
        # no id, not lval
        else:
            return False

    return lvalNodes

#'id':306, ',':44,   '[':91, ']':93, 'int_lit':303, type 301, const 401, { 123,  }125
#'param':[['typename','id'], ['typename','id','[',']']],
#'params':[['param',',','params'], ['param']],


parse_program()   
#print('globalvars: ',globalVars)     
#print('funcs: ',funcs)
#print('globalStructs: ',globalStructs)

globalvars = {} #value : type
globalstructs = {} #value:{member}
funcs = {}
curfunc = '' #func 没有嵌套
curstruct = [] #struct 嵌套
#localvar = {} #global 

def testdfs(root, depth):

    if root.children != []:
        for cnode in root.children:
            cnode.value = '11'
            #print(depth, cnode.nodeType, cnode.type, len(root.children))
            testdfs(cnode, depth + 1)

#testdfs(root,0)

def dfs(node):
    global globalvars
    global globalstructs  # struct name:{member name: type}
    global funcs  #name:[type, isprotopyte(true = 1) , params{name, type},  func local var {name:type}, struct {struct name: local member{name:type}}]
    global curfunc
    global curstruct
    global fname
    global error_log
    #global localvar

    if node.nodeType == 'rootNode':
        if node.children != []:
            for cnode in node.children:
                dfs(cnode)
    #vardec node already have type
    elif node.nodeType == 'vardecNode':

        if curfunc == '' and curstruct == []:
            for ids in node.children:
                for id in ids.children:
                    if id.children != []:
                        id.children[0].ancester = 'no'
                        dfs(id.children[0]) # id use expr to init
                        id.type = id.children[0].type
                    #print
                    print('Line ' + str(id.lineno) + ': global ' + node.type + ' ' + id.value)
                    #check redefine global vars
                    if id.value in globalvars:
                        errmsg = 'Type checking error in file ' + fname +  ' line ' + str(id.lineno) +', redefined global variable ' + id.value
                        error_log.append(errmsg)
                    else:
                        globalvars[id.value] = node.type #add to globalvars
        #local var in global curstruct
        elif curstruct != [] and curfunc == '':
            # update ancester
            node.ancester = curstruct[-1]

            for ids in node.children:
                for id in ids.children:
                    #check redefine global vars
                    if id.children != []:
                        id.children[0].ancester = 'no'
                        dfs(id.children[0]) # id use expr to init
                        id.type = id.children[0].type

                    if id.value in globalstructs[curstruct[-1]]:
                        errmsg = 'Type checking error in file ' + fname +  ' line ' + id.lineno +  ', redefined local member ' + id.value
                        error_log.append(errmsg)
                    #struct struct,only check depth is 2
                        
                    #elif len(curstruct) >=2 and id.value in globalstructs[curstruct[-2]][curstruct[-1]]:
                    #    errmsg = 'Type checking error in file ' + fname +  ' line ' + id.lineno +  ', redefined local member ' + id.value
                    #    error_log.append(errmsg)
                    else:
                        globalstructs[curstruct[-1]][id.value] = node.type #add to func's local vars

                        print('     '+'Line ' + str(id.lineno) + ': member  ' + node.type + ' ' + id.value)


        #local var in local struct in  curfunc
        elif curstruct != [] and curfunc != '':
            # update ancester
            node.ancester = curstruct[-1]

            for ids in node.children:
                for id in ids.children:
                    if id.children != []:
                        id.children[0].ancester = 'no'
                        dfs(id.children[0]) # id use expr to init
                        id.type = id.children[0].type
                    #check redefine global vars
                    if id.value in funcs[curfunc][4][curstruct[-1]]:
                        errmsg = 'Type checking error in file' + fname +  ' line ' + str(id.lineno) +  ', redefined local member ' + id.value
                        error_log.append(errmsg)
                    else:
                        #func = name: {type, {paramname: type}, {varname: type},{structname,type}}
                        #only work for func-struct-member, has bug,no time, should be embeded len(curstruct) depth
                        funcs[curfunc][4][curstruct[-1]][id.value] = node.type #add to func's local struct 's member and type
                        
                        print('     '+'Line ' + str(id.lineno) + ': member  ' + node.type + ' ' + id.value )

        #local var in  curfunc
        elif curstruct == [] and curfunc != '':
            # update ancester
            node.ancester = curfunc

            for ids in node.children:
                for id in ids.children:
                    if id.children != []:
                        id.children[0].ancester = 'no'
                        dfs(id.children[0]) # id use expr to init
                        id.type = id.children[0].type
                    #check redefine local vars,    
                    # could redefine global var in local
                    if id.value in funcs[curfunc][3]:
                        errmsg = 'Type checking error in file' + fname +  ' line ' + str(id.lineno) +  ', redefined local variable ' + id.value
                        error_log.append(errmsg)
                    #check smame name with params or not
                    elif id.value in funcs[curfunc][2][0]:
                        errmsg = 'Type checking error in file' + fname +  ' line ' + str(id.lineno) +  ', same name as function parameter ' + id.value
                        error_log.append(errmsg)                        
                    else:
                        #print(node.nodeType, node.type)

                        #func = name: {type, {paramname: type}, {varname: type},{structname,type}}
                        #only work for func-struct-member, has bug,no time, should be embeded len(curstruct) depth
                        funcs[curfunc][3][id.value] = node.type #add to func's local struct 's member and type
                        if node.isconst == 1:
                            print('     '+'Line ' + str(id.lineno) + ': local const '  + node.type + ' ' + id.value) # + node.type
                        else:
                            print('     '+'Line ' + str(id.lineno) + ': local '  + node.type + ' ' + id.value) # + node.type


    elif node.nodeType == 'funcNode':

        #check func name is defined or not
        #case1, protopyte redefined
        if node.value in funcs and (node.isprototype == 1 and funcs[node.value][1] == 1):
            errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', redefined function protopyte ' + node.value
            error_log.append(errmsg)
        elif node.value in funcs and (node.isprototype == 0 and funcs[node.value][1] == 0):
            errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', redefined function ' + node.value
            error_log.append(errmsg)    
        else:
            funcs[node.value] = [node.type, node.isprototype, [[],[]], {}, {}] #type, isprotopyte, parameters(name, type), local vars, local structs 
            if node.isprototype == 0:
                print('Line ' + str(node.lineno) + ': function  ' + node.type + ' ' + node.value)       

        #curfunc update
        curfunc = node.value
        if node.children != []: #chilren are params and funcbody
            for cnode in node.children:
                dfs(cnode)
        curfunc = '' #finished funcnode, init curfunc to ''

    elif node.nodeType == 'paramsNode':
        localparam = funcs[curfunc][2][0] # [params name]
        node.ancester = curfunc
        if node.children != [] :
            for cp in node.children:
                if cp in localparam:
                    errmsg = 'Type checking error in file' + fname +  ' line ' + str(cp.lineno) +  ', redeclared param ' + node.value
                    error_log.append(errmsg) 
                else:
                    if cp.isconst == 1 :
                        #needs its pos, use [] instead {}
                        funcs[curfunc][2][1].append(cp.type) #updatefunc params
                        funcs[curfunc][2][0].append(cp.value)
                        if funcs[curfunc][1] == 0:
                            print('     ' + 'Line ' + str(cp.lineno) + ': parameter  const ' + cp.type + ' ' + cp.value)  
                    else:
                        #needs its pos, use [] instead {}
                        funcs[curfunc][2][1].append(cp.type) #updatefunc params
                        funcs[curfunc][2][0].append(cp.value)
                        if funcs[curfunc][1] == 0:
                            print('     ' + 'Line ' + str(cp.lineno) + ': parameter ' + cp.type + ' ' + cp.value)  
                        #print( funcs[curfunc][1])
                        
    #funcbody, just dfs its children
    elif node.nodeType == 'funcbodyNode':
        node.ancester = curfunc
        if node.children != []:
            for cp in node.children:
                dfs(cp)


    elif node.nodeType == 'structNode':
        #global
        if curstruct == [] and curfunc == '':
            curstruct.append(node.value) #update struct flag, in the range of struct
            
            if node.value in globalstructs:
                errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', redefined global struct ' + node.value
                error_log.append(errmsg)
            else:
                globalstructs[node.value] = {} # addd to globalstruct and init
                if node.type != None:
                    print('Line ' + str(node.lineno) + ': global struct  ' + node.type + ' ' + node.value)   
                else:
                    print('Line ' + str(node.lineno) + ': global struct  ' + node.value) 
        #in func
        elif curstruct == [] and curfunc != '':
            curstruct.append(node.value)#update struct flag, in the range of struct
            if node.value in funcs[curfunc][4]:
                errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', redefined local struct ' + node.value
                error_log.append(errmsg)  
            else:
                funcs[curfunc][4][node.value] = {} ## addd to func local struct and init
                if node.type != None:
                    print('     ' + 'Line ' + str(node.lineno) + ': local struct  ' + node.type + ' ' + node.value)   
                else:
                    print('     ' + 'Line ' + str(node.lineno) + ': local struct  ' + node.value) 
        # in struct 
        elif curstruct != [] and curfunc == '':
            curstruct.append(node.value)#update struct flag, in the range of struct

            if node.value in globalstructs[curstruct[-2]]:
                errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', redefined local struct ' + node.value
                error_log.append(errmsg)

            else:
                globalstructs[curstruct[-1]] = {}## addd to strcut member struct and init
                if node.type != None:
                    print('     '+ 'Line ' + str(node.lineno) + ': member struct  ' + node.type + ' ' + node.value)   
                else:
                    print('     '+ 'Line ' + str(node.lineno) + ': member struct  ' + node.value) 
                    #struct struct
            '''
            elif len(curstruct)>2:
                globalstructs[curstruct[-2]][curstruct[-1]] = {}## addd to strcut member struct and init
                #print('ccc',globalstructs)
                if node.type != None:
                    print('     '+ 'Line ' + str(node.lineno) + ': member struct  ' + node.type + ' ' + node.value)   
                else:
                    print('     '+ 'Line ' + str(node.lineno) + ': member struct  ' + node.value) 
            '''
        # in func struct 
        elif curstruct != [] and curfunc != '':
            curstruct.append(node.value)#update struct flag, in the range of struct
            if node.value in funcs[curfunc][4][curstruct[-2]]:
                errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', redefined local struct ' + node.value
                error_log.append(errmsg)       
            else:
                funcs[curfunc][4][curstruct[-2]][node.value] = {}
                if node.type != None:
                    print('         '+ 'Line ' + str(node.lineno) + ': member struct  ' + node.type + ' ' + node.value)   
                else:
                    print('         '+ 'Line ' + str(node.lineno) + ': member struct  ' + node.value) 

        #visit children
        if node.children != []:
            for cnode in node.children:
                dfs(cnode)
        del curstruct[-1]


    elif node.nodeType == 'stmtsNode':
        if node.children != []:
            for cp in node.children:
                dfs(cp)

    elif node.nodeType == 'stmtNode':
        if node.children != []:
            for cp in node.children:
                #check return type
                if node.value == 'return':
                    cp.ancester = 'no'
                    dfs(cp)
                    if funcs[curfunc][0] != cp.type and cp.type != None:
                        errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', Return type mismatch: was ' + cp.type +', expected  ' + funcs[curfunc][0] 
                        error_log.append(errmsg)
                else:
                    dfs(cp)


    elif node.nodeType == 'stmtblockNode':
        if node.children != []:
            for cp in node.children:
                dfs(cp)

    elif node.nodeType == 'ifstmtNode':
        if node.children != []:
            for cp in node.children:
                dfs(cp)

    elif node.nodeType == 'forstmtNode':
        if node.children != []:
            for cp in node.children:
                dfs(cp)

    elif node.nodeType == 'whilestmtNode':
        if node.children != []:
            for cp in node.children:
                dfs(cp)

    elif node.nodeType == 'dowhilestmtNode':
        if node.children != []:
            for cp in node.children:
                dfs(cp)

    elif node.nodeType == 'exprlstNode':
        if node.children != []:
            for cp in node.children:
                cp.ancester = 'no'  
                dfs(cp)
                     

    elif node.nodeType == 'exprNode':
        if node.children != []:
            for cp in node.children:
                cp.ancester = 'no' # if not no could print
                dfs(cp) 
                
                #print('check expr children type',cp.type)
        #give the type to expr node
        if len(node.children) == 1: #only expr1
            node.type = node.children[0].type 
            #node.isconst = node.children[0].isconst 
            #print(node.ancester)
            
            if node.isconst == 1 and  node.type != None and node.ancester != 'no':
                print('     '+ 'Line ' + str(node.lineno) + ': expression has type const' + node.type )
            elif node.type != None and node.ancester != 'no':
                print('     '+ 'Line ' + str(node.lineno) + ': expression has type '+ node.type )
                #print(1)

        elif len(node.children) == 2: #expr1 expr2, check the typecl
            #expr2 type
            #print(node.ancester)
            if node.children[1].children[0] == '?': #expr ? expr:expr
                
                node.type = node.children[1].type
                node.isconst = node.children[1].isconst 
                if node.isconst == 1 and  node.type != None and node.ancester != 'no':
                    #print('111check ',node.ancester, node.lineno)
                    print('     '+ 'Line ' + str(node.lineno) + ': expression has type const' + node.type )
                elif node.type != None and node.ancester != 'no':
                    #print('111check ',node.ancester, node.lineno)
                    print('     '+ 'Line ' + str(node.lineno) + ': expression has type ' + node.type )
            elif node.children[1].children[0].nodeType == 'bioperatorNode':
                #dfs(node.children[1].children[1])
                #print('nonsssss',node.children[1].children[1].type)
                #print(node.ancester)

                temp = ['==', '>', '>=', '<', '<=', '&&', '||', '!=']
                if node.children[1].children[0].value in temp:
                    node.type = 'char' #boolean
                else:
                    node.type = widden(node.children[0].type, node.children[1].type) #widden type
                    #print('wawawaa',node.type)
                if node.children[0].isconst == node.children[1].isconst:
                    node.isconst = node.children[1].isconst 
            if node.isconst == 1 and  node.type != None and node.ancester != 'no':
                #print('111check ',node.ancester, node.lineno)
                print('     '+ 'Line ' + str(node.lineno) + ': expression has type const' + node.type )
            elif  node.type != None and  node.type != None and  node.ancester != 'no':
                #print('222check ',node.ancester, node.lineno)
                print('     '+ 'Line ' + str(node.lineno) + ': expression has type ' + node.type )
                #print(2)


    elif node.nodeType == 'expr1Node':
         #only expr1 and  its type is const val, no children, just pass
        if node.children == []:
            # id()
            if node.isconst == 0: # is isconst ==1, means this is constval
                #funcs
                if node.value in funcs:
                    node.type = funcs[node.value][0]
                    #check params, should no params
                    if funcs[node.value][2] == [[],[]]:
                        node.type = funcs[node.value][0] # type == funcs return type
                    else:
                        errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', Parameter mismatch in call to ' + node.value + \
                            ' Expected '+ len(funcs[node.value][2][0]) + ' but received 0 parameters'
                        error_log.append(errmsg)                       
                else:
                    errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', unknow function ' + node.value
                    error_log.append(errmsg)
            # is isconst ==1, means this is constval, it already has type and value, 

        if node.children != []:
            #expr1 as type i nthis case
            if len(node.children) == 1 and node.children[0].nodeType == 'expr2Node':
                #dfs expr
                node.children[0].ancester = 'no'
                dfs(node.children[0])
                

                #print('arrived here ???',node.children[0].type)
                #print(node.type)
                #check const
                if node.isconst != node.children[0].isconst:
                    node.isconst = 0

                if node.children[0].children[0].nodeType == 'bioperatorNode':
                    temp = ['==', '>', '>=', '<', '<=', '&&', '||', '!=']
                    
                    if node.children[0].children[0].value in temp:
                        node.type = 'char' #boolean
                    else:
                        temptype = widden(node.children[0].type, node.type) #widden type
                        if temptype == 'no':
                            errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', expect type ' + node.type + ' but has type '+ node.children[0].type
                            error_log.append(errmsg)
            # id(exprlst)
            elif len(node.children) == 1 and node.children[0].nodeType == 'exprlstNode':
                
                node.children[0].ancester = 'no'
                #print(len(node.children))
                #print(node.children[0].children[0].nodeType)

                #funcs
                if node.value in funcs:
                    node.type = funcs[node.value][0]
                    #check params, 
                    if len(funcs[node.value][2][0]) != len(node.children[0].children):
                        errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', Parameter number mismatch in call to ' + node.value + \
                            ' Expected '+ str(len(funcs[node.value][2][0])) + ' but received ' + str(len(node.children[0].children)) +' parameters'
                        #print(node.value)
                        #print(funcs[node.value])
                        error_log.append(errmsg)       
                    else:
                        #
                        iserror = 0
                        for i in range(len(node.children[0].children)):
                            #print(node.children[0].children[i].type)
                            #print(funcs[node.value][2][1][i])
                            #print(funcs[node.value][2])
                            #print(node.value)
                            if node.children[0].children[i].type != funcs[node.value][2][1][i] and node.children[0].children[i].type != None:
                                errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', Parameter type mismatch in call to ' + node.value + \
                                ' Expected type '+ funcs[node.value][2][1][i] + ' but received '  + node.children[0].children[i].type 
                                error_log.append(errmsg) 
                                iserror = 1
                        #all param type matched
                        if iserror == 0:
                            node.type = funcs[node.value][0] # type == funcs return type
                else:
                    errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', unknow function ' + node.value
                    error_log.append(errmsg)            
            # (exprnode) or (type)expr
            elif len(node.children) == 1 and node.children[0].nodeType == 'exprNode':
                
                node.children[0].ancester = 'no'
                dfs(node.children[0])

                if node.type == None:
                    node.type = node.children[0].type
                node.isconst = node.children[0].isconst

            elif len(node.children) == 1 and node.children[0].nodeType == 'lvalNode':
                
                node.children[0].ancester = 'no'
                dfs(node.children[0])
                node.type = node.children[0].type
                node.isconst = node.children[0].isconst
                #print('check A type', node.type)
                if node.type == None:
                    node.type = node.children[0].type
                           
            # lval ++,--, ;;;;; -, ! ,~ ,++ , --,) lval
            #elif len(node.children) == 2 and (node.children[0].nodeType == 'lvalNode' or node.children[1].nodeType == 'lvalNode'): 
            elif len(node.children) == 2: 
                if type(node.children[0]) != str and node.children[0].nodeType == 'lvalNode':
                    node.children[0].ancester = 'no'
                    dfs(node.children[0])
                    
                    node.type = node.children[0].type # lval ++, --
                    node.isconst = node.children[0].isconst
                    #print('arrived here 1111111111')
                else:
                    dfs(node.children[1])
                    #print('arrived here 1111111111')
                    if node.children[0] == '!':
                        node.type = 'char'
                        node.isconst = node.children[0].isconst
                    else:
                        node.type = node.children[1].type # lval ++, --
                        node.isconst = node.children[1].isconst
            #lval , +=, -=,*=, /=, expr
            elif len(node.children) == 3 and node.children[0].nodeType == 'lvalNode':

                node.children[0].ancester = 'no'
                dfs(node.children[0])
                
                #print('arrived here 1111111111')
                node.children[2].ancester = 'no'
                dfs(node.children[2])
                
                #print('arrived here 1111111111')

                #print('lval first children',node.children[0].type)
                #print('lval second children',node.children[1])
                #print('lval 3rd children',node.children[2].type)

                temptype = widden(node.children[0].type,node.children[2].type)
                node.isconst = node.children[0].isconst

                if temptype == 'no':
                    errmsg = 'Type checking error in file' + fname +  ' line ' +  str(node.lineno) + ', Invalid assignment '
                    error_log.append(errmsg)  
                else:
                    node.type = temptype
        #print('expr1 node', node.type, node.value, node.lineno)
    elif node.nodeType == 'expr2Node':
        if node.children != []:
            if node.children[0] == '?':

                node.children[1].ancester = 'no'
                node.children[2].ancester = 'no'
                dfs(node.children[1]) #expr1
                dfs(node.children[2]) #expr1

                node.type = node.children[1].type # actually need to select one based on former expr1 value
            elif node.children[0].nodeType == 'bioperatorNode':
                
                for cs in node.children:
                    if cs.nodeType == 'expr1Node':
                        cs.ancester = 'no'
                        dfs(cs)
                        
                        node.type = cs.type
                        #print(cs.type)
                        '''
                        if node.type == None:
                            node.type = cs.type
                        else:
                            node.type = widden(node.type, cs.type)
                        '''
                if node.type == 'no':
                    errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', Invalid bioperat action ' 
                    error_log.append(errmsg)                      

    elif node.nodeType == 'lvalNode':
        #print(node.value, node.lineno)
        idflag = 0
        if curfunc != '' and curstruct == []:
            
            #id in func params
            #funcs  #name:[type, isprotopyte(true = 1) , params[[name],[type]],  func local var {name:type}, struct {struct name: local member{name:type}}]
            if funcs[curfunc][2] != [[],[]]:
                for i in range(len(funcs[curfunc][2][0])):
                    
                    if checkidin(node.value, funcs[curfunc][2][0][i]):
                        idflag = 1
                        node.type = funcs[curfunc][2][1][i]
                        #print(node.value, funcs[curfunc][2][0][i], node.lineno)
                        #break
            #check local var
            if idflag == 0 and funcs[curfunc][3] != {}:
                for item in funcs[curfunc][3]:
                    if checkidin(node.value, item):
                        idflag = 1
                        node.type = funcs[curfunc][3][item]
            
            if idflag == 0:
                #errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', unknow variable ' + node.value
                #error_log.append(errmsg)
                tempttt = 0
            else:
                if node.children != []:

                    node.children[0].ancester = 'no'
                    if node.children[-1].type != None or node.children[-1].value != None:
                        dfs(node.children[-1])
                    
                    if node.children[0].type != 'int' and node.children[0].type != None :
                        errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.children[0].lineno) +  ', Expect type int, but received ' 
                        error_log.append(errmsg)
            
        #in global struct
        if curfunc == '' and curstruct != []:
            #id in struct
            #funcs  #name:[type, isprotopyte(true = 1) , params[[name],[type]],  func local var {name:type}, struct {struct name: local member{name:type}}]
            if globalstructs[curstruct[-1]] != {}:
                for item in globalstructs[curstruct[-1]]:
                    if checkidin(node.value, item):
                        idflag = 1
                        node.type = funcs[curfunc][3][node.value]
            if idflag == 0:
                errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', unknow variable ' + node.value
                error_log.append(errmsg)
            
            else:
                if node.children != []:
                    node.children[-1].ancester = 'no'
                    if node.children[-1].type != None or node.children[-1].value != None:
                        dfs(node.children[-1])
                    
                    if node.children[-1].type != 'int':
                        errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.children[0].lineno) +  ', Expect type int in []' 
                        error_log.append(errmsg)       
            

            #print(1)
                #nomatter what case, globalvar all need to check
        
        if idflag == 0:
            for item in globalvars:
                if checkidin(node.value, item):
                    idflag = 1
                    node.type = globalvars[item]
                    break
                #if id[expr]
            if idflag == 0:
                errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.lineno) +  ', unknow variable ' + node.value
                error_log.append(errmsg)
            
            else:
                if node.children != []:
                    node.children[-1].ancester = 'lval'
                    for cnode in node.children:
                        cnode.ancester = 'no'
                        if cnode.type != None or cnode.value != None:
                            dfs(cnode)
                        
                    # id[expr]
                    if node.children[0].type != 'int': #or node.children[0].type != 'char':
                        errmsg = 'Type checking error in file' + fname +  ' line ' + str(node.children[0].lineno) +  ', Expect type int in []' 
                        error_log.append(errmsg)
            
        #print('check A type', node.type, node.lineno, node.value)





                
def checkidin(a,b):
    if a == b:
        return True
    elif a+'[]' == b:
        return True
    # A, A[int]
    elif (len(b) >= len(a) + 3) and a + '[' == b[:len(a)+1] and b[-1] == ']':
        return True
    # A[], A[200]
    elif (len(b) >= len(a) ) and a[:-1] == b[:len(a)-1] and b[-1] == ']' and a[-1] == ']':
        return True
    # A[1], A[100] , no this case, lval will only record A, not A[1]
    else:
        return False
                    

def widden(type1, type2):
    if type1 == type2:
        return type1
    elif (type1 == 'char' and type2 == 'int') or (type2 == 'char' and type1 == 'int'):
        return 'int'
    elif (type1 == 'float' and type2 == 'int') or (type2 == 'int' and type1 == 'float'):
        return 'float'
    elif (type1 == 'float' and type2 == 'char') or (type2 == 'char' and type1 == 'float'):
        return 'float'
    elif type1 == None:
        return type2
    elif type2 == None:
        return type1
    else:
        return 'no'

#dfs(root)
#for item in error_log:
    #print(item)





