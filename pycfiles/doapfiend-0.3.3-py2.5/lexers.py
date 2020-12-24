# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/doapfiend/lexers.py
# Compiled at: 2008-04-26 13:27:20
"""
    pygments.lexers.sw
    ==================

    Lexers for semantic web languages.

    :copyright: 2007 by Philip Cooper <philip.cooper@openvest.com>.
    :license: BSD, see LICENSE for more details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, Literal
__all__ = [
 'Notation3Lexer', 'SparqlLexer']

class Notation3Lexer(RegexLexer):
    """
    Lexer for the N3 / Turtle / NT
    """
    name = 'N3'
    aliases = ['n3', 'turtle']
    filenames = ['*.n3', '*.ttl', '*.NT']
    mimetypes = ['text/rdf+n3', 'application/x-turtle', 'application/n3']
    tokens = {'comments': [
                  (
                   '(\\s*#.*)', Comment)], 
       'root': [
              include('comments'),
              (
               '(\\s*@(?:prefix|base|keywords)\\s*)(\\w*:\\s+)?(<[^> ]*>\\s*\\.\\s*)',
               bygroups(Keyword, Name.Variable, Name.Namespace)),
              (
               '\\s*(<[^>]*\\>)', Name.Class, ('triple', 'predObj')),
              (
               '(\\s*[a-zA-Z_:][a-zA-Z0-9\\-_:]*\\s)',
               Name.Class, ('triple', 'predObj')),
              (
               '\\s*\\[\\]\\s*', Name.Class, ('triple', 'predObj'))], 
       'triple': [
                (
                 '\\s*\\.\\s*', Text, '#pop')], 
       'predObj': [
                 include('comments'),
                 (
                  '(\\s*[a-zA-Z_:][a-zA-Z0-9\\-_:]*\\b\\s*)', Operator, 'object'),
                 (
                  '\\s*(<[^>]*\\>)', Operator, 'object'),
                 (
                  '\\s*\\]\\s*', Text, '#pop'),
                 (
                  '(?=\\s*\\.\\s*)', Keyword, '#pop')], 
       'objList': [
                 (
                  '\\s*\\)', Text, '#pop'),
                 include('object')], 
       'object': [
                (
                 '\\s*\\[', Text, 'predObj'),
                (
                 '\\s*<[^> ]*>', Name.Attribute),
                (
                 '\\s*("""(?:.|\\n)*?""")(\\@[a-z]{2-4}|\\^\\^<?[a-zA-Z0-9\\-\\:_#/\\.]*>?)?\\s*',
                 bygroups(Literal.String, Text)),
                (
                 '\\s*".*?[^\\\\]"(?:\\@[a-z]{2-4}|\\^\\^<?[a-zA-Z0-9\\-\\:_#/\\.]*>?)?\\s*',
                 Literal.String),
                (
                 '\\s*[a-zA-Z0-9\\-_\\:]\\s*', Name.Attribute),
                (
                 '\\s*\\(', Text, 'objList'),
                (
                 '\\s*;\\s*\\n?', Text, '#pop'),
                (
                 '(?=\\s*\\])', Text, '#pop'),
                (
                 '(?=\\s*\\.)', Text, '#pop')]}


class SparqlLexer(RegexLexer):
    """
    Lexer for SPARQL Not Complete
    """
    name = 'SPARQL'
    aliases = ['sparql']
    filenames = ['*.sparql']
    mimetypes = ['text/x-sql']
    flags = re.IGNORECASE
    tokens = {'comments': [
                  (
                   '(\\s*#.*)', Comment)], 
       'root': [
              include('comments'),
              (
               '(\\s*(?:PREFIX|BASE)\\s+)(\\w*:\\w*)?(\\s*<[^> ]*>\\s*)',
               bygroups(Keyword, Name.Variable, Name.Namespace)),
              (
               '(\\s*#.*)', Comment),
              (
               '((?:SELECT|ASK|CONSTRUCT|DESCRIBE)\\s*(?:DISTINCT|REDUCED)?\\s*)((?:\\?[a-zA-Z0-9_-]+\\s*)+|\\*)(\\s*)',
               bygroups(Keyword, Name.Variable, Text)),
              (
               '(FROM\\s*(?:NAMED)?)(\\s*.*)', bygroups(Keyword, Text)),
              (
               '(WHERE)?\\s*({)', bygroups(Keyword, Text), 'graph'),
              (
               '(LIMIT|OFFSET)(\\s*[+-]?[0-9]+)',
               bygroups(Keyword, Literal.String))], 
       'graph': [
               (
                '\\s*(<[^>]*\\>)', Name.Class, ('triple', 'predObj')),
               (
                '(\\s*[a-zA-Z_0-9\\-]*:[a-zA-Z0-9\\-_]*\\s)',
                Name.Class, ('triple', 'predObj')),
               (
                '(\\s*\\?[a-zA-Z0-9_-]*)', Name.Variable, ('triple', 'predObj')),
               (
                '\\s*\\[\\]\\s*', Name.Class, ('triple', 'predObj')),
               (
                '\\s*(FILTER\\s*)((?:regex)?\\()', bygroups(Keyword, Text), 'filterExp'),
               (
                '\\s*}', Text, '#pop')], 
       'triple': [
                (
                 '(?=\\s*})', Text, '#pop'),
                (
                 '\\s*\\.\\s*', Text, '#pop')], 
       'predObj': [
                 include('comments'),
                 (
                  '(\\s*\\?[a-zA-Z0-9_-]*\\b\\s*)', Name.Variable, 'object'),
                 (
                  '(\\s*[a-zA-Z_:][a-zA-Z0-9\\-_:]*\\b\\s*)', Operator, 'object'),
                 (
                  '\\s*(<[^>]*\\>)', Operator, 'object'),
                 (
                  '\\s*\\]\\s*', Text, '#pop'),
                 (
                  '(?=\\s*\\.\\s*)', Keyword, '#pop')], 
       'objList': [
                 (
                  '\\s*\\)', Text, '#pop'),
                 include('object')], 
       'object': [
                include('variable'),
                (
                 '\\s*\\[', Text, 'predObj'),
                (
                 '\\s*<[^> ]*>', Name.Attribute),
                (
                 '\\s*("""(?:.|\\n)*?""")(\\@[a-z]{2-4}|\\^\\^<?[a-zA-Z0-9\\-\\:_#/\\.]*>?)?\\s*', bygroups(Literal.String, Text)),
                (
                 '\\s*".*?[^\\\\]"(?:\\@[a-z]{2-4}|\\^\\^<?[a-zA-Z0-9\\-\\:_#/\\.]*>?)?\\s*', Literal.String),
                (
                 '\\s*[a-zA-Z0-9\\-_\\:]\\s*', Name.Attribute),
                (
                 '\\s*\\(', Text, 'objList'),
                (
                 '\\s*;\\s*', Text, '#pop'),
                (
                 '(?=\\])', Text, '#pop'),
                (
                 '(?=\\.)', Text, '#pop')], 
       'variable': [
                  (
                   '(\\?[a-zA-Z0-9\\-_]+\\s*)', Name.Variable)], 
       'filterExp': [
                   include('variable'),
                   include('object'),
                   (
                    '\\s*[+*/<>=~!%&|-]+\\s*', Operator),
                   (
                    '\\s*\\)', Text, '#pop')]}