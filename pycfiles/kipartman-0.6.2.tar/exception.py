# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: helper/exception.py
# Compiled at: 2018-04-27 05:54:44
from configuration import configuration
import sys, traceback

def print_stack():
    print '---', configuration.debug
    if configuration.debug:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, file=sys.stdout)