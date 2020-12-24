# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyutrack/logger.py
# Compiled at: 2017-10-28 23:27:23
# Size of source mod 2**32: 162 bytes
import logging
instance = None

def get_logger():
    global instance
    if not instance:
        instance = logging.getLogger('pyutrack')
    return instance