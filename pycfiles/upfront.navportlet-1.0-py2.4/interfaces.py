# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/upfront/navportlet/interfaces.py
# Compiled at: 2010-10-13 15:04:43
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

class INavigationCatalogTool(Interface):
    """ Marker interface for INavigationCatalogTool """
    __module__ = __name__


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
    __module__ = __name__