# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/extheme/theme.py
# Compiled at: 2009-07-03 01:50:23
from trac.core import *
from themeengine.api import ThemeBase

class ExampleTheme(ThemeBase):
    """Un tema sencillo para Trac."""
    htdocs = css = screenshot = True