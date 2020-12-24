# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/nix.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 4031 bytes
"""
    pygments.lexers.nix
    ~~~~~~~~~~~~~~~~~~~

    Lexers for the NixOS Nix language.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Literal
__all__ = [
 'NixLexer']

class NixLexer(RegexLexer):
    __doc__ = '\n    For the `Nix language <http://nixos.org/nix/>`_.\n\n    .. versionadded:: 2.0\n    '
    name = 'Nix'
    aliases = ['nixos', 'nix']
    filenames = ['*.nix']
    mimetypes = ['text/x-nix']
    flags = re.MULTILINE | re.UNICODE
    keywords = [
     'rec', 'with', 'let', 'in', 'inherit', 'assert', 'if',
     'else', 'then', '...']
    builtins = ['import', 'abort', 'baseNameOf', 'dirOf', 'isNull', 'builtins',
     'map', 'removeAttrs', 'throw', 'toString', 'derivation']
    operators = ['++', '+', '?', '.', '!', '//', '==',
     '!=', '&&', '||', '->', '=']
    punctuations = [
     '(', ')', '[', ']', ';', '{', '}', ':', ',', '@']
    tokens = {'root': [
              (
               '#.*$', Comment.Single),
              (
               '/\\*', Comment.Multiline, 'comment'),
              (
               '\\s+', Text),
              (
               '(%s)' % '|'.join(re.escape(entry) + '\\b' for entry in keywords), Keyword),
              (
               '(%s)' % '|'.join(re.escape(entry) + '\\b' for entry in builtins),
               Name.Builtin),
              (
               '\\b(true|false|null)\\b', Name.Constant),
              (
               '(%s)' % '|'.join(re.escape(entry) for entry in operators),
               Operator),
              (
               '\\b(or|and)\\b', Operator.Word),
              (
               '(%s)' % '|'.join(re.escape(entry) for entry in punctuations), Punctuation),
              (
               '[0-9]+', Number.Integer),
              (
               '"', String.Double, 'doublequote'),
              (
               "''", String.Single, 'singlequote'),
              (
               '[\\w.+-]*(\\/[\\w.+-]+)+', Literal),
              (
               '\\<[\\w.+-]+(\\/[\\w.+-]+)*\\>', Literal),
              (
               "[a-zA-Z][a-zA-Z0-9\\+\\-\\.]*\\:[\\w%/?:@&=+$,\\\\.!~*\\'-]+", Literal),
              (
               '[\\w-]+\\s*=', String.Symbol),
              (
               "[a-zA-Z_][\\w\\'-]*", Text)], 
     
     'comment': [
                 (
                  '[^/*]+', Comment.Multiline),
                 (
                  '/\\*', Comment.Multiline, '#push'),
                 (
                  '\\*/', Comment.Multiline, '#pop'),
                 (
                  '[*/]', Comment.Multiline)], 
     
     'singlequote': [
                     (
                      "'''", String.Escape),
                     (
                      "''\\$\\{", String.Escape),
                     (
                      "''\\n", String.Escape),
                     (
                      "''\\r", String.Escape),
                     (
                      "''\\t", String.Escape),
                     (
                      "''", String.Single, '#pop'),
                     (
                      '\\$\\{', String.Interpol, 'antiquote'),
                     (
                      "[^']", String.Single)], 
     
     'doublequote': [
                     (
                      '\\\\', String.Escape),
                     (
                      '\\\\"', String.Escape),
                     (
                      '\\\\$\\{', String.Escape),
                     (
                      '"', String.Double, '#pop'),
                     (
                      '\\$\\{', String.Interpol, 'antiquote'),
                     (
                      '[^"]', String.Double)], 
     
     'antiquote': [
                   (
                    '\\}', String.Interpol, '#pop'),
                   (
                    '\\$\\{', String.Interpol, '#push'),
                   include('root')]}

    def analyse_text(text):
        rv = 0.0
        if re.search('import.+?<[^>]+>', text):
            rv += 0.4
        if re.search('mkDerivation\\s+(\\(|\\{|rec)', text):
            rv += 0.4
        if re.search('=\\s+mkIf\\s+', text):
            rv += 0.4
        if re.search('\\{[a-zA-Z,\\s]+\\}:', text):
            rv += 0.1
        return rv