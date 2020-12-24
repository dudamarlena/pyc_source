# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddalg/metrics/interval.py
# Compiled at: 2020-03-30 11:18:59
# Size of source mod 2**32: 1384 bytes
from ddalg.model import Interval

def get_boundary_margin(begin, end, coverage=1.0):
    """
    Returns a value to be added/subtracted to the interval begin and end positions such that another interval
     whose begin and end positions fall within these boundaries will have the required minimum coverage provided in the
     method.
     For example the interval 10-20 with a 0.85 overlap would have a margin value of 1 to be added/subtracted to
     the begin and end - i.e. anywhere between 10+/-1 and 20+/-1 will satisfy the 85% overlap requirement.
    :param begin: 0-based (excluded) begin position of query
    :param end: 0-based (included) end position of query
    :param coverage: float in [0,1] specifying what fraction of query the interval needs to overlap with
    :return: float with margin
    """
    if 1 < coverage > 0:
        raise ValueError('coverage must be in range [0,1]')
    return (end - begin) * (1 - coverage) / 2


def jaccard_coefficient(first: Interval, second: Interval) -> float:
    intersection = first.intersection(second)
    return intersection / (len(first) + len(second) - intersection)


def reciprocal_overlap(first: Interval, second: Interval) -> float:
    intersection = first.intersection(second)
    return min(intersection / len(first), intersection / len(second))