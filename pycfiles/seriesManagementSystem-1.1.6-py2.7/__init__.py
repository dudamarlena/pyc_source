# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/SMS/__init__.py
# Compiled at: 2015-07-29 10:35:26
import sys
from serieManagementSystem import SMS

def main():
    """Entry point for the application script"""
    sms = SMS()
    sms.getArguments(sys.argv[1:])