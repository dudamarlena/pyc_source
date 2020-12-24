# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/payment/content/payment_price.py
# Compiled at: 2008-09-03 11:15:14
from zope.interface import implements
from Products.Archetypes.atapi import *
from easyshop.core.config import *
from easyshop.core.interfaces import IPaymentPrice
schema = Schema((TextField('description', default='', searchable=1, accessor='Description', widget=TextAreaWidget(label='Description', description='A short summary of the content', label_msgid='label_description', description_msgid='help_description', i18n_domain='plone')), FloatField(name='price', required=True, widget=DecimalWidget(size='10', label='Price', label_msgid='schema_price_label', i18n_domain='EasyShop'))))

class PaymentPrice(OrderedBaseFolder):
    """Represents a price for payment methods. Has criteria which makes it
    possible for the payment manager to calculate a payment price.
    """
    __module__ = __name__
    implements(IPaymentPrice)
    _at_rename_after_creation = True
    schema = BaseFolderSchema.copy() + schema.copy()


registerType(PaymentPrice, PROJECTNAME)