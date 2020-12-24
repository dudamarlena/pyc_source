# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkelleconf/workday.py
# Compiled at: 2020-01-24 07:29:17
# Size of source mod 2**32: 2773 bytes
import datetime as dt, sys, numpy as np, pandas_market_calendars as mcal

class workday:
    date = None
    whol = None
    holilist = []

    def holidays():
        us = mcal.get_calendar('NYSE')
        uk = mcal.get_calendar('LSE')
        eurex = mcal.get_calendar('EUREX')
        us_h = us.holidays()
        uk_h = uk.holidays()
        eurex_h = eurex.holidays()
        us_hol = np.asarray(us_h.holidays)
        uk_hol = np.asarray(uk_h.holidays)
        eurex_hol = np.asarray(eurex_h.holidays)
        hol = [us_hol, uk_hol, eurex_hol]
        holilist = []
        for i in range(len(hol)):
            myhol = hol[i]
            for j in range(len(myhol)):
                edate = myhol[j]
                if int(edate.item().year) == int(dt.date.today().strftime('%Y')):
                    eday = edate.item().day
                    emonth = edate.item().month
                    ehol = str(eday) + '-' + str(emonth)
                    if ehol in holilist:
                        pass
                    else:
                        holilist.append(ehol)
                        continue

        return holilist

    def __init__(self, date):
        mlist = [
         6, 7]
        holilist = workday.holidays()
        try:
            datew = dt.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            print('The date is wrong. Check format or date entry:', date)
            sys.exit(1)

        wday = datew.strftime('%-d')
        wmonth = datew.strftime('%-m')
        whol = wday + '-' + wmonth
        workday.whol = whol
        wd = datew.isoweekday()
        if int(wd) in mlist:
            recurs = 1
        else:
            recurs = 0
        if recurs == 1:
            datew = datew - dt.timedelta(days=1)
            workday.date = datew
            workday.holilist = holilist
            workday(str(datew))
        else:
            workday.whol = str(whol)
            workday.date = str(datew)
            workday.holilist = holilist

    def sdate(self):
        return self.date

    def hlist(self):
        return self.holilist

    def hol(self):
        return self.whol