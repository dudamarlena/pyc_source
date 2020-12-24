# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/ooc.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 2999 bytes
"""
    pygments.lexers.ooc
    ~~~~~~~~~~~~~~~~~~~

    Lexers for the Ooc language.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'OocLexer']

class OocLexer(RegexLexer):
    __doc__ = '\n    For `Ooc <http://ooc-lang.org/>`_ source code\n\n    .. versionadded:: 1.2\n    '
    name = 'Ooc'
    aliases = ['ooc']
    filenames = ['*.ooc']
    mimetypes = ['text/x-ooc']
    tokens = {'root':[
      (
       words(('class', 'interface', 'implement', 'abstract', 'extends', 'from', 'this', 'super',
       'new', 'const', 'final', 'static', 'import', 'use', 'extern', 'inline', 'proto',
       'break', 'continue', 'fallthrough', 'operator', 'if', 'else', 'for', 'while',
       'do', 'switch', 'case', 'as', 'in', 'version', 'return', 'true', 'false',
       'null'),
         prefix='\\b', suffix='\\b'),
       Keyword),
      (
       'include\\b', Keyword, 'include'),
      (
       '(cover)([ \\t]+)(from)([ \\t]+)(\\w+[*@]?)',
       bygroups(Keyword, Text, Keyword, Text, Name.Class)),
      (
       '(func)((?:[ \\t]|\\\\\\n)+)(~[a-z_]\\w*)',
       bygroups(Keyword, Text, Name.Function)),
      (
       '\\bfunc\\b', Keyword),
      (
       '//.*', Comment),
      (
       '(?s)/\\*.*?\\*/', Comment.Multiline),
      (
       '(==?|\\+=?|-[=>]?|\\*=?|/=?|:=|!=?|%=?|\\?|>{1,3}=?|<{1,3}=?|\\.\\.|&&?|\\|\\|?|\\^=?)',
       Operator),
      (
       '(\\.)([ \\t]*)([a-z]\\w*)',
       bygroups(Operator, Text, Name.Function)),
      (
       '[A-Z][A-Z0-9_]+', Name.Constant),
      (
       '[A-Z]\\w*([@*]|\\[[ \\t]*\\])?', Name.Class),
      (
       '([a-z]\\w*(?:~[a-z]\\w*)?)((?:[ \\t]|\\\\\\n)*)(?=\\()',
       bygroups(Name.Function, Text)),
      (
       '[a-z]\\w*', Name.Variable),
      (
       '[:(){}\\[\\];,]', Punctuation),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '0c[0-9]+', Number.Oct),
      (
       '0b[01]+', Number.Bin),
      (
       '[0-9_]\\.[0-9_]*(?!\\.)', Number.Float),
      (
       '[0-9_]+', Number.Decimal),
      (
       '"(?:\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\"])*"',
       String.Double),
      (
       "'(?:\\\\.|\\\\[0-9]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'",
       String.Char),
      (
       '@', Punctuation),
      (
       '\\.', Punctuation),
      (
       '\\\\[ \\t\\n]', Text),
      (
       '[ \\t]+', Text)], 
     'include':[
      (
       '[\\w/]+', Name),
      (
       ',', Punctuation),
      (
       '[ \\t]', Text),
      (
       '[;\\n]', Text, '#pop')]}