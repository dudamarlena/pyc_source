# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/max/Desktop/workspace/CGEA/app/CGEA/lib/CGEA_fxn/lib/errorHandling.py
# Compiled at: 2016-01-15 11:13:25
import linecache, sys, traceback

def printException():
    traceback.print_exc(file=sys.stdout)