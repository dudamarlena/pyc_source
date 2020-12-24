# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/matricks/distance.py
# Compiled at: 2011-12-07 16:45:54
"""Distance Functions
------------------

"""
from math import sqrt, pow
NaN = float('nan')

def pearson(a, b, uncentered=False, absolute=False):
    """Returns the *Pearson Product Moment Correlation* between
two, equal-length sequences of numbers.

If the sequences lengths are not equal or of zero length, ``None`` 
is returned.

Note this can be used for the absolute, uncentered, and uncentered absolute
versions of this calculation.  (See Matricks.distance for more info.)

                                        absolute         uncentered
                                        ----------------------------------
    pearson correlation:                False,           False  (Default)
    absolute pearson correlation:       True             False
    uncentered pearson correlation:     False            True
    absolute uncentered pearson corr:   True             True
"""
    av = [ float(x) for x in a if x is not None ]
    bv = [ float(x) for x in b if x is not None ]
    N = len(av)
    if N < 2 or N != len(bv):
        return NaN
    else:
        N = float(N)
        a_bar = 0.0 if uncentered else sum(av) / N
        b_bar = 0.0 if uncentered else sum(bv) / N
        a_diff = map(lambda x: x - a_bar, av)
        b_diff = map(lambda x: x - b_bar, bv)
        a_sdev = sqrt(sum(map(lambda x: x * x, a_diff)) / (N - 1))
        b_sdev = sqrt(sum(map(lambda x: x * x, b_diff)) / (N - 1))
        numerator = a_sdev * b_sdev * (N - 1)
        ppm = sum(map(lambda x, y: x * y, a_diff, b_diff)) / numerator if numerator != 0.0 else 0.0
        return 1 - (abs(ppm) if absolute else ppm)


def spearman(a, b):
    """Spearman's Rank correlation distance.
"""
    av = [ x[0] + 1 for x in sorted(enumerate(a), key=lambda x: x[1])
         ]
    bv = [ x[0] + 1 for x in sorted(enumerate(b), key=lambda x: x[1]) ]
    return pearson(av, bv)


def euclideanDistance(a, b):
    """Euclidean distance between two vectors, *a* amd *b* .
"""
    vec = [ pow(a[i] - b[i], 2) for i in range(len(a)) if None not in [a[i], b[i]] ]
    if len(vec) > 0:
        return sum(vec) / len(vec)
    else:
        return NaN


def blockDistance(a, b):
    """City-block (aka Manhattan)  distance between two vectors, *a* amd *b* .
"""
    vec = [ abs(x[0] - x[1]) for x in zip(a, b) if None not in x ]
    if len(vec) > 0:
        return sum(vec) / len(vec)
    else:
        return NaN


def kendallsTau(a, b):
    """
Based on http://en.wikipedia.org/wiki/Kendall_tau_distance

Count up the number of discordant pairs and divide these by the
number of possible pairings. (n * (n - 1)) / 2)

disconrdant <- (x[i] < x[j] and y[i] > y[j]) or (x[i] > x[j] and y[i] < y[j])

"""
    numerator = 0
    sgn = --- This code section failed: ---

 L. 106         0  LOAD_FAST             0  'x'
                3  LOAD_CONST               0
                6  COMPARE_OP            0  <
                9  JUMP_IF_FALSE         5  'to 17'
             12_0  THEN                     17
               12  POP_TOP          
               13  LOAD_CONST               -1
               16  RETURN_END_IF_LAMBDA
               17  POP_TOP          
               18  LOAD_FAST             0  'x'
               21  LOAD_CONST               0
               24  COMPARE_OP            4  >
               27  JUMP_IF_FALSE         5  'to 35'
             30_0  THEN                     35
               30  POP_TOP          
               31  LOAD_CONST               1
               34  RETURN_END_IF_LAMBDA
               35  POP_TOP          
               36  LOAD_CONST               0
               39  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
    N = len(a)
    if N < 2 or N != len(b):
        return NaN
    else:
        for i in range(len(a) - 1):
            j = i + 1
            if None not in [a[i], a[j], b[i], b[j]]:
                if a[i] < a[j] and b[i] > b[j] or a[i] > a[j] and b[i] < b[j]:
                    numerator = numerator + 1

        return float(numerator) / (N * (N - 1) / 2.0)