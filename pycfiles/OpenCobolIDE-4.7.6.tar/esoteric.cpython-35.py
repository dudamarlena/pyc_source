# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/esoteric.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 7083 bytes
"""
    pygments.lexers.esoteric
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for esoteric languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error, Whitespace
__all__ = [
 'BrainfuckLexer', 'BefungeLexer', 'BoogieLexer', 'RedcodeLexer', 'CAmkESLexer']

class BrainfuckLexer(RegexLexer):
    __doc__ = '\n    Lexer for the esoteric `BrainFuck <http://www.muppetlabs.com/~breadbox/bf/>`_\n    language.\n    '
    name = 'Brainfuck'
    aliases = ['brainfuck', 'bf']
    filenames = ['*.bf', '*.b']
    mimetypes = ['application/x-brainfuck']
    tokens = {'common': [
                (
                 '[.,]+', Name.Tag),
                (
                 '[+-]+', Name.Builtin),
                (
                 '[<>]+', Name.Variable),
                (
                 '[^.,+\\-<>\\[\\]]+', Comment)], 
     
     'root': [
              (
               '\\[', Keyword, 'loop'),
              (
               '\\]', Error),
              include('common')], 
     
     'loop': [
              (
               '\\[', Keyword, '#push'),
              (
               '\\]', Keyword, '#pop'),
              include('common')]}


class BefungeLexer(RegexLexer):
    __doc__ = '\n    Lexer for the esoteric `Befunge <http://en.wikipedia.org/wiki/Befunge>`_\n    language.\n\n    .. versionadded:: 0.7\n    '
    name = 'Befunge'
    aliases = ['befunge']
    filenames = ['*.befunge']
    mimetypes = ['application/x-befunge']
    tokens = {'root': [
              (
               '[0-9a-f]', Number),
              (
               '[+*/%!`-]', Operator),
              (
               '[<>^v?\\[\\]rxjk]', Name.Variable),
              (
               '[:\\\\$.,n]', Name.Builtin),
              (
               '[|_mw]', Keyword),
              (
               '[{}]', Name.Tag),
              (
               '".*?"', String.Double),
              (
               "\\'.", String.Single),
              (
               '[#;]', Comment),
              (
               '[pg&~=@iotsy]', Keyword),
              (
               '[()A-Z]', Comment),
              (
               '\\s+', Text)]}


class CAmkESLexer(RegexLexer):
    __doc__ = '\n    Basic lexer for the input language for the\n    `CAmkES <https://sel4.systems/CAmkES/>`_ component platform.\n\n    .. versionadded:: 2.1\n    '
    name = 'CAmkES'
    aliases = ['camkes', 'idl4']
    filenames = ['*.camkes', '*.idl4']
    tokens = {'root': [
              (
               '^\\s*#.*\\n', Comment.Preproc),
              (
               '\\s+', Text),
              (
               '/\\*(.|\\n)*?\\*/', Comment),
              (
               '//.*\\n', Comment),
              (
               '[\\[\\(\\){},\\.;=\\]]', Punctuation),
              (
               words(('assembly', 'attribute', 'component', 'composition', 'configuration', 'connection',
       'connector', 'consumes', 'control', 'dataport', 'Dataport', 'emits', 'event',
       'Event', 'from', 'group', 'hardware', 'has', 'interface', 'Interface', 'maybe',
       'procedure', 'Procedure', 'provides', 'template', 'to', 'uses'), suffix='\\b'), Keyword),
              (
               words(('bool', 'boolean', 'Buf', 'char', 'character', 'double', 'float', 'in', 'inout',
       'int', 'int16_6', 'int32_t', 'int64_t', 'int8_t', 'integer', 'mutex', 'out',
       'real', 'refin', 'semaphore', 'signed', 'string', 'uint16_t', 'uint32_t',
       'uint64_t', 'uint8_t', 'uintptr_t', 'unsigned', 'void'), suffix='\\b'), Keyword.Type),
              (
               '[a-zA-Z_]\\w*_(priority|domain|buffer)', Keyword.Reserved),
              (
               words(('dma_pool', 'from_access', 'to_access'), suffix='\\b'),
               Keyword.Reserved),
              (
               'import\\s+(<[^>]*>|"[^"]*");', Comment.Preproc),
              (
               'include\\s+(<[^>]*>|"[^"]*");', Comment.Preproc),
              (
               '0[xX][\\da-fA-F]+', Number.Hex),
              (
               '-?[\\d]+', Number),
              (
               '-?[\\d]+\\.[\\d]+', Number.Float),
              (
               '"[^"]*"', String),
              (
               '[a-zA-Z_]\\w*', Name)]}


class RedcodeLexer(RegexLexer):
    __doc__ = "\n    A simple Redcode lexer based on ICWS'94.\n    Contributed by Adam Blinkinsop <blinks@acm.org>.\n\n    .. versionadded:: 0.8\n    "
    name = 'Redcode'
    aliases = ['redcode']
    filenames = ['*.cw']
    opcodes = ('DAT', 'MOV', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'JMP', 'JMZ', 'JMN',
               'DJN', 'CMP', 'SLT', 'SPL', 'ORG', 'EQU', 'END')
    modifiers = ('A', 'B', 'AB', 'BA', 'F', 'X', 'I')
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               ';.*$', Comment.Single),
              (
               '\\b(%s)\\b' % '|'.join(opcodes), Name.Function),
              (
               '\\b(%s)\\b' % '|'.join(modifiers), Name.Decorator),
              (
               '[A-Za-z_]\\w+', Name),
              (
               '[-+*/%]', Operator),
              (
               '[#$@<>]', Operator),
              (
               '[.,]', Punctuation),
              (
               '[-+]?\\d+', Number.Integer)]}


class BoogieLexer(RegexLexer):
    __doc__ = '\n    For `Boogie <https://boogie.codeplex.com/>`_ source code.\n\n    .. versionadded:: 2.1\n    '
    name = 'Boogie'
    aliases = ['boogie']
    filenames = ['*.bpl']
    tokens = {'root': [
              (
               '\\n', Whitespace),
              (
               '\\s+', Whitespace),
              (
               '//[/!](.*?)\\n', Comment.Doc),
              (
               '//(.*?)\\n', Comment.Single),
              (
               '/\\*', Comment.Multiline, 'comment'),
              (
               words(('axiom', 'break', 'call', 'ensures', 'else', 'exists', 'function', 'forall',
       'if', 'invariant', 'modifies', 'procedure', 'requires', 'then', 'var', 'while'), suffix='\\b'), Keyword),
              (
               words(('const', ), suffix='\\b'), Keyword.Reserved),
              (
               words(('bool', 'int', 'ref'), suffix='\\b'), Keyword.Type),
              include('numbers'),
              (
               '(>=|<=|:=|!=|==>|&&|\\|\\||[+/\\-=>*<\\[\\]])', Operator),
              (
               '([{}():;,.])', Punctuation),
              (
               '[a-zA-Z_]\\w*', Name)], 
     
     'comment': [
                 (
                  '[^*/]+', Comment.Multiline),
                 (
                  '/\\*', Comment.Multiline, '#push'),
                 (
                  '\\*/', Comment.Multiline, '#pop'),
                 (
                  '[*/]', Comment.Multiline)], 
     
     'numbers': [
                 (
                  '[0-9]+', Number.Integer)]}