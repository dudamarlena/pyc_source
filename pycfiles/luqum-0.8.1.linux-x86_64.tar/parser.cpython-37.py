# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/luqum/parser.py
# Compiled at: 2018-06-18 05:44:08
# Size of source mod 2**32: 6569 bytes
"""The Lucene Query DSL parser based on PLY
"""
import re
import ply.lex as lex
import ply.yacc as yacc
from .tree import *

class ParseError(ValueError):
    __doc__ = 'Exception while parsing a lucene statement\n    '


reserved = {'AND':'AND_OP', 
 'OR':'OR_OP', 
 'NOT':'NOT', 
 'TO':'TO'}
tokens = [
 'TERM',
 'PHRASE',
 'APPROX',
 'BOOST',
 'MINUS',
 'SEPARATOR',
 'PLUS',
 'COLUMN',
 'LPAREN',
 'RPAREN',
 'LBRACKET',
 'RBRACKET'] + sorted(list(reserved.values()))
t_PLUS = '\\+'
t_MINUS = '\\-'
t_NOT = 'NOT'
t_AND_OP = 'AND'
t_OR_OP = 'OR'
t_COLUMN = ':'
t_LPAREN = '\\('
t_RPAREN = '\\)'
t_LBRACKET = '(\\[|\\{)'
t_RBRACKET = '(\\]|\\})'
precedence = (('left', 'OR_OP'), ('left', 'AND_OP'), ('nonassoc', 'MINUS'), ('nonassoc', 'PLUS'),
              ('nonassoc', 'APPROX'), ('nonassoc', 'BOOST'), ('nonassoc', 'LPAREN', 'RPAREN'),
              ('nonassoc', 'LBRACKET', 'TO', 'RBRACKET'), ('nonassoc', 'PHRASE'),
              ('nonassoc', 'TERM'))
TIME_RE = '\n(?<=T\\d{2}):  # look behind for T and two digits: hours\n\\d{2}         # minutes\n(:\\d{2})?     # seconds\n'
TERM_RE = '\n(?P<term>  # group term\n  (?:\n   [^\\s:^~(){{}}[\\],"\'+\\-\\\\] # first char is not a space neither some char which have meanings\n                             # note: escape of "-" and "]"\n                             #       and doubling of "{{}}" (because we use format)\n   |                         # but\n   \\\\.                       # we can start with an escaped character\n  )\n  ([^\\s:^\\\\~(){{}}[\\]]       # following chars\n   |                       # OR\n   \\\\.                     # an escaped char\n   |                       # OR\n   {time_re}               # a time expression\n  )*\n)\n'.format(time_re=TIME_RE)
PHRASE_RE = '\n(?P<phrase>  # phrase\n  "          # opening quote\n  (?:        # repeating\n    [^\\\\"]   # - a char which is not escape or end of phrase\n    |        # OR\n    \\\\.      # - an escaped char\n  )*\n  "          # closing quote\n)'
APPROX_RE = '~(?P<degree>[0-9.]+)?'
BOOST_RE = '\\^(?P<force>[0-9.]+)?'

def t_SEPARATOR(t):
    r"""\s+"""
    pass


@lex.TOKEN(TERM_RE)
def t_TERM(t):
    t.type = reserved.get(t.value, 'TERM')
    if t.type == 'TERM':
        m = re.match(TERM_RE, t.value, re.VERBOSE)
        value = m.group('term')
        t.value = Word(value)
    return t


@lex.TOKEN(PHRASE_RE)
def t_PHRASE(t):
    m = re.match(PHRASE_RE, t.value, re.VERBOSE)
    value = m.group('phrase')
    t.value = Phrase(value)
    return t


@lex.TOKEN(APPROX_RE)
def t_APPROX(t):
    m = re.match(APPROX_RE, t.value)
    t.value = m.group('degree')
    return t


@lex.TOKEN(BOOST_RE)
def t_BOOST(t):
    m = re.match(BOOST_RE, t.value)
    t.value = m.group('force')
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

def p_expression_or(p):
    """expression : expression OR_OP expression"""
    p[0] = create_operation(OrOperation, p[1], p[3])


def p_expression_and(p):
    """expression : expression AND_OP expression"""
    p[0] = create_operation(AndOperation, p[1], p[(len(p) - 1)])


def p_expression_implicit(p):
    """expression : expression expression"""
    p[0] = create_operation(UnknownOperation, p[1], p[2])


def p_expression_plus(p):
    """unary_expression : PLUS unary_expression"""
    p[0] = Plus(p[2])


def p_expression_minus(p):
    """unary_expression : MINUS unary_expression"""
    p[0] = Prohibit(p[2])


def p_expression_not(p):
    """unary_expression : NOT unary_expression"""
    p[0] = Not(p[2])


def p_expression_unary(p):
    """expression : unary_expression"""
    p[0] = p[1]


def p_grouping(p):
    """unary_expression : LPAREN expression RPAREN"""
    p[0] = Group(p[2])


def p_range(p):
    """unary_expression : LBRACKET phrase_or_term TO phrase_or_term RBRACKET"""
    include_low = p[1] == '['
    include_high = p[5] == ']'
    p[0] = Range(p[2], p[4], include_low, include_high)


def p_field_search(p):
    """unary_expression : TERM COLUMN unary_expression"""
    if isinstance(p[3], Group):
        p[3] = group_to_fieldgroup(p[3])
    p[0] = SearchField(p[1].value, p[3])


def p_quoting(p):
    """unary_expression : PHRASE"""
    p[0] = p[1]


def p_proximity(p):
    """unary_expression : PHRASE APPROX"""
    p[0] = Proximity(p[1], p[2])


def p_boosting(p):
    """expression : expression BOOST"""
    p[0] = Boost(p[1], p[2])


def p_terms(p):
    """unary_expression : TERM"""
    p[0] = p[1]


def p_fuzzy(p):
    """unary_expression : TERM APPROX"""
    p[0] = Fuzzy(p[1], p[2])


def p_to_as_term(p):
    """unary_expression : TO"""
    p[0] = Word(p[1])


def p_phrase_or_term(p):
    """phrase_or_term : TERM
                      | PHRASE"""
    p[0] = p[1]


def p_error(p):
    if p is None:
        p = '(probably at end of input, may be unmatch parenthesis or so)'
    raise ParseError('Syntax error in input at %r!' % p)


parser = yacc.yacc()