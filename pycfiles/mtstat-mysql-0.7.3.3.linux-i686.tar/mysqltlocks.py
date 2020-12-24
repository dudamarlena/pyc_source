# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mysql/mtstat/mysqltlocks.py
# Compiled at: 2007-08-01 14:20:09
import mysqlqps

class mysqltlocks(mysqlqps.mysqlqps):
    mysqlvars = [
     (
      'Table_locks_immediate', ('diff', ('d', 7, 1000), 'timmed')),
     (
      'Table_locks_waited', ('diff', ('d', 7, 1000), 'twait'))]