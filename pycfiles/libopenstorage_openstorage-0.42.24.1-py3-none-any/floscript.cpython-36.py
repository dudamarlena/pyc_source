# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/floscript.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 2667 bytes
"""
    pygments.lexers.floscript
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for FloScript

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'FloScriptLexer']

class FloScriptLexer(RegexLexer):
    __doc__ = '\n    For `FloScript <https://github.com/ioflo/ioflo>`_ configuration language source code.\n\n    .. versionadded:: 2.4\n    '
    name = 'FloScript'
    aliases = ['floscript', 'flo']
    filenames = ['*.flo']

    def innerstring_rules(ttype):
        return [
         (
          '%(\\(\\w+\\))?[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[E-GXc-giorsux%]',
          String.Interpol),
         (
          '[^\\\\\\\'"%\\n]+', ttype),
         (
          '[\\\'"\\\\]', ttype),
         (
          '%', ttype)]

    tokens = {'root':[
      (
       '\\n', Text),
      (
       '[^\\S\\n]+', Text),
      (
       '[]{}:(),;[]', Punctuation),
      (
       '\\\\\\n', Text),
      (
       '\\\\', Text),
      (
       '(to|by|with|from|per|for|cum|qua|via|as|at|in|of|on|re|is|if|be|into|and|not)\\b',
       Operator.Word),
      (
       '!=|==|<<|>>|[-~+/*%=<>&^|.]', Operator),
      (
       '(load|init|server|logger|log|loggee|first|over|under|next|done|timeout|repeat|native|benter|enter|recur|exit|precur|renter|rexit|print|put|inc|copy|set|aux|rear|raze|go|let|do|bid|ready|start|stop|run|abort|use|flo|give|take)\\b',
       Name.Builtin),
      (
       '(frame|framer|house)\\b', Keyword),
      (
       '"', String, 'string'),
      include('name'),
      include('numbers'),
      (
       '#.+$', Comment.Singleline)], 
     'string':[
      (
       '[^"]+', String),
      (
       '"', String, '#pop')], 
     'numbers':[
      (
       '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?j?', Number.Float),
      (
       '\\d+[eE][+-]?[0-9]+j?', Number.Float),
      (
       '0[0-7]+j?', Number.Oct),
      (
       '0[bB][01]+', Number.Bin),
      (
       '0[xX][a-fA-F0-9]+', Number.Hex),
      (
       '\\d+L', Number.Integer.Long),
      (
       '\\d+j?', Number.Integer)], 
     'name':[
      (
       '@[\\w.]+', Name.Decorator),
      (
       '[a-zA-Z_]\\w*', Name)]}