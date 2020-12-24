# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/markup.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 16886 bytes
"""
    pygments.lexers.markup
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for non-HTML markup languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexers.html import HtmlLexer, XmlLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.css import CssLexer
from pygments.lexer import RegexLexer, DelegatingLexer, include, bygroups, using, this, do_insertions, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic, Other
from pygments.util import get_bool_opt, ClassNotFound
__all__ = [
 'BBCodeLexer', 'MoinWikiLexer', 'RstLexer', 'TexLexer', 'GroffLexer',
 'MozPreprocHashLexer', 'MozPreprocPercentLexer',
 'MozPreprocXulLexer', 'MozPreprocJavascriptLexer',
 'MozPreprocCssLexer']

class BBCodeLexer(RegexLexer):
    __doc__ = '\n    A lexer that highlights BBCode(-like) syntax.\n\n    .. versionadded:: 0.6\n    '
    name = 'BBCode'
    aliases = ['bbcode']
    mimetypes = ['text/x-bbcode']
    tokens = {'root': [
              (
               '[^[]+', Text),
              (
               '\\[/?\\w+', Keyword, 'tag'),
              (
               '\\[', Text)], 
     
     'tag': [
             (
              '\\s+', Text),
             (
              '(\\w+)(=)("?[^\\s"\\]]+"?)',
              bygroups(Name.Attribute, Operator, String)),
             (
              '(=)("?[^\\s"\\]]+"?)',
              bygroups(Operator, String)),
             (
              '\\]', Keyword, '#pop')]}


class MoinWikiLexer(RegexLexer):
    __doc__ = '\n    For MoinMoin (and Trac) Wiki markup.\n\n    .. versionadded:: 0.7\n    '
    name = 'MoinMoin/Trac Wiki markup'
    aliases = ['trac-wiki', 'moin']
    filenames = []
    mimetypes = ['text/x-trac-wiki']
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [
              (
               '^#.*$', Comment),
              (
               '(!)(\\S+)', bygroups(Keyword, Text)),
              (
               '^(=+)([^=]+)(=+)(\\s*#.+)?$',
               bygroups(Generic.Heading, using(this), Generic.Heading, String)),
              (
               '(\\{\\{\\{)(\\n#!.+)?', bygroups(Name.Builtin, Name.Namespace), 'codeblock'),
              (
               "(\\'\\'\\'?|\\|\\||`|__|~~|\\^|,,|::)", Comment),
              (
               '^( +)([.*-])( )', bygroups(Text, Name.Builtin, Text)),
              (
               '^( +)([a-z]{1,5}\\.)( )', bygroups(Text, Name.Builtin, Text)),
              (
               '\\[\\[\\w+.*?\\]\\]', Keyword),
              (
               '(\\[[^\\s\\]]+)(\\s+[^\\]]+?)?(\\])',
               bygroups(Keyword, String, Keyword)),
              (
               '^----+$', Keyword),
              (
               "[^\\n\\'\\[{!_~^,|]+", Text),
              (
               '\\n', Text),
              (
               '.', Text)], 
     
     'codeblock': [
                   (
                    '\\}\\}\\}', Name.Builtin, '#pop'),
                   (
                    '\\{\\{\\{', Text, '#push'),
                   (
                    '[^{}]+', Comment.Preproc),
                   (
                    '.', Comment.Preproc)]}


class RstLexer(RegexLexer):
    __doc__ = '\n    For `reStructuredText <http://docutils.sf.net/rst.html>`_ markup.\n\n    .. versionadded:: 0.7\n\n    Additional options accepted:\n\n    `handlecodeblocks`\n        Highlight the contents of ``.. sourcecode:: language``,\n        ``.. code:: language`` and ``.. code-block:: language``\n        directives with a lexer for the given language (default:\n        ``True``).\n\n        .. versionadded:: 0.8\n    '
    name = 'reStructuredText'
    aliases = ['rst', 'rest', 'restructuredtext']
    filenames = ['*.rst', '*.rest']
    mimetypes = ['text/x-rst', 'text/prs.fallenstein.rst']
    flags = re.MULTILINE

    def _handle_sourcecode(self, match):
        from pygments.lexers import get_lexer_by_name
        yield (
         match.start(1), Punctuation, match.group(1))
        yield (match.start(2), Text, match.group(2))
        yield (match.start(3), Operator.Word, match.group(3))
        yield (match.start(4), Punctuation, match.group(4))
        yield (match.start(5), Text, match.group(5))
        yield (match.start(6), Keyword, match.group(6))
        yield (match.start(7), Text, match.group(7))
        lexer = None
        if self.handlecodeblocks:
            try:
                lexer = get_lexer_by_name(match.group(6).strip())
            except ClassNotFound:
                pass

        indention = match.group(8)
        indention_size = len(indention)
        code = indention + match.group(9) + match.group(10) + match.group(11)
        if lexer is None:
            yield (
             match.start(8), String, code)
            return
        ins = []
        codelines = code.splitlines(True)
        code = ''
        for line in codelines:
            if len(line) > indention_size:
                ins.append((len(code), [(0, Text, line[:indention_size])]))
                code += line[indention_size:]
            else:
                code += line

        for item in do_insertions(ins, lexer.get_tokens_unprocessed(code)):
            yield item

    closers = '\'")]}>’”»!?'
    unicode_delimiters = '‐‑‒–—\xa0'
    end_string_suffix = '((?=$)|(?=[-/:.,; \\n\\x00%s%s]))' % (
     re.escape(unicode_delimiters),
     re.escape(closers))
    tokens = {'root': [
              (
               '^(=+|-+|`+|:+|\\.+|\\\'+|"+|~+|\\^+|_+|\\*+|\\++|#+)([ \\t]*\\n)(.+)(\\n)(\\1)(\\n)',
               bygroups(Generic.Heading, Text, Generic.Heading, Text, Generic.Heading, Text)),
              (
               '^(\\S.*)(\\n)(={3,}|-{3,}|`{3,}|:{3,}|\\.{3,}|\\\'{3,}|"{3,}|~{3,}|\\^{3,}|_{3,}|\\*{3,}|\\+{3,}|#{3,})(\\n)',
               bygroups(Generic.Heading, Text, Generic.Heading, Text)),
              (
               '^(\\s*)([-*+])( .+\\n(?:\\1  .+\\n)*)',
               bygroups(Text, Number, using(this, state='inline'))),
              (
               '^(\\s*)([0-9#ivxlcmIVXLCM]+\\.)( .+\\n(?:\\1  .+\\n)*)',
               bygroups(Text, Number, using(this, state='inline'))),
              (
               '^(\\s*)(\\(?[0-9#ivxlcmIVXLCM]+\\))( .+\\n(?:\\1  .+\\n)*)',
               bygroups(Text, Number, using(this, state='inline'))),
              (
               '^(\\s*)([A-Z]+\\.)( .+\\n(?:\\1  .+\\n)+)',
               bygroups(Text, Number, using(this, state='inline'))),
              (
               '^(\\s*)(\\(?[A-Za-z]+\\))( .+\\n(?:\\1  .+\\n)+)',
               bygroups(Text, Number, using(this, state='inline'))),
              (
               '^(\\s*)(\\|)( .+\\n(?:\\|  .+\\n)*)',
               bygroups(Text, Operator, using(this, state='inline'))),
              (
               '^( *\\.\\.)(\\s*)((?:source)?code(?:-block)?)(::)([ \\t]*)([^\\n]+)(\\n[ \\t]*\\n)([ \\t]+)(.*)(\\n)((?:(?:\\8.*|)\\n)+)',
               _handle_sourcecode),
              (
               '^( *\\.\\.)(\\s*)([\\w:-]+?)(::)(?:([ \\t]*)(.*))',
               bygroups(Punctuation, Text, Operator.Word, Punctuation, Text, using(this, state='inline'))),
              (
               '^( *\\.\\.)(\\s*)(_(?:[^:\\\\]|\\\\.)+:)(.*?)$',
               bygroups(Punctuation, Text, Name.Tag, using(this, state='inline'))),
              (
               '^( *\\.\\.)(\\s*)(\\[.+\\])(.*?)$',
               bygroups(Punctuation, Text, Name.Tag, using(this, state='inline'))),
              (
               '^( *\\.\\.)(\\s*)(\\|.+\\|)(\\s*)([\\w:-]+?)(::)(?:([ \\t]*)(.*))',
               bygroups(Punctuation, Text, Name.Tag, Text, Operator.Word, Punctuation, Text, using(this, state='inline'))),
              (
               '^ *\\.\\..*(\\n( +.*\\n|\\n)+)?', Comment.Preproc),
              (
               '^( *)(:[a-zA-Z-]+:)(\\s*)$', bygroups(Text, Name.Class, Text)),
              (
               '^( *)(:.*?:)([ \\t]+)(.*?)$',
               bygroups(Text, Name.Class, Text, Name.Function)),
              (
               '^(\\S.*(?<!::)\\n)((?:(?: +.*)\\n)+)',
               bygroups(using(this, state='inline'), using(this, state='inline'))),
              (
               '(::)(\\n[ \\t]*\\n)([ \\t]+)(.*)(\\n)((?:(?:\\3.*|)\\n)+)',
               bygroups(String.Escape, Text, String, String, Text, String)),
              include('inline')], 
     
     'inline': [
                (
                 '\\\\.', Text),
                (
                 '``', String, 'literal'),
                (
                 '(`.+?)(<.+?>)(`__?)',
                 bygroups(String, String.Interpol, String)),
                (
                 '`.+?`__?', String),
                (
                 '(`.+?`)(:[a-zA-Z0-9:-]+?:)?',
                 bygroups(Name.Variable, Name.Attribute)),
                (
                 '(:[a-zA-Z0-9:-]+?:)(`.+?`)',
                 bygroups(Name.Attribute, Name.Variable)),
                (
                 '\\*\\*.+?\\*\\*', Generic.Strong),
                (
                 '\\*.+?\\*', Generic.Emph),
                (
                 '\\[.*?\\]_', String),
                (
                 '<.+?>', Name.Tag),
                (
                 '[^\\\\\\n\\[*`:]+', Text),
                (
                 '.', Text)], 
     
     'literal': [
                 (
                  '[^`]+', String),
                 (
                  '``' + end_string_suffix, String, '#pop'),
                 (
                  '`', String)]}

    def __init__(self, **options):
        self.handlecodeblocks = get_bool_opt(options, 'handlecodeblocks', True)
        RegexLexer.__init__(self, **options)

    def analyse_text(text):
        if text[:2] == '..' and text[2:3] != '.':
            return 0.3
        p1 = text.find('\n')
        p2 = text.find('\n', p1 + 1)
        if p2 > -1 and p1 * 2 + 1 == p2 and text[(p1 + 1)] in '-=' and text[(p1 + 1)] == text[(p2 - 1)]:
            return 0.5


class TexLexer(RegexLexer):
    __doc__ = '\n    Lexer for the TeX and LaTeX typesetting languages.\n    '
    name = 'TeX'
    aliases = ['tex', 'latex']
    filenames = ['*.tex', '*.aux', '*.toc']
    mimetypes = ['text/x-tex', 'text/x-latex']
    tokens = {'general': [
                 (
                  '%.*?\\n', Comment),
                 (
                  '[{}]', Name.Builtin),
                 (
                  '[&_^]', Name.Builtin)], 
     
     'root': [
              (
               '\\\\\\[', String.Backtick, 'displaymath'),
              (
               '\\\\\\(', String, 'inlinemath'),
              (
               '\\$\\$', String.Backtick, 'displaymath'),
              (
               '\\$', String, 'inlinemath'),
              (
               '\\\\([a-zA-Z]+|.)', Keyword, 'command'),
              (
               '\\\\$', Keyword),
              include('general'),
              (
               '[^\\\\$%&_^{}]+', Text)], 
     
     'math': [
              (
               '\\\\([a-zA-Z]+|.)', Name.Variable),
              include('general'),
              (
               '[0-9]+', Number),
              (
               '[-=!+*/()\\[\\]]', Operator),
              (
               '[^=!+*/()\\[\\]\\\\$%&_^{}0-9-]+', Name.Builtin)], 
     
     'inlinemath': [
                    (
                     '\\\\\\)', String, '#pop'),
                    (
                     '\\$', String, '#pop'),
                    include('math')], 
     
     'displaymath': [
                     (
                      '\\\\\\]', String, '#pop'),
                     (
                      '\\$\\$', String, '#pop'),
                     (
                      '\\$', Name.Builtin),
                     include('math')], 
     
     'command': [
                 (
                  '\\[.*?\\]', Name.Attribute),
                 (
                  '\\*', Keyword),
                 default('#pop')]}

    def analyse_text(text):
        for start in ('\\documentclass', '\\input', '\\documentstyle', '\\relax'):
            if text[:len(start)] == start:
                return True


class GroffLexer(RegexLexer):
    __doc__ = '\n    Lexer for the (g)roff typesetting language, supporting groff\n    extensions. Mainly useful for highlighting manpage sources.\n\n    .. versionadded:: 0.6\n    '
    name = 'Groff'
    aliases = ['groff', 'nroff', 'man']
    filenames = ['*.[1234567]', '*.man']
    mimetypes = ['application/x-troff', 'text/troff']
    tokens = {'root': [
              (
               '(\\.)(\\w+)', bygroups(Text, Keyword), 'request'),
              (
               '\\.', Punctuation, 'request'),
              (
               '[^\\\\\\n]+', Text, 'textline'),
              default('textline')], 
     
     'textline': [
                  include('escapes'),
                  (
                   '[^\\\\\\n]+', Text),
                  (
                   '\\n', Text, '#pop')], 
     
     'escapes': [
                 (
                  '\\\\"[^\\n]*', Comment),
                 (
                  '\\\\[fn]\\w', String.Escape),
                 (
                  '\\\\\\(.{2}', String.Escape),
                 (
                  '\\\\.\\[.*\\]', String.Escape),
                 (
                  '\\\\.', String.Escape),
                 (
                  '\\\\\\n', Text, 'request')], 
     
     'request': [
                 (
                  '\\n', Text, '#pop'),
                 include('escapes'),
                 (
                  '"[^\\n"]+"', String.Double),
                 (
                  '\\d+', Number),
                 (
                  '\\S+', String),
                 (
                  '\\s+', Text)]}

    def analyse_text(text):
        if text[:1] != '.':
            return False
        if text[:3] == '.\\"':
            return True
        if text[:4] == '.TH ':
            return True
        if text[1:3].isalnum() and text[3].isspace():
            return 0.9


class MozPreprocHashLexer(RegexLexer):
    __doc__ = "\n    Lexer for Mozilla Preprocessor files (with '#' as the marker).\n\n    Other data is left untouched.\n\n    .. versionadded:: 2.0\n    "
    name = 'mozhashpreproc'
    aliases = [name]
    filenames = []
    mimetypes = []
    tokens = {'root': [
              (
               '^#', Comment.Preproc, ('expr', 'exprstart')),
              (
               '.+', Other)], 
     
     'exprstart': [
                   (
                    '(literal)(.*)', bygroups(Comment.Preproc, Text), '#pop:2'),
                   (
                    words(('define', 'undef', 'if', 'ifdef', 'ifndef', 'else', 'elif', 'elifdef', 'elifndef',
       'endif', 'expand', 'filter', 'unfilter', 'include', 'includesubst', 'error')),
                    Comment.Preproc, '#pop')], 
     
     'expr': [
              (
               words(('!', '!=', '==', '&&', '||')), Operator),
              (
               '(defined)(\\()', bygroups(Keyword, Punctuation)),
              (
               '\\)', Punctuation),
              (
               '[0-9]+', Number.Decimal),
              (
               '__\\w+?__', Name.Variable),
              (
               '@\\w+?@', Name.Class),
              (
               '\\w+', Name),
              (
               '\\n', Text, '#pop'),
              (
               '\\s+', Text),
              (
               '\\S', Punctuation)]}


class MozPreprocPercentLexer(MozPreprocHashLexer):
    __doc__ = "\n    Lexer for Mozilla Preprocessor files (with '%' as the marker).\n\n    Other data is left untouched.\n\n    .. versionadded:: 2.0\n    "
    name = 'mozpercentpreproc'
    aliases = [name]
    filenames = []
    mimetypes = []
    tokens = {'root': [
              (
               '^%', Comment.Preproc, ('expr', 'exprstart')),
              (
               '.+', Other)]}


class MozPreprocXulLexer(DelegatingLexer):
    __doc__ = '\n    Subclass of the `MozPreprocHashLexer` that highlights unlexed data with the\n    `XmlLexer`.\n\n    .. versionadded:: 2.0\n    '
    name = 'XUL+mozpreproc'
    aliases = ['xul+mozpreproc']
    filenames = ['*.xul.in']
    mimetypes = []

    def __init__(self, **options):
        super(MozPreprocXulLexer, self).__init__(XmlLexer, MozPreprocHashLexer, **options)


class MozPreprocJavascriptLexer(DelegatingLexer):
    __doc__ = '\n    Subclass of the `MozPreprocHashLexer` that highlights unlexed data with the\n    `JavascriptLexer`.\n\n    .. versionadded:: 2.0\n    '
    name = 'Javascript+mozpreproc'
    aliases = ['javascript+mozpreproc']
    filenames = ['*.js.in']
    mimetypes = []

    def __init__(self, **options):
        super(MozPreprocJavascriptLexer, self).__init__(JavascriptLexer, MozPreprocHashLexer, **options)


class MozPreprocCssLexer(DelegatingLexer):
    __doc__ = '\n    Subclass of the `MozPreprocHashLexer` that highlights unlexed data with the\n    `CssLexer`.\n\n    .. versionadded:: 2.0\n    '
    name = 'CSS+mozpreproc'
    aliases = ['css+mozpreproc']
    filenames = ['*.css.in']
    mimetypes = []

    def __init__(self, **options):
        super(MozPreprocCssLexer, self).__init__(CssLexer, MozPreprocPercentLexer, **options)