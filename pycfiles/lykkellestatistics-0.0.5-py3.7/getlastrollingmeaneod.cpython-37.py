# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkellestatistics/getlastrollingmeaneod.py
# Compiled at: 2020-01-24 12:27:06
# Size of source mod 2**32: 6416 bytes
"""
Created on Sun Sep 22 11:56:35 2019

@author: debmishra
"""
from lykkelleconf.connecteod import connect
import pandas as pd, psycopg2 as psg, numpy as np

class getlastrollingmean:

    def rollingmean50d(symbol, table, cursor):
        selret = 'select price, price_date,ma_50d from ' + table + ' where symbol=%s and price_date > current_date - 31 order by price_date desc'
        delret = 'delete from ' + table + ' where symbol=%s and (price is null or price <= 0)'
        print(table, symbol)
        try:
            cursor.execute(delret, (symbol,))
            cursor.execute(selret, (symbol,))
        except (Exception, psg.Error) as e:
            try:
                print('Error fetching data from PostgreSQL table for ', symbol, '& ', table)
                print(e)
            finally:
                e = None
                del e

        rsel = cursor.fetchall()
        sh = pd.DataFrame(rsel, columns=['Price', 'Price_date', 'ma50d'])
        vp = sh['Price'].notnull()
        sh = sh[vp]
        vp = sh['Price'] != 0
        sh = sh[vp]
        if len(sh) > 1:
            rc = 0
            rl = 0
            for i in range(len(sh)):
                ma50d = sh['ma50d'].iloc[i]
                pdate = sh['Price_date'].iloc[i]
                if not ma50d is None:
                    if np.isnan(ma50d):
                        rl = rl + 1
                        selq = 'select price,price_date from\n                            stock_history where symbol=%s and price_date<=%s\n                            order by price_date desc fetch first 50 rows only'
                        cursor.execute(selq, (symbol, pdate))
                        list50d = cursor.fetchall()
                        if len(list50d) == 50:
                            psum = 0
                            for j in range(len(list50d)):
                                pprc = list50d[j][0]
                                psum = psum + pprc

                            p50 = psum / 50
                        else:
                            p50 = None
                        updp50 = 'update ' + table + ' set MA_50D=%s where symbol=%s and price_date=%s and MA_50D is null'
                        try:
                            cursor.execute(updp50, (p50, symbol, pdate))
                            rc = rc + 1
                        except (Exception, psg.Error) as e:
                            try:
                                print('Load unsuccessful for ', symbol, '& ', pdate)
                                print(e)
                            finally:
                                e = None
                                del e

                    continue

            print(rc, ' out of ', rl, 'valid 50D loaded for ticker', symbol, 'having total ', len(sh), 'entries to table ', table)
        else:
            print('Less than 2 entries for symbol ', symbol, 'minmum non null entries needed is 2')
        print('postgres connection closed')

    def rollingmean200d(symbol, table, cursor):
        selret = 'select price, price_date,ma_200d from ' + table + ' where symbol=%s and price_date > current_date - 31 order by price_date desc'
        delret = 'delete from ' + table + ' where symbol=%s and (price is null or price <= 0)'
        print(table, symbol)
        try:
            cursor.execute(delret, (symbol,))
            cursor.execute(selret, (symbol,))
        except (Exception, psg.Error) as e:
            try:
                print('Error fetching data from PostgreSQL table for ', symbol, '& ', table)
                print(e)
            finally:
                e = None
                del e

        rsel = cursor.fetchall()
        sh = pd.DataFrame(rsel, columns=['Price', 'Price_date', 'ma200d'])
        vp = sh['Price'].notnull()
        sh = sh[vp]
        vp = sh['Price'] != 0
        sh = sh[vp]
        if len(sh) > 1:
            rc = 0
            rl = 0
            for i in range(len(sh)):
                ma200d = sh['ma200d'].iloc[i]
                pdate = sh['Price_date'].iloc[i]
                if not ma200d is None:
                    if np.isnan(ma200d):
                        rl = rl + 1
                        selq = 'select price,price_date from\n                            stock_history where symbol=%s and price_date<=%s\n                            order by price_date desc fetch first 200 rows only'
                        cursor.execute(selq, (symbol, pdate))
                        list200d = cursor.fetchall()
                        if len(list200d) == 200:
                            psum = 0
                            for j in range(len(list200d)):
                                pprc = list200d[j][0]
                                psum = psum + pprc

                            p200 = psum / 200
                        else:
                            p200 = None
                        updp200 = 'update ' + table + ' set MA_200D=%s where symbol=%s and price_date=%s and MA_200D is null'
                        try:
                            cursor.execute(updp200, (p200, symbol, pdate))
                            rc = rc + 1
                        except (Exception, psg.Error) as e:
                            try:
                                print('Load unsuccessful for ', symbol, '& ', pdate)
                                print(e)
                            finally:
                                e = None
                                del e

                    continue

            print(rc, ' out of ', rl, 'valid 200D loaded for ticker', symbol, 'having total ', len(sh), 'entries to table ', table)
        else:
            print('Less than 2 entries for symbol ', symbol, 'minmum non null entries needed is 2')
        print('postgres connection closed')