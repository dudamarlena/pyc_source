# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/paulvicol/Code/Python/equibel_to_update/equibel/parsers/formulaparser.py
# Compiled at: 2016-05-29 22:09:09
"""Parser for propositional formulas represented using infix notation.

The symbols used for the logical connectives are as follows:

       +------------+--------+
       | Connective | Symbol |
       +============+========+
       |    conj.   |  ``&`` |
       +------------+--------+
       |    disj.   |  ``|`` |
       +------------+--------+
       |   implies  | ``->`` |
       +------------+--------+
       |    equiv   |  ``=`` |
       +------------+--------+
       |     neg    |  ``~`` |
       +------------+--------+

The precedence and right/left associativity rules of the conectives are as follows:

1. Negation (``~``) has the highest precendence, and is right-associative.
2. Conjunction (``&``) has the next highest precedence, and is left-associative.
3. Disjunction (``|``) is next, is left-associative.
4. Implication (``->``) comes next, and is right-associative.
5. Finally, equivalence (``=``) is last, and is right-associative.

Using these precedence rules, the following formulas are equivalent::

* ``p & q | r   ==   (p & q) | r``
* ``p & q -> r   ==   (p & q) -> r``
* ``p | ~r = q   ==   (p | (~r)) = q``
* ``~p | ~q & r   ==   ((~p) | (~q)) & r``

The only importable function from this file is parse_formula, 
which takes a string such as ``p & q | ~r`` and creates a Sympy logical
formula object representing that formula.
"""
from __future__ import absolute_import
import sys, logging, ply, ply.lex as lex, ply.yacc as yacc
from sympy import symbols, simplify
from sympy.logic.boolalg import *
__all__ = [
 'parse_formula']
log = logging.getLogger('ply')
keywords = {'True': 'TRUE', 'False': 'FALSE'}
tokens = [
 'NEG', 'AND', 'OR', 'IMPLIES', 'EQUIV', 'LPAREN', 'RPAREN',
 'INTEGER', 'IDENTIFIER'] + list(keywords.values())

def t_IDENTIFIER(t):
    """[_a-zA-Z][_a-zA-Z0-9]*"""
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t


t_NEG = '~'
t_AND = '&'
t_OR = '\\|'
t_IMPLIES = '->'
t_EQUIV = '='
t_LPAREN = '\\('
t_RPAREN = '\\)'
t_INTEGER = '[0-9]+'
t_ignore = ' \t\n'

def t_NEWLINE(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    line = t.value.lstrip()
    i = line.find('\n')
    line = line if i == -1 else line[:i]
    raise ValueError(('Syntax error, line {0}: {1}').format(t.lineno + 1, line))


def p_FORMULA(p):
    """FORMULA : ATOM
               | BOOLEAN
               | COMPOUND
               | LPAREN FORMULA RPAREN"""
    p[0] = p[1] if len(p) == 2 else p[2]


def p_ATOM(p):
    """ATOM : IDENTIFIER
            | INTEGER"""
    p[0] = symbols(p[1])


def p_BOOLEAN_TRUE(p):
    """BOOLEAN : TRUE"""
    p[0] = true


def p_BOOLEAN_FALSE(p):
    """BOOLEAN : FALSE"""
    p[0] = false


def p_COMPOUND(p):
    """COMPOUND : NEGATION
                | CONJUNCTION
                | DISJUNCTION
                | IMPLICATION
                | EQUIVALENCE"""
    p[0] = p[1]


def p_NEGATION(p):
    """NEGATION : NEG FORMULA"""
    p[0] = ~p[2]


def p_CONJUNCTION(p):
    """CONJUNCTION : FORMULA AND FORMULA"""
    p[0] = p[1] & p[3]


def p_DISJUNCTION(p):
    """DISJUNCTION : FORMULA OR FORMULA"""
    p[0] = p[1] | p[3]


def p_IMPLICATION(p):
    """IMPLICATION : FORMULA IMPLIES FORMULA"""
    p[0] = p[1] >> p[3]


def p_EQUIVALENCE(p):
    """EQUIVALENCE : FORMULA EQUIV FORMULA"""
    p[0] = p[1] >> p[3] & p[3] >> p[1]


def p_error(p):
    if p is None:
        raise ValueError('Unknown error')
    raise ValueError(('Syntax error, line {0}: {1}').format(p.lineno + 1, p.type))
    return


precedence = (
 ('right', 'EQUIV'),
 ('right', 'IMPLIES'),
 ('left', 'OR'),
 ('left', 'AND'),
 ('right', 'NEG'))
lexer = lex.lex()
parser = yacc.yacc(errorlog=log)

def parse_formula(text):
    try:
        return parser.parse(text, lexer=lexer)
    except ValueError as err:
        raise ValueError(err)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python formulaparser.py FORMULA_STRING'
        sys.exit(1)
    formula_str = sys.argv[1]
    formula = parse_infix_formula(formula_str)
    print repr(formula)
    print ('Simplified = \n{0}').format(repr(simplify(formula)))