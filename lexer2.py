# -*- coding: utf-8 -*-


#import re
import sys, os
sys.path.append(os.pardir)  


token_type = {
    '!':33,
    '%':37,
    '&':38,
    '(':40,
    ')':41,
    '*':42,
    '+':43,
    ',':44,
    '-':45,
    '.':46,
    '/':47,
    ':':58,
    ';':59,
    '<':61,
    '=':61,
    '>':62,
    '?':63,
    '[':91,
    ']':93,
    '{':123,
    '}':125,
    '|':124,
    '~':126,
    '==':351,
    '!=':352,
    '>=':353,
    '<=':354,
    '++':355,
    '--':356,
    '||':357,
    '&&':358,
    '+=':361,
    '-=':362,
    '*=':363,
    '/=':364,
    'const':401,
    'struct':402,
    'for':403,
    'while':404,
    'do':405,
    'if':406,
    'else':407,
    'break':408,
    'continue':409,
    'return':410,
    'switch':411,
    'case':412,
    'default':413,
    'type':301, #void, char, int, float
    #'void':301,
    #'char':301,
    #'int':301,
    #'float':301,
    'char_lit':302,
    'int':303,
    'real':304,
    'str_lit':305,
    'id':306
}
'''
# 运算符表
y_list = {'+','-','*','/','<','<=','>','>=','=','==','!=','+=','-=','*=','/=','%','&','&&','|','||','!','++','--'}
# 分隔符表
f_list = {';','(',')','[',']','{','}', '.',':','\"','\'','\\','?',','}
# 关键字表
k_list = {'const','struct','for','while','do','if','else','break','continue','return','switch','case','default'}

Cmp = ['<', '>', '==', '!=', '>=', '<=']

Type = {'int','float','char','void'}
'''

onechar_lst = ['+','-','*','/','<','>','=','%','&','|','!',';','(',')','[',']','{','}', '.',':','\"','\'','?',',','~']
key_list = ['const','struct','for','while','do','if','else','break','continue','return','switch','case','default','int','float','char','void']

#length limit of tokens for that type
int_limit = real_limit = id_limit = 48
char_limit = str_limit = 1024

'''
# re
#
#match int, return match value, else rteturn none
#re too slow, change to char by char

def is_int(int_word):
    deci = re.match("^([0-9]+)$",int_word) 
    if deci != None:
        return deci
    octaldeci = re.match("^([0][0-7a-fA-F]*)$",int_word) 
    if octaldeci != None:
        return octaldeci
    hexadeci = re.match("^([0][xX][0-9a-fA-F]*)$",int_word) 
    if hexadeci != None:
        return hexadeci
    return None
    
#match real
def is_real(int_word):
    return re.match("^([0-9]{1,}[.]?[0-9]*[eE]?[+-]?[0-9]+)$",int_word) 

# 判断是否为为变量名
def is_id(int_word):
    return re.match("[a-zA-Z_][a-zA-Z0-9_]*",int_word) != None
'''

#token properities
class Token():
    def __init__(self, value, types, linenum):
        self.value = value
        self.type = types
        self.lineno = linenum
    




#add token
def add(res, t, ty, lineno):
    #self.tokenlist.append({'value':t,'type':ty, 'line': lineno})
    res.append(Token(t,ty,lineno))
    

# print token
def print_log(tokenlst,filename):
    print("File ", filename," Line ",  tokenlst[-1].lineno," Token ",  tokenlst[-1].type," Text ", tokenlst[-1].value)
    #print('check:::')


def get_word(filename,res):
    #res = []
    f = open(filename,'r+',encoding='UTF-8')
    # 
    fp = f.read()

    if (len(fp) == 0):
        #print('File can not be opened\n')
        return
    
    #print(text)
    lineno = 1
    i = 0
    while i < len(fp):
        #string
        if fp[i] == '"':
            sstr = '"'
            i += 1
            # \" still continue, \\" will stop
            while(fp[i] != '"' or (i > 1 and fp[i] == '"' and fp[i-1] == '\\' and fp[i-2] != '\\')):
                sstr += fp[i]
                if fp[i] == '\n':
                    lineno += 1
                #error , end of file and no "
                if i == len(fp):
                    print('Lexer error in file',filename,'  Line ',lineno,' near text ',sstr,' \n \t Unclosed String', filename, lineno, sstr)
                    return 
                i += 1
            #add last "
            sstr += fp[i]
            i += 1
            #check str length
            if len(sstr) > str_limit:
                #print('Lexer waring in file ',filename,'  Line ',lineno,' near text ',sstr,' \n \t Too long String; truncating to ',sstr[:str_limit],'\n \t' )
                #add to token list
                add(res,sstr[:str_limit],token_type['str_lit'], lineno)
                #res.append((sstr[:str_limit],token_type['str_lit'], lineno))
            else:
                add(res,sstr,token_type['str_lit'], lineno)
                #print_log(res,filename)
        #char lit
        elif fp[i] == '\'':
            cstr = '\''
            i += 1
            # 
            while(fp[i] != '\'' ):
                cstr += fp[i]
                if fp[i] == '\n':
                    lineno += 1
                
                #error , end of file and no "
                if i == len(fp):
                    print('Lexer error in file ',filename,'  Line ',lineno,' near text ',cstr,' \n \t Unclosed char String')
                    return 
                i += 1
                        #add last "
            cstr += fp[i]
            i += 1
            #check str length
            if len(cstr) > char_limit:
                #print('Lexer waring in file',filename,'  Line ',lineno,' near text ',cstr,' \n \t Too long char String; truncating to ',cstr[:str_limit],'\n \t' )
                #add to token list
                add(res,cstr[:char_limit],token_type['char_lit'], lineno)
            else:
                add( res,cstr,token_type['char_lit'], lineno)
                #print_log(res,filename)
        
        #  #,ignore this line current               
        elif (fp[i] == '#'):
                while(fp[i] != '\n'):
                    i += 1
                lineno += 1
        # comment, 
        elif (fp[i] == '/'):
            #multiple line comment
            if fp[i + 1] == '*':
                i += 2
                flagpos = i
                while 1:                   
                    if i < len(fp) and  fp[i] == '\n':
                        lineno += 1
                    #comment finished
                    elif i < len(fp) and fp[i] == '/' and fp[i - 1] == '*' and i > flagpos:
                        i += 1
                        break
                    elif i == len(fp):
                        print("Lexer error in file ",filename," line ",lineno,"\n\t Unclosed comment")
                        return

                    i += 1
            # //comment
            elif fp[i+1] == '/':
                i += 1
                while(1):
                    if fp[i] == '\n':
                        lineno += 1
                        i += 1
                        break
                    i += 1
            # /=
            elif fp[i + 1] == '=':
                i += 1
                add(res, '/=',token_type['/='], lineno)
                #print_log(res,filename)
                i += 1
            # just /
            else:
                i += 1
                add( res,'/',token_type['/'], lineno)
                #print_log(res,filename)
        
        #two char operator
        # ==， =
        elif fp[i] == '=':
            i += 1
            if fp[i] == '=':
                i += 1
                add(res, '==',token_type['=='], lineno)
                #print_log(res,filename)
                #print(lineno)
            else:
                add(res, '=',token_type['='], lineno)
                #print_log(res,filename)
                
        # +， +=， ++
        elif fp[i] == '+':
            i += 1
            if fp[i] == '=':
                i += 1
                add(res,'+=',token_type['+='], lineno)
                #print_log(res,filename)
            elif fp[i] == '+':
                i += 1
                add(res, '++',token_type['++'], lineno)
                #print_log(res,filename)
            else:
                add(res,'+',token_type['+'], lineno)
                #print_log(res,filename)
        
        # -， -=， --
        elif fp[i] == '-':
            i += 1
            if fp[i] == '=':
                i += 1
                add(res, '-=',token_type['-='], lineno)
                #print_log(res,filename)
            elif fp[i] == '-':
                i += 1
                add(res,'--',token_type['--'], lineno)
                #print_log(res,filename)
            else:
                add(res,'-',token_type['-'], lineno)
                #print_log(res,filename)
        
        # ！=， ！
        elif fp[i] == '!':
            i += 1
            if fp[i] == '=':
                i += 1
                add( res,'!=',token_type['!='], lineno)
                #print_log(res,filename)
            else:
                add(res,'!',token_type['!'], lineno)
                #print_log(res,filename)
        # >=， >
        elif fp[i] == '>':
            i += 1
            if fp[i] == '=':
                i += 1
                add(res,'>=',token_type['>='], lineno)
                #print_log(res,filename)
            else:
                add(res,'>',token_type['>'], lineno)
                #print_log(res,filename)
         # <=， <
        elif fp[i] == '<':
            i += 1
            if fp[i] == '=':
                i += 1
                add(res,'<=',token_type['<='], lineno)
                #print_log(res,filename)
            else:
                add(res,'<',token_type['<'], lineno)
                #print_log(res,filename)  
        # *=， *
        elif fp[i] == '*':
            i += 1
            if fp[i] == '=':
                i += 1
                add( res,'*=',token_type['*='], lineno)
                #print_log(res,filename)
            else:
                add( res,'*',token_type['*'], lineno)
                #print_log(res,filename)  

        # /=， /
        elif fp[i] == '/':
            i += 1
            if fp[i] == '=':
                i += 1
                add(res,'/=',token_type['/='], lineno)
                #print_log(res,filename)
            else:
                add(res,'/',token_type['/'], lineno)
                #print_log(res,filename)  

        # &&， &
        elif fp[i] == '&':
            i += 1
            if fp[i] == '&':
                i += 1
                add(res,'&&',token_type['&&'], lineno)
                #print_log(res,filename)
            else:
                add(res,'&',token_type['&'], lineno)
                #print_log(res,filename)    
  
        # ||， |
        elif fp[i] == '|':
            i += 1
            if fp[i] == '|':
                i += 1
                add(res,'||',token_type['||'], lineno)
                #print_log(res,filename)
            else:
                add(res,'|',token_type['|'], lineno)
                #print_log(res,filename) 
        
        # one operator
        elif fp[i] in onechar_lst:
            
            add(res,fp[i],token_type[fp[i]], lineno)
            #print_log(res,filename) 
            i += 1
        


                
        #digit
        elif fp[i].isdigit():
            istr = str(fp[i])

            #16
            if fp[i] == '0' and (fp[i+1] == 'x' or fp[i+1]=='X'):
                istr += fp[i+1]
                i += 2
                while fp[i].isdigit() or 'a' <=fp[i] <='f' or 'A'<= fp[i]<='F':
                    istr += fp[i]
                    i += 1
                add(res,istr,token_type['int'], lineno)
                print_log(res,filename)                
            #8
            elif fp[i] == '0' and fp[i+1] != '.':
                i += 1
                
                while '0' <= fp[i] <= '7' or 'a' <=fp[i] <='f' or 'A'<= fp[i]<='F':
                    istr += fp[i]
                    i += 1
                add(res, istr,token_type['int'], lineno)
                #print_log(res,filename) 
            
            #10
            else:
                
                i += 1
                #istr += fp[i]
                
                while i < len(fp) and fp[i].isdigit():
                    #print('fp[i]',fp[i])
                    istr += fp[i]
                    i += 1
                
                #real
                if i < len(fp) and fp[i] == '.' :
                    istr += fp[i]
                    i += 1
                    nume = 0
                    numplus_minus = 0
                    while i < len(fp) and (fp[i].isdigit() or (nume < 1 and  ( fp[i] == 'e' or fp[i] =='E' )) or \
                            (numplus_minus < 1 and (fp[i]=='+' or fp[i] =='-') and (fp[i-1] == 'e' or fp[i-1] =='E'))):
                        istr += fp[i]
                        
                        if fp[i] == 'e' or fp[i] =='E':
                            nume += 1
                        if fp[i]=='+' or fp[i] =='-':
                            numplus_minus += 1
                        i += 1
                    # too long, get first 48
                    if len(istr) > 48:
                        istr = istr[:48]
                        #print('Lexer waring in file',filename,'  Line ',lineno,' near text ',istr,' \n \t Number too long; truncating to ',istr,'\n \t' )
                        add(res,istr,token_type['real'], lineno)
                    else:
                        add(res,istr,token_type['real'], lineno)
                        #print_log(res,filename)                    
                    
                elif i < len(fp) and (fp[i] == 'e' or fp[i] == 'E'):
                    istr += fp[i]
                    i += 1
                    if fp[i] == '+' or fp[i] == '-':
                        istr += fp[i]
                        i += 1 
                    while i < len(fp) and fp[i].isdigit():
                        istr += fp[i]
                        i += 1
                    
                    add( res,istr,token_type['real'], lineno)
                    #print_log(res,filename)   
                else:
                    add( res,istr,token_type['int'], lineno)
                    #print_log(res,filename) 

        #id
        elif fp[i] == '_' or fp[i].isalpha():
                _str = fp[i]
                i += 1
                #print(lineno)
    
                #if fp[i] == '\n':
                 #   lineno += 1
                #print(lineno)
                while not fp[i].isspace():
                    #if fp[i] == '\n':
                        #lineno += 1
                    if not fp[i].isdigit() and not fp[i].isalpha() and not fp[i] == '_':
                        break
                    _str += fp[i]
                    i += 1
                #key
                if _str in key_list:
                    if _str == 'void' or _str == 'int' or _str == 'float' or _str == 'char':
                        
                        add(res, _str, token_type['type'], lineno)
                        #res.append((res, _str, token_type['type'], lineno))
                        #print(res, _str, token_type['type'], lineno)
                        #print(len(res))
                        #print(tokenlst)
                        #print_log(res,filename)
                    else:
                        add(res, _str, token_type[_str], lineno)
                        #print_log(res,filename)
                else:
                    if (len(_str) > id_limit):
    
                        add( res,_str[:id_limit], token_type['id'], lineno)
                        #print('Lexer waring in file',filename,'  Line ',lineno,' near text ',_str,' \n \t Too long identifier; truncating to',_str[:id_limit],' \n \t' )
                    else:
                        #print(lineno)
                        add(res, _str, token_type['id'], lineno)
                        #print_log(res,filename)
                        #print(lineno)
        #space
        elif fp[i].isspace():
                #print('isspace 0',lineno)
                if fp[i] == '\n':
                    lineno += 1
                i += 1
                #print('sispace hou',lineno)
        elif i >= len(fp):
                return
        else:
                print("Lexer error in file",filename," line ",lineno," near text ",fp[i]," \n\t Ignore unexpected symbol:", fp[i]);
                i += 1
    #print(len(res))
    #return res
        
class Lexer():
    def __init__(self, filename = 'test.c'):
        self.tokenlst = []
        self.filename = filename    
    
    
    def getToken(self, tokenlst):
        
        for t in tokenlst:
            #print(t.values, t.types,t.linenum)
            self.tokenlst.append(t)
        
        


if __name__ == '__main__':
    fname = 'tricky.c'
    fname = 'test.c'
    
    tokenlst  = []
    get_word(fname,tokenlst)
    #lst = Lexer(fname).getToken(get_word(fname,tokenlst))
    #get_word(fname,tokenlst)
'''
    get_word(fname,tokenlst)
    
    for t in tokenlst:
        print(t.value, t.type,t.lineno)
    print('9th value is ',tokenlst[9].value)
    print(len(tokenlst))
    #print(len(tokenlst))

'''


    
