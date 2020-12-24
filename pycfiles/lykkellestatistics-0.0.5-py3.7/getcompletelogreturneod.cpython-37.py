# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkellestatistics/getcompletelogreturneod.py
# Compiled at: 2020-01-24 20:23:33
# Size of source mod 2**32: 3559 bytes
"""
Created on Wed Jul 17 12:23:51 2019
calculate log returns for any series.
Input parameters are symbol and history table
send totest
@author: debmishra
"""
import os
from lykkelleconf.connecteod import connect
import pandas as pd, psycopg2 as psg, numpy as np
home = os.path.expanduser('~')

class getcompletelogreturn:

    def __init__(self, symbol, table, cursor):
        selret = 'select symbol, price, price_date, source_table, volume  from ' + table + ' where symbol=%s order by price_date'
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
        sh = pd.DataFrame(rsel, columns=['symbol', 'Price', 'Price_date', 'source_table', 'volume'])
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

            sh['return'].fillna((-999), inplace=True)
            firstdate = sh['Price_date'].head(1).iloc[0]
            lastdate = sh['Price_date'].tail(1).iloc[0]
            delret = 'delete from ' + table + ' where symbol=%s and price_date between %s and %s'
            copq = table
            fl = len(sh)
            c = 0
            myfile = './tmp/logrt.csv'
            print(sh.head())
            sh.to_csv(myfile, index=None, header=False)
            try:
                cursor.execute(delret, (symbol, firstdate, lastdate))
                print('delete successful and now loading')
                f = open(myfile, 'r')
                cursor.copy_from(f, copq, columns=('symbol', 'price', 'price_date',
                                                   'source_table', 'volume', 'price_return'), sep=',')
                f.close()
                c = fl
                os.remove(myfile)
            except (Exception, psg.Error) as e:
                try:
                    print('Error fetching data from PostgreSQL table for ', symbol, '& ', table)
                    print(e.pgerror)
                finally:
                    e = None
                    del e

            print(c, ' out of ', fl, ' loaded for ticker', symbol, 'to table ', table)
        else:
            print('Less than 2 entries for symbol ', symbol, 'minmum non null entries needed is 2')
        print('postgres connection closed')