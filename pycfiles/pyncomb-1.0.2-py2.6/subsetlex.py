# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/subsetlex.py
# Compiled at: 2010-10-16 14:06:50
"""An implementation of basic combinatorial subset opertions using
lexicographic ordering.

Note that for our purposes here, sets are represented as lists as
ranking, unranking, and successor functions need a total order on the
elements of the set.

For the base set B, if B is an integer, we assume that our base set is
[0,...,B-1]. Otherwise, assume that B is a pair consisting of:
   1. a list representing the base set
   2. a reverse lookup dict, mapping elements of the base set to their
      position in the total order.
   Example: [0,3,4,2], {0:0, 3:1, 4:2, 2:3}
Note that we require B to contain the reverse lookup information to
speed up the algorithms here; otherwise, we would need to call index on
our base set many times, which would increase complexity by a factor of
the length of the base set.

By Sebastian Raaphorst, 2009."""
from . import combfuncs

def rank(B, S):
    """Return the rank of the subset S in base set B."""
    return reduce(lambda a, b: a | b, [ 1 << (i if type(B) == int else B[1][i]) for i in S ], 0)


def unrank(B, rk):
    """Return the subset of rank rk in base set B."""
    return [ i if type(B) == int else B[0][i] for i in xrange(B if type(B) == int else len(B[0])) if 1 << i & rk ]


def succ(B, S):
    """Return the successor of the subset S in base set B."""
    Sn = unrank(B, rank(B, S) + 1)
    if Sn == []:
        return None
    else:
        return Sn


def all(B):
    """A generator to create all subsets over the specified base set."""
    Bn = B if type(B) == int else (B[0][:], dict(B[1]))
    K = []
    while K != None:
        yield K
        K = succ(Bn, K)

    return