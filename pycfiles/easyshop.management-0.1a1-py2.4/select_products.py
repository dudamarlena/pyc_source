# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/management/viewlets/select_products.py
# Compiled at: 2008-09-03 11:15:03
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.AdvancedQuery import And
from Products.AdvancedQuery import Eq
from Products.AdvancedQuery import In
from easyshop.core.interfaces import ICategoryManagement

class SelectProductsViewlet(ViewletBase):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('select_products.pt')

    def getProducts(self):
        """
        """
        if self.request.get('form-sent') is None:
            return []
        query = Eq('path', ('/').join(self.context.getPhysicalPath()))
        query &= Eq('object_provides', 'easyshop.core.interfaces.catalog.IProduct')
        search_text = self.request.get('search_text', '')
        search_category = self.request.get('search_category', [])
        if search_text != '':
            query &= Eq('Title', search_text)
        if len(search_category) > 0:
            query &= In('categories', search_category)
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.evalAdvancedQuery(query)
        result = []
        for brain in brains:
            product = brain.getObject()
            categories = (', ').join([ c.Title() for c in product.getCategories() ])
            result.append({'uid': product.UID(), 'title': product.Title(), 'price': product.getPrice(), 'categories': categories})

        return result

    def getSelectedCategories(self):
        """
        """
        selected_categories = self.request.get('search_category', [])
        if not isinstance(selected_categories, (list, tuple)):
            selected_categories = (
             selected_categories,)
        return selected_categories