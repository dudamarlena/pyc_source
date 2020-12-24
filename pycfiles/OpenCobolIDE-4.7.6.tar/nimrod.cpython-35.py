# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/nimrod.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 5105 bytes
"""
    pygments.lexers.nimrod
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Nimrod language.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
__all__ = [
 'NimrodLexer']

class NimrodLexer(RegexLexer):
    __doc__ = '\n    For `Nimrod <http://nimrod-code.org/>`_ source code.\n\n    .. versionadded:: 1.5\n    '
    name = 'Nimrod'
    aliases = ['nimrod', 'nim']
    filenames = ['*.nim', '*.nimrod']
    mimetypes = ['text/x-nimrod']
    flags = re.MULTILINE | re.IGNORECASE | re.UNICODE

    def underscorize(words):
        newWords = []
        new = ''
        for word in words:
            for ch in word:
                new += ch + '_?'

            newWords.append(new)
            new = ''

        return '|'.join(newWords)

    keywords = [
     'addr', 'and', 'as', 'asm', 'atomic', 'bind', 'block', 'break',
     'case', 'cast', 'const', 'continue', 'converter', 'discard',
     'distinct', 'div', 'elif', 'else', 'end', 'enum', 'except', 'finally',
     'for', 'generic', 'if', 'implies', 'in', 'yield',
     'is', 'isnot', 'iterator', 'lambda', 'let', 'macro', 'method',
     'mod', 'not', 'notin', 'object', 'of', 'or', 'out', 'proc',
     'ptr', 'raise', 'ref', 'return', 'shl', 'shr', 'template', 'try',
     'tuple', 'type', 'when', 'while', 'with', 'without', 'xor']
    keywordsPseudo = [
     'nil', 'true', 'false']
    opWords = [
     'and', 'or', 'not', 'xor', 'shl', 'shr', 'div', 'mod', 'in',
     'notin', 'is', 'isnot']
    types = [
     'int', 'int8', 'int16', 'int32', 'int64', 'float', 'float32', 'float64',
     'bool', 'char', 'range', 'array', 'seq', 'set', 'string']
    tokens = {'root': [
              (
               '##.*$', String.Doc),
              (
               '#.*$', Comment),
              (
               '[*=><+\\-/@$~&%!?|\\\\\\[\\]]', Operator),
              (
               '\\.\\.|\\.|,|\\[\\.|\\.\\]|\\{\\.|\\.\\}|\\(\\.|\\.\\)|\\{|\\}|\\(|\\)|:|\\^|`|;',
               Punctuation),
              (
               '(?:[\\w]+)"', String, 'rdqs'),
              (
               '"""', String, 'tdqs'),
              (
               '"', String, 'dqs'),
              (
               "'", String.Char, 'chars'),
              (
               '(%s)\\b' % underscorize(opWords), Operator.Word),
              (
               '(p_?r_?o_?c_?\\s)(?![(\\[\\]])', Keyword, 'funcname'),
              (
               '(%s)\\b' % underscorize(keywords), Keyword),
              (
               '(%s)\\b' % underscorize(['from', 'import', 'include']),
               Keyword.Namespace),
              (
               '(v_?a_?r)\\b', Keyword.Declaration),
              (
               '(%s)\\b' % underscorize(types), Keyword.Type),
              (
               '(%s)\\b' % underscorize(keywordsPseudo), Keyword.Pseudo),
              (
               '\\b((?![_\\d])\\w)(((?!_)\\w)|(_(?!_)\\w))*', Name),
              (
               "[0-9][0-9_]*(?=([e.]|\\'f(32|64)))",
               Number.Float, ('float-suffix', 'float-number')),
              (
               '0x[a-f0-9][a-f0-9_]*', Number.Hex, 'int-suffix'),
              (
               '0b[01][01_]*', Number.Bin, 'int-suffix'),
              (
               '0o[0-7][0-7_]*', Number.Oct, 'int-suffix'),
              (
               '[0-9][0-9_]*', Number.Integer, 'int-suffix'),
              (
               '\\s+', Text),
              (
               '.+$', Error)], 
     
     'chars': [
               (
                '\\\\([\\\\abcefnrtvl"\\\']|x[a-f0-9]{2}|[0-9]{1,3})', String.Escape),
               (
                "'", String.Char, '#pop'),
               (
                '.', String.Char)], 
     
     'strings': [
                 (
                  '(?<!\\$)\\$(\\d+|#|\\w+)+', String.Interpol),
                 (
                  '[^\\\\\\\'"$\\n]+', String),
                 (
                  '[\\\'"\\\\]', String),
                 (
                  '\\$', String)], 
     
     'dqs': [
             (
              '\\\\([\\\\abcefnrtvl"\\\']|\\n|x[a-f0-9]{2}|[0-9]{1,3})',
              String.Escape),
             (
              '"', String, '#pop'),
             include('strings')], 
     
     'rdqs': [
              (
               '"(?!")', String, '#pop'),
              (
               '""', String.Escape),
              include('strings')], 
     
     'tdqs': [
              (
               '"""(?!")', String, '#pop'),
              include('strings'),
              include('nl')], 
     
     'funcname': [
                  (
                   '((?![\\d_])\\w)(((?!_)\\w)|(_(?!_)\\w))*', Name.Function, '#pop'),
                  (
                   '`.+`', Name.Function, '#pop')], 
     
     'nl': [
            (
             '\\n', String)], 
     
     'float-number': [
                      (
                       '\\.(?!\\.)[0-9_]*', Number.Float),
                      (
                       'e[+-]?[0-9][0-9_]*', Number.Float),
                      default('#pop')], 
     
     'float-suffix': [
                      (
                       "\\'f(32|64)", Number.Float),
                      default('#pop')], 
     
     'int-suffix': [
                    (
                     "\\'i(32|64)", Number.Integer.Long),
                    (
                     "\\'i(8|16)", Number.Integer),
                    default('#pop')]}