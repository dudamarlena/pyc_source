# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/rsa/rsa/prime.py
# Compiled at: 2018-07-11 18:15:32
"""Numerical functions related to primes.

Implementation based on the book Algorithm Design by Michael T. Goodrich and
Roberto Tamassia, 2002.
"""
import rsa.randnum
__all__ = [
 'getprime', 'are_relatively_prime']

def gcd(p, q):
    """Returns the greatest common divisor of p and q

    >>> gcd(48, 180)
    12
    """
    while q != 0:
        p, q = q, p % q

    return p


def miller_rabin_primality_testing(n, k):
    """Calculates whether n is composite (which is always correct) or prime
    (which theoretically is incorrect with error probability 4**-k), by
    applying Miller-Rabin primality testing.

    For reference and implementation example, see:
    https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test

    :param n: Integer to be tested for primality.
    :type n: int
    :param k: Number of rounds (witnesses) of Miller-Rabin testing.
    :type k: int
    :return: False if the number is composite, True if it's probably prime.
    :rtype: bool
    """
    if n < 2:
        return False
    d = n - 1
    r = 0
    while not d & 1:
        r += 1
        d >>= 1

    for _ in range(k):
        a = rsa.randnum.randint(n - 4) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False

    return True


def is_prime(number):
    """Returns True if the number is prime, and False otherwise.

    >>> is_prime(2)
    True
    >>> is_prime(42)
    False
    >>> is_prime(41)
    True
    >>> [x for x in range(901, 1000) if is_prime(x)]
    [907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    """
    if number < 10:
        return number in (2, 3, 5, 7)
    if not number & 1:
        return False
    return miller_rabin_primality_testing(number, 7)


def getprime(nbits):
    """Returns a prime number that can be stored in 'nbits' bits.

    >>> p = getprime(128)
    >>> is_prime(p-1)
    False
    >>> is_prime(p)
    True
    >>> is_prime(p+1)
    False

    >>> from rsa import common
    >>> common.bit_size(p) == 128
    True
    """
    assert nbits > 3
    while True:
        integer = rsa.randnum.read_random_odd_int(nbits)
        if is_prime(integer):
            return integer


def are_relatively_prime(a, b):
    """Returns True if a and b are relatively prime, and False if they
    are not.

    >>> are_relatively_prime(2, 3)
    True
    >>> are_relatively_prime(2, 4)
    False
    """
    d = gcd(a, b)
    return d == 1


if __name__ == '__main__':
    print 'Running doctests 1000x or until failure'
    import doctest
    for count in range(1000):
        failures, tests = doctest.testmod()
        if failures:
            break
        if count and count % 100 == 0:
            print '%i times' % count

    print 'Doctests done'