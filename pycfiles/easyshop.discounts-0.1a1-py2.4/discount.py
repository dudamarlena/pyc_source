# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/discounts/content/discount.py
# Compiled at: 2008-09-03 11:14:47
from zope.interface import implements
from Products.Archetypes.atapi import *
from easyshop.core.config import _
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IDiscount
schema = Schema((TextField(name='description', accessor='Description', widget=TextAreaWidget(label='Description', description='A short summary of the content', label_msgid='label_description', description_msgid='help_description', i18n_domain='plone')), StringField(name='type', schemata='advanced', vocabulary='_getTypesAsDL', default='absolute', widget=SelectionWidget(label='Type', label_msgid='schema_type_label', description='', description_msgid='schema_type_description', i18n_domain='EasyShop')), StringField(name='base', schemata='advanced', vocabulary='_getBasesAsDL', default='product', widget=SelectionWidget(label='Base', label_msgid='schema_base_label', description='', description_msgid='schema_base_description', i18n_domain='EasyShop')), FloatField(name='value', default=0.0, widget=DecimalWidget(label='Value', label_msgid='schema_value_label', description='The discount which is given.', description_msgid='schema_value_description', i18n_domain='EasyShop'))))

class Discount(OrderedBaseFolder):
    """A discount for cart items.
    """
    __module__ = __name__
    implements(IDiscount)
    _at_rename_after_creation = True
    schema = OrderedBaseFolderSchema.copy() + schema.copy()

    def _getTypesAsDL(self):
        """
        """
        dl = DisplayList()
        dl.add('absolute', _('Absolute'))
        dl.add('percentage', _('Percentage'))
        return dl

    def _getBasesAsDL(self):
        """
        """
        dl = DisplayList()
        dl.add('product', _('Product'))
        dl.add('cart_item', _('Cart Item'))
        return dl


registerType(Discount, PROJECTNAME)