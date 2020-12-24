# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mysql/mtstat/mysqlhandler.py
# Compiled at: 2007-08-01 14:19:23
import mysqlbase

class mysqlhandler(mysqlbase.mysqlbase):
    mysqlvars = [
     (
      'Handler_read_first', ('diff', ('d', 7, 1000), 'hf')),
     (
      'Handler_read_next', ('diff', ('d', 7, 1000), 'hnxt')),
     (
      'Handler_read_key', ('diff', ('d', 7, 1000), 'hkey')),
     (
      'Handler_read_rnd', ('diff', ('d', 7, 1000), 'rrnd')),
     (
      'Handler_read_rnd_next', ('diff', ('d', 7, 1000), 'rnxt'))]