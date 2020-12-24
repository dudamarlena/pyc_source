# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/solidity.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 3255 bytes
"""
    pygments.lexers.solidity
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Solidity.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, bygroups, include, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'SolidityLexer']

class SolidityLexer(RegexLexer):
    __doc__ = '\n    For Solidity source code.\n\n    .. versionadded:: 2.5\n    '
    name = 'Solidity'
    aliases = ['solidity']
    filenames = ['*.sol']
    mimetypes = []
    flags = re.MULTILINE | re.UNICODE
    datatype = '\\b(address|bool|((bytes|hash|int|string|uint)(8|16|24|32|40|48|56|64|72|80|88|96|104|112|120|128|136|144|152|160|168|176|184|192|200|208|216|224|232|240|248|256)?))\\b'
    tokens = {'root':[
      include('whitespace'),
      include('comments'),
      (
       '\\bpragma\\s+solidity\\b', Keyword, 'pragma'),
      (
       '\\b(contract)(\\s+)([a-zA-Z_]\\w*)',
       bygroups(Keyword, Text.WhiteSpace, Name.Entity)),
      (
       datatype + '(\\s+)((external|public|internal|private)\\s+)?' + '([a-zA-Z_]\\w*)',
       bygroups(Keyword.Type, None, None, None, Text.WhiteSpace, Keyword, None, Name.Variable)),
      (
       '\\b(enum|event|function|struct)(\\s+)([a-zA-Z_]\\w*)',
       bygroups(Keyword.Type, Text.WhiteSpace, Name.Variable)),
      (
       '\\b(msg|block|tx)\\.([A-Za-z_][A-Za-z0-9_]*)\\b', Keyword),
      (
       words(('block', 'break', 'constant', 'constructor', 'continue', 'contract', 'do', 'else',
       'external', 'false', 'for', 'function', 'if', 'import', 'inherited', 'internal',
       'is', 'library', 'mapping', 'memory', 'modifier', 'msg', 'new', 'payable',
       'private', 'public', 'require', 'return', 'returns', 'struct', 'suicide',
       'throw', 'this', 'true', 'tx', 'var', 'while'),
         prefix='\\b', suffix='\\b'),
       Keyword.Type),
      (
       words(('keccak256', ), prefix='\\b', suffix='\\b'), Name.Builtin),
      (
       datatype, Keyword.Type),
      include('constants'),
      (
       '[a-zA-Z_]\\w*', Text),
      (
       '[!<=>+*/-]', Operator),
      (
       '[.;:{}(),\\[\\]]', Punctuation)], 
     'comments':[
      (
       '//(\\n|[\\w\\W]*?[^\\\\]\\n)', Comment.Single),
      (
       '/(\\\\\\n)?[*][\\w\\W]*?[*](\\\\\\n)?/', Comment.Multiline),
      (
       '/(\\\\\\n)?[*][\\w\\W]*', Comment.Multiline)], 
     'constants':[
      (
       '("([\\\\]"|.)*?")', String.Double),
      (
       "('([\\\\]'|.)*?')", String.Single),
      (
       '\\b0[xX][0-9a-fA-F]+\\b', Number.Hex),
      (
       '\\b\\d+\\b', Number.Decimal)], 
     'pragma':[
      include('whitespace'),
      include('comments'),
      (
       '(\\^|>=|<)(\\s*)(\\d+\\.\\d+\\.\\d+)',
       bygroups(Operator, Text.WhiteSpace, Keyword)),
      (
       ';', Punctuation, '#pop')], 
     'whitespace':[
      (
       '\\s+', Text.WhiteSpace),
      (
       '\\n', Text.WhiteSpace)]}