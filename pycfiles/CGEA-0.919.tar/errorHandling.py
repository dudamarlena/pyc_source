# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/max/Desktop/workspace/CGEA/app/CGEA/lib/CGEA_fxn/lib/errorHandling.py
# Compiled at: 2016-01-15 11:13:25
import linecache, sys, traceback

def printException():
    traceback.print_exc(file=sys.stdout)