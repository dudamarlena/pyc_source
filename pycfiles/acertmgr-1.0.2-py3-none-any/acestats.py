# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\acerim\acestats.py
# Compiled at: 2017-09-24 23:16:11
__doc__ = '\nThis file contains statistical functions that can be used to quickly\ngenerate statistics on ROIs (e.g. by using the ejecta_stats or\nejecta_profile_stats functions in acefunctions.py).\n\nAdditional desired statistical functions can be added to this file by\nfollowing the naming convention used here:\n\n    def statname(roi_array):\n        \'\'\'What this stat function does\'\'\'\n        return statistics(roi_array)\n\nEach function should take a single numpy array as an arugument and return a\nsingle value.\n\nThe private functions are:\n\n    _listStats(): return names of all non-protected functions in this file\n\n    _getFunctions(stats): return array of pairs of function names and functions\n                            as specified by stats\n\nNon-statistical functions in this file must be private (begin with "_").\n'
from __future__ import division, print_function, absolute_import
import inspect, numpy as np

def maximum(roi):
    """Return maximum pixel value in roi"""
    return np.max(roi)


def mean(roi):
    """Return the mean of roi"""
    return np.mean(roi)


def median(roi):
    """Return the median (50/50) of roi"""
    return np.median(roi)


def minimum(roi):
    """Return minimum pixel value in roi"""
    return np.min(roi)


def pct95(roi):
    """Return the 95th percentile (95/5) value of roi"""
    return np.percentile(roi, 95)


def q1(roi):
    """Return the first quartile value (25/75) of roi"""
    return np.percentile(roi, 25)


def q3(roi):
    """Return the third quartile (75/25) value of roi"""
    return np.percentile(roi, 75)


def _listStats():
    """
    Return list of the names of all non-private functions from acestats.
    Private functions are excluded by their leading '_'.
    """
    from acerim import acestats
    all_func = np.array(inspect.getmembers(acestats, inspect.isfunction))
    stat_func = all_func[np.where([ a[0][0] != '_' for a in all_func ])]
    return stat_func[:, 0]


def _getFunctions(stats):
    """
    Return functions from this module according to stats. If stats is
    undefined, return all functions from this module, excluding private
    functions.

    Returns
    -------
    List of lists containing 2 element pairs of function names and functions.
        E.g. array( ['func name 1', <func1>], ['func name 2', <func2>])
    """
    from acerim import acestats
    if isinstance(stats, str):
        stats = [
         stats]
    invalid_stats = [ stat for stat in stats if stat not in _listStats() ]
    if invalid_stats:
        raise ValueError(('The following stats are not defined in acestats.py:                           {}').format(invalid_stats))
    all_func = inspect.getmembers(acestats, inspect.isfunction)
    stat_func = []
    for i, func in enumerate(all_func):
        if func[0] in stats:
            stat_func.append(all_func[i])

    return stat_func