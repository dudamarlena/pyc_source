# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\disc\crawler\dbsource.py
# Compiled at: 2009-04-27 11:28:48
"""
Created on 2009-4-20

@author: mingqi
"""
import MySQLdb
g_conn = None

def get_conn():
    global g_conn
    if g_conn:
        return g_conn
    g_conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='tbd', use_unicode=True, charset='utf8', client_flag=2)
    return g_conn