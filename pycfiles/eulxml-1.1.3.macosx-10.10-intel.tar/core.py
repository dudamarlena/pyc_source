# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/xpath/core.py
# Compiled at: 2016-02-19 17:15:24
"""Core XPath parsing glue.

This module builds a lexer and parser for XPath expressions for import into
eulxml.xpath. To understand how this module builds the lexer and parser, it
is helpful to understand how the `ply <http://www.dabeaz.com/ply/>`_ module
works.

Note that most client applications will import htese objects from
eulxml.xpath, not directly from here."""
from __future__ import unicode_literals
import os, re
from ply import lex, yacc
import tempfile
from eulxml.xpath import lexrules
from eulxml.xpath import parserules
from eulxml.xpath.ast import serialize
__all__ = [
 b'lexer', b'parser', b'parse', b'serialize']
OPERATOR_FORCERS = set([
 b'ABBREV_AXIS_AT', b'AXIS_SEP', b'OPEN_PAREN', b'OPEN_BRACKET',
 b'AND_OP', b'OR_OP', b'MOD_OP', b'DIV_OP', b'MULT_OP',
 b'PATH_SEP',
 b'ABBREV_PATH_SEP', b'UNION_OP', b'PLUS_OP', b'MINUS_OP',
 b'EQUAL_OP', b'REL_OP',
 b'COLON'])
NODE_TYPES = set([b'comment', b'text', b'processing-instruction', b'node'])

class LexerWrapper(lex.Lexer):

    def token(self):
        tok = lex.Lexer.token(self)
        if tok is not None:
            if tok.type == b'STAR_OP':
                if self.last is not None and self.last.type not in OPERATOR_FORCERS:
                    tok.type = b'MULT_OP'
            if tok.type == b'NCNAME':
                if self.last is not None and self.last.type not in OPERATOR_FORCERS:
                    operator = lexrules.operator_names.get(tok.value, None)
                    if operator is not None:
                        tok.type = operator
                else:
                    next = self.peek()
                    if next is not None:
                        if next.type == b'OPEN_PAREN':
                            if tok.value in NODE_TYPES:
                                tok.type = b'NODETYPE'
                            else:
                                tok.type = b'FUNCNAME'
                        elif next.type == b'AXIS_SEP':
                            tok.type = b'AXISNAME'
        self.last = tok
        return tok

    def peek(self):
        clone = self.clone()
        return clone.token()


lexdir = os.path.dirname(lexrules.__file__)
lexer = None
try:
    lexer = lex.lex(module=lexrules, optimize=1, outputdir=lexdir, reflags=re.UNICODE)
except IOError as e:
    import errno
    if e.errno != errno.EACCES:
        raise

if lexer is None:
    lexer = lex.lex(module=lexrules, reflags=re.UNICODE)
lexer.__class__ = LexerWrapper
lexer.last = None
parsedir = os.path.dirname(parserules.__file__)
if not os.access(parsedir, os.W_OK):
    parsedir = tempfile.gettempdir()
parser = yacc.yacc(module=parserules, outputdir=parsedir, debug=0)

def parse(xpath):
    """Parse an xpath."""
    return parser.parse(xpath, lexer=lexer)


def ptokens(s):
    """Lex a string as XPath tokens, and print each token as it is lexed.
    This is used primarily for debugging. You probably don't want this
    function."""
    lexer.input(s)
    for tok in lexer:
        print tok