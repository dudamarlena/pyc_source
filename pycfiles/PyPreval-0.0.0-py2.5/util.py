# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pypreval/util.py
# Compiled at: 2008-02-20 17:58:55
"""
the popular utility collector module. Enjoy.
"""
import os, errno

def optional_makedirs(path):
    """create all needed directories, ignore EEXIST errors."""
    try:
        os.makedirs(path)
    except os.error, exception:
        if exception.errno != errno.EEXIST:
            raise