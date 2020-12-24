# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\utils\universe.py
# Compiled at: 2018-10-30 03:07:31
# Size of source mod 2**32: 1856 bytes


class Universe(object):
    universeCache = {}

    def __init__(self, var):
        self.var = var

    def __initstock(self, universe):
        allStocks = self.var.retrieveAllStocks()
        if universe == 1 or universe == 3 or universe == 5 or universe == 7:
            if self.var._FRAMEWORK_MARKETTYPE == 'CN':
                return []
            else:
                if universe in Universe.universeCache.keys():
                    universeSeries = Universe.universeCache[universe]
                else:
                    universeSeries = self.var.ips_api._framework_getStockUniverse(universe)
                    Universe.universeCache[universe] = universeSeries
                return allStocks.loc[universeSeries.values].sort_index(ascending=True).asset.tolist()
        else:
            if universe == 4:
                if self.var._FRAMEWORK_MARKETTYPE == 'CN':
                    return allStocks[(allStocks.sec_type == 25)].sort_index(ascending=True).asset.tolist()
                else:
                    return []
            else:
                if self.var._FRAMEWORK_MARKETTYPE == 'CN':
                    return allStocks[(allStocks.sec_type == 24)].sort_index(ascending=True).asset.tolist()
                else:
                    return allStocks.sort_index(ascending=True).asset.tolist()

    def stock_1000(self):
        return self._Universe__initstock(1)

    def etf_100(self):
        return self._Universe__initstock(3)

    def stock_sp500(self):
        return self._Universe__initstock(5)

    def stock_500(self):
        return self._Universe__initstock(7)

    def stock_2000(self):
        return self._Universe__initstock(0)

    def stock_all(self):
        return self._Universe__initstock(2)

    def etf_all(self):
        return self._Universe__initstock(4)