# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/near_prime.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 781 bytes
from __future__ import print_function

def nearfactor(num, thresh):
    """
    find the product of prime factors of num the nearest from thresh 
    """

    def primefactors(x):
        """
        decomposition in prime factors
        """
        factorlist = []
        loop = 2
        while loop <= x:
            if x % loop == 0:
                x /= loop
                factorlist.append(loop)
            else:
                loop += 1

        return factorlist

    lprime = primefactors(num)
    div = 1
    for i in lprime[::-1]:
        div *= i
        if num / div != 0:
            if div <= thresh:
                continue
        div /= i

    return div