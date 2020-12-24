# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/grs/BSR.py
# Compiled at: 2011-10-05 02:42:28


class BSR(object):
    """ 買賣進出紀錄 """

    def __init__(self, init_money=0):
        u"""
      init_money 期初金額
      store 庫存
      avgprice 買賣價格紀錄
    """
        self.money = init_money
        self.store = {}
        self.avgprice = {}

    def buy(self, no, price, value):
        u""" 買 """
        self.money += -price * value
        try:
            self.store[no] += value
        except:
            self.store[no] = value

        try:
            self.avgprice[no]['buy'] += [price]
        except:
            try:
                self.avgprice[no]['buy'] = [
                 price]
            except:
                self.avgprice[no] = {}
                self.avgprice[no]['buy'] = [
                 price]

    def sell(self, no, price, value):
        u""" 賣 """
        self.money += price * value
        try:
            self.store[no] += -value
        except:
            self.store[no] = -value

        try:
            self.avgprice[no]['sell'] += [price]
        except:
            try:
                self.avgprice[no]['sell'] = [
                 price]
            except:
                self.avgprice[no] = {}
                self.avgprice[no]['sell'] = [
                 price]

    def showinfo(self):
        u""" 總覽顯示 """
        print 'money:', self.money
        print 'store:', self.store
        print 'avgprice:', self.avgprice