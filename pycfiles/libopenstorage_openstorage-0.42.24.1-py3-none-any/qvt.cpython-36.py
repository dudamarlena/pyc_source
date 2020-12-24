# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/qvt.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 6097 bytes
"""
    pygments.lexers.qvt
    ~~~~~~~~~~~~~~~~~~~

    Lexer for QVT Operational language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, bygroups, include, combined, default, words
from pygments.token import Text, Comment, Operator, Keyword, Punctuation, Name, String, Number
__all__ = [
 'QVToLexer']

class QVToLexer(RegexLexer):
    __doc__ = "\n    For the `QVT Operational Mapping language <http://www.omg.org/spec/QVT/1.1/>`_.\n\n    Reference for implementing this: «Meta Object Facility (MOF) 2.0\n    Query/View/Transformation Specification», Version 1.1 - January 2011\n    (http://www.omg.org/spec/QVT/1.1/), see §8.4, «Concrete Syntax» in\n    particular.\n\n    Notable tokens assignments:\n\n    - Name.Class is assigned to the identifier following any of the following\n      keywords: metamodel, class, exception, primitive, enum, transformation\n      or library\n\n    - Name.Function is assigned to the names of mappings and queries\n\n    - Name.Builtin.Pseudo is assigned to the pre-defined variables 'this',\n      'self' and 'result'.\n    "
    name = 'QVTO'
    aliases = ['qvto', 'qvt']
    filenames = ['*.qvto']
    tokens = {'root':[
      (
       '\\n', Text),
      (
       '[^\\S\\n]+', Text),
      (
       '(--|//)(\\s*)(directive:)?(.*)$',
       bygroups(Comment, Comment, Comment.Preproc, Comment)),
      (
       '/[*](.|\\n)*?[*]/', Comment.Multiline),
      (
       '\\\\\\n', Text),
      (
       '(and|not|or|xor|##?)\\b', Operator.Word),
      (
       '(:{1,2}=|[-+]=)\\b', Operator.Word),
      (
       '(@|<<|>>)\\b', Keyword),
      (
       '!=|<>|==|=|!->|->|>=|<=|[.]{3}|[+/*%=<>&|.~]', Operator),
      (
       '[]{}:(),;[]', Punctuation),
      (
       '(true|false|unlimited|null)\\b', Keyword.Constant),
      (
       '(this|self|result)\\b', Name.Builtin.Pseudo),
      (
       '(var)\\b', Keyword.Declaration),
      (
       '(from|import)\\b', Keyword.Namespace, 'fromimport'),
      (
       '(metamodel|class|exception|primitive|enum|transformation|library)(\\s+)(\\w+)',
       bygroups(Keyword.Word, Text, Name.Class)),
      (
       '(exception)(\\s+)(\\w+)',
       bygroups(Keyword.Word, Text, Name.Exception)),
      (
       '(main)\\b', Name.Function),
      (
       '(mapping|helper|query)(\\s+)',
       bygroups(Keyword.Declaration, Text), 'operation'),
      (
       '(assert)(\\s+)\\b', bygroups(Keyword, Text), 'assert'),
      (
       '(Bag|Collection|Dict|OrderedSet|Sequence|Set|Tuple|List)\\b',
       Keyword.Type),
      include('keywords'),
      (
       '"', String, combined('stringescape', 'dqs')),
      (
       "'", String, combined('stringescape', 'sqs')),
      include('name'),
      include('numbers')], 
     'fromimport':[
      (
       '(?:[ \\t]|\\\\\\n)+', Text),
      (
       '[a-zA-Z_][\\w.]*', Name.Namespace),
      default('#pop')], 
     'operation':[
      (
       '::', Text),
      (
       '(.*::)([a-zA-Z_]\\w*)([ \\t]*)(\\()',
       bygroups(Text, Name.Function, Text, Punctuation), '#pop')], 
     'assert':[
      (
       '(warning|error|fatal)\\b', Keyword, '#pop'),
      default('#pop')], 
     'keywords':[
      (
       words(('abstract', 'access', 'any', 'assert', 'blackbox', 'break', 'case', 'collect',
       'collectNested', 'collectOne', 'collectselect', 'collectselectOne', 'composes',
       'compute', 'configuration', 'constructor', 'continue', 'datatype', 'default',
       'derived', 'disjuncts', 'do', 'elif', 'else', 'end', 'endif', 'except', 'exists',
       'extends', 'forAll', 'forEach', 'forOne', 'from', 'if', 'implies', 'in', 'inherits',
       'init', 'inout', 'intermediate', 'invresolve', 'invresolveIn', 'invresolveone',
       'invresolveoneIn', 'isUnique', 'iterate', 'late', 'let', 'literal', 'log',
       'map', 'merges', 'modeltype', 'new', 'object', 'one', 'ordered', 'out', 'package',
       'population', 'property', 'raise', 'readonly', 'references', 'refines', 'reject',
       'resolve', 'resolveIn', 'resolveone', 'resolveoneIn', 'return', 'select',
       'selectOne', 'sortedBy', 'static', 'switch', 'tag', 'then', 'try', 'typedef',
       'unlimited', 'uses', 'when', 'where', 'while', 'with', 'xcollect', 'xmap',
       'xselect'),
         suffix='\\b'), Keyword)], 
     'strings':[
      (
       '[^\\\\\\\'"\\n]+', String),
      (
       '[\\\'"\\\\]', String)], 
     'stringescape':[
      (
       '\\\\([\\\\btnfr"\\\']|u[0-3][0-7]{2}|u[0-7]{1,2})', String.Escape)], 
     'dqs':[
      (
       '"', String, '#pop'),
      (
       '\\\\\\\\|\\\\"', String.Escape),
      include('strings')], 
     'sqs':[
      (
       "'", String, '#pop'),
      (
       "\\\\\\\\|\\\\'", String.Escape),
      include('strings')], 
     'name':[
      (
       '[a-zA-Z_]\\w*', Name)], 
     'numbers':[
      (
       '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
      (
       '\\d+[eE][+-]?[0-9]+', Number.Float),
      (
       '\\d+', Number.Integer)]}