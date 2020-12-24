# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/gmssl/sm2_integer.py
# Compiled at: 2020-03-10 11:26:45
# Size of source mod 2**32: 1777 bytes
import math, random

def fast_pow(g, a, p):
    e = int(a % (p - 1))
    if e == 0:
        return 1
    else:
        r = int(math.log2(e))
        x = g
        for i in range(0, r):
            x = int(x ** 2 % p)
            if e & 1 << r - 1 - i == 1 << r - 1 - i:
                x = g * x % p

        return int(x)


def isPrime_MR(u, T):
    v = 0
    w = u - 1
    while w % 2 == 0:
        v += 1
        w = w // 2

    for j in range(1, T + 1):
        nextj = False
        a = random.randint(2, u - 1)
        b = fast_pow(a, w, u)
        if b == 1 or b == u - 1:
            nextj = True
        else:
            for i in range(1, v):
                b = b ** 2 % u
                if b == u - 1:
                    nextj = True
                    break
                if b == 1:
                    return False

            if not nextj:
                return False

    return True


def is_Power_of_two(n):
    if n > 0:
        if n & n - 1 == 0:
            return True
    return False


def inverse(a, n):
    a_ = fast_pow(a, n - 2, n) % n
    return a_