# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/make.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 7329 bytes
"""
    pygments.lexers.make
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for Makefiles and similar.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, include, bygroups, do_insertions, using
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Punctuation
from pygments.lexers.shell import BashLexer
__all__ = [
 'MakefileLexer', 'BaseMakefileLexer', 'CMakeLexer']

class MakefileLexer(Lexer):
    __doc__ = '\n    Lexer for BSD and GNU make extensions (lenient enough to handle both in\n    the same file even).\n\n    *Rewritten in Pygments 0.10.*\n    '
    name = 'Makefile'
    aliases = ['make', 'makefile', 'mf', 'bsdmake']
    filenames = ['*.mak', '*.mk', 'Makefile', 'makefile', 'Makefile.*', 'GNUmakefile']
    mimetypes = ['text/x-makefile']
    r_special = re.compile('^(?:\\.\\s*(include|undef|error|warning|if|else|elif|endif|for|endfor)|\\s*(ifeq|ifneq|ifdef|ifndef|else|endif|-?include|define|endef|:|vpath)|\\s*(if|else|endif))(?=\\s)')
    r_comment = re.compile('^\\s*@?#')

    def get_tokens_unprocessed(self, text):
        ins = []
        lines = text.splitlines(True)
        done = ''
        lex = BaseMakefileLexer(**self.options)
        backslashflag = False
        for line in lines:
            if self.r_special.match(line) or backslashflag:
                ins.append((len(done), [(0, Comment.Preproc, line)]))
                backslashflag = line.strip().endswith('\\')
            else:
                if self.r_comment.match(line):
                    ins.append((len(done), [(0, Comment, line)]))
                else:
                    done += line

        for item in do_insertions(ins, lex.get_tokens_unprocessed(done)):
            yield item

    def analyse_text(text):
        if re.search('\\$\\([A-Z_]+\\)', text):
            return 0.1


class BaseMakefileLexer(RegexLexer):
    __doc__ = '\n    Lexer for simple Makefiles (no preprocessing).\n\n    .. versionadded:: 0.10\n    '
    name = 'Base Makefile'
    aliases = ['basemake']
    filenames = []
    mimetypes = []
    tokens = {'root': [
              (
               '^(?:[\\t ]+.*\\n|\\n)+', using(BashLexer)),
              (
               '\\$[<@$+%?|*]', Keyword),
              (
               '\\s+', Text),
              (
               '#.*?\\n', Comment),
              (
               '(export)(\\s+)(?=[\\w${}\\t -]+\\n)',
               bygroups(Keyword, Text), 'export'),
              (
               'export\\s+', Keyword),
              (
               '([\\w${}.-]+)(\\s*)([!?:+]?=)([ \\t]*)((?:.*\\\\\\n)+|.*\\n)',
               bygroups(Name.Variable, Text, Operator, Text, using(BashLexer))),
              (
               '(?s)"(\\\\\\\\|\\\\.|[^"\\\\])*"', String.Double),
              (
               "(?s)'(\\\\\\\\|\\\\.|[^'\\\\])*'", String.Single),
              (
               '([^\\n:]+)(:+)([ \\t]*)', bygroups(Name.Function, Operator, Text),
               'block-header'),
              (
               '\\$\\(', Keyword, 'expansion')], 
     
     'expansion': [
                   (
                    '[^$a-zA-Z_)]+', Text),
                   (
                    '[a-zA-Z_]+', Name.Variable),
                   (
                    '\\$', Keyword),
                   (
                    '\\(', Keyword, '#push'),
                   (
                    '\\)', Keyword, '#pop')], 
     
     'export': [
                (
                 '[\\w${}-]+', Name.Variable),
                (
                 '\\n', Text, '#pop'),
                (
                 '\\s+', Text)], 
     
     'block-header': [
                      (
                       '[,|]', Punctuation),
                      (
                       '#.*?\\n', Comment, '#pop'),
                      (
                       '\\\\\\n', Text),
                      (
                       '\\$\\(', Keyword, 'expansion'),
                      (
                       '[a-zA-Z_]+', Name),
                      (
                       '\\n', Text, '#pop'),
                      (
                       '.', Text)]}


class CMakeLexer(RegexLexer):
    __doc__ = '\n    Lexer for `CMake <http://cmake.org/Wiki/CMake>`_ files.\n\n    .. versionadded:: 1.2\n    '
    name = 'CMake'
    aliases = ['cmake']
    filenames = ['*.cmake', 'CMakeLists.txt']
    mimetypes = ['text/x-cmake']
    tokens = {'root': [
              (
               '\\b(\\w+)([ \\t]*)(\\()',
               bygroups(Name.Builtin, Text, Punctuation), 'args'),
              include('keywords'),
              include('ws')], 
     
     'args': [
              (
               '\\(', Punctuation, '#push'),
              (
               '\\)', Punctuation, '#pop'),
              (
               '(\\$\\{)(.+?)(\\})', bygroups(Operator, Name.Variable, Operator)),
              (
               '(\\$ENV\\{)(.+?)(\\})', bygroups(Operator, Name.Variable, Operator)),
              (
               '(\\$<)(.+?)(>)', bygroups(Operator, Name.Variable, Operator)),
              (
               '(?s)".*?"', String.Double),
              (
               '\\\\\\S+', String),
              (
               '[^)$"# \\t\\n]+', String),
              (
               '\\n', Text),
              include('keywords'),
              include('ws')], 
     
     'string': [], 
     'keywords': [
                  (
                   '\\b(WIN32|UNIX|APPLE|CYGWIN|BORLAND|MINGW|MSVC|MSVC_IDE|MSVC60|MSVC70|MSVC71|MSVC80|MSVC90)\\b',
                   Keyword)], 
     
     'ws': [
            (
             '[ \\t]+', Text),
            (
             '#.*\\n', Comment)]}

    def analyse_text(text):
        exp = '^ *CMAKE_MINIMUM_REQUIRED *\\( *VERSION *\\d(\\.\\d)* *( FATAL_ERROR)? *\\) *$'
        if re.search(exp, text, flags=re.MULTILINE | re.IGNORECASE):
            return 0.8
        return 0.0