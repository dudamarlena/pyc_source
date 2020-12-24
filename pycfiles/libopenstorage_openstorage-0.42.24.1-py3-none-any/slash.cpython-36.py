# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/slash.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 8522 bytes
"""
    pygments.lexers.slash
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for the `Slash <https://github.com/arturadib/Slash-A>`_ programming
    language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import ExtendedRegexLexer, bygroups, DelegatingLexer
from pygments.token import Name, Number, String, Comment, Punctuation, Other, Keyword, Operator, Whitespace
__all__ = [
 'SlashLexer']

class SlashLanguageLexer(ExtendedRegexLexer):
    _nkw = '(?=[^a-zA-Z_0-9])'

    def move_state(new_state):
        return (
         '#pop', new_state)

    def right_angle_bracket(lexer, match, ctx):
        if len(ctx.stack) > 1:
            if ctx.stack[(-2)] == 'string':
                ctx.stack.pop()
        yield (
         match.start(), String.Interpol, '}')
        ctx.pos = match.end()

    tokens = {'root':[
      (
       '<%=', Comment.Preproc, move_state('slash')),
      (
       '<%!!', Comment.Preproc, move_state('slash')),
      (
       '<%#.*?%>', Comment.Multiline),
      (
       '<%', Comment.Preproc, move_state('slash')),
      (
       '.|\\n', Other)], 
     'string':[
      (
       '\\\\', String.Escape, move_state('string_e')),
      (
       '\\"', String, move_state('slash')),
      (
       '#\\{', String.Interpol, 'slash'),
      (
       '.|\\n', String)], 
     'string_e':[
      (
       'n', String.Escape, move_state('string')),
      (
       't', String.Escape, move_state('string')),
      (
       'r', String.Escape, move_state('string')),
      (
       'e', String.Escape, move_state('string')),
      (
       'x[a-fA-F0-9]{2}', String.Escape, move_state('string')),
      (
       '.', String.Escape, move_state('string'))], 
     'regexp':[
      (
       '}[a-z]*', String.Regex, move_state('slash')),
      (
       '\\\\(.|\\n)', String.Regex),
      (
       '{', String.Regex, 'regexp_r'),
      (
       '.|\\n', String.Regex)], 
     'regexp_r':[
      (
       '}[a-z]*', String.Regex, '#pop'),
      (
       '\\\\(.|\\n)', String.Regex),
      (
       '{', String.Regex, 'regexp_r')], 
     'slash':[
      (
       '%>', Comment.Preproc, move_state('root')),
      (
       '\\"', String, move_state('string')),
      (
       "'[a-zA-Z0-9_]+", String),
      (
       '%r{', String.Regex, move_state('regexp')),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '(#|//).*?\\n', Comment.Single),
      (
       '-?[0-9]+e[+-]?[0-9]+', Number.Float),
      (
       '-?[0-9]+\\.[0-9]+(e[+-]?[0-9]+)?', Number.Float),
      (
       '-?[0-9]+', Number.Integer),
      (
       'nil' + _nkw, Name.Builtin),
      (
       'true' + _nkw, Name.Builtin),
      (
       'false' + _nkw, Name.Builtin),
      (
       'self' + _nkw, Name.Builtin),
      (
       "(class)(\\s+)([A-Z][a-zA-Z0-9_\\']*)",
       bygroups(Keyword, Whitespace, Name.Class)),
      (
       'class' + _nkw, Keyword),
      (
       'extends' + _nkw, Keyword),
      (
       "(def)(\\s+)(self)(\\s*)(\\.)(\\s*)([a-z_][a-zA-Z0-9_\\']*=?|<<|>>|==|<=>|<=|<|>=|>|\\+|-(self)?|~(self)?|\\*|/|%|^|&&|&|\\||\\[\\]=?)",
       bygroups(Keyword, Whitespace, Name.Builtin, Whitespace, Punctuation, Whitespace, Name.Function)),
      (
       "(def)(\\s+)([a-z_][a-zA-Z0-9_\\']*=?|<<|>>|==|<=>|<=|<|>=|>|\\+|-(self)?|~(self)?|\\*|/|%|^|&&|&|\\||\\[\\]=?)",
       bygroups(Keyword, Whitespace, Name.Function)),
      (
       'def' + _nkw, Keyword),
      (
       'if' + _nkw, Keyword),
      (
       'elsif' + _nkw, Keyword),
      (
       'else' + _nkw, Keyword),
      (
       'unless' + _nkw, Keyword),
      (
       'for' + _nkw, Keyword),
      (
       'in' + _nkw, Keyword),
      (
       'while' + _nkw, Keyword),
      (
       'until' + _nkw, Keyword),
      (
       'and' + _nkw, Keyword),
      (
       'or' + _nkw, Keyword),
      (
       'not' + _nkw, Keyword),
      (
       'lambda' + _nkw, Keyword),
      (
       'try' + _nkw, Keyword),
      (
       'catch' + _nkw, Keyword),
      (
       'return' + _nkw, Keyword),
      (
       'next' + _nkw, Keyword),
      (
       'last' + _nkw, Keyword),
      (
       'throw' + _nkw, Keyword),
      (
       'use' + _nkw, Keyword),
      (
       'switch' + _nkw, Keyword),
      (
       '\\\\', Keyword),
      (
       'λ', Keyword),
      (
       '__FILE__' + _nkw, Name.Builtin.Pseudo),
      (
       '__LINE__' + _nkw, Name.Builtin.Pseudo),
      (
       "[A-Z][a-zA-Z0-9_\\']*" + _nkw, Name.Constant),
      (
       "[a-z_][a-zA-Z0-9_\\']*" + _nkw, Name),
      (
       "@[a-z_][a-zA-Z0-9_\\']*" + _nkw, Name.Variable.Instance),
      (
       "@@[a-z_][a-zA-Z0-9_\\']*" + _nkw, Name.Variable.Class),
      (
       '\\(', Punctuation),
      (
       '\\)', Punctuation),
      (
       '\\[', Punctuation),
      (
       '\\]', Punctuation),
      (
       '\\{', Punctuation),
      (
       '\\}', right_angle_bracket),
      (
       ';', Punctuation),
      (
       ',', Punctuation),
      (
       '<<=', Operator),
      (
       '>>=', Operator),
      (
       '<<', Operator),
      (
       '>>', Operator),
      (
       '==', Operator),
      (
       '!=', Operator),
      (
       '=>', Operator),
      (
       '=', Operator),
      (
       '<=>', Operator),
      (
       '<=', Operator),
      (
       '>=', Operator),
      (
       '<', Operator),
      (
       '>', Operator),
      (
       '\\+\\+', Operator),
      (
       '\\+=', Operator),
      (
       '-=', Operator),
      (
       '\\*\\*=', Operator),
      (
       '\\*=', Operator),
      (
       '\\*\\*', Operator),
      (
       '\\*', Operator),
      (
       '/=', Operator),
      (
       '\\+', Operator),
      (
       '-', Operator),
      (
       '/', Operator),
      (
       '%=', Operator),
      (
       '%', Operator),
      (
       '^=', Operator),
      (
       '&&=', Operator),
      (
       '&=', Operator),
      (
       '&&', Operator),
      (
       '&', Operator),
      (
       '\\|\\|=', Operator),
      (
       '\\|=', Operator),
      (
       '\\|\\|', Operator),
      (
       '\\|', Operator),
      (
       '!', Operator),
      (
       '\\.\\.\\.', Operator),
      (
       '\\.\\.', Operator),
      (
       '\\.', Operator),
      (
       '::', Operator),
      (
       ':', Operator),
      (
       '(\\s|\\n)+', Whitespace),
      (
       "[a-z_][a-zA-Z0-9_\\']*", Name.Variable)]}


class SlashLexer(DelegatingLexer):
    __doc__ = '\n    Lexer for the Slash programming language.\n\n    .. versionadded:: 2.4\n    '
    name = 'Slash'
    aliases = ['slash']
    filenames = ['*.sl']

    def __init__(self, **options):
        from pygments.lexers.web import HtmlLexer
        (super(SlashLexer, self).__init__)(HtmlLexer, SlashLanguageLexer, **options)