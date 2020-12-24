# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/stocks/browser/stock_information_container_view.py
# Compiled at: 2008-09-03 11:15:30
from Products.Five.browser import BrowserView
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IStockManagement

class StockInformationContainerView(BrowserView):
    """
    """
    __module__ = __name__

    def getStockInformations(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        sm = IStockManagement(shop)
        result = []
        for stock_information in sm.getStockInformations():
            data = IData(stock_information).asDict()
            result.append({'id': stock_information.getId(), 'title': stock_information.Title(), 'description': stock_information.Description(), 'available': data['available'], 'time_period': data['time_period'], 'url': stock_information.absolute_url(), 'up_url': '%s/es_folder_position?position=up&id=%s' % (self.context.absolute_url(), stock_information.getId()), 'down_url': '%s/es_folder_position?position=down&id=%s' % (self.context.absolute_url(), stock_information.getId()), 'amount_of_criteria': len(stock_information.objectIds())})

        return result