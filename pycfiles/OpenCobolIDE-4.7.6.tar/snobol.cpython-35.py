# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/snobol.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 2756 bytes
"""
    pygments.lexers.snobol
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the SNOBOL language.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'SnobolLexer']

class SnobolLexer(RegexLexer):
    __doc__ = '\n    Lexer for the SNOBOL4 programming language.\n\n    Recognizes the common ASCII equivalents of the original SNOBOL4 operators.\n    Does not require spaces around binary operators.\n\n    .. versionadded:: 1.5\n    '
    name = 'Snobol'
    aliases = ['snobol']
    filenames = ['*.snobol']
    mimetypes = ['text/x-snobol']
    tokens = {'root': [
              (
               '\\*.*\\n', Comment),
              (
               '[+.] ', Punctuation, 'statement'),
              (
               '-.*\\n', Comment),
              (
               'END\\s*\\n', Name.Label, 'heredoc'),
              (
               '[A-Za-z$][\\w$]*', Name.Label, 'statement'),
              (
               '\\s+', Text, 'statement')], 
     
     'statement': [
                   (
                    '\\s*\\n', Text, '#pop'),
                   (
                    '\\s+', Text),
                   (
                    '(?<=[^\\w.])(LT|LE|EQ|NE|GE|GT|INTEGER|IDENT|DIFFER|LGT|SIZE|REPLACE|TRIM|DUPL|REMDR|DATE|TIME|EVAL|APPLY|OPSYN|LOAD|UNLOAD|LEN|SPAN|BREAK|ANY|NOTANY|TAB|RTAB|REM|POS|RPOS|FAIL|FENCE|ABORT|ARB|ARBNO|BAL|SUCCEED|INPUT|OUTPUT|TERMINAL)(?=[^\\w.])',
                    Name.Builtin),
                   (
                    '[A-Za-z][\\w.]*', Name),
                   (
                    '\\*\\*|[?$.!%*/#+\\-@|&\\\\=]', Operator),
                   (
                    '"[^"]*"', String),
                   (
                    "'[^']*'", String),
                   (
                    '[0-9]+(?=[^.EeDd])', Number.Integer),
                   (
                    '[0-9]+(\\.[0-9]*)?([EDed][-+]?[0-9]+)?', Number.Float),
                   (
                    ':', Punctuation, 'goto'),
                   (
                    '[()<>,;]', Punctuation)], 
     
     'goto': [
              (
               '\\s*\\n', Text, '#pop:2'),
              (
               '\\s+', Text),
              (
               'F|S', Keyword),
              (
               '(\\()([A-Za-z][\\w.]*)(\\))',
               bygroups(Punctuation, Name.Label, Punctuation))], 
     
     'heredoc': [
                 (
                  '.*\\n', String.Heredoc)]}