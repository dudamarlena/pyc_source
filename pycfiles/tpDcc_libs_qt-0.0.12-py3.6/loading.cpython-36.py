# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/widgets/loading.py
# Compiled at: 2020-05-03 00:26:03
# Size of source mod 2**32: 5243 bytes
"""
Module that contains implementation for loading widgets
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtGui import *
import tpDcc
from tpDcc.libs.qt.core import base, theme, mixin

@mixin.theme_mixin
class CircleLoading(base.BaseWidget, object):

    def __init__(self, size=None, color=None, speed=1, parent=None):
        super(CircleLoading, self).__init__(parent=parent)
        size = size or self.theme_default_size()
        self.setFixedSize(QSize(size, size))
        self._rotation = 0
        self._loading_pixmap = tpDcc.ResourcesMgr().pixmap('loading',
          extension='svg', color=(color or self.accent_color())).scaledToWidth(size, Qt.SmoothTransformation)
        self._loading_anim = QPropertyAnimation()
        self._loading_anim.setTargetObject(self)
        self._loading_anim.setDuration(1000 * (1 / speed))
        self._loading_anim.setPropertyName('rotation')
        self._loading_anim.setStartValue(0)
        self._loading_anim.setEndValue(360)
        self._loading_anim.setLoopCount(-1)
        self._loading_anim.start()

    def _set_rotation(self, value):
        self._rotation = value
        self.update()

    def _get_rotation(self):
        return self._rotation

    rotation = Property(int, _get_rotation, _set_rotation)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.translate(self._loading_pixmap.width() / 2, self._loading_pixmap.height() / 2)
        painter.rotate(self._rotation)
        painter.drawPixmap(-self._loading_pixmap.width() / 2, -self._loading_pixmap.height() / 2, self._loading_pixmap.width(), self._loading_pixmap.height(), self._loading_pixmap)
        painter.end()
        return super(CircleLoading, self).paintEvent(event)

    def set_size(self, size):
        """
        Sets the size of the widget
        :param size: int
        """
        self.setFixedSize(QSize(size, size))
        self._loading_pixmap = self._loading_pixmap.scaledToWidth(size, Qt.SmoothTransformation)

    @classmethod
    def tiny(cls, color=None, parent=None):
        """
        Creates a circle loading widget with tiny size
        :param color:
        :param parent:
        :return:
        """
        loading_widget = cls(color=color, parent=parent)
        loading_theme = loading_widget.theme()
        loading_size = loading_theme.tiny if loading_theme else theme.Theme.Sizes.TINY
        loading_widget.set_size(loading_size)
        return loading_widget

    @classmethod
    def small(cls, color=None, parent=None):
        """
        Creates a circle loading widget with small size
        :param color:
        :param parent:
        :return:
        """
        loading_widget = cls(color=color)
        loading_theme = loading_widget.theme()
        loading_size = loading_theme.small if loading_theme else theme.Theme.Sizes.SMALL
        loading_widget.set_size(loading_size)
        return loading_widget

    @classmethod
    def medium(cls, color=None, parent=None):
        """
        Creates a circle loading widget with medium size
        :param color:
        :param parent:
        :return:
        """
        loading_widget = cls(color=color)
        loading_theme = loading_widget.theme()
        loading_size = loading_theme.medium if loading_theme else theme.Theme.Sizes.MEDIUM
        loading_widget.set_size(loading_size)
        return loading_widget

    @classmethod
    def large(cls, color=None, parent=None):
        """
        Creates a circle loading widget with large size
        :param color:
        :param parent:
        :return:
        """
        loading_widget = cls(color=color)
        loading_theme = loading_widget.theme()
        loading_size = loading_theme.large if loading_theme else theme.Theme.Sizes.LARGE
        loading_widget.set_size(loading_size)
        return loading_widget

    @classmethod
    def huge(cls, color=None, parent=None):
        """
        Creates a circle loading widget with huge size
        :param color:
        :param parent:
        :return:
        """
        loading_widget = cls(color=color)
        loading_theme = loading_widget.theme()
        loading_size = loading_theme.huge if loading_theme else theme.Theme.Sizes.HUGE
        loading_widget.set_size(loading_size)
        return loading_widget