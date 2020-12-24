# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/Primes.py
# Compiled at: 2017-02-25 12:54:13
"""
A module designed to act as a singleton-like prime suite.

Once imported, it begins processes designed to help determine what numbers are prime
and uses concurrent branching to split primality tests and prime factorizations and
speed up the whole process.
"""
import cPickle
from os.path import join
from threading import Thread
from time import sleep
import atexit
from pyspeedup.memory import OrderedDiskDict, DiskDict
if 'D' not in globals():
    D = DiskDict()
    F = OrderedDiskDict()
    c = 3
    p = 3
    q = 9
    thread = None
    file_location = None

def load_primes(location):
    """
    In order to not repeat computation, states and lists
    need to be saved between runs. This function links a
    location to the computations performed to keep results
    indefinitely.
    """
    global D
    global F
    global c
    global file_location
    global p
    stop_seive()
    del D
    D = DiskDict()
    D.link_to_disk('seive', file_location=location, size_limit=65536, max_pages=32)
    del F
    F = OrderedDiskDict()
    F.link_to_disk('factors', file_location=location, size_limit=65536, max_pages=32)
    try:
        with open(D._file_base + 'current', 'rb') as (f):
            c, p = cPickle.load(f)
    except:
        c, p = (3, 3)

    file_location = location


def start_seive():
    global thread
    if thread == None:
        thread = Thread(target=_prime_seive)
        thread.start()
    return


def stop_seive():
    global stop
    global thread
    if thread:
        stop = True
        thread.join()
    thread = None
    return


atexit.register(stop_seive)

def _prime_seive():
    """
    A persistant seive designed to run in the background.
    WARNING: This is continuously use up memory until it
    runs out, at about a rate of x/ln(x-1).
    """
    global c
    global p
    global stop
    stop = False
    if 2 not in F:
        F[2] = 2
    q = p * p
    while stop == False:
        if c not in D:
            if c < q:
                F[c] = c
            else:
                F[c] = [
                 p, p]
                s = 2 * p
                x = c + s
                while x in D:
                    x += s

                D[x] = p
                p = nextPrime(p)
                q = p * p
        else:
            p1 = D.pop(c)
            F[c] = [p1, c // p1]
            s = 2 * p1
            x = c + s
            while x in D:
                x += s

            D[x] = p1
        c += 2
        sleep(0)

    with open(D._file_base + 'current', 'wb') as (f):
        cPickle.dump((c, p), f)


def nextPrime(p):
    """
    Returns the next prime after 'p'.
    """
    p = round(p)
    if p < 2:
        return 2
    if p % 2 == 0:
        p -= 1
    p += 2
    while not is_prime(p):
        p += 2

    return p


def factor(N):
    """
    Set up a bunch of factorization routines in parallel if
    the factors of N are not known. Once one finds two factors,
    stop all the rest of them and return. If one of the algorithms
    tell us that N is prime, return N.

    This function ignores any algorithms that return "probably prime."
    """
    if N in F:
        return F[N]
    if N < -1:
        return [-1, abs(N)]
    if N < 3:
        return N
    if N % 2 == 0:
        return [2, N // 2]
    found = fermat_factorization(N)
    F[N] = found
    return found


def fermat_factorization(N):
    """
    Fermat's factorization algorithm. Takes N and returns two
    of its factors.

    Reference: http://en.wikipedia.org/wiki/Fermat's_factorization_method
    """
    import math
    if N < -1:
        return [-1, N]
    if N < 3:
        return N
    if N % 2 == 0:
        return [2, N // 2]
    a = math.ceil(math.sqrt(N))
    b2 = a * a - N
    b = math.floor(math.sqrt(b2))
    while b * b != b2:
        b2 += a + a + 1
        a += 1
        b = math.floor(math.sqrt(b2))

    if a - b == 1:
        return N
    return [
     a - b, a + b]


def is_prime(N):
    """
    Uses the cached factorization list to retrieve
    whether N is prime (in O(1)) or Fermat's
    factorization method to figure it out (in O(n)).
    """
    if N < 2:
        return False
    if N in F:
        return F[N] == N
    return factor(N) == N


def get_factorization(q):
    """
    Gets the factorization of q either through looking
    up precomputed values (in O(ln(q)) or O(ln(ln(q)))
    after tree balancing) or by running Fermat's
    factorization method (in O(n ln(n))).
    """
    t = []
    if q in F:
        t = F[q]
    else:
        t = factor(q)
    if t != q:
        m = []
        for i in t:
            m.extend(get_factorization(i))

        t = m
    else:
        t = [
         t]
    return t


if __name__ == '__main__':
    from os.path import expanduser
    load_primes('D:/.pyspeedup')
    start_seive()
    while len(F) < 1000000:
        sleep(1)

    stop_seive()
    print c
    print p
    print F[9]
    print F[7]
    print get_factorization(100)
    print F[205]
    print get_factorization(9999999)
# global q ## Warning: Unused global