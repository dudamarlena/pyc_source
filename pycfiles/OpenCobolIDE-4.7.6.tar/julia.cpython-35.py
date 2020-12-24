# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/julia.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 6974 bytes
"""
    pygments.lexers.julia
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for the Julia language.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, bygroups, combined, do_insertions
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic
from pygments.util import shebang_matches, unirange
__all__ = [
 'JuliaLexer', 'JuliaConsoleLexer']

class JuliaLexer(RegexLexer):
    __doc__ = '\n    For `Julia <http://julialang.org/>`_ source code.\n\n    .. versionadded:: 1.6\n    '
    name = 'Julia'
    aliases = ['julia', 'jl']
    filenames = ['*.jl']
    mimetypes = ['text/x-julia', 'application/x-julia']
    flags = re.MULTILINE | re.UNICODE
    builtins = [
     'exit', 'whos', 'edit', 'load', 'is', 'isa', 'isequal', 'typeof', 'tuple',
     'ntuple', 'uid', 'hash', 'finalizer', 'convert', 'promote', 'subtype',
     'typemin', 'typemax', 'realmin', 'realmax', 'sizeof', 'eps', 'promote_type',
     'method_exists', 'applicable', 'invoke', 'dlopen', 'dlsym', 'system',
     'error', 'throw', 'assert', 'new', 'Inf', 'Nan', 'pi', 'im']
    tokens = {'root': [
              (
               '\\n', Text),
              (
               '[^\\S\\n]+', Text),
              (
               '#=', Comment.Multiline, 'blockcomment'),
              (
               '#.*$', Comment),
              (
               '[]{}:(),;[@]', Punctuation),
              (
               '\\\\\\n', Text),
              (
               '\\\\', Text),
              (
               '(begin|while|for|in|return|break|continue|macro|quote|let|if|elseif|else|try|catch|end|bitstype|ccall|do|using|module|import|export|importall|baremodule|immutable)\\b',
               Keyword),
              (
               '(local|global|const)\\b', Keyword.Declaration),
              (
               '(Bool|Int|Int8|Int16|Int32|Int64|Uint|Uint8|Uint16|Uint32|Uint64|Float32|Float64|Complex64|Complex128|Any|Nothing|None)\\b',
               Keyword.Type),
              (
               '(function)((?:\\s|\\\\\\s)+)',
               bygroups(Keyword, Name.Function), 'funcname'),
              (
               '(type|typealias|abstract|immutable)((?:\\s|\\\\\\s)+)',
               bygroups(Keyword, Name.Class), 'typename'),
              (
               '==|!=|<=|>=|->|&&|\\|\\||::|<:|[-~+/*%=<>&^|.?!$]', Operator),
              (
               '\\.\\*|\\.\\^|\\.\\\\|\\.\\/|\\\\', Operator),
              (
               '(' + '|'.join(builtins) + ')\\b', Name.Builtin),
              (
               '`(?s).*?`', String.Backtick),
              (
               "'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,3}|\\\\u[a-fA-F0-9]{1,4}|\\\\U[a-fA-F0-9]{1,6}|[^\\\\\\'\\n])'",
               String.Char),
              (
               "(?<=[.\\w)\\]])\\'+", Operator),
              (
               '(?:[IL])"', String, 'string'),
              (
               '[E]?"', String, combined('stringescape', 'string')),
              (
               '@[\\w.]+', Name.Decorator),
              (
               '(?:[a-zA-Z_¡-\uffff]|%s)(?:[a-zA-Z_0-9¡-\uffff]|%s)*!*' % ((
                unirange(65536, 1114111),) * 2), Name),
              (
               '(\\d+(_\\d+)+\\.\\d*|\\d*\\.\\d+(_\\d+)+)([eEf][+-]?[0-9]+)?', Number.Float),
              (
               '(\\d+\\.\\d*|\\d*\\.\\d+)([eEf][+-]?[0-9]+)?', Number.Float),
              (
               '\\d+(_\\d+)+[eEf][+-]?[0-9]+', Number.Float),
              (
               '\\d+[eEf][+-]?[0-9]+', Number.Float),
              (
               '0b[01]+(_[01]+)+', Number.Bin),
              (
               '0b[01]+', Number.Bin),
              (
               '0o[0-7]+(_[0-7]+)+', Number.Oct),
              (
               '0o[0-7]+', Number.Oct),
              (
               '0x[a-fA-F0-9]+(_[a-fA-F0-9]+)+', Number.Hex),
              (
               '0x[a-fA-F0-9]+', Number.Hex),
              (
               '\\d+(_\\d+)+', Number.Integer),
              (
               '\\d+', Number.Integer)], 
     
     'funcname': [
                  (
                   '[a-zA-Z_]\\w*', Name.Function, '#pop'),
                  (
                   '\\([^\\s\\w{]{1,2}\\)', Operator, '#pop'),
                  (
                   '[^\\s\\w{]{1,2}', Operator, '#pop')], 
     
     'typename': [
                  (
                   '[a-zA-Z_]\\w*', Name.Class, '#pop')], 
     
     'stringescape': [
                      (
                       '\\\\([\\\\abfnrtv"\\\']|\\n|N\\{.*?\\}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})',
                       String.Escape)], 
     
     'blockcomment': [
                      (
                       '[^=#]', Comment.Multiline),
                      (
                       '#=', Comment.Multiline, '#push'),
                      (
                       '=#', Comment.Multiline, '#pop'),
                      (
                       '[=#]', Comment.Multiline)], 
     
     'string': [
                (
                 '"', String, '#pop'),
                (
                 '\\\\\\\\|\\\\"|\\\\\\n', String.Escape),
                (
                 '\\$[a-zA-Z_]+', String.Interpol),
                (
                 '\\$\\(', String.Interpol, 'in-intp'),
                (
                 '%[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[diouxXeEfFgGcrs%]',
                 String.Interpol),
                (
                 '[^$%"\\\\]+', String),
                (
                 '[$%"\\\\]', String)], 
     
     'in-intp': [
                 (
                  '[^()]+', String.Interpol),
                 (
                  '\\(', String.Interpol, '#push'),
                 (
                  '\\)', String.Interpol, '#pop')]}

    def analyse_text(text):
        return shebang_matches(text, 'julia')


line_re = re.compile('.*?\n')

class JuliaConsoleLexer(Lexer):
    __doc__ = '\n    For Julia console sessions. Modeled after MatlabSessionLexer.\n\n    .. versionadded:: 1.6\n    '
    name = 'Julia console'
    aliases = ['jlcon']

    def get_tokens_unprocessed(self, text):
        jllexer = JuliaLexer(**self.options)
        curcode = ''
        insertions = []
        for match in line_re.finditer(text):
            line = match.group()
            if line.startswith('julia>'):
                insertions.append((len(curcode),
                 [
                  (
                   0, Generic.Prompt, line[:6])]))
                curcode += line[6:]
            elif line.startswith('      '):
                idx = len(curcode)
                line = '\n' + line
                token = (0, Generic.Traceback, line)
                insertions.append((idx, [token]))
            else:
                if curcode:
                    for item in do_insertions(insertions, jllexer.get_tokens_unprocessed(curcode)):
                        yield item

                    curcode = ''
                    insertions = []
                yield (match.start(), Generic.Output, line)

        if curcode:
            for item in do_insertions(insertions, jllexer.get_tokens_unprocessed(curcode)):
                yield item