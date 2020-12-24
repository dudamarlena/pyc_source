# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/tuplelex.py
# Compiled at: 2009-09-20 00:42:25
"""Combinatorial functions for manipulating tuples (represented as lists) over
a base set, ordered by lexicographical ordering.

For example, say we want all 3-tuples over the following set:
          [0,1,2]

Then these would consist of the 27 tuples:
   [0,0,0], [0,0,1], [0,0,2], [0,1,0], [0,1,1], [0,1,2],
   [0,2,0], [0,2,1], [0,2,2], [1,0,0], [1,0,1], [1,0,2],
   [1,1,0], [1,1,1], [1,1,2], [1,2,0], [1,2,1], [1,2,2],
   [2,0,0], [2,0,1], [2,0,2], [2,1,0], [2,1,1], [2,1,2],
   [2,2,0], [2,2,1], [2,2,2]

We allow the elements of the tuple to be picked from a specific base set,
B, which consists of either:
A. a 2-tuple consisting of:
     1. a list of the possible values for position i in a tuple.
     2. a reverse lookup dict for the list of possible values.
   Example: [0,3,4,2], {0:0, 3:1, 4:2, 2:3}.
   We require the reverse lookup dict for efficient algorithms; otherwise, we
   would need to invoke many calls to the list index method.
B. an integer j, representing that the value for position i be taken from
   [0,...,j-1]. Note that this is more efficient as we do not need to perform
   lookups from a dictionary in order to execute the operations."""

def rank(B, T):
    """Return the rank of tuple T over the base represented by B.
    See the library description for how base representations work."""
    rank = 0
    posMult = 1
    for i in xrange(len(T)):
        idx = len(T) - i - 1
        rank += posMult * T[idx] if type(B) == int else posMult * B[1][T[idx]]
        posMult *= B if type(B) == int else len(B[0])

    return rank


def unrank(B, k, rk):
    """Return the k-tuple of rank rk over the base represented by B.
    See the library description for how base representations work."""
    T = [
     0] * k
    mult = B if type(B) == int else len(B[0])
    posMult = mult ** k
    for i in xrange(k):
        posMult /= mult
        idx = rk / posMult
        T[i] = idx if type(B) == int else B[0][idx]
        rk %= posMult

    return T


def succ(B, T):
    """Return the successor of the tuple T over the base represented by B.
    Returns None if T is the last tuple in the ordering.
    See the library description for how base representations work."""
    Tnew = T[:]
    for i in xrange(len(Tnew)):
        idx = len(Tnew) - i - 1
        if type(B) == int:
            Tnew[idx] = (Tnew[idx] + 1) % B
            if Tnew[idx] > 0:
                return Tnew
        else:
            (basis, lookup) = B
            Tnew[idx] = basis[((lookup[Tnew[idx]] + 1) % len(basis))]
            if Tnew[idx] != basis[0]:
                return Tnew

    return


def all(B, k):
    """A generator to create all k-tuples over the supplied mixed base B."""
    T = [ 0 if type(B) == int else B[0][0] for i in xrange(k) ]
    while T != None:
        yield T
        T = succ(B, T)

    return