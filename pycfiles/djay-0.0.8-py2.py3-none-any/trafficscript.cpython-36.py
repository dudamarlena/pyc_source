# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/trafficscript.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 1546 bytes
"""
    pygments.lexers.trafficscript
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for RiverBed's TrafficScript (RTS) language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer
from pygments.token import String, Number, Name, Keyword, Operator, Text, Comment
__all__ = [
 'RtsLexer']

class RtsLexer(RegexLexer):
    __doc__ = '\n    For `Riverbed Stingray Traffic Manager <http://www.riverbed.com/stingray>`_\n\n    .. versionadded:: 2.1\n    '
    name = 'TrafficScript'
    aliases = ['rts', 'trafficscript']
    filenames = ['*.rts']
    tokens = {'root':[
      (
       "'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String),
      (
       '"', String, 'escapable-string'),
      (
       '(0x[0-9a-fA-F]+|\\d+)', Number),
      (
       '\\d+\\.\\d+', Number.Float),
      (
       '\\$[a-zA-Z](\\w|_)*', Name.Variable),
      (
       '(if|else|for(each)?|in|while|do|break|sub|return|import)', Keyword),
      (
       '[a-zA-Z][\\w.]*', Name.Function),
      (
       '[-+*/%=,;(){}<>^.!~|&\\[\\]\\?\\:]', Operator),
      (
       '(>=|<=|==|!=|&&|\\|\\||\\+=|.=|-=|\\*=|/=|%=|<<=|>>=|&=|\\|=|\\^=|>>|<<|\\+\\+|--|=>)',
       Operator),
      (
       '[ \\t\\r]+', Text),
      (
       '#[^\\n]*', Comment)], 
     'escapable-string':[
      (
       '\\\\[tsn]', String.Escape),
      (
       '[^"]', String),
      (
       '"', String, '#pop')]}