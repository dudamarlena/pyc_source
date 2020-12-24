# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/criteria/content/product.py
# Compiled at: 2008-09-03 11:14:39
import transaction
from zope.interface import implements
from DateTime import DateTime
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from easyshop.core.config import *
from easyshop.core.interfaces import IProductCriteria
schema = Schema((StringField(name='title', widget=StringWidget(visible={'edit': 'invisible', 'view': 'invisible'}, label='Title', label_msgid='schema_title_label', i18n_domain='EasyShop'), required=0), LinesField(name='products', widget=MultiSelectionWidget(label='Products', label_msgid='schema_products_label', i18n_domain='EasyShop'), multiValued=1, vocabulary='getProductsAsDL')))

class ProductCriteria(BaseContent):
    """
    """
    __module__ = __name__
    implements(IProductCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def getProductsAsDL(self):
        """
        """
        dl = DisplayList()
        catalog = getToolByName(self, 'portal_catalog')
        for product in catalog.searchResults(portal_type=['Product', 'ProductVariant']):
            dl.add(product.id, product.Title)

        dl.add('shipping', 'Shipping')
        return dl

    def Title(self):
        """
        """
        return 'Products'

    def getValue(self):
        """
        """
        return (', ').join(self.getProducts())

    def _renameAfterCreation(self, check_auto_id=False):
        """Overwritten to set the default value for id"""
        transaction.commit()
        new_id = 'ProductCriteria'
        self.setId(new_id)


registerType(ProductCriteria, PROJECTNAME)