# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/apl.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 3167 bytes
"""
    pygments.lexers.apl
    ~~~~~~~~~~~~~~~~~~~

    Lexers for APL.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'APLLexer']

class APLLexer(RegexLexer):
    __doc__ = '\n    A simple APL lexer.\n\n    .. versionadded:: 2.0\n    '
    name = 'APL'
    aliases = ['apl']
    filenames = ['*.apl']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '[⍝#].*$', Comment.Single),
              (
               "\\'((\\'\\')|[^\\'])*\\'", String.Single),
              (
               '"(("")|[^"])*"', String.Double),
              (
               '[⋄◇()]', Punctuation),
              (
               '[\\[\\];]', String.Regex),
              (
               '⎕[A-Za-zΔ∆⍙][A-Za-zΔ∆⍙_¯0-9]*', Name.Function),
              (
               '[A-Za-zΔ∆⍙][A-Za-zΔ∆⍙_¯0-9]*', Name.Variable),
              (
               '¯?(0[Xx][0-9A-Fa-f]+|[0-9]*\\.?[0-9]+([Ee][+¯]?[0-9]+)?|¯|∞)([Jj]¯?(0[Xx][0-9A-Fa-f]+|[0-9]*\\.?[0-9]+([Ee][+¯]?[0-9]+)?|¯|∞))?',
               Number),
              (
               '[\\.\\\\/⌿⍀¨⍣⍨⍠⍤∘]', Name.Attribute),
              (
               '[+\\-×÷⌈⌊∣|⍳?*⍟○!⌹<≤=>≥≠≡≢∊⍷∪∩~∨∧⍱⍲⍴,⍪⌽⊖⍉↑↓⊂⊃⌷⍋⍒⊤⊥⍕⍎⊣⊢⍁⍂≈⌸⍯↗]',
               Operator),
              (
               '⍬', Name.Constant),
              (
               '[⎕⍞]', Name.Variable.Global),
              (
               '[←→]', Keyword.Declaration),
              (
               '[⍺⍵⍶⍹∇:]', Name.Builtin.Pseudo),
              (
               '[{}]', Keyword.Type)]}