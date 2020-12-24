# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/sgf.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 2024 bytes
"""
    pygments.lexers.sgf
    ~~~~~~~~~~~~~~~~~~~

    Lexer for Smart Game Format (sgf) file format.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, bygroups
from pygments.token import Name, Literal, String, Text, Punctuation
__all__ = [
 'SmartGameFormatLexer']

class SmartGameFormatLexer(RegexLexer):
    __doc__ = '\n    Lexer for Smart Game Format (sgf) file format.\n\n    The format is used to store game records of board games for two players\n    (mainly Go game).\n    For more information about the definition of the format, see:\n    https://www.red-bean.com/sgf/\n\n    .. versionadded:: 2.4\n    '
    name = 'SmartGameFormat'
    aliases = ['sgf']
    filenames = ['*.sgf']
    tokens = {'root': [
              (
               '[\\s():;]', Punctuation),
              (
               '(A[BW]|AE|AN|AP|AR|AS|[BW]L|BM|[BW]R|[BW]S|[BW]T|CA|CH|CP|CR|DD|DM|DO|DT|EL|EV|EX|FF|FG|G[BW]|GC|GM|GN|HA|HO|ID|IP|IT|IY|KM|KO|LB|LN|LT|L|MA|MN|M|N|OB|OM|ON|OP|OT|OV|P[BW]|PC|PL|PM|RE|RG|RO|RU|SO|SC|SE|SI|SL|SO|SQ|ST|SU|SZ|T[BW]|TC|TE|TM|TR|UC|US|VW|V|[BW]|C)',
               Name.Builtin),
              (
               '(\\[)([0-9.]+)(\\])',
               bygroups(Punctuation, Literal.Number, Punctuation)),
              (
               '(\\[)([0-9]{4}-[0-9]{2}-[0-9]{2})(\\])',
               bygroups(Punctuation, Literal.Date, Punctuation)),
              (
               '(\\[)([a-z]{2})(\\])',
               bygroups(Punctuation, String, Punctuation)),
              (
               '(\\[)([a-z]{2})(:)([a-z]{2})(\\])',
               bygroups(Punctuation, String, Punctuation, String, Punctuation)),
              (
               '(\\[)([\\w\\s#()+,\\-.:?]+)(\\])',
               bygroups(Punctuation, String, Punctuation)),
              (
               '(\\[)(\\s.*)(\\])',
               bygroups(Punctuation, Text, Punctuation))]}