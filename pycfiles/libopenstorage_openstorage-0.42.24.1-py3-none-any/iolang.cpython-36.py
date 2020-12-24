# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/iolang.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 1905 bytes
"""
    pygments.lexers.iolang
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the Io language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number
__all__ = [
 'IoLexer']

class IoLexer(RegexLexer):
    __doc__ = '\n    For `Io <http://iolanguage.com/>`_ (a small, prototype-based\n    programming language) source.\n\n    .. versionadded:: 0.10\n    '
    name = 'Io'
    filenames = ['*.io']
    aliases = ['io']
    mimetypes = ['text/x-iosrc']
    tokens = {'root':[
      (
       '\\n', Text),
      (
       '\\s+', Text),
      (
       '//(.*?)\\n', Comment.Single),
      (
       '#(.*?)\\n', Comment.Single),
      (
       '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
      (
       '/\\+', Comment.Multiline, 'nestedcomment'),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       '::=|:=|=|\\(|\\)|;|,|\\*|-|\\+|>|<|@|!|/|\\||\\^|\\.|%|&|\\[|\\]|\\{|\\}',
       Operator),
      (
       '(clone|do|doFile|doString|method|for|if|else|elseif|then)\\b',
       Keyword),
      (
       '(nil|false|true)\\b', Name.Constant),
      (
       '(Object|list|List|Map|args|Sequence|Coroutine|File)\\b',
       Name.Builtin),
      (
       '[a-zA-Z_]\\w*', Name),
      (
       '(\\d+\\.?\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
      (
       '\\d+', Number.Integer)], 
     'nestedcomment':[
      (
       '[^+/]+', Comment.Multiline),
      (
       '/\\+', Comment.Multiline, '#push'),
      (
       '\\+/', Comment.Multiline, '#pop'),
      (
       '[+/]', Comment.Multiline)]}