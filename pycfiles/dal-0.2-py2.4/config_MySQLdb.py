# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dal/dbapi/config_MySQLdb.py
# Compiled at: 2007-06-15 17:41:24
import MySQLdb, datetime, math
quote_chars = [
 '`']
escape_chars = ['\\']

def init1(wrapper):
    wrapper._driver.DATETIME = wrapper._driver.DBAPISet(10, 12)