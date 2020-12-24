# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkellestatistics/getlogreturneod.py
# Compiled at: 2020-01-24 12:27:06
# Size of source mod 2**32: 2674 bytes
"""
Created on Wed Jul 17 12:23:51 2019
calculate log returns for any series.
Input parameters are symbol and history table
send totest
@author: debmishra
"""
from lykkelleconf.connecteod import connect
import pandas as pd, psycopg2 as psg, numpy as np

class getlogreturn:

    def __init__(self, symbol, table, cursor):
        selret = 'select price, price_date from ' + table + ' where symbol=%s and price_date > current_date - 31 order by price_date'
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
        sh = pd.DataFrame(rsel, columns=['Price', 'Price_date'])
        vp = sh['Price'].notnull()
        sh = sh[vp]
        vp = sh['Price'] != 0
        sh = sh[vp]
        if len(sh) > 1:
            try:
                print('Getting log return for:', symbol)
                sh['return'] = np.log(sh['Price']) - np.log(sh['Price'].shift(1))
            except AttributeError:
                print(symbol, " couldn't fetch return. See value sample below")
                print(sh.head())

            updret = 'update ' + table + ' set price_return=%s where symbol=%s and price_date=%s'
            fl = len(sh)
            c = 0
            for i in range(fl):
                pdate = sh.iloc[(i, 1)]
                pret = sh.iloc[(i, 2)]
                if np.isnan(pret):
                    pret = None
                else:
                    try:
                        cursor.execute(updret, (pret, symbol, pdate))
                        c = c + 1
                    except (Exception, psg.Error) as e:
                        try:
                            print('Load unsuccessful for ', symbol, '& ', pdate)
                            print(e)
                        finally:
                            e = None
                            del e

            print(c, ' out of ', fl, ' loaded for ticker', symbol, 'to table ', table)
        else:
            print('Less than 2 entries for symbol ', symbol, 'minmum non null entries needed is 2')
        print('postgres connection closed')