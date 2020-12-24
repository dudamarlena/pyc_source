# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jesse/Source/ttkthemes/ttkthemes/themed_style.py
# Compiled at: 2020-02-09 16:41:04
# Size of source mod 2**32: 1570 bytes
"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
from ._widget import ThemedWidget
import tkinter as tk
from tkinter import ttk

class ThemedStyle(ttk.Style, ThemedWidget):
    __doc__ = '\n    Style that supports setting the theme for a Tk instance. Can be\n    used as a drop-in replacement for normal ttk.Style instances.\n    Supports the themes provided by this package.\n    '

    def __init__(self, *args, **kwargs):
        """
        :param theme: Theme to set up initialization completion. If the
                      theme is not available, fails silently.
        """
        theme = kwargs.pop('theme', None)
        gif_override = kwargs.pop('gif_override', False)
        (ttk.Style.__init__)(self, *args, **kwargs)
        ThemedWidget.__init__(self, self.tk, gif_override)
        if theme is not None:
            if theme in self.get_themes():
                self.set_theme(theme)

    def theme_use(self, theme_name=None):
        """
        Set a new theme to use or return current theme name

        :param theme_name: name of theme to use
        :returns: active theme name
        """
        if theme_name is not None:
            self.set_theme(theme_name)
        return ttk.Style.theme_use(self)

    def theme_names(self):
        """
        Alias of get_themes() to allow for a drop-in replacement of the
        normal ttk.Style instance.

        :returns: Result of get_themes()
        """
        return self.get_themes()