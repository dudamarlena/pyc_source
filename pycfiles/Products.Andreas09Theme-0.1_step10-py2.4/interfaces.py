# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/Andreas09Theme/browser/interfaces.py
# Compiled at: 2008-09-09 18:26:37
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
    __module__ = __name__


class IAndreas09Footer(IViewletManager):
    """A viewlet manager for wrapping the footer into a <div id="footer"> tag.
    """
    __module__ = __name__