# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/finenight/test.py
# Compiled at: 2014-08-29 00:09:34
import fsc
from copy import copy
from pdb import set_trace

def getRightNonSubsumingPositions(n, (i, e), basePos):
    positions = []
    j = i + 1
    maxDistance = basePos[0] + n + 1
    maxHigh = 0
    while j < maxDistance:
        f = e - maxHigh
        while f <= e + maxHigh:
            if f >= 0 and f <= n and fsc.isSubsumming(basePos, (j, f)) and j >= 0:
                positions.append((j, f))
            f += 1

        j += 1
        maxHigh += 1

    return positions


def powerSet(n, pos, basePos):
    positions = getRightNonSubsumingPositions(n, pos, basePos)
    set = []
    set.append([pos])
    for p in positions:
        s = map(lambda s: [pos] + s, powerSet(n, p, basePos))
        set += s

    return set


def possibleStates(n):
    basePosIndex = 0
    j = 0
    set = [[]]
    for f in range(n + 1):
        set += powerSet(n, (j, f), (basePosIndex, 0))
        basePosIndex += 1

    return set