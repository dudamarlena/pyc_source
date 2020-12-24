# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/customers/adapters/completeness.py
# Compiled at: 2008-09-03 11:14:43
from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import IAddress
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import ICustomer
from easyshop.core.interfaces import IShopManagement

class CustomerCompleteness:
    """
    """
    __module__ = __name__
    implements(ICompleteness)
    adapts(ICustomer)

    def __init__(self, context):
        """
        """
        self.context = context

    def isComplete(self):
        """Checks weather the customer is complete to checkout.
        
           Customer completeness means the customer is ready to check out:
             1. Invoice address is complete
             2. Shipping address is complete
             3. Selected payment method is complete
             4. There a items in the cart            
        """
        shop = IShopManagement(self.context).getShop()
        adressman = IAddressManagement(self.context)
        s_addr = adressman.getShippingAddress()
        if s_addr is None:
            return False
        i_addr = adressman.getInvoiceAddress()
        if i_addr is None:
            return False
        pm = IPaymentInformationManagement(self.context)
        payment_method = pm.getSelectedPaymentMethod()
        cart = ICartManagement(shop).getCart()
        if cart is None:
            return False
        im = IItemManagement(cart)
        for toCheck in (s_addr, i_addr, payment_method):
            if ICompleteness(toCheck).isComplete() == False:
                return False

        if im.hasItems() == False:
            return False
        return True


class AddressCompleteness:
    """Provides ICompleteness for address content objects
    """
    __module__ = __name__
    implements(ICompleteness)
    adapts(IAddress)

    def __init__(self, context):
        """
        """
        self.context = context

    def isComplete(self):
        """Checks the completeness of an address.
        """
        if len(self.context.address_1) == 0:
            return False
        elif len(self.context.zip_code) == 0:
            return False
        elif len(self.context.city) == 0:
            return False
        elif len(self.context.country) == 0:
            return False
        return True