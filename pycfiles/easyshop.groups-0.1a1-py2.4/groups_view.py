# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/groups/browser/groups_view.py
# Compiled at: 2008-09-03 11:14:50
from Products.Five.browser import BrowserView
from easyshop.core.interfaces import IGroupManagement
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IShopManagement

class GroupsView(BrowserView):
    """
    """
    __module__ = __name__

    def getGroup(self):
        """Returns a group by given id via request.
        """
        group_id = self.request.get('group_id')
        if group_id is None:
            return
        shop = self._getShop()
        group = IGroupManagement(shop).getGroup(group_id)
        products = []
        line = []
        for (i, product) in enumerate(IProductManagement(group).getProducts()):
            line.append({'title': product.Title(), 'id': product.getId(), 'url': product.absolute_url()})
            if (i + 1) % 5 == 0:
                products.append(line)
                line = []

        if len(line) > 0:
            products.append(line)
        return {'title': group.Title(), 'description': group.Description(), 'url': group.absolute_url(), 'products': products}

    def getGroups(self):
        """Returns groups of the shop.
        """
        shop = self._getShop()
        gm = IGroupManagement(shop)
        return gm.getGroups()

    def _getShop(self):
        """
        """
        return IShopManagement(self.context).getShop()