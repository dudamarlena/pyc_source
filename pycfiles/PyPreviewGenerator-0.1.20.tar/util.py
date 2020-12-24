# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pypreval/util.py
# Compiled at: 2008-02-20 17:58:55
__doc__ = '\nthe popular utility collector module. Enjoy.\n'
import os, errno

def optional_makedirs(path):
    """create all needed directories, ignore EEXIST errors."""
    try:
        os.makedirs(path)
    except os.error, exception:
        if exception.errno != errno.EEXIST:
            raise