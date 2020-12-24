# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/xorg.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 887 bytes
"""
    pygments.lexers.xorg
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for Xorg configs.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, bygroups
from pygments.token import Comment, String, Name, Text
__all__ = [
 'XorgLexer']

class XorgLexer(RegexLexer):
    __doc__ = 'Lexer for xorg.conf file.'
    name = 'Xorg'
    aliases = ['xorg.conf']
    filenames = ['xorg.conf']
    mimetypes = []
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '#.*$', Comment),
              (
               '((?:Sub)?Section)(\\s+)("\\w+")',
               bygroups(String.Escape, Text, String.Escape)),
              (
               '(End(|Sub)Section)', String.Escape),
              (
               '(\\w+)(\\s+)([^\\n#]+)',
               bygroups(Name.Builtin, Text, Name.Constant))]}