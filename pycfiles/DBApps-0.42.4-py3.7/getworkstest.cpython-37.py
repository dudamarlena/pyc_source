# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/getworkstest.py
# Compiled at: 2019-04-22 11:39:38
# Size of source mod 2**32: 1170 bytes
"""
Created on Mar 13, 2018
This is a basic skeleton which shows how to locate a dbConfig file,
and start a connection to its db.

@author: jsk
"""
from pathlib import Path
import sys
from config import config
import pymysql

def getworkstest():
    """
    Read the remote database from a dbConfig and  connect to it
    """
    cfgPath = Path(__file__).parent.parent / 'conf' / 'drsBatch.dbConfig'
    if cfgPath.is_file():
        print('yes')
    cfg = config.DBConfig('prod', str(cfgPath))
    myConnection = pymysql.connect(read_default_file=(cfg.db_cnf), read_default_group=(cfg.db_host),
      db='drs',
      charset='utf8')
    with myConnection.cursor() as (cursor):
        backSet = cursor.execute('select * from Outlines limit 10;')
        results = cursor.fetchall()
        for res in results:
            print(res)


if __name__ == '__main__':
    getworkstest()