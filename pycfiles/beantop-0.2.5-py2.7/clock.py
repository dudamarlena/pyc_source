# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/beantop/clock.py
# Compiled at: 2013-05-21 04:48:44


class Clock:

    def __init__(self, time_library):
        self._time_library = time_library

    def gmtime(self):
        return self._time_library.time()

    def sleep(self, secs):
        return self._time_library.sleep(secs)

    def get_printable_time(self):
        return self._time_library.strftime('%a, %d %b %Y %X', self._time_library.gmtime())