# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\disc\crawler\dbsource.py
# Compiled at: 2009-04-27 11:28:48
__doc__ = '\nCreated on 2009-4-20\n\n@author: mingqi\n'
import MySQLdb
g_conn = None

def get_conn():
    global g_conn
    if g_conn:
        return g_conn
    g_conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='tbd', use_unicode=True, charset='utf8', client_flag=2)
    return g_conn