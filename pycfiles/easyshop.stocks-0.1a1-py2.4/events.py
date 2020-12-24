# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/stocks/events.py
# Compiled at: 2008-09-03 11:15:30
from zope.interface import implements
from easyshop.core.interfaces import IStockAmountIsZeroEvent

class StockAmountIsZeroEvent(object):
    """
    """
    __module__ = __name__
    implements(IStockAmountIsZeroEvent)

    def __init__(self, product):
        """
        """
        self.product = product