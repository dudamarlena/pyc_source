# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/inferno.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 3117 bytes
"""
    pygments.lexers.inferno
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Inferno os and all the related stuff.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, default
from pygments.token import Punctuation, Text, Comment, Operator, Keyword, Name, String, Number
__all__ = [
 'LimboLexer']

class LimboLexer(RegexLexer):
    __doc__ = '\n    Lexer for `Limbo programming language <http://www.vitanuova.com/inferno/limbo.html>`_\n\n    TODO:\n        - maybe implement better var declaration highlighting\n        - some simple syntax error highlighting\n\n    .. versionadded:: 2.0\n    '
    name = 'Limbo'
    aliases = ['limbo']
    filenames = ['*.b']
    mimetypes = ['text/limbo']
    tokens = {'whitespace':[
      (
       '^(\\s*)([a-zA-Z_]\\w*:(\\s*)\\n)',
       bygroups(Text, Name.Label)),
      (
       '\\n', Text),
      (
       '\\s+', Text),
      (
       '#(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single)], 
     'string':[
      (
       '"', String, '#pop'),
      (
       '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|[0-7]{1,3})',
       String.Escape),
      (
       '[^\\\\"\\n]+', String),
      (
       '\\\\', String)], 
     'statements':[
      (
       '"', String, 'string'),
      (
       "'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'", String.Char),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+', Number.Float),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])', Number.Float),
      (
       '16r[0-9a-fA-F]+', Number.Hex),
      (
       '8r[0-7]+', Number.Oct),
      (
       '((([1-3]\\d)|([2-9]))r)?(\\d+)', Number.Integer),
      (
       '[()\\[\\],.]', Punctuation),
      (
       '[~!%^&*+=|?:<>/-]|(->)|(<-)|(=>)|(::)', Operator),
      (
       '(alt|break|case|continue|cyclic|do|else|exitfor|hd|if|implement|import|include|len|load|orpick|return|spawn|tagof|tl|to|while)\\b',
       Keyword),
      (
       '(byte|int|big|real|string|array|chan|list|adt|fn|ref|of|module|self|type)\\b',
       Keyword.Type),
      (
       '(con|iota|nil)\\b', Keyword.Constant),
      (
       '[a-zA-Z_]\\w*', Name)], 
     'statement':[
      include('whitespace'),
      include('statements'),
      (
       '[{}]', Punctuation),
      (
       ';', Punctuation, '#pop')], 
     'root':[
      include('whitespace'),
      default('statement')]}

    def analyse_text(text):
        if re.search('^implement \\w+;', text, re.MULTILINE):
            return 0.7