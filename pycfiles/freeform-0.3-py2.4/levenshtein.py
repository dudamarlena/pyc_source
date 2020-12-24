# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/freeform/levenshtein.py
# Compiled at: 2006-03-28 21:17:57
from itertools import repeat
from heapq import *
__all__ = [
 'LEVENSHTEIN_DEFAULT_MAXDIST', 'levenshtein_distance', 'levenshtein_selectone', '_levenshtein_select']
LEVENSHTEIN_DEFAULT_MAXDIST = 3
_levenshtein_maxwordrange = 0
_levenshtein_firstcol = []
_levenshtein_firstrow = []

def _levenshtein_accomodate_wordlen(wordlenplusone):
    global _levenshtein_firstcol
    global _levenshtein_firstrow
    global _levenshtein_maxwordrange
    if wordlenplusone <= _levenshtein_maxwordrange:
        return (
         _levenshtein_firstcol, _levenshtein_firstrow)
    _levenshtein_firstcol.extend([ ((i, 0), i) for i in xrange(_levenshtein_maxwordrange, wordlenplusone) ])
    _levenshtein_firstrow.extend([ ((0, j), j) for j in xrange(_levenshtein_maxwordrange, wordlenplusone) ])
    _levenshtein_maxwordrange = wordlenplusone
    return (_levenshtein_firstcol, _levenshtein_firstrow)


def _levenshtein_prepare_dtab(a, b, dtab=None):
    dtab = dtab or {}
    dtab.clear()
    n, m = len(a), len(b)
    (firstcol, firstrow) = _levenshtein_accomodate_wordlen(max(n, m) + 1)
    dtab.update(firstcol[:n + 1])
    dtab.update(firstrow[:m + 1])
    return (dtab, n, m)


def levenshtein_distance(a, b):
    """Levenshtein word distance algorithm.

    a is the target word, b is the candidate. return the minimum edit distance
    from b to a. that is, the minimum number of insertions, deletions and 
    substitutions required to produce a from b.
    
    Picked this implementation of the net. However it is described well in:
        Speech & Langauge Processing: ISBN-X013122798X, Ch 5. pp 154
    
    Abridged from the above reference:
    
    This algorithm measures the 'minimum edit distance' between two 
    strings a,b. med(a,b) is defined as the minimum number of editing 
    operations required to transform one string into another. 
    
    The operations are delete,substitute,insert

    Levenshtein solves this problem using 'dynamic programming', essentialy a
    table driven mechanism for solving a problem a bit at a time and
    accumulating the result. Dynamic programming solutions for sequences in
    general work by creating a distance matrix with one column for each item in
    the target sequence and one row for each item in the source - ie., target
    allong the bottom & source down the side. For computing the minimum edit
    distance, this matrix is then the edit-distance matrix. Each cell
    edit-distance[i,j] contains the distance between the first i characters of
    the target and the first j characters of the source. The value of each 
    cell represents the minimum of the three possible paths through the matrix
    that arrive there.
    """
    (c, n, m) = _levenshtein_prepare_dtab(a, b)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            x = c[(i - 1, j)] + 1
            y = c[(i, j - 1)] + 1
            if a[(i - 1)] == b[(j - 1)]:
                z = c[(i - 1, j - 1)]
            else:
                z = c[(i - 1, j - 1)] + 1
            c[(i, j)] = min(x, y, z)

    return c[(n, m)]


def levenshtein_selectone(asequence, b, dtab=None, maxwordlen=0, maxdist=LEVENSHTEIN_DEFAULT_MAXDIST):
    maxdist = min(len(b), maxdist)
    if len(asequence) == 1:
        d = levenshtein_distance(asequence[0], b)
        return d < maxdist and (0, d) or (-1, d)
    state = _levenshtein_select(asequence, b, dtab, maxwordlen, maxdist)
    h = state[1]
    return h[0][0] < maxdist and (h[0][(-1)], h[0][0]) or (-1, maxdist)


def _levenshtein_select(asequence, b, dtab=None, maxwordlen=0, maxdist=LEVENSHTEIN_DEFAULT_MAXDIST, state=None):
    (b, h, dtabs, maxwordlen, maxdist) = state or (b, None, None, maxwordlen, maxdist)
    if maxwordlen == 0:
        asequence.append(b)
        maxwordlen = maxwordlen or reduce(max, map(len, asequence))
        asequence.pop()
        _levenshtein_accomodate_wordlen(maxwordlen + 1)
    dtabs = dtabs or [ [0, 0, c, n] for (c, n, m) in map(_levenshtein_prepare_dtab, asequence, repeat(b, len(asequence)), repeat(dtab, len(asequence)))
                     ]
    m = len(b)
    h = h or [ (0, 0, i) for i in range(len(asequence)) ]
    htop = heappop(h)
    irange = range(1, maxwordlen + 1)
    jrange = range(1, m + 1)
    while htop[0] <= h[0][0] and htop[1] < m:
        ic = htop[(-1)]
        dstart, (istart, jstart, c, n) = htop[0], dtabs[ic]
        for i in irange[istart:n]:
            for j in jrange[jstart:]:
                x, y = c[(i - 1, j)] + 1, c[(i, j - 1)] + 1
                if asequence[ic][(i - 1)] == b[(j - 1)]:
                    z = c[(i - 1, j - 1)]
                else:
                    z = c[(i - 1, j - 1)] + 1
                d = c[(i, j)] = min(x, y, z)
                if i == n and j == m and d == 0:
                    heappush(h, htop)
                    return (b, h, dtabs, maxwordlen, maxdist)
                if i == j and d > dstart:
                    dtabs[ic][0:2] = j < m and [i - 1, j] or [i, 0]
                    htop = heapreplace(h, (d, j, htop[(-1)]))
                    break

            jstart = 0
            if i == j and d > dstart:
                break

        if ic == htop[(-1)]:
            htop = heapreplace(h, (d, m, htop[(-1)]))
        if htop[0] > maxdist:
            return (
             b, h, dtabs, maxwordlen, maxdist)

    heappush(h, htop)
    return (b, h, dtabs, maxwordlen, maxdist)