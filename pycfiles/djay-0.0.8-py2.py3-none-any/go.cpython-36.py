# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/go.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 3701 bytes
"""
    pygments.lexers.go
    ~~~~~~~~~~~~~~~~~~

    Lexers for the Google Go language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'GoLexer']

class GoLexer(RegexLexer):
    __doc__ = '\n    For `Go <http://golang.org>`_ source.\n\n    .. versionadded:: 1.2\n    '
    name = 'Go'
    filenames = ['*.go']
    aliases = ['go']
    mimetypes = ['text/x-gosrc']
    flags = re.MULTILINE | re.UNICODE
    tokens = {'root': [
              (
               '\\n', Text),
              (
               '\\s+', Text),
              (
               '\\\\\\n', Text),
              (
               '//(.*?)\\n', Comment.Single),
              (
               '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
              (
               '(import|package)\\b', Keyword.Namespace),
              (
               '(var|func|struct|map|chan|type|interface|const)\\b',
               Keyword.Declaration),
              (
               words(('break', 'default', 'select', 'case', 'defer', 'go', 'else', 'goto', 'switch',
       'fallthrough', 'if', 'range', 'continue', 'for', 'return'),
                 suffix='\\b'),
               Keyword),
              (
               '(true|false|iota|nil)\\b', Keyword.Constant),
              (
               words(('uint', 'uint8', 'uint16', 'uint32', 'uint64', 'int', 'int8', 'int16', 'int32',
       'int64', 'float', 'float32', 'float64', 'complex64', 'complex128', 'byte',
       'rune', 'string', 'bool', 'error', 'uintptr', 'print', 'println', 'panic',
       'recover', 'close', 'complex', 'real', 'imag', 'len', 'cap', 'append', 'copy',
       'delete', 'new', 'make'),
                 suffix='\\b(\\()'),
               bygroups(Name.Builtin, Punctuation)),
              (
               words(('uint', 'uint8', 'uint16', 'uint32', 'uint64', 'int', 'int8', 'int16', 'int32',
       'int64', 'float', 'float32', 'float64', 'complex64', 'complex128', 'byte',
       'rune', 'string', 'bool', 'error', 'uintptr'),
                 suffix='\\b'),
               Keyword.Type),
              (
               '\\d+i', Number),
              (
               '\\d+\\.\\d*([Ee][-+]\\d+)?i', Number),
              (
               '\\.\\d+([Ee][-+]\\d+)?i', Number),
              (
               '\\d+[Ee][-+]\\d+i', Number),
              (
               '\\d+(\\.\\d+[eE][+\\-]?\\d+|\\.\\d*|[eE][+\\-]?\\d+)',
               Number.Float),
              (
               '\\.\\d+([eE][+\\-]?\\d+)?', Number.Float),
              (
               '0[0-7]+', Number.Oct),
              (
               '0[xX][0-9a-fA-F]+', Number.Hex),
              (
               '(0|[1-9][0-9]*)', Number.Integer),
              (
               '\'(\\\\[\'"\\\\abfnrtv]|\\\\x[0-9a-fA-F]{2}|\\\\[0-7]{1,3}|\\\\u[0-9a-fA-F]{4}|\\\\U[0-9a-fA-F]{8}|[^\\\\])\'',
               String.Char),
              (
               '`[^`]*`', String),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               '(<<=|>>=|<<|>>|<=|>=|&\\^=|&\\^|\\+=|-=|\\*=|/=|%=|&=|\\|=|&&|\\|\\||<-|\\+\\+|--|==|!=|:=|\\.\\.\\.|[+\\-*/%&])',
               Operator),
              (
               '[|^<>=!()\\[\\]{}.,;:]', Punctuation),
              (
               '[^\\W\\d]\\w*', Name.Other)]}