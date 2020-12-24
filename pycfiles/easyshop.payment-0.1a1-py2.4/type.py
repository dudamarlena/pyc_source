# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/payment/adapters/type.py
# Compiled at: 2008-09-03 11:15:12
from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import ICreditCardPaymentMethod
from easyshop.core.interfaces import IDirectDebitPaymentMethod
from easyshop.core.interfaces import IGenericPaymentMethod
from easyshop.core.interfaces import IPayPalPaymentMethod
from easyshop.core.interfaces import IType

class CreditCardType:
    """Provides IType for direct debit content objects.
    """
    __module__ = __name__
    implements(IType)
    adapts(ICreditCardPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context

    def getType(self):
        """Returns type of credit card payment method.
        """
        return 'credit-card'


class DirectDebitType:
    """Provides IType for direct debit payment method.
    """
    __module__ = __name__
    implements(IType)
    adapts(IDirectDebitPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context

    def getType(self):
        """Returns type of direct debit payment method.
        """
        return 'direct-debit'


class GenericPaymentType:
    """Provides IType for simple payment content objects.
    """
    __module__ = __name__
    implements(IType)
    adapts(IGenericPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context

    def getType(self):
        """Returns type.
        """
        return 'generic-payment'


class PayPalType:
    """Provides IType for paypal content objects.
    """
    __module__ = __name__
    implements(IType)
    adapts(IPayPalPaymentMethod)

    def __init__(self, context):
        self.context = context

    def getType(self):
        """Returns type of EasyShopPrepayment.
        """
        return 'paypal'