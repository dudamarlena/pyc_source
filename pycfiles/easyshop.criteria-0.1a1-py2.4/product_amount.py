# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/criteria/content/product_amount.py
# Compiled at: 2008-09-03 11:14:39
from zope.interface import implements
from Products.Archetypes.atapi import *
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IProductAmountCriteria
schema = Schema((FloatField(name='amount', default=0.0, widget=DecimalWidget(label='Amount of Products', label_msgid='schema_amount_of_products_label', description='The amount of same products', description_msgid='schema_amount_of_products_description', i18n_domain='EasyShop')),))
schema = BaseSchema.copy() + schema.copy()
schema['title'].required = False
schema['title'].visible = {'edit': 'invisible', 'view': 'invisible'}

class ProductAmountCriteria(BaseContent):
    """
    """
    __module__ = __name__
    implements(IProductAmountCriteria)
    _at_rename_after_creation = True
    schema = schema

    def Title(self):
        """
        """
        return 'Amount Of Products'

    def getValue(self):
        """
        """
        return self.getAmount()


registerType(ProductAmountCriteria, PROJECTNAME)