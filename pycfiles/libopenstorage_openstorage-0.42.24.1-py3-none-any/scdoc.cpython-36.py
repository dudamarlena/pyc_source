# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/scdoc.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 1983 bytes
"""
    pygments.lexers.scdoc
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for scdoc, a simple man page generator.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, using, this
from pygments.token import Text, Comment, Keyword, String, Generic
__all__ = [
 'ScdocLexer']

class ScdocLexer(RegexLexer):
    __doc__ = '\n    `scdoc` is a simple man page generator for POSIX systems written in C99.\n    https://git.sr.ht/~sircmpwn/scdoc\n\n    .. versionadded:: 2.5\n    '
    name = 'scdoc'
    aliases = ['scdoc', 'scd']
    filenames = ['*.scd', '*.scdoc']
    flags = re.MULTILINE
    tokens = {'root':[
      (
       '^(;.+\\n)', bygroups(Comment)),
      (
       '^(#)([^#].+\\n)', bygroups(Generic.Heading, Text)),
      (
       '^(#{2})(.+\\n)', bygroups(Generic.Subheading, Text)),
      (
       '^(\\s*)([*-])(\\s)(.+\\n)',
       bygroups(Text, Keyword, Text, using(this, state='inline'))),
      (
       '^(\\s*)(\\.+\\.)( .+\\n)',
       bygroups(Text, Keyword, using(this, state='inline'))),
      (
       '^(\\s*>\\s)(.+\\n)', bygroups(Keyword, Generic.Emph)),
      (
       '^(```\\n)([\\w\\W]*?)(^```$)', bygroups(String, Text, String)),
      include('inline')], 
     'inline':[
      (
       '\\\\.', Text),
      (
       '(\\s)(_[^_]+_)(\\W|\\n)', bygroups(Text, Generic.Emph, Text)),
      (
       '(\\s)(\\*[^\\*]+\\*)(\\W|\\n)', bygroups(Text, Generic.Strong, Text)),
      (
       '`[^`]+`', String.Backtick),
      (
       '[^\\\\\\s]+', Text),
      (
       '.', Text)]}