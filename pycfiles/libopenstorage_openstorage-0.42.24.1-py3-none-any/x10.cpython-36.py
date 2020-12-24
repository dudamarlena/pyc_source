# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/x10.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 1965 bytes
"""
    pygments.lexers.x10
    ~~~~~~~~~~~~~~~~~~~

    Lexers for the X10 programming language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
__all__ = [
 'X10Lexer']

class X10Lexer(RegexLexer):
    __doc__ = '\n    For the X10 language.\n\n    .. versionadded:: 0.1\n    '
    name = 'X10'
    aliases = ['x10', 'xten']
    filenames = ['*.x10']
    mimetypes = ['text/x-x10']
    keywords = ('as', 'assert', 'async', 'at', 'athome', 'ateach', 'atomic', 'break',
                'case', 'catch', 'class', 'clocked', 'continue', 'def', 'default',
                'do', 'else', 'final', 'finally', 'finish', 'for', 'goto', 'haszero',
                'here', 'if', 'import', 'in', 'instanceof', 'interface', 'isref',
                'new', 'offer', 'operator', 'package', 'return', 'struct', 'switch',
                'throw', 'try', 'type', 'val', 'var', 'when', 'while')
    types = 'void'
    values = ('false', 'null', 'self', 'super', 'this', 'true')
    modifiers = ('abstract', 'extends', 'implements', 'native', 'offers', 'private',
                 'property', 'protected', 'public', 'static', 'throws', 'transient')
    tokens = {'root': [
              (
               '[^\\S\\n]+', Text),
              (
               '//.*?\\n', Comment.Single),
              (
               '/\\*(.|\\n)*?\\*/', Comment.Multiline),
              (
               '\\b(%s)\\b' % '|'.join(keywords), Keyword),
              (
               '\\b(%s)\\b' % '|'.join(types), Keyword.Type),
              (
               '\\b(%s)\\b' % '|'.join(values), Keyword.Constant),
              (
               '\\b(%s)\\b' % '|'.join(modifiers), Keyword.Declaration),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               "'\\\\.'|'[^\\\\]'|'\\\\u[0-9a-fA-F]{4}'", String.Char),
              (
               '.', Text)]}