# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\collective\threecolorstheme\interfaces.py
# Compiled at: 2008-10-12 05:16:06
from zope.interface import Interface

class IThreeColorsThemeBrowserLayer(Interface):
    """Marker interface that defines a Zope 3 browser layer.
       will be used by local browser layer product
    """
    __module__ = __name__


class IThreeColorsThemeSkin(Interface):
    """
      Marker interface for the based PhantasySkin Type : ThreeColorsThemeSkin
    """
    __module__ = __name__