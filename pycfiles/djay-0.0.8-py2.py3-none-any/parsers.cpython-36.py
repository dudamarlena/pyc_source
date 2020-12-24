# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/parsers.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 27590 bytes
"""
    pygments.lexers.parsers
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for parser generators.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, DelegatingLexer, include, bygroups, using
from pygments.token import Punctuation, Other, Text, Comment, Operator, Keyword, Name, String, Number, Whitespace
from pygments.lexers.jvm import JavaLexer
from pygments.lexers.c_cpp import CLexer, CppLexer
from pygments.lexers.objective import ObjectiveCLexer
from pygments.lexers.d import DLexer
from pygments.lexers.dotnet import CSharpLexer
from pygments.lexers.ruby import RubyLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.perl import PerlLexer
__all__ = [
 'RagelLexer', 'RagelEmbeddedLexer', 'RagelCLexer', 'RagelDLexer',
 'RagelCppLexer', 'RagelObjectiveCLexer', 'RagelRubyLexer',
 'RagelJavaLexer', 'AntlrLexer', 'AntlrPythonLexer',
 'AntlrPerlLexer', 'AntlrRubyLexer', 'AntlrCppLexer',
 'AntlrCSharpLexer', 'AntlrObjectiveCLexer',
 'AntlrJavaLexer', 'AntlrActionScriptLexer',
 'TreetopLexer', 'EbnfLexer']

class RagelLexer(RegexLexer):
    __doc__ = '\n    A pure `Ragel <http://www.complang.org/ragel/>`_ lexer.  Use this for\n    fragments of Ragel.  For ``.rl`` files, use RagelEmbeddedLexer instead\n    (or one of the language-specific subclasses).\n\n    .. versionadded:: 1.1\n    '
    name = 'Ragel'
    aliases = ['ragel']
    filenames = []
    tokens = {'whitespace':[
      (
       '\\s+', Whitespace)], 
     'comments':[
      (
       '\\#.*$', Comment)], 
     'keywords':[
      (
       '(access|action|alphtype)\\b', Keyword),
      (
       '(getkey|write|machine|include)\\b', Keyword),
      (
       '(any|ascii|extend|alpha|digit|alnum|lower|upper)\\b', Keyword),
      (
       '(xdigit|cntrl|graph|print|punct|space|zlen|empty)\\b', Keyword)], 
     'numbers':[
      (
       '0x[0-9A-Fa-f]+', Number.Hex),
      (
       '[+-]?[0-9]+', Number.Integer)], 
     'literals':[
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       "'(\\\\\\\\|\\\\'|[^'])*'", String),
      (
       '\\[(\\\\\\\\|\\\\\\]|[^\\]])*\\]', String),
      (
       '/(?!\\*)(\\\\\\\\|\\\\/|[^/])*/', String.Regex)], 
     'identifiers':[
      (
       '[a-zA-Z_]\\w*', Name.Variable)], 
     'operators':[
      (
       ',', Operator),
      (
       '\\||&|--?', Operator),
      (
       '\\.|<:|:>>?', Operator),
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
       '\\*|\\?|\\+|\\{[0-9]*,[0-9]*\\}', Operator),
      (
       '!|\\^', Operator),
      (
       '\\(|\\)', Operator)], 
     'root':[
      include('literals'),
      include('whitespace'),
      include('comments'),
      include('keywords'),
      include('numbers'),
      include('identifiers'),
      include('operators'),
      (
       '\\{', Punctuation, 'host'),
      (
       '=', Operator),
      (
       ';', Punctuation)], 
     'host':[
      (
       '(' + '|'.join(('[^{}\\\'"/#]+', '[^\\\\]\\\\[{}]', '"(\\\\\\\\|\\\\"|[^"])*"', "'(\\\\\\\\|\\\\'|[^'])*'",
                '//.*$\\n?', '/\\*(.|\\n)*?\\*/', '\\#.*$\\n?', '/(?!\\*)(\\\\\\\\|\\\\/|[^/])*/',
                '/')) + ')+', Other),
      (
       '\\{', Punctuation, '#push'),
      (
       '\\}', Punctuation, '#pop')]}


class RagelEmbeddedLexer(RegexLexer):
    __doc__ = '\n    A lexer for `Ragel`_ embedded in a host language file.\n\n    This will only highlight Ragel statements. If you want host language\n    highlighting then call the language-specific Ragel lexer.\n\n    .. versionadded:: 1.1\n    '
    name = 'Embedded Ragel'
    aliases = ['ragel-em']
    filenames = ['*.rl']
    tokens = {'root':[
      (
       '(' + '|'.join(('[^%\\\'"/#]+', '%(?=[^%]|$)', '"(\\\\\\\\|\\\\"|[^"])*"', "'(\\\\\\\\|\\\\'|[^'])*'",
                '/\\*(.|\\n)*?\\*/', '//.*$\\n?', '\\#.*$\\n?', '/(?!\\*)(\\\\\\\\|\\\\/|[^/])*/',
                '/')) + ')+', Other),
      (
       '(%%)(?![{%])(.*)($|;)(\\n?)',
       bygroups(Punctuation, using(RagelLexer), Punctuation, Text)),
      (
       '(%%%%|%%)\\{', Punctuation, 'multi-line-fsm')], 
     'multi-line-fsm':[
      (
       '(' + '|'.join(('(' + '|'.join(('[^}\\\'"\\[/#]', '\\}(?=[^%]|$)', '\\}%(?=[^%]|$)', '[^\\\\]\\\\[{}]',
                '(>|\\$|%|<|@|<>)/', '/(?!\\*)(\\\\\\\\|\\\\/|[^/])*/\\*', '/(?=[^/*]|$)')) + ')+', '"(\\\\\\\\|\\\\"|[^"])*"', "'(\\\\\\\\|\\\\'|[^'])*'", '\\[(\\\\\\\\|\\\\\\]|[^\\]])*\\]', '/\\*(.|\\n)*?\\*/', '//.*$\\n?', '\\#.*$\\n?')) + ')+', using(RagelLexer)),
      (
       '\\}%%', Punctuation, '#pop')]}

    def analyse_text(text):
        return '@LANG: indep' in text


class RagelRubyLexer(DelegatingLexer):
    __doc__ = '\n    A lexer for `Ragel`_ in a Ruby host file.\n\n    .. versionadded:: 1.1\n    '
    name = 'Ragel in Ruby Host'
    aliases = ['ragel-ruby', 'ragel-rb']
    filenames = ['*.rl']

    def __init__(self, **options):
        (super(RagelRubyLexer, self).__init__)(RubyLexer, RagelEmbeddedLexer, **options)

    def analyse_text(text):
        return '@LANG: ruby' in text


class RagelCLexer(DelegatingLexer):
    __doc__ = '\n    A lexer for `Ragel`_ in a C host file.\n\n    .. versionadded:: 1.1\n    '
    name = 'Ragel in C Host'
    aliases = ['ragel-c']
    filenames = ['*.rl']

    def __init__(self, **options):
        (super(RagelCLexer, self).__init__)(CLexer, RagelEmbeddedLexer, **options)

    def analyse_text(text):
        return '@LANG: c' in text


class RagelDLexer(DelegatingLexer):
    __doc__ = '\n    A lexer for `Ragel`_ in a D host file.\n\n    .. versionadded:: 1.1\n    '
    name = 'Ragel in D Host'
    aliases = ['ragel-d']
    filenames = ['*.rl']

    def __init__(self, **options):
        (super(RagelDLexer, self).__init__)(DLexer, RagelEmbeddedLexer, **options)

    def analyse_text(text):
        return '@LANG: d' in text


class RagelCppLexer(DelegatingLexer):
    __doc__ = '\n    A lexer for `Ragel`_ in a CPP host file.\n\n    .. versionadded:: 1.1\n    '
    name = 'Ragel in CPP Host'
    aliases = ['ragel-cpp']
    filenames = ['*.rl']

    def __init__(self, **options):
        (super(RagelCppLexer, self).__init__)(CppLexer, RagelEmbeddedLexer, **options)

    def analyse_text(text):
        return '@LANG: c++' in text


class RagelObjectiveCLexer(DelegatingLexer):
    __doc__ = '\n    A lexer for `Ragel`_ in an Objective C host file.\n\n    .. versionadded:: 1.1\n    '
    name = 'Ragel in Objective C Host'
    aliases = ['ragel-objc']
    filenames = ['*.rl']

    def __init__(self, **options):
        (super(RagelObjectiveCLexer, self).__init__)(ObjectiveCLexer, 
         RagelEmbeddedLexer, **options)

    def analyse_text(text):
        return '@LANG: objc' in text


class RagelJavaLexer(DelegatingLexer):
    __doc__ = '\n    A lexer for `Ragel`_ in a Java host file.\n\n    .. versionadded:: 1.1\n    '
    name = 'Ragel in Java Host'
    aliases = ['ragel-java']
    filenames = ['*.rl']

    def __init__(self, **options):
        (super(RagelJavaLexer, self).__init__)(JavaLexer, RagelEmbeddedLexer, **options)

    def analyse_text(text):
        return '@LANG: java' in text


class AntlrLexer(RegexLexer):
    __doc__ = '\n    Generic `ANTLR`_ Lexer.\n    Should not be called directly, instead\n    use DelegatingLexer for your target language.\n\n    .. versionadded:: 1.1\n\n    .. _ANTLR: http://www.antlr.org/\n    '
    name = 'ANTLR'
    aliases = ['antlr']
    filenames = []
    _id = '[A-Za-z]\\w*'
    _TOKEN_REF = '[A-Z]\\w*'
    _RULE_REF = '[a-z]\\w*'
    _STRING_LITERAL = "\\'(?:\\\\\\\\|\\\\\\'|[^\\']*)\\'"
    _INT = '[0-9]+'
    tokens = {'whitespace':[
      (
       '\\s+', Whitespace)], 
     'comments':[
      (
       '//.*$', Comment),
      (
       '/\\*(.|\\n)*?\\*/', Comment)], 
     'root':[
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
       '(scope)(\\s*)(' + _id + ')(\\s*)(\\{)',
       bygroups(Keyword, Whitespace, Name.Variable, Whitespace, Punctuation), 'action'),
      (
       '(catch|finally)\\b', Keyword, 'exception'),
      (
       '(@' + _id + ')(\\s*)(::)?(\\s*)(' + _id + ')(\\s*)(\\{)',
       bygroups(Name.Label, Whitespace, Punctuation, Whitespace, Name.Label, Whitespace, Punctuation), 'action'),
      (
       '((?:protected|private|public|fragment)\\b)?(\\s*)(' + _id + ')(!)?',
       bygroups(Keyword, Whitespace, Name.Label, Punctuation),
       ('rule-alts', 'rule-prelims'))], 
     'exception':[
      (
       '\\n', Whitespace, '#pop'),
      (
       '\\s', Whitespace),
      include('comments'),
      (
       '\\[', Punctuation, 'nested-arg-action'),
      (
       '\\{', Punctuation, 'action')], 
     'rule-prelims':[
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
       '(,)(\\s*)(' + _id + ')',
       bygroups(Punctuation, Whitespace, Name.Label)),
      (
       'options\\b', Keyword, 'options'),
      (
       '(scope)(\\s+)(\\{)', bygroups(Keyword, Whitespace, Punctuation),
       'action'),
      (
       '(scope)(\\s+)(' + _id + ')(\\s*)(;)',
       bygroups(Keyword, Whitespace, Name.Label, Whitespace, Punctuation)),
      (
       '(@' + _id + ')(\\s*)(\\{)',
       bygroups(Name.Label, Whitespace, Punctuation), 'action'),
      (
       ':', Punctuation, '#pop')], 
     'rule-alts':[
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
       '\\$?[A-Z_]\\w*', Name.Constant),
      (
       '\\$?[a-z_]\\w*', Name.Variable),
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
     'tokens':[
      include('whitespace'),
      include('comments'),
      (
       '\\{', Punctuation),
      (
       '(' + _TOKEN_REF + ')(\\s*)(=)?(\\s*)(' + _STRING_LITERAL + ')?(\\s*)(;)',
       bygroups(Name.Label, Whitespace, Punctuation, Whitespace, String, Whitespace, Punctuation)),
      (
       '\\}', Punctuation, '#pop')], 
     'options':[
      include('whitespace'),
      include('comments'),
      (
       '\\{', Punctuation),
      (
       '(' + _id + ')(\\s*)(=)(\\s*)(' + '|'.join((_id, _STRING_LITERAL, _INT, '\\*')) + ')(\\s*)(;)',
       bygroups(Name.Variable, Whitespace, Punctuation, Whitespace, Text, Whitespace, Punctuation)),
      (
       '\\}', Punctuation, '#pop')], 
     'action':[
      (
       '(' + '|'.join(('[^${}\\\'"/\\\\]+', '"(\\\\\\\\|\\\\"|[^"])*"', "'(\\\\\\\\|\\\\'|[^'])*'",
                '//.*$\\n?', '/\\*(.|\\n)*?\\*/', '/(?!\\*)(\\\\\\\\|\\\\/|[^/])*/',
                '\\\\(?!%)', '/')) + ')+', Other),
      (
       '(\\\\)(%)', bygroups(Punctuation, Other)),
      (
       '(\\$[a-zA-Z]+)(\\.?)(text|value)?',
       bygroups(Name.Variable, Punctuation, Name.Property)),
      (
       '\\{', Punctuation, '#push'),
      (
       '\\}', Punctuation, '#pop')], 
     'nested-arg-action':[
      (
       '(' + '|'.join(('[^$\\[\\]\\\'"/]+', '"(\\\\\\\\|\\\\"|[^"])*"', "'(\\\\\\\\|\\\\'|[^'])*'",
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
    __doc__ = '\n    `ANTLR`_ with CPP Target\n\n    .. versionadded:: 1.1\n    '
    name = 'ANTLR With CPP Target'
    aliases = ['antlr-cpp']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        (super(AntlrCppLexer, self).__init__)(CppLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*C\\s*;', text, re.M)


class AntlrObjectiveCLexer(DelegatingLexer):
    __doc__ = '\n    `ANTLR`_ with Objective-C Target\n\n    .. versionadded:: 1.1\n    '
    name = 'ANTLR With ObjectiveC Target'
    aliases = ['antlr-objc']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        (super(AntlrObjectiveCLexer, self).__init__)(ObjectiveCLexer, 
         AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*ObjC\\s*;', text)


class AntlrCSharpLexer(DelegatingLexer):
    __doc__ = '\n    `ANTLR`_ with C# Target\n\n    .. versionadded:: 1.1\n    '
    name = 'ANTLR With C# Target'
    aliases = ['antlr-csharp', 'antlr-c#']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        (super(AntlrCSharpLexer, self).__init__)(CSharpLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*CSharp2\\s*;', text, re.M)


class AntlrPythonLexer(DelegatingLexer):
    __doc__ = '\n    `ANTLR`_ with Python Target\n\n    .. versionadded:: 1.1\n    '
    name = 'ANTLR With Python Target'
    aliases = ['antlr-python']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        (super(AntlrPythonLexer, self).__init__)(PythonLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*Python\\s*;', text, re.M)


class AntlrJavaLexer(DelegatingLexer):
    __doc__ = '\n    `ANTLR`_ with Java Target\n\n    .. versionadded:: 1.\n    '
    name = 'ANTLR With Java Target'
    aliases = ['antlr-java']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        (super(AntlrJavaLexer, self).__init__)(JavaLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and 0.9


class AntlrRubyLexer(DelegatingLexer):
    __doc__ = '\n    `ANTLR`_ with Ruby Target\n\n    .. versionadded:: 1.1\n    '
    name = 'ANTLR With Ruby Target'
    aliases = ['antlr-ruby', 'antlr-rb']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        (super(AntlrRubyLexer, self).__init__)(RubyLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*Ruby\\s*;', text, re.M)


class AntlrPerlLexer(DelegatingLexer):
    __doc__ = '\n    `ANTLR`_ with Perl Target\n\n    .. versionadded:: 1.1\n    '
    name = 'ANTLR With Perl Target'
    aliases = ['antlr-perl']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        (super(AntlrPerlLexer, self).__init__)(PerlLexer, AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*Perl5\\s*;', text, re.M)


class AntlrActionScriptLexer(DelegatingLexer):
    __doc__ = '\n    `ANTLR`_ with ActionScript Target\n\n    .. versionadded:: 1.1\n    '
    name = 'ANTLR With ActionScript Target'
    aliases = ['antlr-as', 'antlr-actionscript']
    filenames = ['*.G', '*.g']

    def __init__(self, **options):
        from pygments.lexers.actionscript import ActionScriptLexer
        (super(AntlrActionScriptLexer, self).__init__)(ActionScriptLexer, 
         AntlrLexer, **options)

    def analyse_text(text):
        return AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*ActionScript\\s*;', text, re.M)


class TreetopBaseLexer(RegexLexer):
    __doc__ = '\n    A base lexer for `Treetop <http://treetop.rubyforge.org/>`_ grammars.\n    Not for direct use; use TreetopLexer instead.\n\n    .. versionadded:: 1.6\n    '
    tokens = {'root':[
      include('space'),
      (
       'require[ \\t]+[^\\n\\r]+[\\n\\r]', Other),
      (
       'module\\b', Keyword.Namespace, 'module'),
      (
       'grammar\\b', Keyword, 'grammar')], 
     'module':[
      include('space'),
      include('end'),
      (
       'module\\b', Keyword, '#push'),
      (
       'grammar\\b', Keyword, 'grammar'),
      (
       '[A-Z]\\w*(?:::[A-Z]\\w*)*', Name.Namespace)], 
     'grammar':[
      include('space'),
      include('end'),
      (
       'rule\\b', Keyword, 'rule'),
      (
       'include\\b', Keyword, 'include'),
      (
       '[A-Z]\\w*', Name)], 
     'include':[
      include('space'),
      (
       '[A-Z]\\w*(?:::[A-Z]\\w*)*', Name.Class, '#pop')], 
     'rule':[
      include('space'),
      include('end'),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
      (
       "'(\\\\\\\\|\\\\'|[^'])*'", String.Single),
      (
       '([A-Za-z_]\\w*)(:)', bygroups(Name.Label, Punctuation)),
      (
       '[A-Za-z_]\\w*', Name),
      (
       '[()]', Punctuation),
      (
       '[?+*/&!~]', Operator),
      (
       '\\[(?:\\\\.|\\[:\\^?[a-z]+:\\]|[^\\\\\\]])+\\]', String.Regex),
      (
       '([0-9]*)(\\.\\.)([0-9]*)',
       bygroups(Number.Integer, Operator, Number.Integer)),
      (
       '(<)([^>]+)(>)', bygroups(Punctuation, Name.Class, Punctuation)),
      (
       '\\{', Punctuation, 'inline_module'),
      (
       '\\.', String.Regex)], 
     'inline_module':[
      (
       '\\{', Other, 'ruby'),
      (
       '\\}', Punctuation, '#pop'),
      (
       '[^{}]+', Other)], 
     'ruby':[
      (
       '\\{', Other, '#push'),
      (
       '\\}', Other, '#pop'),
      (
       '[^{}]+', Other)], 
     'space':[
      (
       '[ \\t\\n\\r]+', Whitespace),
      (
       '#[^\\n]*', Comment.Single)], 
     'end':[
      (
       'end\\b', Keyword, '#pop')]}


class TreetopLexer(DelegatingLexer):
    __doc__ = '\n    A lexer for `Treetop <http://treetop.rubyforge.org/>`_ grammars.\n\n    .. versionadded:: 1.6\n    '
    name = 'Treetop'
    aliases = ['treetop']
    filenames = ['*.treetop', '*.tt']

    def __init__(self, **options):
        (super(TreetopLexer, self).__init__)(RubyLexer, TreetopBaseLexer, **options)


class EbnfLexer(RegexLexer):
    __doc__ = '\n    Lexer for `ISO/IEC 14977 EBNF\n    <http://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_Form>`_\n    grammars.\n\n    .. versionadded:: 2.0\n    '
    name = 'EBNF'
    aliases = ['ebnf']
    filenames = ['*.ebnf']
    mimetypes = ['text/x-ebnf']
    tokens = {'root':[
      include('whitespace'),
      include('comment_start'),
      include('identifier'),
      (
       '=', Operator, 'production')], 
     'production':[
      include('whitespace'),
      include('comment_start'),
      include('identifier'),
      (
       '"[^"]*"', String.Double),
      (
       "'[^']*'", String.Single),
      (
       '(\\?[^?]*\\?)', Name.Entity),
      (
       '[\\[\\]{}(),|]', Punctuation),
      (
       '-', Operator),
      (
       ';', Punctuation, '#pop'),
      (
       '\\.', Punctuation, '#pop')], 
     'whitespace':[
      (
       '\\s+', Text)], 
     'comment_start':[
      (
       '\\(\\*', Comment.Multiline, 'comment')], 
     'comment':[
      (
       '[^*)]', Comment.Multiline),
      include('comment_start'),
      (
       '\\*\\)', Comment.Multiline, '#pop'),
      (
       '[*)]', Comment.Multiline)], 
     'identifier':[
      (
       '([a-zA-Z][\\w \\-]*)', Keyword)]}