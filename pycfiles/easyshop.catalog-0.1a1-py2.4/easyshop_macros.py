# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/browser/easyshop_macros.py
# Compiled at: 2008-09-03 11:14:28
from zope.interface import Interface
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProductManagement

class INavigationMacroView(Interface):
    """
    """
    __module__ = __name__

    def getProductURLs():
        """Returns the product urls.
        """
        pass


class NavigationMacroView(BrowserView):
    """
    """
    __module__ = __name__
    implements(INavigationMacroView)

    def getProductURLs(self):
        """
        """
        sorting = self.request.SESSION.get('sorting')
        try:
            (sorted_on, sort_order) = sorting.split('-')
        except (AttributeError, ValueError):
            sorted_on = 'price'
            sort_order = 'desc'

        cm = ICategoryManagement(self.context)
        categories = cm.getTopLevelCategories()
        result = []
        for category in categories:
            pm = IProductManagement(category)
            products = pm.getAllProducts(sorted_on=sorted_on, sort_order=sort_order)
            index = products.index(self.context)
            temp = {}
            if index == 0:
                temp['previous'] = None
                temp['first'] = None
            else:
                product = products[(index - 1)]
                temp['previous'] = product.absolute_url()
                temp['first'] = products[0].absolute_url()
            try:
                product = products[(index + 1)]
                temp['next'] = product.absolute_url()
                temp['last'] = products[(-1)].absolute_url()
            except IndexError:
                temp['next'] = None
                temp['last'] = None

            temp['category_url'] = category.absolute_url()
            temp['category'] = category.Title()
            temp['position'] = index + 1
            temp['amount'] = len(products)
            result.append(temp)

        return result