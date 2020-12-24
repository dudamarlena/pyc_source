# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/haxe.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 30959 bytes
"""
    pygments.lexers.haxe
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for Haxe and related stuff.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import ExtendedRegexLexer, RegexLexer, include, bygroups, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic, Whitespace
__all__ = [
 'HaxeLexer', 'HxmlLexer']

class HaxeLexer(ExtendedRegexLexer):
    __doc__ = '\n    For Haxe source code (http://haxe.org/).\n\n    .. versionadded:: 1.3\n    '
    name = 'Haxe'
    aliases = ['hx', 'haxe', 'hxsl']
    filenames = ['*.hx', '*.hxsl']
    mimetypes = ['text/haxe', 'text/x-haxe', 'text/x-hx']
    keyword = '(?:function|class|static|var|if|else|while|do|for|break|return|continue|extends|implements|import|switch|case|default|public|private|try|untyped|catch|new|this|throw|extern|enum|in|interface|cast|override|dynamic|typedef|package|inline|using|null|true|false|abstract)\\b'
    typeid = '_*[A-Z]\\w*'
    ident = '(?:_*[a-z]\\w*|_+[0-9]\\w*|' + typeid + '|_+|\\$\\w+)'
    binop = '(?:%=|&=|\\|=|\\^=|\\+=|\\-=|\\*=|/=|<<=|>\\s*>\\s*=|>\\s*>\\s*>\\s*=|==|!=|<=|>\\s*=|&&|\\|\\||<<|>>>|>\\s*>|\\.\\.\\.|<|>|%|&|\\||\\^|\\+|\\*|/|\\-|=>|=)'
    ident_no_keyword = '(?!' + keyword + ')' + ident
    flags = re.DOTALL | re.MULTILINE
    preproc_stack = []

    def preproc_callback(self, match, ctx):
        proc = match.group(2)
        if proc == 'if':
            self.preproc_stack.append(ctx.stack[:])
        else:
            if proc in ('else', 'elseif'):
                if self.preproc_stack:
                    ctx.stack = self.preproc_stack[(-1)][:]
            else:
                if proc == 'end':
                    if self.preproc_stack:
                        self.preproc_stack.pop()
        if proc in ('if', 'elseif'):
            ctx.stack.append('preproc-expr')
        if proc in ('error', ):
            ctx.stack.append('preproc-error')
        yield (match.start(), Comment.Preproc, '#' + proc)
        ctx.pos = match.end()

    tokens = {'root':[
      include('spaces'),
      include('meta'),
      (
       '(?:package)\\b', Keyword.Namespace, ('semicolon', 'package')),
      (
       '(?:import)\\b', Keyword.Namespace, ('semicolon', 'import')),
      (
       '(?:using)\\b', Keyword.Namespace, ('semicolon', 'using')),
      (
       '(?:extern|private)\\b', Keyword.Declaration),
      (
       '(?:abstract)\\b', Keyword.Declaration, 'abstract'),
      (
       '(?:class|interface)\\b', Keyword.Declaration, 'class'),
      (
       '(?:enum)\\b', Keyword.Declaration, 'enum'),
      (
       '(?:typedef)\\b', Keyword.Declaration, 'typedef'),
      (
       '(?=.)', Text, 'expr-statement')], 
     'spaces':[
      (
       '\\s+', Text),
      (
       '//[^\\n\\r]*', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '(#)(if|elseif|else|end|error)\\b', preproc_callback)], 
     'string-single-interpol':[
      (
       '\\$\\{', String.Interpol, ('string-interpol-close', 'expr')),
      (
       '\\$\\$', String.Escape),
      (
       '\\$(?=' + ident + ')', String.Interpol, 'ident'),
      include('string-single')], 
     'string-single':[
      (
       "'", String.Single, '#pop'),
      (
       '\\\\.', String.Escape),
      (
       '.', String.Single)], 
     'string-double':[
      (
       '"', String.Double, '#pop'),
      (
       '\\\\.', String.Escape),
      (
       '.', String.Double)], 
     'string-interpol-close':[
      (
       '\\$' + ident, String.Interpol),
      (
       '\\}', String.Interpol, '#pop')], 
     'package':[
      include('spaces'),
      (
       ident, Name.Namespace),
      (
       '\\.', Punctuation, 'import-ident'),
      default('#pop')], 
     'import':[
      include('spaces'),
      (
       ident, Name.Namespace),
      (
       '\\*', Keyword),
      (
       '\\.', Punctuation, 'import-ident'),
      (
       'in', Keyword.Namespace, 'ident'),
      default('#pop')], 
     'import-ident':[
      include('spaces'),
      (
       '\\*', Keyword, '#pop'),
      (
       ident, Name.Namespace, '#pop')], 
     'using':[
      include('spaces'),
      (
       ident, Name.Namespace),
      (
       '\\.', Punctuation, 'import-ident'),
      default('#pop')], 
     'preproc-error':[
      (
       '\\s+', Comment.Preproc),
      (
       "'", String.Single, ('#pop', 'string-single')),
      (
       '"', String.Double, ('#pop', 'string-double')),
      default('#pop')], 
     'preproc-expr':[
      (
       '\\s+', Comment.Preproc),
      (
       '\\!', Comment.Preproc),
      (
       '\\(', Comment.Preproc, ('#pop', 'preproc-parenthesis')),
      (
       ident, Comment.Preproc, '#pop'),
      (
       '\\.[0-9]+', Number.Float),
      (
       '[0-9]+[eE][+\\-]?[0-9]+', Number.Float),
      (
       '[0-9]+\\.[0-9]*[eE][+\\-]?[0-9]+', Number.Float),
      (
       '[0-9]+\\.[0-9]+', Number.Float),
      (
       '[0-9]+\\.(?!' + ident + '|\\.\\.)', Number.Float),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+', Number.Integer),
      (
       "'", String.Single, ('#pop', 'string-single')),
      (
       '"', String.Double, ('#pop', 'string-double'))], 
     'preproc-parenthesis':[
      (
       '\\s+', Comment.Preproc),
      (
       '\\)', Comment.Preproc, '#pop'),
      default('preproc-expr-in-parenthesis')], 
     'preproc-expr-chain':[
      (
       '\\s+', Comment.Preproc),
      (
       binop, Comment.Preproc, ('#pop', 'preproc-expr-in-parenthesis')),
      default('#pop')], 
     'preproc-expr-in-parenthesis':[
      (
       '\\s+', Comment.Preproc),
      (
       '\\!', Comment.Preproc),
      (
       '\\(', Comment.Preproc,
       ('#pop', 'preproc-expr-chain', 'preproc-parenthesis')),
      (
       ident, Comment.Preproc, ('#pop', 'preproc-expr-chain')),
      (
       '\\.[0-9]+', Number.Float, ('#pop', 'preproc-expr-chain')),
      (
       '[0-9]+[eE][+\\-]?[0-9]+', Number.Float, ('#pop', 'preproc-expr-chain')),
      (
       '[0-9]+\\.[0-9]*[eE][+\\-]?[0-9]+', Number.Float, ('#pop', 'preproc-expr-chain')),
      (
       '[0-9]+\\.[0-9]+', Number.Float, ('#pop', 'preproc-expr-chain')),
      (
       '[0-9]+\\.(?!' + ident + '|\\.\\.)', Number.Float, ('#pop', 'preproc-expr-chain')),
      (
       '0x[0-9a-fA-F]+', Number.Hex, ('#pop', 'preproc-expr-chain')),
      (
       '[0-9]+', Number.Integer, ('#pop', 'preproc-expr-chain')),
      (
       "'", String.Single,
       ('#pop', 'preproc-expr-chain', 'string-single')),
      (
       '"', String.Double,
       ('#pop', 'preproc-expr-chain', 'string-double'))], 
     'abstract':[
      include('spaces'),
      default(('#pop', 'abstract-body', 'abstract-relation', 'abstract-opaque', 'type-param-constraint',
         'type-name'))], 
     'abstract-body':[
      include('spaces'),
      (
       '\\{', Punctuation, ('#pop', 'class-body'))], 
     'abstract-opaque':[
      include('spaces'),
      (
       '\\(', Punctuation, ('#pop', 'parenthesis-close', 'type')),
      default('#pop')], 
     'abstract-relation':[
      include('spaces'),
      (
       '(?:to|from)', Keyword.Declaration, 'type'),
      (
       ',', Punctuation),
      default('#pop')], 
     'meta':[
      include('spaces'),
      (
       '@', Name.Decorator, ('meta-body', 'meta-ident', 'meta-colon'))], 
     'meta-colon':[
      include('spaces'),
      (
       ':', Name.Decorator, '#pop'),
      default('#pop')], 
     'meta-ident':[
      include('spaces'),
      (
       ident, Name.Decorator, '#pop')], 
     'meta-body':[
      include('spaces'),
      (
       '\\(', Name.Decorator, ('#pop', 'meta-call')),
      default('#pop')], 
     'meta-call':[
      include('spaces'),
      (
       '\\)', Name.Decorator, '#pop'),
      default(('#pop', 'meta-call-sep', 'expr'))], 
     'meta-call-sep':[
      include('spaces'),
      (
       '\\)', Name.Decorator, '#pop'),
      (
       ',', Punctuation, ('#pop', 'meta-call'))], 
     'typedef':[
      include('spaces'),
      default(('#pop', 'typedef-body', 'type-param-constraint', 'type-name'))], 
     'typedef-body':[
      include('spaces'),
      (
       '=', Operator, ('#pop', 'optional-semicolon', 'type'))], 
     'enum':[
      include('spaces'),
      default(('#pop', 'enum-body', 'bracket-open', 'type-param-constraint', 'type-name'))], 
     'enum-body':[
      include('spaces'),
      include('meta'),
      (
       '\\}', Punctuation, '#pop'),
      (
       ident_no_keyword, Name, ('enum-member', 'type-param-constraint'))], 
     'enum-member':[
      include('spaces'),
      (
       '\\(', Punctuation,
       ('#pop', 'semicolon', 'flag', 'function-param')),
      default(('#pop', 'semicolon', 'flag'))], 
     'class':[
      include('spaces'),
      default(('#pop', 'class-body', 'bracket-open', 'extends', 'type-param-constraint',
         'type-name'))], 
     'extends':[
      include('spaces'),
      (
       '(?:extends|implements)\\b', Keyword.Declaration, 'type'),
      (
       ',', Punctuation),
      default('#pop')], 
     'bracket-open':[
      include('spaces'),
      (
       '\\{', Punctuation, '#pop')], 
     'bracket-close':[
      include('spaces'),
      (
       '\\}', Punctuation, '#pop')], 
     'class-body':[
      include('spaces'),
      include('meta'),
      (
       '\\}', Punctuation, '#pop'),
      (
       '(?:static|public|private|override|dynamic|inline|macro)\\b',
       Keyword.Declaration),
      default('class-member')], 
     'class-member':[
      include('spaces'),
      (
       '(var)\\b', Keyword.Declaration,
       ('#pop', 'optional-semicolon', 'var')),
      (
       '(function)\\b', Keyword.Declaration,
       ('#pop', 'optional-semicolon', 'class-method'))], 
     'function-local':[
      include('spaces'),
      (
       ident_no_keyword, Name.Function,
       ('#pop', 'optional-expr', 'flag', 'function-param', 'parenthesis-open', 'type-param-constraint')),
      default(('#pop', 'optional-expr', 'flag', 'function-param', 'parenthesis-open', 'type-param-constraint'))], 
     'optional-expr':[
      include('spaces'),
      include('expr'),
      default('#pop')], 
     'class-method':[
      include('spaces'),
      (
       ident, Name.Function,
       ('#pop', 'optional-expr', 'flag', 'function-param', 'parenthesis-open', 'type-param-constraint'))], 
     'function-param':[
      include('spaces'),
      (
       '\\)', Punctuation, '#pop'),
      (
       '\\?', Punctuation),
      (
       ident_no_keyword, Name,
       ('#pop', 'function-param-sep', 'assign', 'flag'))], 
     'function-param-sep':[
      include('spaces'),
      (
       '\\)', Punctuation, '#pop'),
      (
       ',', Punctuation, ('#pop', 'function-param'))], 
     'prop-get-set':[
      include('spaces'),
      (
       '\\(', Punctuation,
       ('#pop', 'parenthesis-close', 'prop-get-set-opt', 'comma', 'prop-get-set-opt')),
      default('#pop')], 
     'prop-get-set-opt':[
      include('spaces'),
      (
       '(?:default|null|never|dynamic|get|set)\\b', Keyword, '#pop'),
      (
       ident_no_keyword, Text, '#pop')], 
     'expr-statement':[
      include('spaces'),
      default(('#pop', 'optional-semicolon', 'expr'))], 
     'expr':[
      include('spaces'),
      (
       '@', Name.Decorator,
       ('#pop', 'optional-expr', 'meta-body', 'meta-ident', 'meta-colon')),
      (
       '(?:\\+\\+|\\-\\-|~(?!/)|!|\\-)', Operator),
      (
       '\\(', Punctuation, ('#pop', 'expr-chain', 'parenthesis')),
      (
       '(?:static|public|private|override|dynamic|inline)\\b',
       Keyword.Declaration),
      (
       '(?:function)\\b', Keyword.Declaration,
       ('#pop', 'expr-chain', 'function-local')),
      (
       '\\{', Punctuation, ('#pop', 'expr-chain', 'bracket')),
      (
       '(?:true|false|null)\\b', Keyword.Constant, ('#pop', 'expr-chain')),
      (
       '(?:this)\\b', Keyword, ('#pop', 'expr-chain')),
      (
       '(?:cast)\\b', Keyword, ('#pop', 'expr-chain', 'cast')),
      (
       '(?:try)\\b', Keyword, ('#pop', 'catch', 'expr')),
      (
       '(?:var)\\b', Keyword.Declaration, ('#pop', 'var')),
      (
       '(?:new)\\b', Keyword, ('#pop', 'expr-chain', 'new')),
      (
       '(?:switch)\\b', Keyword, ('#pop', 'switch')),
      (
       '(?:if)\\b', Keyword, ('#pop', 'if')),
      (
       '(?:do)\\b', Keyword, ('#pop', 'do')),
      (
       '(?:while)\\b', Keyword, ('#pop', 'while')),
      (
       '(?:for)\\b', Keyword, ('#pop', 'for')),
      (
       '(?:untyped|throw)\\b', Keyword),
      (
       '(?:return)\\b', Keyword, ('#pop', 'optional-expr')),
      (
       '(?:macro)\\b', Keyword, ('#pop', 'macro')),
      (
       '(?:continue|break)\\b', Keyword, '#pop'),
      (
       '(?:\\$\\s*[a-z]\\b|\\$(?!' + ident + '))', Name, ('#pop', 'dollar')),
      (
       ident_no_keyword, Name, ('#pop', 'expr-chain')),
      (
       '\\.[0-9]+', Number.Float, ('#pop', 'expr-chain')),
      (
       '[0-9]+[eE][+\\-]?[0-9]+', Number.Float, ('#pop', 'expr-chain')),
      (
       '[0-9]+\\.[0-9]*[eE][+\\-]?[0-9]+', Number.Float, ('#pop', 'expr-chain')),
      (
       '[0-9]+\\.[0-9]+', Number.Float, ('#pop', 'expr-chain')),
      (
       '[0-9]+\\.(?!' + ident + '|\\.\\.)', Number.Float, ('#pop', 'expr-chain')),
      (
       '0x[0-9a-fA-F]+', Number.Hex, ('#pop', 'expr-chain')),
      (
       '[0-9]+', Number.Integer, ('#pop', 'expr-chain')),
      (
       "'", String.Single, ('#pop', 'expr-chain', 'string-single-interpol')),
      (
       '"', String.Double, ('#pop', 'expr-chain', 'string-double')),
      (
       '~/(\\\\\\\\|\\\\/|[^/\\n])*/[gimsu]*', String.Regex, ('#pop', 'expr-chain')),
      (
       '\\[', Punctuation, ('#pop', 'expr-chain', 'array-decl'))], 
     'expr-chain':[
      include('spaces'),
      (
       '(?:\\+\\+|\\-\\-)', Operator),
      (
       binop, Operator, ('#pop', 'expr')),
      (
       '(?:in)\\b', Keyword, ('#pop', 'expr')),
      (
       '\\?', Operator, ('#pop', 'expr', 'ternary', 'expr')),
      (
       '(\\.)(' + ident_no_keyword + ')', bygroups(Punctuation, Name)),
      (
       '\\[', Punctuation, 'array-access'),
      (
       '\\(', Punctuation, 'call'),
      default('#pop')], 
     'macro':[
      include('spaces'),
      include('meta'),
      (
       ':', Punctuation, ('#pop', 'type')),
      (
       '(?:extern|private)\\b', Keyword.Declaration),
      (
       '(?:abstract)\\b', Keyword.Declaration, ('#pop', 'optional-semicolon', 'abstract')),
      (
       '(?:class|interface)\\b', Keyword.Declaration, ('#pop', 'optional-semicolon', 'macro-class')),
      (
       '(?:enum)\\b', Keyword.Declaration, ('#pop', 'optional-semicolon', 'enum')),
      (
       '(?:typedef)\\b', Keyword.Declaration, ('#pop', 'optional-semicolon', 'typedef')),
      default(('#pop', 'expr'))], 
     'macro-class':[
      (
       '\\{', Punctuation, ('#pop', 'class-body')),
      include('class')], 
     'cast':[
      include('spaces'),
      (
       '\\(', Punctuation,
       ('#pop', 'parenthesis-close', 'cast-type', 'expr')),
      default(('#pop', 'expr'))], 
     'cast-type':[
      include('spaces'),
      (
       ',', Punctuation, ('#pop', 'type')),
      default('#pop')], 
     'catch':[
      include('spaces'),
      (
       '(?:catch)\\b', Keyword,
       ('expr', 'function-param', 'parenthesis-open')),
      default('#pop')], 
     'do':[
      include('spaces'),
      default(('#pop', 'do-while', 'expr'))], 
     'do-while':[
      include('spaces'),
      (
       '(?:while)\\b', Keyword,
       ('#pop', 'parenthesis', 'parenthesis-open'))], 
     'while':[
      include('spaces'),
      (
       '\\(', Punctuation, ('#pop', 'expr', 'parenthesis'))], 
     'for':[
      include('spaces'),
      (
       '\\(', Punctuation, ('#pop', 'expr', 'parenthesis'))], 
     'if':[
      include('spaces'),
      (
       '\\(', Punctuation,
       ('#pop', 'else', 'optional-semicolon', 'expr', 'parenthesis'))], 
     'else':[
      include('spaces'),
      (
       '(?:else)\\b', Keyword, ('#pop', 'expr')),
      default('#pop')], 
     'switch':[
      include('spaces'),
      default(('#pop', 'switch-body', 'bracket-open', 'expr'))], 
     'switch-body':[
      include('spaces'),
      (
       '(?:case|default)\\b', Keyword, ('case-block', 'case')),
      (
       '\\}', Punctuation, '#pop')], 
     'case':[
      include('spaces'),
      (
       ':', Punctuation, '#pop'),
      default(('#pop', 'case-sep', 'case-guard', 'expr'))], 
     'case-sep':[
      include('spaces'),
      (
       ':', Punctuation, '#pop'),
      (
       ',', Punctuation, ('#pop', 'case'))], 
     'case-guard':[
      include('spaces'),
      (
       '(?:if)\\b', Keyword, ('#pop', 'parenthesis', 'parenthesis-open')),
      default('#pop')], 
     'case-block':[
      include('spaces'),
      (
       '(?!(?:case|default)\\b|\\})', Keyword, 'expr-statement'),
      default('#pop')], 
     'new':[
      include('spaces'),
      default(('#pop', 'call', 'parenthesis-open', 'type'))], 
     'array-decl':[
      include('spaces'),
      (
       '\\]', Punctuation, '#pop'),
      default(('#pop', 'array-decl-sep', 'expr'))], 
     'array-decl-sep':[
      include('spaces'),
      (
       '\\]', Punctuation, '#pop'),
      (
       ',', Punctuation, ('#pop', 'array-decl'))], 
     'array-access':[
      include('spaces'),
      default(('#pop', 'array-access-close', 'expr'))], 
     'array-access-close':[
      include('spaces'),
      (
       '\\]', Punctuation, '#pop')], 
     'comma':[
      include('spaces'),
      (
       ',', Punctuation, '#pop')], 
     'colon':[
      include('spaces'),
      (
       ':', Punctuation, '#pop')], 
     'semicolon':[
      include('spaces'),
      (
       ';', Punctuation, '#pop')], 
     'optional-semicolon':[
      include('spaces'),
      (
       ';', Punctuation, '#pop'),
      default('#pop')], 
     'ident':[
      include('spaces'),
      (
       ident, Name, '#pop')], 
     'dollar':[
      include('spaces'),
      (
       '\\{', Punctuation, ('#pop', 'expr-chain', 'bracket-close', 'expr')),
      default(('#pop', 'expr-chain'))], 
     'type-name':[
      include('spaces'),
      (
       typeid, Name, '#pop')], 
     'type-full-name':[
      include('spaces'),
      (
       '\\.', Punctuation, 'ident'),
      default('#pop')], 
     'type':[
      include('spaces'),
      (
       '\\?', Punctuation),
      (
       ident, Name, ('#pop', 'type-check', 'type-full-name')),
      (
       '\\{', Punctuation, ('#pop', 'type-check', 'type-struct')),
      (
       '\\(', Punctuation, ('#pop', 'type-check', 'type-parenthesis'))], 
     'type-parenthesis':[
      include('spaces'),
      default(('#pop', 'parenthesis-close', 'type'))], 
     'type-check':[
      include('spaces'),
      (
       '->', Punctuation, ('#pop', 'type')),
      (
       '<(?!=)', Punctuation, 'type-param'),
      default('#pop')], 
     'type-struct':[
      include('spaces'),
      (
       '\\}', Punctuation, '#pop'),
      (
       '\\?', Punctuation),
      (
       '>', Punctuation, ('comma', 'type')),
      (
       ident_no_keyword, Name, ('#pop', 'type-struct-sep', 'type', 'colon')),
      include('class-body')], 
     'type-struct-sep':[
      include('spaces'),
      (
       '\\}', Punctuation, '#pop'),
      (
       ',', Punctuation, ('#pop', 'type-struct'))], 
     'type-param-type':[
      (
       '\\.[0-9]+', Number.Float, '#pop'),
      (
       '[0-9]+[eE][+\\-]?[0-9]+', Number.Float, '#pop'),
      (
       '[0-9]+\\.[0-9]*[eE][+\\-]?[0-9]+', Number.Float, '#pop'),
      (
       '[0-9]+\\.[0-9]+', Number.Float, '#pop'),
      (
       '[0-9]+\\.(?!' + ident + '|\\.\\.)', Number.Float, '#pop'),
      (
       '0x[0-9a-fA-F]+', Number.Hex, '#pop'),
      (
       '[0-9]+', Number.Integer, '#pop'),
      (
       "'", String.Single, ('#pop', 'string-single')),
      (
       '"', String.Double, ('#pop', 'string-double')),
      (
       '~/(\\\\\\\\|\\\\/|[^/\\n])*/[gim]*', String.Regex, '#pop'),
      (
       '\\[', Operator, ('#pop', 'array-decl')),
      include('type')], 
     'type-param':[
      include('spaces'),
      default(('#pop', 'type-param-sep', 'type-param-type'))], 
     'type-param-sep':[
      include('spaces'),
      (
       '>', Punctuation, '#pop'),
      (
       ',', Punctuation, ('#pop', 'type-param'))], 
     'type-param-constraint':[
      include('spaces'),
      (
       '<(?!=)', Punctuation,
       ('#pop', 'type-param-constraint-sep', 'type-param-constraint-flag', 'type-name')),
      default('#pop')], 
     'type-param-constraint-sep':[
      include('spaces'),
      (
       '>', Punctuation, '#pop'),
      (
       ',', Punctuation,
       ('#pop', 'type-param-constraint-sep', 'type-param-constraint-flag', 'type-name'))], 
     'type-param-constraint-flag':[
      include('spaces'),
      (
       ':', Punctuation, ('#pop', 'type-param-constraint-flag-type')),
      default('#pop')], 
     'type-param-constraint-flag-type':[
      include('spaces'),
      (
       '\\(', Punctuation,
       ('#pop', 'type-param-constraint-flag-type-sep', 'type')),
      default(('#pop', 'type'))], 
     'type-param-constraint-flag-type-sep':[
      include('spaces'),
      (
       '\\)', Punctuation, '#pop'),
      (
       ',', Punctuation, 'type')], 
     'parenthesis':[
      include('spaces'),
      default(('#pop', 'parenthesis-close', 'flag', 'expr'))], 
     'parenthesis-open':[
      include('spaces'),
      (
       '\\(', Punctuation, '#pop')], 
     'parenthesis-close':[
      include('spaces'),
      (
       '\\)', Punctuation, '#pop')], 
     'var':[
      include('spaces'),
      (
       ident_no_keyword, Text, ('#pop', 'var-sep', 'assign', 'flag', 'prop-get-set'))], 
     'var-sep':[
      include('spaces'),
      (
       ',', Punctuation, ('#pop', 'var')),
      default('#pop')], 
     'assign':[
      include('spaces'),
      (
       '=', Operator, ('#pop', 'expr')),
      default('#pop')], 
     'flag':[
      include('spaces'),
      (
       ':', Punctuation, ('#pop', 'type')),
      default('#pop')], 
     'ternary':[
      include('spaces'),
      (
       ':', Operator, '#pop')], 
     'call':[
      include('spaces'),
      (
       '\\)', Punctuation, '#pop'),
      default(('#pop', 'call-sep', 'expr'))], 
     'call-sep':[
      include('spaces'),
      (
       '\\)', Punctuation, '#pop'),
      (
       ',', Punctuation, ('#pop', 'call'))], 
     'bracket':[
      include('spaces'),
      (
       '(?!(?:\\$\\s*[a-z]\\b|\\$(?!' + ident + ')))' + ident_no_keyword, Name,
       ('#pop', 'bracket-check')),
      (
       "'", String.Single, ('#pop', 'bracket-check', 'string-single')),
      (
       '"', String.Double, ('#pop', 'bracket-check', 'string-double')),
      default(('#pop', 'block'))], 
     'bracket-check':[
      include('spaces'),
      (
       ':', Punctuation, ('#pop', 'object-sep', 'expr')),
      default(('#pop', 'block', 'optional-semicolon', 'expr-chain'))], 
     'block':[
      include('spaces'),
      (
       '\\}', Punctuation, '#pop'),
      default('expr-statement')], 
     'object':[
      include('spaces'),
      (
       '\\}', Punctuation, '#pop'),
      default(('#pop', 'object-sep', 'expr', 'colon', 'ident-or-string'))], 
     'ident-or-string':[
      include('spaces'),
      (
       ident_no_keyword, Name, '#pop'),
      (
       "'", String.Single, ('#pop', 'string-single')),
      (
       '"', String.Double, ('#pop', 'string-double'))], 
     'object-sep':[
      include('spaces'),
      (
       '\\}', Punctuation, '#pop'),
      (
       ',', Punctuation, ('#pop', 'object'))]}

    def analyse_text(text):
        if re.match('\\w+\\s*:\\s*\\w', text):
            return 0.3


class HxmlLexer(RegexLexer):
    __doc__ = '\n    Lexer for `haXe build <http://haxe.org/doc/compiler>`_ files.\n\n    .. versionadded:: 1.6\n    '
    name = 'Hxml'
    aliases = ['haxeml', 'hxml']
    filenames = ['*.hxml']
    tokens = {'root': [
              (
               '(--)(next)', bygroups(Punctuation, Generic.Heading)),
              (
               '(-)(prompt|debug|v)', bygroups(Punctuation, Keyword.Keyword)),
              (
               '(--)(neko-source|flash-strict|flash-use-stage|no-opt|no-traces|no-inline|times|no-output)',
               bygroups(Punctuation, Keyword)),
              (
               '(-)(cpp|js|neko|x|as3|swf9?|swf-lib|php|xml|main|lib|D|resource|cp|cmd)( +)(.+)',
               bygroups(Punctuation, Keyword, Whitespace, String)),
              (
               '(-)(swf-version)( +)(\\d+)',
               bygroups(Punctuation, Keyword, Number.Integer)),
              (
               '(-)(swf-header)( +)(\\d+)(:)(\\d+)(:)(\\d+)(:)([A-Fa-f0-9]{6})',
               bygroups(Punctuation, Keyword, Whitespace, Number.Integer, Punctuation, Number.Integer, Punctuation, Number.Integer, Punctuation, Number.Hex)),
              (
               '(--)(js-namespace|php-front|php-lib|remap|gen-hx-classes)( +)(.+)',
               bygroups(Punctuation, Keyword, Whitespace, String)),
              (
               '#.*', Comment.Single)]}