# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/monte.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 6307 bytes
"""
    pygments.lexers.monte
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Monte programming language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.token import Comment, Error, Keyword, Name, Number, Operator, Punctuation, String, Whitespace
from pygments.lexer import RegexLexer, include, words
__all__ = [
 'MonteLexer']
_declarations = [
 'bind', 'def', 'fn', 'object']
_methods = ['method', 'to']
_keywords = [
 'as', 'break', 'catch', 'continue', 'else', 'escape', 'exit', 'exports',
 'extends', 'finally', 'for', 'guards', 'if', 'implements', 'import',
 'in', 'match', 'meta', 'pass', 'return', 'switch', 'try', 'via', 'when',
 'while']
_operators = [
 '~', '!',
 '+', '-', '*', '/', '%', '**', '&', '|', '^', '<<', '>>',
 '+=', '-=', '*=', '/=', '%=', '**=', '&=', '|=', '^=', '<<=', '>>=',
 '==', '!=', '<', '<=', '>', '>=', '<=>',
 ':=', '?', '=~', '!~', '=>',
 '.', '<-', '->']
_escape_pattern = '(?:\\\\x[0-9a-fA-F]{2}|\\\\u[0-9a-fA-F]{4}|\\\\U[0-9a-fA-F]{8}|\\\\["\\\'\\\\bftnr])'
_identifier = '[_a-zA-Z]\\w*'
_constants = [
 'null',
 'false', 'true',
 'Infinity', 'NaN',
 'M', 'Ref', 'throw', 'traceln']
_guards = [
 'Any', 'Binding', 'Bool', 'Bytes', 'Char', 'DeepFrozen', 'Double',
 'Empty', 'Int', 'List', 'Map', 'Near', 'NullOk', 'Same', 'Selfless',
 'Set', 'Str', 'SubrangeGuard', 'Transparent', 'Void']
_safeScope = [
 '_accumulateList', '_accumulateMap', '_auditedBy', '_bind',
 '_booleanFlow', '_comparer', '_equalizer', '_iterForever', '_loop',
 '_makeBytes', '_makeDouble', '_makeFinalSlot', '_makeInt', '_makeList',
 '_makeMap', '_makeMessageDesc', '_makeOrderedSpace', '_makeParamDesc',
 '_makeProtocolDesc', '_makeSourceSpan', '_makeString', '_makeVarSlot',
 '_makeVerbFacet', '_mapExtract', '_matchSame', '_quasiMatcher',
 '_slotToBinding', '_splitList', '_suchThat', '_switchFailed',
 '_validateFor', 'b__quasiParser', 'eval', 'import', 'm__quasiParser',
 'makeBrandPair', 'makeLazySlot', 'safeScope', 'simple__quasiParser']

class MonteLexer(RegexLexer):
    __doc__ = '\n    Lexer for the `Monte <https://monte.readthedocs.io/>`_ programming language.\n\n    .. versionadded:: 2.2\n    '
    name = 'Monte'
    aliases = ['monte']
    filenames = ['*.mt']
    tokens = {'root':[
      (
       '#[^\\n]*\\n', Comment),
      (
       '/\\*\\*.*?\\*/', String.Doc),
      (
       '\\bvar\\b', Keyword.Declaration, 'var'),
      (
       '\\binterface\\b', Keyword.Declaration, 'interface'),
      (
       words(_methods, prefix='\\b', suffix='\\b'),
       Keyword, 'method'),
      (
       words(_declarations, prefix='\\b', suffix='\\b'),
       Keyword.Declaration),
      (
       words(_keywords, prefix='\\b', suffix='\\b'), Keyword),
      (
       '[+-]?0x[_0-9a-fA-F]+', Number.Hex),
      (
       '[+-]?[_0-9]+\\.[_0-9]*([eE][+-]?[_0-9]+)?', Number.Float),
      (
       '[+-]?[_0-9]+', Number.Integer),
      (
       "'", String.Double, 'char'),
      (
       '"', String.Double, 'string'),
      (
       '`', String.Backtick, 'ql'),
      (
       words(_operators), Operator),
      (
       _identifier + '=', Operator.Word),
      (
       words(_constants, prefix='\\b', suffix='\\b'),
       Keyword.Pseudo),
      (
       words(_guards, prefix='\\b', suffix='\\b'), Keyword.Type),
      (
       words(_safeScope, prefix='\\b', suffix='\\b'),
       Name.Builtin),
      (
       _identifier, Name),
      (
       '\\(|\\)|\\{|\\}|\\[|\\]|:|,', Punctuation),
      (
       ' +', Whitespace),
      (
       '=', Error)], 
     'char':[
      (
       "'", Error, 'root'),
      (
       _escape_pattern, String.Escape, 'charEnd'),
      (
       '.', String.Char, 'charEnd')], 
     'charEnd':[
      (
       "'", String.Char, '#pop:2'),
      (
       '.', Error)], 
     'interface':[
      (
       ' +', Whitespace),
      (
       _identifier, Name.Class, '#pop'),
      include('root')], 
     'method':[
      (
       ' +', Whitespace),
      (
       _identifier, Name.Function, '#pop'),
      include('root')], 
     'string':[
      (
       '"', String.Double, 'root'),
      (
       _escape_pattern, String.Escape),
      (
       '\\n', String.Double),
      (
       '.', String.Double)], 
     'ql':[
      (
       '`', String.Backtick, 'root'),
      (
       '\\$' + _escape_pattern, String.Escape),
      (
       '\\$\\$', String.Escape),
      (
       '@@', String.Escape),
      (
       '\\$\\{', String.Interpol, 'qlNest'),
      (
       '@\\{', String.Interpol, 'qlNest'),
      (
       '\\$' + _identifier, Name),
      (
       '@' + _identifier, Name),
      (
       '.', String.Backtick)], 
     'qlNest':[
      (
       '\\}', String.Interpol, '#pop'),
      include('root')], 
     'var':[
      (
       ' +', Whitespace),
      (
       _identifier, Name.Variable, '#pop'),
      include('root')]}