# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/core/decorators.py
# Compiled at: 2020-04-15 12:12:43
# Size of source mod 2**32: 1274 bytes
"""
Module that contains decorators for Qt
"""
from __future__ import print_function, division, absolute_import
from tpDcc.libs.qt.core import theme as core_theme

def theme_widget(cls):
    """
    Decorator that can be used to allow custom widget classes to retrieve theme info of its main tpDcc window
    :param cls:
    :return: cls
    """

    def theme(self):
        found_theme = None
        top_widget = self
        while top_widget.parentWidget():
            top_widget = top_widget.parentWidget()
            if hasattr(top_widget, 'theme'):
                if callable(getattr(top_widget, 'theme')):
                    found_theme = top_widget.theme()
                    break

        return found_theme

    def theme_default_size(self):
        theme = self.theme()
        if not theme:
            return core_theme.Theme.DEFAULT_SIZE
        else:
            return theme.default_size

    def accent_color(self):
        theme = self.theme()
        if not theme:
            return core_theme.Theme.Colors.BLUE
        else:
            return theme.accent_color

    setattr(cls, 'theme', theme)
    setattr(cls, 'theme_default_size', theme_default_size)
    setattr(cls, 'accent_color', accent_color)
    return cls