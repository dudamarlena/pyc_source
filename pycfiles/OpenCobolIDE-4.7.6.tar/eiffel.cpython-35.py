# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/eiffel.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 2482 bytes
"""
    pygments.lexers.eiffel
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Eiffel language.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'EiffelLexer']

class EiffelLexer(RegexLexer):
    __doc__ = '\n    For `Eiffel <http://www.eiffel.com>`_ source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'Eiffel'
    aliases = ['eiffel']
    filenames = ['*.e']
    mimetypes = ['text/x-eiffel']
    tokens = {'root': [
              (
               '[^\\S\\n]+', Text),
              (
               '--.*?\\n', Comment.Single),
              (
               '[^\\S\\n]+', Text),
              (
               '(?i)(true|false|void|current|result|precursor)\\b', Keyword.Constant),
              (
               '(?i)(and(\\s+then)?|not|xor|implies|or(\\s+else)?)\\b', Operator.Word),
              (
               words(('across', 'agent', 'alias', 'all', 'as', 'assign', 'attached', 'attribute',
       'check', 'class', 'convert', 'create', 'debug', 'deferred', 'detachable',
       'do', 'else', 'elseif', 'end', 'ensure', 'expanded', 'export', 'external',
       'feature', 'from', 'frozen', 'if', 'inherit', 'inspect', 'invariant', 'like',
       'local', 'loop', 'none', 'note', 'obsolete', 'old', 'once', 'only', 'redefine',
       'rename', 'require', 'rescue', 'retry', 'select', 'separate', 'then', 'undefine',
       'until', 'variant', 'when'), prefix='(?i)\\b', suffix='\\b'),
               Keyword.Reserved),
              (
               '"\\[(([^\\]%]|\\n)|%(.|\\n)|\\][^"])*?\\]"', String),
              (
               '"([^"%\\n]|%.)*?"', String),
              include('numbers'),
              (
               "'([^'%]|%'|%%)'", String.Char),
              (
               '(//|\\\\\\\\|>=|<=|:=|/=|~|/~|[\\\\?!#%&@|+/\\-=>*$<^\\[\\]])', Operator),
              (
               '([{}():;,.])', Punctuation),
              (
               '([a-z]\\w*)|([A-Z][A-Z0-9_]*[a-z]\\w*)', Name),
              (
               '([A-Z][A-Z0-9_]*)', Name.Class),
              (
               '\\n+', Text)], 
     
     'numbers': [
                 (
                  '0[xX][a-fA-F0-9]+', Number.Hex),
                 (
                  '0[bB][01]+', Number.Bin),
                 (
                  '0[cC][0-7]+', Number.Oct),
                 (
                  '([0-9]+\\.[0-9]*)|([0-9]*\\.[0-9]+)', Number.Float),
                 (
                  '[0-9]+', Number.Integer)]}