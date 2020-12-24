# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/development/checkouts/inqbus.collection.proxy/inqbus/collection/proxy/browser/collectionproxyview.py
# Compiled at: 2011-06-06 08:05:24
from Acquisition import aq_base
from zope.interface import implements, Interface
from zope.component import getMultiAdapter
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.browser import IBrowserView
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.interface import ISelectableBrowserDefault
from AccessControl.SecurityManagement import newSecurityManager

class ICollectionProxyView(IBrowserView):
    """
    ContentProxy view interface
    """
    pass


class CollectionProxyView(BrowserView):
    """
    ContentProxy browser view
    """
    implements(ICollectionProxyView)

    def get_item_url(self, item):
        """
        """
        if hasattr(self.context, 'boolean_proxy_field') and self.context.boolean_proxy_field:
            return self.context.absolute_url() + '/»' + item.getPath()
        else:
            if hasattr(item, 'getURL'):
                return item.getURL()
            return item.absolute_url()