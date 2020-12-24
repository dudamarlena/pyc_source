# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/multicore/utils.py
# Compiled at: 2017-08-07 06:37:07
import math
from multicore import NUMBER_OF_WORKERS

def ranges(iterable, min_range_size=0, number_of_workers=None):
    """Return a set of ranges (start, end) points so an iterable can be passed
    in optimal chunks to a task."""
    count = len(iterable)
    delta = max(int(math.ceil(count * 1.0 / (number_of_workers or NUMBER_OF_WORKERS))), min_range_size)
    start = 0
    while start < count:
        end = min(start + delta, count)
        yield (start, end)
        start = end