# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:03:26 2022

@author: Administrator
"""


# grammer

program -> declarationList
declarationList -> declarationList declaration \ declaration
declaration -> varDec \ functionDeclaration \ includeStatement

# Variable Declarations

varDec -> typeSpecifier ID = expression ; \ typeSpecifier ID ;
assignment -> exprAssignment \ incEqualAssignment \ decEqualAssignment \ incAssignment \ decAssignment \ multEqualAssignment \ divEqualAssignment
exprAssignment -> ID = expression ;
incEqualAssignment -> ID += expression ;
decEqualAssignment -> ID -= expression ;
multEqualAssignment -> ID *= expression ;
divEqualAssignment -> ID /= expression ;
incAssignment -> ID ++ ;
decAssignment -> ID -- ;

# Function Declarations

functionDeclaration -> typeSpecifier ID ( argList ) { statementList }
argList -> argList , arg \ arg \ EMPTY
arg -> typeSpecifier ID \ typeSpecifier

# Other Declarations

labelDeclaration -> label : statementListNew
statementListNew -> statementListNew statementNew \ statementNew
statementNew -> varDec \ returnStatement \ ifStatement \ assignment \ includeStatement \ forStatement \ whileStatement \ callStatement ; \ gotoStatement \ breakStatement \ continueStatement \ switchStatement \ enumStatement \ structStatement

# Statements

statementList -> statementList statement \ statement
statement -> varDec \ returnStatement \ ifStatement \ assignment \ includeStatement \ forStatement \ whileStatement \ callStatement ; \ gotoStatement \ labelDeclaration \ breakStatement \ continueStatement \ switchStatement \ enumStatement \ structStatement
breakStatement -> break ;
continueStatement -> continue ;
returnStatement -> return expression ;
includeStatement -> fileName
callStatement -> ID ( paramList )
gotoStatement -> goto ID ;
paramList -> paramList , param \ param \ EMPTY
param -> constNum \ ID \ str
enumStatement -> specialTypeSpecifier ID { enumList } ; \ specialTypeSpecifier ID ID ;
enumList -> enumList , ID \ ID
structStatement -> specialTypeSpecifier ID { structList } ;
structList -> structList , structDec \ structDec
structDec -> typeSpecifier varList
varList -> varList , ID \ ID

switchStatement -> switch ( switchCondition ) { caseList }
switchCondition -> expression
caseList -> caseList switchCase \ switchCase \ EMPTY
switchCase -> case constNum : { statementList }

# Control Flow

ifStatement -> if ( condition ) { ifBody } \ if ( condition ) { ifBody } elseStatement
ifBody -> statementList
condition -> expression
elseStatement -> else { statementList }
forStatement -> for ( assignment expression ; ID ++ ) { statementList }
whileStatement -> while ( whileCondition ) { statementList }
whileCondition -> expression

# Expressions

expression -> a

# Boolean operations
a -> boolAnd \ boolOr \ c

boolAnd -> c && a
boolOr -> c || a

c -> boolNot \ d
boolNot -> ! d

# Comparisons
d -> lteExpr \ gteExpr \ ltExpr \ gtExpr \ neExpr \ eExpr \ e
lteExpr -> e <= d
gteExpr -> e >= d
ltExpr -> e < d
gtExpr -> e > d
neExpr -> e != d
eExpr -> e == d

# Multiplication and addition
e -> addExpr \ subExpr \ f
addExpr -> f + e
subExpr -> f - e

f -> multExpr \ divExpr \ modExpr \ g
multExpr -> g * f
divExpr -> g / f
modExpr -> g % f

g -> bitAnd \ bitOr \ bitXor \ bitNot \ leftShift \ rightShift \ h
bitAnd -> h & g
bitOr -> h | g
bitXor -> h ^ g
bitNot -> ~ h
leftShift -> h << g
rightShift -> h >> g

# Immutables
h -> constNum \ ID \ str \ callStatement \ nestedExpr
nestedExpr -> ( expression )