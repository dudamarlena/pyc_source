# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/widgets/avatar.py
# Compiled at: 2020-04-26 16:40:12
# Size of source mod 2**32: 4855 bytes
"""
Module that contains implementation for avatar/user widgets
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *
import tpDcc
from tpDcc.libs.qt.core import theme, mixin

@mixin.theme_mixin
class Avatar(QLabel, object):
    __doc__ = '\n    Widget that can be used to represent users or objects\n    '

    def __init__(self, parent=None, flags=0):
        super(Avatar, self).__init__(parent, flags)
        self._default_pixmap = tpDcc.ResourcesMgr().pixmap('user')
        self._pixmap = self._default_pixmap
        self._size = 0
        self._set_size(self.theme_default_size())

    def _get_size(self):
        """
        Returns the avatar height size
        :return: float
        """
        return self._size

    def _set_size(self, value):
        """
        Sets avatar height size
        :param value: float
        """
        self._size = value
        self.setFixedSize(self._size, self._size)
        self.setPixmap(self._pixmap.scaledToWidth(self.height(), Qt.SmoothTransformation))

    def _get_image(self):
        """
        Returns avatar image
        :return: QPixmap
        """
        return self._pixmap

    def _set_image(self, value):
        """
        Sets avatar image
        :param value: QPixmap or None
        """
        if value is None:
            self._pixmap = self._default_pixmap
        else:
            if isinstance(value, QPixmap):
                self._pixmap = value
            else:
                raise TypeError('Input argument value should be QPixmap or None, but get "{}"'.format(type(value)))
        self.setPixmap(self._pixmap.scaledToWidth(self.height(), Qt.SmoothTransformation))

    theme_size = Property(int, _get_size, _set_size)
    image = Property(QPixmap, _get_image, _set_image)

    @classmethod
    def tiny(cls, image=None, parent=None):
        """
        Creates a new avatar widget with tiny size
        :param image:
        :param parent:
        :return:
        """
        avatar_widget = cls(parent=parent)
        loading_theme = avatar_widget.theme()
        loading_size = loading_theme.tiny if loading_theme else theme.Theme.Sizes.TINY
        avatar_widget.theme_size = loading_size
        avatar_widget.image = image
        return avatar_widget

    @classmethod
    def small(cls, image=None, parent=None):
        """
        Creates a new avatar widget with small size
        :param image:
        :param parent:
        :return:
        """
        avatar_widget = cls(parent=parent)
        loading_theme = avatar_widget.theme()
        loading_size = loading_theme.small if loading_theme else theme.Theme.Sizes.SMALL
        avatar_widget.theme_size = loading_size
        avatar_widget.image = image
        return avatar_widget

    @classmethod
    def medium(cls, image=None, parent=None):
        """
        Creates a new avatar widget with medium size
        :param image:
        :param parent:
        :return:
        """
        avatar_widget = cls(parent=parent)
        loading_theme = avatar_widget.theme()
        loading_size = loading_theme.medium if loading_theme else theme.Theme.Sizes.MEDIUM
        avatar_widget.theme_size = loading_size
        avatar_widget.image = image
        return avatar_widget

    @classmethod
    def large(cls, image=None, parent=None):
        """
        Creates a new avatar widget with large size
        :param image:
        :param parent:
        :return:
        """
        avatar_widget = cls(parent=parent)
        loading_theme = avatar_widget.theme()
        loading_size = loading_theme.large if loading_theme else theme.Theme.Sizes.LARGE
        avatar_widget.theme_size = loading_size
        avatar_widget.image = image
        return avatar_widget

    @classmethod
    def huge(cls, image=None, parent=None):
        """
        Creates a new avatar widget with huge size
        :param image:
        :param parent:
        :return:
        """
        avatar_widget = cls(parent=parent)
        loading_theme = avatar_widget.theme()
        loading_size = loading_theme.huge if loading_theme else theme.Theme.Sizes.HUGE
        avatar_widget.theme_size = loading_size
        avatar_widget.image = image
        return avatar_widget