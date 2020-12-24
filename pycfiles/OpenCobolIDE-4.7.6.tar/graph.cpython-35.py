# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/graph.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 2370 bytes
"""
    pygments.lexers.graph
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for graph query languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, using, this
from pygments.token import Keyword, Punctuation, Comment, Operator, Name, String, Number, Whitespace
__all__ = [
 'CypherLexer']

class CypherLexer(RegexLexer):
    __doc__ = '\n    For `Cypher Query Language\n    <http://docs.neo4j.org/chunked/milestone/cypher-query-lang.html>`_\n\n    For the Cypher version in Neo4J 2.0\n\n    .. versionadded:: 2.0\n    '
    name = 'Cypher'
    aliases = ['cypher']
    filenames = ['*.cyp', '*.cypher']
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [
              include('comment'),
              include('keywords'),
              include('clauses'),
              include('relations'),
              include('strings'),
              include('whitespace'),
              include('barewords')], 
     
     'comment': [
                 (
                  '^.*//.*\\n', Comment.Single)], 
     
     'keywords': [
                  (
                   '(create|order|match|limit|set|skip|start|return|with|where|delete|foreach|not|by)\\b',
                   Keyword)], 
     
     'clauses': [
                 (
                  '(all|any|as|asc|create|create\\s+unique|delete|desc|distinct|foreach|in|is\\s+null|limit|match|none|order\\s+by|return|set|skip|single|start|union|where|with)\\b',
                  Keyword)], 
     
     'relations': [
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
     
     'strings': [
                 (
                  '"(?:\\\\[tbnrf\\\'"\\\\]|[^\\\\"])*"', String),
                 (
                  '`(?:``|[^`])+`', Name.Variable)], 
     
     'whitespace': [
                    (
                     '\\s+', Whitespace)], 
     
     'barewords': [
                   (
                    '[a-z]\\w*', Name),
                   (
                    '\\d+', Number)]}