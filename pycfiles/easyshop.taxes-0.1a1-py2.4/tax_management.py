# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/taxes/adapters/tax_management.py
# Compiled at: 2008-09-03 11:15:45
from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import ITaxManagement

class TaxManagement:
    """An adapter, which provides methods to manage tax objects for shop context
    objects.
    """
    __module__ = __name__
    implements(ITaxManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.taxes = self.context.taxes

    def getCustomerTaxes(self):
        """
        """
        return self.taxes.objectValues('CustomerTax')

    def getDefaultTaxes(self):
        """
        """
        return self.taxes.objectValues('DefaultTax')

    def getTax(self, id):
        """
        """
        try:
            return self.taxes[id]
        except KeyError:
            return

        return