# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/parser/pplexer.py
# Compiled at: 2019-12-10 16:20:40
# Size of source mod 2**32: 8942 bytes
"""Preprocess a C source file using gcc and convert the result into
   a token stream

Reference is C99:
  * http://www.open-std.org/JTC1/SC22/WG14/www/docs/n1124.pdf

"""
__docformat__ = 'restructuredtext'
import os, re, shlex, sys, tokenize, traceback, ctypes
from .lex import TOKEN
tokens = ('HEADER_NAME', 'IDENTIFIER', 'PP_NUMBER', 'CHARACTER_CONSTANT', 'STRING_LITERAL',
          'OTHER', 'PTR_OP', 'INC_OP', 'DEC_OP', 'LEFT_OP', 'RIGHT_OP', 'LE_OP',
          'GE_OP', 'EQ_OP', 'NE_OP', 'AND_OP', 'OR_OP', 'MUL_ASSIGN', 'DIV_ASSIGN',
          'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN',
          'AND_ASSIGN', 'XOR_ASSIGN', 'OR_ASSIGN', 'PERIOD', 'ELLIPSIS', 'LPAREN',
          'NEWLINE', 'PP_DEFINE', 'PP_DEFINE_NAME', 'PP_DEFINE_MACRO_NAME', 'PP_UNDEFINE',
          'PP_MACRO_PARAM', 'PP_STRINGIFY', 'PP_IDENTIFIER_PASTE', 'PP_END_DEFINE',
          'PRAGMA', 'PRAGMA_PACK', 'PRAGMA_END')
states = [
 ('DEFINE', 'exclusive'), ('PRAGMA', 'exclusive')]
subs = {'D':'[0-9]', 
 'L':'[a-zA-Z_]', 
 'H':'[a-fA-F0-9]', 
 'E':'[Ee][+-]?\\s*{D}+', 
 'FS':'([FflL]|D[FDL]|[fF]\\d+x?)', 
 'IS':'[uUlL]*'}
sub_pattern = re.compile('{([^}]*)}')

def sub_repl_match(m):
    return subs[m.groups()[0]]


def sub(s):
    return sub_pattern.sub(sub_repl_match, s)


class StringLiteral(str):

    def __new__(cls, value):
        if not (value[0] == '"' and value[(-1)] == '"'):
            raise AssertionError
        value = value[1:-1]
        return str.__new__(cls, value)


punctuators = {'...':('\\.\\.\\.', 'ELLIPSIS'), 
 '>>=':('>>=', 'RIGHT_ASSIGN'), 
 '<<=':('<<=', 'LEFT_ASSIGN'), 
 '+=':('\\+=', 'ADD_ASSIGN'), 
 '-=':('-=', 'SUB_ASSIGN'), 
 '*=':('\\*=', 'MUL_ASSIGN'), 
 '/=':('/=', 'DIV_ASSIGN'), 
 '%=':('%=', 'MOD_ASSIGN'), 
 '&=':('&=', 'AND_ASSIGN'), 
 '^=':('\\^=', 'XOR_ASSIGN'), 
 '|=':('\\|=', 'OR_ASSIGN'), 
 '>>':('>>', 'RIGHT_OP'), 
 '<<':('<<', 'LEFT_OP'), 
 '++':('\\+\\+', 'INC_OP'), 
 '--':('--', 'DEC_OP'), 
 '->':('->', 'PTR_OP'), 
 '&&':('&&', 'AND_OP'), 
 '||':('\\|\\|', 'OR_OP'), 
 '<=':('<=', 'LE_OP'), 
 '>=':('>=', 'GE_OP'), 
 '==':('==', 'EQ_OP'), 
 '!=':('!=', 'NE_OP'), 
 '<:':('<:', '['), 
 ':>':(':>', ']'), 
 '<%':('<%', '{'), 
 '%>':('%>', '}'), 
 ';':(';', ';'), 
 '{':('{', '{'), 
 '}':('}', '}'), 
 ',':(',', ','), 
 ':':(':', ':'), 
 '=':('=', '='), 
 ')':('\\)', ')'), 
 '[':('\\[', '['), 
 ']':(']', ']'), 
 '.':('\\.', 'PERIOD'), 
 '&':('&', '&'), 
 '!':('!', '!'), 
 '~':('~', '~'), 
 '-':('-', '-'), 
 '+':('\\+', '+'), 
 '*':('\\*', '*'), 
 '/':('/', '/'), 
 '%':('%', '%'), 
 '<':('<', '<'), 
 '>':('>', '>'), 
 '^':('\\^', '^'), 
 '|':('\\|', '|'), 
 '?':('\\?', '?')}

def punctuator_regex(punctuators):
    punctuator_regexes = [v[0] for v in punctuators.values()]
    punctuator_regexes.sort(key=len, reverse=True)
    return '(%s)' % '|'.join(punctuator_regexes)


DIRECTIVE = '\\#\\s+(\\d+)\\s+"([^"]+)"[ \\d]*\\n'

@TOKEN(DIRECTIVE)
def t_ANY_directive(t):
    t.lexer.filename = t.groups[2]
    t.lexer.lineno = int(t.groups[1])


@TOKEN(punctuator_regex(punctuators))
def t_ANY_punctuator(t):
    t.type = punctuators[t.value][1]
    return t


IDENTIFIER = sub('{L}({L}|{D})*')

@TOKEN(IDENTIFIER)
def t_INITIAL_identifier(t):
    t.type = 'IDENTIFIER'
    return t


@TOKEN(IDENTIFIER)
def t_DEFINE_identifier(t):
    if t.lexer.next_is_define_name:
        if t.lexpos + len(t.value) < t.lexer.lexlen and t.lexer.lexdata[(t.lexpos + len(t.value))] == '(':
            t.type = 'PP_DEFINE_MACRO_NAME'
            lexdata = t.lexer.lexdata
            pos = t.lexpos + len(t.value) + 1
            while lexdata[pos] not in '\n)':
                pos += 1

            params = lexdata[t.lexpos + len(t.value) + 1:pos]
            paramlist = [x.strip() for x in params.split(',') if x.strip()]
            t.lexer.macro_params = paramlist
        else:
            t.type = 'PP_DEFINE_NAME'
        t.lexer.next_is_define_name = False
    else:
        if t.value in t.lexer.macro_params:
            t.type = 'PP_MACRO_PARAM'
        else:
            t.type = 'IDENTIFIER'
    return t


FLOAT_LITERAL = sub('(?P<p1>{D}+)?(?P<dp>[.]?)(?P<p2>(?(p1){D}*|{D}+))(?P<exp>(?:[Ee][+-]?{D}+)?)(?P<suf>{FS}?)(?!\\w)')

@TOKEN(FLOAT_LITERAL)
def t_ANY_float(t):
    t.type = 'PP_NUMBER'
    m = t.lexer.lexmatch
    p1 = m.group('p1')
    dp = m.group('dp')
    p2 = m.group('p2')
    exp = m.group('exp')
    suf = m.group('suf')
    if not (dp or exp):
        if not suf or re.match(subs['FS'] + '$', suf):
            s = m.group(0)
            if suf:
                s = s[:-len(suf)]
            t.value = 'f' + s
    elif suf and suf in 'Ll':
        t.value = 'l' + p1
    else:
        t.value = 'i' + p1
    return t


INT_LITERAL = sub('(?P<p1>(?:0x{H}+)|(?:{D}+))(?P<suf>{IS})')

@TOKEN(INT_LITERAL)
def t_ANY_int(t):
    t.type = 'PP_NUMBER'
    m = t.lexer.lexmatch
    if 'L' in m.group(3) or 'l' in m.group(2):
        prefix = 'l'
    else:
        prefix = 'i'
    g1 = m.group(2)
    if g1.startswith('0x'):
        g1 = str(int(g1[2:], 16))
    else:
        if g1[0] == '0':
            g1 = str(int(g1, 8))
    t.value = prefix + g1
    return t


CHARACTER_CONSTANT = sub("L?'(\\\\.|[^\\\\'])+'")

@TOKEN(CHARACTER_CONSTANT)
def t_ANY_character_constant(t):
    t.type = 'CHARACTER_CONSTANT'
    return t


STRING_LITERAL = sub('L?"(\\\\.|[^\\\\"])*"')

@TOKEN(STRING_LITERAL)
def t_ANY_string_literal(t):
    t.type = 'STRING_LITERAL'
    t.value = StringLiteral(t.value)
    return t


@TOKEN('\\(')
def t_ANY_lparen(t):
    if t.lexpos == 0 or t.lexer.lexdata[(t.lexpos - 1)] not in ' \t\x0c\x0b\n':
        t.type = 'LPAREN'
    else:
        t.type = '('
    return t


@TOKEN('\\n')
def t_INITIAL_newline(t):
    t.lexer.lineno += 1


@TOKEN('\\#undef')
def t_INITIAL_pp_undefine(t):
    t.type = 'PP_UNDEFINE'
    t.lexer.begin('DEFINE')
    t.lexer.next_is_define_name = True
    t.lexer.macro_params = set()
    return t


@TOKEN('\\#define')
def t_INITIAL_pp_define(t):
    t.type = 'PP_DEFINE'
    t.lexer.begin('DEFINE')
    t.lexer.next_is_define_name = True
    t.lexer.macro_params = set()
    return t


@TOKEN('\\#pragma')
def t_INITIAL_pragma(t):
    t.type = 'PRAGMA'
    t.lexer.begin('PRAGMA')
    return t


@TOKEN('pack')
def t_PRAGMA_pack(t):
    t.type = 'PRAGMA_PACK'
    return t


@TOKEN('\\n')
def t_PRAGMA_newline(t):
    t.type = 'PRAGMA_END'
    t.lexer.begin('INITIAL')
    t.lexer.lineno += 1
    return t


@TOKEN(IDENTIFIER)
def t_PRAGMA_identifier(t):
    t.type = 'IDENTIFIER'
    return t


def t_PRAGMA_error(t):
    t.type = 'OTHER'
    t.value = t.value[0:30]
    t.lexer.lexpos += 1
    return t


@TOKEN('\\n')
def t_DEFINE_newline(t):
    t.type = 'PP_END_DEFINE'
    t.lexer.begin('INITIAL')
    t.lexer.lineno += 1
    del t.lexer.macro_params
    t.lexer.next_is_define_name = False
    return t


@TOKEN('(\\#\\#)|(\\#)')
def t_DEFINE_pp_param_op(t):
    if t.value == '#':
        t.type = 'PP_STRINGIFY'
    else:
        t.type = 'PP_IDENTIFIER_PASTE'
    return t


def t_INITIAL_error(t):
    t.type = 'OTHER'
    return t


def t_DEFINE_error(t):
    t.type = 'OTHER'
    t.value = t.value[0]
    t.lexer.lexpos += 1
    return t


t_ANY_ignore = ' \t\x0b\x0c\r'