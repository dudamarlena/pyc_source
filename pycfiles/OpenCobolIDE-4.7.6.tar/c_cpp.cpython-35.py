# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/c_cpp.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 10145 bytes
"""
    pygments.lexers.c_cpp
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for C/C++ languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, using, this, inherit, default, words
from pygments.util import get_bool_opt
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
__all__ = [
 'CLexer', 'CppLexer']

class CFamilyLexer(RegexLexer):
    __doc__ = '\n    For C family source code.  This is used as a base class to avoid repetitious\n    definitions.\n    '
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    _ws1 = '\\s*(?:/[*].*?[*]/\\s*)?'
    tokens = {'whitespace': [
                    (
                     '^#if\\s+0', Comment.Preproc, 'if0'),
                    (
                     '^#', Comment.Preproc, 'macro'),
                    (
                     '^(' + _ws1 + ')(#if\\s+0)',
                     bygroups(using(this), Comment.Preproc), 'if0'),
                    (
                     '^(' + _ws1 + ')(#)',
                     bygroups(using(this), Comment.Preproc), 'macro'),
                    (
                     '\\n', Text),
                    (
                     '\\s+', Text),
                    (
                     '\\\\\\n', Text),
                    (
                     '//(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single),
                    (
                     '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline)], 
     
     'statements': [
                    (
                     'L?"', String, 'string'),
                    (
                     "L?'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'", String.Char),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[LlUu]*', Number.Float),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
                    (
                     '0x[0-9a-fA-F]+[LlUu]*', Number.Hex),
                    (
                     '0[0-7]+[LlUu]*', Number.Oct),
                    (
                     '\\d+[LlUu]*', Number.Integer),
                    (
                     '\\*/', Error),
                    (
                     '[~!%^&*+=|?:<>/-]', Operator),
                    (
                     '[()\\[\\],.]', Punctuation),
                    (
                     words(('auto', 'break', 'case', 'const', 'continue', 'default', 'do', 'else', 'enum',
       'extern', 'for', 'goto', 'if', 'register', 'restricted', 'return', 'sizeof',
       'static', 'struct', 'switch', 'typedef', 'union', 'volatile', 'while'), suffix='\\b'), Keyword),
                    (
                     '(bool|int|long|float|short|double|char|unsigned|signed|void)\\b',
                     Keyword.Type),
                    (
                     words(('inline', '_inline', '__inline', 'naked', 'restrict', 'thread', 'typename'), suffix='\\b'), Keyword.Reserved),
                    (
                     '(__m(128i|128d|128|64))\\b', Keyword.Reserved),
                    (
                     words(('asm', 'int8', 'based', 'except', 'int16', 'stdcall', 'cdecl', 'fastcall', 'int32',
       'declspec', 'finally', 'int64', 'try', 'leave', 'wchar_t', 'w64', 'unaligned',
       'raise', 'noop', 'identifier', 'forceinline', 'assume'), prefix='__', suffix='\\b'), Keyword.Reserved),
                    (
                     '(true|false|NULL)\\b', Name.Builtin),
                    (
                     '([a-zA-Z_]\\w*)(\\s*)(:)(?!:)', bygroups(Name.Label, Text, Punctuation)),
                    (
                     '[a-zA-Z_]\\w*', Name)], 
     
     'root': [
              include('whitespace'),
              (
               '((?:[\\w*\\s])+?(?:\\s|[*]))([a-zA-Z_]\\w*)(\\s*\\([^;]*?\\))([^;{]*)(\\{)',
               bygroups(using(this), Name.Function, using(this), using(this), Punctuation),
               'function'),
              (
               '((?:[\\w*\\s])+?(?:\\s|[*]))([a-zA-Z_]\\w*)(\\s*\\([^;]*?\\))([^;]*)(;)',
               bygroups(using(this), Name.Function, using(this), using(this), Punctuation)),
              default('statement')], 
     
     'statement': [
                   include('whitespace'),
                   include('statements'),
                   (
                    '[{}]', Punctuation),
                   (
                    ';', Punctuation, '#pop')], 
     
     'function': [
                  include('whitespace'),
                  include('statements'),
                  (
                   ';', Punctuation),
                  (
                   '\\{', Punctuation, '#push'),
                  (
                   '\\}', Punctuation, '#pop')], 
     
     'string': [
                (
                 '"', String, '#pop'),
                (
                 '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|[0-7]{1,3})',
                 String.Escape),
                (
                 '[^\\\\"\\n]+', String),
                (
                 '\\\\\\n', String),
                (
                 '\\\\', String)], 
     
     'macro': [
               (
                '(include)(' + _ws1 + ')([^\n]+)', bygroups(Comment.Preproc, Text, Comment.PreprocFile)),
               (
                '[^/\\n]+', Comment.Preproc),
               (
                '/[*](.|\\n)*?[*]/', Comment.Multiline),
               (
                '//.*?\\n', Comment.Single, '#pop'),
               (
                '/', Comment.Preproc),
               (
                '(?<=\\\\)\\n', Comment.Preproc),
               (
                '\\n', Comment.Preproc, '#pop')], 
     
     'if0': [
             (
              '^\\s*#if.*?(?<!\\\\)\\n', Comment.Preproc, '#push'),
             (
              '^\\s*#el(?:se|if).*\\n', Comment.Preproc, '#pop'),
             (
              '^\\s*#endif.*?(?<!\\\\)\\n', Comment.Preproc, '#pop'),
             (
              '.*?\\n', Comment)]}
    stdlib_types = set(('size_t', 'ssize_t', 'off_t', 'wchar_t', 'ptrdiff_t', 'sig_atomic_t',
                        'fpos_t', 'clock_t', 'time_t', 'va_list', 'jmp_buf', 'FILE',
                        'DIR', 'div_t', 'ldiv_t', 'mbstate_t', 'wctrans_t', 'wint_t',
                        'wctype_t'))
    c99_types = set(('_Bool', '_Complex', 'int8_t', 'int16_t', 'int32_t', 'int64_t',
                     'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t', 'int_least8_t',
                     'int_least16_t', 'int_least32_t', 'int_least64_t', 'uint_least8_t',
                     'uint_least16_t', 'uint_least32_t', 'uint_least64_t', 'int_fast8_t',
                     'int_fast16_t', 'int_fast32_t', 'int_fast64_t', 'uint_fast8_t',
                     'uint_fast16_t', 'uint_fast32_t', 'uint_fast64_t', 'intptr_t',
                     'uintptr_t', 'intmax_t', 'uintmax_t'))
    linux_types = set(('clockid_t', 'cpu_set_t', 'cpumask_t', 'dev_t', 'gid_t', 'id_t',
                       'ino_t', 'key_t', 'mode_t', 'nfds_t', 'pid_t', 'rlim_t', 'sig_t',
                       'sighandler_t', 'siginfo_t', 'sigset_t', 'sigval_t', 'socklen_t',
                       'timer_t', 'uid_t'))

    def __init__(self, **options):
        self.stdlibhighlighting = get_bool_opt(options, 'stdlibhighlighting', True)
        self.c99highlighting = get_bool_opt(options, 'c99highlighting', True)
        self.platformhighlighting = get_bool_opt(options, 'platformhighlighting', True)
        RegexLexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if self.stdlibhighlighting and value in self.stdlib_types:
                    token = Keyword.Type
                else:
                    if self.c99highlighting and value in self.c99_types:
                        token = Keyword.Type
                    elif self.platformhighlighting and value in self.linux_types:
                        token = Keyword.Type
                yield (
                 index, token, value)


class CLexer(CFamilyLexer):
    __doc__ = '\n    For C source code with preprocessor directives.\n    '
    name = 'C'
    aliases = ['c']
    filenames = ['*.c', '*.h', '*.idc']
    mimetypes = ['text/x-chdr', 'text/x-csrc']
    priority = 0.1

    def analyse_text(text):
        if re.search('^\\s*#include [<"]', text, re.MULTILINE):
            return 0.1
        if re.search('^\\s*#ifn?def ', text, re.MULTILINE):
            return 0.1


class CppLexer(CFamilyLexer):
    __doc__ = '\n    For C++ source code with preprocessor directives.\n    '
    name = 'C++'
    aliases = ['cpp', 'c++']
    filenames = ['*.cpp', '*.hpp', '*.c++', '*.h++',
     '*.cc', '*.hh', '*.cxx', '*.hxx',
     '*.C', '*.H', '*.cp', '*.CPP']
    mimetypes = ['text/x-c++hdr', 'text/x-c++src']
    priority = 0.1
    tokens = {'statements': [
                    (
                     words(('asm', 'catch', 'const_cast', 'delete', 'dynamic_cast', 'explicit', 'export',
       'friend', 'mutable', 'namespace', 'new', 'operator', 'private', 'protected',
       'public', 'reinterpret_cast', 'restrict', 'static_cast', 'template', 'this',
       'throw', 'throws', 'try', 'typeid', 'typename', 'using', 'virtual', 'constexpr',
       'nullptr', 'decltype', 'thread_local', 'alignas', 'alignof', 'static_assert',
       'noexcept', 'override', 'final'), suffix='\\b'), Keyword),
                    (
                     'char(16_t|32_t)\\b', Keyword.Type),
                    (
                     '(class)(\\s+)', bygroups(Keyword, Text), 'classname'),
                    (
                     'R"\\(', String, 'rawstring'),
                    inherit], 
     
     'root': [
              inherit,
              (
               words(('virtual_inheritance', 'uuidof', 'super', 'single_inheritance', 'multiple_inheritance',
       'interface', 'event'), prefix='__', suffix='\\b'), Keyword.Reserved),
              (
               '__(offload|blockingoffload|outer)\\b', Keyword.Pseudo)], 
     
     'classname': [
                   (
                    '[a-zA-Z_]\\w*', Name.Class, '#pop'),
                   (
                    '\\s*(?=>)', Text, '#pop')], 
     
     'rawstring': [
                   (
                    '\\)"', String, '#pop'),
                   (
                    '[^)]+', String),
                   (
                    '\\)', String)]}

    def analyse_text(text):
        if re.search('#include <[a-z_]+>', text):
            return 0.2
        if re.search('using namespace ', text):
            return 0.4