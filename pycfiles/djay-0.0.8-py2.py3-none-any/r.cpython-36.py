# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/r.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 6279 bytes
"""
    pygments.lexers.r
    ~~~~~~~~~~~~~~~~~

    Lexers for the R/S languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, include, do_insertions, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic
__all__ = [
 'RConsoleLexer', 'SLexer', 'RdLexer']
line_re = re.compile('.*?\n')

class RConsoleLexer(Lexer):
    __doc__ = '\n    For R console transcripts or R CMD BATCH output files.\n    '
    name = 'RConsole'
    aliases = ['rconsole', 'rout']
    filenames = ['*.Rout']

    def get_tokens_unprocessed(self, text):
        slexer = SLexer(**self.options)
        current_code_block = ''
        insertions = []
        for match in line_re.finditer(text):
            line = match.group()
            if line.startswith('>') or line.startswith('+'):
                insertions.append((len(current_code_block),
                 [
                  (
                   0, Generic.Prompt, line[:2])]))
                current_code_block += line[2:]
            else:
                if current_code_block:
                    for item in do_insertions(insertions, slexer.get_tokens_unprocessed(current_code_block)):
                        yield item

                    current_code_block = ''
                    insertions = []
                yield (match.start(), Generic.Output, line)

        if current_code_block:
            for item in do_insertions(insertions, slexer.get_tokens_unprocessed(current_code_block)):
                yield item


class SLexer(RegexLexer):
    __doc__ = '\n    For S, S-plus, and R source code.\n\n    .. versionadded:: 0.10\n    '
    name = 'S'
    aliases = ['splus', 's', 'r']
    filenames = ['*.S', '*.R', '.Rhistory', '.Rprofile', '.Renviron']
    mimetypes = ['text/S-plus', 'text/S', 'text/x-r-source', 'text/x-r',
     'text/x-R', 'text/x-r-history', 'text/x-r-profile']
    valid_name = '(?:`[^`\\\\]*(?:\\\\.[^`\\\\]*)*`)|(?:(?:[a-zA-z]|[_.][^0-9])[\\w_.]*)'
    tokens = {'comments':[
      (
       '#.*$', Comment.Single)], 
     'valid_name':[
      (
       valid_name, Name)], 
     'punctuation':[
      (
       '\\[{1,2}|\\]{1,2}|\\(|\\)|;|,', Punctuation)], 
     'keywords':[
      (
       '(if|else|for|while|repeat|in|next|break|return|switch|function)(?![\\w.])',
       Keyword.Reserved)], 
     'operators':[
      (
       '<<?-|->>?|-|==|<=|>=|<|>|&&?|!=|\\|\\|?|\\?', Operator),
      (
       '\\*|\\+|\\^|/|!|%[^%]*%|=|~|\\$|@|:{1,3}', Operator)], 
     'builtin_symbols':[
      (
       '(NULL|NA(_(integer|real|complex|character)_)?|letters|LETTERS|Inf|TRUE|FALSE|NaN|pi|\\.\\.(\\.|[0-9]+))(?![\\w.])',
       Keyword.Constant),
      (
       '(T|F)\\b', Name.Builtin.Pseudo)], 
     'numbers':[
      (
       '0[xX][a-fA-F0-9]+([pP][0-9]+)?[Li]?', Number.Hex),
      (
       '[+-]?([0-9]+(\\.[0-9]+)?|\\.[0-9]+|\\.)([eE][+-]?[0-9]+)?[Li]?',
       Number)], 
     'statements':[
      include('comments'),
      (
       '\\s+', Text),
      (
       "\\'", String, 'string_squote'),
      (
       '\\"', String, 'string_dquote'),
      include('builtin_symbols'),
      include('valid_name'),
      include('numbers'),
      include('keywords'),
      include('punctuation'),
      include('operators')], 
     'root':[
      (
       '(%s)\\s*(?=\\()' % valid_name, Name.Function),
      include('statements'),
      (
       '\\{|\\}', Punctuation),
      (
       '.', Text)], 
     'string_squote':[
      (
       "([^\\'\\\\]|\\\\.)*\\'", String, '#pop')], 
     'string_dquote':[
      (
       '([^"\\\\]|\\\\.)*"', String, '#pop')]}

    def analyse_text(text):
        if re.search('[a-z0-9_\\])\\s]<-(?!-)', text):
            return 0.11


class RdLexer(RegexLexer):
    __doc__ = '\n    Pygments Lexer for R documentation (Rd) files\n\n    This is a very minimal implementation, highlighting little more\n    than the macros. A description of Rd syntax is found in `Writing R\n    Extensions <http://cran.r-project.org/doc/manuals/R-exts.html>`_\n    and `Parsing Rd files <http://developer.r-project.org/parseRd.pdf>`_.\n\n    .. versionadded:: 1.6\n    '
    name = 'Rd'
    aliases = ['rd']
    filenames = ['*.Rd']
    mimetypes = ['text/x-r-doc']
    tokens = {'root': [
              (
               '\\\\[\\\\{}%]', String.Escape),
              (
               '%.*$', Comment),
              (
               '\\\\(?:cr|l?dots|R|tab)\\b', Keyword.Constant),
              (
               '\\\\[a-zA-Z]+\\b', Keyword),
              (
               '^\\s*#(?:ifn?def|endif).*\\b', Comment.Preproc),
              (
               '[{}]', Name.Builtin),
              (
               '[^\\\\%\\n{}]+', Text),
              (
               '.', Text)]}