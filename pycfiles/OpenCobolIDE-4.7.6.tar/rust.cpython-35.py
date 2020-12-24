# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/rust.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 6930 bytes
"""
    pygments.lexers.rust
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for the Rust language.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include, bygroups, words, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = [
 'RustLexer']

class RustLexer(RegexLexer):
    __doc__ = '\n    Lexer for the Rust programming language (version 1.0).\n\n    .. versionadded:: 1.6\n    '
    name = 'Rust'
    filenames = ['*.rs', '*.rs.in']
    aliases = ['rust']
    mimetypes = ['text/rust']
    tokens = {'root': [
              (
               '#![^[\\r\\n].*$', Comment.Preproc),
              default('base')], 
     
     'base': [
              (
               '\\n', Whitespace),
              (
               '\\s+', Whitespace),
              (
               '//!.*?\\n', String.Doc),
              (
               '///(\\n|[^/].*?\\n)', String.Doc),
              (
               '//(.*?)\\n', Comment.Single),
              (
               '/\\*\\*(\\n|[^/*])', String.Doc, 'doccomment'),
              (
               '/\\*!', String.Doc, 'doccomment'),
              (
               '/\\*', Comment.Multiline, 'comment'),
              (
               '\\$([a-zA-Z_]\\w*|\\(,?|\\),?|,?)', Comment.Preproc),
              (
               words(('as', 'box', 'crate', 'do', 'else', 'enum', 'extern', 'fn', 'for', 'if', 'impl',
       'in', 'loop', 'match', 'mut', 'priv', 'proc', 'pub', 'ref', 'return', 'static',
       'struct', 'trait', 'true', 'type', 'unsafe', 'while'), suffix='\\b'),
               Keyword),
              (
               words(('alignof', 'be', 'const', 'offsetof', 'pure', 'sizeof', 'typeof', 'once', 'unsized',
       'yield'), suffix='\\b'),
               Keyword.Reserved),
              (
               '(mod|use)\\b', Keyword.Namespace),
              (
               '(true|false)\\b', Keyword.Constant),
              (
               'let\\b', Keyword.Declaration),
              (
               words(('u8', 'u16', 'u32', 'u64', 'i8', 'i16', 'i32', 'i64', 'usize', 'isize', 'f32',
       'f64', 'str', 'bool'), suffix='\\b'),
               Keyword.Type),
              (
               'self\\b', Name.Builtin.Pseudo),
              (
               words(('Copy', 'Send', 'Sized', 'Sync', 'Drop', 'Fn', 'FnMut', 'FnOnce', 'drop', 'Box',
       'ToOwned', 'Clone', 'PartialEq', 'PartialOrd', 'Eq', 'Ord', 'AsRef', 'AsMut',
       'Into', 'From', 'Default', 'Iterator', 'Extend', 'IntoIterator', 'DoubleEndedIterator',
       'ExactSizeIterator', 'Option', 'Some', 'None', 'Result', 'Ok', 'Err', 'SliceConcatExt',
       'String', 'ToString', 'Vec'), suffix='\\b'),
               Name.Builtin),
              (
               "(break|continue)(\\s*)(\\'[A-Za-z_]\\w*)?", bygroups(Keyword, Text.Whitespace, Name.Label)),
              (
               '\'(\\\\[\'"\\\\nrt]|\\\\x[0-7][0-9a-fA-F]|\\\\0|\\\\u\\{[0-9a-fA-F]{1,6}\\}|.)\'',
               String.Char),
              (
               'b\'(\\\\[\'"\\\\nrt]|\\\\x[0-9a-fA-F]{2}|\\\\0|\\\\u\\{[0-9a-fA-F]{1,6}\\}|.)\'',
               String.Char),
              (
               '0b[01_]+', Number.Bin, 'number_lit'),
              (
               '0o[0-7_]+', Number.Oct, 'number_lit'),
              (
               '0[xX][0-9a-fA-F_]+', Number.Hex, 'number_lit'),
              (
               '[0-9][0-9_]*(\\.[0-9_]+[eE][+\\-]?[0-9_]+|\\.[0-9_]*(?!\\.)|[eE][+\\-]?[0-9_]+)',
               Number.Float, 'number_lit'),
              (
               '[0-9][0-9_]*', Number.Integer, 'number_lit'),
              (
               'b"', String, 'bytestring'),
              (
               '"', String, 'string'),
              (
               'b?r(#*)".*?"\\1', String),
              (
               "'static", Name.Builtin),
              (
               "'[a-zA-Z_]\\w*", Name.Attribute),
              (
               '[{}()\\[\\],.;]', Punctuation),
              (
               '[+\\-*/%&|<>^!~@=:?]', Operator),
              (
               '[a-zA-Z_]\\w*', Name),
              (
               '#!?\\[', Comment.Preproc, 'attribute['),
              (
               '([A-Za-z_]\\w*)(!)(\\s*)([A-Za-z_]\\w*)?(\\s*)(\\{)',
               bygroups(Comment.Preproc, Punctuation, Whitespace, Name, Whitespace, Punctuation), 'macro{'),
              (
               '([A-Za-z_]\\w*)(!)(\\s*)([A-Za-z_]\\w*)?(\\()',
               bygroups(Comment.Preproc, Punctuation, Whitespace, Name, Punctuation), 'macro(')], 
     
     'comment': [
                 (
                  '[^*/]+', Comment.Multiline),
                 (
                  '/\\*', Comment.Multiline, '#push'),
                 (
                  '\\*/', Comment.Multiline, '#pop'),
                 (
                  '[*/]', Comment.Multiline)], 
     
     'doccomment': [
                    (
                     '[^*/]+', String.Doc),
                    (
                     '/\\*', String.Doc, '#push'),
                    (
                     '\\*/', String.Doc, '#pop'),
                    (
                     '[*/]', String.Doc)], 
     
     'number_lit': [
                    (
                     '[ui](8|16|32|64|size)', Keyword, '#pop'),
                    (
                     'f(32|64)', Keyword, '#pop'),
                    default('#pop')], 
     
     'string': [
                (
                 '"', String, '#pop'),
                (
                 '\\\\[\'"\\\\nrt]|\\\\x[0-7][0-9a-fA-F]|\\\\0|\\\\u\\{[0-9a-fA-F]{1,6}\\}',
                 String.Escape),
                (
                 '[^\\\\"]+', String),
                (
                 '\\\\', String)], 
     
     'bytestring': [
                    (
                     '\\\\x[89a-fA-F][0-9a-fA-F]', String.Escape),
                    include('string')], 
     
     'macro{': [
                (
                 '\\{', Operator, '#push'),
                (
                 '\\}', Operator, '#pop')], 
     
     'macro(': [
                (
                 '\\(', Operator, '#push'),
                (
                 '\\)', Operator, '#pop')], 
     
     'attribute_common': [
                          (
                           '"', String, 'string'),
                          (
                           '\\[', Comment.Preproc, 'attribute['),
                          (
                           '\\(', Comment.Preproc, 'attribute(')], 
     
     'attribute[': [
                    include('attribute_common'),
                    (
                     '\\];?', Comment.Preproc, '#pop'),
                    (
                     '[^"\\]]+', Comment.Preproc)], 
     
     'attribute(': [
                    include('attribute_common'),
                    (
                     '\\);?', Comment.Preproc, '#pop'),
                    (
                     '[^")]+', Comment.Preproc)]}