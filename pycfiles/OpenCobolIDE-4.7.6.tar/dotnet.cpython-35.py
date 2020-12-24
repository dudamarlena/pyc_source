# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/dotnet.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 27321 bytes
"""
    pygments.lexers.dotnet
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for .net languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, DelegatingLexer, bygroups, include, using, this, default
from pygments.token import Punctuation, Text, Comment, Operator, Keyword, Name, String, Number, Literal, Other
from pygments.util import get_choice_opt, iteritems
from pygments import unistring as uni
from pygments.lexers.html import XmlLexer
__all__ = [
 'CSharpLexer', 'NemerleLexer', 'BooLexer', 'VbNetLexer',
 'CSharpAspxLexer', 'VbNetAspxLexer', 'FSharpLexer']

class CSharpLexer(RegexLexer):
    __doc__ = '\n    For `C# <http://msdn2.microsoft.com/en-us/vcsharp/default.aspx>`_\n    source code.\n\n    Additional options accepted:\n\n    `unicodelevel`\n      Determines which Unicode characters this lexer allows for identifiers.\n      The possible values are:\n\n      * ``none`` -- only the ASCII letters and numbers are allowed. This\n        is the fastest selection.\n      * ``basic`` -- all Unicode characters from the specification except\n        category ``Lo`` are allowed.\n      * ``full`` -- all Unicode characters as specified in the C# specs\n        are allowed.  Note that this means a considerable slowdown since the\n        ``Lo`` category has more than 40,000 characters in it!\n\n      The default value is ``basic``.\n\n      .. versionadded:: 0.8\n    '
    name = 'C#'
    aliases = ['csharp', 'c#']
    filenames = ['*.cs']
    mimetypes = ['text/x-csharp']
    flags = re.MULTILINE | re.DOTALL | re.UNICODE
    levels = {'none': '@?[_a-zA-Z]\\w*', 
     'basic': '@?[_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl') + ']' + '[' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*', 
     
     'full': '@?(?:_|[^' + uni.allexcept('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl') + '])' + '[^' + uni.allexcept('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*'}
    tokens = {}
    token_variants = True
    for levelname, cs_ident in iteritems(levels):
        tokens[levelname] = {'root': [
                  (
                   '^([ \\t]*(?:' + cs_ident + '(?:\\[\\])?\\s+)+?)(' + cs_ident + ')(\\s*)(\\()',
                   bygroups(using(this), Name.Function, Text, Punctuation)),
                  (
                   '^\\s*\\[.*?\\]', Name.Attribute),
                  (
                   '[^\\S\\n]+', Text),
                  (
                   '\\\\\\n', Text),
                  (
                   '//.*?\\n', Comment.Single),
                  (
                   '/[*].*?[*]/', Comment.Multiline),
                  (
                   '\\n', Text),
                  (
                   '[~!%^&*()+=|\\[\\]:;,.<>/?-]', Punctuation),
                  (
                   '[{}]', Punctuation),
                  (
                   '@"(""|[^"])*"', String),
                  (
                   '"(\\\\\\\\|\\\\"|[^"\\n])*["\\n]', String),
                  (
                   "'\\\\.'|'[^\\\\]'", String.Char),
                  (
                   '[0-9](\\.[0-9]*)?([eE][+-][0-9]+)?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?',
                   Number),
                  (
                   '#[ \\t]*(if|endif|else|elif|define|undef|line|error|warning|region|endregion|pragma)\\b.*?\\n',
                   Comment.Preproc),
                  (
                   '\\b(extern)(\\s+)(alias)\\b',
                   bygroups(Keyword, Text, Keyword)),
                  (
                   '(abstract|as|async|await|base|break|by|case|catch|checked|const|continue|default|delegate|do|else|enum|event|explicit|extern|false|finally|fixed|for|foreach|goto|if|implicit|in|interface|internal|is|let|lock|new|null|on|operator|out|override|params|private|protected|public|readonly|ref|return|sealed|sizeof|stackalloc|static|switch|this|throw|true|try|typeof|unchecked|unsafe|virtual|void|while|get|set|new|partial|yield|add|remove|value|alias|ascending|descending|from|group|into|orderby|select|thenby|where|join|equals)\\b',
                   Keyword),
                  (
                   '(global)(::)', bygroups(Keyword, Punctuation)),
                  (
                   '(bool|byte|char|decimal|double|dynamic|float|int|long|object|sbyte|short|string|uint|ulong|ushort|var)\\b\\??',
                   Keyword.Type),
                  (
                   '(class|struct)(\\s+)', bygroups(Keyword, Text), 'class'),
                  (
                   '(namespace|using)(\\s+)', bygroups(Keyword, Text), 'namespace'),
                  (
                   cs_ident, Name)], 
         
         'class': [
                   (
                    cs_ident, Name.Class, '#pop'),
                   default('#pop')], 
         
         'namespace': [
                       (
                        '(?=\\()', Text, '#pop'),
                       (
                        '(' + cs_ident + '|\\.)+', Name.Namespace, '#pop')]}

    def __init__(self, **options):
        level = get_choice_opt(options, 'unicodelevel', list(self.tokens), 'basic')
        if level not in self._all_tokens:
            self._tokens = self.__class__.process_tokendef(level)
        else:
            self._tokens = self._all_tokens[level]
        RegexLexer.__init__(self, **options)


class NemerleLexer(RegexLexer):
    __doc__ = '\n    For `Nemerle <http://nemerle.org>`_ source code.\n\n    Additional options accepted:\n\n    `unicodelevel`\n      Determines which Unicode characters this lexer allows for identifiers.\n      The possible values are:\n\n      * ``none`` -- only the ASCII letters and numbers are allowed. This\n        is the fastest selection.\n      * ``basic`` -- all Unicode characters from the specification except\n        category ``Lo`` are allowed.\n      * ``full`` -- all Unicode characters as specified in the C# specs\n        are allowed.  Note that this means a considerable slowdown since the\n        ``Lo`` category has more than 40,000 characters in it!\n\n      The default value is ``basic``.\n\n    .. versionadded:: 1.5\n    '
    name = 'Nemerle'
    aliases = ['nemerle']
    filenames = ['*.n']
    mimetypes = ['text/x-nemerle']
    flags = re.MULTILINE | re.DOTALL | re.UNICODE
    levels = {'none': '@?[_a-zA-Z]\\w*', 
     'basic': '@?[_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl') + ']' + '[' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*', 
     
     'full': '@?(?:_|[^' + uni.allexcept('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl') + '])' + '[^' + uni.allexcept('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*'}
    tokens = {}
    token_variants = True
    for levelname, cs_ident in iteritems(levels):
        tokens[levelname] = {'root': [
                  (
                   '^([ \\t]*(?:' + cs_ident + '(?:\\[\\])?\\s+)+?)(' + cs_ident + ')(\\s*)(\\()',
                   bygroups(using(this), Name.Function, Text, Punctuation)),
                  (
                   '^\\s*\\[.*?\\]', Name.Attribute),
                  (
                   '[^\\S\\n]+', Text),
                  (
                   '\\\\\\n', Text),
                  (
                   '//.*?\\n', Comment.Single),
                  (
                   '/[*].*?[*]/', Comment.Multiline),
                  (
                   '\\n', Text),
                  (
                   '\\$\\s*"', String, 'splice-string'),
                  (
                   '\\$\\s*<#', String, 'splice-string2'),
                  (
                   '<#', String, 'recursive-string'),
                  (
                   '(<\\[)\\s*(' + cs_ident + ':)?', Keyword),
                  (
                   '\\]\\>', Keyword),
                  (
                   '\\$' + cs_ident, Name),
                  (
                   '(\\$)(\\()', bygroups(Name, Punctuation),
                   'splice-string-content'),
                  (
                   '[~!%^&*()+=|\\[\\]:;,.<>/?-]', Punctuation),
                  (
                   '[{}]', Punctuation),
                  (
                   '@"(""|[^"])*"', String),
                  (
                   '"(\\\\\\\\|\\\\"|[^"\\n])*["\\n]', String),
                  (
                   "'\\\\.'|'[^\\\\]'", String.Char),
                  (
                   '0[xX][0-9a-fA-F]+[Ll]?', Number),
                  (
                   '[0-9](\\.[0-9]*)?([eE][+-][0-9]+)?[flFLdD]?', Number),
                  (
                   '#[ \\t]*(if|endif|else|elif|define|undef|line|error|warning|region|endregion|pragma)\\b.*?\\n',
                   Comment.Preproc),
                  (
                   '\\b(extern)(\\s+)(alias)\\b',
                   bygroups(Keyword, Text, Keyword)),
                  (
                   '(abstract|and|as|base|catch|def|delegate|enum|event|extern|false|finally|fun|implements|interface|internal|is|macro|match|matches|module|mutable|new|null|out|override|params|partial|private|protected|public|ref|sealed|static|syntax|this|throw|true|try|type|typeof|virtual|volatile|when|where|with|assert|assert2|async|break|checked|continue|do|else|ensures|for|foreach|if|late|lock|new|nolate|otherwise|regexp|repeat|requires|return|surroundwith|unchecked|unless|using|while|yield)\\b',
                   Keyword),
                  (
                   '(global)(::)', bygroups(Keyword, Punctuation)),
                  (
                   '(bool|byte|char|decimal|double|float|int|long|object|sbyte|short|string|uint|ulong|ushort|void|array|list)\\b\\??',
                   Keyword.Type),
                  (
                   '(:>?)\\s*(' + cs_ident + '\\??)',
                   bygroups(Punctuation, Keyword.Type)),
                  (
                   '(class|struct|variant|module)(\\s+)',
                   bygroups(Keyword, Text), 'class'),
                  (
                   '(namespace|using)(\\s+)', bygroups(Keyword, Text),
                   'namespace'),
                  (
                   cs_ident, Name)], 
         
         'class': [
                   (
                    cs_ident, Name.Class, '#pop')], 
         
         'namespace': [
                       (
                        '(?=\\()', Text, '#pop'),
                       (
                        '(' + cs_ident + '|\\.)+', Name.Namespace, '#pop')], 
         
         'splice-string': [
                           (
                            '[^"$]', String),
                           (
                            '\\$' + cs_ident, Name),
                           (
                            '(\\$)(\\()', bygroups(Name, Punctuation),
                            'splice-string-content'),
                           (
                            '\\\\"', String),
                           (
                            '"', String, '#pop')], 
         
         'splice-string2': [
                            (
                             '[^#<>$]', String),
                            (
                             '\\$' + cs_ident, Name),
                            (
                             '(\\$)(\\()', bygroups(Name, Punctuation),
                             'splice-string-content'),
                            (
                             '<#', String, '#push'),
                            (
                             '#>', String, '#pop')], 
         
         'recursive-string': [
                              (
                               '[^#<>]', String),
                              (
                               '<#', String, '#push'),
                              (
                               '#>', String, '#pop')], 
         
         'splice-string-content': [
                                   (
                                    'if|match', Keyword),
                                   (
                                    '[~!%^&*+=|\\[\\]:;,.<>/?-\\\\"$ ]', Punctuation),
                                   (
                                    cs_ident, Name),
                                   (
                                    '\\d+', Number),
                                   (
                                    '\\(', Punctuation, '#push'),
                                   (
                                    '\\)', Punctuation, '#pop')]}

    def __init__(self, **options):
        level = get_choice_opt(options, 'unicodelevel', list(self.tokens), 'basic')
        if level not in self._all_tokens:
            self._tokens = self.__class__.process_tokendef(level)
        else:
            self._tokens = self._all_tokens[level]
        RegexLexer.__init__(self, **options)


class BooLexer(RegexLexer):
    __doc__ = '\n    For `Boo <http://boo.codehaus.org/>`_ source code.\n    '
    name = 'Boo'
    aliases = ['boo']
    filenames = ['*.boo']
    mimetypes = ['text/x-boo']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '(#|//).*$', Comment.Single),
              (
               '/[*]', Comment.Multiline, 'comment'),
              (
               '[]{}:(),.;[]', Punctuation),
              (
               '\\\\\\n', Text),
              (
               '\\\\', Text),
              (
               '(in|is|and|or|not)\\b', Operator.Word),
              (
               '/(\\\\\\\\|\\\\/|[^/\\s])/', String.Regex),
              (
               '@/(\\\\\\\\|\\\\/|[^/])*/', String.Regex),
              (
               '=~|!=|==|<<|>>|[-+/*%=<>&^|]', Operator),
              (
               '(as|abstract|callable|constructor|destructor|do|import|enum|event|final|get|interface|internal|of|override|partial|private|protected|public|return|set|static|struct|transient|virtual|yield|super|and|break|cast|continue|elif|else|ensure|except|for|given|goto|if|in|is|isa|not|or|otherwise|pass|raise|ref|try|unless|when|while|from|as)\\b',
               Keyword),
              (
               'def(?=\\s+\\(.*?\\))', Keyword),
              (
               '(def)(\\s+)', bygroups(Keyword, Text), 'funcname'),
              (
               '(class)(\\s+)', bygroups(Keyword, Text), 'classname'),
              (
               '(namespace)(\\s+)', bygroups(Keyword, Text), 'namespace'),
              (
               '(?<!\\.)(true|false|null|self|__eval__|__switch__|array|assert|checked|enumerate|filter|getter|len|lock|map|matrix|max|min|normalArrayIndexing|print|property|range|rawArrayIndexing|required|typeof|unchecked|using|yieldAll|zip)\\b',
               Name.Builtin),
              (
               '"""(\\\\\\\\|\\\\"|.*?)"""', String.Double),
              (
               '"(\\\\\\\\|\\\\"|[^"]*?)"', String.Double),
              (
               "'(\\\\\\\\|\\\\'|[^']*?)'", String.Single),
              (
               '[a-zA-Z_]\\w*', Name),
              (
               '(\\d+\\.\\d*|\\d*\\.\\d+)([fF][+-]?[0-9]+)?', Number.Float),
              (
               '[0-9][0-9.]*(ms?|d|h|s)', Number),
              (
               '0\\d+', Number.Oct),
              (
               '0x[a-fA-F0-9]+', Number.Hex),
              (
               '\\d+L', Number.Integer.Long),
              (
               '\\d+', Number.Integer)], 
     
     'comment': [
                 (
                  '/[*]', Comment.Multiline, '#push'),
                 (
                  '[*]/', Comment.Multiline, '#pop'),
                 (
                  '[^/*]', Comment.Multiline),
                 (
                  '[*/]', Comment.Multiline)], 
     
     'funcname': [
                  (
                   '[a-zA-Z_]\\w*', Name.Function, '#pop')], 
     
     'classname': [
                   (
                    '[a-zA-Z_]\\w*', Name.Class, '#pop')], 
     
     'namespace': [
                   (
                    '[a-zA-Z_][\\w.]*', Name.Namespace, '#pop')]}


class VbNetLexer(RegexLexer):
    __doc__ = '\n    For\n    `Visual Basic.NET <http://msdn2.microsoft.com/en-us/vbasic/default.aspx>`_\n    source code.\n    '
    name = 'VB.net'
    aliases = ['vb.net', 'vbnet']
    filenames = ['*.vb', '*.bas']
    mimetypes = ['text/x-vbnet', 'text/x-vba']
    uni_name = '[_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl') + ']' + '[' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*'
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [
              (
               '^\\s*<.*?>', Name.Attribute),
              (
               '\\s+', Text),
              (
               '\\n', Text),
              (
               'rem\\b.*?\\n', Comment),
              (
               "'.*?\\n", Comment),
              (
               '#If\\s.*?\\sThen|#ElseIf\\s.*?\\sThen|#Else|#End\\s+If|#Const|#ExternalSource.*?\\n|#End\\s+ExternalSource|#Region.*?\\n|#End\\s+Region|#ExternalChecksum',
               Comment.Preproc),
              (
               '[(){}!#,.:]', Punctuation),
              (
               'Option\\s+(Strict|Explicit|Compare)\\s+(On|Off|Binary|Text)',
               Keyword.Declaration),
              (
               '(?<!\\.)(AddHandler|Alias|ByRef|ByVal|Call|Case|Catch|CBool|CByte|CChar|CDate|CDec|CDbl|CInt|CLng|CObj|Continue|CSByte|CShort|CSng|CStr|CType|CUInt|CULng|CUShort|Declare|Default|Delegate|DirectCast|Do|Each|Else|ElseIf|EndIf|Erase|Error|Event|Exit|False|Finally|For|Friend|Get|Global|GoSub|GoTo|Handles|If|Implements|Inherits|Interface|Let|Lib|Loop|Me|MustInherit|MustOverride|MyBase|MyClass|Narrowing|New|Next|Not|Nothing|NotInheritable|NotOverridable|Of|On|Operator|Option|Optional|Overloads|Overridable|Overrides|ParamArray|Partial|Private|Protected|Public|RaiseEvent|ReadOnly|ReDim|RemoveHandler|Resume|Return|Select|Set|Shadows|Shared|Single|Static|Step|Stop|SyncLock|Then|Throw|To|True|Try|TryCast|Wend|Using|When|While|Widening|With|WithEvents|WriteOnly)\\b',
               Keyword),
              (
               '(?<!\\.)End\\b', Keyword, 'end'),
              (
               '(?<!\\.)(Dim|Const)\\b', Keyword, 'dim'),
              (
               '(?<!\\.)(Function|Sub|Property)(\\s+)',
               bygroups(Keyword, Text), 'funcname'),
              (
               '(?<!\\.)(Class|Structure|Enum)(\\s+)',
               bygroups(Keyword, Text), 'classname'),
              (
               '(?<!\\.)(Module|Namespace|Imports)(\\s+)',
               bygroups(Keyword, Text), 'namespace'),
              (
               '(?<!\\.)(Boolean|Byte|Char|Date|Decimal|Double|Integer|Long|Object|SByte|Short|Single|String|Variant|UInteger|ULong|UShort)\\b',
               Keyword.Type),
              (
               '(?<!\\.)(AddressOf|And|AndAlso|As|GetType|In|Is|IsNot|Like|Mod|Or|OrElse|TypeOf|Xor)\\b',
               Operator.Word),
              (
               '&=|[*]=|/=|\\\\=|\\^=|\\+=|-=|<<=|>>=|<<|>>|:=|<=|>=|<>|[-&*/\\\\^+=<>\\[\\]]',
               Operator),
              (
               '"', String, 'string'),
              (
               '_\\n', Text),
              (
               uni_name + '[%&@!#$]?', Name),
              (
               '#.*?#', Literal.Date),
              (
               '(\\d+\\.\\d*|\\d*\\.\\d+)(F[+-]?[0-9]+)?', Number.Float),
              (
               '\\d+([SILDFR]|US|UI|UL)?', Number.Integer),
              (
               '&H[0-9a-f]+([SILDFR]|US|UI|UL)?', Number.Integer),
              (
               '&O[0-7]+([SILDFR]|US|UI|UL)?', Number.Integer)], 
     
     'string': [
                (
                 '""', String),
                (
                 '"C?', String, '#pop'),
                (
                 '[^"]+', String)], 
     
     'dim': [
             (
              uni_name, Name.Variable, '#pop'),
             default('#pop')], 
     
     'funcname': [
                  (
                   uni_name, Name.Function, '#pop')], 
     
     'classname': [
                   (
                    uni_name, Name.Class, '#pop')], 
     
     'namespace': [
                   (
                    uni_name, Name.Namespace),
                   (
                    '\\.', Name.Namespace),
                   default('#pop')], 
     
     'end': [
             (
              '\\s+', Text),
             (
              '(Function|Sub|Property|Class|Structure|Enum|Module|Namespace)\\b',
              Keyword, '#pop'),
             default('#pop')]}

    def analyse_text(text):
        if re.search('^\\s*(#If|Module|Namespace)', text, re.MULTILINE):
            return 0.5


class GenericAspxLexer(RegexLexer):
    __doc__ = '\n    Lexer for ASP.NET pages.\n    '
    name = 'aspx-gen'
    filenames = []
    mimetypes = []
    flags = re.DOTALL
    tokens = {'root': [
              (
               '(<%[@=#]?)(.*?)(%>)', bygroups(Name.Tag, Other, Name.Tag)),
              (
               '(<script.*?>)(.*?)(</script>)',
               bygroups(using(XmlLexer), Other, using(XmlLexer))),
              (
               '(.+?)(?=<)', using(XmlLexer)),
              (
               '.+', using(XmlLexer))]}


class CSharpAspxLexer(DelegatingLexer):
    __doc__ = '\n    Lexer for highlighting C# within ASP.NET pages.\n    '
    name = 'aspx-cs'
    aliases = ['aspx-cs']
    filenames = ['*.aspx', '*.asax', '*.ascx', '*.ashx', '*.asmx', '*.axd']
    mimetypes = []

    def __init__(self, **options):
        super(CSharpAspxLexer, self).__init__(CSharpLexer, GenericAspxLexer, **options)

    def analyse_text(text):
        if re.search('Page\\s*Language="C#"', text, re.I) is not None:
            return 0.2
        if re.search('script[^>]+language=["\\\']C#', text, re.I) is not None:
            return 0.15


class VbNetAspxLexer(DelegatingLexer):
    __doc__ = '\n    Lexer for highlighting Visual Basic.net within ASP.NET pages.\n    '
    name = 'aspx-vb'
    aliases = ['aspx-vb']
    filenames = ['*.aspx', '*.asax', '*.ascx', '*.ashx', '*.asmx', '*.axd']
    mimetypes = []

    def __init__(self, **options):
        super(VbNetAspxLexer, self).__init__(VbNetLexer, GenericAspxLexer, **options)

    def analyse_text(text):
        if re.search('Page\\s*Language="Vb"', text, re.I) is not None:
            return 0.2
        if re.search('script[^>]+language=["\\\']vb', text, re.I) is not None:
            return 0.15


class FSharpLexer(RegexLexer):
    __doc__ = '\n    For the F# language (version 3.0).\n\n    AAAAACK Strings\n    http://research.microsoft.com/en-us/um/cambridge/projects/fsharp/manual/spec.html#_Toc335818775\n\n    .. versionadded:: 1.5\n    '
    name = 'FSharp'
    aliases = ['fsharp']
    filenames = ['*.fs', '*.fsi']
    mimetypes = ['text/x-fsharp']
    keywords = [
     'abstract', 'as', 'assert', 'base', 'begin', 'class', 'default',
     'delegate', 'do!', 'do', 'done', 'downcast', 'downto', 'elif', 'else',
     'end', 'exception', 'extern', 'false', 'finally', 'for', 'function',
     'fun', 'global', 'if', 'inherit', 'inline', 'interface', 'internal',
     'in', 'lazy', 'let!', 'let', 'match', 'member', 'module', 'mutable',
     'namespace', 'new', 'null', 'of', 'open', 'override', 'private', 'public',
     'rec', 'return!', 'return', 'select', 'static', 'struct', 'then', 'to',
     'true', 'try', 'type', 'upcast', 'use!', 'use', 'val', 'void', 'when',
     'while', 'with', 'yield!', 'yield']
    keywords += [
     'atomic', 'break', 'checked', 'component', 'const', 'constraint',
     'constructor', 'continue', 'eager', 'event', 'external', 'fixed',
     'functor', 'include', 'method', 'mixin', 'object', 'parallel',
     'process', 'protected', 'pure', 'sealed', 'tailcall', 'trait',
     'virtual', 'volatile']
    keyopts = [
     '!=', '#', '&&', '&', '\\(', '\\)', '\\*', '\\+', ',', '-\\.',
     '->', '-', '\\.\\.', '\\.', '::', ':=', ':>', ':', ';;', ';', '<-',
     '<\\]', '<', '>\\]', '>', '\\?\\?', '\\?', '\\[<', '\\[\\|', '\\[', '\\]',
     '_', '`', '\\{', '\\|\\]', '\\|', '\\}', '~', '<@@', '<@', '=', '@>', '@@>']
    operators = '[!$%&*+\\./:<=>?@^|~-]'
    word_operators = ['and', 'or', 'not']
    prefix_syms = '[!?~]'
    infix_syms = '[=<>@^|&+\\*/$%-]'
    primitives = [
     'sbyte', 'byte', 'char', 'nativeint', 'unativeint', 'float32', 'single',
     'float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32',
     'uint32', 'int64', 'uint64', 'decimal', 'unit', 'bool', 'string',
     'list', 'exn', 'obj', 'enum']
    tokens = {'escape-sequence': [
                         (
                          '\\\\[\\\\"\\\'ntbrafv]', String.Escape),
                         (
                          '\\\\[0-9]{3}', String.Escape),
                         (
                          '\\\\u[0-9a-fA-F]{4}', String.Escape),
                         (
                          '\\\\U[0-9a-fA-F]{8}', String.Escape)], 
     
     'root': [
              (
               '\\s+', Text),
              (
               '\\(\\)|\\[\\]', Name.Builtin.Pseudo),
              (
               "\\b(?<!\\.)([A-Z][\\w\\']*)(?=\\s*\\.)",
               Name.Namespace, 'dotted'),
              (
               "\\b([A-Z][\\w\\']*)", Name),
              (
               '///.*?\\n', String.Doc),
              (
               '//.*?\\n', Comment.Single),
              (
               '\\(\\*(?!\\))', Comment, 'comment'),
              (
               '@"', String, 'lstring'),
              (
               '"""', String, 'tqs'),
              (
               '"', String, 'string'),
              (
               '\\b(open|module)(\\s+)([\\w.]+)',
               bygroups(Keyword, Text, Name.Namespace)),
              (
               '\\b(let!?)(\\s+)(\\w+)',
               bygroups(Keyword, Text, Name.Variable)),
              (
               '\\b(type)(\\s+)(\\w+)',
               bygroups(Keyword, Text, Name.Class)),
              (
               '\\b(member|override)(\\s+)(\\w+)(\\.)(\\w+)',
               bygroups(Keyword, Text, Name, Punctuation, Name.Function)),
              (
               '\\b(%s)\\b' % '|'.join(keywords), Keyword),
              (
               '``([^`\\n\\r\\t]|`[^`\\n\\r\\t])+``', Name),
              (
               '(%s)' % '|'.join(keyopts), Operator),
              (
               '(%s|%s)?%s' % (infix_syms, prefix_syms, operators), Operator),
              (
               '\\b(%s)\\b' % '|'.join(word_operators), Operator.Word),
              (
               '\\b(%s)\\b' % '|'.join(primitives), Keyword.Type),
              (
               '#[ \\t]*(if|endif|else|line|nowarn|light|\\d+)\\b.*?\\n',
               Comment.Preproc),
              (
               "[^\\W\\d][\\w']*", Name),
              (
               '\\d[\\d_]*[uU]?[yslLnQRZINGmM]?', Number.Integer),
              (
               '0[xX][\\da-fA-F][\\da-fA-F_]*[uU]?[yslLn]?[fF]?', Number.Hex),
              (
               '0[oO][0-7][0-7_]*[uU]?[yslLn]?', Number.Oct),
              (
               '0[bB][01][01_]*[uU]?[yslLn]?', Number.Bin),
              (
               '-?\\d[\\d_]*(.[\\d_]*)?([eE][+\\-]?\\d[\\d_]*)[fFmM]?',
               Number.Float),
              (
               '\'(?:(\\\\[\\\\\\"\'ntbr ])|(\\\\[0-9]{3})|(\\\\x[0-9a-fA-F]{2}))\'B?',
               String.Char),
              (
               "'.'", String.Char),
              (
               "'", Keyword),
              (
               '@?"', String.Double, 'string'),
              (
               "[~?][a-z][\\w\\']*:", Name.Variable)], 
     
     'dotted': [
                (
                 '\\s+', Text),
                (
                 '\\.', Punctuation),
                (
                 "[A-Z][\\w\\']*(?=\\s*\\.)", Name.Namespace),
                (
                 "[A-Z][\\w\\']*", Name, '#pop'),
                (
                 "[a-z_][\\w\\']*", Name, '#pop'),
                default('#pop')], 
     
     'comment': [
                 (
                  '[^(*)@"]+', Comment),
                 (
                  '\\(\\*', Comment, '#push'),
                 (
                  '\\*\\)', Comment, '#pop'),
                 (
                  '@"', String, 'lstring'),
                 (
                  '"""', String, 'tqs'),
                 (
                  '"', String, 'string'),
                 (
                  '[(*)@]', Comment)], 
     
     'string': [
                (
                 '[^\\\\"]+', String),
                include('escape-sequence'),
                (
                 '\\\\\\n', String),
                (
                 '\\n', String),
                (
                 '"B?', String, '#pop')], 
     
     'lstring': [
                 (
                  '[^"]+', String),
                 (
                  '\\n', String),
                 (
                  '""', String),
                 (
                  '"B?', String, '#pop')], 
     
     'tqs': [
             (
              '[^"]+', String),
             (
              '\\n', String),
             (
              '"""B?', String, '#pop'),
             (
              '"', String)]}