# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pygments_arm/__init__.py
# Compiled at: 2018-04-12 08:38:05
"""
    ARM lexer
    ~~~~~~~~~

    Pygments lexer for ARM Assembly.

    :copyright: Copyright 2017 Jacques Supcik
    :license: Apache 2, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include
from pygments.token import Text, Name, Number, String, Comment, Punctuation
__all__ = [
 'ArmLexer']

class ArmLexer(RegexLexer):
    name = 'ARM'
    aliases = ['arm']
    filenames = ['*.S']
    string = '"(\\\\"|[^"])*"'
    char = '[\\w$.@-]'
    identifier = '(?:[a-zA-Z$_]' + char + '*|\\.' + char + '+)'
    number = '(?:0[xX][a-zA-Z0-9]+|\\d+)'
    tokens = {'root': [
              include('whitespace'),
              (
               identifier + ':', Name.Label),
              (
               number + ':', Name.Label),
              (
               '[.#]' + identifier, Name.Attribute, 'directive-args'),
              (
               identifier, Name.Function, 'instruction-args'),
              (
               '[\\r\\n]+', Text)], 
       'directive-args': [
                        (
                         identifier, Name.Constant),
                        (
                         string, String),
                        (
                         number, Number.Integer),
                        (
                         '[\\r\\n]+', Text, '#pop'),
                        include('punctuation'),
                        include('whitespace')], 
       'instruction-args': [
                          (
                           identifier, Name.Constant),
                          (
                           number, Number.Integer),
                          (
                           'r[rR]\\d+', Name.Variable),
                          (
                           "'(.|\\\\')'?", String.Char),
                          (
                           '[\\r\\n]+', Text, '#pop'),
                          include('punctuation'),
                          include('whitespace')], 
       'whitespace': [
                    (
                     '[ \\t]', Text),
                    (
                     '//[\\w\\W]*?(?=\\n)', Comment.Single),
                    (
                     '/[*][\\w\\W]*?[*]/', Comment.Multiline),
                    (
                     '[;@].*?(?=\\n)', Comment.Single)], 
       'punctuation': [
                     (
                      '[-*,.()\\[\\]!:{}^=#\\+\\\\]+', Punctuation)], 
       'eol': [
             (
              '[\\r\\n]+', Text)]}