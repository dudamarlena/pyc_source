# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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