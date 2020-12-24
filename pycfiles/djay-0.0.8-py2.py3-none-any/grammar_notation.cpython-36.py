# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/grammar_notation.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 6329 bytes
"""
    pygments.lexers.grammar_notation
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for grammer notations like BNF.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, bygroups, include, this, using, words
from pygments.token import Comment, Keyword, Literal, Name, Number, Operator, Punctuation, String, Text
__all__ = [
 'BnfLexer', 'AbnfLexer', 'JsgfLexer']

class BnfLexer(RegexLexer):
    __doc__ = "\n    This lexer is for grammer notations which are similar to\n    original BNF.\n\n    In order to maximize a number of targets of this lexer,\n    let's decide some designs:\n\n    * We don't distinguish `Terminal Symbol`.\n\n    * We do assume that `NonTerminal Symbol` are always enclosed\n      with arrow brackets.\n\n    * We do assume that `NonTerminal Symbol` may include\n      any printable characters except arrow brackets and ASCII 0x20.\n      This assumption is for `RBNF <http://www.rfc-base.org/txt/rfc-5511.txt>`_.\n\n    * We do assume that target notation doesn't support comment.\n\n    * We don't distinguish any operators and punctuation except\n      `::=`.\n\n    Though these desision making might cause too minimal highlighting\n    and you might be disappointed, but it is reasonable for us.\n\n    .. versionadded:: 2.1\n    "
    name = 'BNF'
    aliases = ['bnf']
    filenames = ['*.bnf']
    mimetypes = ['text/x-bnf']
    tokens = {'root': [
              (
               '(<)([ -;=?-~]+)(>)',
               bygroups(Punctuation, Name.Class, Punctuation)),
              (
               '::=', Operator),
              (
               '[^<>:]+', Text),
              (
               '.', Text)]}


class AbnfLexer(RegexLexer):
    __doc__ = '\n    Lexer for `IETF 7405 ABNF\n    <http://www.ietf.org/rfc/rfc7405.txt>`_\n    (Updates `5234 <http://www.ietf.org/rfc/rfc5234.txt>`_)\n    grammars.\n\n    .. versionadded:: 2.1\n    '
    name = 'ABNF'
    aliases = ['abnf']
    filenames = ['*.abnf']
    mimetypes = ['text/x-abnf']
    _core_rules = ('ALPHA', 'BIT', 'CHAR', 'CR', 'CRLF', 'CTL', 'DIGIT', 'DQUOTE',
                   'HEXDIG', 'HTAB', 'LF', 'LWSP', 'OCTET', 'SP', 'VCHAR', 'WSP')
    tokens = {'root': [
              (
               ';.*$', Comment.Single),
              (
               '(%[si])?"[^"]*"', Literal),
              (
               '%b[01]+\\-[01]+\\b', Literal),
              (
               '%b[01]+(\\.[01]+)*\\b', Literal),
              (
               '%d[0-9]+\\-[0-9]+\\b', Literal),
              (
               '%d[0-9]+(\\.[0-9]+)*\\b', Literal),
              (
               '%x[0-9a-fA-F]+\\-[0-9a-fA-F]+\\b', Literal),
              (
               '%x[0-9a-fA-F]+(\\.[0-9a-fA-F]+)*\\b', Literal),
              (
               '\\b[0-9]+\\*[0-9]+', Operator),
              (
               '\\b[0-9]+\\*', Operator),
              (
               '\\b[0-9]+', Operator),
              (
               '\\*', Operator),
              (
               words(_core_rules, suffix='\\b'), Keyword),
              (
               '[a-zA-Z][a-zA-Z0-9-]+\\b', Name.Class),
              (
               '(=/|=|/)', Operator),
              (
               '[\\[\\]()]', Punctuation),
              (
               '\\s+', Text),
              (
               '.', Text)]}


class JsgfLexer(RegexLexer):
    __doc__ = '\n    For `JSpeech Grammar Format <https://www.w3.org/TR/jsgf/>`_\n    grammars.\n\n    .. versionadded:: 2.2\n    '
    name = 'JSGF'
    aliases = ['jsgf']
    filenames = ['*.jsgf']
    mimetypes = ['application/jsgf', 'application/x-jsgf', 'text/jsgf']
    flags = re.MULTILINE | re.UNICODE
    tokens = {'root':[
      include('comments'),
      include('non-comments')], 
     'comments':[
      (
       '/\\*\\*(?!/)', Comment.Multiline, 'documentation comment'),
      (
       '/\\*[\\w\\W]*?\\*/', Comment.Multiline),
      (
       '//.*', Comment.Single)], 
     'non-comments':[
      (
       '\\A#JSGF[^;]*', Comment.Preproc),
      (
       '\\s+', Text),
      (
       ';', Punctuation),
      (
       '[=|()\\[\\]*+]', Operator),
      (
       '/[^/]+/', Number.Float),
      (
       '"', String.Double, 'string'),
      (
       '\\{', String.Other, 'tag'),
      (
       words(('import', 'public'), suffix='\\b'), Keyword.Reserved),
      (
       'grammar\\b', Keyword.Reserved, 'grammar name'),
      (
       '(<)(NULL|VOID)(>)',
       bygroups(Punctuation, Name.Builtin, Punctuation)),
      (
       '<', Punctuation, 'rulename'),
      (
       '\\w+|[^\\s;=|()\\[\\]*+/"{<\\w]+', Text)], 
     'string':[
      (
       '"', String.Double, '#pop'),
      (
       '\\\\.', String.Escape),
      (
       '[^\\\\"]+', String.Double)], 
     'tag':[
      (
       '\\}', String.Other, '#pop'),
      (
       '\\\\.', String.Escape),
      (
       '[^\\\\}]+', String.Other)], 
     'grammar name':[
      (
       ';', Punctuation, '#pop'),
      (
       '\\s+', Text),
      (
       '\\.', Punctuation),
      (
       '[^;\\s.]+', Name.Namespace)], 
     'rulename':[
      (
       '>', Punctuation, '#pop'),
      (
       '\\*', Punctuation),
      (
       '\\s+', Text),
      (
       '([^.>]+)(\\s*)(\\.)', bygroups(Name.Namespace, Text, Punctuation)),
      (
       '[^.>]+', Name.Constant)], 
     'documentation comment':[
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '(^\\s*\\*?\\s*)(@(?:example|see)\\s+)([\\w\\W]*?(?=(?:^\\s*\\*?\\s*@|\\*/)))',
       bygroups(Comment.Multiline, Comment.Special, using(this, state='example'))),
      (
       '(^\\s*\\*?\\s*)(@\\S*)',
       bygroups(Comment.Multiline, Comment.Special)),
      (
       '[^*\\n@]+|\\w|\\W', Comment.Multiline)], 
     'example':[
      (
       '\\n\\s*\\*', Comment.Multiline),
      include('non-comments'),
      (
       '.', Comment.Multiline)]}