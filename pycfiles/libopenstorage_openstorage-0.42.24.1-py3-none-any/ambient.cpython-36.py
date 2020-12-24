# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/ambient.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 2557 bytes
"""
    pygments.lexers.ambient
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for AmbientTalk language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'AmbientTalkLexer']

class AmbientTalkLexer(RegexLexer):
    __doc__ = '\n    Lexer for `AmbientTalk <https://code.google.com/p/ambienttalk>`_ source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'AmbientTalk'
    filenames = ['*.at']
    aliases = ['at', 'ambienttalk', 'ambienttalk/2']
    mimetypes = ['text/x-ambienttalk']
    flags = re.MULTILINE | re.DOTALL
    builtin = words(('if:', 'then:', 'else:', 'when:', 'whenever:', 'discovered:',
                     'disconnected:', 'reconnected:', 'takenOffline:', 'becomes:',
                     'export:', 'as:', 'object:', 'actor:', 'mirror:', 'taggedAs:',
                     'mirroredBy:', 'is:'))
    tokens = {'root':[
      (
       '\\s+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '(def|deftype|import|alias|exclude)\\b', Keyword),
      (
       builtin, Name.Builtin),
      (
       '(true|false|nil)\\b', Keyword.Constant),
      (
       '(~|lobby|jlobby|/)\\.', Keyword.Constant, 'namespace'),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       '\\|', Punctuation, 'arglist'),
      (
       '<:|[*^!%&<>+=,./?-]|:=', Operator),
      (
       '`[a-zA-Z_]\\w*', String.Symbol),
      (
       '[a-zA-Z_]\\w*:', Name.Function),
      (
       '[{}()\\[\\];`]', Punctuation),
      (
       '(self|super)\\b', Name.Variable.Instance),
      (
       '[a-zA-Z_]\\w*', Name.Variable),
      (
       '@[a-zA-Z_]\\w*', Name.Class),
      (
       '@\\[', Name.Class, 'annotations'),
      include('numbers')], 
     'numbers':[
      (
       '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
      (
       '\\d+', Number.Integer)], 
     'namespace':[
      (
       '[a-zA-Z_]\\w*\\.', Name.Namespace),
      (
       '[a-zA-Z_]\\w*:', Name.Function, '#pop'),
      (
       '[a-zA-Z_]\\w*(?!\\.)', Name.Function, '#pop')], 
     'annotations':[
      (
       '(.*?)\\]', Name.Class, '#pop')], 
     'arglist':[
      (
       '\\|', Punctuation, '#pop'),
      (
       '\\s*(,)\\s*', Punctuation),
      (
       '[a-zA-Z_]\\w*', Name.Variable)]}