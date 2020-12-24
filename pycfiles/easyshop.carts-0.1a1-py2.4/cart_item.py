# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/carts/content/cart_item.py
# Compiled at: 2008-09-03 11:14:22
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from easyshop.core.interfaces import ICartItem
from easyshop.carts.config import PROJECTNAME
schema = Schema((IntegerField(name='amount', default='1', widget=IntegerWidget(label='Amount', label_msgid='schema_amount_label', i18n_domain='EasyShop')), DataGridField('properties', searchable=True, columns=('id', 'selected_option'), widget=DataGridWidget(columns={'id': Column('ID'), 'selected_option': Column('Selected Option')})), ReferenceField(name='product', widget=ReferenceWidget(label='Product', label_msgid='schema_easyshop_products_label', i18n_domain='EasyShop'), allowed_types=('Product', ), multiValued=0, relationship='cartitem_product')))

class CartItem(BaseContent):
    """A cart item holds a product, the quantity of the product and the 
    choosen properties.
    """
    __module__ = __name__
    implements(ICartItem)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def getProduct(self):
        """Returns product of the item or None.
        """
        try:
            return self.getRefs('cartitem_product')[0]
        except IndexError:
            return

        return

    def setProduct(self, product):
        """Sets the product of the cart item.
        """
        self.deleteReferences('cartitem_product')
        self.addReference(product, 'cartitem_product')


registerType(CartItem, PROJECTNAME)