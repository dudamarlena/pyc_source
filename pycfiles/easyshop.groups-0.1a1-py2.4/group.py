# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/groups/content/group.py
# Compiled at: 2008-09-03 11:14:50
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import *
from easyshop.core.interfaces import IProductGroup
from easyshop.core.interfaces import IShopManagement
from easyshop.core.config import *
schema = Schema((TextField(name='description', widget=TextAreaWidget(label='Description', label_msgid='schema_help_description', description='A short summary of the content', description_msgid='schema_help_description', i18n_domain='plone')), ReferenceField(name='products', multiValued=1, relationship='groups_products', allowed_types=('Product', ), widget=ReferenceBrowserWidget(label='Products', label_msgid='schema_products_label', description='Please select all products, which should associated with this category.', description_msgid='schema_products_description', i18n_domain='EasyShop', show_path=1, allow_search=1, allow_browse=1, allow_sorting=1, restrict_browsing_to_startup_directory=1, startup_directory='getStartupDirectoryForProducts', available_indexes={'Title': "Product's Title", 'SearchableText': 'Free text search', 'Description': "Object's description"}))))

class ProductGroup(BaseFolder):
    """Arrange products to a group, which can be associated with taxes, 
    discounts, etc. A group is invisible for customers.
    """
    __module__ = __name__
    implements(IProductGroup)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def getStartupDirectoryForProducts(self):
        """
        """
        shop = IShopManagement(self).getShop()
        return ('/').join(shop.getPhysicalPath()) + '/products'


registerType(ProductGroup, PROJECTNAME)