# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/joe/devel/covviz/covviz/utils.py
# Compiled at: 2020-01-24 15:00:16
# Size of source mod 2**32: 1401 bytes
import gzip
COLORS = [
 '#1f77b4',
 '#ff7f0e',
 '#2ca02c',
 '#d62728',
 '#9467bd',
 '#8c564b',
 '#e377c2',
 '#7f7f7f',
 '#bcbd22',
 '#17becf',
 '#7CB5EC',
 '#434348',
 '#90ED7D',
 '#F7A35C',
 '#8085E9',
 '#F15C80',
 '#E4D354',
 '#2B908F',
 '#F45B5B',
 '#91E8E1',
 '#4E79A7',
 '#F28E2C',
 '#E15759',
 '#76B7B2',
 '#59A14F',
 '#EDC949',
 '#AF7AA1',
 '#FF9DA7',
 '#9C755F',
 '#BAB0AB']

def gzopen(f):
    if f.endswith('.gz'):
        return gzip.open(f, 'rt')
    return open(f)


def merge_intervals(intervals):
    sorted_intervals = sorted(intervals, key=(lambda i: i[0]))
    merged = list()
    for higher in sorted_intervals:
        if not merged:
            merged.append(higher)
        else:
            lower = merged[(-1)]
            if higher[0] - lower[1] == 1:
                merged[-1] = [lower[0], higher[1], lower[2] + higher[2]]
            elif higher[0] <= lower[1]:
                upper_bound = max(lower[1], higher[1])
                merged[-1] = [
                 lower[0], upper_bound, lower[2] + higher[2]]
            else:
                merged.append(higher)

    return merged