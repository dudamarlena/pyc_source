# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/net6mon/utils.py
# Compiled at: 2006-06-08 09:28:25
import time

def get_timestamp():
    """
        return a timestamp suitable for 
    """
    ts = '%s' % time.time()
    return int(ts.split('.')[0])