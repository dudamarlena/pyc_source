# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomislav/dev/seveno_pyutil/build/lib/seveno_pyutil/benchmarking_utilities.py
# Compiled at: 2018-03-29 11:58:07
# Size of source mod 2**32: 638 bytes
import timeit

class Stopwatch(object):
    __doc__ = '\n    Simple stopwatch that measures duration of block of code in [ms]\n\n    Example:\n        >>> import time\n        >>>\n        >>> with Stopwatch() as stopwatch:\n        ...    time.sleep(1)\n        >>> assert stopwatch.duration_ms >= 1000\n    '

    def __init__(self):
        self.start = 0
        self.end = 0

    def __enter__(self):
        self.start = timeit.default_timer()
        return self

    def __exit__(self, *args):
        self.end = timeit.default_timer()
        return False

    @property
    def duration_ms(self):
        return (self.end - self.start) * 1000