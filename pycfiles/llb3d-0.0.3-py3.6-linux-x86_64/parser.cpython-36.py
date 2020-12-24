# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/llb3d/parser.py
# Compiled at: 2019-01-14 10:33:18
# Size of source mod 2**32: 2745 bytes
"""Parser for Blitz3D language."""
from ply import yacc
from . import ast, lexer
from .lexer import tokens

class ParserGlobals:
    __doc__ = 'Global variables for parser.'

    def __init__(self):
        """Global variables for parser."""
        self.error_list = []


start = 'program'

def p_empty(_p):
    """empty : """
    pass


def p_statement_descent(p):
    """global_statement : statement
        local_statement : statement
    """
    p[0] = p[1]


def p_statements_start(p):
    """global_statements : global_statement
        local_statements : local_statement
    """
    p[0] = ast.Body((p[1],))


def p_statement_rest(p):
    r"""global_statements : global_statements '\n' global_statement
        local_statements : local_statements '\n' local_statement
    """
    p[0] = ast.Body(p[1]['statements'] + (p[3],))


def p_id(p):
    """id : ID"""
    p[0] = ast.Identifier(p[1])


def p_atom_int(p):
    """atom : INTLIT"""
    p[0] = ast.IntLiteral(int(p[1]))


def p_atom_float(p):
    """atom : FLOATLIT"""
    p[0] = ast.FloatLiteral(float(p[1]))


def p_atom_string(p):
    """atom : STRLIT"""
    p[0] = ast.StrLiteral(p[1])


def p_atom_id(p):
    """atom : id"""
    p[0] = p[1]


def p_expression_descent(p):
    """expression : atom
        statement : expression
    """
    p[0] = p[1]


def p_exprlist_start(p):
    """exprlist : expression"""
    p[0] = (
     p[1],)


def p_exprlist_rest(p):
    """exprlist : exprlist ',' expression"""
    p[0] = p[1] + (p[3],)


def p_statement_proccall(p):
    """statement : proccall"""
    p[0] = p[1]


def p_proccall(p):
    """proccall : id exprlist
                 | id empty
    """
    if p[2] is None:
        p[0] = ast.ProcedureCall(p[1], tuple())
    else:
        p[0] = ast.ProcedureCall(p[1], p[2])


def p_start(p):
    """program : global_statements"""
    p[0] = ast.Program(p[1]['statements'])


def p_error(p):
    """Error handler."""
    if not p:
        parser.globals.error_list.append('Unexpected EOF')
        return
    parser.globals.error_list.append("Unexpected {type} '{value}' at {position}".format(type=(p.type),
      value=(p.value),
      position=(lexer.position(p))))


parser = yacc.yacc()

def get_ast(code):
    """Get AST from the source code."""
    parser.globals = ParserGlobals()
    syntax_tree = parser.parse(lexer=(lexer.get_lexer(code)))
    if parser.globals.error_list != []:
        raise SyntaxError('\n'.join(parser.globals.error_list))
    return syntax_tree