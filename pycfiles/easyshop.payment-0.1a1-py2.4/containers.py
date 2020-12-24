# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/payment/content/containers.py
# Compiled at: 2008-09-03 11:15:14
from zope.interface import implements
from Products.Archetypes.atapi import *
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IPaymentMethodsContainer
from easyshop.core.interfaces import IPaymentPriceManagementContainer

class PaymentMethodsContainer(OrderedBaseFolder):
    """A simple container to hold payment methods.
    """
    __module__ = __name__
    implements(IPaymentMethodsContainer)


class PaymentPricesContainer(OrderedBaseFolder):
    """A simple container to hold payment prices.
    """
    __module__ = __name__
    implements(IPaymentPriceManagementContainer)


registerType(PaymentMethodsContainer, PROJECTNAME)
registerType(PaymentPricesContainer, PROJECTNAME)