import sys
import lexer1
from lexer1 import get_word
#from parser4 import parse_program

n = len(sys.argv)
#python3 mycc -n testfile
#sys.argv[0] = 'mycc', sys.argv[1] = -n, sys.argv[2] = testfile
#lexer
if n < 3:
    print('please input argv and testfile')
    sys.exit()
def infile():
    if n < 3:
        print('please input argv and testfile')
        sys.exit()
    else:
        return sys.argv[2]
if sys.argv[1] == '-1':
    tokenlst  = []
    fname = sys.argv[2]
    get_word(fname,tokenlst)

elif sys.argv[1] == '-3':
    #parse_program()
    print('parse')

elif sys.argv[1] == '-4':
    print('typechecking')

elif sys.argv[1] == '-2':
    print('not done yet')

elif sys.argv[1] == '-5':
    print('not done yet')

elif sys.argv[1] == '-6':
    print('not done yet')
else:
    print('no this part')