# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/_Shanks.py
# Compiled at: 2017-02-25 12:54:13
import math, operator
from pyspeedup.algorithms import invMod

def Shanks(n, alpha, beta):
    """Uses the Shanks algorithm to solve the discrete log problem for log_alpha(beta) in mod n."""
    m = int(math.ceil(math.sqrt(n)))
    alphaM = pow(alpha, m, n)
    invAlpha = invMod(alpha, n)
    L1 = [(0, 1)]
    L2 = [(0, beta)]
    for j in range(1, m - 1):
        L1.append((j, L1[(j - 1)][1] * alphaM % n))
        L2.append((j, L2[(j - 1)][1] * invAlpha % n))

    L1.sort(key=operator.itemgetter(1))
    L2.sort(key=operator.itemgetter(1))
    try:
        j = 0
        i = 0
        while L1[j][1] != L2[i][1]:
            if L1[j][1] > L2[i][1]:
                i += 1
            else:
                j += 1

        return (m * L1[j][0] + L2[i][0]) % n
    except:
        raise Exception('No solution.')