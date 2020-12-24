# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/nit.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 2743 bytes
"""
    pygments.lexers.nit
    ~~~~~~~~~~~~~~~~~~~

    Lexer for the Nit language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'NitLexer']

class NitLexer(RegexLexer):
    __doc__ = '\n    For `nit <http://nitlanguage.org>`_ source.\n\n    .. versionadded:: 2.0\n    '
    name = 'Nit'
    aliases = ['nit']
    filenames = ['*.nit']
    tokens = {'root': [
              (
               '#.*?$', Comment.Single),
              (
               words(('package', 'module', 'import', 'class', 'abstract', 'interface', 'universal',
       'enum', 'end', 'fun', 'type', 'init', 'redef', 'isa', 'do', 'readable', 'writable',
       'var', 'intern', 'extern', 'public', 'protected', 'private', 'intrude', 'if',
       'then', 'else', 'while', 'loop', 'for', 'in', 'and', 'or', 'not', 'implies',
       'return', 'continue', 'break', 'abort', 'assert', 'new', 'is', 'once', 'super',
       'self', 'true', 'false', 'nullable', 'null', 'as', 'isset', 'label', '__debug__'),
                 suffix='(?=[\\r\\n\\t( ])'),
               Keyword),
              (
               '[A-Z]\\w*', Name.Class),
              (
               '"""(([^\\\'\\\\]|\\\\.)|\\\\r|\\\\n)*((\\{\\{?)?(""?\\{\\{?)*""""*)', String),
              (
               "\\'\\'\\'(((\\\\.|[^\\'\\\\])|\\\\r|\\\\n)|\\'((\\\\.|[^\\'\\\\])|\\\\r|\\\\n)|\\'\\'((\\\\.|[^\\'\\\\])|\\\\r|\\\\n))*\\'\\'\\'",
               String),
              (
               '"""(([^\\\'\\\\]|\\\\.)|\\\\r|\\\\n)*((""?)?(\\{\\{?""?)*\\{\\{\\{\\{*)', String),
              (
               '\\}\\}\\}(((\\\\.|[^\\\'\\\\])|\\\\r|\\\\n))*(""?)?(\\{\\{?""?)*\\{\\{\\{\\{*', String),
              (
               '\\}\\}\\}(((\\\\.|[^\\\'\\\\])|\\\\r|\\\\n))*(\\{\\{?)?(""?\\{\\{?)*""""*', String),
              (
               '"(\\\\.|([^"}{\\\\]))*"', String),
              (
               '"(\\\\.|([^"}{\\\\]))*\\{', String),
              (
               '\\}(\\\\.|([^"}{\\\\]))*\\{', String),
              (
               '\\}(\\\\.|([^"}{\\\\]))*"', String),
              (
               "(\\'[^\\'\\\\]\\')|(\\'\\\\.\\')", String.Char),
              (
               '[0-9]+', Number.Integer),
              (
               '[0-9]*.[0-9]+', Number.Float),
              (
               '0(x|X)[0-9A-Fa-f]+', Number.Hex),
              (
               '[a-z]\\w*', Name),
              (
               '_\\w+', Name.Variable.Instance),
              (
               '==|!=|<==>|>=|>>|>|<=|<<|<|\\+|-|=|/|\\*|%|\\+=|-=|!|@', Operator),
              (
               '\\(|\\)|\\[|\\]|,|\\.\\.\\.|\\.\\.|\\.|::|:', Punctuation),
              (
               '`\\{[^`]*`\\}', Text),
              (
               '[\\r\\n\\t ]+', Text)]}