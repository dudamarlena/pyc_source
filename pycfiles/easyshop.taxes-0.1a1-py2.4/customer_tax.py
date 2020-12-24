# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/taxes/content/customer_tax.py
# Compiled at: 2008-09-03 11:15:45
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.Archetypes.atapi import *
from easyshop.core.config import *
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import ITax
schema = Schema((FloatField(name='rate', widget=DecimalWidget(label='Rate', label_msgid='schema_rate_label', i18n_domain='EasyShop')),))

class CustomerTax(OrderedBaseFolder):
    """Represents taxes for customers.
    
    This is used to calculate the price for the customer on base of the net
    price.
    
    It is able to hold criteria which let the tax manager decide which tax is
    taken for a customer / product / category / group / date / ...
    """
    __module__ = __name__
    implements(ITax)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = OrderedBaseFolderSchema.copy() + schema.copy()


registerType(CustomerTax, PROJECTNAME)