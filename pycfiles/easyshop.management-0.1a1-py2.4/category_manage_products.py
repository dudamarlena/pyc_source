# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/management/browser/category_manage_products.py
# Compiled at: 2008-09-03 11:15:03
from Products.Five.browser import BrowserView
from ZTUtils import make_query
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import Batch
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IProductManagement

class ManageProductsView(BrowserView):
    """
    """
    __module__ = __name__

    def getProducts(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        pm = IProductManagement(shop)
        result = []
        for product in pm.getProducts():
            result.append({'uid': product.UID, 'title': product.Title})

        b_start = self.request.get('b_start', 0)
        batch = Batch(result, 20, int(b_start), orphan=0)
        return {'batch': batch, 'next_url': self._getNextUrl(batch), 'previous_url': self._getPreviousUrl(batch)}

    def _getNextUrl(self, batch):
        """
        """
        try:
            start_str = batch.next.first
        except AttributeError:
            start_str = None

        query = make_query(self.request.form, {batch.b_start_str: start_str})
        return '%s/manage-products?%s' % (self.context.absolute_url(), query)

    def _getPreviousUrl(self, batch):
        """
        """
        try:
            start_str = batch.previous.first
        except AttributeError:
            start_str = None

        query = make_query(self.request.form, {batch.b_start_str: start_str})
        return '%s/manage-products?%s' % (self.context.absolute_url(), query)

    def addProducts(self):
        """
        """
        product_uids = self.request.get('product_uids', [])
        self.context.setProducts(product_uids)
        self.context.reindexObject()
        self.request.response.redirect('manage-products')