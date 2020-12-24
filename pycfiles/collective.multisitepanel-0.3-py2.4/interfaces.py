# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/multisitepanel/browser/interfaces.py
# Compiled at: 2010-07-15 11:13:22
from plone.theme.interfaces import IDefaultPloneLayer
from zope import interface

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
    __module__ = __name__


class IMultiSitePanel(interface.Interface):
    __module__ = __name__


class IMultiSiteProductsPanel(interface.Interface):
    __module__ = __name__