# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/common/helper.py
# Compiled at: 2015-05-28 03:51:49


def linear_interpolation(first, last, steps):
    """Interpolates all missing values using linear interpolation.

    :param numeric first:    Start value for the interpolation.
    :param numeric last:    End Value for the interpolation
    :param integer steps:    Number of missing values that have to be calculated.

    :return:    Returns a list of floats containing only the missing values.
    :rtype: list

    :todo:     Define a more general interface!
    """
    result = []
    for step in xrange(0, steps):
        fpart = (steps - step) * first
        lpart = (step + 1) * last
        value = (fpart + lpart) / float(steps + 1)
        result.append(value)

    return result