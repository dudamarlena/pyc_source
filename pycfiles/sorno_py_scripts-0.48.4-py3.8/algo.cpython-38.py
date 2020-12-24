# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sorno/algo.py
# Compiled at: 2020-03-16 00:44:32
# Size of source mod 2**32: 728 bytes


def min_edit_distance_dp(s1, s2):
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    dists = [0] * (1 + len(s2))
    dists2 = [0] * (1 + len(s2))
    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            if i == 0:
                dists[j] = j
            elif j == 0:
                dists[j] = i
            elif s1[(i - 1)] == s2[(j - 1)]:
                dists[j] = dists2[(j - 1)]
            else:
                dists[j] = 1 + min([
                 dists2[j],
                 dists[(j - 1)],
                 dists2[(j - 1)]])
        else:
            dists, dists2 = dists2, dists

    else:
        return dists2[(-1)]