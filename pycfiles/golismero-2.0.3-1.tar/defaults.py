# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/core/defaults.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
from lib.core.datatype import AttribDict
_defaults = {'csvDel': ',', 
   'timeSec': 5, 
   'googlePage': 1, 
   'cpuThrottle': 5, 
   'verbose': 1, 
   'delay': 0, 
   'timeout': 30, 
   'retries': 3, 
   'saFreq': 0, 
   'threads': 1, 
   'level': 1, 
   'risk': 1, 
   'dumpFormat': 'CSV', 
   'tech': 'BEUSTQ', 
   'torType': 'HTTP'}
defaults = AttribDict(_defaults)