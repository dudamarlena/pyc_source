# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpclitools/error.py
# Compiled at: 2018-12-30 05:15:40
from pysnmp import error

class SnmpApplicationError(error.PySnmpError):
    __module__ = __name__