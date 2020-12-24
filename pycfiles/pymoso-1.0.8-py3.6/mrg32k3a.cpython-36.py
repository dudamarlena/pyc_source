# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/prng/mrg32k3a.py
# Compiled at: 2019-10-01 17:47:30
# Size of source mod 2**32: 8949 bytes
"""
Summary
-------
Provide a subclass of random.Random using mrg32k3a as the generator
with substream support.

Listing
-------
MRG323k3a
get_next_prnstream
jump_substream
"""
import random
from math import log
import functools
a1p127 = [
 [
  2427906178.0, 3580155704.0, 949770784.0],
 [
  226153695.0, 1230515664.0, 3580155704.0],
 [
  1988835001.0, 986791581.0, 1230515664.0]]
a2p127 = [
 [
  1464411153.0, 277697599.0, 1610723613.0],
 [
  32183930.0, 1464411153.0, 1022607788.0],
 [
  2824425944.0, 32183930.0, 2093834863.0]]
a1p76 = [
 [
  82758667.0, 1871391091.0, 4127413238.0],
 [
  3672831523.0, 69195019.0, 1871391091.0],
 [
  3672091415.0, 3528743235.0, 69195019.0]]
a2p76 = [
 [
  1511326704.0, 3759209742.0, 1610795712.0],
 [
  4292754251.0, 1511326704.0, 3889917532.0],
 [
  3859662829.0, 4292754251.0, 3708466080.0]]
mrgnorm = 2.328306549295728e-10
mrgm1 = 4294967087.0
mrgm2 = 4294944443.0
mrga12 = 1403580.0
mrga13n = 810728.0
mrga21 = 527612.0
mrga23n = 1370589.0
bsma = [
 2.50662823884, -18.61500062529, 41.39119773534, -25.44106049637]
bsmb = [-8.4735109309, 23.08336743743, -21.06224101826, 3.13082909833]
bsmc = [0.3374754822726147, 0.9761690190917186, 0.1607979714918209, 0.0276438810333863, 0.0038405729373609, 0.0003951896411919, 3.21767881768e-05, 2.888167364e-07, 3.960315187e-07]

def mrg32k3a(seed):
    """
    Generate a random number between 0 and 1 from a seed.

    Parameters
    ----------
    seed : tuple of int
        Length must be 6.

    Returns
    -------
    newseed : tuple of int
    u : float
    """
    p1 = mrga12 * seed[1] - mrga13n * seed[0]
    k1 = int(p1 / mrgm1)
    p1 -= k1 * mrgm1
    if p1 < 0.0:
        p1 += mrgm1
    else:
        p2 = mrga21 * seed[5] - mrga23n * seed[3]
        k2 = int(p2 / mrgm2)
        p2 -= k2 * mrgm2
        if p2 < 0.0:
            p2 += mrgm2
        if p1 <= p2:
            u = (p1 - p2 + mrgm1) * mrgnorm
        else:
            u = (p1 - p2) * mrgnorm
    newseed = (
     seed[1], seed[2], int(p1), seed[4], seed[5], int(p2))
    return (newseed, u)


def bsm(u):
    """
    Approximate the quantiles of the standard normal distribution.

    Parameters
    ----------
    u : float
        Desired quantile between 0 and 1

    Returns
    -------
    z : float
    """
    y = u - 0.5
    if abs(y) < 0.42:
        r = pow(y, 2)
        r2 = pow(r, 2)
        r3 = pow(r, 3)
        r4 = pow(r, 4)
        asum = sum([bsma[0], bsma[1] * r, bsma[2] * r2, bsma[3] * r3])
        bsum = sum([1, bsmb[0] * r, bsmb[1] * r2, bsmb[2] * r3, bsmb[3] * r4])
        z = y * (asum / bsum)
    else:
        if y < 0.0:
            signum = -1
            r = u
        else:
            signum = 1
            r = 1 - u
        s = log(-log(r))
        s0 = pow(s, 2)
        s1 = pow(s, 3)
        s2 = pow(s, 4)
        s3 = pow(s, 5)
        s4 = pow(s, 6)
        s5 = pow(s, 7)
        s6 = pow(s, 8)
        clst = [bsmc[0], bsmc[1] * s, bsmc[2] * s0, bsmc[3] * s1, bsmc[4] * s2, bsmc[5] * s3, bsmc[6] * s4, bsmc[7] * s5, bsmc[8] * s6]
        t = sum(clst)
        z = signum * t
    return z


class MRG32k3a(random.Random):
    __doc__ = '\n    Implements mrg32k3a as the generator for a random.Random object\n\n    Attributes\n    ----------\n    _current_seed : tuple of int\n        6 integer mrg32k3a seed\n\n    Parameters\n    ----------\n    x : tuple of int, optional\n        Seed from which to start the generator\n\n    See also\n    --------\n    random.Random\n    '

    def __init__(self, x=None):
        if not x:
            x = (12345, 12345, 12345, 12345, 12345, 12345)
        elif not len(x) == 6:
            raise AssertionError
        self.version = 2
        self.generate = mrg32k3a
        self.bsm = bsm
        super().__init__(x)

    def set_class_cache(self, cache_flag):
        """
        Sets whether to use an LRU cache for both the random function and the
        bsm function.

        Parameters
        ----------
        cache_flag : bool

        See also
        --------
        functools.lru_cache
        """
        if not cache_flag:
            self.generate = mrg32k3a
            self.bsm = bsm
        else:
            self.generate = functools.lru_cache(maxsize=None)(mrg32k3a)
            self.bsm = functools.lru_cache(maxsize=None)(bsm)

    def seed(self, a):
        assert len(a) == 6
        self._current_seed = a
        super().seed(a)

    def random(self):
        """
        Generate a standard uniform variate and advance the generator
        state.

        Returns
        -------
        u : float
        """
        seed = self._current_seed
        newseed, u = self.generate(seed)
        self.seed(newseed)
        return u

    def get_seed(self):
        """
        Return the current mrg32k3a seed.

        Returns
        -------
        tuple of int
            The current mrg32k3a seed
        """
        return self._current_seed

    def getstate(self):
        return (
         self.get_seed(), super().getstate())

    def setstate(self, state):
        self.seed(state[0])
        super().setstate(state[1])

    def normalvariate(self, mu=0, sigma=1):
        """
        Generate a normal random variate.

        Parameters
        ----------
        mu : float
            Expected value of the normal distribution from which to
            generate. Default is 0.
        sigma : float
            Standard deviatoin of the normal distribution from which to
            generate. Default is 1.

        Returns
        -------
        float
            A normal variate from the specified distribution

        """
        u = self.random()
        z = self.bsm(u)
        return sigma * z + mu


def mat333mult(a, b):
    """
    Multiply a 3x3 matrix with a 3x1 matrix.

    Parameters
    ----------
    a : tuple of tuple of float
        3x3 matrix
    b : tuple of tuple if float
        3x1 matrix

    Returns
    -------
    res : list of float
        3x1 matrix
    """
    res = [
     0, 0, 0]
    r3 = range(3)
    for i in r3:
        res[i] = sum([a[i][j] * b[j] for j in r3])

    return res


def mat311mod(a, b):
    """
    Compute moduli of a 3x1 matrix.

    Parameters
    ----------
    a : tuple of float
        3x1 matrix
    b : float
        modulus

    Returns
    -------
    res : tuple of float
        3x1 matrix
    """
    res = [
     0, 0, 0]
    r3 = range(3)
    for i in r3:
        res[i] = int(a[i] - int(a[i] / b) * b)

    return res


def get_next_prnstream(seed, use_cache):
    """
    Instantiate a generator seeded 2^127 steps from the input seed.

    Parameters
    ----------
    seed : tuple of int
    crn : bool

    Returns
    -------
    prn : MRG32k3a object
    """
    assert len(seed) == 6
    s1 = seed[0:3]
    s2 = seed[3:6]
    ns1m = mat333mult(a1p127, s1)
    ns2m = mat333mult(a2p127, s2)
    ns1 = mat311mod(ns1m, mrgm1)
    ns2 = mat311mod(ns2m, mrgm2)
    sseed = tuple(ns1 + ns2)
    prn = MRG32k3a(sseed)
    prn.set_class_cache(use_cache)
    return prn


def jump_substream(prn):
    """
    Advance the rng to the next substream 2^76 steps.

    Parameters
    ----------
    prn : MRG32k3a object
    """
    seed = prn.get_seed()
    s1 = seed[0:3]
    s2 = seed[3:6]
    ns1m = mat333mult(a1p76, s1)
    ns2m = mat333mult(a2p76, s2)
    ns1 = mat311mod(ns1m, mrgm1)
    ns2 = mat311mod(ns2m, mrgm2)
    sseed = tuple(ns1 + ns2)
    prn.seed(sseed)