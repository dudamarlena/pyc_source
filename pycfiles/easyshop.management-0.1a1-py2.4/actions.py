# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/management/viewlets/actions.py
# Compiled at: 2008-09-03 11:15:03
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import ICategoryManagement

class ActionsViewlet(ViewletBase):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('actions.pt')

    def getSelectedCategories(self):
        """
        """
        selected_categories = self.request.get('search_category', [])
        if not isinstance(selected_categories, (list, tuple)):
            selected_categories = (
             selected_categories,)
        return selected_categories

    def getSelectedProducts(self):
        """
        """
        selected_uids = self.request.get('selected_uids')
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(UID=selected_uids)
        result = []
        for brain in brains:
            product = brain.getObject()
            cm = ICategoryManagement(product)
            categories = cm.getTopLevelCategories()
            categories = (', ').join([ c.Title() for c in categories ])
            result.append({'uid': product.UID(), 'id': product.getId(), 'title': product.Title(), 'price': product.getPrice(), 'categories': categories})

        return result

    def showChangePrice(self):
        """
        """
        return self.request.get('action') == 'change_price'

    def showRename(self):
        """
        """
        return self.request.get('action') == 'rename'

    def showAddToGroup(self):
        """
        """
        return self.request.get('action') == 'add_to_group'

    def showChangeCategory(self):
        """
        """
        return self.request.get('action') in 'change_category'