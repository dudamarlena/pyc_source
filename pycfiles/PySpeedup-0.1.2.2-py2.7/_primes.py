# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/_primes.py
# Compiled at: 2017-02-25 12:54:13
import random, math
from pyspeedup.algorithms import gcd, factor

def FermatPrimeTest(n, t=2):
    """Tests for primitivity using Fermat's Primitivity Test. Does not guarantee primitivity."""
    return pow(t, n - 1, n) == 1


def FermatConsecutivePrimality(n):
    if not FermatPrimeTest(n, 2):
        return False
    else:
        if n < 341:
            return True
        if not FermatPrimeTest(n, 3):
            return False
        if n < 1105:
            return True
        if not FermatPrimeTest(n, 5):
            return False
        if n < 1729:
            return True
        if not FermatPrimeTest(n, 7):
            return False
        if n < 29341:
            return True
        return


def pollard_p1(N):
    if N <= 2:
        return [N]
    B = 1
    M = math.factorial(B)
    a = random.randint(2, N - 1)
    g = gcd(a, N)
    while g == 1 or g == N:
        B += 1
        M *= B
        g = gcd(pow(a, M, N) - 1, N)

    print B
    return [g, N // g]


def BrutePrimitivityTest(n):
    """Uses simple brute force calculation to determine primitivity."""
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            return False

    return True


def BailliePSWPrimalityTest(n):
    if n > BailliePSWPrimalityTest.knownupperbound:
        raise Exception('Not dealing with probable primes yet.')
    return StrongPrimeTest(n) and LucasProbablePrime(n)


BailliePSWPrimalityTest.knownupperbound = 18446744073709551616

def LucasProbablePrime(n):
    pass


def StrongPrimeTest(n, t=2):
    """Tests for primitivity using a strong primitivity test. Does not guarantee primitivity."""
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    m = n - 1
    k = 0
    while m % 2 == 0:
        m //= 2
        k += 1

    b = pow(t, m, n)
    if b == 1:
        return True
    for i in range(0, k):
        if b == n - 1:
            return True
        b = b * b % n

    return False


def ConsecutiveStrongPrimeTest(n):
    if not StrongPrimeTest(n, 2):
        return False
    else:
        if n < 2047:
            return True
        if not StrongPrimeTest(n, 3):
            return False
        if n < 233017:
            return True
        return


def certificateOfPrimitivity(number, modulo):
    """Generates a set of the distinct prime factors, and their least nonnegative residues of the given number in the given modulo."""
    DIV = set(factor(modulo - 1))
    RES = []
    for i in DIV:
        RES.append(int(number ** ((modulo - 1) / i) % modulo))

    return (
     DIV, RES)


def pollard_rho(N):
    if N <= 2:
        return [N]
    else:

        def f(x):
            return (x * x + 1) % N

        x = 2
        y = 2
        d = 1
        c = 0
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = gcd(abs(x - y), N)
            c += 1

        print c
        if d == N:
            return None
        return [
         d, N // d]


def findCertificateOfPrimitivity(p):
    i = 1
    b = [1]
    while 1 in b:
        i += 1
        a, b = certificateOfPrimitivity(i, p)

    return (
     a, b)