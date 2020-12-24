# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/stocks/adapters/data.py
# Compiled at: 2008-09-03 11:15:30
from zope.component import adapts
from zope.interface import implements
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IStockInformation

class StockInformationData:
    """
    """
    __module__ = __name__
    implements(IData)
    adapts(IStockInformation)

    def __init__(self, context):
        """
        """
        self.context = context

    def asDict(self):
        """
        """
        delivery_min = self.context.getDeliveryTimeMin()
        delivery_max = self.context.getDeliveryTimeMax()
        time_unit = self.context.getDeliveryTimeUnit()
        if delivery_min == delivery_max:
            if delivery_min == '1':
                time_unit = time_unit[:-1]
            time_period = delivery_min
        else:
            time_period = '%s-%s' % (delivery_min, delivery_max)
        return {'available': self.context.getAvailable(), 'time_period': time_period, 'time_unit': time_unit, 'url': self.context.absolute_url()}