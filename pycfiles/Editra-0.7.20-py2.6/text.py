# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/lexers/text.py
# Compiled at: 2011-04-22 17:53:26
"""
    pygments.lexers.text
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for non-source code file types.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from bisect import bisect
from pygments.lexer import Lexer, LexerContext, RegexLexer, ExtendedRegexLexer, bygroups, include, using, this, do_insertions
from pygments.token import Punctuation, Text, Comment, Keyword, Name, String, Generic, Operator, Number, Whitespace, Literal
from pygments.util import get_bool_opt
from pygments.lexers.other import BashLexer
__all__ = [
 'IniLexer', 'PropertiesLexer', 'SourcesListLexer', 'BaseMakefileLexer',
 'MakefileLexer', 'DiffLexer', 'IrcLogsLexer', 'TexLexer',
 'GroffLexer', 'ApacheConfLexer', 'BBCodeLexer', 'MoinWikiLexer',
 'RstLexer', 'VimLexer', 'GettextLexer', 'SquidConfLexer',
 'DebianControlLexer', 'DarcsPatchLexer', 'YamlLexer',
 'LighttpdConfLexer', 'NginxConfLexer', 'CMakeLexer']

class IniLexer(RegexLexer):
    """
    Lexer for configuration files in INI style.
    """
    name = 'INI'
    aliases = ['ini', 'cfg']
    filenames = ['*.ini', '*.cfg']
    mimetypes = ['text/x-ini']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '[;#].*?$', Comment),
              (
               '\\[.*?\\]$', Keyword),
              (
               '(.*?)([ \\t]*)(=)([ \\t]*)(.*(?:\\n[ \\t].+)*)',
               bygroups(Name.Attribute, Text, Operator, Text, String))]}

    def analyse_text(text):
        npos = text.find('\n')
        if npos < 3:
            return False
        return text[0] == '[' and text[(npos - 1)] == ']'


class PropertiesLexer(RegexLexer):
    """
    Lexer for configuration files in Java's properties format.

    *New in Pygments 1.4.*
    """
    name = 'Properties'
    aliases = ['properties']
    filenames = ['*.properties']
    mimetypes = ['text/x-java-properties']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '(?:[;#]|//).*$', Comment),
              (
               '(.*?)([ \\t]*)([=:])([ \\t]*)(.*(?:(?<=\\\\)\\n.*)*)',
               bygroups(Name.Attribute, Text, Operator, Text, String))]}


class SourcesListLexer(RegexLexer):
    """
    Lexer that highlights debian sources.list files.

    *New in Pygments 0.7.*
    """
    name = 'Debian Sourcelist'
    aliases = ['sourceslist', 'sources.list']
    filenames = ['sources.list']
    mimetype = ['application/x-debian-sourceslist']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '#.*?$', Comment),
              (
               '^(deb(?:-src)?)(\\s+)',
               bygroups(Keyword, Text), 'distribution')], 
       'distribution': [
                      (
                       '#.*?$', Comment, '#pop'),
                      (
                       '\\$\\(ARCH\\)', Name.Variable),
                      (
                       '[^\\s$[]+', String),
                      (
                       '\\[', String.Other, 'escaped-distribution'),
                      (
                       '\\$', String),
                      (
                       '\\s+', Text, 'components')], 
       'escaped-distribution': [
                              (
                               '\\]', String.Other, '#pop'),
                              (
                               '\\$\\(ARCH\\)', Name.Variable),
                              (
                               '[^\\]$]+', String.Other),
                              (
                               '\\$', String.Other)], 
       'components': [
                    (
                     '#.*?$', Comment, '#pop:2'),
                    (
                     '$', Text, '#pop:2'),
                    (
                     '\\s+', Text),
                    (
                     '\\S+', Keyword.Pseudo)]}

    def analyse_text(text):
        for line in text.split('\n'):
            line = line.strip()
            if not (line.startswith('#') or line.startswith('deb ') or line.startswith('deb-src ') or not line):
                return False

        return True


class MakefileLexer(Lexer):
    """
    Lexer for BSD and GNU make extensions (lenient enough to handle both in
    the same file even).

    *Rewritten in Pygments 0.10.*
    """
    name = 'Makefile'
    aliases = ['make', 'makefile', 'mf', 'bsdmake']
    filenames = ['*.mak', 'Makefile', 'makefile', 'Makefile.*', 'GNUmakefile']
    mimetypes = ['text/x-makefile']
    r_special = re.compile('^(?:\\.\\s*(include|undef|error|warning|if|else|elif|endif|for|endfor)|\\s*(ifeq|ifneq|ifdef|ifndef|else|endif|-?include|define|endef|:))(?=\\s)')
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
            elif self.r_comment.match(line):
                ins.append((len(done), [(0, Comment, line)]))
            else:
                done += line

        for item in do_insertions(ins, lex.get_tokens_unprocessed(done)):
            yield item


class BaseMakefileLexer(RegexLexer):
    """
    Lexer for simple Makefiles (no preprocessing).

    *New in Pygments 0.10.*
    """
    name = 'Makefile'
    aliases = ['basemake']
    filenames = []
    mimetypes = []
    tokens = {'root': [
              (
               '^(?:[\\t ]+.*\\n|\\n)+', using(BashLexer)),
              (
               '\\$\\((?:.*\\\\\\n|.*\\n)+', using(BashLexer)),
              (
               '\\s+', Text),
              (
               '#.*?\\n', Comment),
              (
               '(export)(\\s+)(?=[a-zA-Z0-9_${}\\t -]+\\n)',
               bygroups(Keyword, Text), 'export'),
              (
               'export\\s+', Keyword),
              (
               '([a-zA-Z0-9_${}.-]+)(\\s*)([!?:+]?=)([ \\t]*)((?:.*\\\\\\n|.*\\n)+)',
               bygroups(Name.Variable, Text, Operator, Text, using(BashLexer))),
              (
               '(?s)"(\\\\\\\\|\\\\.|[^"\\\\])*"', String.Double),
              (
               "(?s)'(\\\\\\\\|\\\\.|[^'\\\\])*'", String.Single),
              (
               '([^\\n:]+)(:+)([ \\t]*)', bygroups(Name.Function, Operator, Text),
               'block-header')], 
       'export': [
                (
                 '[a-zA-Z0-9_${}-]+', Name.Variable),
                (
                 '\\n', Text, '#pop'),
                (
                 '\\s+', Text)], 
       'block-header': [
                      (
                       '[^,\\\\\\n#]+', Number),
                      (
                       ',', Punctuation),
                      (
                       '#.*?\\n', Comment),
                      (
                       '\\\\\\n', Text),
                      (
                       '\\\\.', Text),
                      (
                       '(?:[\\t ]+.*\\n|\\n)+', using(BashLexer), '#pop')]}


class DiffLexer(RegexLexer):
    """
    Lexer for unified or context-style diffs or patches.
    """
    name = 'Diff'
    aliases = ['diff', 'udiff']
    filenames = ['*.diff', '*.patch']
    mimetypes = ['text/x-diff', 'text/x-patch']
    tokens = {'root': [
              (
               ' .*\\n', Text),
              (
               '\\+.*\\n', Generic.Inserted),
              (
               '-.*\\n', Generic.Deleted),
              (
               '!.*\\n', Generic.Strong),
              (
               '@.*\\n', Generic.Subheading),
              (
               '([Ii]ndex|diff).*\\n', Generic.Heading),
              (
               '=.*\\n', Generic.Heading),
              (
               '.*\\n', Text)]}

    def analyse_text(text):
        if text[:7] == 'Index: ':
            return True
        if text[:5] == 'diff ':
            return True
        if text[:4] == '--- ':
            return 0.9


DPATCH_KEYWORDS = [
 'hunk', 'addfile', 'adddir', 'rmfile', 'rmdir', 'move',
 'replace']

class DarcsPatchLexer(RegexLexer):
    """
    DarcsPatchLexer is a lexer for the various versions of the darcs patch
    format.  Examples of this format are derived by commands such as
    ``darcs annotate --patch`` and ``darcs send``.

    *New in Pygments 0.10.*
    """
    name = 'Darcs Patch'
    aliases = ['dpatch']
    filenames = ['*.dpatch', '*.darcspatch']
    tokens = {'root': [
              (
               '<', Operator),
              (
               '>', Operator),
              (
               '{', Operator),
              (
               '}', Operator),
              (
               '(\\[)((?:TAG )?)(.*)(\\n)(.*)(\\*\\*)(\\d+)(\\s?)(\\])',
               bygroups(Operator, Keyword, Name, Text, Name, Operator, Literal.Date, Text, Operator)),
              (
               '(\\[)((?:TAG )?)(.*)(\\n)(.*)(\\*\\*)(\\d+)(\\s?)',
               bygroups(Operator, Keyword, Name, Text, Name, Operator, Literal.Date, Text), 'comment'),
              (
               'New patches:', Generic.Heading),
              (
               'Context:', Generic.Heading),
              (
               'Patch bundle hash:', Generic.Heading),
              (
               '(\\s*)(%s)(.*\\n)' % ('|').join(DPATCH_KEYWORDS),
               bygroups(Text, Keyword, Text)),
              (
               '\\+', Generic.Inserted, 'insert'),
              (
               '-', Generic.Deleted, 'delete'),
              (
               '.*\\n', Text)], 
       'comment': [
                 (
                  '[^\\]].*\\n', Comment),
                 (
                  '\\]', Operator, '#pop')], 
       'specialText': [
                     (
                      '\\n', Text, '#pop'),
                     (
                      '\\[_[^_]*_]', Operator)], 
       'insert': [
                include('specialText'),
                (
                 '\\[', Generic.Inserted),
                (
                 '[^\\n\\[]*', Generic.Inserted)], 
       'delete': [
                include('specialText'),
                (
                 '\\[', Generic.Deleted),
                (
                 '[^\\n\\[]*', Generic.Deleted)]}


class IrcLogsLexer(RegexLexer):
    """
    Lexer for IRC logs in *irssi*, *xchat* or *weechat* style.
    """
    name = 'IRC logs'
    aliases = ['irc']
    filenames = ['*.weechatlog']
    mimetypes = ['text/x-irclog']
    flags = re.VERBOSE | re.MULTILINE
    timestamp = '\n        (\n          # irssi / xchat and others\n          (?: \\[|\\()?                  # Opening bracket or paren for the timestamp\n            (?:                        # Timestamp\n                (?: (?:\\d{1,4} [-/]?)+ # Date as - or /-separated groups of digits\n                 [T ])?                # Date/time separator: T or space\n                (?: \\d?\\d [:.]?)+      # Time as :/.-separated groups of 1 or 2 digits\n            )\n          (?: \\]|\\))?\\s+               # Closing bracket or paren for the timestamp\n        |\n          # weechat\n          \\d{4}\\s\\w{3}\\s\\d{2}\\s        # Date\n          \\d{2}:\\d{2}:\\d{2}\\s+         # Time + Whitespace\n        |\n          # xchat\n          \\w{3}\\s\\d{2}\\s               # Date\n          \\d{2}:\\d{2}:\\d{2}\\s+         # Time + Whitespace\n        )?\n    '
    tokens = {'root': [
              (
               '^\\*\\*\\*\\*(.*)\\*\\*\\*\\*$', Comment),
              (
               '^' + timestamp + '(\\s*<[^>]*>\\s*)$', bygroups(Comment.Preproc, Name.Tag)),
              (
               '^' + timestamp + '\n                (\\s*<.*?>\\s*)          # Nick ',
               bygroups(Comment.Preproc, Name.Tag), 'msg'),
              (
               '^' + timestamp + '\n                (\\s*[*]\\s+)            # Star\n                ([^\\s]+\\s+.*?\\n)       # Nick + rest of message ',
               bygroups(Comment.Preproc, Keyword, Generic.Inserted)),
              (
               '^' + timestamp + '\n                (\\s*(?:\\*{3}|<?-[!@=P]?->?)\\s*)  # Star(s) or symbols\n                ([^\\s]+\\s+)                     # Nick + Space\n                (.*?\\n)                         # Rest of message ',
               bygroups(Comment.Preproc, Keyword, String, Comment)),
              (
               '^.*?\\n', Text)], 
       'msg': [
             (
              '[^\\s]+:(?!//)', Name.Attribute),
             (
              '.*\\n', Text, '#pop')]}


class BBCodeLexer(RegexLexer):
    """
    A lexer that highlights BBCode(-like) syntax.

    *New in Pygments 0.6.*
    """
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


class TexLexer(RegexLexer):
    """
    Lexer for the TeX and LaTeX typesetting languages.
    """
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
                 (
                  '', Text, '#pop')]}

    def analyse_text(text):
        for start in ('\\documentclass', '\\input', '\\documentstyle', '\\relax'):
            if text[:len(start)] == start:
                return True


class GroffLexer(RegexLexer):
    """
    Lexer for the (g)roff typesetting language, supporting groff
    extensions. Mainly useful for highlighting manpage sources.

    *New in Pygments 0.6.*
    """
    name = 'Groff'
    aliases = ['groff', 'nroff', 'man']
    filenames = ['*.[1234567]', '*.man']
    mimetypes = ['application/x-troff', 'text/troff']
    tokens = {'root': [
              (
               '(?i)(\\.)(\\w+)', bygroups(Text, Keyword), 'request'),
              (
               '\\.', Punctuation, 'request'),
              (
               '[^\\\\\\n]*', Text, 'textline')], 
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
                  '\\\\\\(..', String.Escape),
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


class ApacheConfLexer(RegexLexer):
    """
    Lexer for configuration files following the Apache config file
    format.

    *New in Pygments 0.6.*
    """
    name = 'ApacheConf'
    aliases = ['apacheconf', 'aconf', 'apache']
    filenames = ['.htaccess', 'apache.conf', 'apache2.conf']
    mimetypes = ['text/x-apacheconf']
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '(#.*?)$', Comment),
              (
               '(<[^\\s>]+)(?:(\\s+)(.*?))?(>)',
               bygroups(Name.Tag, Text, String, Name.Tag)),
              (
               '([a-zA-Z][a-zA-Z0-9]*)(\\s+)',
               bygroups(Name.Builtin, Text), 'value'),
              (
               '\\.+', Text)], 
       'value': [
               (
                '$', Text, '#pop'),
               (
                '[^\\S\\n]+', Text),
               (
                '\\d+\\.\\d+\\.\\d+\\.\\d+(?:/\\d+)?', Number),
               (
                '\\d+', Number),
               (
                '/([a-zA-Z0-9][a-zA-Z0-9_./-]+)', String.Other),
               (
                '(on|off|none|any|all|double|email|dns|min|minimal|os|productonly|full|emerg|alert|crit|error|warn|notice|info|debug|registry|script|inetd|standalone|user|group)\\b',
                Keyword),
               (
                '"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)"', String.Double),
               (
                '[^\\s"]+', Text)]}


class MoinWikiLexer(RegexLexer):
    """
    For MoinMoin (and Trac) Wiki markup.

    *New in Pygments 0.7.*
    """
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
               '({{{)(\\n#!.+)?', bygroups(Name.Builtin, Name.Namespace), 'codeblock'),
              (
               "(\\'\\'\\'?|\\|\\||`|__|~~|\\^|,,|::)", Comment),
              (
               '^( +)([.*-])( )', bygroups(Text, Name.Builtin, Text)),
              (
               '^( +)([a-zivx]{1,5}\\.)( )', bygroups(Text, Name.Builtin, Text)),
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
                    '}}}', Name.Builtin, '#pop'),
                   (
                    '{{{', Text, '#push'),
                   (
                    '[^{}]+', Comment.Preproc),
                   (
                    '.', Comment.Preproc)]}


class RstLexer(RegexLexer):
    """
    For `reStructuredText <http://docutils.sf.net/rst.html>`_ markup.

    *New in Pygments 0.7.*

    Additional options accepted:

    `handlecodeblocks`
        Highlight the contents of ``.. sourcecode:: langauge`` and
        ``.. code:: language`` directives with a lexer for the given
        language (default: ``True``). *New in Pygments 0.8.*
    """
    name = 'reStructuredText'
    aliases = ['rst', 'rest', 'restructuredtext']
    filenames = ['*.rst', '*.rest']
    mimetypes = ['text/x-rst', 'text/prs.fallenstein.rst']
    flags = re.MULTILINE

    def _handle_sourcecode(self, match):
        from pygments.lexers import get_lexer_by_name
        from pygments.util import ClassNotFound
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
        else:
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

            return

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
               '^( *\\.\\.)(\\s*)((?:source)?code)(::)([ \\t]*)([^\\n]+)(\\n[ \\t]*\\n)([ \\t]+)(.*)(\\n)((?:(?:\\8.*|)\\n)+)',
               _handle_sourcecode),
              (
               '^( *\\.\\.)(\\s*)([\\w:-]+?)(::)(?:([ \\t]*)(.*))',
               bygroups(Punctuation, Text, Operator.Word, Punctuation, Text, using(this, state='inline'))),
              (
               '^( *\\.\\.)(\\s*)([\\w\\t ]+:)(.*?)$',
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
               '^([^ ].*(?<!::)\\n)((?:(?: +.*)\\n)+)',
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
                  '[^`\\\\]+', String),
                 (
                  '\\\\.', String),
                 (
                  '``', String, '#pop'),
                 (
                  '[`\\\\]', String)]}

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


class VimLexer(RegexLexer):
    """
    Lexer for VimL script files.

    *New in Pygments 0.8.*
    """
    name = 'VimL'
    aliases = ['vim']
    filenames = ['*.vim', '.vimrc']
    mimetypes = ['text/x-vim']
    flags = re.MULTILINE
    tokens = {'root': [
              (
               '^\\s*".*', Comment),
              (
               '(?<=\\s)"[^\\-:.%#=*].*', Comment),
              (
               '[ \\t]+', Text),
              (
               '/(\\\\\\\\|\\\\/|[^\\n/])*/', String.Regex),
              (
               '"(\\\\\\\\|\\\\"|[^\\n"])*"', String.Double),
              (
               "'(\\\\\\\\|\\\\'|[^\\n'])*'", String.Single),
              (
               '-?\\d+', Number),
              (
               '#[0-9a-f]{6}', Number.Hex),
              (
               '^:', Punctuation),
              (
               '[()<>+=!|,~-]', Punctuation),
              (
               '\\b(let|if|else|endif|elseif|fun|function|endfunction)\\b',
               Keyword),
              (
               '\\b(NONE|bold|italic|underline|dark|light)\\b', Name.Builtin),
              (
               '\\b\\w+\\b', Name.Other),
              (
               '.', Text)]}

    def __init__(self, **options):
        from pygments.lexers._vimbuiltins import command, option, auto
        self._cmd = command
        self._opt = option
        self._aut = auto
        RegexLexer.__init__(self, **options)

    def is_in(self, w, mapping):
        r"""
        It's kind of difficult to decide if something might be a keyword
        in VimL because it allows you to abbreviate them.  In fact,
        'ab[breviate]' is a good example.  :ab, :abbre, or :abbreviate are
        valid ways to call it so rather than making really awful regexps
        like::

            \bab(?:b(?:r(?:e(?:v(?:i(?:a(?:t(?:e)?)?)?)?)?)?)?)?\b

        we match `\b\w+\b` and then call is_in() on those tokens.  See
        `scripts/get_vimkw.py` for how the lists are extracted.
        """
        p = bisect(mapping, (w,))
        if p > 0:
            if mapping[(p - 1)][0] == w[:len(mapping[(p - 1)][0])] and mapping[(p - 1)][1][:len(w)] == w:
                return True
        if p < len(mapping):
            return mapping[p][0] == w[:len(mapping[p][0])] and mapping[p][1][:len(w)] == w
        return False

    def get_tokens_unprocessed(self, text):
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name.Other:
                if self.is_in(value, self._cmd):
                    yield (
                     index, Keyword, value)
                elif self.is_in(value, self._opt) or self.is_in(value, self._aut):
                    yield (
                     index, Name.Builtin, value)
                else:
                    yield (
                     index, Text, value)
            else:
                yield (
                 index, token, value)


class GettextLexer(RegexLexer):
    """
    Lexer for Gettext catalog files.

    *New in Pygments 0.9.*
    """
    name = 'Gettext Catalog'
    aliases = ['pot', 'po']
    filenames = ['*.pot', '*.po']
    mimetypes = ['application/x-gettext', 'text/x-gettext', 'text/gettext']
    tokens = {'root': [
              (
               '^#,\\s.*?$', Keyword.Type),
              (
               '^#:\\s.*?$', Keyword.Declaration),
              (
               '^(#|#\\.\\s|#\\|\\s|#~\\s|#\\s).*$', Comment.Single),
              (
               '^(")([A-Za-z-]+:)(.*")$',
               bygroups(String, Name.Property, String)),
              (
               '^".*"$', String),
              (
               '^(msgid|msgid_plural|msgstr)(\\s+)(".*")$',
               bygroups(Name.Variable, Text, String)),
              (
               '^(msgstr\\[)(\\d)(\\])(\\s+)(".*")$',
               bygroups(Name.Variable, Number.Integer, Name.Variable, Text, String))]}


class SquidConfLexer(RegexLexer):
    """
    Lexer for `squid <http://www.squid-cache.org/>`_ configuration files.

    *New in Pygments 0.9.*
    """
    name = 'SquidConf'
    aliases = ['squidconf', 'squid.conf', 'squid']
    filenames = ['squid.conf']
    mimetypes = ['text/x-squidconf']
    flags = re.IGNORECASE
    keywords = [
     'acl', 'always_direct', 'announce_host',
     'announce_period', 'announce_port', 'announce_to',
     'anonymize_headers', 'append_domain', 'as_whois_server',
     'auth_param_basic', 'authenticate_children',
     'authenticate_program', 'authenticate_ttl', 'broken_posts',
     'buffered_logs', 'cache_access_log', 'cache_announce',
     'cache_dir', 'cache_dns_program', 'cache_effective_group',
     'cache_effective_user', 'cache_host', 'cache_host_acl',
     'cache_host_domain', 'cache_log', 'cache_mem',
     'cache_mem_high', 'cache_mem_low', 'cache_mgr',
     'cachemgr_passwd', 'cache_peer', 'cache_peer_access',
     'cahce_replacement_policy', 'cache_stoplist',
     'cache_stoplist_pattern', 'cache_store_log', 'cache_swap',
     'cache_swap_high', 'cache_swap_log', 'cache_swap_low',
     'client_db', 'client_lifetime', 'client_netmask',
     'connect_timeout', 'coredump_dir', 'dead_peer_timeout',
     'debug_options', 'delay_access', 'delay_class',
     'delay_initial_bucket_level', 'delay_parameters',
     'delay_pools', 'deny_info', 'dns_children', 'dns_defnames',
     'dns_nameservers', 'dns_testnames', 'emulate_httpd_log',
     'err_html_text', 'fake_user_agent', 'firewall_ip',
     'forwarded_for', 'forward_snmpd_port', 'fqdncache_size',
     'ftpget_options', 'ftpget_program', 'ftp_list_width',
     'ftp_passive', 'ftp_user', 'half_closed_clients',
     'header_access', 'header_replace', 'hierarchy_stoplist',
     'high_response_time_warning', 'high_page_fault_warning',
     'htcp_port', 'http_access', 'http_anonymizer', 'httpd_accel',
     'httpd_accel_host', 'httpd_accel_port',
     'httpd_accel_uses_host_header', 'httpd_accel_with_proxy',
     'http_port', 'http_reply_access', 'icp_access',
     'icp_hit_stale', 'icp_port', 'icp_query_timeout',
     'ident_lookup', 'ident_lookup_access', 'ident_timeout',
     'incoming_http_average', 'incoming_icp_average',
     'inside_firewall', 'ipcache_high', 'ipcache_low',
     'ipcache_size', 'local_domain', 'local_ip', 'logfile_rotate',
     'log_fqdn', 'log_icp_queries', 'log_mime_hdrs',
     'maximum_object_size', 'maximum_single_addr_tries',
     'mcast_groups', 'mcast_icp_query_timeout', 'mcast_miss_addr',
     'mcast_miss_encode_key', 'mcast_miss_port', 'memory_pools',
     'memory_pools_limit', 'memory_replacement_policy',
     'mime_table', 'min_http_poll_cnt', 'min_icp_poll_cnt',
     'minimum_direct_hops', 'minimum_object_size',
     'minimum_retry_timeout', 'miss_access', 'negative_dns_ttl',
     'negative_ttl', 'neighbor_timeout', 'neighbor_type_domain',
     'netdb_high', 'netdb_low', 'netdb_ping_period',
     'netdb_ping_rate', 'never_direct', 'no_cache',
     'passthrough_proxy', 'pconn_timeout', 'pid_filename',
     'pinger_program', 'positive_dns_ttl', 'prefer_direct',
     'proxy_auth', 'proxy_auth_realm', 'query_icmp', 'quick_abort',
     'quick_abort', 'quick_abort_max', 'quick_abort_min',
     'quick_abort_pct', 'range_offset_limit', 'read_timeout',
     'redirect_children', 'redirect_program',
     'redirect_rewrites_host_header', 'reference_age',
     'reference_age', 'refresh_pattern', 'reload_into_ims',
     'request_body_max_size', 'request_size', 'request_timeout',
     'shutdown_lifetime', 'single_parent_bypass',
     'siteselect_timeout', 'snmp_access', 'snmp_incoming_address',
     'snmp_port', 'source_ping', 'ssl_proxy',
     'store_avg_object_size', 'store_objects_per_bucket',
     'strip_query_terms', 'swap_level1_dirs', 'swap_level2_dirs',
     'tcp_incoming_address', 'tcp_outgoing_address',
     'tcp_recv_bufsize', 'test_reachability', 'udp_hit_obj',
     'udp_hit_obj_size', 'udp_incoming_address',
     'udp_outgoing_address', 'unique_hostname', 'unlinkd_program',
     'uri_whitespace', 'useragent_log', 'visible_hostname',
     'wais_relay', 'wais_relay_host', 'wais_relay_port']
    opts = [
     'proxy-only', 'weight', 'ttl', 'no-query', 'default',
     'round-robin', 'multicast-responder', 'on', 'off', 'all',
     'deny', 'allow', 'via', 'parent', 'no-digest', 'heap', 'lru',
     'realm', 'children', 'credentialsttl', 'none', 'disable',
     'offline_toggle', 'diskd', 'q1', 'q2']
    actions = [
     'shutdown', 'info', 'parameter', 'server_list',
     'client_list', 'squid\\.conf']
    actions_stats = [
     'objects', 'vm_objects', 'utilization',
     'ipcache', 'fqdncache', 'dns', 'redirector', 'io',
     'reply_headers', 'filedescriptors', 'netdb']
    actions_log = [
     'status', 'enable', 'disable', 'clear']
    acls = [
     'url_regex', 'urlpath_regex', 'referer_regex', 'port',
     'proto', 'req_mime_type', 'rep_mime_type', 'method',
     'browser', 'user', 'src', 'dst', 'time', 'dstdomain', 'ident',
     'snmp_community']
    ip_re = '\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b'

    def makelistre(list):
        return '\\b(?:' + ('|').join(list) + ')\\b'

    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '#', Comment, 'comment'),
              (
               makelistre(keywords), Keyword),
              (
               makelistre(opts), Name.Constant),
              (
               makelistre(actions), String),
              (
               'stats/' + makelistre(actions), String),
              (
               'log/' + makelistre(actions) + '=', String),
              (
               makelistre(acls), Keyword),
              (
               ip_re + '(?:/(?:' + ip_re + ')|\\d+)?', Number),
              (
               '\\b\\d+\\b', Number),
              (
               '\\S+', Text)], 
       'comment': [
                 (
                  '\\s*TAG:.*', String.Escape, '#pop'),
                 (
                  '.*', Comment, '#pop')]}


class DebianControlLexer(RegexLexer):
    """
    Lexer for Debian ``control`` files and ``apt-cache show <pkg>`` outputs.

    *New in Pygments 0.9.*
    """
    name = 'Debian Control file'
    aliases = ['control']
    filenames = ['control']
    tokens = {'root': [
              (
               '^(Description)', Keyword, 'description'),
              (
               '^(Maintainer)(:\\s*)', bygroups(Keyword, Text), 'maintainer'),
              (
               '^((Build-)?Depends)', Keyword, 'depends'),
              (
               '^((?:Python-)?Version)(:\\s*)([^\\s]+)$',
               bygroups(Keyword, Text, Number)),
              (
               '^((?:Installed-)?Size)(:\\s*)([^\\s]+)$',
               bygroups(Keyword, Text, Number)),
              (
               '^(MD5Sum|SHA1|SHA256)(:\\s*)([^\\s]+)$',
               bygroups(Keyword, Text, Number)),
              (
               '^([a-zA-Z\\-0-9\\.]*?)(:\\s*)(.*?)$',
               bygroups(Keyword, Whitespace, String))], 
       'maintainer': [
                    (
                     '<[^>]+>', Generic.Strong),
                    (
                     '<[^>]+>$', Generic.Strong, '#pop'),
                    (
                     ',\\n?', Text),
                    (
                     '.', Text)], 
       'description': [
                     (
                      '(.*)(Homepage)(: )([^\\s]+)', bygroups(Text, String, Name, Name.Class)),
                     (
                      ':.*\\n', Generic.Strong),
                     (
                      ' .*\\n', Text),
                     (
                      '', Text, '#pop')], 
       'depends': [
                 (
                  ':\\s*', Text),
                 (
                  '(\\$)(\\{)(\\w+\\s*:\\s*\\w+)', bygroups(Operator, Text, Name.Entity)),
                 (
                  '\\(', Text, 'depend_vers'),
                 (
                  ',', Text),
                 (
                  '\\|', Operator),
                 (
                  '[\\s]+', Text),
                 (
                  '[}\\)]\\s*$', Text, '#pop'),
                 (
                  '[}]', Text),
                 (
                  '[^,]$', Name.Function, '#pop'),
                 (
                  '([\\+\\.a-zA-Z0-9-][\\s\\n]*)', Name.Function),
                 (
                  '\\[.*?\\]', Name.Entity)], 
       'depend_vers': [
                     (
                      '\\),', Text, '#pop'),
                     (
                      '\\)[^,]', Text, '#pop:2'),
                     (
                      '([><=]+)(\\s*)([^\\)]+)', bygroups(Operator, Text, Number))]}


class YamlLexerContext(LexerContext):
    """Indentation context for the YAML lexer."""

    def __init__(self, *args, **kwds):
        super(YamlLexerContext, self).__init__(*args, **kwds)
        self.indent_stack = []
        self.indent = -1
        self.next_indent = 0
        self.block_scalar_indent = None
        return


class YamlLexer(ExtendedRegexLexer):
    """
    Lexer for `YAML <http://yaml.org/>`_, a human-friendly data serialization
    language.

    *New in Pygments 0.11.*
    """
    name = 'YAML'
    aliases = ['yaml']
    filenames = ['*.yaml', '*.yml']
    mimetypes = ['text/x-yaml']

    def something(token_class):
        """Do not produce empty tokens."""

        def callback(lexer, match, context):
            text = match.group()
            if not text:
                return
            yield (
             match.start(), token_class, text)
            context.pos = match.end()

        return callback

    def reset_indent(token_class):
        """Reset the indentation levels."""

        def callback(lexer, match, context):
            text = match.group()
            context.indent_stack = []
            context.indent = -1
            context.next_indent = 0
            context.block_scalar_indent = None
            yield (match.start(), token_class, text)
            context.pos = match.end()
            return

        return callback

    def save_indent(token_class, start=False):
        """Save a possible indentation level."""

        def callback(lexer, match, context):
            text = match.group()
            extra = ''
            if start:
                context.next_indent = len(text)
                if context.next_indent < context.indent:
                    while context.next_indent < context.indent:
                        context.indent = context.indent_stack.pop()

                    if context.next_indent > context.indent:
                        extra = text[context.indent:]
                        text = text[:context.indent]
            else:
                context.next_indent += len(text)
            if text:
                yield (
                 match.start(), token_class, text)
            if extra:
                yield (
                 match.start() + len(text), token_class.Error, extra)
            context.pos = match.end()

        return callback

    def set_indent(token_class, implicit=False):
        """Set the previously saved indentation level."""

        def callback(lexer, match, context):
            text = match.group()
            if context.indent < context.next_indent:
                context.indent_stack.append(context.indent)
                context.indent = context.next_indent
            if not implicit:
                context.next_indent += len(text)
            yield (
             match.start(), token_class, text)
            context.pos = match.end()

        return callback

    def set_block_scalar_indent(token_class):
        """Set an explicit indentation level for a block scalar."""

        def callback(lexer, match, context):
            text = match.group()
            context.block_scalar_indent = None
            if not text:
                return
            else:
                increment = match.group(1)
                if increment:
                    current_indent = max(context.indent, 0)
                    increment = int(increment)
                    context.block_scalar_indent = current_indent + increment
                if text:
                    yield (
                     match.start(), token_class, text)
                    context.pos = match.end()
                return

        return callback

    def parse_block_scalar_empty_line(indent_token_class, content_token_class):
        """Process an empty line in a block scalar."""

        def callback(lexer, match, context):
            text = match.group()
            if context.block_scalar_indent is None or len(text) <= context.block_scalar_indent:
                if text:
                    yield (
                     match.start(), indent_token_class, text)
            else:
                indentation = text[:context.block_scalar_indent]
                content = text[context.block_scalar_indent:]
                yield (match.start(), indent_token_class, indentation)
                yield (match.start() + context.block_scalar_indent,
                 content_token_class, content)
            context.pos = match.end()
            return

        return callback

    def parse_block_scalar_indent(token_class):
        """Process indentation spaces in a block scalar."""

        def callback(lexer, match, context):
            text = match.group()
            if context.block_scalar_indent is None:
                if len(text) <= max(context.indent, 0):
                    context.stack.pop()
                    context.stack.pop()
                    return
                context.block_scalar_indent = len(text)
            elif len(text) < context.block_scalar_indent:
                context.stack.pop()
                context.stack.pop()
                return
            if text:
                yield (
                 match.start(), token_class, text)
                context.pos = match.end()
            return

        return callback

    def parse_plain_scalar_indent(token_class):
        """Process indentation spaces in a plain scalar."""

        def callback(lexer, match, context):
            text = match.group()
            if len(text) <= context.indent:
                context.stack.pop()
                context.stack.pop()
                return
            if text:
                yield (
                 match.start(), token_class, text)
                context.pos = match.end()

        return callback

    tokens = {'root': [
              (
               '[ ]+(?=#|$)', Text),
              (
               '\\n+', Text),
              (
               '#[^\\n]*', Comment.Single),
              (
               '^%YAML(?=[ ]|$)', reset_indent(Name.Tag), 'yaml-directive'),
              (
               '^%TAG(?=[ ]|$)', reset_indent(Name.Tag), 'tag-directive'),
              (
               '^(?:---|\\.\\.\\.)(?=[ ]|$)', reset_indent(Name.Namespace),
               'block-line'),
              (
               '[ ]*(?![ \\t\\n\\r\\f\\v]|$)', save_indent(Text, start=True),
               ('block-line', 'indentation'))], 
       'ignored-line': [
                      (
                       '[ ]+(?=#|$)', Text),
                      (
                       '#[^\\n]*', Comment.Single),
                      (
                       '\\n', Text, '#pop:2')], 
       'yaml-directive': [
                        (
                         '([ ]+)([0-9]+\\.[0-9]+)',
                         bygroups(Text, Number), 'ignored-line')], 
       'tag-directive': [
                       (
                        "([ ]+)(!|![0-9A-Za-z_-]*!)([ ]+)(!|!?[0-9A-Za-z;/?:@&=+$,_.!~*\\'()\\[\\]%-]+)",
                        bygroups(Text, Keyword.Type, Text, Keyword.Type),
                        'ignored-line')], 
       'indentation': [
                     (
                      '[ ]*$', something(Text), '#pop:2'),
                     (
                      '[ ]+(?=[?:-](?:[ ]|$))', save_indent(Text)),
                     (
                      '[?:-](?=[ ]|$)', set_indent(Punctuation.Indicator)),
                     (
                      '[ ]*', save_indent(Text), '#pop')], 
       'block-line': [
                    (
                     '[ ]*(?=#|$)', something(Text), '#pop'),
                    (
                     '[ ]+', Text),
                    include('descriptors'),
                    include('block-nodes'),
                    include('flow-nodes'),
                    (
                     '(?=[^ \\t\\n\\r\\f\\v?:,\\[\\]{}#&*!|>\\\'"%@`-]|[?:-][^ \\t\\n\\r\\f\\v])',
                     something(Name.Variable),
                     'plain-scalar-in-block-context')], 
       'descriptors': [
                     (
                      "!<[0-9A-Za-z;/?:@&=+$,_.!~*\\'()\\[\\]%-]+>", Keyword.Type),
                     (
                      "!(?:[0-9A-Za-z_-]+)?(?:![0-9A-Za-z;/?:@&=+$,_.!~*\\'()\\[\\]%-]+)?",
                      Keyword.Type),
                     (
                      '&[0-9A-Za-z_-]+', Name.Label),
                     (
                      '\\*[0-9A-Za-z_-]+', Name.Variable)], 
       'block-nodes': [
                     (
                      ':(?=[ ]|$)', set_indent(Punctuation.Indicator, implicit=True)),
                     (
                      '[|>]', Punctuation.Indicator,
                      ('block-scalar-content', 'block-scalar-header'))], 
       'flow-nodes': [
                    (
                     '\\[', Punctuation.Indicator, 'flow-sequence'),
                    (
                     '\\{', Punctuation.Indicator, 'flow-mapping'),
                    (
                     "\\'", String, 'single-quoted-scalar'),
                    (
                     '\\"', String, 'double-quoted-scalar')], 
       'flow-collection': [
                         (
                          '[ ]+', Text),
                         (
                          '\\n+', Text),
                         (
                          '#[^\\n]*', Comment.Single),
                         (
                          '[?:,]', Punctuation.Indicator),
                         include('descriptors'),
                         include('flow-nodes'),
                         (
                          '(?=[^ \\t\\n\\r\\f\\v?:,\\[\\]{}#&*!|>\\\'"%@`])',
                          something(Name.Variable),
                          'plain-scalar-in-flow-context')], 
       'flow-sequence': [
                       include('flow-collection'),
                       (
                        '\\]', Punctuation.Indicator, '#pop')], 
       'flow-mapping': [
                      include('flow-collection'),
                      (
                       '\\}', Punctuation.Indicator, '#pop')], 
       'block-scalar-content': [
                              (
                               '\\n', Text),
                              (
                               '^[ ]+$',
                               parse_block_scalar_empty_line(Text, Name.Constant)),
                              (
                               '^[ ]*', parse_block_scalar_indent(Text)),
                              (
                               '[^\\n\\r\\f\\v]+', Name.Constant)], 
       'block-scalar-header': [
                             (
                              '([1-9])?[+-]?(?=[ ]|$)',
                              set_block_scalar_indent(Punctuation.Indicator),
                              'ignored-line'),
                             (
                              '[+-]?([1-9])?(?=[ ]|$)',
                              set_block_scalar_indent(Punctuation.Indicator),
                              'ignored-line')], 
       'quoted-scalar-whitespaces': [
                                   (
                                    '^[ ]+|[ ]+$', Text),
                                   (
                                    '\\n+', Text),
                                   (
                                    '[ ]+', Name.Variable)], 
       'single-quoted-scalar': [
                              include('quoted-scalar-whitespaces'),
                              (
                               "\\'\\'", String.Escape),
                              (
                               "[^ \\t\\n\\r\\f\\v\\']+", String),
                              (
                               "\\'", String, '#pop')], 
       'double-quoted-scalar': [
                              include('quoted-scalar-whitespaces'),
                              (
                               '\\\\[0abt\\tn\\nvfre "\\\\N_LP]', String),
                              (
                               '\\\\(?:x[0-9A-Fa-f]{2}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})',
                               String.Escape),
                              (
                               '[^ \\t\\n\\r\\f\\v\\"\\\\]+', String),
                              (
                               '"', String, '#pop')], 
       'plain-scalar-in-block-context-new-line': [
                                                (
                                                 '^[ ]+$', Text),
                                                (
                                                 '\\n+', Text),
                                                (
                                                 '^(?=---|\\.\\.\\.)', something(Name.Namespace), '#pop:3'),
                                                (
                                                 '^[ ]*', parse_plain_scalar_indent(Text), '#pop')], 
       'plain-scalar-in-block-context': [
                                       (
                                        '[ ]*(?=:[ ]|:$)', something(Text), '#pop'),
                                       (
                                        '[ ]+(?=#)', Text, '#pop'),
                                       (
                                        '[ ]+$', Text),
                                       (
                                        '\\n+', Text, 'plain-scalar-in-block-context-new-line'),
                                       (
                                        '[ ]+', Literal.Scalar.Plain),
                                       (
                                        '(?::(?![ \\t\\n\\r\\f\\v])|[^ \\t\\n\\r\\f\\v:])+', Literal.Scalar.Plain)], 
       'plain-scalar-in-flow-context': [
                                      (
                                       '[ ]*(?=[,:?\\[\\]{}])', something(Text), '#pop'),
                                      (
                                       '[ ]+(?=#)', Text, '#pop'),
                                      (
                                       '^[ ]+|[ ]+$', Text),
                                      (
                                       '\\n+', Text),
                                      (
                                       '[ ]+', Name.Variable),
                                      (
                                       '[^ \\t\\n\\r\\f\\v,:?\\[\\]{}]+', Name.Variable)]}

    def get_tokens_unprocessed(self, text=None, context=None):
        if context is None:
            context = YamlLexerContext(text, 0)
        return super(YamlLexer, self).get_tokens_unprocessed(text, context)


class LighttpdConfLexer(RegexLexer):
    """
    Lexer for `Lighttpd <http://lighttpd.net/>`_ configuration files.

    *New in Pygments 0.11.*
    """
    name = 'Lighttpd configuration file'
    aliases = ['lighty', 'lighttpd']
    filenames = []
    mimetypes = ['text/x-lighttpd-conf']
    tokens = {'root': [
              (
               '#.*\\n', Comment.Single),
              (
               '/\\S*', Name),
              (
               '[a-zA-Z._-]+', Keyword),
              (
               '\\d+\\.\\d+\\.\\d+\\.\\d+(?:/\\d+)?', Number),
              (
               '[0-9]+', Number),
              (
               '=>|=~|\\+=|==|=|\\+', Operator),
              (
               '\\$[A-Z]+', Name.Builtin),
              (
               '[(){}\\[\\],]', Punctuation),
              (
               '"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)"', String.Double),
              (
               '\\s+', Text)]}


class NginxConfLexer(RegexLexer):
    """
    Lexer for `Nginx <http://nginx.net/>`_ configuration files.

    *New in Pygments 0.11.*
    """
    name = 'Nginx configuration file'
    aliases = ['nginx']
    filenames = []
    mimetypes = ['text/x-nginx-conf']
    tokens = {'root': [
              (
               '(include)(\\s+)([^\\s;]+)', bygroups(Keyword, Text, Name)),
              (
               '[^\\s;#]+', Keyword, 'stmt'),
              include('base')], 
       'block': [
               (
                '}', Punctuation, '#pop:2'),
               (
                '[^\\s;#]+', Keyword.Namespace, 'stmt'),
               include('base')], 
       'stmt': [
              (
               '{', Punctuation, 'block'),
              (
               ';', Punctuation, '#pop'),
              include('base')], 
       'base': [
              (
               '#.*\\n', Comment.Single),
              (
               'on|off', Name.Constant),
              (
               '\\$[^\\s;#()]+', Name.Variable),
              (
               '([a-z0-9.-]+)(:)([0-9]+)',
               bygroups(Name, Punctuation, Number.Integer)),
              (
               '[a-z-]+/[a-z-+]+', String),
              (
               '[0-9]+[km]?\\b', Number.Integer),
              (
               '(~)(\\s*)([^\\s{]+)', bygroups(Punctuation, Text, String.Regex)),
              (
               '[:=~]', Punctuation),
              (
               '[^\\s;#{}$]+', String),
              (
               '/[^\\s;#]*', Name),
              (
               '\\s+', Text),
              (
               '[$;]', Text)]}


class CMakeLexer(RegexLexer):
    """
    Lexer for `CMake <http://cmake.org/Wiki/CMake>`_ files.

    *New in Pygments 1.2.*
    """
    name = 'CMake'
    aliases = ['cmake']
    filenames = ['*.cmake', 'CMakeLists.txt']
    mimetypes = ['text/x-cmake']
    tokens = {'root': [
              (
               '\\b([A-Za-z_]+)([ \\t]*)(\\()',
               bygroups(Name.Builtin, Text, Punctuation), 'args'),
              include('keywords'),
              include('ws')], 
       'args': [
              (
               '\\(', Punctuation, '#push'),
              (
               '\\)', Punctuation, '#pop'),
              (
               '(\\${)(.+?)(})', bygroups(Operator, Name.Variable, Operator)),
              (
               '(?s)".*?"', String.Double),
              (
               '\\\\\\S+', String),
              (
               '[^\\)$"# \\t\\n]+', String),
              (
               '\\n', Text),
              include('keywords'),
              include('ws')], 
       'string': [], 'keywords': [
                  (
                   '\\b(WIN32|UNIX|APPLE|CYGWIN|BORLAND|MINGW|MSVC|MSVC_IDE|MSVC60|MSVC70|MSVC71|MSVC80|MSVC90)\\b',
                   Keyword)], 
       'ws': [
            (
             '[ \\t]+', Text),
            (
             '#.+\\n', Comment)]}