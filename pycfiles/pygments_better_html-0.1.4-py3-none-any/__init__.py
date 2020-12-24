# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pygments_arm/__init__.py
# Compiled at: 2018-04-12 08:38:05
__doc__ = '\n    ARM lexer\n    ~~~~~~~~~\n\n    Pygments lexer for ARM Assembly.\n\n    :copyright: Copyright 2017 Jacques Supcik\n    :license: Apache 2, see LICENSE for details.\n'
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