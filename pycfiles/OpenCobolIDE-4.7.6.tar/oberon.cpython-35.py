# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/oberon.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 3741 bytes
"""
    pygments.lexers.oberon
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Oberon family languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'ComponentPascalLexer']

class ComponentPascalLexer(RegexLexer):
    __doc__ = '\n    For `Component Pascal <http://www.oberon.ch/pdf/CP-Lang.pdf>`_ source code.\n\n    .. versionadded:: 2.1\n    '
    name = 'Component Pascal'
    aliases = ['componentpascal', 'cp']
    filenames = ['*.cp', '*.cps']
    mimetypes = ['text/x-component-pascal']
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [
              include('whitespace'),
              include('comments'),
              include('punctuation'),
              include('numliterals'),
              include('strings'),
              include('operators'),
              include('builtins'),
              include('identifiers')], 
     
     'whitespace': [
                    (
                     '\\n+', Text),
                    (
                     '\\s+', Text)], 
     
     'comments': [
                  (
                   '\\(\\*([^\\$].*?)\\*\\)', Comment.Multiline)], 
     
     'punctuation': [
                     (
                      '[\\(\\)\\[\\]\\{\\},.:;\\|]', Punctuation)], 
     
     'numliterals': [
                     (
                      '[0-9A-F]+X\\b', Number.Hex),
                     (
                      '[0-9A-F]+[HL]\\b', Number.Hex),
                     (
                      '[0-9]+\\.[0-9]+E[+-][0-9]+', Number.Float),
                     (
                      '[0-9]+\\.[0-9]+', Number.Float),
                     (
                      '[0-9]+', Number.Integer)], 
     
     'strings': [
                 (
                  "'[^\\n']*'", String),
                 (
                  '"[^\\n"]*"', String)], 
     
     'operators': [
                   (
                    '[+-]', Operator),
                   (
                    '[*/]', Operator),
                   (
                    '[=#<>]', Operator),
                   (
                    '\\^', Operator),
                   (
                    '&', Operator),
                   (
                    '~', Operator),
                   (
                    ':=', Operator),
                   (
                    '\\.\\.', Operator),
                   (
                    '\\$', Operator)], 
     
     'identifiers': [
                     (
                      '([a-zA-Z_\\$][\\w\\$]*)', Name)], 
     
     'builtins': [
                  (
                   words(('ANYPTR', 'ANYREC', 'BOOLEAN', 'BYTE', 'CHAR', 'INTEGER', 'LONGINT', 'REAL',
       'SET', 'SHORTCHAR', 'SHORTINT', 'SHORTREAL'), suffix='\\b'), Keyword.Type),
                  (
                   words(('ABS', 'ABSTRACT', 'ARRAY', 'ASH', 'ASSERT', 'BEGIN', 'BITS', 'BY', 'CAP', 'CASE',
       'CHR', 'CLOSE', 'CONST', 'DEC', 'DIV', 'DO', 'ELSE', 'ELSIF', 'EMPTY', 'END',
       'ENTIER', 'EXCL', 'EXIT', 'EXTENSIBLE', 'FOR', 'HALT', 'IF', 'IMPORT', 'IN',
       'INC', 'INCL', 'IS', 'LEN', 'LIMITED', 'LONG', 'LOOP', 'MAX', 'MIN', 'MOD',
       'MODULE', 'NEW', 'ODD', 'OF', 'OR', 'ORD', 'OUT', 'POINTER', 'PROCEDURE',
       'RECORD', 'REPEAT', 'RETURN', 'SHORT', 'SHORTCHAR', 'SHORTINT', 'SIZE', 'THEN',
       'TYPE', 'TO', 'UNTIL', 'VAR', 'WHILE', 'WITH'), suffix='\\b'), Keyword.Reserved),
                  (
                   '(TRUE|FALSE|NIL|INF)\\b', Keyword.Constant)]}