# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/lexers/parsers.py
# Compiled at: 2011-04-22 17:53:26
"""
    pygments.lexers.parsers
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for parser generators.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, DelegatingLexer, include, bygroups, using
from pygments.token import Punctuation, Other, Text, Comment, Operator, Keyword, Name, String, Number, Whitespace
from pygments.lexers.compiled import JavaLexer, CLexer, CppLexer, ObjectiveCLexer, DLexer
from pygments.lexers.dotnet import CSharpLexer
from pygments.lexers.agile import RubyLexer, PythonLexer, PerlLexer
from pygments.lexers.web import ActionScriptLexer
__all__ = [
 'RagelLexer', 'RagelEmbeddedLexer', 'RagelCLexer', 'RagelDLexer',
 'RagelCppLexer', 'RagelObjectiveCLexer', 'RagelRubyLexer',
 'RagelJavaLexer', 'AntlrLexer', 'AntlrPythonLexer',
 'AntlrPerlLexer', 'AntlrRubyLexer', 'AntlrCppLexer',
 'AntlrCSharpLexer', 'AntlrObjectiveCLexer',
 'AntlrJavaLexer', 'AntlrActionScriptLexer']

class RagelLexer(RegexLexer):
    """
    A pure `Ragel <http://www.complang.org/ragel/>`_ lexer.  Use this for
    fragments of Ragel.  For ``.rl`` files, use RagelEmbeddedLexer instead
    (or one of the language-specific subclasses).

    *New in Pygments 1.1.*
    """
    name = 'Ragel'
    aliases = ['ragel']
    filenames = []
    tokens = {'whitespace': [
                    (
                     '\\s+', Whitespace)], 
       'comments': [
                  (
                   '\\#.*$', Comment)], 
       'keywords': [
                  (
                   '(access|action|alphtype)\\b', Keyword),
                  (
                   '(getkey|write|machine|include)\\b', Keyword),
                  (
                   '(any|ascii|extend|alpha|digit|alnum|lower|upper)\\b', Keyword),
                  (
                   '(xdigit|cntrl|graph|print|punct|space|zlen|empty)\\b', Keyword)], 
       'numbers': [
                 (
                  '0x[0-9A-Fa-f]+', Number.Hex),
                 (
                  '[+-]?[0-9]+', Number.Integer)], 
       'literals': [
                  (
                   '"(\\\\\\\\|\\\\"|[^"])*"', String),
                  (
                   "'(\\\\\\\\|\\\\'|[^'])*'", String),
                  (
                   '\\[(\\\\\\\\|\\\\\\]|[^\\]])*\\]', String),
                  (
                   '/(?!\\*)(\\\\\\\\|\\\\/|[^/])*/', String.Regex)], 
       'identifiers': [
                     (
                      '[a-zA-Z_][a-zA-Z_0-9]*', Name.Variable)], 
       'operators': [
                   (
                    ',', Operator),
                   (
                    '\\||&|-|--', Operator),
                   (
                    '\\.|<:|:>|:>>', Operator),
                   (
                    ':', Operator),
                   (
                    '->', Operator),
                   (
                    '(>|\\$|%|<|@|<>)(/|eof\\b)', Operator),
                   (
                    '(>|\\$|%|<|@|<>)(!|err\\b)', Operator),
                   (
                    '(>|\\$|%|<|@|<>)(\\^|lerr\\b)', Operator),
                   (
                    '(>|\\$|%|<|@|<>)(~|to\\b)', Operator),
                   (
                    '(>|\\$|%|<|@|<>)(\\*|from\\b)', Operator),
                   (
                    '>|@|\\$|%', Operator),
                   (
                    '\\*|\\?|\\+|{[0-9]*,[0-9]*}', Operator),
                   (
                    '!|\\^', Operator),
                   (
                    '\\(|\\)', Operator)], 
       'root': [
              include('literals'),
              include('whitespace'),
              include('comments'),
              include('keywords'),
              include('numbers'),
              include('identifiers'),
              include('operators'),
              (
               '{', Punctuation, 'host'),
              (
               '=', Operator),
              (
               ';', Punctuation)], 
       'host': [
              (
               '(' + ('|').join(('[^{}\\\'"/#]+', '[^\\\\][\\\\][{}]', '"(\\\\\\\\|\\\\"|[^"])*"',
                  "'(\\\\\\\\|\\\\'|[^'])*'", '//.*$\\n?', '/\\*(.|\\n)*?\\*/', '\\#.*$\\n?',
                  '/(?!\\*)(\\\\\\\\|\\\\/|[^/])*/', '/')) + ')+', Other),
              (
               '{', Punctuation, '#push'),
              (
               '}', Punctuation, '#pop')]}


class RagelEmbeddedLexer(RegexLexer):
    """
    A lexer for `Ragel`_ embedded in a host language file.

    This will only highlight Ragel statements. If you want host language
    highlighting then call the language-specific Ragel lexer.

    *New in Pygments 1.1.*
    """
    name = 'Embedded Ragel'
    aliases = ['ragel-em']
    filenames = ['*.rl']
    tokens = {'root': [
              (
               '(' + ('|').join(('[^%\\\'"/#]+', '%(?=[^%]|$)', '"(\\\\\\\\|\\\\"|[^"])*"', "'(\\\\\\\\|\\\\'|[^'])*'",
                  '/\\*(.|\\n)*?\\*/', '//.*$\\n?', '\\#.*$\\n?', '/(?!\\*)(\\\\\\\\|\\\\/|[^/])*/',
                  '/')) + ')+', Other),
              (
               '(%%)(?![{%])(.*)($|;)(\\n?)',
               bygroups(Punctuation, using(RagelLexer), Punctuation, Text)),
              (
               '(%%%%|%%){', Punctuation, 'multi-line-fsm')], 
       'multi-line-fsm': [
                        (
                         '(' + ('|').join(('(' + ('|').join(('[^}\\\'"\\[/#]', '}(?=[^%]|$)', '}%(?=[^%]|$)', '[^\\\\][\\\\][{}]',
                  '(>|\\$|%|<|@|<>)/', '/(?!\\*)(\\\\\\\\|\\\\/|[^/])*/\\*', '/(?=[^/\\*]|$)')) + ')+', '"(\\\\\\\\|\\\\"|[^"])*"', "'(\\\\\\\\|\\\\'|[^'])*'", '\\[(\\\\\\\\|\\\\\\]|[^\\]])*\\]', '/\\*(.|\\n)*?\\*/', '//.*$\\n?', '\\#.*$\\n?')) + ')+', using(RagelLexer)),
                        (
                         '}%%', Punctuation, '#pop')]}

    def analyse_text(text):
        return '@LANG: indep' in text or 0.1


class RagelRubyLexer(DelegatingLexer):
    """
    A lexer for `Ragel`_ in a Ruby host file.

    *New in Pygments 1.1.*
    """
    name = 'Ragel in Ruby Host'
    aliases = ['ragel-ruby', 'ragel-rb']
    filenames = ['*.rl']

    def __init__(self, **options):
        super(RagelRubyLexer, self).__init__(RubyLexer, RagelEmbeddedLexer, **options)

    def analyse_text(text):
        return '@LANG: ruby' in text


class RagelCLexer(DelegatingLexer):
    """
    A lexer for `Ragel`_ in a C host file.

    *New in Pygments 1.1.*
    """
    name = 'Ragel in C Host'
    aliases = ['ragel-c']
    filenames = ['*.rl']

    def __init__(self, **options):
        super(RagelCLexer, self).__init__(CLexer, RagelEmbeddedLexer, **options)

    def analyse_text(text):
        return '@LANG: c' in text


class RagelDLexer(DelegatingLexer):
    """
    A lexer for `Ragel`_ in a D host file.

    *New in Pygments 1.1.*
    """
    name = 'Ragel in D Host'
    aliases = ['ragel-d']
    filenames = ['*.rl']

    def __init__(self, **options):
        super(RagelDLexer, self).__init__(DLexer, RagelEmbeddedLexer, **options)

    def analyse_text(text):
        return '@LANG: d' in text


class RagelCppLexer(DelegatingLexer):
    """
    A lexer for `Ragel`_ in a CPP host file.

    *New in Pygments 1.1.*
    """
    name = 'Ragel in CPP Host'
    aliases = ['ragel-cpp']
    filenames = ['*.rl']

    def __init__(self, **options):
        super(RagelCppLexer, self).__init__(CppLexer, RagelEmbeddedLexer, **options)

    def analyse_text(text):
        return '@LANG: c++' in text


class RagelObjectiveCLexer(DelegatingLexer):
    """
    A lexer for `Ragel`_ in an Objective C host file.

    *New in Pygments 1.1.*
    """
    name = 'Ragel in Objective C Host'
    aliases = ['ragel-objc']
    filenames = ['*.rl']

    def __init__(self, **options):
        super(RagelObjectiveCLexer, self).__init__(ObjectiveCLexer, RagelEmbeddedLexer, **options)

    def analyse_text(text):
        return '@LANG: objc' in text


class RagelJavaLexer(DelegatingLexer):
    """
    A lexer for `Ragel`_ in a Java host file.

    *New in Pygments 1.1.*
    """
    name = 'Ragel in Java Host'
    aliases = ['ragel-java']
    filenames = ['*.rl']

    def __init__(self, **options):
        super(RagelJavaLexer, self).__init__(JavaLexer, RagelEmbeddedLexer, **options)

    def analyse_text(text):
        return '@LANG: java' in text


class AntlrLexer(RegexLexer):
    """
    Generic `ANTLR`_ Lexer.
    Should not be called directly, instead
    use DelegatingLexer for your target language.

    *New in Pygments 1.1.*

    .. _ANTLR: http://www.antlr.org/
    """
    name = 'ANTLR'
    aliases = ['antlr']
    filenames = []
    _id = '[A-Za-z][A-Za-z_0-9]*'
    _TOKEN_REF = '[A-Z][A-Za-z_0-9]*'
    _RULE_REF = '[a-z][A-Za-z_0-9]*'
    _STRING_LITERAL = "\\'(?:\\\\\\\\|\\\\\\'|[^\\']*)\\'"
    _INT = '[0-9]+'
    tokens = {'whitespace': [
                    (
                     '\\s+', Whitespace)], 
       'comments': [
                  (
                   '//.*$', Comment),
                  (
                   '/\\*(.|\\n)*?\\*/', Comment)], 
       'root': [
              include('whitespace'),
              include('comments'),
              (
               '(lexer|parser|tree)?(\\s*)(grammar\\b)(\\s*)(' + _id + ')(;)',
               bygroups(Keyword, Whitespace, Keyword, Whitespace, Name.Class, Punctuation)),
              (
               'options\\b', Keyword, 'options'),
              (
               'tokens\\b', Keyword, 'tokens'),
              (
               '(scope)(\\s*)(' + _id + ')(\\s*)({)',
               bygroups(Keyword, Whitespace, Name.Variable, Whitespace, Punctuation), 'action'),
              (
               '(catch|finally)\\b', Keyword, 'exception'),
              (
               '(@' + _id + ')(\\s*)(::)?(\\s*)(' + _id + ')(\\s*)({)',
               bygroups(Name.Label, Whitespace, Punctuation, Whitespace, Name.Label, Whitespace, Punctuation), 'action'),
              (
               '((?:protected|private|public|fragment)\\b)?(\\s*)(' + _id + ')(!)?',
               bygroups(Keyword, Whitespace, Name.Label, Punctuation),
               ('rule-alts', 'rule-prelims'))], 
       'exception': [
                   (
                    '\\n', Whitespace, '#pop'),
                   (
                    '\\s', Whitespace),
                   include('comments'),
                   (
                    '\\[', Punctuation, 'nested-arg-action'),
                   (
                    '\\{', Punctuation, 'action')], 
       'rule-prelims': [
                      include('whitespace'),
                      include('comments'),
                      (
                       'returns\\b', Keyword),
                      (
                       '\\[', Punctuation, 'nested-arg-action'),
                      (
                       '\\{', Punctuation, 'action'),
                      (
                       '(throws)(\\s+)(' + _id + ')',
                       bygroups(Keyword, Whitespace, Name.Label)),
                      (
                       '(?:(,)(\\s*)(' + _id + '))+',
                       bygroups(Punctuation, Whitespace, Name.Label)),
                      (
                       'options\\b', Keyword, 'options'),
                      (
                       '(scope)(\\s+)({)', bygroups(Keyword, Whitespace, Punctuation),
                       'action'),
                      (
                       '(scope)(\\s+)(' + _id + ')(\\s*)(;)',
                       bygroups(Keyword, Whitespace, Name.Label, Whitespace, Punctuation)),
                      (
                       '(@' + _id + ')(\\s*)({)',
                       bygroups(Name.Label, Whitespace, Punctuation), 'action'),
                      (
                       ':', Punctuation, '#pop')], 
       'rule-alts': [
                   include('whitespace'),
                   include('comments'),
                   (
                    'options\\b', Keyword, 'options'),
                   (
                    ':', Punctuation),
                   (
                    "'(\\\\\\\\|\\\\'|[^'])*'", String),
                   (
                    '"(\\\\\\\\|\\\\"|[^"])*"', String),
                   (
                    '<<([^>]|>[^>])>>', String),
                   (
                    '\\$?[A-Z_][A-Za-z_0-9]*', Name.Constant),
                   (
                    '\\$?[a-z_][A-Za-z_0-9]*', Name.Variable),
                   (
                    '(\\+|\\||->|=>|=|\\(|\\)|\\.\\.|\\.|\\?|\\*|\\^|!|\\#|~)', Operator),
                   (
                    ',', Punctuation),
                   (
                    '\\[', Punctuation, 'nested-arg-action'),
                   (
                    '\\{', Punctuation, 'action'),
                   (
                    ';', Punctuation, '#pop')], 
       'tokens': [
                include('whitespace'),
                include('comments'),
                (
                 '{', Punctuation),
                (
                 '(' + _TOKEN_REF + ')(\\s*)(=)?(\\s*)(' + _STRING_LITERAL + ')?(\\s*)(;)',
                 bygroups(Name.Label, Whitespace, Punctuation, Whitespace, String, Whitespace, Punctuation)),
                (
                 '}', Punctuation, '#pop')], 
       'options': [
                 include('whitespace'),
                 include('comments'),
                 (
                  '{', Punctuation),
                 (
                  '(' + _id + ')(\\s*)(=)(\\s*)(' + ('|').join((_id, _STRING_LITERAL, _INT, '\\*')) + ')(\\s*)(;)',
                  bygroups(Name.Variable, Whitespace, Punctuation, Whitespace, Text, Whitespace, Punctuation)),
                 (
                  '}', Punctuation, '#pop')], 
       'action': [
                (
                 '(' + ('|').join(('[^\\${}\\\'"/\\\\]+', '"(\\\\\\\\|\\\\"|[^"])*"', "'(\\\\\\\\|\\\\'|[^'])*'",
                  '//.*$\\n?', '/\\*(.|\\n)*?\\*/', '/(?!\\*)(\\\\\\\\|\\\\/|[^/])*/',
                  '\\\\(?!%)', '/')) + ')+', Other),
                (
                 '(\\\\)(%)', bygroups(Punctuation, Other)),
                (
                 '(\\$[a-zA-Z]+)(\\.?)(text|value)?',
                 bygroups(Name.Variable, Punctuation, Name.Property)),
                (
                 '{', Punctuation, '#push'),
                (
                 '}', Punctuation, '#pop')], 
       'nested-arg-action': [
                           (
                            '(' + ('|').join(('[^\\$\\[\\]\\\'"/]+', '"(\\\\\\\\|\\\\"|[^"])*"', "'(\\\\\\\\|\\\\'|[^'])*'",
                  '//.*$\\n?', '/\\*(.|\\n)*?\\*/', '/(?!\\*)(\\\\\\\\|\\\\/|[^/])*/',
                  '/')) + ')+', Other),
                           (
                            '\\[', Punctuation, '#push'),
                           (
                            '\\]', Punctuation, '#pop'),
                           (
                            '(\\$[a-zA-Z]+)(\\.?)(text|value)?',
                            bygroups(Name.Variable, Punctuation, Name.Property)),
                           (
                            '(\\\\\\\\|\\\\\\]|\\\\\\[|[^\\[\\]])+', Other)]}

    def analyse_text(text):
        return re.search('^\\s*grammar\\s+[a-zA-Z0-9]+\\s*;', text, re.M)


class AntlrCppLexer(DelegatingLexer):
    """
    `ANTLR`_ with CPP Target

    *New in Pygments 1.1.*
    """
    name = 'ANTLR With CPP Target'
    aliases = ['antlr-cpp']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        super(AntlrCppLexer, self).__init__(CppLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*C\\s*;', text, re.M)


class AntlrObjectiveCLexer(DelegatingLexer):
    """
    `ANTLR`_ with Objective-C Target

    *New in Pygments 1.1.*
    """
    name = 'ANTLR With ObjectiveC Target'
    aliases = ['antlr-objc']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        super(AntlrObjectiveCLexer, self).__init__(ObjectiveCLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*ObjC\\s*;', text)


class AntlrCSharpLexer(DelegatingLexer):
    """
    `ANTLR`_ with C# Target

    *New in Pygments 1.1.*
    """
    name = 'ANTLR With C# Target'
    aliases = ['antlr-csharp', 'antlr-c#']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        super(AntlrCSharpLexer, self).__init__(CSharpLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*CSharp2\\s*;', text, re.M)


class AntlrPythonLexer(DelegatingLexer):
    """
    `ANTLR`_ with Python Target

    *New in Pygments 1.1.*
    """
    name = 'ANTLR With Python Target'
    aliases = ['antlr-python']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        super(AntlrPythonLexer, self).__init__(PythonLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*Python\\s*;', text, re.M)


class AntlrJavaLexer(DelegatingLexer):
    """
    `ANTLR`_ with Java Target

    *New in Pygments 1.1*
    """
    name = 'ANTLR With Java Target'
    aliases = ['antlr-java']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        super(AntlrJavaLexer, self).__init__(JavaLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and 0.9


class AntlrRubyLexer(DelegatingLexer):
    """
    `ANTLR`_ with Ruby Target

    *New in Pygments 1.1.*
    """
    name = 'ANTLR With Ruby Target'
    aliases = ['antlr-ruby', 'antlr-rb']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        super(AntlrRubyLexer, self).__init__(RubyLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*Ruby\\s*;', text, re.M)


class AntlrPerlLexer(DelegatingLexer):
    """
    `ANTLR`_ with Perl Target

    *New in Pygments 1.1.*
    """
    name = 'ANTLR With Perl Target'
    aliases = ['antlr-perl']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        super(AntlrPerlLexer, self).__init__(PerlLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*Perl5\\s*;', text, re.M)


class AntlrActionScriptLexer(DelegatingLexer):
    """
    `ANTLR`_ with ActionScript Target

    *New in Pygments 1.1.*
    """
    name = 'ANTLR With ActionScript Target'
    aliases = ['antlr-as', 'antlr-actionscript']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        super(AntlrActionScriptLexer, self).__init__(ActionScriptLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*ActionScript\\s*;', text, re.M)