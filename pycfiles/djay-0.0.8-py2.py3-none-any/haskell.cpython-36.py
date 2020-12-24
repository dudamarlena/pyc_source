# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/haskell.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 32071 bytes
"""
    pygments.lexers.haskell
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Haskell and related languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, bygroups, do_insertions, default, include, inherit
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic
from pygments import unistring as uni
__all__ = [
 'HaskellLexer', 'HspecLexer', 'IdrisLexer', 'AgdaLexer', 'CryptolLexer',
 'LiterateHaskellLexer', 'LiterateIdrisLexer', 'LiterateAgdaLexer',
 'LiterateCryptolLexer', 'KokaLexer']
line_re = re.compile('.*?\n')

class HaskellLexer(RegexLexer):
    __doc__ = '\n    A Haskell lexer based on the lexemes defined in the Haskell 98 Report.\n\n    .. versionadded:: 0.8\n    '
    name = 'Haskell'
    aliases = ['haskell', 'hs']
    filenames = ['*.hs']
    mimetypes = ['text/x-haskell']
    flags = re.MULTILINE | re.UNICODE
    reserved = ('case', 'class', 'data', 'default', 'deriving', 'do', 'else', 'family',
                'if', 'in', 'infix[lr]?', 'instance', 'let', 'newtype', 'of', 'then',
                'type', 'where', '_')
    ascii = ('NUL', 'SOH', '[SE]TX', 'EOT', 'ENQ', 'ACK', 'BEL', 'BS', 'HT', 'LF',
             'VT', 'FF', 'CR', 'S[OI]', 'DLE', 'DC[1-4]', 'NAK', 'SYN', 'ETB', 'CAN',
             'EM', 'SUB', 'ESC', '[FGRU]S', 'SP', 'DEL')
    tokens = {'root':[
      (
       '\\s+', Text),
      (
       '--(?![!#$%&*+./<=>?@^|_~:\\\\]).*?$', Comment.Single),
      (
       '\\{-', Comment.Multiline, 'comment'),
      (
       '\\bimport\\b', Keyword.Reserved, 'import'),
      (
       '\\bmodule\\b', Keyword.Reserved, 'module'),
      (
       '\\berror\\b', Name.Exception),
      (
       "\\b(%s)(?!\\')\\b" % '|'.join(reserved), Keyword.Reserved),
      (
       "'[^\\\\]'", String.Char),
      (
       '^[_' + uni.Ll + "][\\w\\']*", Name.Function),
      (
       "'?[_" + uni.Ll + "][\\w']*", Name),
      (
       "('')?[" + uni.Lu + "][\\w\\']*", Keyword.Type),
      (
       "(')[" + uni.Lu + "][\\w\\']*", Keyword.Type),
      (
       "(')\\[[^\\]]*\\]", Keyword.Type),
      (
       "(')\\([^)]*\\)", Keyword.Type),
      (
       '\\\\(?![:!#$%&*+.\\\\/<=>?@^|~-]+)', Name.Function),
      (
       '(<-|::|->|=>|=)(?![:!#$%&*+.\\\\/<=>?@^|~-]+)', Operator.Word),
      (
       ':[:!#$%&*+.\\\\/<=>?@^|~-]*', Keyword.Type),
      (
       '[:!#$%&*+.\\\\/<=>?@^|~-]+', Operator),
      (
       '0[xX]_*[\\da-fA-F](_*[\\da-fA-F])*_*[pP][+-]?\\d(_*\\d)*', Number.Float),
      (
       '0[xX]_*[\\da-fA-F](_*[\\da-fA-F])*\\.[\\da-fA-F](_*[\\da-fA-F])*(_*[pP][+-]?\\d(_*\\d)*)?',
       Number.Float),
      (
       '\\d(_*\\d)*_*[eE][+-]?\\d(_*\\d)*', Number.Float),
      (
       '\\d(_*\\d)*\\.\\d(_*\\d)*(_*[eE][+-]?\\d(_*\\d)*)?', Number.Float),
      (
       '0[bB]_*[01](_*[01])*', Number.Bin),
      (
       '0[oO]_*[0-7](_*[0-7])*', Number.Oct),
      (
       '0[xX]_*[\\da-fA-F](_*[\\da-fA-F])*', Number.Hex),
      (
       '\\d(_*\\d)*', Number.Integer),
      (
       "'", String.Char, 'character'),
      (
       '"', String, 'string'),
      (
       '\\[\\]', Keyword.Type),
      (
       '\\(\\)', Name.Builtin),
      (
       '[][(),;`{}]', Punctuation)], 
     'import':[
      (
       '\\s+', Text),
      (
       '"', String, 'string'),
      (
       '\\)', Punctuation, '#pop'),
      (
       'qualified\\b', Keyword),
      (
       '([' + uni.Lu + '][\\w.]*)(\\s+)(as)(\\s+)([' + uni.Lu + '][\\w.]*)',
       bygroups(Name.Namespace, Text, Keyword, Text, Name), '#pop'),
      (
       '([' + uni.Lu + '][\\w.]*)(\\s+)(hiding)(\\s+)(\\()',
       bygroups(Name.Namespace, Text, Keyword, Text, Punctuation), 'funclist'),
      (
       '([' + uni.Lu + '][\\w.]*)(\\s+)(\\()',
       bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
      (
       '[\\w.]+', Name.Namespace, '#pop')], 
     'module':[
      (
       '\\s+', Text),
      (
       '([' + uni.Lu + '][\\w.]*)(\\s+)(\\()',
       bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
      (
       '[' + uni.Lu + '][\\w.]*', Name.Namespace, '#pop')], 
     'funclist':[
      (
       '\\s+', Text),
      (
       '[' + uni.Lu + ']\\w*', Keyword.Type),
      (
       "(_[\\w\\']+|[" + uni.Ll + "][\\w\\']*)", Name.Function),
      (
       '--(?![!#$%&*+./<=>?@^|_~:\\\\]).*?$', Comment.Single),
      (
       '\\{-', Comment.Multiline, 'comment'),
      (
       ',', Punctuation),
      (
       '[:!#$%&*+.\\\\/<=>?@^|~-]+', Operator),
      (
       '\\(', Punctuation, ('funclist', 'funclist')),
      (
       '\\)', Punctuation, '#pop:2')], 
     'comment':[
      (
       '[^-{}]+', Comment.Multiline),
      (
       '\\{-', Comment.Multiline, '#push'),
      (
       '-\\}', Comment.Multiline, '#pop'),
      (
       '[-{}]', Comment.Multiline)], 
     'character':[
      (
       "[^\\\\']'", String.Char, '#pop'),
      (
       '\\\\', String.Escape, 'escape'),
      (
       "'", String.Char, '#pop')], 
     'string':[
      (
       '[^\\\\"]+', String),
      (
       '\\\\', String.Escape, 'escape'),
      (
       '"', String, '#pop')], 
     'escape':[
      (
       '[abfnrtv"\\\'&\\\\]', String.Escape, '#pop'),
      (
       '\\^[][' + uni.Lu + '@^_]', String.Escape, '#pop'),
      (
       '|'.join(ascii), String.Escape, '#pop'),
      (
       'o[0-7]+', String.Escape, '#pop'),
      (
       'x[\\da-fA-F]+', String.Escape, '#pop'),
      (
       '\\d+', String.Escape, '#pop'),
      (
       '\\s+\\\\', String.Escape, '#pop')]}


class HspecLexer(HaskellLexer):
    __doc__ = '\n    A Haskell lexer with support for Hspec constructs.\n\n    .. versionadded:: 2.4.0\n    '
    name = 'Hspec'
    aliases = ['hspec']
    filenames = []
    mimetypes = []
    tokens = {'root': [
              (
               '(it\\s*)("[^"]*")', bygroups(Text, String.Doc)),
              (
               '(describe\\s*)("[^"]*")', bygroups(Text, String.Doc)),
              (
               '(context\\s*)("[^"]*")', bygroups(Text, String.Doc)),
              inherit]}


class IdrisLexer(RegexLexer):
    __doc__ = '\n    A lexer for the dependently typed programming language Idris.\n\n    Based on the Haskell and Agda Lexer.\n\n    .. versionadded:: 2.0\n    '
    name = 'Idris'
    aliases = ['idris', 'idr']
    filenames = ['*.idr']
    mimetypes = ['text/x-idris']
    reserved = ('case', 'class', 'data', 'default', 'using', 'do', 'else', 'if', 'in',
                'infix[lr]?', 'instance', 'rewrite', 'auto', 'namespace', 'codata',
                'mutual', 'private', 'public', 'abstract', 'total', 'partial', 'let',
                'proof', 'of', 'then', 'static', 'where', '_', 'with', 'pattern',
                'term', 'syntax', 'prefix', 'postulate', 'parameters', 'record',
                'dsl', 'impossible', 'implicit', 'tactics', 'intros', 'intro', 'compute',
                'refine', 'exact', 'trivial')
    ascii = ('NUL', 'SOH', '[SE]TX', 'EOT', 'ENQ', 'ACK', 'BEL', 'BS', 'HT', 'LF',
             'VT', 'FF', 'CR', 'S[OI]', 'DLE', 'DC[1-4]', 'NAK', 'SYN', 'ETB', 'CAN',
             'EM', 'SUB', 'ESC', '[FGRU]S', 'SP', 'DEL')
    directives = ('lib', 'link', 'flag', 'include', 'hide', 'freeze', 'access', 'default',
                  'logging', 'dynamic', 'name', 'error_handlers', 'language')
    tokens = {'root':[
      (
       '^(\\s*)(%%%s)' % '|'.join(directives),
       bygroups(Text, Keyword.Reserved)),
      (
       '(\\s*)(--(?![!#$%&*+./<=>?@^|_~:\\\\]).*?)$', bygroups(Text, Comment.Single)),
      (
       '(\\s*)(\\|{3}.*?)$', bygroups(Text, Comment.Single)),
      (
       '(\\s*)(\\{-)', bygroups(Text, Comment.Multiline), 'comment'),
      (
       '^(\\s*)([^\\s(){}]+)(\\s*)(:)(\\s*)',
       bygroups(Text, Name.Function, Text, Operator.Word, Text)),
      (
       "\\b(%s)(?!\\')\\b" % '|'.join(reserved), Keyword.Reserved),
      (
       '(import|module)(\\s+)', bygroups(Keyword.Reserved, Text), 'module'),
      (
       "('')?[A-Z][\\w\\']*", Keyword.Type),
      (
       "[a-z][\\w\\']*", Text),
      (
       '(<-|::|->|=>|=)', Operator.Word),
      (
       '([(){}\\[\\]:!#$%&*+.\\\\/<=>?@^|~-]+)', Operator.Word),
      (
       '\\d+[eE][+-]?\\d+', Number.Float),
      (
       '\\d+\\.\\d+([eE][+-]?\\d+)?', Number.Float),
      (
       '0[xX][\\da-fA-F]+', Number.Hex),
      (
       '\\d+', Number.Integer),
      (
       "'", String.Char, 'character'),
      (
       '"', String, 'string'),
      (
       '[^\\s(){}]+', Text),
      (
       '\\s+?', Text)], 
     'module':[
      (
       '\\s+', Text),
      (
       '([A-Z][\\w.]*)(\\s+)(\\()',
       bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
      (
       '[A-Z][\\w.]*', Name.Namespace, '#pop')], 
     'funclist':[
      (
       '\\s+', Text),
      (
       '[A-Z]\\w*', Keyword.Type),
      (
       "(_[\\w\\']+|[a-z][\\w\\']*)", Name.Function),
      (
       '--.*$', Comment.Single),
      (
       '\\{-', Comment.Multiline, 'comment'),
      (
       ',', Punctuation),
      (
       '[:!#$%&*+.\\\\/<=>?@^|~-]+', Operator),
      (
       '\\(', Punctuation, ('funclist', 'funclist')),
      (
       '\\)', Punctuation, '#pop:2')], 
     'comment':[
      (
       '[^-{}]+', Comment.Multiline),
      (
       '\\{-', Comment.Multiline, '#push'),
      (
       '-\\}', Comment.Multiline, '#pop'),
      (
       '[-{}]', Comment.Multiline)], 
     'character':[
      (
       "[^\\\\']", String.Char),
      (
       '\\\\', String.Escape, 'escape'),
      (
       "'", String.Char, '#pop')], 
     'string':[
      (
       '[^\\\\"]+', String),
      (
       '\\\\', String.Escape, 'escape'),
      (
       '"', String, '#pop')], 
     'escape':[
      (
       '[abfnrtv"\\\'&\\\\]', String.Escape, '#pop'),
      (
       '\\^[][A-Z@^_]', String.Escape, '#pop'),
      (
       '|'.join(ascii), String.Escape, '#pop'),
      (
       'o[0-7]+', String.Escape, '#pop'),
      (
       'x[\\da-fA-F]+', String.Escape, '#pop'),
      (
       '\\d+', String.Escape, '#pop'),
      (
       '\\s+\\\\', String.Escape, '#pop')]}


class AgdaLexer(RegexLexer):
    __doc__ = '\n    For the `Agda <http://wiki.portal.chalmers.se/agda/pmwiki.php>`_\n    dependently typed functional programming language and proof assistant.\n\n    .. versionadded:: 2.0\n    '
    name = 'Agda'
    aliases = ['agda']
    filenames = ['*.agda']
    mimetypes = ['text/x-agda']
    reserved = [
     'abstract', 'codata', 'coinductive', 'constructor', 'data',
     'field', 'forall', 'hiding', 'in', 'inductive', 'infix',
     'infixl', 'infixr', 'instance', 'let', 'mutual', 'open',
     'pattern', 'postulate', 'primitive', 'private',
     'quote', 'quoteGoal', 'quoteTerm',
     'record', 'renaming', 'rewrite', 'syntax', 'tactic',
     'unquote', 'unquoteDecl', 'using', 'where', 'with']
    tokens = {'root':[
      (
       '^(\\s*)([^\\s(){}]+)(\\s*)(:)(\\s*)',
       bygroups(Text, Name.Function, Text, Operator.Word, Text)),
      (
       '--(?![!#$%&*+./<=>?@^|_~:\\\\]).*?$', Comment.Single),
      (
       '\\{-', Comment.Multiline, 'comment'),
      (
       '\\{!', Comment.Directive, 'hole'),
      (
       "\\b(%s)(?!\\')\\b" % '|'.join(reserved), Keyword.Reserved),
      (
       '(import|module)(\\s+)', bygroups(Keyword.Reserved, Text), 'module'),
      (
       '\\b(Set|Prop)\\b', Keyword.Type),
      (
       '(\\(|\\)|\\{|\\})', Operator),
      (
       '(\\.{1,3}|\\||Λ|∀|→|:|=|->)', Operator.Word),
      (
       '\\d+[eE][+-]?\\d+', Number.Float),
      (
       '\\d+\\.\\d+([eE][+-]?\\d+)?', Number.Float),
      (
       '0[xX][\\da-fA-F]+', Number.Hex),
      (
       '\\d+', Number.Integer),
      (
       "'", String.Char, 'character'),
      (
       '"', String, 'string'),
      (
       '[^\\s(){}]+', Text),
      (
       '\\s+?', Text)], 
     'hole':[
      (
       '[^!{}]+', Comment.Directive),
      (
       '\\{!', Comment.Directive, '#push'),
      (
       '!\\}', Comment.Directive, '#pop'),
      (
       '[!{}]', Comment.Directive)], 
     'module':[
      (
       '\\{-', Comment.Multiline, 'comment'),
      (
       '[a-zA-Z][\\w.]*', Name, '#pop'),
      (
       '[\\W0-9_]+', Text)], 
     'comment':HaskellLexer.tokens['comment'], 
     'character':HaskellLexer.tokens['character'], 
     'string':HaskellLexer.tokens['string'], 
     'escape':HaskellLexer.tokens['escape']}


class CryptolLexer(RegexLexer):
    __doc__ = '\n    FIXME: A Cryptol2 lexer based on the lexemes defined in the Haskell 98 Report.\n\n    .. versionadded:: 2.0\n    '
    name = 'Cryptol'
    aliases = ['cryptol', 'cry']
    filenames = ['*.cry']
    mimetypes = ['text/x-cryptol']
    reserved = ('Arith', 'Bit', 'Cmp', 'False', 'Inf', 'True', 'else', 'export', 'extern',
                'fin', 'if', 'import', 'inf', 'lg2', 'max', 'min', 'module', 'newtype',
                'pragma', 'property', 'then', 'type', 'where', 'width')
    ascii = ('NUL', 'SOH', '[SE]TX', 'EOT', 'ENQ', 'ACK', 'BEL', 'BS', 'HT', 'LF',
             'VT', 'FF', 'CR', 'S[OI]', 'DLE', 'DC[1-4]', 'NAK', 'SYN', 'ETB', 'CAN',
             'EM', 'SUB', 'ESC', '[FGRU]S', 'SP', 'DEL')
    tokens = {'root':[
      (
       '\\s+', Text),
      (
       '//.*$', Comment.Single),
      (
       '/\\*', Comment.Multiline, 'comment'),
      (
       '\\bimport\\b', Keyword.Reserved, 'import'),
      (
       '\\bmodule\\b', Keyword.Reserved, 'module'),
      (
       '\\berror\\b', Name.Exception),
      (
       "\\b(%s)(?!\\')\\b" % '|'.join(reserved), Keyword.Reserved),
      (
       "^[_a-z][\\w\\']*", Name.Function),
      (
       "'?[_a-z][\\w']*", Name),
      (
       "('')?[A-Z][\\w\\']*", Keyword.Type),
      (
       '\\\\(?![:!#$%&*+.\\\\/<=>?@^|~-]+)', Name.Function),
      (
       '(<-|::|->|=>|=)(?![:!#$%&*+.\\\\/<=>?@^|~-]+)', Operator.Word),
      (
       ':[:!#$%&*+.\\\\/<=>?@^|~-]*', Keyword.Type),
      (
       '[:!#$%&*+.\\\\/<=>?@^|~-]+', Operator),
      (
       '\\d+[eE][+-]?\\d+', Number.Float),
      (
       '\\d+\\.\\d+([eE][+-]?\\d+)?', Number.Float),
      (
       '0[oO][0-7]+', Number.Oct),
      (
       '0[xX][\\da-fA-F]+', Number.Hex),
      (
       '\\d+', Number.Integer),
      (
       "'", String.Char, 'character'),
      (
       '"', String, 'string'),
      (
       '\\[\\]', Keyword.Type),
      (
       '\\(\\)', Name.Builtin),
      (
       '[][(),;`{}]', Punctuation)], 
     'import':[
      (
       '\\s+', Text),
      (
       '"', String, 'string'),
      (
       '\\)', Punctuation, '#pop'),
      (
       'qualified\\b', Keyword),
      (
       '([A-Z][\\w.]*)(\\s+)(as)(\\s+)([A-Z][\\w.]*)',
       bygroups(Name.Namespace, Text, Keyword, Text, Name), '#pop'),
      (
       '([A-Z][\\w.]*)(\\s+)(hiding)(\\s+)(\\()',
       bygroups(Name.Namespace, Text, Keyword, Text, Punctuation), 'funclist'),
      (
       '([A-Z][\\w.]*)(\\s+)(\\()',
       bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
      (
       '[\\w.]+', Name.Namespace, '#pop')], 
     'module':[
      (
       '\\s+', Text),
      (
       '([A-Z][\\w.]*)(\\s+)(\\()',
       bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
      (
       '[A-Z][\\w.]*', Name.Namespace, '#pop')], 
     'funclist':[
      (
       '\\s+', Text),
      (
       '[A-Z]\\w*', Keyword.Type),
      (
       "(_[\\w\\']+|[a-z][\\w\\']*)", Name.Function),
      (
       ',', Punctuation),
      (
       '[:!#$%&*+.\\\\/<=>?@^|~-]+', Operator),
      (
       '\\(', Punctuation, ('funclist', 'funclist')),
      (
       '\\)', Punctuation, '#pop:2')], 
     'comment':[
      (
       '[^/*]+', Comment.Multiline),
      (
       '/\\*', Comment.Multiline, '#push'),
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '[*/]', Comment.Multiline)], 
     'character':[
      (
       "[^\\\\']'", String.Char, '#pop'),
      (
       '\\\\', String.Escape, 'escape'),
      (
       "'", String.Char, '#pop')], 
     'string':[
      (
       '[^\\\\"]+', String),
      (
       '\\\\', String.Escape, 'escape'),
      (
       '"', String, '#pop')], 
     'escape':[
      (
       '[abfnrtv"\\\'&\\\\]', String.Escape, '#pop'),
      (
       '\\^[][A-Z@^_]', String.Escape, '#pop'),
      (
       '|'.join(ascii), String.Escape, '#pop'),
      (
       'o[0-7]+', String.Escape, '#pop'),
      (
       'x[\\da-fA-F]+', String.Escape, '#pop'),
      (
       '\\d+', String.Escape, '#pop'),
      (
       '\\s+\\\\', String.Escape, '#pop')]}
    EXTRA_KEYWORDS = set(('join', 'split', 'reverse', 'transpose', 'width', 'length',
                          'tail', '<<', '>>', '<<<', '>>>', 'const', 'reg', 'par',
                          'seq', 'ASSERT', 'undefined', 'error', 'trace'))

    def get_tokens_unprocessed(self, text):
        stack = [
         'root']
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text, stack):
            if token is Name and value in self.EXTRA_KEYWORDS:
                yield (
                 index, Name.Builtin, value)
            else:
                yield (
                 index, token, value)


class LiterateLexer(Lexer):
    __doc__ = '\n    Base class for lexers of literate file formats based on LaTeX or Bird-style\n    (prefixing each code line with ">").\n\n    Additional options accepted:\n\n    `litstyle`\n        If given, must be ``"bird"`` or ``"latex"``.  If not given, the style\n        is autodetected: if the first non-whitespace character in the source\n        is a backslash or percent character, LaTeX is assumed, else Bird.\n    '
    bird_re = re.compile('(>[ \\t]*)(.*\\n)')

    def __init__(self, baselexer, **options):
        self.baselexer = baselexer
        (Lexer.__init__)(self, **options)

    def get_tokens_unprocessed(self, text):
        style = self.options.get('litstyle')
        if style is None:
            style = text.lstrip()[0:1] in '%\\' and 'latex' or 'bird'
        else:
            code = ''
            insertions = []
            if style == 'bird':
                for match in line_re.finditer(text):
                    line = match.group()
                    m = self.bird_re.match(line)
                    if m:
                        insertions.append((len(code),
                         [
                          (
                           0, Comment.Special, m.group(1))]))
                        code += m.group(2)
                    else:
                        insertions.append((len(code), [(0, Text, line)]))

            else:
                from pygments.lexers.markup import TexLexer
                lxlexer = TexLexer(**self.options)
                codelines = 0
                latex = ''
                for match in line_re.finditer(text):
                    line = match.group()
                    if codelines:
                        if line.lstrip().startswith('\\end{code}'):
                            codelines = 0
                            latex += line
                        else:
                            code += line
                    else:
                        if line.lstrip().startswith('\\begin{code}'):
                            codelines = 1
                            latex += line
                            insertions.append((len(code),
                             list(lxlexer.get_tokens_unprocessed(latex))))
                            latex = ''
                        else:
                            latex += line

                insertions.append((len(code),
                 list(lxlexer.get_tokens_unprocessed(latex))))
        for item in do_insertions(insertions, self.baselexer.get_tokens_unprocessed(code)):
            yield item


class LiterateHaskellLexer(LiterateLexer):
    __doc__ = '\n    For Literate Haskell (Bird-style or LaTeX) source.\n\n    Additional options accepted:\n\n    `litstyle`\n        If given, must be ``"bird"`` or ``"latex"``.  If not given, the style\n        is autodetected: if the first non-whitespace character in the source\n        is a backslash or percent character, LaTeX is assumed, else Bird.\n\n    .. versionadded:: 0.9\n    '
    name = 'Literate Haskell'
    aliases = ['lhs', 'literate-haskell', 'lhaskell']
    filenames = ['*.lhs']
    mimetypes = ['text/x-literate-haskell']

    def __init__(self, **options):
        hslexer = HaskellLexer(**options)
        (LiterateLexer.__init__)(self, hslexer, **options)


class LiterateIdrisLexer(LiterateLexer):
    __doc__ = '\n    For Literate Idris (Bird-style or LaTeX) source.\n\n    Additional options accepted:\n\n    `litstyle`\n        If given, must be ``"bird"`` or ``"latex"``.  If not given, the style\n        is autodetected: if the first non-whitespace character in the source\n        is a backslash or percent character, LaTeX is assumed, else Bird.\n\n    .. versionadded:: 2.0\n    '
    name = 'Literate Idris'
    aliases = ['lidr', 'literate-idris', 'lidris']
    filenames = ['*.lidr']
    mimetypes = ['text/x-literate-idris']

    def __init__(self, **options):
        hslexer = IdrisLexer(**options)
        (LiterateLexer.__init__)(self, hslexer, **options)


class LiterateAgdaLexer(LiterateLexer):
    __doc__ = '\n    For Literate Agda source.\n\n    Additional options accepted:\n\n    `litstyle`\n        If given, must be ``"bird"`` or ``"latex"``.  If not given, the style\n        is autodetected: if the first non-whitespace character in the source\n        is a backslash or percent character, LaTeX is assumed, else Bird.\n\n    .. versionadded:: 2.0\n    '
    name = 'Literate Agda'
    aliases = ['lagda', 'literate-agda']
    filenames = ['*.lagda']
    mimetypes = ['text/x-literate-agda']

    def __init__(self, **options):
        agdalexer = AgdaLexer(**options)
        (LiterateLexer.__init__)(self, agdalexer, litstyle='latex', **options)


class LiterateCryptolLexer(LiterateLexer):
    __doc__ = '\n    For Literate Cryptol (Bird-style or LaTeX) source.\n\n    Additional options accepted:\n\n    `litstyle`\n        If given, must be ``"bird"`` or ``"latex"``.  If not given, the style\n        is autodetected: if the first non-whitespace character in the source\n        is a backslash or percent character, LaTeX is assumed, else Bird.\n\n    .. versionadded:: 2.0\n    '
    name = 'Literate Cryptol'
    aliases = ['lcry', 'literate-cryptol', 'lcryptol']
    filenames = ['*.lcry']
    mimetypes = ['text/x-literate-cryptol']

    def __init__(self, **options):
        crylexer = CryptolLexer(**options)
        (LiterateLexer.__init__)(self, crylexer, **options)


class KokaLexer(RegexLexer):
    __doc__ = '\n    Lexer for the `Koka <http://koka.codeplex.com>`_\n    language.\n\n    .. versionadded:: 1.6\n    '
    name = 'Koka'
    aliases = ['koka']
    filenames = ['*.kk', '*.kki']
    mimetypes = ['text/x-koka']
    keywords = [
     'infix', 'infixr', 'infixl',
     'type', 'cotype', 'rectype', 'alias',
     'struct', 'con',
     'fun', 'function', 'val', 'var',
     'external',
     'if', 'then', 'else', 'elif', 'return', 'match',
     'private', 'public', 'private',
     'module', 'import', 'as',
     'include', 'inline',
     'rec',
     'try', 'yield', 'enum',
     'interface', 'instance']
    typeStartKeywords = [
     'type', 'cotype', 'rectype', 'alias', 'struct', 'enum']
    typekeywords = [
     'forall', 'exists', 'some', 'with']
    builtin = [
     'for', 'while', 'repeat',
     'foreach', 'foreach-indexed',
     'error', 'catch', 'finally',
     'cs', 'js', 'file', 'ref', 'assigned']
    symbols = '[$%&*+@!/\\\\^~=.:\\-?|<>]+'
    sboundary = '(?!' + symbols + ')'
    boundary = '(?![\\w/])'
    tokenType = Name.Attribute
    tokenTypeDef = Name.Class
    tokenConstructor = Generic.Emph
    tokens = {'root':[
      include('whitespace'),
      (
       '::?' + sboundary, tokenType, 'type'),
      (
       '(alias)(\\s+)([a-z]\\w*)?', bygroups(Keyword, Text, tokenTypeDef),
       'alias-type'),
      (
       '(struct)(\\s+)([a-z]\\w*)?', bygroups(Keyword, Text, tokenTypeDef),
       'struct-type'),
      (
       '(%s)' % '|'.join(typeStartKeywords) + '(\\s+)([a-z]\\w*)?', bygroups(Keyword, Text, tokenTypeDef),
       'type'),
      (
       '(module)(\\s+)(interface\\s+)?((?:[a-z]\\w*/)*[a-z]\\w*)',
       bygroups(Keyword, Text, Keyword, Name.Namespace)),
      (
       '(import)(\\s+)((?:[a-z]\\w*/)*[a-z]\\w*)(?:(\\s*)(=)(\\s*)((?:qualified\\s*)?)((?:[a-z]\\w*/)*[a-z]\\w*))?',
       bygroups(Keyword, Text, Name.Namespace, Text, Keyword, Text, Keyword, Name.Namespace)),
      (
       '(^(?:(?:public|private)\\s*)?(?:function|fun|val))(\\s+)([a-z]\\w*|\\((?:' + symbols + '|/)\\))',
       bygroups(Keyword, Text, Name.Function)),
      (
       '(^(?:(?:public|private)\\s*)?external)(\\s+)(inline\\s+)?([a-z]\\w*|\\((?:' + symbols + '|/)\\))',
       bygroups(Keyword, Text, Keyword, Name.Function)),
      (
       '(%s)' % '|'.join(typekeywords) + boundary, Keyword.Type),
      (
       '(%s)' % '|'.join(keywords) + boundary, Keyword),
      (
       '(%s)' % '|'.join(builtin) + boundary, Keyword.Pseudo),
      (
       '::?|:=|\\->|[=.]' + sboundary, Keyword),
      (
       '((?:[a-z]\\w*/)*)([A-Z]\\w*)',
       bygroups(Name.Namespace, tokenConstructor)),
      (
       '((?:[a-z]\\w*/)*)([a-z]\\w*)', bygroups(Name.Namespace, Name)),
      (
       '((?:[a-z]\\w*/)*)(\\((?:' + symbols + '|/)\\))',
       bygroups(Name.Namespace, Name)),
      (
       '_\\w*', Name.Variable),
      (
       '@"', String.Double, 'litstring'),
      (
       symbols + '|/(?![*/])', Operator),
      (
       '`', Operator),
      (
       '[{}()\\[\\];,]', Punctuation),
      (
       '[0-9]+\\.[0-9]+([eE][\\-+]?[0-9]+)?', Number.Float),
      (
       '0[xX][0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+', Number.Integer),
      (
       "'", String.Char, 'char'),
      (
       '"', String.Double, 'string')], 
     'alias-type':[
      (
       '=', Keyword),
      include('type')], 
     'struct-type':[
      (
       '(?=\\((?!,*\\)))', Punctuation, '#pop'),
      include('type')], 
     'type':[
      (
       '[(\\[<]', tokenType, 'type-nested'),
      include('type-content')], 
     'type-nested':[
      (
       '[)\\]>]', tokenType, '#pop'),
      (
       '[(\\[<]', tokenType, 'type-nested'),
      (
       ',', tokenType),
      (
       '([a-z]\\w*)(\\s*)(:)(?!:)',
       bygroups(Name, Text, tokenType)),
      include('type-content')], 
     'type-content':[
      include('whitespace'),
      (
       '(%s)' % '|'.join(typekeywords) + boundary, Keyword),
      (
       '(?=((%s)' % '|'.join(keywords) + boundary + '))',
       Keyword, '#pop'),
      (
       '[EPHVX]' + boundary, tokenType),
      (
       '[a-z][0-9]*(?![\\w/])', tokenType),
      (
       '_\\w*', tokenType.Variable),
      (
       '((?:[a-z]\\w*/)*)([A-Z]\\w*)',
       bygroups(Name.Namespace, tokenType)),
      (
       '((?:[a-z]\\w*/)*)([a-z]\\w+)',
       bygroups(Name.Namespace, tokenType)),
      (
       '::|->|[.:|]', tokenType),
      default('#pop')], 
     'whitespace':[
      (
       '\\n\\s*#.*$', Comment.Preproc),
      (
       '\\s+', Text),
      (
       '/\\*', Comment.Multiline, 'comment'),
      (
       '//.*$', Comment.Single)], 
     'comment':[
      (
       '[^/*]+', Comment.Multiline),
      (
       '/\\*', Comment.Multiline, '#push'),
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '[*/]', Comment.Multiline)], 
     'litstring':[
      (
       '[^"]+', String.Double),
      (
       '""', String.Escape),
      (
       '"', String.Double, '#pop')], 
     'string':[
      (
       '[^\\\\"\\n]+', String.Double),
      include('escape-sequence'),
      (
       '["\\n]', String.Double, '#pop')], 
     'char':[
      (
       "[^\\\\\\'\\n]+", String.Char),
      include('escape-sequence'),
      (
       "[\\'\\n]", String.Char, '#pop')], 
     'escape-sequence':[
      (
       '\\\\[nrt\\\\"\\\']', String.Escape),
      (
       '\\\\x[0-9a-fA-F]{2}', String.Escape),
      (
       '\\\\u[0-9a-fA-F]{4}', String.Escape),
      (
       '\\\\U[0-9a-fA-F]{6}', String.Escape)]}