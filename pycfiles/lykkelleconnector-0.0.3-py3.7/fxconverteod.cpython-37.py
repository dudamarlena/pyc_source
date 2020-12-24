# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkelleconnector/fxconverteod.py
# Compiled at: 2020-01-24 12:14:31
# Size of source mod 2**32: 8154 bytes
"""
Created on Wed Jul 10 23:35:00 2019

@author: debmishra
"""
import requests as req, json as js
import lykkelleconf.connecteod as c
import psycopg2 as pgs, datetime as dt
import lykkelleconf.time2epoch2time as tet
import lykkelleconf.workday as workday

class fxconvert:

    def __init__(self, cursor):
        pdate = dt.datetime.today()
        hr = dt.datetime.strftime(pdate, '%H')
        hr = int(hr)
        if hr < 11:
            pdate = dt.datetime.today().date() - dt.timedelta(days=1)
        else:
            pdate = dt.datetime.today().date()
        pdate = dt.datetime.strftime(pdate, '%Y-%m-%d')
        pdate = workday(pdate).sdate()
        basecurr = 'EUR'
        currqry = "select distinct currency from\n        ((select distinct currency from dbo.benchmark_All where currency is not null and currency<>'GLBL'\n        union\n        select distinct currency from ref_currency where is_active is true)\n        except\n        select currency from currency where currency_date>=%s) a\n        "
        cur_rate = {}
        cnt = 0
        latestcurr = []
        stalecurr = []
        lcur = 1
        while lcur > 0 and cnt < 3:
            try:
                cursor.execute(currqry, (pdate,))
                currlist = cursor.fetchall()
                lcur = len(currlist)
            except pgs.Error as e:
                try:
                    print('the query to get currency list from system failed')
                    print(e.pgerror)
                    lcur = 0
                finally:
                    e = None
                    del e

            for i in range(lcur):
                tgtcurr = currlist[i][0]
                currsym = basecurr + tgtcurr + '.FOREX'
                url = 'https://eodhistoricaldata.com/api/real-time/' + currsym
                params = {'api_token':'5d80cd89e4b201.98976318',  'fmt':'json'}
                response = req.request('GET', url, params=params)
                if response.status_code == 200:
                    cnt = 4
                    quotedata = response.json()
                    print(type(quotedata))
                    if type(quotedata) == dict:
                        currpair = quotedata
                        curr = currpair.get('code')
                        tgtcurr = curr[3:6]
                        cd = currpair.get('timestamp')
                        currdate = tet.epoch2dateeod(cd)
                        curclose = currpair.get('close')
                        print(tgtcurr, currdate, curclose)
                        if currdate is None:
                            if curr == 'EUREUR.FOREX':
                                tgtcurr = 'EUR'
                                curclose = 1
                                currdate = pdate
                                try:
                                    cq = 'insert into dbo.currency (currency,rate,currency_date)\n                                    values (%s,%s,%s) ON CONFLICT (currency, currency_date)\n                                    DO UPDATE SET rate = EXCLUDED.rate'
                                    cursor.execute(cq, (tgtcurr, curclose, currdate))
                                    print('successfully inserted ', tgtcurr, 'to table on ', currdate)
                                    latestcurr.append(curr + ':' + str(currdate) + ':' + str(curclose))
                                except pgs.Error as e:
                                    try:
                                        print(e.pgerror)
                                        print('failed to load ', tgtcurr)
                                    finally:
                                        e = None
                                        del e

                                except ValueError:
                                    print(curr, ' is not in list-', tgtlist)

                            else:
                                if currdate is not None and currdate >= pdate:
                                    try:
                                        cq = 'insert into dbo.currency (currency,rate,currency_date)\n                                values (%s,%s,%s) ON CONFLICT (currency, currency_date)\n                                DO UPDATE SET rate = EXCLUDED.rate'
                                        cursor.execute(cq, (tgtcurr, curclose, currdate))
                                        print('successfully inserted ', tgtcurr, 'to table on ', currdate)
                                        latestcurr.append(curr + ':' + str(currdate) + ':' + str(curclose))
                                    except pgs.Error as e:
                                        try:
                                            print(e.pgerror)
                                            print('failed to load ', tgtcurr)
                                        finally:
                                            e = None
                                            del e

                                else:
                                    print('Curr date turned out to be NULL for:', curr)
                        else:
                            print('Non-loadable output came as json\n', quotedata)
                            curr = tgtcurr
                            currdate = None
                            curclose = None
                    else:
                        print('Error code not 200 for the batch')
                        cnt = cnt + 1
                    if cnt == 3:
                        print("No valid load after 5 attempts. Updating with yesterday's data")
                        lcq = 'select rate from dbo.currency\n                    where currency=%s\n                    order by currency_date desc fetch first 1 rows only'
                        try:
                            print('searching last known currency rate for ', tgtcurr)
                            cursor.execute(lcq, (tgtcurr,))
                            fxrate = cursor.fetchone()
                            if fxrate is not None:
                                fxrate = fxrate[0]
                            else:
                                print('cant find last currency value for ', tgtcurr, ' so defaulting to 1')
                                fxrate = 1
                        except pgs.Error as e:
                            try:
                                print('cant find last currency value for ', tgtcurr, ' so defaulting to -99')
                                fxrate = -99
                            finally:
                                e = None
                                del e

                        try:
                            cq = 'insert into dbo.currency (currency,rate,currency_date)\n                        values (%s,%s,%s) ON CONFLICT (currency, currency_date)\n                        DO UPDATE SET rate = EXCLUDED.rate'
                            cursor.execute(cq, (tgtcurr, fxrate, pdate))
                            print('successfully inserted ', tgtcurr, 'to table on ', pdate)
                            stalecurr.append(tgtcurr + ':' + str(pdate) + ':' + str(fxrate))
                        except pgs.Error as e:
                            try:
                                print(e.pgerror)
                                print('failed to load ', tgtcurr)
                            finally:
                                e = None
                                del e

                else:
                    print('all currencies are updated with values >=', pdate)

            print('list of newly updated currencies\n', latestcurr)
            print('currencies whose current rate is overriden with last available rate\n', stalecurr)
            lc = 'select currency, rate from (\n                select currency,rate,currency_date,row_number()\n                over (partition by currency order by currency_date desc) as rc\n                from dbo.currency where currency_date>=%s\n                order by currency_date desc) as lc\n                where lc.rc=1'
            try:
                cursor.execute(lc, (pdate,))
                cres = cursor.fetchall()
            except pgs.Error as e:
                try:
                    print(e.pgerror)
                    print('failure to fetch currencies for ', pdate)
                finally:
                    e = None
                    del e

            if cres is None:
                cres = []
            else:
                if len(cres) > 0:
                    for i in range(len(cres)):
                        tcurr = cres[i][0]
                        trate = cres[i][1]
                        cur_rate.update({tcurr: trate})

                else:
                    print('no currencies present in currency table for ', pdate)
                self.cur_rate = cur_rate

        print('postgresconnection closed')