# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/AG/Projects/intk/Plone3/intk/src/plonetheme.INTKmodern/plonetheme/intkModern/browser/interfaces.py
# Compiled at: 2014-09-22 11:28:47
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager
from zope import schema
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.interfaces import IColumn

class IMediaTypes(Interface):
    """
    Marks all Media types from Products.media*
    """


class IThemeSpecific(Interface):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IFooterPortlet(IColumn):
    """we need our own portlet manager for the footer.
    """