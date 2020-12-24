# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pytpptheme/theme.py
# Compiled at: 2009-05-12 23:25:43
from trac.core import *
from themeengine.api import ThemeBase

class PyTppTheme(ThemeBase):
    """Trac theme based on python.org and The Python Papers."""
    template = htdocs = css = screenshot = True