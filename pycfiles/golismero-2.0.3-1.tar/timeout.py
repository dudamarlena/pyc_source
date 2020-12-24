# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/utils/timeout.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import threading
from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING

def timeout(func, args=(), kwargs={}, duration=1, default=None):

    class InterruptableThread(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None
            return

        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except Exception as msg:
                logger.log(CUSTOM_LOGGING.TRAFFIC_IN, msg)
                self.result = default

    thread = InterruptableThread()
    thread.start()
    thread.join(duration)
    if thread.isAlive():
        return default
    else:
        return thread.result