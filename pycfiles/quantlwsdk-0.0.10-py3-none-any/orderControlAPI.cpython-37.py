# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\orderControlAPI.py
# Compiled at: 2020-04-02 03:37:05
# Size of source mod 2**32: 2742 bytes
"""
.. moduleauthor:: lw
"""
from pyalgotrade import commonHelpBylw
from apscheduler.schedulers.background import BackgroundScheduler
from pyalgotrade import config

def initABscheduler(tablename):
    sched = BackgroundScheduler()
    url = 'mysql+pymysql://admin:admin@192.168.10.81:3306/tradeprojectdata_lw?charset=utf8'
    sched.add_jobstore('sqlalchemy', url=url, tablename=tablename, engine_options={'pool_recycle': 21600})
    sched.start()
    return sched


class orderControlObj:
    __doc__ = 'lw李文实现的，用来封下单的一些控制动作的，基于掘金的下单函数的.\n\n    '

    def __init__(self, aNewTradeCalendar, tablename):
        self.symTradeTime = config.tradeTimeDict
        self.sched = initABscheduler(tablename)
        self.aNewTradeCalendar = aNewTradeCalendar

    def controlByOrderTime(self, datetimeStr, symbol, action, fun, funargs=None, funkargs=None):
        underlygingSym = commonHelpBylw.getMainContinContract(symbol)
        dateList = self.symTradeTime[underlygingSym]
        listLength = len(dateList)
        date_ = datetimeStr[0:10]
        time_ = datetimeStr[11:]
        for indx_ in range(listLength):
            currDateRange = dateList[indx_]
            if time_ == currDateRange[1]:
                nextInx_ = (indx_ + 1) % listLength
                nextTime_ = dateList[nextInx_][0]
                if nextTime_ < time_:
                    nextTDate = self.aNewTradeCalendar.tradingDaysOffset(date_, 1)
                    nextDatetime = nextTDate + ' ' + nextTime_
                if nextTime_ > time_:
                    nextDatetime = date_ + ' ' + nextTime_
                self.sched.add_job(fun, 'date', run_date=nextDatetime, misfire_grace_time=60, args=funargs, kwargs=funkargs, id=(symbol + '-' + nextDatetime + '-' + action))
                return True

        return False