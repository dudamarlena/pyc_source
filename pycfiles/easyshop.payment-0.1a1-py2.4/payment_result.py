# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/payment/content/payment_result.py
# Compiled at: 2008-09-03 11:15:14
from zope.interface import implements
from easyshop.core.interfaces import IPaymentResult

class PaymentResult(object):
    """A payment result is returned by all payment processors.
    """
    __module__ = __name__
    implements(IPaymentResult)

    def __init__(self, code, message=''):
        """
        """
        self.code = code
        self.message = message