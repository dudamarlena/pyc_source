# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/textedit.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 6057 bytes
"""
    pygments.lexers.textedit
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for languages related to text processing.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from bisect import bisect
from pygments.lexer import RegexLexer, include, default, bygroups, using, this
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
from pygments.lexers.python import PythonLexer
__all__ = [
 'AwkLexer', 'VimLexer']

class AwkLexer(RegexLexer):
    __doc__ = '\n    For Awk scripts.\n\n    .. versionadded:: 1.5\n    '
    name = 'Awk'
    aliases = ['awk', 'gawk', 'mawk', 'nawk']
    filenames = ['*.awk']
    mimetypes = ['application/x-awk']
    tokens = {'commentsandwhitespace':[
      (
       '\\s+', Text),
      (
       '#.*$', Comment.Single)], 
     'slashstartsregex':[
      include('commentsandwhitespace'),
      (
       '/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/\\B',
       String.Regex, '#pop'),
      (
       '(?=/)', Text, ('#pop', 'badregex')),
      default('#pop')], 
     'badregex':[
      (
       '\\n', Text, '#pop')], 
     'root':[
      (
       '^(?=\\s|/)', Text, 'slashstartsregex'),
      include('commentsandwhitespace'),
      (
       '\\+\\+|--|\\|\\||&&|in\\b|\\$|!?~|(\\*\\*|[-<>+*%\\^/!=|])=?',
       Operator, 'slashstartsregex'),
      (
       '[{(\\[;,]', Punctuation, 'slashstartsregex'),
      (
       '[})\\].]', Punctuation),
      (
       '(break|continue|do|while|exit|for|if|else|return)\\b',
       Keyword, 'slashstartsregex'),
      (
       'function\\b', Keyword.Declaration, 'slashstartsregex'),
      (
       '(atan2|cos|exp|int|log|rand|sin|sqrt|srand|gensub|gsub|index|length|match|split|sprintf|sub|substr|tolower|toupper|close|fflush|getline|next|nextfile|print|printf|strftime|systime|delete|system)\\b',
       Keyword.Reserved),
      (
       '(ARGC|ARGIND|ARGV|BEGIN|CONVFMT|ENVIRON|END|ERRNO|FIELDWIDTHS|FILENAME|FNR|FS|IGNORECASE|NF|NR|OFMT|OFS|ORFS|RLENGTH|RS|RSTART|RT|SUBSEP)\\b',
       Name.Builtin),
      (
       '[$a-zA-Z_]\\w*', Name.Other),
      (
       '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+', Number.Integer),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
      (
       "'(\\\\\\\\|\\\\'|[^'])*'", String.Single)]}


class VimLexer(RegexLexer):
    __doc__ = '\n    Lexer for VimL script files.\n\n    .. versionadded:: 0.8\n    '
    name = 'VimL'
    aliases = ['vim']
    filenames = ['*.vim', '.vimrc', '.exrc', '.gvimrc',
     '_vimrc', '_exrc', '_gvimrc', 'vimrc', 'gvimrc']
    mimetypes = ['text/x-vim']
    flags = re.MULTILINE
    _python = 'py(?:t(?:h(?:o(?:n)?)?)?)?'
    tokens = {'root': [
              (
               '^([ \\t:]*)(' + _python + ')([ \\t]*)(<<)([ \\t]*)(.*)((?:\\n|.)*)(\\6)',
               bygroups(using(this), Keyword, Text, Operator, Text, Text, using(PythonLexer), Text)),
              (
               '^([ \\t:]*)(' + _python + ')([ \\t])(.*)',
               bygroups(using(this), Keyword, Text, using(PythonLexer))),
              (
               '^\\s*".*', Comment),
              (
               '[ \\t]+', Text),
              (
               '/(\\\\\\\\|\\\\/|[^\\n/])*/', String.Regex),
              (
               '"(\\\\\\\\|\\\\"|[^\\n"])*"', String.Double),
              (
               "'(''|[^\\n'])*'", String.Single),
              (
               '(?<=\\s)"[^\\-:.%#=*].*', Comment),
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
        from pygments.lexers._vim_builtins import command, option, auto
        self._cmd = command
        self._opt = option
        self._aut = auto
        (RegexLexer.__init__)(self, **options)

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
            if mapping[(p - 1)][0] == w[:len(mapping[(p - 1)][0])]:
                if mapping[(p - 1)][1][:len(w)] == w:
                    return True
        if p < len(mapping):
            return mapping[p][0] == w[:len(mapping[p][0])] and mapping[p][1][:len(w)] == w
        else:
            return False

    def get_tokens_unprocessed(self, text):
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name.Other:
                if self.is_in(value, self._cmd):
                    yield (
                     index, Keyword, value)
                else:
                    if self.is_in(value, self._opt) or self.is_in(value, self._aut):
                        yield (
                         index, Name.Builtin, value)
                    else:
                        yield (
                         index, Text, value)
            else:
                yield (
                 index, token, value)