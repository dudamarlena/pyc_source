# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/fantom.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 9982 bytes
"""
    pygments.lexers.fantom
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Fantom language.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from string import Template
from pygments.lexer import RegexLexer, include, bygroups, using, this, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Literal
__all__ = [
 'FantomLexer']

class FantomLexer(RegexLexer):
    __doc__ = '\n    For Fantom source code.\n\n    .. versionadded:: 1.5\n    '
    name = 'Fantom'
    aliases = ['fan']
    filenames = ['*.fan']
    mimetypes = ['application/x-fantom']

    def s(str):
        return Template(str).substitute(dict(pod='[\\"\\w\\.]+', eos='\\n|;', id='[a-zA-Z_]\\w*', type='(?:\\[|[a-zA-Z_]|\\|)[:\\w\\[\\]|\\->?]*?'))

    tokens = {'comments': [
                  (
                   '(?s)/\\*.*?\\*/', Comment.Multiline),
                  (
                   '//.*?\\n', Comment.Single),
                  (
                   '\\*\\*.*?\\n', Comment.Special),
                  (
                   '#.*\\n', Comment.Single)], 
     
     'literals': [
                  (
                   '\\b-?[\\d_]+(ns|ms|sec|min|hr|day)', Number),
                  (
                   '\\b-?[\\d_]*\\.[\\d_]+(ns|ms|sec|min|hr|day)', Number),
                  (
                   '\\b-?(\\d+)?\\.\\d+(f|F|d|D)?', Number.Float),
                  (
                   '\\b-?0x[0-9a-fA-F_]+', Number.Hex),
                  (
                   '\\b-?[\\d_]+', Number.Integer),
                  (
                   "'\\\\.'|'[^\\\\]'|'\\\\u[0-9a-f]{4}'", String.Char),
                  (
                   '"', Punctuation, 'insideStr'),
                  (
                   '`', Punctuation, 'insideUri'),
                  (
                   '\\b(true|false|null)\\b', Keyword.Constant),
                  (
                   '(?:(\\w+)(::))?(\\w+)(<\\|)(.*?)(\\|>)',
                   bygroups(Name.Namespace, Punctuation, Name.Class, Punctuation, String, Punctuation)),
                  (
                   '(?:(\\w+)(::))?(\\w+)?(#)(\\w+)?',
                   bygroups(Name.Namespace, Punctuation, Name.Class, Punctuation, Name.Function)),
                  (
                   '\\[,\\]', Literal),
                  (
                   s('($type)(\\[,\\])'),
                   bygroups(using(this, state='inType'), Literal)),
                  (
                   '\\[:\\]', Literal),
                  (
                   s('($type)(\\[:\\])'),
                   bygroups(using(this, state='inType'), Literal))], 
     
     'insideStr': [
                   (
                    '\\\\\\\\', String.Escape),
                   (
                    '\\\\"', String.Escape),
                   (
                    '\\\\`', String.Escape),
                   (
                    '\\$\\w+', String.Interpol),
                   (
                    '\\$\\{.*?\\}', String.Interpol),
                   (
                    '"', Punctuation, '#pop'),
                   (
                    '.', String)], 
     
     'insideUri': [
                   (
                    '\\\\\\\\', String.Escape),
                   (
                    '\\\\"', String.Escape),
                   (
                    '\\\\`', String.Escape),
                   (
                    '\\$\\w+', String.Interpol),
                   (
                    '\\$\\{.*?\\}', String.Interpol),
                   (
                    '`', Punctuation, '#pop'),
                   (
                    '.', String.Backtick)], 
     
     'protectionKeywords': [
                            (
                             '\\b(public|protected|private|internal)\\b', Keyword)], 
     
     'typeKeywords': [
                      (
                       '\\b(abstract|final|const|native|facet|enum)\\b', Keyword)], 
     
     'methodKeywords': [
                        (
                         '\\b(abstract|native|once|override|static|virtual|final)\\b',
                         Keyword)], 
     
     'fieldKeywords': [
                       (
                        '\\b(abstract|const|final|native|override|static|virtual|readonly)\\b',
                        Keyword)], 
     
     'otherKeywords': [
                       (
                        words(('try', 'catch', 'throw', 'finally', 'for', 'if', 'else', 'while', 'as', 'is',
       'isnot', 'switch', 'case', 'default', 'continue', 'break', 'do', 'return',
       'get', 'set'), prefix='\\b', suffix='\\b'),
                        Keyword),
                       (
                        '\\b(it|this|super)\\b', Name.Builtin.Pseudo)], 
     
     'operators': [
                   (
                    '\\+\\+|\\-\\-|\\+|\\-|\\*|/|\\|\\||&&|<=>|<=|<|>=|>|=|!|\\[|\\]', Operator)], 
     
     'inType': [
                (
                 '[\\[\\]|\\->:?]', Punctuation),
                (
                 s('$id'), Name.Class),
                default('#pop')], 
     
     'root': [
              include('comments'),
              include('protectionKeywords'),
              include('typeKeywords'),
              include('methodKeywords'),
              include('fieldKeywords'),
              include('literals'),
              include('otherKeywords'),
              include('operators'),
              (
               'using\\b', Keyword.Namespace, 'using'),
              (
               '@\\w+', Name.Decorator, 'facet'),
              (
               '(class|mixin)(\\s+)(\\w+)', bygroups(Keyword, Text, Name.Class),
               'inheritance'),
              (
               s('($type)([ \\t]+)($id)(\\s*)(:=)'),
               bygroups(using(this, state='inType'), Text, Name.Variable, Text, Operator)),
              (
               s('($id)(\\s*)(:=)'),
               bygroups(Name.Variable, Text, Operator)),
              (
               s('(\\.|(?:\\->))($id)(\\s*)(\\()'),
               bygroups(Operator, Name.Function, Text, Punctuation),
               'insideParen'),
              (
               s('(\\.|(?:\\->))($id)'),
               bygroups(Operator, Name.Function)),
              (
               '(new)(\\s+)(make\\w*)(\\s*)(\\()',
               bygroups(Keyword, Text, Name.Function, Text, Punctuation),
               'insideMethodDeclArgs'),
              (
               s('($type)([ \\t]+)($id)(\\s*)(\\()'),
               bygroups(using(this, state='inType'), Text, Name.Function, Text, Punctuation),
               'insideMethodDeclArgs'),
              (
               s('($type)(\\s+)($id)(\\s*)(,)'),
               bygroups(using(this, state='inType'), Text, Name.Variable, Text, Punctuation)),
              (
               s('($type)(\\s+)($id)(\\s*)(\\->)(\\s*)($type)(\\|)'),
               bygroups(using(this, state='inType'), Text, Name.Variable, Text, Punctuation, Text, using(this, state='inType'), Punctuation)),
              (
               s('($type)(\\s+)($id)(\\s*)(\\|)'),
               bygroups(using(this, state='inType'), Text, Name.Variable, Text, Punctuation)),
              (
               s('($type)([ \\t]+)($id)'),
               bygroups(using(this, state='inType'), Text, Name.Variable)),
              (
               '\\(', Punctuation, 'insideParen'),
              (
               '\\{', Punctuation, 'insideBrace'),
              (
               '.', Text)], 
     
     'insideParen': [
                     (
                      '\\)', Punctuation, '#pop'),
                     include('root')], 
     
     'insideMethodDeclArgs': [
                              (
                               '\\)', Punctuation, '#pop'),
                              (
                               s('($type)(\\s+)($id)(\\s*)(\\))'),
                               bygroups(using(this, state='inType'), Text, Name.Variable, Text, Punctuation), '#pop'),
                              include('root')], 
     
     'insideBrace': [
                     (
                      '\\}', Punctuation, '#pop'),
                     include('root')], 
     
     'inheritance': [
                     (
                      '\\s+', Text),
                     (
                      ':|,', Punctuation),
                     (
                      '(?:(\\w+)(::))?(\\w+)',
                      bygroups(Name.Namespace, Punctuation, Name.Class)),
                     (
                      '\\{', Punctuation, '#pop')], 
     
     'using': [
               (
                '[ \\t]+', Text),
               (
                '(\\[)(\\w+)(\\])',
                bygroups(Punctuation, Comment.Special, Punctuation)),
               (
                '(\\")?([\\w.]+)(\\")?',
                bygroups(Punctuation, Name.Namespace, Punctuation)),
               (
                '::', Punctuation, 'usingClass'),
               default('#pop')], 
     
     'usingClass': [
                    (
                     '[ \\t]+', Text),
                    (
                     '(as)(\\s+)(\\w+)',
                     bygroups(Keyword.Declaration, Text, Name.Class), '#pop:2'),
                    (
                     '[\\w$]+', Name.Class),
                    default('#pop:2')], 
     
     'facet': [
               (
                '\\s+', Text),
               (
                '\\{', Punctuation, 'facetFields'),
               default('#pop')], 
     
     'facetFields': [
                     include('comments'),
                     include('literals'),
                     include('operators'),
                     (
                      '\\s+', Text),
                     (
                      '(\\s*)(\\w+)(\\s*)(=)', bygroups(Text, Name, Text, Operator)),
                     (
                      '\\}', Punctuation, '#pop'),
                     (
                      '.', Text)]}