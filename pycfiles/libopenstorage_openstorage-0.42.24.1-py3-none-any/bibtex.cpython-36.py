# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/bibtex.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 4725 bytes
"""
    pygments.lexers.bibtex
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for BibTeX bibliography data and styles

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, ExtendedRegexLexer, include, default, words
from pygments.token import Name, Comment, String, Error, Number, Text, Keyword, Punctuation
__all__ = [
 'BibTeXLexer', 'BSTLexer']

class BibTeXLexer(ExtendedRegexLexer):
    __doc__ = '\n    A lexer for BibTeX bibliography data format.\n\n    .. versionadded:: 2.2\n    '
    name = 'BibTeX'
    aliases = ['bib', 'bibtex']
    filenames = ['*.bib']
    mimetypes = ['text/x-bibtex']
    flags = re.IGNORECASE
    ALLOWED_CHARS = '@!$&*+\\-./:;<>?\\[\\\\\\]^`|~'
    IDENTIFIER = '[{}][{}]*'.format('a-z_' + ALLOWED_CHARS, '\\w' + ALLOWED_CHARS)

    def open_brace_callback(self, match, ctx):
        opening_brace = match.group()
        ctx.opening_brace = opening_brace
        yield (match.start(), Punctuation, opening_brace)
        ctx.pos = match.end()

    def close_brace_callback(self, match, ctx):
        closing_brace = match.group()
        if ctx.opening_brace == '{' and closing_brace != '}' or ctx.opening_brace == '(' and closing_brace != ')':
            yield (match.start(), Error, closing_brace)
        else:
            yield (
             match.start(), Punctuation, closing_brace)
        del ctx.opening_brace
        ctx.pos = match.end()

    tokens = {'root':[
      include('whitespace'),
      (
       '@comment', Comment),
      (
       '@preamble', Name.Class, ('closing-brace', 'value', 'opening-brace')),
      (
       '@string', Name.Class, ('closing-brace', 'field', 'opening-brace')),
      (
       '@' + IDENTIFIER, Name.Class,
       ('closing-brace', 'command-body', 'opening-brace')),
      (
       '.+', Comment)], 
     'opening-brace':[
      include('whitespace'),
      (
       '[{(]', open_brace_callback, '#pop')], 
     'closing-brace':[
      include('whitespace'),
      (
       '[})]', close_brace_callback, '#pop')], 
     'command-body':[
      include('whitespace'),
      (
       '[^\\s\\,\\}]+', Name.Label, ('#pop', 'fields'))], 
     'fields':[
      include('whitespace'),
      (
       ',', Punctuation, 'field'),
      default('#pop')], 
     'field':[
      include('whitespace'),
      (
       IDENTIFIER, Name.Attribute, ('value', '=')),
      default('#pop')], 
     '=':[
      include('whitespace'),
      (
       '=', Punctuation, '#pop')], 
     'value':[
      include('whitespace'),
      (
       IDENTIFIER, Name.Variable),
      (
       '"', String, 'quoted-string'),
      (
       '\\{', String, 'braced-string'),
      (
       '[\\d]+', Number),
      (
       '#', Punctuation),
      default('#pop')], 
     'quoted-string':[
      (
       '\\{', String, 'braced-string'),
      (
       '"', String, '#pop'),
      (
       '[^\\{\\"]+', String)], 
     'braced-string':[
      (
       '\\{', String, '#push'),
      (
       '\\}', String, '#pop'),
      (
       '[^\\{\\}]+', String)], 
     'whitespace':[
      (
       '\\s+', Text)]}


class BSTLexer(RegexLexer):
    __doc__ = '\n    A lexer for BibTeX bibliography styles.\n\n    .. versionadded:: 2.2\n    '
    name = 'BST'
    aliases = ['bst', 'bst-pybtex']
    filenames = ['*.bst']
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'root':[
      include('whitespace'),
      (
       words(['read', 'sort']), Keyword),
      (
       words(['execute', 'integers', 'iterate', 'reverse', 'strings']),
       Keyword, 'group'),
      (
       words(['function', 'macro']), Keyword, ('group', 'group')),
      (
       words(['entry']), Keyword, ('group', 'group', 'group'))], 
     'group':[
      include('whitespace'),
      (
       '\\{', Punctuation, ('#pop', 'group-end', 'body'))], 
     'group-end':[
      include('whitespace'),
      (
       '\\}', Punctuation, '#pop')], 
     'body':[
      include('whitespace'),
      (
       '\\\'[^#\\"\\{\\}\\s]+', Name.Function),
      (
       '[^#\\"\\{\\}\\s]+\\$', Name.Builtin),
      (
       '[^#\\"\\{\\}\\s]+', Name.Variable),
      (
       '"[^\\"]*"', String),
      (
       '#-?\\d+', Number),
      (
       '\\{', Punctuation, ('group-end', 'body')),
      default('#pop')], 
     'whitespace':[
      (
       '\\s+', Text),
      (
       '%.*?$', Comment.SingleLine)]}