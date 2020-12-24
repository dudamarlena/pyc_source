# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Support/whoosh/support/levenshtein.py
# Compiled at: 2015-06-30 06:52:38
__doc__ = '\nContains functions implementing the Levenshtein distance algorithm.\n'

def relative(a, b):
    """Returns the relative distance between two strings, in the range
    [0-1] where 1 means total equality.
    """
    d = distance(a, b)
    longer = float(max((len(a), len(b))))
    shorter = float(min((len(a), len(b))))
    r = (longer - d) / longer * (shorter / longer)
    return r


def distance(s, t):
    """Returns the Levenshtein edit distance between two strings."""
    m, n = len(s), len(t)
    d = [range(n + 1)]
    d += [ [i] for i in range(1, m + 1) ]
    for i in range(0, m):
        for j in range(0, n):
            cost = 1
            if s[i] == t[j]:
                cost = 0
            d[(i + 1)].append(min(d[i][(j + 1)] + 1, d[(i + 1)][j] + 1, d[i][j] + cost))

    return d[m][n]