# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/recpoisson.py
# Compiled at: 2018-04-23 11:23:30
# Size of source mod 2**32: 2797 bytes
import math, random, sys
if sys.version_info < (3, 2):
    from repoze.lru import lru_cache
else:
    from functools import lru_cache

@lru_cache(1000)
def _get_poisson_var(parameter):
    return Poisson(parameter)


class Poisson(object):

    def __init__(self, parameter):
        self.parameter = parameter

        def c_p(k):
            if k == 0:
                return self._p(0)
            return self._compute_poisson_cdf(k - 1) + self._p(k)

        self._compute_poisson_cdf = lru_cache(int(2.5 * self.parameter) + 1)(c_p)

    @staticmethod
    def _get_random():
        return random.random()

    def _p(self, k):
        l = self.parameter
        l_to_the_k = k * math.log(l)
        k_fact = sum([math.log(i + 1) for i in range(k)])
        return math.exp(l_to_the_k - l - k_fact)

    def sample(self):
        f = self._get_random()
        current_cdf = -1
        current_x = -1
        while current_cdf < f:
            current_x += 1
            current_cdf = self._compute_poisson_cdf(current_x)

        return current_x


def poisson(parameter):
    return _get_poisson_var(parameter).sample()