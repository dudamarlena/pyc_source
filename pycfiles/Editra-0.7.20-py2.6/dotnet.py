# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/lexers/dotnet.py
# Compiled at: 2011-04-22 17:53:26
"""
    pygments.lexers.dotnet
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for .net languages.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, DelegatingLexer, bygroups, using, this
from pygments.token import Punctuation, Text, Comment, Operator, Keyword, Name, String, Number, Literal, Other
from pygments.util import get_choice_opt
from pygments import unistring as uni
from pygments.lexers.web import XmlLexer
__all__ = [
 'CSharpLexer', 'BooLexer', 'VbNetLexer', 'CSharpAspxLexer',
 'VbNetAspxLexer']

def _escape(st):
    return st.replace('\\', '\\\\').replace('-', '\\-').replace('[', '\\[').replace(']', '\\]')


class CSharpLexer(RegexLexer):
    """
    For `C# <http://msdn2.microsoft.com/en-us/vcsharp/default.aspx>`_
    source code.

    Additional options accepted:

    `unicodelevel`
      Determines which Unicode characters this lexer allows for identifiers.
      The possible values are:

      * ``none`` -- only the ASCII letters and numbers are allowed. This
        is the fastest selection.
      * ``basic`` -- all Unicode characters from the specification except
        category ``Lo`` are allowed.
      * ``full`` -- all Unicode characters as specified in the C# specs
        are allowed.  Note that this means a considerable slowdown since the
        ``Lo`` category has more than 40,000 characters in it!

      The default value is ``basic``.

      *New in Pygments 0.8.*
    """
    name = 'C#'
    aliases = ['csharp', 'c#']
    filenames = ['*.cs']
    mimetypes = ['text/x-csharp']
    flags = re.MULTILINE | re.DOTALL | re.UNICODE
    levels = {'none': '@?[_a-zA-Z][a-zA-Z0-9_]*', 
       'basic': '@?[_' + uni.Lu + uni.Ll + uni.Lt + uni.Lm + uni.Nl + ']' + '[' + uni.Lu + uni.Ll + uni.Lt + uni.Lm + uni.Nl + uni.Nd + uni.Pc + uni.Cf + uni.Mn + uni.Mc + ']*', 
       'full': '@?(?:_|[^' + _escape(uni.allexcept('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl')) + '])' + '[^' + _escape(uni.allexcept('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc')) + ']*'}
    tokens = {}
    token_variants = True
    for (levelname, cs_ident) in levels.items():
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
                   '/[*](.|\\n)*?[*]/', Comment.Multiline),
                  (
                   '\\n', Text),
                  (
                   '[~!%^&*()+=|\\[\\]:;,.<>/?-]', Punctuation),
                  (
                   '[{}]', Punctuation),
                  (
                   '@"(\\\\\\\\|\\\\"|[^"])*"', String),
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
                   '(abstract|as|base|break|case|catch|checked|const|continue|default|delegate|do|else|enum|event|explicit|extern|false|finally|fixed|for|foreach|goto|if|implicit|in|interface|internal|is|lock|new|null|operator|out|override|params|private|protected|public|readonly|ref|return|sealed|sizeof|stackalloc|static|switch|this|throw|true|try|typeof|unchecked|unsafe|virtual|void|while|get|set|new|partial|yield|add|remove|value)\\b',
                   Keyword),
                  (
                   '(global)(::)', bygroups(Keyword, Punctuation)),
                  (
                   '(bool|byte|char|decimal|double|float|int|long|object|sbyte|short|string|uint|ulong|ushort)\\b\\??',
                   Keyword.Type),
                  (
                   '(class|struct)(\\s+)', bygroups(Keyword, Text), 'class'),
                  (
                   '(namespace|using)(\\s+)', bygroups(Keyword, Text), 'namespace'),
                  (
                   cs_ident, Name)], 
           'class': [
                   (
                    cs_ident, Name.Class, '#pop')], 
           'namespace': [
                       (
                        '(?=\\()', Text, '#pop'),
                       (
                        '(' + cs_ident + '|\\.)+', Name.Namespace, '#pop')]}

    def __init__(self, **options):
        level = get_choice_opt(options, 'unicodelevel', self.tokens.keys(), 'basic')
        if level not in self._all_tokens:
            self._tokens = self.__class__.process_tokendef(level)
        else:
            self._tokens = self._all_tokens[level]
        RegexLexer.__init__(self, **options)


class BooLexer(RegexLexer):
    """
    For `Boo <http://boo.codehaus.org/>`_ source code.
    """
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
               '"""(\\\\|\\"|.*?)"""', String.Double),
              (
               '"(\\\\|\\"|[^"]*?)"', String.Double),
              (
               "'(\\\\|\\'|[^']*?)'", String.Single),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*', Name),
              (
               '(\\d+\\.\\d*|\\d*\\.\\d+)([fF][+-]?[0-9]+)?', Number.Float),
              (
               '[0-9][0-9\\.]*(m|ms|d|h|s)', Number),
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
                   '[a-zA-Z_][a-zA-Z0-9_]*', Name.Function, '#pop')], 
       'classname': [
                   (
                    '[a-zA-Z_][a-zA-Z0-9_]*', Name.Class, '#pop')], 
       'namespace': [
                   (
                    '[a-zA-Z_][a-zA-Z0-9_.]*', Name.Namespace, '#pop')]}


class VbNetLexer(RegexLexer):
    """
    For
    `Visual Basic.NET <http://msdn2.microsoft.com/en-us/vbasic/default.aspx>`_
    source code.
    """
    name = 'VB.net'
    aliases = ['vb.net', 'vbnet']
    filenames = ['*.vb', '*.bas']
    mimetypes = ['text/x-vbnet', 'text/x-vba']
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
               '#If\\s.*?\\sThen|#ElseIf\\s.*?\\sThen|#End\\s+If|#Const|#ExternalSource.*?\\n|#End\\s+ExternalSource|#Region.*?\\n|#End\\s+Region|#ExternalChecksum',
               Comment.Preproc),
              (
               '[\\(\\){}!#,.:]', Punctuation),
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
               '&=|[*]=|/=|\\\\=|\\^=|\\+=|-=|<<=|>>=|<<|>>|:=|<=|>=|<>|[-&*/\\\\^+=<>]',
               Operator),
              (
               '"', String, 'string'),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*[%&@!#$]?', Name),
              (
               '#.*?#', Literal.Date),
              (
               '(\\d+\\.\\d*|\\d*\\.\\d+)([fF][+-]?[0-9]+)?', Number.Float),
              (
               '\\d+([SILDFR]|US|UI|UL)?', Number.Integer),
              (
               '&H[0-9a-f]+([SILDFR]|US|UI|UL)?', Number.Integer),
              (
               '&O[0-7]+([SILDFR]|US|UI|UL)?', Number.Integer),
              (
               '_\\n', Text)], 
       'string': [
                (
                 '""', String),
                (
                 '"C?', String, '#pop'),
                (
                 '[^"]+', String)], 
       'dim': [
             (
              '[a-z_][a-z0-9_]*', Name.Variable, '#pop'),
             (
              '', Text, '#pop')], 
       'funcname': [
                  (
                   '[a-z_][a-z0-9_]*', Name.Function, '#pop')], 
       'classname': [
                   (
                    '[a-z_][a-z0-9_]*', Name.Class, '#pop')], 
       'namespace': [
                   (
                    '[a-z_][a-z0-9_.]*', Name.Namespace, '#pop')], 
       'end': [
             (
              '\\s+', Text),
             (
              '(Function|Sub|Property|Class|Structure|Enum|Module|Namespace)\\b',
              Keyword, '#pop'),
             (
              '', Text, '#pop')]}


class GenericAspxLexer(RegexLexer):
    """
    Lexer for ASP.NET pages.
    """
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
    """
    Lexer for highligting C# within ASP.NET pages.
    """
    name = 'aspx-cs'
    aliases = ['aspx-cs']
    filenames = ['*.aspx', '*.asax', '*.ascx', '*.ashx', '*.asmx', '*.axd']
    mimetypes = []

    def __init__(self, **options):
        super(CSharpAspxLexer, self).__init__(CSharpLexer, GenericAspxLexer, **options)

    def analyse_text(text):
        if re.search('Page\\s*Language="C#"', text, re.I) is not None:
            return 0.2
        else:
            if re.search('script[^>]+language=["\\\']C#', text, re.I) is not None:
                return 0.15
            return 0.001


class VbNetAspxLexer(DelegatingLexer):
    """
    Lexer for highligting Visual Basic.net within ASP.NET pages.
    """
    name = 'aspx-vb'
    aliases = ['aspx-vb']
    filenames = ['*.aspx', '*.asax', '*.ascx', '*.ashx', '*.asmx', '*.axd']
    mimetypes = []

    def __init__(self, **options):
        super(VbNetAspxLexer, self).__init__(VbNetLexer, GenericAspxLexer, **options)

    def analyse_text(text):
        if re.search('Page\\s*Language="Vb"', text, re.I) is not None:
            return 0.2
        else:
            if re.search('script[^>]+language=["\\\']vb', text, re.I) is not None:
                return 0.15
            return