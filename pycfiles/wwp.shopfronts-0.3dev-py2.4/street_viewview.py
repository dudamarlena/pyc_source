# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/shopfronts/browser/street_viewview.py
# Compiled at: 2009-09-22 06:30:28
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from wwp.shopfronts import shopfrontsMessageFactory as _
from Products.CMFCore.utils import getToolByName

class Istreet_viewView(Interface):
    """
    street_view view interface
    """
    __module__ = __name__

    def test():
        """ test method"""
        pass


class street_viewView(BrowserView):
    """
    street_view browser view
    """
    __module__ = __name__
    implements(Istreet_viewView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _('a dummy string')
        return {'dummy': dummy}

    def get_index(self):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        query = {}
        query['type'] = 'street_view'
        brains = portal_catalog.searchResults(**query)
        print brains