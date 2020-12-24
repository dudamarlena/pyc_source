# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mysql/mtstat/mysqlqcache.py
# Compiled at: 2007-08-07 16:37:45
import mysqlbase

class mysqlqcache(mysqlbase.mysqlbase):
    mysqlvars = [
     (
      'Qcache_hits', ('diff', ('d', 7, 1000), 'qhit')),
     (
      'Qcache_inserts', ('diff', ('d', 7, 1000), 'qins')),
     (
      'Qcache_lowmem_prunes', ('diff', ('d', 7, 1000), 'qlow')),
     (
      'Qcache_not_cached', ('diff', ('d', 7, 1000), 'qnot'))]