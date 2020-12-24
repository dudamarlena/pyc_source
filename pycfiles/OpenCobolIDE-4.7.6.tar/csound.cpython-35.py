# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/csound.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 12513 bytes
"""
    pygments.lexers.csound
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for CSound languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import copy, re
from pygments.lexer import RegexLexer, bygroups, default, include, using, words
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Text
from pygments.lexers._csound_builtins import OPCODES
from pygments.lexers.html import HtmlLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.scripting import LuaLexer
__all__ = [
 'CsoundScoreLexer', 'CsoundOrchestraLexer', 'CsoundDocumentLexer']
newline = (
 '((?:;|//).*)*(\\n)', bygroups(Comment.Single, Text))

class CsoundLexer(RegexLexer):
    tokens = {'whitespace': [
                    (
                     '[ \\t]+', Text),
                    (
                     '\\\\\\n', Text),
                    (
                     '/[*](.|\\n)*?[*]/', Comment.Multiline)], 
     
     'macro call': [
                    (
                     '(\\$\\w+\\.?)(\\()', bygroups(Comment.Preproc, Punctuation),
                     'function macro call'),
                    (
                     '\\$\\w+(\\.|\\b)', Comment.Preproc)], 
     
     'function macro call': [
                             (
                              "((?:\\\\['\\)]|[^'\\)])+)(')", bygroups(Comment.Preproc, Punctuation)),
                             (
                              "([^'\\)]+)(\\))", bygroups(Comment.Preproc, Punctuation), '#pop')], 
     
     'whitespace or macro call': [
                                  include('whitespace'),
                                  include('macro call')], 
     
     'preprocessor directives': [
                                 (
                                  '#(e(nd(if)?|lse)|ifn?def|undef)\\b|##', Comment.Preproc),
                                 (
                                  '#include\\b', Comment.Preproc, 'include'),
                                 (
                                  '#[ \\t]*define\\b', Comment.Preproc, 'macro name'),
                                 (
                                  '@+[ \\t]*\\d*', Comment.Preproc)], 
     
     'include': [
                 include('whitespace'),
                 (
                  '"', String, 'single-line string')], 
     
     'macro name': [
                    include('whitespace'),
                    (
                     '(\\w+)(\\()', bygroups(Comment.Preproc, Text),
                     'function macro argument list'),
                    (
                     '\\w+', Comment.Preproc, 'object macro definition after name')], 
     
     'object macro definition after name': [
                                            include('whitespace'),
                                            (
                                             '#', Punctuation, 'object macro replacement text')], 
     
     'object macro replacement text': [
                                       (
                                        '(\\\\#|[^#])+', Comment.Preproc),
                                       (
                                        '#', Punctuation, '#pop:3')], 
     
     'function macro argument list': [
                                      (
                                       "(\\w+)(['#])", bygroups(Comment.Preproc, Punctuation)),
                                      (
                                       '(\\w+)(\\))', bygroups(Comment.Preproc, Punctuation),
                                       'function macro definition after name')], 
     
     'function macro definition after name': [
                                              (
                                               '[ \\t]+', Text),
                                              (
                                               '#', Punctuation, 'function macro replacement text')], 
     
     'function macro replacement text': [
                                         (
                                          '(\\\\#|[^#])+', Comment.Preproc),
                                         (
                                          '#', Punctuation, '#pop:4')]}


class CsoundScoreLexer(CsoundLexer):
    __doc__ = '\n    For `Csound <http://csound.github.io>`_ scores.\n\n    .. versionadded:: 2.1\n    '
    name = 'Csound Score'
    aliases = ['csound-score', 'csound-sco']
    filenames = ['*.sco']
    tokens = {'partial statement': [
                           include('preprocessor directives'),
                           (
                            '\\d+e[+-]?\\d+|(\\d+\\.\\d*|\\d*\\.\\d+)(e[+-]?\\d+)?', Number.Float),
                           (
                            '0[xX][a-fA-F0-9]+', Number.Hex),
                           (
                            '\\d+', Number.Integer),
                           (
                            '"', String, 'single-line string'),
                           (
                            '[+\\-*/%^!=<>|&#~.]', Operator),
                           (
                            '[]()[]', Punctuation),
                           (
                            '\\w+', Comment.Preproc)], 
     
     'statement': [
                   include('whitespace or macro call'),
                   newline + ('#pop', ),
                   include('partial statement')], 
     
     'root': [
              newline,
              include('whitespace or macro call'),
              (
               '[{}]', Punctuation, 'statement'),
              (
               '[abefimq-tv-z]|[nN][pP]?', Keyword, 'statement')], 
     
     'single-line string': [
                            (
                             '"', String, '#pop'),
                            (
                             '[^\\\\"]+', String)]}


class CsoundOrchestraLexer(CsoundLexer):
    __doc__ = '\n    For `Csound <http://csound.github.io>`_ orchestras.\n\n    .. versionadded:: 2.1\n    '
    name = 'Csound Orchestra'
    aliases = ['csound', 'csound-orc']
    filenames = ['*.orc']
    user_defined_opcodes = set()

    def opcode_name_callback(lexer, match):
        opcode = match.group(0)
        lexer.user_defined_opcodes.add(opcode)
        yield (match.start(), Name.Function, opcode)

    def name_callback(lexer, match):
        name = match.group(0)
        if re.match('p\\d+$', name) or name in OPCODES:
            yield (
             match.start(), Name.Builtin, name)
        else:
            if name in lexer.user_defined_opcodes:
                yield (
                 match.start(), Name.Function, name)
            else:
                nameMatch = re.search('^(g?[aikSw])(\\w+)', name)
                if nameMatch:
                    yield (
                     nameMatch.start(1), Keyword.Type, nameMatch.group(1))
                    yield (nameMatch.start(2), Name, nameMatch.group(2))
                else:
                    yield (
                     match.start(), Name, name)

    tokens = {'label': [
               (
                '\\b(\\w+)(:)', bygroups(Name.Label, Punctuation))], 
     
     'partial expression': [
                            include('preprocessor directives'),
                            (
                             '\\b(0dbfs|k(r|smps)|nchnls(_i)?|sr)\\b', Name.Variable.Global),
                            (
                             '\\d+e[+-]?\\d+|(\\d+\\.\\d*|\\d*\\.\\d+)(e[+-]?\\d+)?', Number.Float),
                            (
                             '0[xX][a-fA-F0-9]+', Number.Hex),
                            (
                             '\\d+', Number.Integer),
                            (
                             '"', String, 'single-line string'),
                            (
                             '{{', String, 'multi-line string'),
                            (
                             '[+\\-*/%^!=&|<>#~¬]', Operator),
                            (
                             '[](),?:[]', Punctuation),
                            (
                             words(('do', 'else', 'elseif', 'endif', 'enduntil', 'fi', 'if', 'ithen', 'kthen', 'od',
       'then', 'until', 'while', 'return', 'timout'), prefix='\\b', suffix='\\b'), Keyword),
                            (
                             words(('goto', 'igoto', 'kgoto', 'rigoto', 'tigoto'), prefix='\\b', suffix='\\b'), Keyword, 'goto label'),
                            (
                             words(('cggoto', 'cigoto', 'cingoto', 'ckgoto', 'cngoto'), prefix='\\b', suffix='\\b'), Keyword,
                             ('goto label', 'goto expression')),
                            (
                             words(('loop_ge', 'loop_gt', 'loop_le', 'loop_lt'), prefix='\\b', suffix='\\b'), Keyword,
                             ('goto label', 'goto expression', 'goto expression', 'goto expression')),
                            (
                             '\\bscoreline(_i)?\\b', Name.Builtin, 'scoreline opcode'),
                            (
                             '\\bpyl?run[it]?\\b', Name.Builtin, 'python opcode'),
                            (
                             '\\blua_(exec|opdef)\\b', Name.Builtin, 'lua opcode'),
                            (
                             '\\b[a-zA-Z_]\\w*\\b', name_callback)], 
     
     'expression': [
                    include('whitespace or macro call'),
                    newline + ('#pop', ),
                    include('partial expression')], 
     
     'root': [
              newline,
              include('whitespace or macro call'),
              (
               '\\binstr\\b', Keyword, ('instrument block', 'instrument name list')),
              (
               '\\bopcode\\b', Keyword,
               ('opcode block', 'opcode parameter list', 'opcode types', 'opcode types', 'opcode name')),
              include('label'),
              default('expression')], 
     
     'instrument name list': [
                              include('whitespace or macro call'),
                              (
                               '\\d+|\\+?[a-zA-Z_]\\w*', Name.Function),
                              (
                               ',', Punctuation),
                              newline + ('#pop', )], 
     
     'instrument block': [
                          newline,
                          include('whitespace or macro call'),
                          (
                           '\\bendin\\b', Keyword, '#pop'),
                          include('label'),
                          default('expression')], 
     
     'opcode name': [
                     include('whitespace or macro call'),
                     (
                      '[a-zA-Z_]\\w*', opcode_name_callback, '#pop')], 
     
     'opcode types': [
                      include('whitespace or macro call'),
                      (
                       '0|[]afijkKoOpPStV[]+', Keyword.Type, '#pop'),
                      (
                       ',', Punctuation)], 
     
     'opcode parameter list': [
                               include('whitespace or macro call'),
                               newline + ('#pop', )], 
     
     'opcode block': [
                      newline,
                      include('whitespace or macro call'),
                      (
                       '\\bendop\\b', Keyword, '#pop'),
                      include('label'),
                      default('expression')], 
     
     'goto label': [
                    include('whitespace or macro call'),
                    (
                     '\\w+', Name.Label, '#pop'),
                    default('#pop')], 
     
     'goto expression': [
                         include('whitespace or macro call'),
                         (
                          ',', Punctuation, '#pop'),
                         include('partial expression')], 
     
     'single-line string': [
                            include('macro call'),
                            (
                             '"', String, '#pop'),
                            (
                             '%\\d*(\\.\\d+)?[cdhilouxX]', String.Interpol),
                            (
                             '%[!%nNrRtT]|[~^]|\\\\([\\\\aAbBnNrRtT"]|[0-7]{1,3})', String.Escape),
                            (
                             '[^\\\\"~$%\\^\\n]+', String),
                            (
                             '[\\\\"~$%\\^\\n]', String)], 
     
     'multi-line string': [
                           (
                            '}}', String, '#pop'),
                           (
                            '[^\\}]+|\\}(?!\\})', String)], 
     
     'scoreline opcode': [
                          include('whitespace or macro call'),
                          (
                           '{{', String, 'scoreline'),
                          default('#pop')], 
     
     'scoreline': [
                   (
                    '}}', String, '#pop'),
                   (
                    '([^\\}]+)|\\}(?!\\})', using(CsoundScoreLexer))], 
     
     'python opcode': [
                       include('whitespace or macro call'),
                       (
                        '{{', String, 'python'),
                       default('#pop')], 
     
     'python': [
                (
                 '}}', String, '#pop'),
                (
                 '([^\\}]+)|\\}(?!\\})', using(PythonLexer))], 
     
     'lua opcode': [
                    include('whitespace or macro call'),
                    (
                     '"', String, 'single-line string'),
                    (
                     '{{', String, 'lua'),
                    (
                     ',', Punctuation),
                    default('#pop')], 
     
     'lua': [
             (
              '}}', String, '#pop'),
             (
              '([^\\}]+)|\\}(?!\\})', using(LuaLexer))]}


class CsoundDocumentLexer(RegexLexer):
    __doc__ = '\n    For `Csound <http://csound.github.io>`_ documents.\n\n    \n    '
    name = 'Csound Document'
    aliases = ['csound-document', 'csound-csd']
    filenames = ['*.csd']
    tokens = {'root': [
              newline,
              (
               '/[*](.|\\n)*?[*]/', Comment.Multiline),
              (
               '[^<&;/]+', Text),
              (
               '<\\s*CsInstruments', Name.Tag, ('orchestra', 'tag')),
              (
               '<\\s*CsScore', Name.Tag, ('score', 'tag')),
              (
               '<\\s*[hH][tT][mM][lL]', Name.Tag, ('HTML', 'tag')),
              (
               '<\\s*[\\w:.-]+', Name.Tag, 'tag'),
              (
               '<\\s*/\\s*[\\w:.-]+\\s*>', Name.Tag)], 
     
     'orchestra': [
                   (
                    '<\\s*/\\s*CsInstruments\\s*>', Name.Tag, '#pop'),
                   (
                    '(.|\\n)+?(?=<\\s*/\\s*CsInstruments\\s*>)', using(CsoundOrchestraLexer))], 
     
     'score': [
               (
                '<\\s*/\\s*CsScore\\s*>', Name.Tag, '#pop'),
               (
                '(.|\\n)+?(?=<\\s*/\\s*CsScore\\s*>)', using(CsoundScoreLexer))], 
     
     'HTML': [
              (
               '<\\s*/\\s*[hH][tT][mM][lL]\\s*>', Name.Tag, '#pop'),
              (
               '(.|\\n)+?(?=<\\s*/\\s*[hH][tT][mM][lL]\\s*>)', using(HtmlLexer))], 
     
     'tag': [
             (
              '\\s+', Text),
             (
              '[\\w.:-]+\\s*=', Name.Attribute, 'attr'),
             (
              '/?\\s*>', Name.Tag, '#pop')], 
     
     'attr': [
              (
               '\\s+', Text),
              (
               '".*?"', String, '#pop'),
              (
               "'.*?'", String, '#pop'),
              (
               '[^\\s>]+', String, '#pop')]}