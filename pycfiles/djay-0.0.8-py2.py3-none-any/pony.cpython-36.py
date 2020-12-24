# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/pony.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 3269 bytes
"""
    pygments.lexers.pony
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for Pony and related languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'PonyLexer']

class PonyLexer(RegexLexer):
    __doc__ = '\n    For Pony source code.\n\n    .. versionadded:: 2.4\n    '
    name = 'Pony'
    aliases = ['pony']
    filenames = ['*.pony']
    _caps = '(iso|trn|ref|val|box|tag)'
    tokens = {'root':[
      (
       '\\n', Text),
      (
       '[^\\S\\n]+', Text),
      (
       '//.*\\n', Comment.Single),
      (
       '/\\*', Comment.Multiline, 'nested_comment'),
      (
       '"""(?:.|\\n)*?"""', String.Doc),
      (
       '"', String, 'string'),
      (
       "\\'.*\\'", String.Char),
      (
       '=>|[]{}:().~;,|&!^?[]', Punctuation),
      (
       words(('addressof', 'and', 'as', 'consume', 'digestof', 'is', 'isnt', 'not', 'or'),
         suffix='\\b'),
       Operator.Word),
      (
       '!=|==|<<|>>|[-+/*%=<>]', Operator),
      (
       words(('box', 'break', 'compile_error', 'compile_intrinsic', 'continue', 'do', 'else',
       'elseif', 'embed', 'end', 'error', 'for', 'if', 'ifdef', 'in', 'iso', 'lambda',
       'let', 'match', 'object', 'recover', 'ref', 'repeat', 'return', 'tag', 'then',
       'this', 'trn', 'try', 'until', 'use', 'var', 'val', 'where', 'while', 'with',
       '#any', '#read', '#send', '#share'),
         suffix='\\b'),
       Keyword),
      (
       '(actor|class|struct|primitive|interface|trait|type)((?:\\s)+)',
       bygroups(Keyword, Text), 'typename'),
      (
       '(new|fun|be)((?:\\s)+)', bygroups(Keyword, Text), 'methodname'),
      (
       words(('I8', 'U8', 'I16', 'U16', 'I32', 'U32', 'I64', 'U64', 'I128', 'U128', 'ILong',
       'ULong', 'ISize', 'USize', 'F32', 'F64', 'Bool', 'Pointer', 'None', 'Any',
       'Array', 'String', 'Iterator'),
         suffix='\\b'),
       Name.Builtin.Type),
      (
       '_?[A-Z]\\w*', Name.Type),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+', Number.Float),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '\\d+', Number.Integer),
      (
       '(true|false)\\b', Name.Builtin),
      (
       '_\\d*', Name),
      (
       "_?[a-z][\\w\\'_]*", Name)], 
     'typename':[
      (
       _caps + '?((?:\\s)*)(_?[A-Z]\\w*)',
       bygroups(Keyword, Text, Name.Class), '#pop')], 
     'methodname':[
      (
       _caps + '?((?:\\s)*)(_?[a-z]\\w*)',
       bygroups(Keyword, Text, Name.Function), '#pop')], 
     'nested_comment':[
      (
       '[^*/]+', Comment.Multiline),
      (
       '/\\*', Comment.Multiline, '#push'),
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '[*/]', Comment.Multiline)], 
     'string':[
      (
       '"', String, '#pop'),
      (
       '\\\\"', String),
      (
       '[^\\\\"]+', String)]}