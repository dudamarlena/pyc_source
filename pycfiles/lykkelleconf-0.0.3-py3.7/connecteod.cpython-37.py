# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkelleconf/connecteod.py
# Compiled at: 2020-01-24 07:29:17
# Size of source mod 2**32: 1961 bytes
import psycopg2 as pgs, sys
from requests import get
ip = get('https://api.ipify.org').text

class connect:

    def create():
        host_prod = 'lykkelle-prod-us-east.postgres.database.azure.com'
        if ip == '213.127.49.192':
            mydb = 'lykkelledev_db'
            print('this is connected to Dev Database')
        else:
            if ip == '40.121.44.65':
                mydb = 'lykkelle_db'
                print('this is connected to Prod Database')
            else:
                if '40.121.104.114' in ip:
                    mydb = 'lykkelletest_db'
                    print('This is connected to release database')
                else:
                    print('Linking to Dev database as you are not connecting from authorized IPs. Your ip:', ip)
                    mydb = 'lykkelledev_db'
        usr = 'lykkelle@lykkelle-prod-us-east'
        try:
            conn = pgs.connect(database=mydb, user=usr,
              host=host_prod,
              port='5432',
              password='Debajyoti86')
        except pgs.Error as e:
            try:
                print('Unable to connect!')
                print(e.pgerror)
                sys.exit(1)
            finally:
                e = None
                del e

        conn.autocommit = True
        cursor = conn.cursor()
        set_path = 'SET search_path = dbo'
        cursor.execute(set_path)
        return conn