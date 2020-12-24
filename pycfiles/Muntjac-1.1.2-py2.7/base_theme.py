# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/themes/base_theme.py
# Compiled at: 2013-04-04 15:36:36
"""The foundation for all Muntjac themes."""

class BaseTheme(object):
    """The Base theme is the foundation for all Muntjac themes. Although
    it is not necessary to use it as the starting point for all other
    themes, it is heavily encouraged, since it abstracts and hides away
    many necessary style properties that the Muntjac terminal expects and
    needs.

    When creating your own theme, either extend this class and specify
    the styles implemented in your theme here, or extend some other theme
    that has a class file specified (e.g. Reindeer or Runo).

    All theme class files should follow the convention of specifying the
    theme name as a string constant C{THEME_NAME}.
    """
    THEME_NAME = 'base'
    BUTTON_LINK = 'link'
    PANEL_LIGHT = 'light'