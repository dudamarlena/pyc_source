# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/widgets/switch.py
# Compiled at: 2020-04-24 23:12:07
# Size of source mod 2**32: 3038 bytes
"""
Module that contains implementation for switch widget
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *
from tpDcc.libs.qt.core import mixin, theme

@mixin.theme_mixin
@mixin.cursor_mixin
class SwitchWidget(QRadioButton, object):

    def __init__(self, parent=None):
        super(SwitchWidget, self).__init__(parent)
        self._size = self.theme_default_size()
        self.setAutoExclusive(False)

    def _get_size(self):
        """
        Returns switch size
        :return: float
        """
        return self._size

    def _set_size(self, value):
        """
        Sets switch size
        :param value: float
        """
        self._size = value
        self.style().polish(self)

    theme_size = Property(int, _get_size, _set_size)

    def minimumSizeHint(self):
        """
        Overrides base QRadioButton minimumSizeHint functino
        We do not need text space
        :return: QSize
        """
        height = self._size * 1.2
        return QSize(height, height / 2)

    def tiny(self):
        """
        Sets button to tiny size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.tiny if widget_theme else theme.Theme.Sizes.TINY
        return self

    def small(self):
        """
        Sets button to small size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.small if widget_theme else theme.Theme.Sizes.SMALL
        return self

    def medium(self):
        """
        Sets button to medium size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.medium if widget_theme else theme.Theme.Sizes.MEDIUM
        return self

    def large(self):
        """
        Sets button to large size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.large if widget_theme else theme.Theme.Sizes.LARGE
        return self

    def huge(self):
        """
        Sets button to large size
        """
        widget_theme = self.theme()
        self.theme_size = widget_theme.huge if widget_theme else theme.Theme.Sizes.HUGE
        return self