# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkelleloader/loadstockhisteod.py
# Compiled at: 2020-01-24 20:23:33
# Size of source mod 2**32: 12637 bytes
"""
Created on Sat Jul  6 11:25:21 2019

@author: debmishra
"""
import lykkelleconf.connecteod as c
import lykkelleconnector.geteodstock as ysh
import datetime as dt
import lykkelleconf.workday as wd
import sys
import lykkelleconf.time2epoch2time as et
import psycopg2 as pgs, time, os, pandas as pd, math
home = os.path.expanduser('~')

class loadstockhist:

    def stockhist(ticker, todate, fromdate, sourcetable, cursor):
        loaddata = []
        fromdate = fromdate.strftime('%Y-%m-%d')
        todate = todate.strftime('%Y-%m-%d')
        if todate == fromdate:
            print('the dates used for history calculation are same.\n                  History requires delta of dates. Moving to next ticker')
            status = -999
            header = None
        else:
            histr = ysh(ticker, fromdate, todate)
            status = histr.sts
            header = histr.header
        att = 0
        while status != 200:
            if status != -999:
                if att <= 5:
                    print('begins wait of 30 sec. att-', att)
                    time.sleep(30)
                    histr = ysh(ticker, fromdate, todate)
                    status = histr.sts
                    header = histr.header
                    att = att + 1
            else:
                print('even after 6 reattempts not getting status code 200')
                status = -899
                break

        if status == 200:
            val = histr.stock_Response
            if val is not None:
                lt = len(val)
                if lt > 0:
                    load = 0
                    badload = 0
                    ldate = []
                    lprice = []
                    lvolume = []
                    lticker = []
                    lsource = []
                    for i in range(lt):
                        try:
                            volume = val[i].get('volume')
                            if volume is not None and volume > 0:
                                volume = math.floor(volume)
                                volume = int(volume)
                            else:
                                volume = 0
                        except AttributeError:
                            volume = None

                        try:
                            close = val[i].get('adjusted_close')
                        except AttributeError:
                            try:
                                close = val[i].get('close')
                            except AttributeError:
                                close = None

                        try:
                            pricedate = val[i].get('date')
                        except AttributeError:
                            pricedate = None

                        if pricedate is not None and close is not None:
                            if 'benchmark' in sourcetable:
                                delq = 'delete from benchmark_history where symbol=%s\n                                        and price_date between %s and %s'
                                copq = 'benchmark_history'
                            else:
                                delq = 'delete from stock_history where symbol=%s\n                                        and price_date between %s and %s'
                                copq = 'stock_history'
                            try:
                                ldate.append(pricedate)
                                lprice.append(close)
                                lvolume.append(volume)
                                lticker.append(ticker)
                                lsource.append(sourcetable)
                                load = load + 1
                            except Exception as e:
                                try:
                                    badload = badload + 1
                                    print(e)
                                finally:
                                    e = None
                                    del e

                        else:
                            print('Failed load for ', ticker, ' had a close price of ', close, 'for date ', pricedate)

                    data = {'ticker':lticker, 
                     'pricedate':ldate, 
                     'price':lprice, 
                     'volume':lvolume, 
                     'sourcetable':lsource}
                    myfile = './tmp/ticker.csv'
                    df = pd.DataFrame(data, columns=['ticker', 'pricedate', 'price', 'volume', 'sourcetable'])
                    df.to_csv(myfile, index=None, header=False)
                    cursor.execute(delq, (ticker, fromdate, todate))
                    f = open(myfile, 'r')
                    cursor.copy_from(f, copq, columns=('symbol', 'price_date', 'price',
                                                       'volume', 'source_table'), sep=',')
                    f.close()
                    os.remove(myfile)
                    loaddata = [ticker, load, badload]
                    return loaddata
                print('No history data found for ticker', ticker, 'and dates ', fromdate, ':', todate)
                loaddata = [ticker, 'fail']
                return loaddata
            else:
                print('No history data found for ticker', ticker, 'and dates ', fromdate, ':', todate)
                loaddata = [status, ticker]
                return loaddata
        else:
            if status == -899:
                print('Error code 200 after 5 attempts for ticker', ticker, 'and dates ', fromdate, ':', todate)
                loaddata = [ticker, 'fail']
                if header is not None:
                    ldate = dt.date.today()
                    ldate = wd.workday(str(ldate)).sdate()
                    myheader = header.get('X-RateLimit-Remaining')
                else:
                    myheader = None
                desc = (
                 ticker + ':' + str(fromdate) + ':' + str(todate) + ':=', status)
                nrtbl = 'insert into ticker_no_response_list\n            (symbol, load_date,src,"description",tablename,errorcode,headeroutput)\n            values (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING'
                cursor.execute(nrtbl, (ticker, ldate, 'mhistory', desc, sourcetable, status, myheader))
                return loaddata
            print('Ignored as data already present for ticker', ticker, 'and dates ', fromdate, ':', todate)
            loaddata = [ticker, 'ignore']
            return loaddata

    def __init__(self, ticker, sourcetable, mode, jday, cursor):
        self.ticker = ticker
        self.sourcetable = sourcetable
        td = dt.date.today()
        iwd = td.isoweekday()
        todate = wd.workday(str(td)).sdate()
        todate = dt.datetime.strptime(todate, '%Y-%m-%d').date()
        modevalue = ['A', 'M']
        if mode in modevalue:
            pass
        else:
            print('Possible entries in mode are A or M. System will exit now')
            sys.exit(1)
        if not iwd == 6:
            if iwd == 7 or mode == 'M':
                if 'benchmark' in self.sourcetable:
                    maxdate = 'select max(price_date) from benchmark_history\n                        where symbol = %s'
                    mindate = 'select min(price_date) from benchmark_history\n                        where symbol = %s'
                else:
                    maxdate = 'select max(price_date) from stock_history\n                        where symbol = %s'
                    mindate = 'select min(price_date) from stock_history\n                        where symbol = %s'
                cursor.execute(maxdate, (ticker,))
                md = cursor.fetchone()
                cursor.execute(mindate, (ticker,))
                mid = cursor.fetchone()
                md = md[0]
                mid = mid[0]
                eparam = 1
                if not md is None:
                    if md == mid or mode == 'M':
                        wks = 780
                        fromdate = todate - dt.timedelta(weeks=wks)
                elif md < todate - dt.timedelta(days=2):
                    fromdate = md
                else:
                    eparam = 0
                if eparam == 0:
                    print('No valid history since the max history date is equal or > to latest date for symbol:', self.ticker)
                    jobload = "update jobrunlist\n                set runstatus = 'ignored' where symbol=%s and\n                runsource='mhistory' and rundate=%s and jobtable=%s "
                    try:
                        cursor.execute(jobload, (ticker, jday, sourcetable))
                        print(ticker, ' job executed successfully')
                    except pgs.Error as e:
                        try:
                            print(e.pgerror)
                        finally:
                            e = None
                            del e

                else:
                    shload = loadstockhist.stockhist(self.ticker, todate, fromdate, self.sourcetable, cursor)
                    ignr = 0
                    if shload[1] == 'fail':
                        print('the ticker ', shload[0], "didn't find a result from eodhd")
                        rdate = dt.datetime.today().date()
                        print('date for no response:', rdate)
                        print(shload[0], ' was not able to fetch history data from EODHD even after 5 attempts')
                    else:
                        if shload[1] == 'ignore':
                            print('the ticker ', shload[0], ' was ignored from run as data already present')
                            rdate = dt.datetime.today().date()
                            print('date for no response:', rdate)
                            print(shload[0], ' was ignored as data already present')
                            ignr = 1
                        else:
                            if isinstance(shload[0], int) is True and shload[0] != -999:
                                rdate = dt.datetime.today().date()
                                print('date for no response:', rdate)
                                print(self.ticker, ' was not able to fetch history data from EODHD even after 5 attempts')
                            else:
                                if isinstance(shload[0], int) is True and shload[0] == -999:
                                    print(self.ticker, "'s history is too recent. There should be at least>1 days delta")
                                    ignr = 1
                                else:
                                    print('For the ticker:', shload[0], ', total of ', shload[1], ' number of successful records were loaded and ', shload[2], ' number of records could not be loaded')
                    if ignr == 1:
                        jobload = "update jobrunlist\n                    set runstatus = 'ignored' where symbol=%s and\n                    runsource='mhistory' and rundate=%s and jobtable=%s "
                        try:
                            cursor.execute(jobload, (ticker, jday, sourcetable))
                            print(ticker, ' job executed successfully')
                        except pgs.Error as e:
                            try:
                                print(e.pgerror)
                            finally:
                                e = None
                                del e

                    else:
                        jobload = "update jobrunlist\n                    set runstatus = 'complete' where symbol=%s and\n                    runsource='mhistory' and rundate=%s and jobtable=%s "
                        try:
                            cursor.execute(jobload, (ticker, jday, sourcetable))
                            print(ticker, ' job executed successfully')
                        except pgs.Error as e:
                            try:
                                print(e.pgerror)
                            finally:
                                e = None
                                del e

        else:
            print('not a weekend. scrapping history run')
            sys.exit(1)