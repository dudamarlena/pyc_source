# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cooking/theme/browser/interfaces.py
# Compiled at: 2010-08-12 16:17:02
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager
from plone.portlets.interfaces import IPortletManager

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "Ameria Cooking theme" theme, this interface must be its layer
       (in theme/viewlets/configure.zcml).
    """
    __module__ = __name__


class ISimpleTitleViewlet(IViewletManager):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "Ameria Cooking theme" theme, this interface must be its layer
       (in theme/viewlets/configure.zcml).
    """
    __module__ = __name__


class IPortalSiteHeader(IViewletManager):
    """A viewlet manager that sits above all content in left column, normally used to hold
    the content views (tabs) and associated actions.
    """
    __module__ = __name__


class IPortalUpperRightColumn(IViewletManager):
    """A viewlet manager that sits above all content in right column.
    """
    __module__ = __name__