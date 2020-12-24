# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/grs/twseopen.py
# Compiled at: 2011-10-05 02:42:28
from cttwt import TWTime
import csv
from datetime import datetime
_CSVFILEPATH = __name__.split('.')[(-2)]

class twseopen(object):
    """ 判斷當日是否開市 """

    def __init__(self, time):
        if type(TWTime().now) == type(time):
            self.twtime = TWTime().now
        elif type(TWTime().date) == type(time):
            self.twtime = TWTime().date
        self.ptime = time
        self.ocdate = self.loaddate()

    def loaddate(self):
        u""" 載入檔案
        檔案依據 http://www.twse.com.tw/ch/trading/trading_days.php
    """
        ld = csv.reader(open('./%s/opendate.csv' % _CSVFILEPATH, 'r'))
        re = {}
        re['close'] = []
        re['open'] = []
        for i in ld:
            if i[1] == '0':
                re['close'] += [datetime.strptime(i[0], '%Y/%m/%d').date()]
            elif i[1] == '1':
                re['open'] += [datetime.strptime(i[0], '%Y/%m/%d').date()]

        return re

    def ooc(self):
        u""" Open or close
        回傳 True：開市，False：休市。
    """
        if self.ptime.date() in self.ocdate['close']:
            return False
        else:
            if self.ptime.date() in self.ocdate['open']:
                return True
            if self.ptime.weekday() <= 4:
                return True
            return False