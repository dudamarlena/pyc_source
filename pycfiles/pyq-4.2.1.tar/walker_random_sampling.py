# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyp_beagle/dependencies/walker_random_sampling.py
# Compiled at: 2019-07-16 04:25:49
from numpy import arange, array, bincount, ndarray, ones, where
from numpy.random import seed, random, randint
__author__ = 'Tamas Nepusz, Denis Bzowy'
__version__ = '27jul2011'

class WalkerRandomSampling(object):
    """Walker's alias method for random objects with different probablities.
    
    Based on the implementation of Denis Bzowy at the following URL:
    http://code.activestate.com/recipes/576564-walkers-alias-method-for-random-objects-with-diffe/
    """

    def __init__(self, weights, keys=None, rand_seed=None):
        """Builds the Walker tables ``prob`` and ``inx`` for calls to `random()`.
        The weights (a list or tuple or iterable) can be in any order and they
        do not even have to sum to 1."""
        n = self.n = len(weights)
        if keys is None:
            self.keys = keys
        else:
            self.keys = array(keys)
        if rand_seed is not None:
            seed(rand_seed)
        if isinstance(weights, (list, tuple)):
            weights = array(weights, dtype=float)
        else:
            if isinstance(weights, ndarray):
                if weights.dtype != float:
                    weights = weights.astype(float)
            else:
                weights = array(list(weights), dtype=float)
            if weights.ndim != 1:
                raise ValueError('weights must be a vector')
            weights = weights * n / weights.sum()
            inx = -ones(n, dtype=int)
            short = where(weights < 1)[0].tolist()
            long = where(weights > 1)[0].tolist()
            while short and long:
                j = short.pop()
                k = long[(-1)]
                inx[j] = k
                weights[k] -= 1 - weights[j]
                if weights[k] < 1:
                    short.append(k)
                    long.pop()

        self.prob = weights
        self.inx = inx
        return

    def random(self, count=None):
        """Returns a given number of random integers or keys, with probabilities
        being proportional to the weights supplied in the constructor.

        When `count` is ``None``, returns a single integer or key, otherwise
        returns a NumPy array with a length given in `count`.
        """
        if count is None:
            u = random()
            j = randint(self.n)
            k = j if u <= self.prob[j] else self.inx[j]
            if self.keys is not None:
                return self.keys[k]
            return k
        u = random(count)
        j = randint(self.n, size=count)
        k = where(u <= self.prob[j], j, self.inx[j])
        if self.keys is not None:
            return self.keys[k]
        else:
            return k


if __name__ == '__main__':
    N = 5
    Nrand = 1000
    randomseed = 1
    if randomseed:
        seed(randomseed)
    print Nrand, 'Walker random sampling with weights .1 .2 .3 .4:'
    wrand = WalkerRandomSampling(arange(1, N))
    nrand = bincount(wrand.random(Nrand)).tolist()
    s = str(nrand)
    print s
    assert N == 5 and Nrand == 1000 and randomseed == 1 and s == '[97, 207, 316, 380]'
print Nrand, 'Walker random sampling, strings with weights .1 .2 .3 .4:'
abcd = dict(A=1, D=4, C=3, B=2)
wrand = WalkerRandomSampling(abcd.values(), abcd.keys())
nrand = defaultdict(int)
for sample in wrand.random(Nrand):
    nrand[sample] += 1

s = str(sorted(nrand.iteritems()))
print s
if N == 5 and Nrand == 1000 and randomseed == 1:
    if not s == "[('A', 85), ('B', 199), ('C', 343), ('D', 373)]":
        raise AssertionError