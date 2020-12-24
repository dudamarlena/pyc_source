# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/management/viewlets/categories.py
# Compiled at: 2008-09-03 11:15:03
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IShopManagement

class CategoriesViewlet(ViewletBase):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('categories.pt')

    def getCategories(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        return self._getCategories(shop)

    def hasSelectedCategories(self):
        """
        """
        selected_categories = self.request.get('selected_category', [])
        if not isinstance(selected_categories, (list, tuple)):
            selected_categories = (
             selected_categories,)
        return len(selected_categories) > 0

    def _getCategories(self, obj):
        """
        """
        selected_categories = self.request.get('selected_category', [])
        if not isinstance(selected_categories, (list, tuple)):
            selected_categories = (
             selected_categories,)
        categories = []
        tl_categories = ICategoryManagement(obj).getTopLevelCategories()
        for tl_category in tl_categories:
            if tl_category.UID == self.context.UID():
                klass = 'current-category'
            else:
                klass = ''
            selected = tl_category.UID() in selected_categories
            if selected or self._isChildOfSelected(tl_category):
                display_checkbox = False
            else:
                display_checkbox = True
            if tl_category.UID() in self.request.SESSION.get('extended', []):
                children_class = 'extended'
            else:
                children_class = 'collapsed'
            categories.append({'title': tl_category.Title(), 'uid': tl_category.UID(), 'url': tl_category.absolute_url, 'selected': selected, 'display_checkbox': display_checkbox, 'children': self._getCategories(tl_category), 'class': klass, 'children_class': children_class})

        return categories

    def _isChildOfSelected(self, category):
        """Returns true if given category is child of any selected category.
        """
        selected_categories = self.request.get('selected_category', [])
        if not isinstance(selected_categories, (list, tuple)):
            selected_categories = (
             selected_categories,)
        while category is not None:
            if category.UID() in selected_categories:
                return True
            category = category.getParentCategory()

        return False