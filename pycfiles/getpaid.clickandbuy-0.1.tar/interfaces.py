# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/olauzanne/workspace/paguro/getpaid.clickandbuy/getpaid/clickandbuy/interfaces.py
# Compiled at: 2009-01-30 04:18:04
from getpaid.core import interfaces
from zope import schema

class IClickAndBuyStandardProcessor(interfaces.IPaymentProcessor):
    """
    Click and Buy Standard Processor
    """
    __module__ = __name__


class IClickAndBuyStandardOptions(interfaces.IPaymentProcessorOptions):
    """
    Click and Buy Standard Options
    """
    __module__ = __name__
    premium_url = schema.ASCIILine(title='premium URL')
    seller_id = schema.Int(title='SellerID')
    tm_password = schema.ASCIILine(title='TMI-Password')