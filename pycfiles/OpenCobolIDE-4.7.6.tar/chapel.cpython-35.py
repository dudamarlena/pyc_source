# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/chapel.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 3458 bytes
"""
    pygments.lexers.chapel
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Chapel language.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'ChapelLexer']

class ChapelLexer(RegexLexer):
    __doc__ = '\n    For `Chapel <http://chapel.cray.com/>`_ source.\n\n    .. versionadded:: 2.0\n    '
    name = 'Chapel'
    filenames = ['*.chpl']
    aliases = ['chapel', 'chpl']
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
               '(config|const|in|inout|out|param|ref|type|var)\\b',
               Keyword.Declaration),
              (
               '(false|nil|true)\\b', Keyword.Constant),
              (
               '(bool|complex|imag|int|opaque|range|real|string|uint)\\b',
               Keyword.Type),
              (
               words(('align', 'atomic', 'begin', 'break', 'by', 'cobegin', 'coforall', 'continue',
       'delete', 'dmapped', 'do', 'domain', 'else', 'enum', 'except', 'export', 'extern',
       'for', 'forall', 'if', 'index', 'inline', 'iter', 'label', 'lambda', 'let',
       'local', 'new', 'noinit', 'on', 'only', 'otherwise', 'pragma', 'private',
       'public', 'reduce', 'require', 'return', 'scan', 'select', 'serial', 'single',
       'sparse', 'subdomain', 'sync', 'then', 'use', 'when', 'where', 'while', 'with',
       'yield', 'zip'), suffix='\\b'),
               Keyword),
              (
               '(proc)((?:\\s|\\\\\\s)+)', bygroups(Keyword, Text), 'procname'),
              (
               '(class|module|record|union)(\\s+)', bygroups(Keyword, Text),
               'classname'),
              (
               '\\d+i', Number),
              (
               '\\d+\\.\\d*([Ee][-+]\\d+)?i', Number),
              (
               '\\.\\d+([Ee][-+]\\d+)?i', Number),
              (
               '\\d+[Ee][-+]\\d+i', Number),
              (
               '(\\d*\\.\\d+)([eE][+-]?[0-9]+)?i?', Number.Float),
              (
               '\\d+[eE][+-]?[0-9]+i?', Number.Float),
              (
               '0[bB][01]+', Number.Bin),
              (
               '0[xX][0-9a-fA-F]+', Number.Hex),
              (
               '0[oO][0-7]+', Number.Oct),
              (
               '[0-9]+', Number.Integer),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               "'(\\\\\\\\|\\\\'|[^'])*'", String),
              (
               '(=|\\+=|-=|\\*=|/=|\\*\\*=|%=|&=|\\|=|\\^=|&&=|\\|\\|=|<<=|>>=|<=>|<~>|\\.\\.|by|#|\\.\\.\\.|&&|\\|\\||!|&|\\||\\^|~|<<|>>|==|!=|<=|>=|<|>|[+\\-*/%]|\\*\\*)',
               Operator),
              (
               '[:;,.?()\\[\\]{}]', Punctuation),
              (
               '[a-zA-Z_][\\w$]*', Name.Other)], 
     
     'classname': [
                   (
                    '[a-zA-Z_][\\w$]*', Name.Class, '#pop')], 
     
     'procname': [
                  (
                   '[a-zA-Z_][\\w$]*', Name.Function, '#pop')]}