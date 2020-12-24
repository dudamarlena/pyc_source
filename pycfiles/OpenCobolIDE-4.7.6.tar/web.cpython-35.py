# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/web.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 918 bytes
"""
    pygments.lexers.web
    ~~~~~~~~~~~~~~~~~~~

    Just export previously exported lexers.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexers.html import HtmlLexer, DtdLexer, XmlLexer, XsltLexer, HamlLexer, ScamlLexer, JadeLexer
from pygments.lexers.css import CssLexer, SassLexer, ScssLexer
from pygments.lexers.javascript import JavascriptLexer, LiveScriptLexer, DartLexer, TypeScriptLexer, LassoLexer, ObjectiveJLexer, CoffeeScriptLexer
from pygments.lexers.actionscript import ActionScriptLexer, ActionScript3Lexer, MxmlLexer
from pygments.lexers.php import PhpLexer
from pygments.lexers.webmisc import DuelLexer, XQueryLexer, SlimLexer, QmlLexer
from pygments.lexers.data import JsonLexer
JSONLexer = JsonLexer
__all__ = []