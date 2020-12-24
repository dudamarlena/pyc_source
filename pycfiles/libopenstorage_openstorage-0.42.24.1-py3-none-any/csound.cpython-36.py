# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/csound.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 16739 bytes
"""
    pygments.lexers.csound
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Csound languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, bygroups, default, include, using, words
from pygments.token import Comment, Error, Keyword, Name, Number, Operator, Punctuation, String, Text, Whitespace
from pygments.lexers._csound_builtins import OPCODES, DEPRECATED_OPCODES
from pygments.lexers.html import HtmlLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.scripting import LuaLexer
__all__ = [
 'CsoundScoreLexer', 'CsoundOrchestraLexer', 'CsoundDocumentLexer']
newline = (
 '((?:(?:;|//).*)*)(\\n)', bygroups(Comment.Single, Text))

class CsoundLexer(RegexLexer):
    tokens = {'whitespace':[
      (
       '[ \\t]+', Text),
      (
       '/[*](?:.|\\n)*?[*]/', Comment.Multiline),
      (
       '(?:;|//).*$', Comment.Single),
      (
       '(\\\\)(\\n)', bygroups(Whitespace, Text))], 
     'preprocessor directives':[
      (
       '#(?:e(?:nd(?:if)?|lse)\\b|##)|@@?[ \\t]*\\d+', Comment.Preproc),
      (
       '#includestr', Comment.Preproc, 'includestr directive'),
      (
       '#include', Comment.Preproc, 'include directive'),
      (
       '#[ \\t]*define', Comment.Preproc, 'define directive'),
      (
       '#(?:ifn?def|undef)\\b', Comment.Preproc, 'macro directive')], 
     'include directive':[
      include('whitespace'),
      (
       '([^ \\t]).*?\\1', String, '#pop')], 
     'includestr directive':[
      include('whitespace'),
      (
       '"', String, ('#pop', 'quoted string'))], 
     'define directive':[
      (
       '\\n', Text),
      include('whitespace'),
      (
       '([A-Z_a-z]\\w*)(\\()', bygroups(Comment.Preproc, Punctuation),
       ('#pop', 'macro parameter name list')),
      (
       '[A-Z_a-z]\\w*', Comment.Preproc, ('#pop', 'before macro body'))], 
     'macro parameter name list':[
      include('whitespace'),
      (
       '[A-Z_a-z]\\w*', Comment.Preproc),
      (
       "['#]", Punctuation),
      (
       '\\)', Punctuation, ('#pop', 'before macro body'))], 
     'before macro body':[
      (
       '\\n', Text),
      include('whitespace'),
      (
       '#', Punctuation, ('#pop', 'macro body'))], 
     'macro body':[
      (
       '(?:\\\\(?!#)|[^#\\\\]|\\n)+', Comment.Preproc),
      (
       '\\\\#', Comment.Preproc),
      (
       '(?<!\\\\)#', Punctuation, '#pop')], 
     'macro directive':[
      include('whitespace'),
      (
       '[A-Z_a-z]\\w*', Comment.Preproc, '#pop')], 
     'macro uses':[
      (
       '(\\$[A-Z_a-z]\\w*\\.?)(\\()', bygroups(Comment.Preproc, Punctuation),
       'macro parameter value list'),
      (
       '\\$[A-Z_a-z]\\w*(?:\\.|\\b)', Comment.Preproc)], 
     'macro parameter value list':[
      (
       '(?:[^\\\'#"{()]|\\{(?!\\{))+', Comment.Preproc),
      (
       "['#]", Punctuation),
      (
       '"', String, 'macro parameter value quoted string'),
      (
       '\\{\\{', String, 'macro parameter value braced string'),
      (
       '\\(', Comment.Preproc, 'macro parameter value parenthetical'),
      (
       '\\)', Punctuation, '#pop')], 
     'macro parameter value quoted string':[
      (
       "\\\\[#'()]", Comment.Preproc),
      (
       "[#'()]", Error),
      include('quoted string')], 
     'macro parameter value braced string':[
      (
       "\\\\[#'()]", Comment.Preproc),
      (
       "[#'()]", Error),
      include('braced string')], 
     'macro parameter value parenthetical':[
      (
       '(?:[^\\\\()]|\\\\\\))+', Comment.Preproc),
      (
       '\\(', Comment.Preproc, '#push'),
      (
       '\\)', Comment.Preproc, '#pop')], 
     'whitespace and macro uses':[
      include('whitespace'),
      include('macro uses')], 
     'numbers':[
      (
       '\\d+[Ee][+-]?\\d+|(\\d+\\.\\d*|\\d*\\.\\d+)([Ee][+-]?\\d+)?', Number.Float),
      (
       '(0[Xx])([0-9A-Fa-f]+)', bygroups(Keyword.Type, Number.Hex)),
      (
       '\\d+', Number.Integer)], 
     'quoted string':[
      (
       '"', String, '#pop'),
      (
       '[^"$]+', String),
      include('macro uses'),
      (
       '[$]', String)], 
     'braced string':[]}


class CsoundScoreLexer(CsoundLexer):
    __doc__ = '\n    For `Csound <https://csound.com>`_ scores.\n\n    .. versionadded:: 2.1\n    '
    name = 'Csound Score'
    aliases = ['csound-score', 'csound-sco']
    filenames = ['*.sco']
    tokens = {'root':[
      (
       '\\n', Text),
      include('whitespace and macro uses'),
      include('preprocessor directives'),
      (
       '[abCdefiqstvxy]', Keyword),
      (
       'z', Keyword.Constant),
      (
       '([nNpP][pP])(\\d+)', bygroups(Keyword, Number.Integer)),
      (
       '[mn]', Keyword, 'mark statement'),
      include('numbers'),
      (
       '[!+\\-*/^%&|<>#~.]', Operator),
      (
       '[()\\[\\]]', Punctuation),
      (
       '"', String, 'quoted string'),
      (
       '\\{', Comment.Preproc, 'loop after left brace')], 
     'mark statement':[
      include('whitespace and macro uses'),
      (
       '[A-Z_a-z]\\w*', Name.Label),
      (
       '\\n', Text, '#pop')], 
     'loop after left brace':[
      include('whitespace and macro uses'),
      (
       '\\d+', Number.Integer, ('#pop', 'loop after repeat count'))], 
     'loop after repeat count':[
      include('whitespace and macro uses'),
      (
       '[A-Z_a-z]\\w*', Comment.Preproc, ('#pop', 'loop'))], 
     'loop':[
      (
       '\\}', Comment.Preproc, '#pop'),
      include('root')], 
     'braced string':[
      (
       '\\}\\}', String, '#pop'),
      (
       '[^}]|\\}(?!\\})', String)]}


class CsoundOrchestraLexer(CsoundLexer):
    __doc__ = '\n    For `Csound <https://csound.com>`_ orchestras.\n\n    .. versionadded:: 2.1\n    '
    name = 'Csound Orchestra'
    aliases = ['csound', 'csound-orc']
    filenames = ['*.orc', '*.udo']
    user_defined_opcodes = set()

    def opcode_name_callback(lexer, match):
        opcode = match.group(0)
        lexer.user_defined_opcodes.add(opcode)
        yield (match.start(), Name.Function, opcode)

    def name_callback(lexer, match):
        type_annotation_token = Keyword.Type
        name = match.group(1)
        if name in OPCODES or name in DEPRECATED_OPCODES:
            yield (
             match.start(), Name.Builtin, name)
        else:
            if name in lexer.user_defined_opcodes:
                yield (
                 match.start(), Name.Function, name)
            else:
                type_annotation_token = Name
                name_match = re.search('^(g?[afikSw])(\\w+)', name)
                if name_match:
                    yield (
                     name_match.start(1), Keyword.Type, name_match.group(1))
                    yield (name_match.start(2), Name, name_match.group(2))
                else:
                    yield (
                     match.start(), Name, name)
        if match.group(2):
            yield (
             match.start(2), Punctuation, match.group(2))
            yield (match.start(3), type_annotation_token, match.group(3))

    tokens = {'root':[
      (
       '\\n', Text),
      (
       '^([ \\t]*)(\\w+)(:)(?:[ \\t]+|$)', bygroups(Text, Name.Label, Punctuation)),
      include('whitespace and macro uses'),
      include('preprocessor directives'),
      (
       '\\binstr\\b', Keyword.Declaration, 'instrument numbers and identifiers'),
      (
       '\\bopcode\\b', Keyword.Declaration, 'after opcode keyword'),
      (
       '\\b(?:end(?:in|op))\\b', Keyword.Declaration),
      include('partial statements')], 
     'partial statements':[
      (
       '\\b(?:0dbfs|A4|k(?:r|smps)|nchnls(?:_i)?|sr)\\b', Name.Variable.Global),
      include('numbers'),
      (
       '\\+=|-=|\\*=|/=|<<|>>|<=|>=|==|!=|&&|\\|\\||[~¬]|[=!+\\-*/^%&|<>#?:]', Operator),
      (
       '[(),\\[\\]]', Punctuation),
      (
       '"', String, 'quoted string'),
      (
       '\\{\\{', String, 'braced string'),
      (
       words(('do', 'else', 'elseif', 'endif', 'enduntil', 'fi', 'if', 'ithen', 'kthen', 'od',
       'then', 'until', 'while'),
         prefix='\\b',
         suffix='\\b'), Keyword),
      (
       words(('return', 'rireturn'), prefix='\\b', suffix='\\b'), Keyword.Pseudo),
      (
       '\\b[ik]?goto\\b', Keyword, 'goto label'),
      (
       '\\b(r(?:einit|igoto)|tigoto)(\\(|\\b)', bygroups(Keyword.Pseudo, Punctuation),
       'goto label'),
      (
       '\\b(c(?:g|in?|k|nk?)goto)(\\(|\\b)', bygroups(Keyword.Pseudo, Punctuation),
       ('goto label', 'goto argument')),
      (
       '\\b(timout)(\\(|\\b)', bygroups(Keyword.Pseudo, Punctuation),
       ('goto label', 'goto argument', 'goto argument')),
      (
       '\\b(loop_[gl][et])(\\(|\\b)', bygroups(Keyword.Pseudo, Punctuation),
       ('goto label', 'goto argument', 'goto argument', 'goto argument')),
      (
       '\\bprintk?s\\b', Name.Builtin, 'prints opcode'),
      (
       '\\b(?:readscore|scoreline(?:_i)?)\\b', Name.Builtin, 'Csound score opcode'),
      (
       '\\bpyl?run[it]?\\b', Name.Builtin, 'Python opcode'),
      (
       '\\blua_(?:exec|opdef)\\b', Name.Builtin, 'Lua opcode'),
      (
       '\\bp\\d+\\b', Name.Variable.Instance),
      (
       '\\b([A-Z_a-z]\\w*)(?:(:)([A-Za-z]))?\\b', name_callback)], 
     'instrument numbers and identifiers':[
      include('whitespace and macro uses'),
      (
       '\\d+|[A-Z_a-z]\\w*', Name.Function),
      (
       '[+,]', Punctuation),
      (
       '\\n', Text, '#pop')], 
     'after opcode keyword':[
      include('whitespace and macro uses'),
      (
       '[A-Z_a-z]\\w*', opcode_name_callback, ('#pop', 'opcode type signatures')),
      (
       '\\n', Text, '#pop')], 
     'opcode type signatures':[
      include('whitespace and macro uses'),
      (
       '0|[afijkKoOpPStV\\[\\]]+', Keyword.Type),
      (
       ',', Punctuation),
      (
       '\\n', Text, '#pop')], 
     'quoted string':[
      (
       '"', String, '#pop'),
      (
       '[^\\\\"$%)]+', String),
      include('macro uses'),
      include('escape sequences'),
      include('format specifiers'),
      (
       '[\\\\$%)]', String)], 
     'braced string':[
      (
       '\\}\\}', String, '#pop'),
      (
       '(?:[^\\\\%)}]|\\}(?!\\}))+', String),
      include('escape sequences'),
      include('format specifiers'),
      (
       '[\\\\%)]', String)], 
     'escape sequences':[
      (
       '\\\\(?:[\\\\abnrt"]|[0-7]{1,3})', String.Escape)], 
     'format specifiers':[
      (
       '%[#0\\- +]*\\d*(?:\\.\\d+)?[diuoxXfFeEgGaAcs]', String.Interpol),
      (
       '%%', String.Escape)], 
     'goto argument':[
      include('whitespace and macro uses'),
      (
       ',', Punctuation, '#pop'),
      include('partial statements')], 
     'goto label':[
      include('whitespace and macro uses'),
      (
       '\\w+', Name.Label, '#pop'),
      default('#pop')], 
     'prints opcode':[
      include('whitespace and macro uses'),
      (
       '"', String, 'prints quoted string'),
      default('#pop')], 
     'prints quoted string':[
      (
       '\\\\\\\\[aAbBnNrRtT]', String.Escape),
      (
       '%[!nNrRtT]|[~^]{1,2}', String.Escape),
      include('quoted string')], 
     'Csound score opcode':[
      include('whitespace and macro uses'),
      (
       '"', String, 'quoted string'),
      (
       '\\{\\{', String, 'Csound score'),
      (
       '\\n', Text, '#pop')], 
     'Csound score':[
      (
       '\\}\\}', String, '#pop'),
      (
       '([^}]+)|\\}(?!\\})', using(CsoundScoreLexer))], 
     'Python opcode':[
      include('whitespace and macro uses'),
      (
       '"', String, 'quoted string'),
      (
       '\\{\\{', String, 'Python'),
      (
       '\\n', Text, '#pop')], 
     'Python':[
      (
       '\\}\\}', String, '#pop'),
      (
       '([^}]+)|\\}(?!\\})', using(PythonLexer))], 
     'Lua opcode':[
      include('whitespace and macro uses'),
      (
       '"', String, 'quoted string'),
      (
       '\\{\\{', String, 'Lua'),
      (
       '\\n', Text, '#pop')], 
     'Lua':[
      (
       '\\}\\}', String, '#pop'),
      (
       '([^}]+)|\\}(?!\\})', using(LuaLexer))]}


class CsoundDocumentLexer(RegexLexer):
    __doc__ = '\n    For `Csound <https://csound.com>`_ documents.\n\n    .. versionadded:: 2.1\n    '
    name = 'Csound Document'
    aliases = ['csound-document', 'csound-csd']
    filenames = ['*.csd']
    tokens = {'root':[
      (
       '/[*](.|\\n)*?[*]/', Comment.Multiline),
      (
       '(?:;|//).*$', Comment.Single),
      (
       '[^/;<]+|/(?!/)', Text),
      (
       '<\\s*CsInstruments', Name.Tag, ('orchestra', 'tag')),
      (
       '<\\s*CsScore', Name.Tag, ('score', 'tag')),
      (
       '<\\s*[Hh][Tt][Mm][Ll]', Name.Tag, ('HTML', 'tag')),
      (
       '<\\s*[\\w:.-]+', Name.Tag, 'tag'),
      (
       '<\\s*/\\s*[\\w:.-]+\\s*>', Name.Tag)], 
     'orchestra':[
      (
       '<\\s*/\\s*CsInstruments\\s*>', Name.Tag, '#pop'),
      (
       '(.|\\n)+?(?=<\\s*/\\s*CsInstruments\\s*>)', using(CsoundOrchestraLexer))], 
     'score':[
      (
       '<\\s*/\\s*CsScore\\s*>', Name.Tag, '#pop'),
      (
       '(.|\\n)+?(?=<\\s*/\\s*CsScore\\s*>)', using(CsoundScoreLexer))], 
     'HTML':[
      (
       '<\\s*/\\s*[Hh][Tt][Mm][Ll]\\s*>', Name.Tag, '#pop'),
      (
       '(.|\\n)+?(?=<\\s*/\\s*[Hh][Tt][Mm][Ll]\\s*>)', using(HtmlLexer))], 
     'tag':[
      (
       '\\s+', Text),
      (
       '[\\w.:-]+\\s*=', Name.Attribute, 'attr'),
      (
       '/?\\s*>', Name.Tag, '#pop')], 
     'attr':[
      (
       '\\s+', Text),
      (
       '".*?"', String, '#pop'),
      (
       "'.*?'", String, '#pop'),
      (
       '[^\\s>]+', String, '#pop')]}