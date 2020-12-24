# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/mcmc_idxr.py
# Compiled at: 2011-05-13 03:23:36
import re, math, random, numpy, mcmc

class probdist_c(object):

    def __call__(self):
        """Sample from the probability distribution.
                @return: the sample
                @rtype: C{float}
                """
        raise RuntimeError, 'Virtual function'

    def logdens(self, x):
        """Return the log(density) of the probability distribution at x.
                @param x: the position where the density should be evaluated.
                @type x: C{float}
                @return: C{log(density)}
                @rtype: C{float}
                @raise mcmc.NotGoodPosition: when the density is not defined at C{x}.
                """
        raise RuntimeError, 'Virtual function'


class Weibull(probdist_c):
    """Weibull distribution"""

    def __init__(self, scale, shape):
        assert shape >= 0.0 and scale >= 0.0
        self.shape = shape
        self.scale = scale

    def __call__(self):
        return random.weibullvariate(self.scale, self.shape)

    def logdens(self, x):
        assert x >= 0.0
        x /= self.scale
        return -x ** self.shape + math.log(x) * (self.shape - 1) + math.log(self.shape / self.scale)

    @property
    def __doc__(self):
        return 'Weibull(%g,%s)' % (self.scale, self.shape)


class Expo(probdist_c):
    """Exponential distribution"""

    def __init__(self, lmbda):
        assert lmbda > 0.0
        self.lmbda = lmbda

    def __call__(self):
        return random.expovariate(self.lmbda)

    def logdens(self, x):
        if x < 0.0:
            raise mcmc.NotGoodPosition, 'x=%s' % str(x)
        assert x >= 0.0
        return -self.lmbda * x + math.log(self.lmbda)

    @property
    def __doc__(self):
        return 'Exponential(%g)' % self.lmbda


class Normal(probdist_c):
    """Normal distribution"""

    def __init__(self, mu, sigma):
        if sigma <= 0.0:
            raise mcmc.NotGoodPosition, 'sigma=%s' % str(sigma)
        self.mu = mu
        self.sigma = sigma

    def __call__(self):
        return random.normalvariate(self.mu, self.sigma)

    def logdens(self, x):
        return -((x - self.mu) / self.sigma) ** 2 / 2.0 - math.log(math.sqrt(2 * math.pi) * self.sigma)

    @property
    def __doc__(self):
        return 'Normal(%g+-%g)' % (self.mu, self.sigma)


class Uniform(probdist_c):
    """Uniform distribution"""

    def __init__(self, low, high):
        if not low < high:
            raise mcmc.NotGoodPosition, 'low=%s >= high=%s' % (low, high)
        self.low = low
        self.high = high

    def __call__(self):
        return random.uniform(self.low, self.high)

    def logdens(self, x):
        return 1.0 / (self.high - self.low)

    @property
    def __doc__(self):
        return 'Uniform(%g,%g)' % (self.low, self.high)


class LogNormal(probdist_c):
    """Lognormal distribution"""

    def __init__(self, mu, sigma):
        if sigma <= 0.0:
            raise mcmc.NotGoodPosition, 'sigma=%s' % str(sigma)
        self.mu = mu
        self.sigma = sigma

    def __call__(self):
        return self.mu * math.exp(random.normalvariate(0.0, self.sigma))

    def logdens(self, x):
        if (x > 0.0) != (self.mu > 0.0):
            raise mcmc.NotGoodPosition, 'x=%s, mu=%s' % (str(x), str(self.mu))
        x = math.log(x / self.mu)
        return -(x / self.sigma) ** 2 / 2.0 - math.log(math.sqrt(2 * math.pi) * self.sigma)

    @property
    def __doc__(self):
        return 'Lognormal(%g+-%g)' % (self.mu, self.sigma)


def logp_prior_normalized(x, guess_prob_dist):
    """
        @type guess_prob_dist: list((str, probdist_c))
        @type x: newstem2.indexclass.index_base
        @rtype: float
        @return: the log of the prior probability.
        """
    lp = 0.0
    gpd = [ (re.compile(pat), sampler) for pat, sampler in guess_prob_dist ]
    for key in x.map.keys():
        v = x.p(*key)
        vv = None
        fkey = x._fmt(key)
        for pat, sampler in gpd:
            if pat.match(fkey):
                vv = sampler
                break

        if vv is None:
            raise KeyError, "No match found for '%s'" % fkey
        logp = vv.logdens(v)
        lp += logp

    return lp


class problem_definition(mcmc.problem_definition):

    def __init__(self):
        mcmc.problem_definition.__init__(self)
        self.idxr = None
        self.cached = -1e+30
        self.ckey = None
        return

    def set_idxr(self, idxr):
        self.idxr = idxr

    def plot(self, idxr, arg, pylab, inum):
        raise RuntimeError, 'Virtual Function'

    def do_print(self, idxr, arg, iter):
        raise RuntimeError, 'Virtual Function'

    def logp--- This code section failed: ---

 L. 177         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'idxr'
                6  LOAD_CONST               None
                9  COMPARE_OP            9  is-not
               12  POP_JUMP_IF_TRUE     24  'to 24'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_CONST               'You need to call self.set_idxr().'
               21  RAISE_VARARGS_2       2  None

 L. 178        24  LOAD_FAST             0  'self'
               27  LOAD_ATTR             3  'ckey'
               30  LOAD_CONST               None
               33  COMPARE_OP            9  is-not
               36  POP_JUMP_IF_FALSE    73  'to 73'
               39  LOAD_GLOBAL           4  'numpy'
               42  LOAD_ATTR             5  'equal'
               45  LOAD_FAST             0  'self'
               48  LOAD_ATTR             3  'ckey'
               51  LOAD_FAST             1  'x'
               54  CALL_FUNCTION_2       2  None
               57  LOAD_ATTR             6  'all'
               60  CALL_FUNCTION_0       0  None
             63_0  COME_FROM            36  '36'
               63  POP_JUMP_IF_FALSE    73  'to 73'

 L. 179        66  LOAD_FAST             0  'self'
               69  LOAD_ATTR             7  'cached'
               72  RETURN_END_IF    
             73_0  COME_FROM            63  '63'

 L. 180        73  LOAD_FAST             0  'self'
               76  LOAD_ATTR             0  'idxr'
               79  LOAD_ATTR             8  'clear'
               82  CALL_FUNCTION_0       0  None
               85  POP_TOP          

 L. 181        86  LOAD_FAST             0  'self'
               89  LOAD_ATTR             0  'idxr'
               92  LOAD_ATTR             9  'set_prms'
               95  LOAD_FAST             1  'x'
               98  CALL_FUNCTION_1       1  None
              101  POP_TOP          

 L. 182       102  LOAD_FAST             0  'self'
              105  LOAD_ATTR            10  'logp_guts'
              108  LOAD_FAST             0  'self'
              111  LOAD_ATTR             0  'idxr'
              114  CALL_FUNCTION_1       1  None
              117  UNPACK_SEQUENCE_3     3 
              120  STORE_FAST            2  'prob'
              123  STORE_FAST            3  'constraint'
              126  STORE_FAST            4  'logprior'

 L. 183       129  LOAD_FAST             2  'prob'
              132  LOAD_FAST             3  'constraint'
              135  BINARY_SUBTRACT  
              136  LOAD_FAST             4  'logprior'
              139  BINARY_ADD       
              140  LOAD_FAST             0  'self'
              143  STORE_ATTR            7  'cached'

 L. 184       146  LOAD_GLOBAL           4  'numpy'
              149  LOAD_ATTR            11  'array'
              152  LOAD_FAST             0  'self'
              155  LOAD_ATTR             0  'idxr'
              158  LOAD_ATTR            12  'get_prms'
              161  CALL_FUNCTION_0       0  None
              164  LOAD_CONST               'copy'
              167  LOAD_GLOBAL          13  'True'
              170  CALL_FUNCTION_257   257  None
              173  LOAD_FAST             0  'self'
              176  STORE_ATTR            3  'ckey'

 L. 185       179  LOAD_FAST             0  'self'
              182  LOAD_ATTR             7  'cached'
              185  RETURN_VALUE     

Parse error at or near `LOAD_ATTR' instruction at offset 182

    def logp_data_normalized(self, x):
        """Only define this if you can compute the actual probability
                density for the data given model & parameters,
                not just something proportional to it!
                To do this
                function, you need to be able to do the full multidimensional
                integral over the probability distribution!

                NOTE that x is an indexer!
                NOTE that this is not the full logp function: it doesn't contain the prior!
                """
        prob, constraint, logprior = self.logp_guts(x)
        return prob

    def fixer--- This code section failed: ---

 L. 204         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'idxr'
                6  LOAD_CONST               None
                9  COMPARE_OP            9  is-not
               12  POP_JUMP_IF_TRUE     24  'to 24'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_CONST               'You need to call self.set_idxr().'
               21  RAISE_VARARGS_2       2  None

 L. 207        24  LOAD_FAST             0  'self'
               27  LOAD_ATTR             0  'idxr'
               30  LOAD_ATTR             3  'set_prms'
               33  LOAD_FAST             1  'x'
               36  CALL_FUNCTION_1       1  None
               39  POP_TOP          

 L. 208        40  LOAD_FAST             0  'self'
               43  LOAD_ATTR             4  'logp_guts'
               46  LOAD_FAST             0  'self'
               49  LOAD_ATTR             0  'idxr'
               52  CALL_FUNCTION_1       1  None
               55  UNPACK_SEQUENCE_3     3 
               58  STORE_FAST            2  'prob'
               61  STORE_FAST            3  'constraint'
               64  STORE_FAST            4  'logprior'

 L. 210        67  LOAD_FAST             2  'prob'
               70  LOAD_FAST             3  'constraint'
               73  BINARY_SUBTRACT  
               74  LOAD_FAST             4  'logprior'
               77  BINARY_ADD       
               78  LOAD_FAST             0  'self'
               81  STORE_ATTR            5  'cached'

 L. 211        84  LOAD_GLOBAL           6  'numpy'
               87  LOAD_ATTR             7  'array'
               90  LOAD_FAST             0  'self'
               93  LOAD_ATTR             0  'idxr'
               96  LOAD_ATTR             8  'get_prms'
               99  CALL_FUNCTION_0       0  None
              102  LOAD_CONST               'copy'
              105  LOAD_GLOBAL           9  'True'
              108  CALL_FUNCTION_257   257  None
              111  LOAD_FAST             0  'self'
              114  STORE_ATTR           10  'ckey'

 L. 213       117  LOAD_FAST             0  'self'
              120  LOAD_ATTR            10  'ckey'
              123  RETURN_VALUE     

Parse error at or near `LOAD_ATTR' instruction at offset 120

    def logp_prior_normalized(self, x):
        return logp_prior_normalized(x, self.PriorProbDist)

    PriorProbDist = None

    def logp_guts(self, idxr, data_sink=None):
        raise RuntimeError, 'Virtual method'