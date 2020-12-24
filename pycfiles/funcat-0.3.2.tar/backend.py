# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cedricporter/git/funcat/funcat/data/backend.py
# Compiled at: 2017-04-18 08:40:20


class DataBackend(object):
    skip_suspended = True

    def get_price(self, order_book_id, start, end, freq):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :param freq: 1m 1d 5m 15m ...
        :returns:
        :rtype: numpy.rec.array
        """
        raise NotImplementedError

    def get_order_book_id_list(self):
        u"""获取所有的
        """
        raise NotImplementedError

    def get_trading_dates(self, start, end):
        u"""获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        raise NotImplementedError

    def symbol(self, order_book_id):
        u"""获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        raise NotImplementedError