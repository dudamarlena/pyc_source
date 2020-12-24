# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/_factor.py
# Compiled at: 2017-02-25 12:54:13
from pyspeedup import concurrent
import math
from pyspeedup.algorithms import isSquare

@concurrent.Cache
def factor(N):
    """Utilizes Fermat's sieve and recursive caching to reduce factorization time, mostly in repeated factorization."""
    if N < 0:
        t = factor(-N)
        t.insert(0, -1)
        return t
    else:
        if N < 4:
            return [N]
        if N % 2 == 0:
            t = factor(N // 2)
            t.insert(0, 2)
            return t
        a = int(math.ceil(math.sqrt(N)))
        b2 = a * a - N
        while not isSquare(b2):
            b2 += a + a + 1
            a += 1

        b = int(math.floor(math.sqrt(b2)))
        assert b * b == b2
        if a - b == 1:
            return [a + b]
        factor.apply_async(a - b)
        factor.apply_async(a + b)
        t = factor(a - b)
        for i in factor(a + b):
            t.append(i)

        return list(sorted(t))