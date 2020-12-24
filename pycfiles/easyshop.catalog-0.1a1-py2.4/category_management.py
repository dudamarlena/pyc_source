# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/adapters/category_management.py
# Compiled at: 2008-09-03 11:14:27
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import IProductVariant
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IShop

class CategoryCategoryManagement(object):
    """Adapter which provides ICategoryManagement for category content 
    objects.
    """
    __module__ = __name__
    implements(ICategoryManagement)
    adapts(ICategory)

    def __init__(self, context):
        """
        """
        self.context = context

    def getCategories(self):
        """
        """
        self.categories = []
        for category in self.getTopLevelCategories():
            self.categories.append(category)
            self._getCategories(category)

        return self.categories

    def _getCategories(self, parent_category):
        """
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(object_provides='easyshop.core.interfaces.catalog.ICategory', getParentCategory=parent_category.UID(), sort_on='getPositionInParent')
        for brain in brains:
            category = brain.getObject()
            self.categories.append(category)
            self._getCategories(category)

    def getTopLevelCategories(self):
        """Returns objects.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(object_provides='easyshop.core.interfaces.catalog.ICategory', getParentCategory=self.context.UID(), sort_on='getPositionInParent')
        return [ brain.getObject() for brain in brains ]


class ProductCategoryManagement(object):
    """Adapter which provides ICategoryManagement for product content objects.
    """
    __module__ = __name__
    implements(ICategoryManagement)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context

    def getCategories(self):
        """
        """
        return self.context.getCategories()

    def getTopLevelCategories(self):
        """Returns objects.
        """
        try:
            mtool = getToolByName(self.context, 'portal_membership')
            categories = self.context.getBRefs('categories_products')
        except AttributeError:
            return []

        result = []
        for category in categories:
            if mtool.checkPermission('View', category):
                result.append(category)

        return result


class ProductVariantCategoryManagement(object):
    """Adapter which provides ICategoryManagement for product content objects.
    """
    __module__ = __name__
    implements(ICategoryManagement)
    adapts(IProductVariant)

    def __init__(self, context):
        """
        """
        self.context = context
        self.product = context.aq_inner.aq_parent

    def getCategories(self):
        """Returns brains.
        """
        return ICategoryManagement(self.product).getCategories()

    def getTopLevelCategories(self):
        """Returns objects.
        """
        return ICategoryManagement(self.product).getTopLevelCategories()


class ShopCategoryManagement(object):
    """An adapter which provides ICategoryManagement for shop content objects.
    """
    __module__ = __name__
    implements(ICategoryManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context

    def getCategories(self):
        """Returns brains.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), object_provides='easyshop.core.interfaces.catalog.ICategory', sort_on='getPositionInParent')
        return brains

    def getTopLevelCategories(self):
        """Returns objects.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(path=('/').join(self.context.getPhysicalPath()), object_provides='easyshop.core.interfaces.catalog.ICategory', sort_on='getPositionInParent', getParentCategory=None)
        return [ brain.getObject() for brain in brains ]