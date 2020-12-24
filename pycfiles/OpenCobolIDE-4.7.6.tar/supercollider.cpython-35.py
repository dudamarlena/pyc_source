# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/supercollider.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 3539 bytes
"""
    pygments.lexers.supercollider
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for SuperCollider

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'SuperColliderLexer']

class SuperColliderLexer(RegexLexer):
    __doc__ = '\n    For `SuperCollider <http://supercollider.github.io/>`_ source code.\n\n    .. versionadded:: 2.1\n    '
    name = 'SuperCollider'
    aliases = ['sc', 'supercollider']
    filenames = ['*.sc', '*.scd']
    mimetypes = ['application/supercollider', 'text/supercollider']
    flags = re.DOTALL | re.MULTILINE
    tokens = {'commentsandwhitespace': [
                               (
                                '\\s+', Text),
                               (
                                '<!--', Comment),
                               (
                                '//.*?\\n', Comment.Single),
                               (
                                '/\\*.*?\\*/', Comment.Multiline)], 
     
     'slashstartsregex': [
                          include('commentsandwhitespace'),
                          (
                           '/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)',
                           String.Regex, '#pop'),
                          (
                           '(?=/)', Text, ('#pop', 'badregex')),
                          (
                           '', Text, '#pop')], 
     
     'badregex': [
                  (
                   '\\n', Text, '#pop')], 
     
     'root': [
              (
               '^(?=\\s|/|<!--)', Text, 'slashstartsregex'),
              include('commentsandwhitespace'),
              (
               '\\+\\+|--|~|&&|\\?|:|\\|\\||\\\\(?=\\n)|(<<|>>>?|==?|!=?|[-<>+*%&|^/])=?',
               Operator, 'slashstartsregex'),
              (
               '[{(\\[;,]', Punctuation, 'slashstartsregex'),
              (
               '[})\\].]', Punctuation),
              (
               words(('for', 'in', 'while', 'do', 'break', 'return', 'continue', 'switch', 'case',
       'default', 'if', 'else', 'throw', 'try', 'catch', 'finally', 'new', 'delete',
       'typeof', 'instanceof', 'void'), suffix='\\b'),
               Keyword, 'slashstartsregex'),
              (
               words(('var', 'let', 'with', 'function', 'arg'), suffix='\\b'),
               Keyword.Declaration, 'slashstartsregex'),
              (
               words(('(abstract', 'boolean', 'byte', 'char', 'class', 'const', 'debugger', 'double',
       'enum', 'export', 'extends', 'final', 'float', 'goto', 'implements', 'import',
       'int', 'interface', 'long', 'native', 'package', 'private', 'protected', 'public',
       'short', 'static', 'super', 'synchronized', 'throws', 'transient', 'volatile'), suffix='\\b'),
               Keyword.Reserved),
              (
               words(('true', 'false', 'nil', 'inf'), suffix='\\b'), Keyword.Constant),
              (
               words(('Array', 'Boolean', 'Date', 'Error', 'Function', 'Number', 'Object', 'Packages',
       'RegExp', 'String', 'Error', 'isFinite', 'isNaN', 'parseFloat', 'parseInt',
       'super', 'thisFunctionDef', 'thisFunction', 'thisMethod', 'thisProcess', 'thisThread',
       'this'), suffix='\\b'),
               Name.Builtin),
              (
               '[$a-zA-Z_][a-zA-Z0-9_]*', Name.Other),
              (
               '\\\\?[$a-zA-Z_][a-zA-Z0-9_]*', String.Symbol),
              (
               '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
              (
               '0x[0-9a-fA-F]+', Number.Hex),
              (
               '[0-9]+', Number.Integer),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
              (
               "'(\\\\\\\\|\\\\'|[^'])*'", String.Single)]}