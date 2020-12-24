# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/felix.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 9410 bytes
"""
    pygments.lexers.felix
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Felix language.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include, bygroups, default, words, combined
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'FelixLexer']

class FelixLexer(RegexLexer):
    __doc__ = '\n    For `Felix <http://www.felix-lang.org>`_ source code.\n\n    .. versionadded:: 1.2\n    '
    name = 'Felix'
    aliases = ['felix', 'flx']
    filenames = ['*.flx', '*.flxh']
    mimetypes = ['text/x-felix']
    preproc = ('elif', 'else', 'endif', 'if', 'ifdef', 'ifndef')
    keywords = ('_', '_deref', 'all', 'as', 'assert', 'attempt', 'call', 'callback',
                'case', 'caseno', 'cclass', 'code', 'compound', 'ctypes', 'do', 'done',
                'downto', 'elif', 'else', 'endattempt', 'endcase', 'endif', 'endmatch',
                'enum', 'except', 'exceptions', 'expect', 'finally', 'for', 'forall',
                'forget', 'fork', 'functor', 'goto', 'ident', 'if', 'incomplete',
                'inherit', 'instance', 'interface', 'jump', 'lambda', 'loop', 'match',
                'module', 'namespace', 'new', 'noexpand', 'nonterm', 'obj', 'of',
                'open', 'parse', 'raise', 'regexp', 'reglex', 'regmatch', 'rename',
                'return', 'the', 'then', 'to', 'type', 'typecase', 'typedef', 'typematch',
                'typeof', 'upto', 'when', 'whilst', 'with', 'yield')
    keyword_directives = ('_gc_pointer', '_gc_type', 'body', 'comment', 'const', 'export',
                          'header', 'inline', 'lval', 'macro', 'noinline', 'noreturn',
                          'package', 'private', 'pod', 'property', 'public', 'publish',
                          'requires', 'todo', 'virtual', 'use')
    keyword_declarations = ('def', 'let', 'ref', 'val', 'var')
    keyword_types = ('unit', 'void', 'any', 'bool', 'byte', 'offset', 'address', 'caddress',
                     'cvaddress', 'vaddress', 'tiny', 'short', 'int', 'long', 'vlong',
                     'utiny', 'ushort', 'vshort', 'uint', 'ulong', 'uvlong', 'int8',
                     'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64',
                     'float', 'double', 'ldouble', 'complex', 'dcomplex', 'lcomplex',
                     'imaginary', 'dimaginary', 'limaginary', 'char', 'wchar', 'uchar',
                     'charp', 'charcp', 'ucharp', 'ucharcp', 'string', 'wstring',
                     'ustring', 'cont', 'array', 'varray', 'list', 'lvalue', 'opt',
                     'slice')
    keyword_constants = ('false', 'true')
    operator_words = ('and', 'not', 'in', 'is', 'isin', 'or', 'xor')
    name_builtins = ('_svc', 'while')
    name_pseudo = ('root', 'self', 'this')
    decimal_suffixes = '([tTsSiIlLvV]|ll|LL|([iIuU])(8|16|32|64))?'
    tokens = {'root': [
              include('whitespace'),
              (
               words(('axiom', 'ctor', 'fun', 'gen', 'proc', 'reduce', 'union'), suffix='\\b'),
               Keyword, 'funcname'),
              (
               words(('class', 'cclass', 'cstruct', 'obj', 'struct'), suffix='\\b'),
               Keyword, 'classname'),
              (
               '(instance|module|typeclass)\\b', Keyword, 'modulename'),
              (
               words(keywords, suffix='\\b'), Keyword),
              (
               words(keyword_directives, suffix='\\b'), Name.Decorator),
              (
               words(keyword_declarations, suffix='\\b'), Keyword.Declaration),
              (
               words(keyword_types, suffix='\\b'), Keyword.Type),
              (
               words(keyword_constants, suffix='\\b'), Keyword.Constant),
              include('operators'),
              (
               '0[xX]([0-9a-fA-F_]*\\.[0-9a-fA-F_]+|[0-9a-fA-F_]+)[pP][+\\-]?[0-9_]+[lLfFdD]?',
               Number.Float),
              (
               '[0-9_]+(\\.[0-9_]+[eE][+\\-]?[0-9_]+|\\.[0-9_]*|[eE][+\\-]?[0-9_]+)[lLfFdD]?',
               Number.Float),
              (
               '\\.(0|[1-9][0-9_]*)([eE][+\\-]?[0-9_]+)?[lLfFdD]?',
               Number.Float),
              (
               '0[Bb][01_]+%s' % decimal_suffixes, Number.Bin),
              (
               '0[0-7_]+%s' % decimal_suffixes, Number.Oct),
              (
               '0[xX][0-9a-fA-F_]+%s' % decimal_suffixes, Number.Hex),
              (
               '(0|[1-9][0-9_]*)%s' % decimal_suffixes, Number.Integer),
              (
               '([rR][cC]?|[cC][rR])"""', String, 'tdqs'),
              (
               "([rR][cC]?|[cC][rR])'''", String, 'tsqs'),
              (
               '([rR][cC]?|[cC][rR])"', String, 'dqs'),
              (
               "([rR][cC]?|[cC][rR])'", String, 'sqs'),
              (
               '[cCfFqQwWuU]?"""', String, combined('stringescape', 'tdqs')),
              (
               "[cCfFqQwWuU]?'''", String, combined('stringescape', 'tsqs')),
              (
               '[cCfFqQwWuU]?"', String, combined('stringescape', 'dqs')),
              (
               "[cCfFqQwWuU]?'", String, combined('stringescape', 'sqs')),
              (
               '[\\[\\]{}:(),;?]', Punctuation),
              (
               '[a-zA-Z_]\\w*:>', Name.Label),
              (
               '(%s)\\b' % '|'.join(name_builtins), Name.Builtin),
              (
               '(%s)\\b' % '|'.join(name_pseudo), Name.Builtin.Pseudo),
              (
               '[a-zA-Z_]\\w*', Name)], 
     
     'whitespace': [
                    (
                     '\\n', Text),
                    (
                     '\\s+', Text),
                    include('comment'),
                    (
                     '#\\s*if\\s+0', Comment.Preproc, 'if0'),
                    (
                     '#', Comment.Preproc, 'macro')], 
     
     'operators': [
                   (
                    '(%s)\\b' % '|'.join(operator_words), Operator.Word),
                   (
                    '!=|==|<<|>>|\\|\\||&&|[-~+/*%=<>&^|.$]', Operator)], 
     
     'comment': [
                 (
                  '//(.*?)\\n', Comment.Single),
                 (
                  '/[*]', Comment.Multiline, 'comment2')], 
     
     'comment2': [
                  (
                   '[^/*]', Comment.Multiline),
                  (
                   '/[*]', Comment.Multiline, '#push'),
                  (
                   '[*]/', Comment.Multiline, '#pop'),
                  (
                   '[/*]', Comment.Multiline)], 
     
     'if0': [
             (
              '^\\s*#if.*?(?<!\\\\)\\n', Comment, '#push'),
             (
              '^\\s*#endif.*?(?<!\\\\)\\n', Comment, '#pop'),
             (
              '.*?\\n', Comment)], 
     
     'macro': [
               include('comment'),
               (
                '(import|include)(\\s+)(<[^>]*?>)',
                bygroups(Comment.Preproc, Text, String), '#pop'),
               (
                '(import|include)(\\s+)("[^"]*?")',
                bygroups(Comment.Preproc, Text, String), '#pop'),
               (
                "(import|include)(\\s+)('[^']*?')",
                bygroups(Comment.Preproc, Text, String), '#pop'),
               (
                '[^/\\n]+', Comment.Preproc),
               (
                '/', Comment.Preproc),
               (
                '(?<=\\\\)\\n', Comment.Preproc),
               (
                '\\n', Comment.Preproc, '#pop')], 
     
     'funcname': [
                  include('whitespace'),
                  (
                   '[a-zA-Z_]\\w*', Name.Function, '#pop'),
                  (
                   '(?=\\()', Text, '#pop')], 
     
     'classname': [
                   include('whitespace'),
                   (
                    '[a-zA-Z_]\\w*', Name.Class, '#pop'),
                   (
                    '(?=\\{)', Text, '#pop')], 
     
     'modulename': [
                    include('whitespace'),
                    (
                     '\\[', Punctuation, ('modulename2', 'tvarlist')),
                    default('modulename2')], 
     
     'modulename2': [
                     include('whitespace'),
                     (
                      '([a-zA-Z_]\\w*)', Name.Namespace, '#pop:2')], 
     
     'tvarlist': [
                  include('whitespace'),
                  include('operators'),
                  (
                   '\\[', Punctuation, '#push'),
                  (
                   '\\]', Punctuation, '#pop'),
                  (
                   ',', Punctuation),
                  (
                   '(with|where)\\b', Keyword),
                  (
                   '[a-zA-Z_]\\w*', Name)], 
     
     'stringescape': [
                      (
                       '\\\\([\\\\abfnrtv"\\\']|\\n|N\\{.*?\\}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})',
                       String.Escape)], 
     
     'strings': [
                 (
                  '%(\\([a-zA-Z0-9]+\\))?[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[diouxXeEfFgGcrs%]',
                  String.Interpol),
                 (
                  '[^\\\\\\\'"%\\n]+', String),
                 (
                  '[\\\'"\\\\]', String),
                 (
                  '%', String)], 
     
     'nl': [
            (
             '\\n', String)], 
     
     'dqs': [
             (
              '"', String, '#pop'),
             (
              '\\\\\\\\|\\\\"|\\\\\\n', String.Escape),
             include('strings')], 
     
     'sqs': [
             (
              "'", String, '#pop'),
             (
              "\\\\\\\\|\\\\'|\\\\\\n", String.Escape),
             include('strings')], 
     
     'tdqs': [
              (
               '"""', String, '#pop'),
              include('strings'),
              include('nl')], 
     
     'tsqs': [
              (
               "'''", String, '#pop'),
              include('strings'),
              include('nl')]}