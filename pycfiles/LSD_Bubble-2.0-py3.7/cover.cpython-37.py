# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/LSD/cycles/cover.py
# Compiled at: 2019-01-19 15:32:53
# Size of source mod 2**32: 1194 bytes
from LSD.cycles import cycle_distance, generate_cycle_range

def find_cover_cut(cmax):
    k = len(cmax)
    m = max(((cycle_distance(k, i, cmax[i]), i) for i in range(k)))[1]
    md = cycle_distance(k, m, cmax[m])
    laststart = m
    lastend = m
    while md <= cycle_distance(k, m, cmax[laststart]):
        next_path = None
        max_dist = 0
        for i in generate_cycle_range(k, lastend, cmax[laststart]):
            if cycle_distance(k, i, cmax[i]) <= cycle_distance(k, i, cmax[laststart]):
                continue
            if cycle_distance(k, cmax[laststart], cmax[i]) > max_dist:
                max_dist = cycle_distance(k, cmax[laststart], cmax[i])
                next_path = i

        if next_path is None:
            return (True, cmax[laststart])
        lastend = cmax[laststart]
        laststart = next_path

    return (False, cmax[laststart])