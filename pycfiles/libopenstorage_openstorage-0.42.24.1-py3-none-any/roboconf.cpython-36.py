# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/roboconf.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 2070 bytes
"""
    pygments.lexers.roboconf
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Roboconf DSL.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, words, re
from pygments.token import Text, Operator, Keyword, Name, Comment
__all__ = [
 'RoboconfGraphLexer', 'RoboconfInstancesLexer']

class RoboconfGraphLexer(RegexLexer):
    __doc__ = '\n    Lexer for `Roboconf <http://roboconf.net/en/roboconf.html>`_ graph files.\n\n    .. versionadded:: 2.1\n    '
    name = 'Roboconf Graph'
    aliases = ['roboconf-graph']
    filenames = ['*.graph']
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '=', Operator),
              (
               words(('facet', 'import'), suffix='\\s*\\b', prefix='\\b'), Keyword),
              (
               words(('installer', 'extends', 'exports', 'imports', 'facets', 'children'),
                 suffix='\\s*:?', prefix='\\b'), Name),
              (
               '#.*\\n', Comment),
              (
               '[^#]', Text),
              (
               '.*\\n', Text)]}


class RoboconfInstancesLexer(RegexLexer):
    __doc__ = '\n    Lexer for `Roboconf <http://roboconf.net/en/roboconf.html>`_ instances files.\n\n    .. versionadded:: 2.1\n    '
    name = 'Roboconf Instances'
    aliases = ['roboconf-instances']
    filenames = ['*.instances']
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               words(('instance of', 'import'), suffix='\\s*\\b', prefix='\\b'), Keyword),
              (
               words(('name', 'count'), suffix='s*:?', prefix='\\b'), Name),
              (
               '\\s*[\\w.-]+\\s*:', Name),
              (
               '#.*\\n', Comment),
              (
               '[^#]', Text),
              (
               '.*\\n', Text)]}