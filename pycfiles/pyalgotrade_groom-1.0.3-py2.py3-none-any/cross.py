# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/technical/cross.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'

def compute_diff(values1, values2):
    assert len(values1) == len(values2)
    ret = []
    for i in range(len(values1)):
        v1 = values1[i]
        v2 = values2[i]
        if v1 is not None and v2 is not None:
            diff = v1 - v2
        else:
            diff = None
        ret.append(diff)

    return ret


def _get_stripped(values1, values2, alignLeft):
    if len(values1) > len(values2):
        if alignLeft:
            values1 = values1[0:len(values2)]
        else:
            values1 = values1[len(values1) - len(values2):]
    elif len(values2) > len(values1):
        if alignLeft:
            values2 = values2[0:len(values1)]
        else:
            values2 = values2[len(values2) - len(values1):]
    return (
     values1, values2)


def _cross_impl(values1, values2, start, end, signCheck):
    values1, values2 = _get_stripped(values1[start:end], values2[start:end], start > 0)
    ret = 0
    diffs = compute_diff(values1, values2)
    diffs = filter(lambda x: x != 0, diffs)
    prevDiff = None
    for diff in diffs:
        if prevDiff is not None and not signCheck(prevDiff) and signCheck(diff):
            ret += 1
        prevDiff = diff

    return ret


def cross_above(values1, values2, start=-2, end=None):
    """Checks for a cross above conditions over the specified period between two DataSeries objects.

    It returns the number of times values1 crossed above values2 during the given period.

    :param values1: The DataSeries that crosses.
    :type values1: :class:`pyalgotrade.dataseries.DataSeries`.
    :param values2: The DataSeries being crossed.
    :type values2: :class:`pyalgotrade.dataseries.DataSeries`.
    :param start: The start of the range.
    :type start: int.
    :param end: The end of the range.
    :type end: int.

    .. note::
        The default start and end values check for cross above conditions over the last 2 values.
    """
    return _cross_impl(values1, values2, start, end, lambda x: x > 0)


def cross_below(values1, values2, start=-2, end=None):
    """Checks for a cross below conditions over the specified period between two DataSeries objects.

    It returns the number of times values1 crossed below values2 during the given period.

    :param values1: The DataSeries that crosses.
    :type values1: :class:`pyalgotrade.dataseries.DataSeries`.
    :param values2: The DataSeries being crossed.
    :type values2: :class:`pyalgotrade.dataseries.DataSeries`.
    :param start: The start of the range.
    :type start: int.
    :param end: The end of the range.
    :type end: int.

    .. note::
        The default start and end values check for cross below conditions over the last 2 values.
    """
    return _cross_impl(values1, values2, start, end, lambda x: x < 0)