# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/boa.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 3942 bytes
"""
    pygments.lexers.boa
    ~~~~~~~~~~~~~~~~~~~

    Lexers for the Boa language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, words
from pygments.token import String, Comment, Keyword, Name, Number, Text, Operator, Punctuation
__all__ = [
 'BoaLexer']
line_re = re.compile('.*?\n')

class BoaLexer(RegexLexer):
    __doc__ = '\n    Lexer for the `Boa <http://boa.cs.iastate.edu/docs/>`_ language.\n\n    .. versionadded:: 2.4\n    '
    name = 'Boa'
    aliases = ['boa']
    filenames = ['*.boa']
    reserved = words(('input', 'output', 'of', 'weight', 'before', 'after', 'stop',
                      'ifall', 'foreach', 'exists', 'function', 'break', 'switch',
                      'case', 'visitor', 'default', 'return', 'visit', 'while', 'if',
                      'else'),
      suffix='\\b',
      prefix='\\b')
    keywords = words(('bottom', 'collection', 'maximum', 'mean', 'minimum', 'set',
                      'sum', 'top', 'string', 'int', 'bool', 'float', 'time', 'false',
                      'true', 'array', 'map', 'stack', 'enum', 'type'),
      suffix='\\b', prefix='\\b')
    classes = words(('Project', 'ForgeKind', 'CodeRepository', 'Revision', 'RepositoryKind',
                     'ChangedFile', 'FileKind', 'ASTRoot', 'Namespace', 'Declaration',
                     'Type', 'Method', 'Variable', 'Statement', 'Expression', 'Modifier',
                     'StatementKind', 'ExpressionKind', 'ModifierKind', 'Visibility',
                     'TypeKind', 'Person', 'ChangeKind'),
      suffix='\\b',
      prefix='\\b')
    operators = ('->', ':=', ':', '=', '<<', '!', '++', '||', '&&', '+', '-', '*',
                 '>', '<')
    string_sep = ('`', '"')
    built_in_functions = words(('new', 'sort', 'yearof', 'dayofyear', 'hourof', 'minuteof',
                                'secondof', 'now', 'addday', 'addmonth', 'addweek',
                                'addyear', 'dayofmonth', 'dayofweek', 'dayofyear',
                                'formattime', 'trunctoday', 'trunctohour', 'trunctominute',
                                'trunctomonth', 'trunctosecond', 'trunctoyear', 'clear',
                                'haskey', 'keys', 'lookup', 'remove', 'values', 'abs',
                                'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2',
                                'atanh', 'ceil', 'cos', 'cosh', 'exp', 'floor', 'highbit',
                                'isfinite', 'isinf', 'isnan', 'isnormal', 'log',
                                'log10', 'max', 'min', 'nrand', 'pow', 'rand', 'round',
                                'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc', 'def',
                                'hash', 'len', 'add', 'contains', 'remove', 'format',
                                'lowercase', 'match', 'matchposns', 'matchstrs',
                                'regex', 'split', 'splitall', 'splitn', 'strfind',
                                'strreplace', 'strrfind', 'substring', 'trim', 'uppercase',
                                'bool', 'float', 'int', 'string', 'time', 'getast',
                                'getsnapshot', 'hasfiletype', 'isfixingrevision',
                                'iskind', 'isliteral'),
      prefix='\\b',
      suffix='\\(')
    tokens = {'root': [
              (
               '#.*?$', Comment.Single),
              (
               '/\\*.*?\\*/', Comment.Multiline),
              (
               reserved, Keyword.Reserved),
              (
               built_in_functions, Name.Function),
              (
               keywords, Keyword.Type),
              (
               classes, Name.Classes),
              (
               words(operators), Operator),
              (
               '[][(),;{}\\\\.]', Punctuation),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               '`(\\\\\\\\|\\\\`|[^`])*`', String),
              (
               words(string_sep), String.Delimeter),
              (
               '[a-zA-Z_]+', Name.Variable),
              (
               '[0-9]+', Number.Integer),
              (
               '\\s+?', Text)]}