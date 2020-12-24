# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mysql/mtstat/mysqlqps.py
# Compiled at: 2007-07-20 18:59:51
import mysqlbase

class mysqlqps(mysqlbase.mysqlbase):
    mysqlvars = [
     (
      'Uptime', ('total', ('d', 7, 1000), 'uptime')),
     (
      'Com_select', ('diff', ('d', 7, 1000), 'sel')),
     (
      'Com_insert', ('diff', ('d', 7, 1000), 'ins')),
     (
      'Com_delete', ('diff', ('d', 7, 1000), 'del')),
     (
      'Com_update', ('diff', ('d', 7, 1000), 'upd')),
     (
      'Questions', ('diff', ('d', 7, 1000), 'quest'))]