# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/adapters/validity.py
# Compiled at: 2008-09-03 11:15:25
from zope.interface import implements
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IValidity

class Validity(object):
    """An adapter which provides IValidity for several classes. See 
    configure.zcml for more information.
    """
    __module__ = __name__
    implements(IValidity)

    def __init__(self, context):
        """
        """
        self.context = context

    def isValid(self, product=None):
        """Returns true if all contained criteria are true.
        """
        for criteria in self.context.objectValues():
            try:
                if criteria.isValid(product) == False:
                    return False
            except AttributeError:
                if IValidity(criteria).isValid(product) == False:
                    return False

        return True


class PayPalValidity(Validity):
    """An adapter which provides IValidity for PayPal payment method.
    """
    __module__ = __name__
    implements(IValidity)

    def __init__(self, context):
        """
        """
        self.context = context

    def isValid(self, product=None):
        """Returns False if the PayPal id is not filled in.
        """
        shop = IShopManagement(self.context).getShop()
        if shop.getPayPalId() == '':
            return False
        return super(PayPalValidity, self).isValid(product)