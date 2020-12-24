# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/ampl.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 4123 bytes
"""
    pygments.lexers.ampl
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for the AMPL language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, bygroups, using, this, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'AmplLexer']

class AmplLexer(RegexLexer):
    __doc__ = '\n    For `AMPL <http://ampl.com/>`_ source code.\n\n    .. versionadded:: 2.2\n    '
    name = 'Ampl'
    aliases = ['ampl']
    filenames = ['*.run']
    tokens = {'root': [
              (
               '\\n', Text),
              (
               '\\s+', Text.Whitespace),
              (
               '#.*?\\n', Comment.Single),
              (
               '/[*](.|\\n)*?[*]/', Comment.Multiline),
              (
               words(('call', 'cd', 'close', 'commands', 'data', 'delete', 'display', 'drop', 'end',
       'environ', 'exit', 'expand', 'include', 'load', 'model', 'objective', 'option',
       'problem', 'purge', 'quit', 'redeclare', 'reload', 'remove', 'reset', 'restore',
       'shell', 'show', 'solexpand', 'solution', 'solve', 'update', 'unload', 'xref',
       'coeff', 'coef', 'cover', 'obj', 'interval', 'default', 'from', 'to', 'to_come',
       'net_in', 'net_out', 'dimen', 'dimension', 'check', 'complements', 'write',
       'function', 'pipe', 'format', 'if', 'then', 'else', 'in', 'while', 'repeat',
       'for'),
                 suffix='\\b'), Keyword.Reserved),
              (
               '(integer|binary|symbolic|ordered|circular|reversed|INOUT|IN|OUT|LOCAL)',
               Keyword.Type),
              (
               '\\".*?\\"', String.Double),
              (
               "\\'.*?\\'", String.Single),
              (
               '[()\\[\\]{},;:]+', Punctuation),
              (
               '\\b(\\w+)(\\.)(astatus|init0|init|lb0|lb1|lb2|lb|lrc|lslack|rc|relax|slack|sstatus|status|ub0|ub1|ub2|ub|urc|uslack|val)',
               bygroups(Name.Variable, Punctuation, Keyword.Reserved)),
              (
               '(set|param|var|arc|minimize|maximize|subject to|s\\.t\\.|subj to|node|table|suffix|read table|write table)(\\s+)(\\w+)',
               bygroups(Keyword.Declaration, Text, Name.Variable)),
              (
               '(param)(\\s*)(:)(\\s*)(\\w+)(\\s*)(:)(\\s*)((\\w|\\s)+)',
               bygroups(Keyword.Declaration, Text, Punctuation, Text, Name.Variable, Text, Punctuation, Text, Name.Variable)),
              (
               '(let|fix|unfix)(\\s*)((?:\\{.*\\})?)(\\s*)(\\w+)',
               bygroups(Keyword.Declaration, Text, using(this), Text, Name.Variable)),
              (
               words(('abs', 'acos', 'acosh', 'alias', 'asin', 'asinh', 'atan', 'atan2', 'atanh',
       'ceil', 'ctime', 'cos', 'exp', 'floor', 'log', 'log10', 'max', 'min', 'precision',
       'round', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'time', 'trunc', 'Beta', 'Cauchy',
       'Exponential', 'Gamma', 'Irand224', 'Normal', 'Normal01', 'Poisson', 'Uniform',
       'Uniform01', 'num', 'num0', 'ichar', 'char', 'length', 'substr', 'sprintf',
       'match', 'sub', 'gsub', 'print', 'printf', 'next', 'nextw', 'prev', 'prevw',
       'first', 'last', 'ord', 'ord0', 'card', 'arity', 'indexarity'),
                 prefix='\\b', suffix='\\b'), Name.Builtin),
              (
               '(\\+|\\-|\\*|/|\\*\\*|=|<=|>=|==|\\||\\^|<|>|\\!|\\.\\.|:=|\\&|\\!=|<<|>>)',
               Operator),
              (
               words(('or', 'exists', 'forall', 'and', 'in', 'not', 'within', 'union', 'diff', 'difference',
       'symdiff', 'inter', 'intersect', 'intersection', 'cross', 'setof', 'by', 'less',
       'sum', 'prod', 'product', 'div', 'mod'),
                 suffix='\\b'),
               Keyword.Reserved),
              (
               '(\\d+\\.(?!\\.)\\d*|\\.(?!.)\\d+)([eE][+-]?\\d+)?', Number.Float),
              (
               '\\d+([eE][+-]?\\d+)?', Number.Integer),
              (
               '[+-]?Infinity', Number.Integer),
              (
               '(\\w+|(\\.(?!\\.)))', Text)]}