# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/elm.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 2996 bytes
"""
    pygments.lexers.elm
    ~~~~~~~~~~~~~~~~~~~

    Lexer for the Elm programming language.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, words, include
from pygments.token import Comment, Keyword, Name, Number, Punctuation, String, Text
__all__ = [
 'ElmLexer']

class ElmLexer(RegexLexer):
    __doc__ = '\n    For `Elm <http://elm-lang.org/>`_ source code.\n\n    .. versionadded:: 2.1\n    '
    name = 'Elm'
    aliases = ['elm']
    filenames = ['*.elm']
    mimetypes = ['text/x-elm']
    validName = "[a-z_][a-zA-Z_\\']*"
    specialName = '^main '
    builtinOps = ('~', '||', '|>', '|', '`', '^', '\\', "'", '>>', '>=', '>', '==',
                  '=', '<~', '<|', '<=', '<<', '<-', '<', '::', ':', '/=', '//',
                  '/', '..', '.', '->', '-', '++', '+', '*', '&&', '%')
    reservedWords = words(('alias', 'as', 'case', 'else', 'if', 'import', 'in', 'let',
                           'module', 'of', 'port', 'then', 'type', 'where'), suffix='\\b')
    tokens = {'root': [
              (
               '{-', Comment.Multiline, 'comment'),
              (
               '--.*', Comment.Single),
              (
               '\\s+', Text),
              (
               '"', String, 'doublequote'),
              (
               '^\\s*module\\s*', Keyword.Namespace, 'imports'),
              (
               '^\\s*import\\s*', Keyword.Namespace, 'imports'),
              (
               '\\[glsl\\|.*', Name.Entity, 'shader'),
              (
               reservedWords, Keyword.Reserved),
              (
               '[A-Z]\\w*', Keyword.Type),
              (
               specialName, Keyword.Reserved),
              (
               words(builtinOps, prefix='\\(', suffix='\\)'), Name.Function),
              (
               words(builtinOps), Name.Function),
              include('numbers'),
              (
               validName, Name.Variable),
              (
               '[,\\(\\)\\[\\]{}]', Punctuation)], 
     
     'comment': [
                 (
                  '-(?!})', Comment.Multiline),
                 (
                  '{-', Comment.Multiline, 'comment'),
                 (
                  '[^-}]', Comment.Multiline),
                 (
                  '-}', Comment.Multiline, '#pop')], 
     
     'doublequote': [
                     (
                      '\\\\u[0-9a-fA-F]\\{4}', String.Escape),
                     (
                      '\\\\[nrfvb\\\\\\"]', String.Escape),
                     (
                      '[^"]', String),
                     (
                      '"', String, '#pop')], 
     
     'imports': [
                 (
                  '\\w+(\\.\\w+)*', Name.Class, '#pop')], 
     
     'numbers': [
                 (
                  '_?\\d+\\.(?=\\d+)', Number.Float),
                 (
                  '_?\\d+', Number.Integer)], 
     
     'shader': [
                (
                 '\\|(?!\\])', Name.Entity),
                (
                 '\\|\\]', Name.Entity, '#pop'),
                (
                 '.*\\n', Name.Entity)]}