# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/management/scripts/manage_sessions.py
# Compiled at: 2008-09-03 11:15:04
from zLOG import LOG, INFO
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

class ManageSessions:
    """
    """
    __module__ = __name__

    def deleteCarts(self):
        """Delete expired Sessions
        """
        now = DateTime()
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(object_provides='easyshop.core.interfaces.shop.IShop')
        for brain in brains:
            shop = brain.getObject()
            to_delete = []
            for cart in shop.carts.objectValues():
                if now - cart.modified() < 10:
                    continue
                if cart.getId().isdigit() == False:
                    continue
                to_delete.append(cart.getId())

            shop.carts.manage_delObjects(to_delete)
            LOG('Delete Carts', INFO, '%s expired carts deleted for %s' % (len(to_delete), shop.Title()))

    def deleteCustomers(self):
        """
        """
        now = DateTime()
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(object_provides='easyshop.core.interfaces.shop.IShop')
        for brain in brains:
            shop = brain.getObject()
            to_delete = []
            for customer in shop.customers.objectValues():
                if now - customer.modified() < 10:
                    continue
                if customer.getId().isdigit() == False:
                    continue
                to_delete.append(cart.getId())

            shop.customers.manage_delObjects(to_delete)
            LOG('Delete Customers', INFO, '%s expired customers deleted for %s' % (len(to_delete), shop.Title()))