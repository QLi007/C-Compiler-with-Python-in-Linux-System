# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:24:07 2022

@author: Administrator

"""

import sys, os, collections
from turtle import Turtle
import lexer2
from lexer2 import get_word
#from mycc import infile
sys.path.append(os.pardir)


sys.setrecursionlimit(1000)
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
    
    #def parse_file():

    
#tokenlst  = []
#fname = 'test1_part3.c'
#fname = 'test.c'
#lexer1.get_word(fname,tokenlst)
#fname = infile()
fname = sys.argv[2]
tokenlst = parser(filename = fname).getToken()
#tokenlst = parser(filename = 'test.c').getToken()
#print(tokenlst)

index = 0
#'program':[['vardec','program'], ['funcprototype','program'], ['funcdef','program'],['structdef','program'],['null']],

def parse_program():
    global index
    global tokenlst
    #empty file
    if len(tokenlst) == 0:
        print('empty file, syntax correct')
        return True
    #LL(K) check, NO UPDATE index
    

    if index >= len(tokenlst):
        print('syntax correct')
        return True
    else:
        #'vardec':[['const','typename','idents',';'],['typename','const','idents',';'],['typename','idents',';']],
        #'vardecs':[['vardec'],['vardec','vardecs']],
        #'funcprototype':[['funcdec',';']],
        #'funcdec':[['typename','id','(',')'],['typename','id','(','params',')']],
        #'funcdef':[['funcdec','{','}'], ['funcdec','{','vardecs','stmts','}'], ['funcdec','{','vardecs','}'], ['funcdec','{','stmts','}']],
        #'structdef':[['struct','id','{','}',';'],['struct','id','{','vardecs','}',';'],['struct','id','id','{','vardecs','}',';'],['struct','id','id','{','}',';']],
        #print(index)
        while index < len(tokenlst):
            
            #funcdec
            if parse_funcdec():
                #funcprotopyte
                if tokenlst[index].value == ';':
                    index+=1
                    return parse_program()
                #funcdef
                elif parse_funcbody():
                    return parse_program()
            #vardec
            elif parse_vardec():
                return parse_program()
            elif parse_strcutdef():
                return parse_program()
            else:
                #print(index)
                print('syntax error, should start with vardec or funcdec or structdec in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        print('syntax correct, end of file')
        return True
#'structdef':[['struct','id','{','}',';'],['struct','id','{','vardecs','}',';'],['struct','id','{','vardecs','}',';'], not all rules
#id : 306
def parse_strcutdef():
    global index
    global tokenlst
    while index < len(tokenlst):
        #struct
        if tokenlst[index].value == 'struct' or (tokenlst[index].value == 'const' and tokenlst[index +1].value == 'struct'):
            
            if tokenlst[index].value == 'const' and tokenlst[index +1].value == 'struct':
                index += 2
            else:
                index += 1
            #struct id, this id is a struct type
            if index < len(tokenlst) and tokenlst[index].type == 306 :
                index += 1
                #struct id id also work
                if index < len(tokenlst) and tokenlst[index].type == 306 :
                    index += 1
                #struct id  {
                if index < len(tokenlst) and tokenlst[index].value == '{':
                    index += 1
                    #struct id  { }
                    if index < len(tokenlst) and tokenlst[index].value == '}':
                        index += 1
                        if index < len(tokenlst) and tokenlst[index].value == ';':
                            index += 1
                            return True
                        else:
                            print('syntax error, expect "}" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                            return False
                    elif parse_vardec() or parse_strcutdef():
                        while parse_vardec() or parse_strcutdef():
                            continue
                        if index < len(tokenlst) and tokenlst[index].value == '}':
                            index += 1
                            if index < len(tokenlst) and tokenlst[index].value == ';':
                                index += 1
                                return True
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
                    return True
                
                else:
                    #print('syntax error, expect "}" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect identifier in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        else:
            #not struct
            return False
    return True
#'vardec':[['const','typename','idents',';'],['typename','const','idents',';'],['typename','idents',';']],
def parse_vardec():
    global index
    global tokenlst
    while index < len(tokenlst) :
        
        #const type or type const + idents + ;
        if index < len(tokenlst) - 2 and ((tokenlst[index].value == 'const' and tokenlst[index+1].type == 301) or \
            (tokenlst[index+1].value == 'const' and tokenlst[index].type == 301)):
            index += 2
            if parse_idents():
                if index < len(tokenlst) and tokenlst[index].value == ';':
                    #print('vardec in line', tokenlst[index].lineno)
                    index += 1
                    
                    return True
                elif index < len(tokenlst)  and tokenlst[index].value == '{' or tokenlst[index].value == '(':
                    #index -= 2
                    # const type id ( or {
                    index -= 3
                    return parse_funcdec()
                else:
                    print('syntax error, expect ; in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect idents in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        
        #type + idents + ;
        elif tokenlst[index].type == 301:
            index += 1
            if parse_idents():
                if index < len(tokenlst) and tokenlst[index].value == ';':
                    #print('vardec in line', tokenlst[index].lineno)
                    index += 1
                    
                    return True
                elif tokenlst[index].value == '{' or tokenlst[index].value == '(':
                    #index -= 1
                    index -= 2
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
    return True
    

#indents,'id':306, ',':44,   '[':91, ']':93, 'int_lit':303,
#'idents':[['id'],['id','[','int_val',']'], ['id','[','int_val',']',',','idents'],['id',',','idents']],



def parse_ident():
    global index
    global tokenlst
    while index < len(tokenlst):
        # id + [ ]  continue parse_idents
        if index < len(tokenlst) -3 and tokenlst[index].type == 306 and tokenlst[index+1].type == 91 and tokenlst[index + 2].type == 93:
            index += 3
            return True
        # id + [int_val ]  continue parse_idents
        elif index < len(tokenlst) -4 and tokenlst[index].type == 306 and tokenlst[index+1].type == 91 and tokenlst[index + 2].type == 303 and tokenlst[index + 3].type == 93:
            index += 4
            return True
        elif tokenlst[index].type == 306:
            index += 1
            return True
        else :
            print('syntax error, expect ident in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    #end of file, true
    return True
    

#   'char_lit':302,
#   'int':303,
#   'real':304,
#   'str_lit':305,
#vardec include init
def parse_idents():
    global index
    global tokenlst
    while index < len(tokenlst):
        if parse_ident():
            # , = 44
            if index < len(tokenlst) and tokenlst[index].type == 44:
                index += 1
                return parse_idents()
            #ident initlize
            elif index < len(tokenlst) and tokenlst[index].value == '=':
                index += 1
                # init with expr value, = expr value, include constval
                if index < len(tokenlst):
                    if parse_expr():
                        return True
                '''
                #this is only for init with constval
                if index < len(tokenlst) and  tokenlst[index].type == 302 or tokenlst[index].type == 303 or tokenlst[index].type == 304 or tokenlst[index].type == 305:
                    index += 1
                    return True
                '''
                
            else:
                return True
    return True

        

#     'id':306, ',':44,   '[':91, ']':93, 'int_lit':303, type 301, const 401, { 123,  }125
#    'funcprototype':[['funcdec',';']],
#    'funcdec':[['typename','id','(',')'],['typename','id','(','params',')']],[['typename','const','id','(',')'],['const','typename','id','(','params',')']]
#    'param':[['typename','id'], ['typename','id','[',']']],
#    'params':[['param',',','params'], ['param']],
#    'funcdef':[['funcdec','{','}'], ['funcdec','{','vardecs','stmts','}'], ['funcdec','{','vardecs','}'], ['funcdec','{','stmts','}']],
#    'funcbody':[['{','}'], ['{','vardecs','stmts','}'], ['{','vardecs','}'], ['{','stmts','}']],
#     funcdef = funcdec + funcbody, no funcdef, divide it to two parts
def parse_funcdec():
    global index
    global tokenlst
    # have trouble to exactly pos the error with all conditions in one line
    while index < len(tokenlst):
        # const typename id (, or typename const id (
        if index < len(tokenlst) -5 and ((tokenlst[index].type == 401 and tokenlst[index + 1].type == 301 and tokenlst[index + 2].type == 306 and tokenlst[index+3].value == '(')\
            or (tokenlst[index].type == 301 and tokenlst[index + 1].type == 401 and tokenlst[index + 2].type == 306 and tokenlst[index+3].value == '(')):
            #
            if tokenlst[index+4].value == ')':
                index += 5
                return True
            else:
                index += 4
                if parse_params():
                    if tokenlst[index].value == ')':
                        index+=1
                        return True
                    else:
                        print('syntax error in funcdec, expect ) in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)  
                        return False
                else:
                    print('syntax error in funcdec, expect params in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False

       # typename id (
        elif index < len(tokenlst) -4 and tokenlst[index].type == 301 and tokenlst[index + 1].type == 306 and tokenlst[index+2].value == '(':
            #
            if tokenlst[index+3].value == ')':
                index += 4
                return True
            else:
                index += 3
                if parse_params():
                    if tokenlst[index].value == ')':
                        index+=1
                        return True
                    else:
                        print('syntax error in funcdec, expect ) in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)  
                        return False
                else:
                    print('syntax error in funcdec, expect params in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
        else:
            return False
    print('end of file')    
    exit
    return True     

#    'funcbody':[['{','}'], ['{','vardecs','stmts','}'], ['{','vardecs','}'], ['{','stmts','}']],
#    'stmt':[[';'], ['expr',';'], ['break',';'], ['continue',';'], ['return',';'], ['return','expr',';'], ['ifstmt'],['forstmt'],
#    ['whilestmt'],['dowhilestmt']],

#countf = 0

def parse_funcbody():
    global countf
    global index
    global tokenlst
    while index < len(tokenlst):
        if tokenlst[index].value == '{':
            index += 1
            #{ }
            if tokenlst[index].value == '}':
                index += 1
                return True
            elif parse_vardec() or parse_stmts():
                    while  parse_vardec() or parse_stmts() :
                        if tokenlst[index].value == '}':
                            #print('funcbody } in ',tokenlst[index].lineno )
                            index += 1
                            #countf += 1
                            #print('countf',countf)
                            return True
                    if tokenlst[index].value == '}':
                        #print('11111funcbody } in ',tokenlst[index].lineno )
                        index += 1
                        #countf += 1
                        #print('countf',countf)
                        return True
                    else:
                        #print('syntax error, expect } in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                        return False
            else:
                print('syntax error, expect vardec or stmts in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
            
        else:
            #print('syntax error, expect { in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    #end of file
    return True
                    
#    'stmt':[[';'], ['expr',';'], ['break',';'], ['continue',';'], ['return',';'], ['return','expr',';'], ['ifstmt'],['forstmt'],
#    ['whilestmt'],['dowhilestmt']],
def parse_stmt():
    global index
    global tokenlst
    while index < len(tokenlst):
        # ;
        if tokenlst[index].value == ';':
            index += 1
            return True
        # break ;
        elif index < len(tokenlst) - 1 and tokenlst[index].value == 'break' and tokenlst[index+1].value == ';':
            index += 2
            return True
        # continue ;
        elif index < len(tokenlst) - 1 and tokenlst[index].value == 'continue' and tokenlst[index+1].value == ';':
            index += 2
            return True
        #return ;
        elif index < len(tokenlst) - 1 and tokenlst[index].value == 'return' and tokenlst[index+1].value == ';':
            index += 2
            #print('test return ;',tokenlst[index].value)
            return True
        # if 
        elif tokenlst[index].value == 'if':
            return parse_ifstmt()
            #    return True
            #else:
            #    print('syntax error in if stmts in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            #    return False
        #for 
        elif tokenlst[index].value == 'for':
            return parse_forstmt()
            #    return True   
            #else:
            #    print('syntax error in for stmts in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            #    return False
        #while
        elif tokenlst[index].value == 'while':
            return parse_whilestmt()
            #    return True   
            #else:
            #    print('syntax error in while stmts in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            #    return False
        # do while
        elif tokenlst[index].value == 'do':
            return parse_dowhilestmt()
            #    return True   
            #else:
            #    print('syntax error in dowhile stmts in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            #    return False
        #return expr ;
        elif tokenlst[index].value == 'return':
            #print('11111111111111111111111111111111111111111111111test return ',tokenlst[index].value)
            #print(tokenlst[index].lineno, 'lineno and index ', index)
            index += 1
            if parse_expr():
                if tokenlst[index].value == ';':
                    index += 1
                    return True
                else:
                    print('syntax error, expect ";" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        #expr ; 
        elif parse_expr():
            if tokenlst[index].value == ';':
                index += 1
                return True
            else:
                print('syntax error, expect ";" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False   
        else:
            #not stmt
            return False         
    return True

#    'stmts':[['stmt','stmts'], ['stmt']],
def parse_stmts():
    global index
    global tokenlst
    while index < len(tokenlst):
        if parse_stmt():
            
            while parse_stmt():
                continue
            return True
        else:
            #print('111syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    return True
#stmtblock':[['{','}'], ['{','stmts','}']],
def parse_stmtblock():
    global index
    global tokenlst
    while index < len(tokenlst):
        if tokenlst[index].value == '{':
            #print('stmtblock { in ',tokenlst[index].lineno,' with value ', tokenlst[index].value )
            index += 1
            if index < len(tokenlst) and tokenlst[index].value == '}':
                #print('stmtblock } in ',tokenlst[index].lineno ,' with value ', tokenlst[index].value )
                #print('stmtblock } in ',tokenlst[index].lineno )
                index += 1
                return True

            elif parse_stmts():
                if index < len(tokenlst) and tokenlst[index].value == '}':
                    index += 1
                    #print('2222222stmtblock } in ',tokenlst[index].lineno,' with value ', tokenlst[index].value  )
                    #index += 1
                    return True
                else:
                    print('syntax error, expect } in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect } or statements in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        else:
            return False
    return True
#expr     
def parse_expr():
    global index
    global tokenlst
    #basic 
    #constval
    while index < len(tokenlst):
        if parse_expr1():
            if parse_expr2():
                return True
            #no expr2
            return True
        else:
            return False
    return True


#'expr': [['constval'],['id','(','exprlst',')'], ['lval'], ['lval','assignoperator','expr'], ['++','lval'], ['lval','++'], 
# ['--','lval'], ['lval','--'], ['uoperator','expr'], ['expr','bioperator','expr'], ['expr','?','expr',':','expr'],['(','typename',')','expr'], ['(','expr',')']],
def parse_expr1():
    global index
    global tokenlst
    #basic 
    #constval
    while index < len(tokenlst):
        #constval,    'char_lit':302, 'int_lit':303, 'real_lit':304,'str_lit':305,
        if tokenlst[index].type == 302 or tokenlst[index].type == 303 or tokenlst[index].type == 304 or tokenlst[index].type == 305:
            index +=1
            if parse_expr2():
                return True
            else:
                return True
        # id','(','exprlst',')'
        #id
        elif tokenlst[index].type == 306 and tokenlst[index + 1].value == '(':
            index += 2
            # id ( )
            if index < len(tokenlst) and tokenlst[index].value == ')':
                index += 1
                return True
            #id ( exprlst
            elif parse_exprlst():
                #id ( exprlst )
                if index < len(tokenlst) and tokenlst[index].value == ')':
                    index += 1
                    return True
                else:
                    print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect ")" or exprlst in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False

        #++ or -- or uoperator
        elif tokenlst[index].value == '++' or tokenlst[index].value == '--' or tokenlst[index].value == '-' or tokenlst[index].value == '!' or tokenlst[index].value == '~':
            index += 1
            if parse_lval():
                return True
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
                index += 1
                #( typename )
                if  index < len(tokenlst) and tokenlst[index].value == ')':
                    index += 1
                    if parse_expr():
                        return True
                    else:
                        print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                else:
                    print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            # ( expr         
            elif parse_expr():
                # ( expr )
                if index < len(tokenlst) and tokenlst[index].value == ')':
                    index += 1
                    return True
                else:
                    print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect expr or typename in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        #['lval','assignoperator','expr']
        #lval, lval ++, lval --, 
        elif tokenlst[index].type == 306 and parse_lval():
            if index < len(tokenlst) and (tokenlst[index].value == '++' or tokenlst[index].value == '--'):
                index += 1
                return True
            #'assignoperator':[['='], ['+='], ['-='], ['*='], ['/=']],
            #lval assignmentoperator expr
            elif index < len(tokenlst) and (tokenlst[index].value == '+=' or tokenlst[index].value == '-=' or tokenlst[index].value == '*=' or tokenlst[index].value == '/=' or  tokenlst[index].value == '='):
                index += 1 
                if parse_expr():
                    return True
                else:
                    print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                #only lval also true
                return True
        else:
            # not expr
            return False
    return True

def parse_expr2():
    global index
    global tokenlst
    #basic 
    #constval
    while index < len(tokenlst):
            # ['expr','bioperator','expr'], ['expr','?','expr',':','expr']
        #expr bioperator expr ,left recursion,套娃，change to bioperator expr
        #elif parse_expr() and (parse_bioperator() or tokenlst[index].value == '?'):
        if parse_bioperator():
            if parse_expr1():
                return True
            else:
                print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
        elif tokenlst[index].value == '?':
            index += 1
            if parse_expr1():
                if index < len(tokenlst) and tokenlst[index].value == ':':
                    index += 1
                    if parse_expr1():
                        return True
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
    return True
#'expr': [['constval'],['id','(','exprlst',')'], ['lval'], ['lval','assignoperator','expr'], ['++','lval'], ['lval','++'], 
# ['--','lval'], ['lval','--'], ['uoperator','expr'], ['expr','bioperator','expr'], ['expr','?','expr',':','expr'],['(','typename',')','expr'], ['(','expr',')']],
""" def parse_expr():
    global index
    global tokenlst
    #basic 
    #constval
    while index < len(tokenlst):
        #constval,    'char_lit':302, 'int_lit':303, 'real_lit':304,'str_lit':305,
        if tokenlst[index].type == 302 or tokenlst[index].type == 303 or tokenlst[index].type == 304 or tokenlst[index].type == 305:
            index +=1
            return True
        # id','(','exprlst',')'
        elif index < len(tokenlst) - 1 and tokenlst[index].type == 306 and tokenlst[index+1].value == '(':
            index += 2
            #id','(',')'
            if tokenlst[index].value == ')':
                index += 1
                return True
            #id','(','exprlst',')'
            elif parse_exprlst():
                if tokenlst[index].value == ')':
                    index += 1
                    return True
            else:
                print('syntax error, expect ) or exprlst in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        
        
        #++ or -- or uoperator
        elif tokenlst[index].value == '++' or tokenlst[index].value == '--' or tokenlst[index].value == '-' or tokenlst[index].value == '!' or tokenlst[index].value == '~':
            index += 1
            if parse_lval():
                return True
            else:
                print('syntax error, expect lval in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False
        #['(','typename',')','expr'], ['(','expr',')']],
        elif tokenlst[index].value == '(':
            index += 1
            # type 301
            if index < len(tokenlst) -1 and tokenlst[index].type == 301 and tokenlst[index+1].value == ')':
                return True
            elif parse_expr():
                if index < len(tokenlst) and tokenlst[index].value == ')':
                    index += 1
                    return True
                else:
                    print('syntax error, expect ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                print('syntax error, expect expr or typename in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                return False

        #lval, lval ++, lval --, 
        elif parse_lval():
            if tokenlst[index].value == '++' or tokenlst[index].value == '--':
                index += 1
                return True
            #'assignoperator':[['='], ['+='], ['-='], ['*='], ['/=']],
            #lval assignmentoperator expr
            elif tokenlst[index].value == '+=' or tokenlst[index].value == '-=' or tokenlst[index].value == '*=' or tokenlst[index].value == '/=' or  tokenlst[index].value == '=':
                index += 1 
                if parse_expr():
                    return True
                else:
                    print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            else:
                return True
        # ['expr','bioperator','expr'], ['expr','?','expr',':','expr']
        elif parse_expr():
            if parse_bioperator():
                if parse_expr():
                    return True
                else:
                    print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            elif tokenlst[index].value == '?':
                index += 1
                if parse_expr():
                    if tokenlst[index].value == ':':
                        index += 1
                        if parse_expr():
                            return True
                        else:
                            print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                            return False
                    else:
                        print('syntax error, expect ":" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                        return False
                else:
                    print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
        else:
            print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    return True
 """

#'bioperator':[['=='],['!='],['>'],['>='],['<'],['<='],['+'],['-'],['*'],['/'],['%'],['|'],['&'],['||'],['&&']],
""" def parse_bioperator():
    global index
    global tokenlst
    if index >= len(tokenlst):
        return True
    if tokenlst[index].value == '==' or tokenlst[index].value == '!=' or tokenlst[index].value == '>' or tokenlst[index].value == '>=' or \
        tokenlst[index].value == '<' or tokenlst[index].value == '<=' or tokenlst[index].value == '+' or tokenlst[index].value == '-' or \
            tokenlst[index].value == '*' or tokenlst[index].value == '/' or tokenlst[index].value == '%' or tokenlst[index].value == '|' or \
                tokenlst[index].value == '&' or tokenlst[index].value == '||' or tokenlst[index].value == '&&':
                index += 1
                return True
    else:
        print('syntax error, expect bi operator in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
        return False 
"""
#'ifstmt':[['if','(','expr',')','stmt'], ['if','(','expr',')','stmtblock'], ['if','(','expr',')','stmt','else','stmt'],\
#              ['if','(','expr',')','stmt','else','stmtblock'], ['if','(','expr',')','stmtblock','else','stmt'],
#               ['if','(','expr',')','stmtblock','else','stmtblock']],
def parse_ifstmt():
    global index
    global tokenlst
    while index < len(tokenlst):
        if tokenlst[index].value == 'if':
            index += 1
            if index < len(tokenlst) and tokenlst[index].value == '(':
                index += 1
                if parse_expr():
                    if index < len(tokenlst) and tokenlst[index].value == ')':
                        index += 1
                        if parse_stmt():
                            if tokenlst[index].value == 'else':
                                index += 1
                                if parse_stmt():
                                    return True
                                elif parse_stmtblock():
                                    return True
                                else:
                                    print('syntax error, expect stmt or stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            else:
                                return True   
                        elif parse_stmtblock():
                            if tokenlst[index].value == 'else':
                                index += 1
                                if parse_stmt():
                                    return True
                                elif parse_stmtblock():
                                    return True
                                else:
                                    print('syntax error, expect stmt or stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            else:
                                return True
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
    return True

#'forstmt':[['for','(','optexpr',';','optexpr',';','optexpr',')','stmtblock'], ['for','(','optexpr',';','optexpr',';','optexpr',')','stmt']],
def parse_forstmt():
    global index
    global tokenlst
    while index < len(tokenlst):
        if tokenlst[index].value == 'for':
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
                                    return True
                                else:
                                    print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            elif parse_stmt():
                                return True
                            else:
                                print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                return False
                        elif parse_expr():
                            if index < len(tokenlst) and tokenlst[index].value == ')':
                                index += 1
                                if index < len(tokenlst) and tokenlst[index].value == '{':
                                    if parse_stmtblock():
                                        return True
                                    else:
                                        print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                        return False
                                elif parse_stmt():
                                    return True
                                else:
                                    print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                        else:
                            print('syntax error, expect expr or ")" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                            return False
                    
                    # expr ; ) stmtblock or stmt
                    # expr ; expr ) stmtblock or stmt
                    elif parse_expr():
                        if index < len(tokenlst) and tokenlst[index].value == ';':
                            index += 1
                            if index < len(tokenlst) and tokenlst[index].value == ')':
                                index += 1
                                if index < len(tokenlst) and tokenlst[index].value == '{':
                                    if parse_stmtblock():
                                        return True
                                    else:
                                        print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                        return False
                                elif parse_stmt():
                                    return True
                                else:
                                    print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            elif parse_expr():
                                if index < len(tokenlst) and tokenlst[index].value == ')':
                                    index += 1
                                    if index < len(tokenlst) and tokenlst[index].value == '{':
                                        if parse_stmtblock():
                                            return True
                                        else:
                                            print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                            return False
                                    elif parse_stmt():
                                        return True
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
                    if index < len(tokenlst) and tokenlst[index].value == ';':
                        index += 1
                        if index < len(tokenlst) and tokenlst[index].value == ';':
                            index += 1
                            if index < len(tokenlst) and tokenlst[index].value == ')':
                                index += 1
                                if index < len(tokenlst) and tokenlst[index].value == '{':
                                    if parse_stmtblock:
                                        return True
                                    else:
                                        print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                        return False
                                elif parse_stmt():
                                    return True
                                else:
                                    print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                    return False
                            elif parse_expr():
                                if index < len(tokenlst) and tokenlst[index].value == ')':
                                    index += 1
                                    if index < len(tokenlst) and tokenlst[index].value == '{':
                                        if parse_stmtblock():
                                            return True
                                        else:
                                            print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                            return False
                                    elif parse_stmt():
                                        return True
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
                            if index < len(tokenlst) and tokenlst[index].value == ';':
                                index += 1
                                if index < len(tokenlst) and tokenlst[index].value == ')':
                                    index += 1
                                    if index < len(tokenlst) and tokenlst[index].value == '{':
                                        if parse_stmtblock:
                                            return True
                                        else:
                                            print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                            return False
                                    elif parse_stmt():
                                        return True
                                    else:
                                        print('syntax error, expect stmt in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                        return False
                                elif parse_expr():
                                    if index < len(tokenlst) and tokenlst[index].value == ')':
                                        index += 1
                                        if index < len(tokenlst) and tokenlst[index].value == '{':
                                            if parse_stmtblock():
                                                return True
                                            else:
                                                print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                                return False
                                        elif parse_stmt():
                                            return True
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
    return True
#'whilestmt':[['while','(','expr',')','stmtblock'],['while','(','expr',')','stmt']],
def parse_whilestmt():
    global index
    global tokenlst
    while index < len(tokenlst):
        if tokenlst[index].value == 'while':
            #print('whilestmt in ',tokenlst[index].lineno )
            index += 1
            if index < len(tokenlst) and tokenlst[index].value == '(':
                index += 1
                if parse_expr():
                    if index < len(tokenlst) and tokenlst[index].value == ')':
                        index += 1
                        if index < len(tokenlst) and tokenlst[index].value == '{':
                            #print('whilestmt block { in line ', tokenlst[index].lineno)
                            if parse_stmtblock():
                                return True
                            else:
                                #print('syntax error, expect stmtblock in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
                                return False
                        elif parse_stmt():
                            return True
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
    return True
# 'dowhile':[['do','stmt','while','(','expr',')',';'], ['do','stmtblock','while','(','expr',')',';']],    
def parse_dowhilestmt():
    global index
    global tokenlst
    while index < len(tokenlst):
        if tokenlst[index].value == 'do':
            index += 1
            if index < len(tokenlst) and tokenlst[index].value == '{':
                if parse_stmtblock():
                    if index < len(tokenlst) and tokenlst[index].value == 'while':
                        index += 1
                        if index < len(tokenlst) and tokenlst[index].value == '(':
                            if parse_expr():
                                if index < len(tokenlst) and tokenlst[index].value == ')':
                                    index += 1
                                    if index < len(tokenlst) and tokenlst[index].value == ';':
                                        index += 1
                                        return True
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
                if index < len(tokenlst) and tokenlst[index].value == 'while':
                    index += 1
                    if index < len(tokenlst) and tokenlst[index].value == '(':
                        if parse_expr():
                            if index < len(tokenlst) and tokenlst[index].value == ')':
                                index += 1
                                if index < len(tokenlst) and tokenlst[index].value == ';':
                                    index += 1
                                    return True
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
    return True
#    'exprlst':[['expr'], ['expr',',','exprlst']],

#    'uoperator':[['-'], ['!'], ['~']],

#    'lval':[['id'], ['id','(','expr',')'], ['lval','.','id'], ['lval','.','id','(','expr',')']]
def parse_exprlst():
    global index
    global tokenlst
    while index < len(tokenlst):
        if not parse_expr():
            print('syntax error, expect expr in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
        else:
            if tokenlst[index].value == ',':
                index += 1
                return parse_exprlst()
            else:
                return True
    return True
#    'assignoperator':[['='], ['+='], ['-='], ['*='], ['/=']],
def parse_assignoperator():
    global index
    global tokenlst
    while index < len(tokenlst):
        if tokenlst[index].value == '=' or tokenlst[index].value == '+=' or tokenlst[index].value == '-=' or tokenlst[index].value == '*=' or tokenlst[index].value == '/=':
            index += 1
            return True
        else:
            print('syntax error, expect assignoperator in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    return True

#    'uoperator':[['-'], ['!'], ['~']],
def parse_uoperator():
    global index
    global tokenlst
    while index < len(tokenlst):
        if tokenlst[index].value == '-' or tokenlst[index].value == '!' or tokenlst[index].value == '~' :
            index += 1
            return True
        else:
            print('syntax error, expect uoperator in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    return True
#    'bioperator':[['=='],['!='],['>'],['>='],['<'],['<='],['+'],['-'],['*'],['/'],['%'],['|'],['&'],['||'],['&&']],
bioperatorlst = ['==','!=','>','>=','<','<=','+','-','*','/','%','|','&','||','&&']
def parse_bioperator():
    global index
    global tokenlst
    while index < len(tokenlst):
        if tokenlst[index].value in bioperatorlst:
            index += 1
            return True
        else:
            #print('syntax error, expect bioperator in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value)
            return False
    return True 
#'lval':[['id'], ['id','[','expr',']'], ['lval','.','id'], ['lval','.','id','[','expr',']']], left recursion, elimilate left recursion
##'lval':[['id'], ['id','[','expr',']'], ['id','.','lval'], left recursion, elimilate left recursion
#'id':306, ',':44,   '[':91, ']':93, 'int_lit':303, type 301, const 401, { 123,  }125
def parse_lval():
    global index
    global tokenlst
    while index < len(tokenlst):
        #print(index, 'tokenvalue is', tokenlst[index].value)
        # id 
        if tokenlst[index].type == 306:
            #print("lval index is ", tokenlst[index].value, ' with token num ',index, ' in line ', tokenlst[index].lineno)
            index += 1
            
            # id (
            if index < len(tokenlst) and tokenlst[index].value == '[':
                index += 1
                if parse_expr():
                    if index < len(tokenlst) and tokenlst[index].value == ']':
                        index += 1
                        if index < len(tokenlst) and tokenlst[index].value == '.':
                            return parse_lval()
                        else:
                            # not . , lval finished
                            return True
                    else:
                        print('syntax error, expect ) in lval, in line ', tokenlst[index].lineno, ' near ', tokenlst[index].value)
                        return False
                else:
                    print('syntax error, expect expr in lval, in line ', tokenlst[index].lineno, ' near ', tokenlst[index].value)
                    return False
            # id .
            elif index < len(tokenlst) and tokenlst[index].value == '.':
                index += 1
                return parse_lval()
            # just id
            else:
                return True
        # no id, not lval
        else:
            return False

    return True

#'id':306, ',':44,   '[':91, ']':93, 'int_lit':303, type 301, const 401, { 123,  }125
#'param':[['typename','id'], ['typename','id','[',']']],
#'params':[['param',',','params'], ['param']],
def parse_parm():
    global index
    global tokenlst
    while index < len(tokenlst):
        #typename 
        if index < len(tokenlst) and tokenlst[index].type == 301:
            index += 1
            #typename id
            if index < len(tokenlst) and tokenlst[index].type == 306:
                index += 1
                #typename id [
                if index < len(tokenlst) and tokenlst[index].value == '[':
                    index += 1
                    #typename id [ ]
                    if index < len(tokenlst) and tokenlst[index].value == ']':
                        index += 1
                        return True
                    else:
                        print('syntax error, expect "]" in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value) 
                        return False
                #just type id
                else:
                    return True
            else:
                print('syntax error, expect identifier in line ',tokenlst[index].lineno, ' near ', tokenlst[index].value) 
                return False
        else:
            # not type id, not param
            return False
    return True

def parse_params():
    global index
    global tokenlst
    if parse_parm():
        if index < len(tokenlst) and tokenlst[index].value == ',':
            index += 1
            return parse_params()
        else:
            #param
            return True
    else:
        # not params
        return False

parse_program()        

'''
if __name__ == '__main__':
    #fname = 'tricky.c'
    #fname = 'test.c'
    fname = 'test1_part3.c'
    #lst = Lexer(fname).getToken(get_word(fname))
    tokenlst  = []
    lexer1.get_word(fname,tokenlst)


    #print(len(tokenlst))
    parse_program()
'''



