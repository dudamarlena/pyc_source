# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/relax/rnc_tokenize.py
# Compiled at: 2015-04-13 16:10:50
import lex
tokens = tuple(('\n  ELEM ATTR EMPTY TEXT KEYWORD LITERAL ANNOTATION COMMENT\n  BEG_PAREN END_PAREN BEG_BODY END_BODY EQUAL NAME CHOICE SEQ\n  INTERLEAVE ANY SOME MAYBE WHITESPACE TODO DATATAG PATTERN\n  DEFAULT_NS NS DATATYPES NS_ANNOTATION START DEFINE\n  ').split())
reserved = {'element': 'ELEM', 
   'attribute': 'ATTR', 
   'empty': 'EMPTY', 
   'text': 'TEXT', 
   'div': 'TODO', 
   'external': 'TODO', 
   'grammar': 'TODO', 
   'include': 'TODO', 
   'inherit': 'TODO', 
   'list': 'TODO', 
   'mixed': 'TODO', 
   'notAllowed': 'TODO', 
   'parent': 'TODO', 
   'string': 'TODO', 
   'token': 'TODO'}

def t_START(t):
    r"""(?im)^start\s*=\s*.*$"""
    t.value = t.value.split('=')[1].strip()
    return t


def t_DEFINE(t):
    r"""(?im)^[\w-]+\s*="""
    t.value = t.value.split('=')[0].strip()
    return t


def t_ANNOTATION(t):
    r"""(?im)^\#\# .*$"""
    t.value = t.value[3:]
    return t


def t_COMMENT(t):
    r"""(?im)^\# .*$"""
    t.value = t.value[2:]
    return t


def t_DEFAULT_NS(t):
    r"""(?im)default\s+namespace\s*=\s*.*$"""
    t.value = t.value.split('=')[1].strip()
    return t


def t_DATATYPES(t):
    r"""(?im)datatypes\s+xsd\s*=\s*.*$"""
    t.value = t.value.split('=')[1].strip()
    return t


def t_DATATAG(t):
    r"""xsd:\w+"""
    t.value = t.value.split(':')[1]
    return t


def t_PATTERN(t):
    r"""{\s*pattern\s*=\s*".*"\s*}"""
    t.value = t.value[:-1].split('=')[1].strip()[1:-1]
    return t


def t_NS(t):
    r"""(?im)^namespace\s+.*$"""
    t.value = t.value.split(None, 1)[1]
    return t


def t_ID(t):
    r"""[\w:_-]+"""
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_LITERAL(t):
    """".+?\""""
    t.value = t.value[1:-1]
    return t


t_BEG_PAREN = '\\('
t_END_PAREN = '\\)'
t_BEG_BODY = '{'
t_END_BODY = '}'
t_EQUAL = '='
t_CHOICE = '[|]'
t_SEQ = ','
t_INTERLEAVE = '&'
t_ANY = '[*]'
t_SOME = '[+]'
t_MAYBE = '[?]'
t_WHITESPACE = '\\s+'
t_ignore = ' \t\n\r'

def t_error(t):
    t.skip(1)


def token_list(rnc):
    lex.lex()
    lex.input(rnc)
    ts = []
    while 1:
        t = lex.token()
        if t is None:
            break
        ts.append(t)

    return ts


if __name__ == '__main__':
    import sys
    del t_ignore
    tokens = token_list(sys.stdin.read())
    print ('\n').join(map(repr, tokens))