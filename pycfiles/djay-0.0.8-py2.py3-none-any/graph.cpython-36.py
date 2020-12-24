# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/graph.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 2756 bytes
"""
    pygments.lexers.graph
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for graph query languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, using, this
from pygments.token import Keyword, Punctuation, Comment, Operator, Name, String, Number, Whitespace
__all__ = [
 'CypherLexer']

class CypherLexer(RegexLexer):
    __doc__ = '\n    For `Cypher Query Language\n    <https://neo4j.com/docs/developer-manual/3.3/cypher/>`_\n\n    For the Cypher version in Neo4j 3.3\n\n    .. versionadded:: 2.0\n    '
    name = 'Cypher'
    aliases = ['cypher']
    filenames = ['*.cyp', '*.cypher']
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root':[
      include('comment'),
      include('keywords'),
      include('clauses'),
      include('relations'),
      include('strings'),
      include('whitespace'),
      include('barewords')], 
     'comment':[
      (
       '^.*//.*\\n', Comment.Single)], 
     'keywords':[
      (
       '(create|order|match|limit|set|skip|start|return|with|where|delete|foreach|not|by|true|false)\\b',
       Keyword)], 
     'clauses':[
      (
       '(all|any|as|asc|ascending|assert|call|case|create|create\\s+index|create\\s+unique|delete|desc|descending|distinct|drop\\s+constraint\\s+on|drop\\s+index\\s+on|end|ends\\s+with|fieldterminator|foreach|in|is\\s+node\\s+key|is\\s+null|is\\s+unique|limit|load\\s+csv\\s+from|match|merge|none|not|null|on\\s+match|on\\s+create|optional\\s+match|order\\s+by|remove|return|set|skip|single|start|starts\\s+with|then|union|union\\s+all|unwind|using\\s+periodic\\s+commit|yield|where|when|with)\\b',
       Keyword)], 
     'relations':[
      (
       '(-\\[)(.*?)(\\]->)', bygroups(Operator, using(this), Operator)),
      (
       '(<-\\[)(.*?)(\\]-)', bygroups(Operator, using(this), Operator)),
      (
       '(-\\[)(.*?)(\\]-)', bygroups(Operator, using(this), Operator)),
      (
       '-->|<--|\\[|\\]', Operator),
      (
       '<|>|<>|=|<=|=>|\\(|\\)|\\||:|,|;', Punctuation),
      (
       '[.*{}]', Punctuation)], 
     'strings':[
      (
       '"(?:\\\\[tbnrf\\\'"\\\\]|[^\\\\"])*"', String),
      (
       '`(?:``|[^`])+`', Name.Variable)], 
     'whitespace':[
      (
       '\\s+', Whitespace)], 
     'barewords':[
      (
       '[a-z]\\w*', Name),
      (
       '\\d+', Number)]}