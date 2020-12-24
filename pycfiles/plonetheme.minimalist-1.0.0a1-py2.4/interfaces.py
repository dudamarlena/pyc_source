# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/minimalist/browser/interfaces.py
# Compiled at: 2008-09-20 00:50:42
from plone.theme.interfaces import IDefaultPloneLayer
from plone.portlets.interfaces import IPortletManager

class IHeader(IPortletManager):
    """We need our own portlet manager in the portal header.
    """
    __module__ = __name__


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
    __module__ = __name__