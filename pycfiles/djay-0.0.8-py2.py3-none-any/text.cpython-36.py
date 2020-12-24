# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/text.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 1030 bytes
"""
    pygments.lexers.text
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for non-source code file types.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexers.configs import ApacheConfLexer, NginxConfLexer, SquidConfLexer, LighttpdConfLexer, IniLexer, RegeditLexer, PropertiesLexer
from pygments.lexers.console import PyPyLogLexer
from pygments.lexers.textedit import VimLexer
from pygments.lexers.markup import BBCodeLexer, MoinWikiLexer, RstLexer, TexLexer, GroffLexer
from pygments.lexers.installers import DebianControlLexer, SourcesListLexer
from pygments.lexers.make import MakefileLexer, BaseMakefileLexer, CMakeLexer
from pygments.lexers.haxe import HxmlLexer
from pygments.lexers.sgf import SmartGameFormatLexer
from pygments.lexers.diff import DiffLexer, DarcsPatchLexer
from pygments.lexers.data import YamlLexer
from pygments.lexers.textfmts import IrcLogsLexer, GettextLexer, HttpLexer
__all__ = []