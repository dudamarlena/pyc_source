# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/ply_test.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 2312 bytes
tokens = ('NAME', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'LPAREN',
          'RPAREN')
t_PLUS = '\\+'
t_MINUS = '-'
t_TIMES = '\\*'
t_DIVIDE = '/'
t_EQUALS = '='
t_LPAREN = '\\('
t_RPAREN = '\\)'
t_NAME = '[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r"""\d+"""
    try:
        t.value = int(t.value)
    except ValueError:
        print('Integer value too large %d', t.value)
        t.value = 0

    return t


t_ignore = ' \t'

def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count('\n')


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex
lexer = lex.lex()
precedence = (('left', 'PLUS', 'MINUS'), ('left', 'TIMES', 'DIVIDE'), ('right', 'UMINUS'))
names = {}

def p_statement_assign(t):
    """statement : NAME EQUALS expression"""
    names[t[1]] = t[3]


def p_statement_expr(t):
    """statement : expression"""
    print(t[1])


def p_expression_binop(t):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression"""
    if t[2] == '+':
        t[0] = t[1] + t[3]
    else:
        if t[2] == '-':
            t[0] = t[1] - t[3]
        else:
            if t[2] == '*':
                t[0] = t[1] * t[3]
            elif t[2] == '/':
                t[0] = t[1] / t[3]


def p_expression_uminus(t):
    """expression : MINUS expression %prec UMINUS"""
    t[0] = -t[2]


def p_expression_group(t):
    """expression : LPAREN expression RPAREN"""
    t[0] = t[2]


def p_expression_number(t):
    """expression : NUMBER"""
    t[0] = t[1]


def p_expression_name(t):
    """expression : NAME"""
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0


def p_error(t):
    print("Syntax error at '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()
while True:
    try:
        s = input('calc > ')
    except EOFError:
        break

    parser.parse(s)