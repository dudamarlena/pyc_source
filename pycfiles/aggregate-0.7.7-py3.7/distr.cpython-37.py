# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aggregate\distr.py
# Compiled at: 2020-01-21 10:38:07
# Size of source mod 2**32: 112836 bytes
import scipy.stats as ss
import numpy as np
from scipy.integrate import quad
import pandas as pd, collections, logging, json
from .utils import sln_fit, sgamma_fit, ft, ift, axiter_factory, estimate_agg_percentile, suptitle_and_tight, html_title, MomentAggregator, xsden_to_meancv
from .spectral import Distortion
from scipy import interpolate
from scipy.optimize import newton
import IPython.core.display as display
from scipy.special import kv, gammaln, hyp1f1
from scipy.optimize import broyden2, newton_krylov
from scipy.optimize.nonlin import NoConvergence
import itertools
from numpy.linalg import inv, pinv, det, matrix_rank
logger = logging.getLogger('aggregate')

class Frequency(object):
    __doc__ = '\n    Manages Frequency distributions: creates moment function and MGF.\n\n    freq_moms(n): returns EN, EN^2 and EN^3 when EN=n\n\n    mgf(n, z): returns the moment generating function applied to z when EN=n\n\n    **Available Frequency Distributions**\n\n    **Non-Mixture** Types\n\n    * ``fixed``: no parameters\n    * ``bernoulli``: exp_en interpreted as a probability, must be < 1\n    * ``binomial``: Binomial(n, p) where p = freq_a, and n = exp_en\n    * ``poisson``: Poisson(freq_a)\n    * ``pascal``: pascal-poisson distribution, a poisson stopped sum of negative binomial; exp_en gives the overall\n      claim count. freq_a is the CV of the negative binomial distribution and freq_b is the\n      number of claimants per claim (or claims per occurrence). Hence the Poisson component\n      has mean exp_en / freq_b and the number of claims per occurrence has mean freq_b and\n      cv freq_a\n\n    **Mixture** Types\n\n    These distributions are G-mixed Poisson, so N | G ~ Poisson(n G). They are labelled by\n    the name of the mixing distribution or the common name for the resulting frequency\n    distribution. See Panjer and Willmot or JKK.\n\n    In all cases freq_a is the CV of the mixing distribution which corresponds to the\n    asympototic CV of the frequency distribution and of any aggregate when the severity has a variance.\n\n    * ``gamma``: negative binomial, freq_a = cv of gamma distribution\n    * ``delaporte``: shifted gamma, freq_a = cv of mixing disitribution, freq_b = proportion of\n      certain claims = shift. freq_b must be between 0 and 1.\n    * ``ig``: inverse gaussian, freq_a = cv of mixing distribution\n    * ``sig``: shifted inverse gaussian, freq_a = cv of mixing disitribution, freq_b = proportion of\n      certain claims = shift. freq_b must be between 0 and 1.\n    * ``sichel``: generalized inverse gaussian mixing distribution, freq_a = cv of mixing distribution and\n      freq_b = lambda value. The beta and mu parameters solved to match moments. Note lambda =\n      -0.5 corresponds to inverse gaussian and 0.5 to reciprocal inverse gauusian. Other special\n      cases are available.\n    * ``sichel.gamma``: generalized inverse gaussian mixture where the parameters match the moments of a\n      delaporte distribution with given freq_a and freq_b\n    * ``sichel.ig``: generalized inverse gaussian mixture where the parameters match the moments of a\n      shifted inverse gaussian distribution with given freq_a and freq_b. This parameterization\n      has poor numerical stability and may fail.\n    * ``beta``: beta mixing with freq_a = Cv where beta is supported on the interval [0, freq_b]. This\n      method should be used carefully. It has poor numerical stability and can produce bizzare\n      aggregates when the alpha or beta parameters are < 1 (so there is a mode at 0 or freq_b).\n\n    :param freq_name:\n    :param freq_a:\n    :param freq_b:\n\n    '
    __slots__ = [
     'freq_moms', 'mgf', 'freq_name', 'freq_a', 'freq_b']

    def __init__(self, freq_name, freq_a, freq_b):
        self.freq_name = freq_name
        self.freq_a = freq_a
        self.freq_b = freq_b
        logger.info(f"Frequency.__init__ | creating new Frequency {self.freq_name} at {super(Frequency, self).__repr__()}")
        if self.freq_name == 'fixed':

            def _freq_moms(n):
                freq_2 = n ** 2
                freq_3 = n * freq_2
                return (n, freq_2, freq_3)

            def mgf(n, z):
                return z ** n

        else:
            if self.freq_name == 'bernoulli':

                def _freq_moms(n):
                    freq_2 = n
                    freq_3 = n
                    return (n, freq_2, freq_3)

                def mgf(n, z):
                    return z * n + np.ones_like(z) * (1 - n)

            else:
                if self.freq_name == 'binomial':

                    def _freq_moms(n):
                        p = self.freq_a
                        N = n / p
                        freq_1 = N * p
                        freq_2 = N * p * (1 - p + N * p)
                        freq_3 = N * p * (1 + p * (N - 1) * (3 + p * (N - 2)))
                        return (freq_1, freq_2, freq_3)

                    def mgf(n, z):
                        N = n / self.freq_a
                        return (z * self.freq_a + np.ones_like(z) * (1 - self.freq_a)) ** N

                else:
                    if self.freq_name == 'poisson' and self.freq_a == 0:

                        def _freq_moms(n):
                            freq_2 = n * (1 + n)
                            freq_3 = n * (1 + n * (3 + n))
                            return (n, freq_2, freq_3)

                        def mgf(n, z):
                            return np.exp(n * (z - 1))

                    else:
                        if self.freq_name == 'pascal':
                            ν = self.freq_a
                            κ = self.freq_b

                            def _freq_moms(n):
                                c = (n * ν ** 2 - 1 - κ) / κ
                                λ = n / κ
                                g = κ * λ * (2 * c ** 2 * κ ** 2 + 3 * c * κ ** 2 * λ + 3 * c * κ ** 2 + 3 * c * κ + κ ** 2 * λ ** 2 + 3 * κ ** 2 * λ + κ ** 2 + 3 * κ * λ + 3 * κ + 1)
                                return (n, n * (κ * (1 + c + λ) + 1), g)

                            def mgf(n, z):
                                c = (n * ν ** 2 - 1 - κ) / κ
                                a = 1 / c
                                θ = κ * c
                                λ = n / κ
                                return np.exp(λ * ((1 - θ * (z - 1)) ** (-a) - 1))

                        else:
                            if self.freq_name == 'gamma':
                                c = self.freq_a * self.freq_a
                                a = 1 / c
                                θ = c
                                g = 1 + 3 * c + 2 * c * c

                                def _freq_moms(n):
                                    freq_2 = n * (1 + (1 + c) * n)
                                    freq_3 = n * (1 + n * (3 * (1 + c) + n * g))
                                    return (n, freq_2, freq_3)

                                def mgf(n, z):
                                    return (1 - θ * n * (z - 1)) ** (-a)

                            else:
                                if self.freq_name == 'delaporte':
                                    ν = self.freq_a
                                    c = ν * ν
                                    f = self.freq_b
                                    a = (1 - f) ** 2 / c
                                    θ = (1 - f) / a
                                    g = 2 * ν ** 4 / (1 - f) + 3 * c + 1

                                    def _freq_moms(n):
                                        freq_2 = n * (1 + (1 + c) * n)
                                        freq_3 = n * (1 + n * (3 * (1 + c) + n * g))
                                        return (n, freq_2, freq_3)

                                    def mgf(n, z):
                                        return np.exp(f * n * (z - 1)) * (1 - θ * n * (z - 1)) ** (-a)

                                else:
                                    if self.freq_name == 'ig':
                                        ν = self.freq_a
                                        c = ν ** 2
                                        μ = c
                                        λ = 1 / μ
                                        γ = 3 * np.sqrt(μ)
                                        g = γ * ν ** 3 + 3 * c + 1

                                        def _freq_moms(n):
                                            freq_2 = n * (1 + (1 + c) * n)
                                            freq_3 = n * (1 + n * (3 * (1 + c) + n * g))
                                            return (n, freq_2, freq_3)

                                        def mgf(n, z):
                                            return np.exp(1 / μ * (1 - np.sqrt(1 - 2 * μ ** 2 * λ * n * (z - 1))))

                                    else:
                                        if self.freq_name == 'sig':
                                            ν = self.freq_a
                                            f = self.freq_b
                                            c = ν * ν
                                            μ = c / (1 - f) ** 2
                                            λ = (1 - f) / μ
                                            γ = 3 * np.sqrt(μ)
                                            g = γ * ν ** 3 + 3 * c + 1

                                            def _freq_moms(n):
                                                freq_2 = n * (1 + (1 + c) * n)
                                                freq_3 = n * (1 + n * (3 * (1 + c) + n * g))
                                                return (n, freq_2, freq_3)

                                            def mgf(n, z):
                                                return np.exp(f * n * (z - 1)) * np.exp(1 / μ * (1 - np.sqrt(1 - 2 * μ ** 2 * λ * n * (z - 1))))

                                        else:
                                            if self.freq_name == 'beta':
                                                ν = self.freq_a
                                                c = ν * ν
                                                r = self.freq_b
                                                assert r > 1

                                                def _freq_moms(n):
                                                    b = (r - n * (1 + c)) * (r - n) / (c * n * r)
                                                    a = n / (r - n) * b
                                                    g = r ** 3 * np.exp(gammaln(a + b) + gammaln(a + 3) - gammaln(a + b + 3) - gammaln(a))
                                                    freq_2 = n * (1 + (1 + c) * n)
                                                    freq_3 = n * (1 + n * (3 * (1 + c) + n * g))
                                                    return (n, freq_2, freq_3)

                                                def mgf(n, z):
                                                    b = (r - n * (1 + c)) * (r - n) / (c * n * r)
                                                    a = (r - n * (1 + c)) / (c * r)
                                                    return hyp1f1(a, a + b, r * (z - 1))

                                            else:
                                                if self.freq_name[0:6] == 'sichel':
                                                    _type = self.freq_name.split('.')
                                                    add_sichel = True
                                                    ν = self.freq_a
                                                    c = ν * ν
                                                    if len(_type) > 1:
                                                        f = self.freq_b
                                                        λ = -0.5
                                                        μ = 1
                                                        β = ν ** 2
                                                        if _type[1] == 'gamma':
                                                            target = np.array([1, ν, 2 * ν / (1 - f)])
                                                        else:
                                                            if _type[1] == 'ig':
                                                                target = np.array([1, ν, 3.0 * ν / (1 - f)])
                                                            else:
                                                                raise ValueError(f"Inadmissible frequency type {self.freq_name}...")
                                                    else:

                                                        def f(arrIn):
                                                            μ, β, λ = arrIn
                                                            μ = np.exp(μ)
                                                            β = np.exp(β)
                                                            ex1, ex2, ex3 = np.array([μ ** r * kv(λ + r, μ / β) / kv(λ, μ / β) for r in (1,
                                                                                                                                         2,
                                                                                                                                         3)])
                                                            sd = np.sqrt(ex2 - ex1 * ex1)
                                                            skew = (ex3 - 3 * ex2 * ex1 + 2 * ex1 ** 3) / sd ** 3
                                                            return np.array([ex1, sd, skew]) - target

                                                        try:
                                                            params = broyden2(f, (np.log(μ), np.log(β), λ), verbose=False, iter=10000, f_rtol=1e-11)
                                                            if np.linalg.norm(params) > 20:
                                                                λ = -0.5
                                                                μ = 1
                                                                β = ν ** 2
                                                                params1 = newton_krylov(f, (np.log(μ), np.log(β), λ), verbose=False, iter=10000, f_rtol=1e-11)
                                                                logger.warning(f"Frequency.__init__ | {self.freq_name} type Broyden gave large result {params},Newton Krylov {params1}")
                                                                if np.linalg.norm(params) > np.linalg.norm(params1):
                                                                    params = params1
                                                                    logger.warning('Frequency.__init__ | using Newton K')
                                                        except NoConvergence as e:
                                                            try:
                                                                print('ERROR: broyden did not converge')
                                                                print(e)
                                                                add_sichel = False
                                                                raise e
                                                            finally:
                                                                e = None
                                                                del e

                                                else:
                                                    λ = self.freq_b
                                                    target = np.array([1, ν])
                                                    μ = 1
                                                    β = ν ** 2

                                                    def f(arrIn):
                                                        μ, β = arrIn
                                                        μ = np.exp(μ)
                                                        β = np.exp(β)
                                                        ex1, ex2 = np.array([μ ** r * kv(λ + r, μ / β) / kv(λ, μ / β) for r in (1,
                                                                                                                                2)])
                                                        sd = np.sqrt(ex2 - ex1 * ex1)
                                                        return np.array([ex1, sd]) - target

                                                    try:
                                                        params = broyden2(f, (np.log(μ), np.log(β)), verbose=False, iter=10000, f_rtol=1e-11)
                                                    except NoConvergence as e:
                                                        try:
                                                            print('ERROR: broyden did not converge')
                                                            print(e)
                                                            add_sichel = False
                                                            raise e
                                                        finally:
                                                            e = None
                                                            del e

                                                    logger.info(f"{self.freq_name} type, params from Broyden {params}")
                                                    if add_sichel:
                                                        if len(_type) == 1:
                                                            μ, β = params
                                                        else:
                                                            μ, β, λ = params
                                                        μ, β = np.exp(μ), np.exp(β)
                                                        g = μ ** 2 * kv(λ + 2, μ / β) / kv(λ, μ / β)

                                                        def _freq_moms(n):
                                                            freq_2 = n * (1 + (1 + c) * n)
                                                            freq_3 = n * (1 + n * (3 * (1 + c) + n * g))
                                                            return (n, freq_2, freq_3)

                                                        def mgf(n, z):
                                                            kernel = n * (z - 1)
                                                            inner = np.sqrt(1 - 2 * β * kernel)
                                                            return inner ** (-λ) * kv(λ, μ * inner / β) / kv(λ, μ / β)

                                                    else:
                                                        raise ValueError(f"Inadmissible frequency type {self.freq_name}...")
        self.freq_moms = _freq_moms
        self.mgf = mgf

    def __str__(self):
        return f"Frequency object of type {self.freq_name}\n{super(Frequency, self).__repr__()}"


class Aggregate(Frequency):
    __doc__ = "\n    Aggregate distribution class manages creation and calculation of aggregate distributions.\n        Aggregate allows for very flexible creation of Aggregate distributions. Severity\n        can express a limit profile, a mixed severity or both. Mixed frequency types share\n        a mixing distribution across all broadcast terms to ensure an appropriate inter-\n        class correlation.\n\n    Limit Profiles\n        The exposure variables can be vectors to express a *limit profile*.\n        All ```exp_[en|prem|loss|count]``` related elements are broadcast against one-another.\n        For example\n\n        ::\n\n        [100 200 400 100] premium at 0.65 lr [1000 2000 5000 10000] xs 1000\n\n        expresses a limit profile with 100 of premium at 1000 x 1000; 200 at 2000 x 1000\n        400 at 5000 x 1000 and 100 at 10000 x 1000. In this case all the loss ratios are\n        the same, but they could vary too, as could the attachments.\n\n    Mixtures\n        The severity variables can be vectors to express a *mixed severity*. All ``sev_``\n        elements are broadcast against one-another. For example\n\n        ::\n\n            sev lognorm 1000 cv [0.75 1.0 1.25 1.5 2] wts [0.4, 0.2, 0.1, 0.1, 0.1]\n\n        expresses a mixture of five lognormals with a mean of 1000 and CVs as indicated with\n        weights 0.4, 0.2, 0.1, 0.1, 0.1. Equal weights can be express as wts=[5], or the\n        relevant number of components.\n\n    Limit Profiles and Mixtures\n        Limit profiles and mixtures can be combined. Each mixed severity is applied to each\n        limit profile component. For example\n\n        ::\n\n            ag = uw('agg multiExp [10 20 30] claims [100 200 75] xs [0 50 75]\n                sev lognorm 100 cv [1 2] wts [.6 .4] mixed gamma 0.4')```\n\n        creates an aggregate with six severity subcomponents\n\n        +---+-------+------------+--------+\n        | # | limit | attachment | claims |\n        +===+=======+============+========+\n        | 0 | 100   |  0         |  6     |\n        +---+-------+------------+--------+\n        | 1 | 100   |  0         |  4     |\n        +---+-------+------------+--------+\n        | 2 | 200   | 50         | 12     |\n        +---+-------+------------+--------+\n        | 3 | 200   | 50         |  8     |\n        +---+-------+------------+--------+\n        | 4 |  75   | 75         | 18     |\n        +---+-------+------------+--------+\n        | 5 |  75   | 75         | 12     |\n        +---+-------+------------+--------+\n\n    Circumventing Products\n        It is sometimes desirable to enter two or more lines each with a different severity but\n        with a shared mixing variable. For example to model the current accident year and a run-\n        off reserve, where the current year is gamma mean 100 cv 1 and the reserves are\n        larger lognormal mean 150 cv 0.5 claims requires\n\n        ::\n\n            agg MixedPremReserve [100 200] claims sev [gamma lognorm] [100 150] cv [1 0.5] mixed gamma 0.4\n\n        so that the result is not the four-way exposure / severity product but just a two-way\n        combination. These two cases are distinguished looking at the total weights. If the weights sum to\n        one then the result is an exposure / severity product. If the weights are missing or sum to the number\n        of severity components (i.e. are all equal to 1) then the result is a row by row combination.\n\n    Other Programs\n        Below are a series of programs illustrating the different ways exposure, frequency and severity can be\n        broadcast together, several different types of severity and all the different types of severity.\n\n        ::\n\n            test_string_0 = '''\n            # use to create sev and aggs so can illustrate use of sev. and agg. below\n\n            sev sev1 lognorm 10 cv .3\n\n            agg Agg0 1 claim sev lognorm 10 cv .09 fixed\n\n            '''\n\n            test_string_1 = f'''\n            agg Agg1  1 claim sev {10*np.exp(-.3**2/2)} * lognorm .3      fixed note{{sigma=.3 mean=10}}\n            agg Agg2  1 claim sev {10*np.exp(-.3**2/2)} * lognorm .3 + 5  fixed note{{shifted right by 5}}'''             '''\n            agg Agg3  1 claim sev 10 * lognorm 0.5 cv .3                  fixed note{mean 0.5 scaled by 10 and cv 0.3}\n            agg Agg4  1 claim sev 10 * lognorm 1 cv .5 + 5                fixed note{shifted right by 5}\n\n            agg Agg5  1 claim sev 10 * gamma .3                           fixed note{gamma distribution....can use any two parameter scipy.stats distribution plus expon, uniform and normal}\n            agg Agg6  1 claim sev 10 * gamma 1 cv .3 + 5                  fixed note{mean 10 x 1, cv 0.3 shifted right by 5}\n\n            agg Agg7  1 claim sev 2 * pareto 1.6 - 2                      fixed note{pareto alpha=1.6 lambda=2}\n            agg Agg8  1 claim sev 2 * uniform 5 + 2.5                     fixed note{uniform 2.5 to 12.5}\n\n            agg Agg9  1 claim 10 x  2 sev lognorm 20 cv 1.5               fixed note{10 x 2 layer, 1 claim}\n            agg Agg10 10 loss 10 xs 2 sev lognorm 20 cv 1.5               fixed note{10 x 2 layer, total loss 10, derives requency}\n            agg Agg11 14 prem at .7    10 x 1 sev lognorm 20 cv 1.5       fixed note{14 prem at .7 lr derive frequency}\n            agg Agg11 14 prem at .7 lr 10 x 1 sev lognorm 20 cv 1.5       fixed note{14 prem at .7 lr derive frequency, lr is optional}\n\n            agg Agg12: 14 prem at .7 lr (10 x 1) sev (lognorm 20 cv 1.5)  fixed note{trailing semi and other punct ignored};\n\n            agg Agg13: 1 claim sev 50 * beta 3 2 + 10 fixed note{scaled and shifted beta, two parameter distribution}\n            agg Agg14: 1 claim sev 100 * expon + 10   fixed note{exponential single parameter, needs scale, optional shift}\n            agg Agg15: 1 claim sev 10 * norm + 50     fixed note{normal is single parameter too, needs scale, optional shift}\n\n            # any scipy.stat distribution taking one parameter can be used; only cts vars supported on R+ make sense\n            agg Agg16: 1 claim sev 1 * invgamma 4.07 fixed  note{inverse gamma distribution}\n\n            # mixtures\n            agg MixedLine1: 1 claim 25 xs 0 sev lognorm 10                   cv [0.2, 0.4, 0.6, 0.8, 1.0] wts=5             fixed note{equally weighted mixture of 5 lognormals different cvs}\n            agg MixedLine2: 1 claim 25 xs 0 sev lognorm [10, 15, 20, 25, 50] cv [0.2, 0.4, 0.6, 0.8, 1.0] wts=5             fixed note{equal weighted mixture of 5 lognormals different cvs and means}\n            agg MixedLine3: 1 claim 25 xs 0 sev lognorm 10                   cv [0.2, 0.4, 0.6, 0.8, 1.0] wt [.2, .3, .3, .15, .05]   fixed note{weights scaled to equal 1 if input}\n\n            # limit profile\n            agg LimitProfile1: 1 claim [1, 5, 10, 20] xs 0 sev lognorm 10 cv 1.2 wt [.50, .20, .20, .1]   fixed note{maybe input EL by band for wt}\n            agg LimitProfile2: 5 claim            20  xs 0 sev lognorm 10 cv 1.2 wt [.50, .20, .20, .1]   fixed note{input EL by band for wt}\n            agg LimitProfile3: [10 10 10 10] claims [inf 10 inf 10] xs [0 0 5 5] sev lognorm 10 cv 1.25   fixed note{input counts directly}\n\n            # limits and distribution blend\n            agg Blend1 50  claims [5 10 15] x 0         sev lognorm 12 cv [1, 1.5, 3]          fixed note{options all broadcast against one another, 50 claims of each}\n            agg Blend2 50  claims [5 10 15] x 0         sev lognorm 12 cv [1, 1.5, 3] wt=3     fixed note{options all broadcast against one another, 50 claims of each}\n\n            agg Blend5cv1  50 claims  5 x 0 sev lognorm 12 cv 1 fixed\n            agg Blend10cv1 50 claims 10 x 0 sev lognorm 12 cv 1 fixed\n            agg Blend15cv1 50 claims 15 x 0 sev lognorm 12 cv 1 fixed\n\n            agg Blend5cv15  50 claims  5 x 0 sev lognorm 12 cv 1.5 fixed\n            agg Blend10cv15 50 claims 10 x 0 sev lognorm 12 cv 1.5 fixed\n            agg Blend15cv15 50 claims 15 x 0 sev lognorm 12 cv 1.5 fixed\n\n            # semi colon can be used for newline and backslash works\n            agg Blend5cv3  50 claims  5 x 0 sev lognorm 12 cv 3 fixed; agg Blend10cv3 50 claims 10 x 0 sev lognorm 12 cv 3 fixed\n            agg Blend15cv3 50 claims 15 x 0 sev             lognorm 12 cv 3 fixed\n\n            # not sure if it will broadcast limit profile against severity mixture...\n            agg LimitProfile4: [10 30 15 5] claims [inf 10 inf 10] xs [0 0 5 5] sev lognorm 10 cv [1.0, 1.25, 1.5] wts=3  fixed note{input counts directly}\n            '''             f'''\n            # the logo\n            agg logo 1 claim {np.linspace(10, 250, 20)} xs 0 sev lognorm 100 cv 1 fixed'''\n\n            test_string_2 = '''\n            # empirical distributions\n            agg dHist1 1 claim sev dhistogram xps [1, 10, 40] [.5, .3, .2] fixed     note{discrete histogram}\n            agg cHist1 1 claim sev chistogram xps [1, 10, 40] [.5, .3, .2] fixed     note{continuous histogram, guessed right hand endpiont}\n            agg cHist2 1 claim sev chistogram xps [1 10 40 45] [.5 .3 .2]  fixed     note{continuous histogram, explicit right hand endpoint, don't need commas}\n            agg BodoffWind  1 claim sev dhistogram xps [0,  99] [0.80, 0.20] fixed   note{examples from Bodoffs paper}\n            agg BodoffQuake 1 claim sev dhistogram xps [0, 100] [0.95, 0.05] fixed\n\n            # set up fixed sev for future use\n            sev One dhistogram xps [1] [1]   note{a certain loss of 1}\n            '''\n\n            test_string_3 = '''\n            # sev, agg and port: using built in objects [have to exist prior to running program]\n            agg ppa:       0.01 * agg.PPAL       note{this is using lmult on aggs, needs a dictionary specification to adjust means}\n            agg cautoQS:   1e-5 * agg.CAL        note{lmult is quota share or scale for rmul see below }\n            agg cautoClms: agg.CAL * 1e-5        note{rmult adjusts the claim count}\n\n            # scaling works with distributions already made by uw\n            agg mdist: 5000 * agg.dHist1\n\n            '''\n\n            test_string_4 = '''\n            # frequency options\n            agg FreqFixed      10 claims sev sev.One fixed\n            agg FreqPoisson    10 claims sev sev.One poisson                   note{Poisson frequency}\n            agg FreqBernoulli  .8 claims sev sev.One bernoulli               note{Bernoulli en is frequency }\n            agg FreqBinomial   10 claims sev sev.One binomial 0.5\n            agg FreqPascal     10 claims sev sev.One pascal .8 3\n\n            # mixed freqs\n            agg FreqNegBin     10 claims sev sev.One (mixed gamma 0.65)     note{gamma mixed Poisson = negative binomial}\n            agg FreqDelaporte  10 claims sev sev.One mixed delaporte .65 .25\n            agg FreqIG         10 claims sev sev.One mixed ig  .65\n            agg FreqSichel     10 claims sev sev.One mixed delaporte .65 -0.25\n            agg FreqSichel.gamma  10 claims sev sev.One mixed sichel.gamma .65 .25\n            agg FreqSichel.ig     10 claims sev sev.One mixed sichel.ig  .65 .25\n            agg FreqBeta       10 claims sev sev.One mixed beta .5  4  note{second param is max mix}\n            '''\n            test_strings = [test_string_0, test_string_1, test_string_2, test_string_3, test_string_4]\n\n            # run the various tests\n            uw = agg.Underwriter()\n            uw.glob = globals()\n            uw.create_all = True\n            uw.update = True\n            uw.log2 = 8\n            ans = {}\n            # make sure we have this base first:\n            uw('sev One dhistogram xps [1] [1]   note{a certain loss of 1}')\n            for i, t in enumerate(test_strings):\n                print(f'line {i} of {len(test_strings)}')\n                ans.update(uw(t))\n\n    Other Notes\n        How Expected Claim Count is determined etc.\n        * en determines en\n        * prem x loss ratio -> el\n        * severity x en -> el\n\n        * always have en and el; may have prem and exp_lr\n        * if prem then exp_lr computed\n        * if exp_lr then premium computed\n\n        * el is determined using np.where(el==0, prem*exp_lr, el)\n        * if el==0 then el = freq * sev\n        * assert np.all( el>0 or en>0 )\n\n        * call with el (or prem x exp_lr) (or n) expressing a mixture, with the same severity\n        * call with el expressing lines of business with an array of severities\n        * call with single el and array of sevs expressing a mixture; [] broken down by weights\n\n        * n is the CONDITIONAL claim count\n        * X is the GROUND UP severity, so X | X > attachment is used and generates n claims\n\n        * For fixed or histogram have to separate the parameter so they are not broad cast; otherwise\n          you end up with multiple lines when you intend only one\n\n\n        :param name:            name of the aggregate\n        :param exp_el:          expected loss or vector\n        :param exp_premium:     premium volume or vector  (requires loss ratio)\n        :param exp_lr:          loss ratio or vector  (requires premium)\n        :param exp_en:          expected claim count per segment (self.n = total claim count)\n        :param exp_attachment:  occurrence attachment\n        :param exp_limit:       occurrence limit\n        :param sev_name:        severity name or sev.BUILTIN_SEV or meta.var agg or port or similar or vector or matrix\n        :param sev_a:           scipy stats shape parameter\n        :param sev_b:           scipy stats shape parameter\n        :param sev_mean:        average (unlimited) severity\n        :param sev_cv:          unlimited severity coefficient of variation\n        :param sev_loc:         scipy stats location parameter\n        :param sev_scale:       scipy stats scale parameter\n        :param sev_xs:          xs and ps must be provided if sev_name is (c|d)histogram, xs are the bucket break points\n        :param sev_ps:          ps are the probability densities within each bucket; if buckets equal size no adjustments needed\n        :param sev_wt:          weight for mixed distribution\n        :param freq_name:       name of frequency distribution\n        :param freq_a:          cv of freq dist mixing distribution\n        :param freq_b:          claims per occurrence (delaporte or sig), scale of beta or lambda (Sichel)\n    "
    aggregate_keys = [
     'name', 'exp_el', 'exp_premium', 'exp_lr', 'exp_en', 'exp_attachment', 'exp_limit', 'sev_name',
     'sev_a', 'sev_b', 'sev_mean', 'sev_cv', 'sev_loc', 'sev_scale', 'sev_xs', 'sev_ps',
     'sev_wt', 'freq_name', 'freq_a', 'freq_b', 'note']

    @property
    def spec(self):
        """
        get the dictionary specification but treat as a read only
        property
        :return:
        """
        return self._spec

    @property
    def density_df(self):
        """
        create and return the _density_df data frame
        read only property...though if you write d = a.density_df you can obviously edit d...
        :return:
        """
        if self._density_df is None:
            self._density_df = pd.DataFrame(dict(loss=(self.xs), p=(self.agg_density), p_sev=(self.sev_density)))
            eps = 2.5e-16
            self._density_df.loc[:, self._density_df.select_dtypes(include=['float64']).columns] = self._density_df.select_dtypes(include=['float64']).applymap(lambda x:             if abs(x) < eps:
0 # Avoid dead code: x)
            self._density_df = self._density_df.set_index('loss', drop=False)
            self._density_df['log_p'] = np.log(self._density_df.p)
            if self._density_df.p_sev.dtype == np.dtype('O'):
                self._density_df['log_p_sev'] = np.nan
            else:
                self._density_df['log_p_sev'] = np.log(self._density_df.p_sev)
            self._density_df['F'] = self._density_df.p.cumsum()
            self._density_df['F_sev'] = self._density_df.p_sev.cumsum()
            self._density_df['S'] = 1 - self._density_df.F
            self._density_df['S_sev'] = 1 - self._density_df.F_sev
            self._density_df['lev'] = np.hstack((0, self._density_df.S.iloc[:-1])).cumsum() * self.bs
            self._density_df['exa'] = self._density_df['lev']
            self._density_df['exlea'] = (self._density_df.lev - self._density_df.loss * self._density_df.S) / self._density_df.F
            n_ = self._density_df.shape[0]
            if n_ < 1100:
                mult = 1
            else:
                if n_ < 15000:
                    mult = 10
                else:
                    mult = 100
            loss_max = self._density_df[['loss', 'exlea']].query(' exlea > loss ').loss.max()
            if np.isnan(loss_max):
                loss_max = 0
            else:
                loss_max += mult * self.bs
            self._density_df.loc[0:loss_max, 'exlea'] = 0
            self._density_df['e'] = np.sum(self._density_df.p * self._density_df.loss)
            self._density_df.loc[:, 'epd'] = np.maximum(0, self._density_df.loc[:, 'e'] - self._density_df.loc[:, 'lev']) / self._density_df.loc[:, 'e']
            self._density_df['exgta'] = self._density_df.loss + (self._density_df.e - self._density_df.exa) / self._density_df.S
            self._density_df['exeqa'] = self._density_df.loss
        return self._density_df

    def rescale(self, scale, kind='homog'):
        """
        return a rescaled Aggregate object - used to compute derivatives

        all need to be safe mults because of array specification there is an array that is not a numpy array

        TODO have parser return numpy arrays not lists!

        :param scale:  amount of scale
        :param kind:  homog of inhomog

        :return:
        """
        spec = self._spec.copy()

        def safe_scale(sc, x):
            """
            if x is a list wrap it

            :param x:
            :param sc:
            :return: sc x
            """
            if type(x) == list:
                return sc * np.array(x)
            return sc * x

        if kind == 'homog':
            spec['exp_el'] = safe_scale(scale, spec['exp_el'])
            spec['exp_premium'] = safe_scale(scale, spec['exp_premium'])
            spec['exp_attachment'] = safe_scale(scale, spec['exp_attachment'])
            spec['exp_limit'] = safe_scale(scale, spec['exp_limit'])
            spec['sev_loc'] = safe_scale(scale, spec['sev_loc'])
            if type(spec['sev_scale']) not in (int, float) or spec['sev_scale']:
                spec['sev_scale'] = safe_scale(scale, spec['sev_scale'])
            else:
                spec['sev_mean'] = safe_scale(scale, spec['sev_mean'])
            if spec['sev_xs']:
                spec['sev_xs'] = safe_scale(scale, spec['sev_xs'])
        else:
            if kind == 'inhomog':
                spec['exp_el'] = safe_scale(scale, spec['exp_el'])
                spec['exp_premium'] = safe_scale(scale, spec['exp_premium'])
                spec['exp_n'] = safe_scale(scale, spec['exp_n'])
            else:
                raise ValueError(f"Inadmissible option {kind} passed to rescale, kind should be homog or inhomog.")
        return Aggregate(**spec)

    def __init__(self, name, exp_el=0, exp_premium=0, exp_lr=0, exp_en=0, exp_attachment=0, exp_limit=np.inf, sev_name='', sev_a=0, sev_b=0, sev_mean=0, sev_cv=0, sev_loc=0, sev_scale=0, sev_xs=None, sev_ps=None, sev_wt=1, freq_name='', freq_a=0, freq_b=0, note=''):

        def get_value(v):
            if isinstance(v, list):
                return v[0]
            return v

        self.name = get_value(name)
        self._spec = dict(name=name, exp_el=exp_el, exp_premium=exp_premium, exp_lr=exp_lr, exp_en=exp_en, exp_attachment=exp_attachment,
          exp_limit=exp_limit,
          sev_name=sev_name,
          sev_a=sev_a,
          sev_b=sev_b,
          sev_mean=sev_mean,
          sev_cv=sev_cv,
          sev_loc=sev_loc,
          sev_scale=sev_scale,
          sev_xs=sev_xs,
          sev_ps=sev_ps,
          sev_wt=sev_wt,
          freq_name=freq_name,
          freq_a=freq_a,
          freq_b=freq_b,
          note=note)
        logger.info(f"Aggregate.__init__ | creating new Aggregate {self.name} at {super(Aggregate, self).__repr__()}")
        Frequency.__init__(self, get_value(freq_name), get_value(freq_a), get_value(freq_b))
        self.note = note
        self.sev_density = None
        self.ftagg_density = None
        self.agg_density = None
        self.xs = None
        self.fzapprox = None
        self.agg_m, self.agg_cv, self.agg_skew = (0, 0, 0)
        self._linear_quantile_function = None
        self._cdf = None
        self._pdf = None
        self.en = None
        self.n = 0
        self.attachment = None
        self.limit = None
        self.sev_density = None
        self.fzapprox = None
        self.agg_density = None
        self.ftagg_density = None
        self.xs = None
        self.bs = 0
        self.log2 = 0
        self.dh_agg_density = None
        self.dh_sev_density = None
        self.beta_name = ''
        self.sevs = None
        self.audit_df = None
        self._careful_q = None
        self._density_df = None
        self._linear_quantile_function
        self.q_temp = None
        self.statistics_df = pd.DataFrame(columns=([
         'name', 'limit', 'attachment', 'sevcv_param', 'el', 'prem', 'lr'] + MomentAggregator.column_names() + [
         'mix_cv']))
        self.statistics_total_df = self.statistics_df.copy()
        ma = MomentAggregator(self.freq_moms)
        if not isinstance(exp_el, collections.Iterable):
            exp_el = np.array([exp_el])
        else:
            if not isinstance(sev_wt, collections.Iterable):
                sev_wt = np.array([sev_wt])
            elif np.sum(sev_wt) == len(sev_wt):
                exp_el, exp_premium, exp_lr, en, attachment, limit, sev_name, sev_a, sev_b, sev_mean, sev_cv, sev_loc, sev_scale, sev_wt = np.broadcast_arrays(exp_el, exp_premium, exp_lr, exp_en, exp_attachment, exp_limit, sev_name, sev_a, sev_b, sev_mean, sev_cv, sev_loc, sev_scale, sev_wt)
                exp_el = np.where(exp_el > 0, exp_el, exp_premium * exp_lr)
                all_arrays = list(zip(exp_el, exp_premium, exp_lr, en, attachment, limit, sev_name, sev_a, sev_b, sev_mean, sev_cv, sev_loc, sev_scale, sev_wt))
                self.en = en
                self.attachment = attachment
                self.limit = limit
                n_components = len(all_arrays)
                logger.info(f"Aggregate.__init__ | Broadcast/align: exposures + severity = {len(exp_el)} exp = {len(sev_a)} sevs = {n_components} componets")
                self.sevs = np.empty(n_components, dtype=(type(Severity)))
            else:
                exp_el, exp_premium, exp_lr, en, attachment, limit = np.broadcast_arrays(exp_el, exp_premium, exp_lr, exp_en, exp_attachment, exp_limit)
                sev_name, sev_a, sev_b, sev_mean, sev_cv, sev_loc, sev_scale, sev_wt = np.broadcast_arrays(sev_name, sev_a, sev_b, sev_mean, sev_cv, sev_loc, sev_scale, sev_wt)
                exp_el = np.where(exp_el > 0, exp_el, exp_premium * exp_lr)
                exp_arrays = [exp_el, exp_premium, exp_lr, en, attachment, limit]
                sev_arrays = [sev_name, sev_a, sev_b, sev_mean, sev_cv, sev_loc, sev_scale, sev_wt]
                all_arrays = [[k for j in i for k in j] for i in itertools.product(zip(*exp_arrays), zip(*sev_arrays))]
                self.en = np.array([i[3] * i[(-1)] for i in all_arrays])
                self.attachment = np.array([i[4] for i in all_arrays])
                self.limit = np.array([i[5] for i in all_arrays])
                n_components = len(all_arrays)
                logger.info(f"Aggregate.__init__ | Broadcast/product: exposures x severity = {len(exp_arrays)} x {len(sev_arrays)} =  {n_components}")
                self.sevs = np.empty(n_components, dtype=(type(Severity)))
            mix_cv = self.freq_a
            r = 0
            for _el, _pr, _lr, _en, _at, _y, _sn, _sa, _sb, _sm, _scv, _sloc, _ssc, _swt in all_arrays:
                self.sevs[r] = Severity(_sn, _at, _y, _sm, _scv, _sa, _sb, _sloc, _ssc, sev_xs, sev_ps, True)
                sev1, sev2, sev3 = self.sevs[r].moms()
                if _en > 0:
                    _el = _en * sev1
                elif _el > 0:
                    _en = _el / sev1
                if _pr > 0:
                    _lr = _el / _pr
                else:
                    if _lr > 0:
                        _pr = _el / _lr
                    _pr *= _swt
                    _el *= _swt
                    _lr *= _swt
                    _en *= _swt
                    ma.add_f1s(_en, sev1, sev2, sev3)
                    self.statistics_df.loc[r, :] = [
                     self.name, _y, _at, _scv, _el, _pr, _lr] + ma.get_fsa_stats(total=False) + [mix_cv]
                    r += 1

            avg_limit = np.sum(self.statistics_df.limit * self.statistics_df.freq_1) / ma.tot_freq_1
            avg_attach = np.sum(self.statistics_df.attachment * self.statistics_df.freq_1) / ma.tot_freq_1
            tot_prem = self.statistics_df.prem.sum()
            tot_loss = self.statistics_df.el.sum()
            if tot_prem > 0:
                lr = tot_loss / tot_prem
            else:
                lr = np.nan
        self.statistics_total_df.loc['mixed', :] = [self.name, avg_limit, avg_attach, 0, tot_loss, tot_prem, lr] + ma.get_fsa_stats(total=True, remix=True) + [mix_cv]
        self.statistics_total_df.loc['independent', :] = [
         self.name, avg_limit, avg_attach, 0, tot_loss, tot_prem, lr] + ma.get_fsa_stats(total=True, remix=False) + [mix_cv]
        self.statistics_df['wt'] = self.statistics_df.freq_1 / ma.tot_freq_1
        self.statistics_total_df['wt'] = self.statistics_df.wt.sum()
        self.n = ma.tot_freq_1
        self.agg_m = self.statistics_total_df.loc[('mixed', 'agg_m')]
        self.agg_cv = self.statistics_total_df.loc[('mixed', 'agg_cv')]
        self.agg_skew = self.statistics_total_df.loc[('mixed', 'agg_skew')]
        self.report_ser = ma.stats_series((self.name), (np.max(self.limit)), 0.999, remix=True)
        self._middle_q = None
        self._q = None

    def __repr__(self):
        return f"{super(Aggregate, self).__repr__()} name: {self.name}"

    def __str__(self):
        """
        Goal: readability

        :return:
        """
        ags = self.statistics_total_df.loc['mixed', :]
        s = f"Aggregate: {self.name}\n\tEN={ags['freq_1']}, CV(N)={ags['freq_cv']:5.3f}\n\t{len(self.sevs)} severit{'ies' if len(self.sevs) > 1 else 'y'}, EX={ags['sev_1']:,.1f}, CV(X)={ags['sev_cv']:5.3f}\n\tEA={ags['agg_1']:,.1f}, CV={ags['agg_cv']:5.3f}"
        return s

    def _repr_html_(self):
        s = [
         f"<h3>Aggregate object: {self.name}</h3>"]
        s.append(f"Claim count {self.n:0,.2f}, {self.freq_name} distribution<br>")
        _n = len(self.statistics_df)
        if _n == 1:
            sv = self.sevs[0]
            if sv.limit == np.inf and sv.attachment == 0:
                _la = 'unlimited'
            else:
                _la = f"{sv.limit} xs {sv.attachment}"
            s.append(f"Severity{sv.long_name} distribution, {_la}<br>")
        else:
            s.append(f"Severity with {_n} components<br>")
        if self.bs > 0:
            s.append(f"Updated with bucket size {self.bs:.2f} and log2 = {self.log2}")
        st = self.statistics_total_df.loc['mixed', :]
        sev_m = st.sev_m
        sev_cv = st.sev_cv
        sev_skew = st.sev_skew
        n_m = st.freq_m
        n_cv = st.freq_cv
        a_m = st.agg_m
        a_cv = st.agg_cv
        _df = pd.DataFrame({'E(X)':[sev_m, n_m, a_m],  'CV(X)':[sev_cv, n_cv, a_cv],  'Skew(X)':[
          sev_skew, self.statistics_total_df.loc[('mixed', 'freq_skew')], st.agg_skew]},
          index=[
         'Sev', 'Freq', 'Agg'])
        _df.index.name = 'X'
        if self.audit_df is not None:
            esev_m = self.audit_df.loc[('mixed', 'emp_sev_1')]
            esev_cv = self.audit_df.loc[('mixed', 'emp_sev_cv')]
            ea_m = self.audit_df.loc[('mixed', 'emp_agg_1')]
            ea_cv = self.audit_df.loc[('mixed', 'emp_agg_cv')]
            _df.loc[('Sev', 'Est E(X)')] = esev_m
            _df.loc[('Agg', 'Est E(X)')] = ea_m
            _df.loc[:, 'Err E(X)'] = _df['Est E(X)'] / _df['E(X)'] - 1
            _df.loc[('Sev', 'Est CV(X)')] = esev_cv
            _df.loc[('Agg', 'Est CV(X)')] = ea_cv
            _df.loc[:, 'Err CV(X)'] = _df['Est CV(X)'] / _df['CV(X)'] - 1
            _df = _df[['E(X)', 'Est E(X)', 'Err E(X)', 'CV(X)', 'Est CV(X)', 'Err CV(X)', 'Skew(X)']]
        _df = _df.fillna('')
        return '\n'.join(s) + _df._repr_html_()

    def discretize(self, sev_calc, discretization_calc='survival'):
        """
        Continuous is used when you think of the resulting distribution as continuous across the buckets
        (which we generally don't). We use the discretized distribution as though it is fully discrete
        and only takes values at the bucket points. Hence we should use sev_calc='discrete'. The buckets are
        shifted left by half a bucket, so :math:`Pr(X=b_i) = Pr( b_i - b/2 < X <= b_i + b/2)`.

        The other wrinkle is the right hand end of the range. If we extend to np.inf then we ensure we have
        probabilities that sum to 1. But that method introduces a probability mass in the last bucket that
        is often not desirable (we expect to see a smooth continuous distribution and we get a mass). The
        other alternative is to use endpoint = 1 bucket beyond the last, which avoids this problem but can leave
        the probabilities short. We opt here for the latter and rescale

        :param sev_calc:  continuous or discrete or raw (for...)
        :param discretization_calc:  survival, distribution or both
        :return:
        """
        if sev_calc == 'continuous':
            adj_xs = np.hstack((self.xs, self.xs[(-1)] + self.bs))
        else:
            if sev_calc == 'discrete':
                adj_xs = np.hstack((self.xs - self.bs / 2, self.xs[(-1)] + self.bs / 2))
            else:
                if sev_calc == 'raw':
                    adj_xs = self.xs
                else:
                    raise ValueError(f"Invalid parameter {sev_calc} passed to double_diff; options are raw, discrete or histogram")
        beds = []
        for fz in self.sevs:
            if discretization_calc == 'both':
                appx = np.maximum(np.diff(fz.cdf(adj_xs)), -np.diff(fz.sf(adj_xs)))
                beds.append(appx / np.sum(appx))
            elif discretization_calc == 'survival':
                appx = -np.diff(fz.sf(adj_xs))
                beds.append(appx / np.sum(appx))
            elif discretization_calc == 'distribution':
                appx = np.diff(fz.cdf(adj_xs))
                beds.append(appx / np.sum(appx))
            else:
                raise ValueError(f"Invalid options {discretization_calc} to double_diff; options are density, survival or both")

        return beds

    def easy_update(self, log2=13, bs=0, **kwargs):
        """
        Convenience function, delegates to update. Avoids having to pass xs.

        :param log2:
        :param bs:
        :param kwargs:  passed through to update
        :return:
        """
        if bs == 0:
            bs = self.recommend_bucket(log2)
        else:
            xs = np.arange(0, (1 << log2), dtype=float) * bs
            if 'approximation' not in kwargs:
                if self.n > 100:
                    kwargs['approximation'] = 'slognorm'
                else:
                    kwargs['approximation'] = 'exact'
        return (self.update)(xs, **kwargs)

    def update(self, xs, padding=1, tilt_vector=None, approximation='exact', sev_calc='discrete', discretization_calc='survival', force_severity=False, verbose=False):
        """
        Compute the density

        :param xs:  range of x values used to discretize
        :param padding: for FFT calculation
        :param tilt_vector: tilt_vector = np.exp(self.tilt_amount * np.arange(N)), N=2**log2, and
                tilt_amount * N < 20 recommended
        :param approximation: exact = perform frequency / severity convolution using FFTs. slognorm or
                sgamma apply shifted lognormal or shifted gamma approximations.
        :param sev_calc:   discrete = suitable for fft, continuous = for rv_histogram cts version
        :param discretization_calc: use survival, distribution or both (=max(cdf, sf)) which is most accurate calc
        :param force_severity: make severities even if using approximation, for plotting
        :param verbose: make partial plots and return details of all moments by limit profile or
                severity mixture component.
        :return:
        """
        axiter = None
        verbose_audit_df = None
        self._density_df = None
        if verbose:
            axiter = axiter_factory(None, (len(self.sevs) + 2), aspect=1.414)
            verbose_audit_df = pd.DataFrame(columns=[
             'n', 'limit', 'attachment', 'en', 'emp ex1', 'emp cv', 'sum p_i', 'wt', 'nans', 'max', 'wtmax',
             'min'])
            verbose_audit_df = verbose_audit_df.set_index('n')
        r = 0
        self.xs = xs
        self.bs = xs[1]
        self.log2 = int(np.log(len(xs)) / np.log(2))
        if approximation == 'exact' or force_severity:
            wts = self.statistics_df.freq_1 / self.statistics_df.freq_1.sum()
            self.sev_density = np.zeros_like(xs)
            beds = self.discretize(sev_calc, discretization_calc)
            for temp, w, a, l, n in zip(beds, wts, self.attachment, self.limit, self.en):
                self.sev_density += temp * w
                if verbose:
                    _m, _cv = xsden_to_meancv(xs, temp)
                    verbose_audit_df.loc[r, :] = [l, a, n, _m, _cv,
                     temp.sum(),
                     w, np.sum(np.where(np.isinf(temp), 1, 0)),
                     temp.max(), w * temp.max(), temp.min()]
                    r += 1
                    next(axiter).plot(xs, temp, label='compt', lw=0.5, drawstyle='steps-post')
                    axiter.ax.plot(xs, (self.sev_density), label='run tot', lw=0.5, drawstyle='steps-post')
                    if np.all(self.limit < np.inf):
                        axiter.ax.set(xlim=(0, np.max(self.limit) * 1.1), title=f"{l:,.0f} xs {a:,.0f}, wt={w:.2f}")
                    else:
                        axiter.ax.set(title=f"{l:,.0f} xs {a:,.0f}, wt={w:.2f}")
                    axiter.ax.legend()

            if verbose:
                next(axiter).plot(xs, (self.sev_density), lw=0.5, drawstyle='steps-post')
                axiter.ax.set_title('Occurrence Density')
                aa = float(np.sum(verbose_audit_df.attachment * verbose_audit_df.wt))
                al = float(np.sum(verbose_audit_df.limit * verbose_audit_df.wt))
                if np.all(self.limit < np.inf):
                    axiter.ax.set_xlim(0, np.max(self.limit) * 1.05)
                else:
                    axiter.ax.set_xlim(0, xs[(-1)])
                _m, _cv = xsden_to_meancv(xs, self.sev_density)
                verbose_audit_df.loc[10001, :] = [
                 al, aa, self.n, _m, _cv,
                 self.sev_density.sum(),
                 np.sum(wts), np.sum(np.where(np.isinf(self.sev_density), 1, 0)),
                 self.sev_density.max(), np.nan, self.sev_density.min()]
        if force_severity:
            return
        if approximation == 'exact':
            if self.n > 100:
                logger.warning(f"Aggregate.update | warning, claim count {self.n} is high; consider an approximation ")
            if self.n == 0:
                self.agg_density = np.zeros_like(self.xs)
                self.agg_density[0] = 1
                self.ftagg_density = ft(self.agg_density, padding, tilt_vector)
            else:
                z = ft(self.sev_density, padding, tilt_vector)
                self.ftagg_density = self.mgf(self.n, z)
                self.agg_density = np.real(ift(self.ftagg_density, padding, tilt_vector))
        else:
            if self.agg_skew == 0:
                self.fzapprox = ss.norm(scale=(self.agg_m * self.agg_cv), loc=(self.agg_m))
            else:
                if approximation == 'slognorm':
                    shift, mu, sigma = sln_fit(self.agg_m, self.agg_cv, self.agg_skew)
                    self.fzapprox = ss.lognorm(sigma, scale=(np.exp(mu)), loc=shift)
                else:
                    if approximation == 'sgamma':
                        shift, alpha, theta = sgamma_fit(self.agg_m, self.agg_cv, self.agg_skew)
                        self.fzapprox = ss.gamma(alpha, scale=theta, loc=shift)
                    else:
                        raise ValueError(f"Invalid approximation {approximation} option passed to CAgg density. Allowable options are: exact | slogorm | sgamma")
            ps = self.fzapprox.pdf(xs)
            self.agg_density = ps / np.sum(ps)
            self.ftagg_density = ft(self.agg_density, padding, tilt_vector)
        cols = [
         'name', 'limit', 'attachment', 'el', 'freq_1', 'sev_1', 'agg_m', 'agg_cv', 'agg_skew']
        self.audit_df = pd.concat((self.statistics_df[cols],
         self.statistics_total_df.loc[(['mixed'], cols)]),
          axis=0)
        if self.sev_density is not None:
            _m, _cv = xsden_to_meancv(self.xs, self.sev_density)
        else:
            _m = np.nan
            _cv = np.nan
        self.audit_df.loc[('mixed', 'emp_sev_1')] = _m
        self.audit_df.loc[('mixed', 'emp_sev_cv')] = _cv
        _m, _cv = xsden_to_meancv(self.xs, self.agg_density)
        self.audit_df.loc[('mixed', 'emp_agg_1')] = _m
        self.audit_df.loc[('mixed', 'emp_agg_cv')] = _cv
        if verbose:
            ax = next(axiter)
            ax.plot(xs, self.agg_density, 'b')
            ax.set(xlim=(0, self.agg_m * (1 + 5 * self.agg_cv)), title='Aggregate Density')
            suptitle_and_tight(f"Severity Audit For: {self.name}")
            verbose_audit_df = pd.concat((verbose_audit_df[['limit', 'attachment', 'emp ex1', 'emp cv']],
             self.statistics_df[['freq_1', 'sev_1', 'sev_cv']]),
              sort=True,
              axis=1)
            verbose_audit_df.loc[(10001, 'freq_1')] = self.statistics_total_df.loc[('mixed',
                                                                                    'freq_1')]
            verbose_audit_df.loc[:, 'freq_cv'] = np.hstack((self.statistics_df.loc[:, 'freq_cv'],
             self.statistics_total_df.loc[('mixed', 'freq_cv')]))
            verbose_audit_df.loc[(10001, 'sev_1')] = self.statistics_total_df.loc[('mixed',
                                                                                   'sev_1')]
            verbose_audit_df.loc[(10001, 'sev_cv')] = self.statistics_total_df.loc[('mixed',
                                                                                    'sev_cv')]
            verbose_audit_df['abs sev err'] = verbose_audit_df.sev_1 - verbose_audit_df['emp ex1']
            verbose_audit_df['rel sev err'] = verbose_audit_df['abs sev err'] / verbose_audit_df['emp ex1']
        self.nearest_quantile_function = None
        self._cdf = None
        return verbose_audit_df

    def emp_stats(self):
        """
        report_ser on empirical statistics_df - useful when investigating dh transformations.

        :return:
        """
        ex = np.sum(self.xs * self.agg_density)
        ex2 = np.sum(self.xs ** 2 * self.agg_density)
        v = ex2 - ex * ex
        sd = np.sqrt(v)
        cv = sd / ex
        s1 = pd.Series([ex, sd, cv], index=['mean', 'sd', 'cv'])
        if self.dh_sev_density is not None:
            ex = np.sum(self.xs * self.dh_agg_density)
            ex2 = np.sum(self.xs ** 2 * self.dh_agg_density)
            v = ex2 - ex * ex
            sd = np.sqrt(v)
            cv = sd / ex
            s2 = pd.Series([ex, sd, cv], index=['mean', 'sd', 'cv'])
            df = pd.DataFrame({'numeric': s1, self.beta_name: s2})
        else:
            df = pd.DataFrame(s1, columns=['numeric'])
        df.loc[('mean', 'theory')] = self.statistics_total_df.loc[('Agg', 'agg1')]
        df.loc[('sd', 'theory')] = np.sqrt(self.statistics_total_df.loc[('Agg', 'agg2')] - self.statistics_total_df.loc[('Agg',
                                                                                                                         'agg1')] ** 2)
        df.loc[('cv', 'theory')] = self.statistics_total_df.loc[('Agg', 'agg_cv')]
        df['err'] = df['numeric'] / df['theory'] - 1
        return df

    def delbaen_haezendonck_density(self, xs, padding, tilt_vector, beta, beta_name=''):
        """
        Compare the base and Delbaen Haezendonck transformed aggregates

        * beta(x) = alpha + gamma(x)
        * alpha = log(freq' / freq): log of the increase in claim count
        * gamma = log(Radon Nikodym derv of adjusted severity) = log(tilde f / f)

        Adjustment guarantees a positive loading iff beta is an increasing function
        iff gamma is increasing iff tilde f / f is increasing.
        cf. eqn 3.7 and 3.8

        Note conditions that E(exp(beta(X)) and E(X exp(beta(X)) must both be finite (3.4, 3.5)
        form of beta function described in 2.23 via, 2.16-17 and 2.18

        From examples on last page of paper:

        ::

            beta(x) = a ==> adjust frequency by factor of e^a
            beta(x) = log(1 + b(x - E(X)))  ==> variance principle EN(EX + bVar(X))
            beta(x) = ax- logE_P(exp(a x))  ==> Esscher principle

        To make a 'multiple' of an existing distortion you can use a simple wrapper class like this:

        ::

            class dist_wrap(agg.Distortion):
                '''
                wrap a distortion to include higher or lower freq
                in DH α is actually exp(α)
                this will pass isinstance(g2, agg.Distortion)
                '''
                def __init__(self, α, dist):
                    def loc_g(s):
                        return α * dist.g(s)
                    self.g = loc_g
                    self.name = dist.name

        :param xs: is part of agg so can use that
        :param padding: = 1 (default)
        :param tilt_vector: None (default)
        :param beta: function R+ to R with appropriate properties or name of prob distortion function
        :param beta_name:
        :return:
        """
        if self.agg_density is None:
            self.update(xs, padding, tilt_vector, 'exact')
        else:
            if isinstance(beta, Distortion):
                beta_name = beta.name
                self.dh_sev_density = -np.diff(beta.g(1 - np.cumsum(np.hstack((0, self.sev_density)))))
                ex_beta = np.sum(self.dh_sev_density)
            else:
                self.dh_sev_density = self.sev_density * np.exp(beta.g(xs))
                ex_beta = np.sum(self.dh_sev_density)
            self.dh_sev_density = self.dh_sev_density / ex_beta
            adj_n = ex_beta * self.n
            if self.freq_name == 'poisson':
                ftagg_density = np.exp(adj_n * (ft(self.dh_sev_density, padding, tilt_vector) - 1))
                self.dh_agg_density = np.real(ift(ftagg_density, padding, tilt_vector))
            else:
                raise ValueError('Must use compound Poisson for DH density')
        self.beta_name = beta_name

    def plot(self, kind='quick', axiter=None, aspect=1, figsize=None):
        """
        plot computed density and aggregate

        **kind** option:

        * quick (default): Density for sev and agg on nominal and log scale; Lee diagram sev and agg
        * long: severity, log sev density, sev dist, agg with sev, agg on own, agg on log, S, Lee, return period

        :param kind: quick or long
        :param axiter: optional axiter object
        :param aspect: optional aspect ratio of individual plots
        :param figsize: optional overall figure size
        :return:
        """
        if self.agg_density is None:
            print('Cannot plot before update')
            return
        if self.sev_density is None:
            self.update((self.xs), 1, None, sev_calc='discrete', force_severity=True)
        set_tight = axiter is None
        if kind == 'long':
            axiter = axiter_factory(axiter, 10, aspect=aspect, figsize=figsize)
            max_lim = min(self.xs[(-1)], np.max(self.limit)) * 1.05
            if max_lim < 1:
                max_lim = 1
            else:
                next(axiter).plot(self.xs, self.sev_density)
                axiter.ax.set(title='Severity', xlim=(0, max_lim))
                next(axiter).plot(self.xs, self.sev_density)
                axiter.ax.set(title='Log Severity')
                if np.sum(self.sev_density == 1) >= 1:
                    axiter.ax.set(title='Severity Degenerate')
                    axiter.ax.set(xlim=(0, max_lim * 2))
                else:
                    axiter.ax.set(title='Log Severity')
                    axiter.ax.set(title='Log Severity', yscale='log')
                    axiter.ax.set(xlim=(0, max_lim))
                next(axiter).plot((self.xs), (self.sev_density.cumsum()), drawstyle='steps-post')
                axiter.ax.set(title='Severity Distribution')
                axiter.ax.set(xlim=(0, max_lim))
                next(axiter).plot((self.xs), (self.agg_density), label='aggregate_project')
                axiter.ax.plot((self.xs), (self.sev_density), lw=0.5, drawstyle='steps-post', label='severity')
                axiter.ax.set(title='Aggregate')
                axiter.ax.legend()
                next(axiter).plot((self.xs), (self.agg_density), label='aggregate_project')
                axiter.ax.set(title='Aggregate')
                next(axiter).plot((self.xs), (self.agg_density), label='aggregate_project')
                axiter.ax.set(yscale='log', title='Aggregate, log scale')
                F = self.agg_density.cumsum()
                next(axiter).plot(self.xs, 1 - F)
                axiter.ax.set(title='Survival Function')
                next(axiter).plot(self.xs, 1 - F)
                axiter.ax.set(title='Survival Function, log scale', yscale='log')
                next(axiter).plot((1 - F), (self.xs), label='aggregate_project')
                axiter.ax.plot((1 - self.sev_density.cumsum()), (self.xs), label='severity')
                axiter.ax.set(title='Lee Diagram')
                axiter.ax.legend()
                max_p = F[(-1)]
                if max_p > 0.9999:
                    _n = 10
                else:
                    _n = 5
            if max_p >= 1:
                max_p = 0.9999999999
            k = (max_p / 0.99) ** (1 / _n)
            extraps = 0.99 * k ** np.arange(_n)
            q = interpolate.interp1d(F, (self.xs), kind='linear', fill_value='extrapolate', bounds_error=False)
            ps = np.hstack((np.linspace(0, 1, 100, endpoint=False), extraps))
            qs = q(ps)
            next(axiter).plot(1 / (1 - ps), qs)
            axiter.ax.set(title='Return Period', xscale='log')
        else:
            if self.dh_agg_density is not None:
                n = 4
            else:
                n = 3
            axiter = axiter_factory(axiter, n, figsize, aspect=aspect)
            F = np.cumsum(self.agg_density)
            mx = np.argmax(F > 0.99999)
            if mx == 0:
                mx = len(F) + 1
            else:
                mx += 1
            dh_F = None
            if self.dh_agg_density is not None:
                dh_F = np.cumsum(self.dh_agg_density)
                mx = max(mx, np.argmax(dh_F > 0.99999))
                dh_F = dh_F[:mx]
            F = F[:mx]
            xs = self.xs[:mx]
            d = self.agg_density[:mx]
            sevF = np.cumsum(self.sev_density)
            sevF = sevF[:mx]
            f = self.sev_density[:mx]
            ax = next(axiter)
            ax.plot(xs, d, label='agg', drawstyle='steps-post')
            ax.plot(xs, f, label='sev', drawstyle='steps-post')
            if np.sum(f > 1e-06) < 20:
                ax.plot(xs, f, 'o', label=None)
            if self.dh_agg_density is not None:
                ax.plot(xs, (self.dh_agg_density[:mx]), label=('dh {:} agg'.format(self.beta_name)))
                ax.plot(xs, (self.dh_sev_density[:mx]), label=('dh {:} sev'.format(self.beta_name)))
            max_y = min(2 * np.max(d), np.max(f[1:])) * 1.05
            if max_y > 0:
                ax.set_ylim(0, max_y)
            ax.legend()
            ax.set_title('Density')
            ax = next(axiter)
            ax.plot(xs, d, label='agg')
            ax.plot(xs, f, label='sev')
            if self.dh_agg_density is not None:
                ax.plot(xs, (self.dh_agg_density[:mx]), label=('dh {:} agg'.format(self.beta_name)))
                ax.plot(xs, (self.dh_sev_density[:mx]), label=('dh {:} sev'.format(self.beta_name)))
            ax.set_yscale('log')
            ax.legend()
            ax.set_title('Log Density')
            ax = next(axiter)
            ax.plot(F, xs, label='Agg')
            ax.plot(sevF, xs, label='Sev')
            if self.dh_agg_density is not None:
                dh_F = np.cumsum(self.dh_agg_density[:mx])
                ax.plot(dh_F, xs, label=('dh {:} agg'.format(self.beta_name)))
            ax.legend()
            ax.set_title('Lee Diagram')
            if self.dh_agg_density is not None:
                ax = next(axiter)
                ax.plot((1 - F), (1 - dh_F), label='g(S) vs S')
                ax.plot((1 - F), (1 - F), 'k', linewidth=0.5, label=None)
            if set_tight:
                axiter.tidy()
                suptitle_and_tight(f"Aggregate {self.name}")

    def report(self, report_list='quick'):
        """
        statistics, quick or audit reports

        :param report_list:
        :return:
        """
        full_report_list = [
         'statistics', 'quick', 'audit']
        if report_list == 'all':
            report_list = full_report_list
        if 'quick' in report_list:
            html_title(f"{self.name} Quick Report (Theoretic)", 1)
            display(pd.DataFrame(self.report_ser).unstack())
        if 'audit' in report_list:
            if self.audit_df is not None:
                html_title(f"{self.name} Audit Report", 1)
                display(self.audit_df)
        if 'statistics' in report_list:
            if len(self.statistics_df) > 1:
                df = pd.concat((self.statistics_df, self.statistics_total_df), axis=1)
            else:
                df = self.statistics_df
            html_title(f"{self.name} Statistics Report", 1)
            display(df)

    def recommend_bucket(self, log2=10, verbose=False):
        """
        recommend a bucket size given 2**N buckets

        :param log2: log2 of number of buckets. log2=10 is default.
        :return:
        """
        N = 1 << log2
        if not verbose:
            moment_est = estimate_agg_percentile(self.agg_m, self.agg_cv, self.agg_skew) / N
            limit_est = self.limit.max() / N
            if limit_est == np.inf:
                limit_est = 0
            logger.info(f"Agg.recommend_bucket | {self.name} moment: {moment_est}, limit {limit_est}")
            return max(moment_est, limit_est)
        for n in sorted({log2, 16, 13, 10}):
            rb = self.recommend_bucket(n)
            if n == log2:
                rbr = rb
            print(f"Recommended bucket size with {2 ** n} buckets: {rb:,.0f}")

        if self.bs != 0:
            print(f"Bucket size set with {N} buckets at {self.bs:,.0f}")
        return rbr

    def q_old(self, p):
        """
        return lowest quantile, appropriate for discrete bucketing.
        quantile guaranteed to be in the index
        nearest does not work because you always want to pick rounding up

        Definition 2.1 (Quantiles)
        x(α) = qα(X) = inf{x ∈ R : P[X ≤ x] ≥ α} is the lower α-quantile of X
        x(α) = qα(X) = inf{x ∈ R : P[X ≤ x] > α} is the upper α-quantile of X.

        We use the x-notation if the dependence on X is evident, otherwise the q-notion.
        Acerbi and Tasche (2002)

        :param p:
        :return:
        """
        if self._q is None:
            self._q = interpolate.interp1d((self.density_df.F), (self.density_df.loss), kind='linear')
        l = float(self._q(p))
        l1 = self.density_df.index.get_loc(l, 'bfill')
        l1 = self.density_df.index[l1]
        return l1

    def q(self, p, kind='lower'):
        """
        Exact same code from Portfolio.q

        kind==middle reproduces middle_q

        :param p:
        :param kind:
        :return:
        """
        if self._linear_quantile_function is None:
            self._linear_quantile_function = {}
            self.q_temp = self.density_df[['loss', 'F']].groupby('F').agg({'loss': np.min})
            self.q_temp.loc[(1, 'loss')] = self.q_temp.loss.iloc[(-1)]
            self.q_temp.loc[(0, 'loss')] = 0
            self.q_temp = self.q_temp.sort_index()
            self.q_temp['loss_s'] = self.q_temp.loss.shift(-1)
            self.q_temp.iloc[(-1, 1)] = self.q_temp.iloc[(-1, 0)]
            self._linear_quantile_function['upper'] = interpolate.interp1d((self.q_temp.index), (self.q_temp.loss_s), kind='previous', bounds_error=False, fill_value='extrapolate')
            self._linear_quantile_function['lower'] = interpolate.interp1d((self.q_temp.index), (self.q_temp.loss), kind='next', bounds_error=False, fill_value='extrapolate')
            self._linear_quantile_function['middle'] = interpolate.interp1d((self.q_temp.index), (self.q_temp.loss_s), kind='linear', bounds_error=False, fill_value='extrapolate')
        l = float(self._linear_quantile_function[kind](p))
        if not kind == 'middle':
            if not l in self.density_df.index:
                logger.error(f"Unexpected weirdness in {self.name} quantile...computed {p}th {kind} percentile as {l} which is not in the index but is expected to be.")
        return l

    def middle_q(self, p):
        """
        not as careful as careful q but much better than q
        vectorized
        does not return element of the index!

        :param p:
        :return:
        """
        logger.warning('middle_q has been deprecated...use q(p, kind="middle") instead ')
        if self._middle_q is None:
            temp = self.density_df.groupby('F')[['loss']].agg(np.min)
            temp.loc[(1.0, 'loss')] = temp.iloc[-1, :].loss
            temp.loc[(0.0, 'loss')] = 0.0
            temp = temp.sort_index()
            self._middle_q = interpolate.interp1d((temp.index), (temp.loss), kind='linear')
        return self._middle_q(p)

    def careful_q(self, p):
        """
        careful calculation of q handling jumps (based of SRM_Examples Noise class originally).
        Note this is automatically vectorized and returns and array whereas q isn't.
        It doesn't necessarily return a element of the index.

        Just for reference here is code to illustrate the problem. This code is used in Vig_0_Audit.ipynb.

            uw = agg.Underwriter(create_all=True)

            def plot_eg_agg(b, e, w, n=32, axs=None, x_range=1):
                '''
                makes a tricky distribution function with a poss isolated jump
                creates an agg object and checks the quantile function is correct

                mass at w

                '''

                if axs is None:
                    f, axs0 = plt.subplots(2,3, figsize=(9,6))
                    axs = iter(axs0.flatten())

                tm = np.linspace(0, 1, 33)
                tf = lambda x : f'{32*x:.0f}'

                def pretty(axis, ticks, formatter):
                    maj = ticks[::4]
                    mnr = [i for i in ticks if i not in maj]
                    labels = [formatter(i) for i in maj]
                    axis.set_ticks(maj)
                    axis.set_ticks(mnr, True)
                    axis.set_ticklabels(labels)
                    axis.grid(True, 'major', lw=0.707, c='lightblue')
                    axis.grid(True, 'minor', lw=0.35, c='lightblue')

                # make the distribution
                xs = np.linspace(0, x_range, n+1)
                Fx = np.zeros_like(xs)
                Fx[b:13] = 1
                Fx[20:e] = 1
                Fx[w] = 32 - np.sum(Fx)
                Fx = Fx / Fx.sum()
                Fx = np.cumsum(Fx)

                # make an agg version: find the jumps and create a dhistogram
                temp = pd.DataFrame(dict(x=xs, F=Fx))
                temp['f'] = np.diff(temp.F, prepend=0)
                temp = temp.query('f > 0')
                pgm = f'agg Tricky 1 claim sev dhistogram xps {temp.x.values} {temp.f.values} fixed'
                a = uw(pgm)
                a.easy_update(10, 0.001)
                # plot
                a.plot(axiter=axs)
                pretty(axs0[0,0].xaxis, tm, tf)
                pretty(axs0[0,2].xaxis, tm, tf)
                pretty(axs0[0,2].yaxis, tm, tf)

                # lower left plot: distribution function
                ax = next(axs)
                ax.step(xs, Fx, where='post', marker='.')
                ax.plot(a.xs, a.agg_density.cumsum(), linewidth=3, alpha=0.5, label='from agg')
                ax.set(title=f'b={b}, e={e}, w={w}', ylim=-0.05, aspect='equal')
                if x_range  == 1:
                    ax.set(aspect='equal')
                ax.legend(frameon=False, loc='upper left')
                pretty(ax.xaxis, tm, tf)
                pretty(ax.yaxis, tm, tf)

                # lower middle plot
                ps = np.linspace(0, 1, 301)
                agg_careful = a.careful_q(ps)
                ax = next(axs)
                ax.step(Fx, xs, where='pre', marker='.', label='input')
                ax.plot(Fx, xs, ':', label='input joined')
                ax.plot(ps, agg_careful, linewidth=1, label='agg careful')
                ax.set(title='Inverse', ylim=-0.05)
                if x_range  == 1:
                    ax.set(aspect='equal')
                pretty(ax.xaxis, tm, tf)
                pretty(ax.yaxis, tm, tf)
                ax.legend()

                # lower right plot
                ax = next(axs)
                dmq = np.zeros_like(ps)
                for i, p in enumerate(ps):
                    try:
                        dmq[i] = a.q(p)
                    except:
                        dmq[i] = 0
                ax.plot(ps, agg_careful, label='careful (agg obj)', linewidth=1, alpha=1)
                ax.plot(ps, dmq, label='agg version')
                ax.legend(frameon=False, loc='upper left')
                pretty(ax.xaxis, tm, tf)
                pretty(ax.yaxis, tm, tf)
                ax.set(title='Check with agg version')

                plt.tight_layout()

                return a

            aw = plot_eg_agg(6, 29, 16)

        :param p: single or vector of values of ps, 0<1
        :return:  quantiles
        """
        if self._careful_q is None:
            self._careful_q = CarefulInverse.dist_inv1d(self.xs, self.agg_density)
        return self._careful_q(p)

    def careful_tvar(self, p):
        """
        compute a very careful tvar...this may be very slow...
        TODO SORT OUT...this does not work well
        :param p:
        :return:
        """
        if isinstance(p, np.ndarray):
            ans = np.zeros_like(p)
            for j, pv in enumerate(p):
                i = quad(self.careful_q, pv, 1)
                ans[j] = i[0] / (1 - pv)

            return ans
        i = quad(self.careful_q, p, 1)
        return i[0] / (1 - p)

    def var(self, p):
        """
        value at risk = alias for quantile function

        :param p:
        :return:
        """
        return self.q(p)

    def tvar(self, p):
        """
        Compute the tail value at risk at threshold p

        Definition 2.6 (Tail mean and Expected Shortfall)
        Assume E[X−] < ∞. Then
        x¯(α) = TM_α(X) = α^{−1}E[X 1{X≤x(α)}] + x(α) (α − P[X ≤ x(α)])
        is α-tail mean at level α the of X.
        Acerbi and Tasche (2002)

        We are interested in the right hand exceedence [?? note > vs ≥]
        α^{−1}E[X 1{X > x(α)}] + x(α) (P[X ≤ x(α)] − α)

        McNeil etc. p66-70 - this follows from def of ES as an integral
        of the quantile function

        q is exact quantile (most of the time)
        q1 is the smallest index element (bucket multiple) greater than or equal to q

        tvar integral is int_p^1 q(s)ds = int_q^infty xf(x)dx = q + int_q^infty S(x)dx
        we use the last approach. np.trapz approxes the integral. And the missing piece
        between q and q1 approx as a trapezoid too.

        :param p:
        :return:
        """
        q = float(self.q(p, 'middle'))
        l1 = self.density_df.index.get_loc(q, 'bfill')
        q1 = self.density_df.index[l1]
        i1 = np.trapz((self.density_df.loc[q1:, 'S']), dx=(self.bs))
        i2 = (q1 - q) * (2 - p - self.density_df.at[(q1, 'F')]) / 2
        return q + (i1 + i2) / (1 - p)

    def cdf(self, x):
        """
        return cumulative probability distribution using linear interpolation

        :param x: loss size
        :return:
        """
        if self._cdf is None:
            self._cdf = interpolate.interp1d((self.xs), (self.agg_density.cumsum()), kind='linear', bounds_error=False,
              fill_value='extrapolate')
        return self._cdf(x)

    def sf(self, x):
        """
        return survival function using linear interpolation

        :param x: loss size
        :return:
        """
        return 1 - self.cdf(x)

    def pdf(self, x):
        """
        probability density function, assuming a continuous approximation of the bucketed density
        :param x:
        :return:
        """
        if self._pdf is None:
            self._pdf = interpolate.interp1d((self.xs), (self.agg_density), kind='linear', bounds_error=False,
              fill_value='extrapolate')
        return self._pdf(x) / self.bs

    def json(self):
        """
        write in json
        :return:
        """
        return json.dumps(self._spec)

    def agg_lang(self):
        """
        write in aggregate language...
        :return:
        """
        raise ValueError('agg_lang not yet implemented...')

    def entropy_fit(self, n_const, tol=1e-10, verbose=False):
        """
        Find  the max entropy fit to the aggregate based on n_moments fit
        n_moments must include 0 powers (so for two moments enter 3)

        Based on discussions with and R code from Jon Evans

        :param n_const: number of moments to match, including 0 for sum of probs
        :param tol:
        :param verbose:
        :return:
        """
        xs = self.xs.copy()
        p = self.agg_density.copy()
        p = np.where(abs(p) < 1e-16, 0, p)
        p = p / np.sum(p)
        p1 = p.copy()
        mtargets = np.zeros(n_const)
        for i in range(n_const):
            mtargets[i] = np.sum(p)
            p *= xs

        parm1 = np.zeros(n_const)
        x = np.array([xs ** i for i in range(n_const)])
        probs = np.exp(-x.T @ parm1)
        machieved = x @ probs
        der1 = -(x * probs) @ x.T
        er = 1
        iters = 0
        while er > tol:
            iters += 1
            try:
                parm1 = parm1 - inv(der1) @ (machieved - mtargets)
            except np.linalg.LinAlgError:
                print('Singluar matrix')
                print(der1)
                return
            else:
                probs = np.exp(-x.T @ parm1)
                machieved = x @ probs
                der1 = -(x * probs) @ x.T
                er = (machieved - mtargets).dot(machieved - mtargets)
                if verbose:
                    print(f"Error: {er}\nParameter {parm1}")

        ans = pd.DataFrame(dict(xs=xs, agg=p1, fit=probs))
        ans = ans.set_index('xs')
        return dict(params=parm1, machieved=machieved, mtargets=mtargets, ans_df=ans)


class Severity(ss.rv_continuous):
    __doc__ = '\n\n    A continuous random variable, subclasses ``scipy.statistics_df.rv_continuous``.\n\n    adds layer and attachment to scipy statistics_df continuous random variable class\n    overrides\n\n    * cdf\n    * pdf\n    * isf\n    * ppf\n    * moments\n\n    Should consider over-riding: sf, **statistics_df** ?munp\n\n    TODO issues remain using numerical integration to compute moments for distributions having\n    infinite support and a low standard deviation. See logger for more information in particular\n    cases.\n\n    '

    def __init__--- This code section failed: ---

 L.1977         0  LOAD_CONST               1
                2  LOAD_CONST               ('Portfolio',)
                4  IMPORT_NAME              port
                6  IMPORT_FROM              Portfolio
                8  STORE_FAST               'Portfolio'
               10  POP_TOP          

 L.1979        12  LOAD_GLOBAL              ss
               14  LOAD_ATTR                rv_continuous
               16  LOAD_ATTR                __init__
               18  LOAD_FAST                'self'
               20  LOAD_FAST                'sev_name'
               22  FORMAT_VALUE          0  ''
               24  LOAD_STR                 '['
               26  LOAD_FAST                'exp_limit'
               28  FORMAT_VALUE          0  ''
               30  LOAD_STR                 ' xs '
               32  LOAD_FAST                'exp_attachment'
               34  LOAD_STR                 ',.0f'
               36  FORMAT_VALUE_ATTR     4  ''
               38  LOAD_STR                 ']'
               40  BUILD_STRING_6        6 
               42  LOAD_CONST               ('name',)
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  POP_TOP          

 L.1982        48  LOAD_FAST                'exp_limit'
               50  LOAD_FAST                'self'
               52  STORE_ATTR               limit

 L.1983        54  LOAD_FAST                'exp_attachment'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               attachment

 L.1984        60  LOAD_FAST                'exp_limit'
               62  LOAD_FAST                'exp_attachment'
               64  BINARY_ADD       
               66  LOAD_FAST                'self'
               68  STORE_ATTR               detachment

 L.1985        70  LOAD_CONST               None
               72  LOAD_FAST                'self'
               74  STORE_ATTR               fz

 L.1986        76  LOAD_CONST               0
               78  LOAD_FAST                'self'
               80  STORE_ATTR               pattach

 L.1987        82  LOAD_CONST               0
               84  LOAD_FAST                'self'
               86  STORE_ATTR               pdetach

 L.1988        88  LOAD_FAST                'conditional'
               90  LOAD_FAST                'self'
               92  STORE_ATTR               conditional

 L.1989        94  LOAD_FAST                'sev_name'
               96  LOAD_FAST                'self'
               98  STORE_ATTR               sev_name

 L.1990       100  LOAD_FAST                'name'
              102  LOAD_FAST                'self'
              104  STORE_ATTR               name

 L.1991       106  LOAD_FAST                'sev_name'
              108  FORMAT_VALUE          0  ''
              110  LOAD_STR                 '['
              112  LOAD_FAST                'exp_limit'
              114  FORMAT_VALUE          0  ''
              116  LOAD_STR                 ' xs '
              118  LOAD_FAST                'exp_attachment'
              120  LOAD_STR                 ',.0f'
              122  FORMAT_VALUE_ATTR     4  ''
              124  BUILD_STRING_5        5 
              126  LOAD_FAST                'self'
              128  STORE_ATTR               long_name

 L.1992       130  LOAD_FAST                'note'
              132  LOAD_FAST                'self'
              134  STORE_ATTR               note

 L.1993       136  LOAD_CONST               None
              138  DUP_TOP          
              140  LOAD_FAST                'self'
              142  STORE_ATTR               sev1
              144  DUP_TOP          
              146  LOAD_FAST                'self'
              148  STORE_ATTR               sev2
              150  LOAD_FAST                'self'
              152  STORE_ATTR               sev3

 L.1994       154  LOAD_GLOBAL              logger
              156  LOAD_METHOD              info

 L.1995       158  LOAD_STR                 'Severity.__init__  | creating new Severity '
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                sev_name
              164  FORMAT_VALUE          0  ''
              166  LOAD_STR                 ' at '
              168  LOAD_GLOBAL              super
              170  LOAD_GLOBAL              Severity
              172  LOAD_FAST                'self'
              174  CALL_FUNCTION_2       2  '2 positional arguments'
              176  LOAD_METHOD              __repr__
              178  CALL_METHOD_0         0  '0 positional arguments'
              180  FORMAT_VALUE          0  ''
              182  BUILD_STRING_4        4 
              184  CALL_METHOD_1         1  '1 positional argument'
              186  POP_TOP          

 L.1998       188  LOAD_FAST                'sev_xs'
              190  LOAD_CONST               None
              192  COMPARE_OP               is-not
          194_196  POP_JUMP_IF_FALSE   768  'to 768'

 L.1999       198  LOAD_FAST                'sev_name'
              200  LOAD_STR                 'fixed'
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   220  'to 220'

 L.2001       206  LOAD_STR                 'dhistogram'
              208  STORE_FAST               'sev_name'

 L.2002       210  LOAD_GLOBAL              np
              212  LOAD_METHOD              array
              214  LOAD_CONST               1
              216  CALL_METHOD_1         1  '1 positional argument'
              218  STORE_FAST               'sev_ps'
            220_0  COME_FROM           204  '204'

 L.2003       220  LOAD_FAST                'sev_name'
              222  LOAD_CONST               1
              224  LOAD_CONST               None
              226  BUILD_SLICE_2         2 
              228  BINARY_SUBSCR    
              230  LOAD_STR                 'histogram'
              232  COMPARE_OP               ==
              234  POP_JUMP_IF_TRUE    240  'to 240'
              236  LOAD_ASSERT              AssertionError
              238  RAISE_VARARGS_1       1  'exception instance'
            240_0  COME_FROM           234  '234'

 L.2005       240  SETUP_EXCEPT        274  'to 274'

 L.2006       242  LOAD_GLOBAL              np
              244  LOAD_METHOD              broadcast_arrays
              246  LOAD_GLOBAL              np
              248  LOAD_METHOD              array
              250  LOAD_FAST                'sev_xs'
              252  CALL_METHOD_1         1  '1 positional argument'
              254  LOAD_GLOBAL              np
              256  LOAD_METHOD              array
              258  LOAD_FAST                'sev_ps'
              260  CALL_METHOD_1         1  '1 positional argument'
              262  CALL_METHOD_2         2  '2 positional arguments'
              264  UNPACK_SEQUENCE_2     2 
              266  STORE_FAST               'xs'
              268  STORE_FAST               'ps'
              270  POP_BLOCK        
              272  JUMP_FORWARD        334  'to 334'
            274_0  COME_FROM_EXCEPT    240  '240'

 L.2007       274  DUP_TOP          
              276  LOAD_GLOBAL              ValueError
              278  COMPARE_OP               exception-match
          280_282  POP_JUMP_IF_FALSE   332  'to 332'
              284  POP_TOP          
              286  POP_TOP          
              288  POP_TOP          

 L.2009       290  LOAD_GLOBAL              logger
              292  LOAD_METHOD              warning
              294  LOAD_STR                 'Severity.init | '
              296  LOAD_FAST                'sev_name'
              298  FORMAT_VALUE          0  ''
              300  LOAD_STR                 ' sev_xs and sev_ps cannot be broadcast'
              302  BUILD_STRING_3        3 
              304  CALL_METHOD_1         1  '1 positional argument'
              306  POP_TOP          

 L.2010       308  LOAD_GLOBAL              np
              310  LOAD_METHOD              array
              312  LOAD_FAST                'sev_xs'
              314  CALL_METHOD_1         1  '1 positional argument'
              316  STORE_FAST               'xs'

 L.2011       318  LOAD_GLOBAL              np
              320  LOAD_METHOD              array
              322  LOAD_FAST                'sev_ps'
              324  CALL_METHOD_1         1  '1 positional argument'
              326  STORE_FAST               'ps'
              328  POP_EXCEPT       
              330  JUMP_FORWARD        334  'to 334'
            332_0  COME_FROM           280  '280'
              332  END_FINALLY      
            334_0  COME_FROM           330  '330'
            334_1  COME_FROM           272  '272'

 L.2012       334  LOAD_GLOBAL              np
              336  LOAD_METHOD              isclose
              338  LOAD_GLOBAL              np
              340  LOAD_METHOD              sum
              342  LOAD_FAST                'ps'
              344  CALL_METHOD_1         1  '1 positional argument'
              346  LOAD_CONST               1.0
              348  CALL_METHOD_2         2  '2 positional arguments'
          350_352  POP_JUMP_IF_TRUE    382  'to 382'

 L.2013       354  LOAD_GLOBAL              logger
              356  LOAD_METHOD              error
              358  LOAD_STR                 'Severity.init | '
              360  LOAD_FAST                'sev_name'
              362  FORMAT_VALUE          0  ''
              364  LOAD_STR                 ' histogram/fixed severity with probs do not sum to 1, '
              366  LOAD_GLOBAL              np
              368  LOAD_METHOD              sum
              370  LOAD_FAST                'ps'
              372  CALL_METHOD_1         1  '1 positional argument'
              374  FORMAT_VALUE          0  ''
              376  BUILD_STRING_4        4 
              378  CALL_METHOD_1         1  '1 positional argument'
              380  POP_TOP          
            382_0  COME_FROM           350  '350'

 L.2016       382  LOAD_GLOBAL              min
              384  LOAD_GLOBAL              np
              386  LOAD_METHOD              min
              388  LOAD_FAST                'exp_limit'
              390  CALL_METHOD_1         1  '1 positional argument'
              392  LOAD_FAST                'xs'
              394  LOAD_METHOD              max
              396  CALL_METHOD_0         0  '0 positional arguments'
              398  CALL_FUNCTION_2       2  '2 positional arguments'
              400  STORE_FAST               'exp_limit'

 L.2017       402  LOAD_FAST                'sev_name'
              404  LOAD_STR                 'chistogram'
              406  COMPARE_OP               ==
          408_410  POP_JUMP_IF_FALSE   604  'to 604'

 L.2023       412  LOAD_GLOBAL              len
              414  LOAD_FAST                'xs'
              416  CALL_FUNCTION_1       1  '1 positional argument'
              418  LOAD_GLOBAL              len
              420  LOAD_FAST                'ps'
              422  CALL_FUNCTION_1       1  '1 positional argument'
              424  COMPARE_OP               ==
          426_428  POP_JUMP_IF_FALSE   464  'to 464'

 L.2024       430  LOAD_GLOBAL              np
              432  LOAD_METHOD              sort
              434  LOAD_GLOBAL              np
              436  LOAD_METHOD              hstack
              438  LOAD_FAST                'xs'
              440  LOAD_FAST                'xs'
              442  LOAD_CONST               -1
              444  BINARY_SUBSCR    
              446  LOAD_FAST                'xs'
              448  LOAD_CONST               -2
              450  BINARY_SUBSCR    
              452  BINARY_ADD       
              454  BUILD_TUPLE_2         2 
              456  CALL_METHOD_1         1  '1 positional argument'
              458  CALL_METHOD_1         1  '1 positional argument'
              460  STORE_FAST               'xss'
              462  JUMP_FORWARD        468  'to 468'
            464_0  COME_FROM           426  '426'

 L.2027       464  LOAD_FAST                'xs'
              466  STORE_FAST               'xss'
            468_0  COME_FROM           462  '462'

 L.2028       468  LOAD_FAST                'ps'
              470  LOAD_GLOBAL              np
              472  LOAD_METHOD              diff
              474  LOAD_FAST                'xss'
              476  CALL_METHOD_1         1  '1 positional argument'
              478  BINARY_TRUE_DIVIDE
              480  STORE_FAST               'aps'

 L.2030       482  LOAD_GLOBAL              min
              484  LOAD_GLOBAL              np
              486  LOAD_METHOD              min
              488  LOAD_FAST                'exp_limit'
              490  CALL_METHOD_1         1  '1 positional argument'
              492  LOAD_FAST                'xss'
              494  LOAD_METHOD              max
              496  CALL_METHOD_0         0  '0 positional arguments'
              498  CALL_FUNCTION_2       2  '2 positional arguments'
              500  STORE_FAST               'exp_limit'

 L.2032       502  LOAD_FAST                'xss'
              504  LOAD_CONST               None
              506  LOAD_CONST               -1
              508  BUILD_SLICE_2         2 
              510  BINARY_SUBSCR    
              512  LOAD_FAST                'xss'
              514  LOAD_CONST               1
              516  LOAD_CONST               None
              518  BUILD_SLICE_2         2 
              520  BINARY_SUBSCR    
              522  BINARY_ADD       
              524  LOAD_CONST               2
              526  BINARY_TRUE_DIVIDE
              528  STORE_FAST               'xsm'

 L.2033       530  LOAD_GLOBAL              np
              532  LOAD_METHOD              sum
              534  LOAD_FAST                'xsm'
              536  LOAD_FAST                'ps'
              538  BINARY_MULTIPLY  
              540  CALL_METHOD_1         1  '1 positional argument'
              542  LOAD_FAST                'self'
              544  STORE_ATTR               sev1

 L.2034       546  LOAD_GLOBAL              np
              548  LOAD_METHOD              sum
              550  LOAD_FAST                'xsm'
              552  LOAD_CONST               2
              554  BINARY_POWER     
              556  LOAD_FAST                'ps'
              558  BINARY_MULTIPLY  
              560  CALL_METHOD_1         1  '1 positional argument'
              562  LOAD_FAST                'self'
              564  STORE_ATTR               sev2

 L.2035       566  LOAD_GLOBAL              np
              568  LOAD_METHOD              sum
              570  LOAD_FAST                'xsm'
              572  LOAD_CONST               3
              574  BINARY_POWER     
              576  LOAD_FAST                'ps'
              578  BINARY_MULTIPLY  
              580  CALL_METHOD_1         1  '1 positional argument'
              582  LOAD_FAST                'self'
              584  STORE_ATTR               sev3

 L.2036       586  LOAD_GLOBAL              ss
              588  LOAD_METHOD              rv_histogram
              590  LOAD_FAST                'aps'
              592  LOAD_FAST                'xss'
              594  BUILD_TUPLE_2         2 
              596  CALL_METHOD_1         1  '1 positional argument'
              598  LOAD_FAST                'self'
              600  STORE_ATTR               fz
              602  JUMP_FORWARD       1524  'to 1524'
            604_0  COME_FROM           408  '408'

 L.2037       604  LOAD_FAST                'sev_name'
              606  LOAD_STR                 'dhistogram'
              608  COMPARE_OP               ==
          610_612  POP_JUMP_IF_FALSE   750  'to 750'

 L.2039       614  LOAD_GLOBAL              np
              616  LOAD_METHOD              sum
              618  LOAD_FAST                'xs'
              620  LOAD_FAST                'ps'
              622  BINARY_MULTIPLY  
              624  CALL_METHOD_1         1  '1 positional argument'
              626  LOAD_FAST                'self'
              628  STORE_ATTR               sev1

 L.2040       630  LOAD_GLOBAL              np
              632  LOAD_METHOD              sum
              634  LOAD_FAST                'xs'
              636  LOAD_CONST               2
              638  BINARY_POWER     
              640  LOAD_FAST                'ps'
              642  BINARY_MULTIPLY  
              644  CALL_METHOD_1         1  '1 positional argument'
              646  LOAD_FAST                'self'
              648  STORE_ATTR               sev2

 L.2041       650  LOAD_GLOBAL              np
              652  LOAD_METHOD              sum
              654  LOAD_FAST                'xs'
              656  LOAD_CONST               3
              658  BINARY_POWER     
              660  LOAD_FAST                'ps'
              662  BINARY_MULTIPLY  
              664  CALL_METHOD_1         1  '1 positional argument'
              666  LOAD_FAST                'self'
              668  STORE_ATTR               sev3

 L.2042       670  LOAD_GLOBAL              np
              672  LOAD_METHOD              sort
              674  LOAD_GLOBAL              np
              676  LOAD_METHOD              hstack
              678  LOAD_FAST                'xs'
              680  LOAD_CONST               1e-05
              682  BINARY_SUBTRACT  
              684  LOAD_FAST                'xs'
              686  BUILD_TUPLE_2         2 
              688  CALL_METHOD_1         1  '1 positional argument'
              690  CALL_METHOD_1         1  '1 positional argument'
              692  STORE_FAST               'xss'

 L.2043       694  LOAD_GLOBAL              np
              696  LOAD_METHOD              vstack
              698  LOAD_FAST                'ps'
              700  LOAD_GLOBAL              np
              702  LOAD_METHOD              zeros_like
              704  LOAD_FAST                'ps'
              706  CALL_METHOD_1         1  '1 positional argument'
              708  BUILD_TUPLE_2         2 
              710  CALL_METHOD_1         1  '1 positional argument'
              712  LOAD_ATTR                reshape
              714  LOAD_CONST               (-1,)
              716  LOAD_STR                 'F'
              718  LOAD_CONST               ('order',)
              720  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              722  LOAD_CONST               None
              724  LOAD_CONST               -1
              726  BUILD_SLICE_2         2 
              728  BINARY_SUBSCR    
              730  STORE_FAST               'pss'

 L.2044       732  LOAD_GLOBAL              ss
              734  LOAD_METHOD              rv_histogram
              736  LOAD_FAST                'pss'
              738  LOAD_FAST                'xss'
              740  BUILD_TUPLE_2         2 
              742  CALL_METHOD_1         1  '1 positional argument'
              744  LOAD_FAST                'self'
              746  STORE_ATTR               fz
              748  JUMP_FORWARD       1524  'to 1524'
            750_0  COME_FROM           610  '610'

 L.2046       750  LOAD_GLOBAL              ValueError
              752  LOAD_STR                 'Histogram must be chistogram (continuous) or dhistogram (discrete), you passed '
              754  LOAD_FAST                'sev_name'
              756  FORMAT_VALUE          0  ''
              758  BUILD_STRING_2        2 
              760  CALL_FUNCTION_1       1  '1 positional argument'
              762  RAISE_VARARGS_1       1  'exception instance'
          764_766  JUMP_FORWARD       1524  'to 1524'
            768_0  COME_FROM           194  '194'

 L.2049       768  LOAD_GLOBAL              isinstance
              770  LOAD_FAST                'sev_name'
              772  LOAD_GLOBAL              Severity
              774  CALL_FUNCTION_2       2  '2 positional arguments'
          776_778  POP_JUMP_IF_FALSE   790  'to 790'

 L.2050       780  LOAD_FAST                'sev_name'
              782  LOAD_FAST                'self'
              784  STORE_ATTR               fz
          786_788  JUMP_FORWARD       1524  'to 1524'
            790_0  COME_FROM           776  '776'

 L.2052       790  LOAD_GLOBAL              isinstance
              792  LOAD_FAST                'sev_name'
              794  LOAD_GLOBAL              str
              796  LOAD_GLOBAL              np
              798  LOAD_ATTR                str_
              800  BUILD_TUPLE_2         2 
              802  CALL_FUNCTION_2       2  '2 positional arguments'
          804_806  POP_JUMP_IF_TRUE   1174  'to 1174'

 L.2054       808  LOAD_FAST                'sev_a'
              810  STORE_FAST               'log2'

 L.2055       812  LOAD_FAST                'sev_b'
              814  STORE_FAST               'bs'

 L.2056       816  LOAD_GLOBAL              isinstance
              818  LOAD_FAST                'sev_name'
              820  LOAD_GLOBAL              Aggregate
              822  CALL_FUNCTION_2       2  '2 positional arguments'
          824_826  POP_JUMP_IF_FALSE   894  'to 894'

 L.2057       828  LOAD_FAST                'log2'
          830_832  POP_JUMP_IF_FALSE   880  'to 880'
              834  LOAD_FAST                'log2'
              836  LOAD_FAST                'sev_name'
              838  LOAD_ATTR                log2
              840  COMPARE_OP               !=
          842_844  POP_JUMP_IF_TRUE    868  'to 868'
              846  LOAD_FAST                'bs'
              848  LOAD_FAST                'sev_name'
              850  LOAD_ATTR                bs
              852  COMPARE_OP               !=
          854_856  POP_JUMP_IF_FALSE   880  'to 880'
              858  LOAD_FAST                'bs'
              860  LOAD_CONST               0
              862  COMPARE_OP               !=
          864_866  POP_JUMP_IF_FALSE   880  'to 880'
            868_0  COME_FROM           842  '842'

 L.2059       868  LOAD_FAST                'sev_name'
              870  LOAD_METHOD              easy_update
              872  LOAD_FAST                'log2'
              874  LOAD_FAST                'bs'
              876  CALL_METHOD_2         2  '2 positional arguments'
              878  POP_TOP          
            880_0  COME_FROM           864  '864'
            880_1  COME_FROM           854  '854'
            880_2  COME_FROM           830  '830'

 L.2060       880  LOAD_FAST                'sev_name'
              882  LOAD_ATTR                xs
              884  STORE_FAST               'xs'

 L.2061       886  LOAD_FAST                'sev_name'
              888  LOAD_ATTR                agg_density
              890  STORE_FAST               'ps'
              892  JUMP_FORWARD       1010  'to 1010'
            894_0  COME_FROM           824  '824'

 L.2062       894  LOAD_GLOBAL              isinstance
              896  LOAD_FAST                'sev_name'
              898  LOAD_FAST                'Portfolio'
              900  CALL_FUNCTION_2       2  '2 positional arguments'
          902_904  POP_JUMP_IF_FALSE   984  'to 984'

 L.2063       906  LOAD_FAST                'log2'
          908_910  POP_JUMP_IF_FALSE   962  'to 962'
              912  LOAD_FAST                'log2'
              914  LOAD_FAST                'sev_name'
              916  LOAD_ATTR                log2
              918  COMPARE_OP               !=
          920_922  POP_JUMP_IF_TRUE    946  'to 946'
              924  LOAD_FAST                'bs'
              926  LOAD_FAST                'sev_name'
              928  LOAD_ATTR                bs
              930  COMPARE_OP               !=
          932_934  POP_JUMP_IF_FALSE   962  'to 962'
              936  LOAD_FAST                'bs'
              938  LOAD_CONST               0
              940  COMPARE_OP               !=
          942_944  POP_JUMP_IF_FALSE   962  'to 962'
            946_0  COME_FROM           920  '920'

 L.2065       946  LOAD_FAST                'sev_name'
              948  LOAD_ATTR                update
              950  LOAD_FAST                'log2'
              952  LOAD_FAST                'bs'
              954  LOAD_CONST               False
              956  LOAD_CONST               ('add_exa',)
              958  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              960  POP_TOP          
            962_0  COME_FROM           942  '942'
            962_1  COME_FROM           932  '932'
            962_2  COME_FROM           908  '908'

 L.2066       962  LOAD_FAST                'sev_name'
              964  LOAD_ATTR                density_df
              966  LOAD_ATTR                loss
              968  LOAD_ATTR                values
              970  STORE_FAST               'xs'

 L.2067       972  LOAD_FAST                'sev_name'
              974  LOAD_ATTR                density_df
              976  LOAD_ATTR                p_total
              978  LOAD_ATTR                values
              980  STORE_FAST               'ps'
              982  JUMP_FORWARD       1010  'to 1010'
            984_0  COME_FROM           902  '902'

 L.2069       984  LOAD_GLOBAL              ValueError
              986  LOAD_STR                 'Object '
              988  LOAD_FAST                'sev_name'
              990  FORMAT_VALUE          0  ''
              992  LOAD_STR                 ' passed as a proto-severity type '
              994  LOAD_GLOBAL              type
              996  LOAD_GLOBAL              obj
              998  CALL_FUNCTION_1       1  '1 positional argument'
             1000  FORMAT_VALUE          0  ''
             1002  LOAD_STR                 ' only Aggregate, Portfolio and Severity objects allowed'
             1004  BUILD_STRING_5        5 
             1006  CALL_FUNCTION_1       1  '1 positional argument'
             1008  RAISE_VARARGS_1       1  'exception instance'
           1010_0  COME_FROM           982  '982'
           1010_1  COME_FROM           892  '892'

 L.2074      1010  LOAD_CONST               1e-07
             1012  STORE_FAST               'b1size'

 L.2075      1014  LOAD_GLOBAL              np
             1016  LOAD_METHOD              hstack
             1018  LOAD_FAST                'bs'
             1020  UNARY_NEGATIVE   
             1022  LOAD_FAST                'b1size'
             1024  BINARY_MULTIPLY  
             1026  LOAD_CONST               0
             1028  LOAD_FAST                'xs'
             1030  LOAD_CONST               1
             1032  LOAD_CONST               None
             1034  BUILD_SLICE_2         2 
             1036  BINARY_SUBSCR    
             1038  LOAD_FAST                'bs'
             1040  LOAD_CONST               2
             1042  BINARY_TRUE_DIVIDE
             1044  BINARY_SUBTRACT  
             1046  LOAD_FAST                'xs'
             1048  LOAD_CONST               -1
             1050  BINARY_SUBSCR    
             1052  LOAD_FAST                'bs'
             1054  LOAD_CONST               2
             1056  BINARY_TRUE_DIVIDE
             1058  BINARY_ADD       
             1060  BUILD_TUPLE_4         4 
             1062  CALL_METHOD_1         1  '1 positional argument'
             1064  STORE_FAST               'xss'

 L.2076      1066  LOAD_GLOBAL              np
             1068  LOAD_METHOD              hstack
             1070  LOAD_FAST                'ps'
             1072  LOAD_CONST               0
             1074  BINARY_SUBSCR    
             1076  LOAD_FAST                'b1size'
             1078  BINARY_TRUE_DIVIDE
             1080  LOAD_CONST               0
             1082  LOAD_FAST                'ps'
             1084  LOAD_CONST               1
             1086  LOAD_CONST               None
             1088  BUILD_SLICE_2         2 
             1090  BINARY_SUBSCR    
             1092  BUILD_TUPLE_3         3 
             1094  CALL_METHOD_1         1  '1 positional argument'
             1096  STORE_FAST               'pss'

 L.2077      1098  LOAD_GLOBAL              ss
             1100  LOAD_METHOD              rv_histogram
             1102  LOAD_FAST                'pss'
             1104  LOAD_FAST                'xss'
             1106  BUILD_TUPLE_2         2 
             1108  CALL_METHOD_1         1  '1 positional argument'
             1110  LOAD_FAST                'self'
             1112  STORE_ATTR               fz

 L.2078      1114  LOAD_GLOBAL              np
             1116  LOAD_METHOD              sum
             1118  LOAD_FAST                'xs'
             1120  LOAD_FAST                'ps'
             1122  BINARY_MULTIPLY  
             1124  CALL_METHOD_1         1  '1 positional argument'
             1126  LOAD_FAST                'self'
             1128  STORE_ATTR               sev1

 L.2079      1130  LOAD_GLOBAL              np
             1132  LOAD_METHOD              sum
             1134  LOAD_FAST                'xs'
             1136  LOAD_CONST               2
             1138  BINARY_POWER     
             1140  LOAD_FAST                'ps'
             1142  BINARY_MULTIPLY  
             1144  CALL_METHOD_1         1  '1 positional argument'
             1146  LOAD_FAST                'self'
             1148  STORE_ATTR               sev2

 L.2080      1150  LOAD_GLOBAL              np
             1152  LOAD_METHOD              sum
             1154  LOAD_FAST                'xs'
             1156  LOAD_CONST               3
             1158  BINARY_POWER     
             1160  LOAD_FAST                'ps'
             1162  BINARY_MULTIPLY  
             1164  CALL_METHOD_1         1  '1 positional argument'
             1166  LOAD_FAST                'self'
             1168  STORE_ATTR               sev3
         1170_1172  JUMP_FORWARD       1524  'to 1524'
           1174_0  COME_FROM           804  '804'

 L.2082      1174  LOAD_FAST                'sev_name'
             1176  LOAD_CONST               ('norm', 'expon', 'uniform')
             1178  COMPARE_OP               in
         1180_1182  POP_JUMP_IF_FALSE  1264  'to 1264'

 L.2085      1184  LOAD_FAST                'sev_loc'
             1186  LOAD_CONST               0
             1188  COMPARE_OP               ==
         1190_1192  POP_JUMP_IF_FALSE  1208  'to 1208'
             1194  LOAD_FAST                'sev_mean'
             1196  LOAD_CONST               0
             1198  COMPARE_OP               >
         1200_1202  POP_JUMP_IF_FALSE  1208  'to 1208'

 L.2086      1204  LOAD_FAST                'sev_mean'
             1206  STORE_FAST               'sev_loc'
           1208_0  COME_FROM          1200  '1200'
           1208_1  COME_FROM          1190  '1190'

 L.2087      1208  LOAD_FAST                'sev_scale'
             1210  LOAD_CONST               0
             1212  COMPARE_OP               ==
         1214_1216  POP_JUMP_IF_FALSE  1236  'to 1236'
             1218  LOAD_FAST                'sev_cv'
             1220  LOAD_CONST               0
             1222  COMPARE_OP               >
         1224_1226  POP_JUMP_IF_FALSE  1236  'to 1236'

 L.2088      1228  LOAD_FAST                'sev_cv'
             1230  LOAD_FAST                'sev_loc'
             1232  BINARY_MULTIPLY  
             1234  STORE_FAST               'sev_scale'
           1236_0  COME_FROM          1224  '1224'
           1236_1  COME_FROM          1214  '1214'

 L.2089      1236  LOAD_GLOBAL              getattr
             1238  LOAD_GLOBAL              ss
             1240  LOAD_FAST                'sev_name'
             1242  CALL_FUNCTION_2       2  '2 positional arguments'
             1244  STORE_FAST               'gen'

 L.2090      1246  LOAD_FAST                'gen'
             1248  LOAD_FAST                'sev_loc'
             1250  LOAD_FAST                'sev_scale'
             1252  LOAD_CONST               ('loc', 'scale')
             1254  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1256  LOAD_FAST                'self'
             1258  STORE_ATTR               fz
         1260_1262  JUMP_FORWARD       1524  'to 1524'
           1264_0  COME_FROM          1180  '1180'

 L.2092      1264  LOAD_FAST                'sev_name'
             1266  LOAD_CONST               ('beta',)
             1268  COMPARE_OP               in
         1270_1272  POP_JUMP_IF_FALSE  1432  'to 1432'

 L.2099      1274  LOAD_FAST                'sev_name'
             1276  LOAD_STR                 'beta'
             1278  COMPARE_OP               ==
         1280_1282  POP_JUMP_IF_FALSE  1402  'to 1402'
             1284  LOAD_FAST                'sev_mean'
             1286  LOAD_CONST               0
             1288  COMPARE_OP               >
         1290_1292  POP_JUMP_IF_FALSE  1402  'to 1402'
             1294  LOAD_FAST                'sev_cv'
             1296  LOAD_CONST               0
             1298  COMPARE_OP               >
         1300_1302  POP_JUMP_IF_FALSE  1402  'to 1402'

 L.2100      1304  LOAD_FAST                'sev_mean'
             1306  LOAD_FAST                'sev_scale'
             1308  BINARY_TRUE_DIVIDE
             1310  STORE_FAST               'm'

 L.2101      1312  LOAD_FAST                'm'
             1314  LOAD_FAST                'm'
             1316  BINARY_MULTIPLY  
             1318  LOAD_FAST                'sev_cv'
             1320  BINARY_MULTIPLY  
             1322  LOAD_FAST                'sev_cv'
             1324  BINARY_MULTIPLY  
             1326  STORE_FAST               'v'

 L.2102      1328  LOAD_FAST                'm'
             1330  LOAD_FAST                'm'
             1332  LOAD_CONST               1
             1334  LOAD_FAST                'm'
             1336  BINARY_SUBTRACT  
             1338  BINARY_MULTIPLY  
             1340  LOAD_FAST                'v'
             1342  BINARY_TRUE_DIVIDE
             1344  LOAD_CONST               1
             1346  BINARY_SUBTRACT  
             1348  BINARY_MULTIPLY  
             1350  STORE_FAST               'sev_a'

 L.2103      1352  LOAD_CONST               1
             1354  LOAD_FAST                'm'
             1356  BINARY_SUBTRACT  
             1358  LOAD_FAST                'm'
           1360_0  COME_FROM           602  '602'
             1360  LOAD_CONST               1
             1362  LOAD_FAST                'm'
             1364  BINARY_SUBTRACT  
             1366  BINARY_MULTIPLY  
             1368  LOAD_FAST                'v'
             1370  BINARY_TRUE_DIVIDE
             1372  LOAD_CONST               1
             1374  BINARY_SUBTRACT  
             1376  BINARY_MULTIPLY  
             1378  STORE_FAST               'sev_b'

 L.2104      1380  LOAD_GLOBAL              ss
             1382  LOAD_ATTR                beta
             1384  LOAD_FAST                'sev_a'
             1386  LOAD_FAST                'sev_b'
             1388  LOAD_CONST               0
             1390  LOAD_FAST                'sev_scale'
             1392  LOAD_CONST               ('loc', 'scale')
             1394  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1396  LOAD_FAST                'self'
             1398  STORE_ATTR               fx
             1400  JUMP_FORWARD       1430  'to 1430'
           1402_0  COME_FROM          1300  '1300'
           1402_1  COME_FROM          1290  '1290'
           1402_2  COME_FROM          1280  '1280'

 L.2106      1402  LOAD_GLOBAL              getattr
             1404  LOAD_GLOBAL              ss
             1406  LOAD_FAST                'sev_name'
             1408  CALL_FUNCTION_2       2  '2 positional arguments'
             1410  STORE_FAST               'gen'

 L.2107      1412  LOAD_FAST                'gen'
             1414  LOAD_FAST                'sev_a'
             1416  LOAD_FAST                'sev_b'
             1418  LOAD_FAST                'sev_loc'
             1420  LOAD_FAST                'sev_scale'
             1422  LOAD_CONST               ('loc', 'scale')
             1424  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1426  LOAD_FAST                'self'
             1428  STORE_ATTR               fz
           1430_0  COME_FROM          1400  '1400'
             1430  JUMP_FORWARD       1524  'to 1524'
           1432_0  COME_FROM          1270  '1270'

 L.2110      1432  LOAD_FAST                'sev_a'
             1434  LOAD_CONST               0
             1436  COMPARE_OP               ==
         1438_1440  POP_JUMP_IF_FALSE  1456  'to 1456'

 L.2111      1442  LOAD_FAST                'self'
             1444  LOAD_METHOD              cv_to_shape
             1446  LOAD_FAST                'sev_cv'
             1448  CALL_METHOD_1         1  '1 positional argument'
             1450  UNPACK_SEQUENCE_2     2 
             1452  STORE_FAST               'sev_a'
             1454  STORE_FAST               '_'
           1456_0  COME_FROM          1438  '1438'

 L.2112      1456  LOAD_FAST                'sev_scale'
             1458  LOAD_CONST               0
             1460  COMPARE_OP               ==
         1462_1464  POP_JUMP_IF_FALSE  1498  'to 1498'
             1466  LOAD_FAST                'sev_mean'
             1468  LOAD_CONST               0
             1470  COMPARE_OP               >
         1472_1474  POP_JUMP_IF_FALSE  1498  'to 1498'

 L.2113      1476  LOAD_FAST                'self'
             1478  LOAD_METHOD              mean_to_scale
             1480  LOAD_FAST                'sev_a'
             1482  LOAD_FAST                'sev_mean'
             1484  LOAD_FAST                'sev_loc'
             1486  CALL_METHOD_3         3  '3 positional arguments'
             1488  UNPACK_SEQUENCE_2     2 
             1490  STORE_FAST               'sev_scale'
             1492  LOAD_FAST                'self'
             1494  STORE_ATTR               fz
             1496  JUMP_FORWARD       1524  'to 1524'
           1498_0  COME_FROM          1472  '1472'
           1498_1  COME_FROM          1462  '1462'

 L.2115      1498  LOAD_GLOBAL              getattr
             1500  LOAD_GLOBAL              ss
             1502  LOAD_FAST                'sev_name'
             1504  CALL_FUNCTION_2       2  '2 positional arguments'
           1506_0  COME_FROM           748  '748'
             1506  STORE_FAST               'gen'

 L.2116      1508  LOAD_FAST                'gen'
             1510  LOAD_FAST                'sev_a'
             1512  LOAD_FAST                'sev_scale'
             1514  LOAD_FAST                'sev_loc'
             1516  LOAD_CONST               ('scale', 'loc')
             1518  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1520  LOAD_FAST                'self'
             1522  STORE_ATTR               fz
           1524_0  COME_FROM          1496  '1496'
           1524_1  COME_FROM          1430  '1430'
           1524_2  COME_FROM          1260  '1260'
           1524_3  COME_FROM          1170  '1170'
           1524_4  COME_FROM           786  '786'
           1524_5  COME_FROM           764  '764'

 L.2118      1524  LOAD_FAST                'self'
             1526  LOAD_ATTR                detachment
             1528  LOAD_GLOBAL              np
             1530  LOAD_ATTR                inf
             1532  COMPARE_OP               ==
         1534_1536  POP_JUMP_IF_FALSE  1546  'to 1546'

 L.2119      1538  LOAD_CONST               0
             1540  LOAD_FAST                'self'
             1542  STORE_ATTR               pdetach
             1544  JUMP_FORWARD       1562  'to 1562'
           1546_0  COME_FROM          1534  '1534'

 L.2121      1546  LOAD_FAST                'self'
             1548  LOAD_ATTR                fz
             1550  LOAD_METHOD              sf
             1552  LOAD_FAST                'self'
             1554  LOAD_ATTR                detachment
             1556  CALL_METHOD_1         1  '1 positional argument'
             1558  LOAD_FAST                'self'
             1560  STORE_ATTR               pdetach
           1562_0  COME_FROM          1544  '1544'

 L.2123      1562  LOAD_FAST                'self'
             1564  LOAD_ATTR                attachment
             1566  LOAD_CONST               0
             1568  COMPARE_OP               ==
         1570_1572  POP_JUMP_IF_FALSE  1582  'to 1582'

 L.2124      1574  LOAD_CONST               1
             1576  LOAD_FAST                'self'
             1578  STORE_ATTR               pattach
             1580  JUMP_FORWARD       1598  'to 1598'
           1582_0  COME_FROM          1570  '1570'

 L.2126      1582  LOAD_FAST                'self'
             1584  LOAD_ATTR                fz
             1586  LOAD_METHOD              sf
             1588  LOAD_FAST                'self'
             1590  LOAD_ATTR                attachment
             1592  CALL_METHOD_1         1  '1 positional argument'
             1594  LOAD_FAST                'self'
             1596  STORE_ATTR               pattach
           1598_0  COME_FROM          1580  '1580'

 L.2128      1598  LOAD_FAST                'sev_mean'
             1600  LOAD_CONST               0
             1602  COMPARE_OP               >
         1604_1606  POP_JUMP_IF_TRUE   1618  'to 1618'
             1608  LOAD_FAST                'sev_cv'
             1610  LOAD_CONST               0
             1612  COMPARE_OP               >
         1614_1616  POP_JUMP_IF_FALSE  1808  'to 1808'
           1618_0  COME_FROM          1604  '1604'

 L.2130      1618  LOAD_FAST                'self'
             1620  LOAD_ATTR                fz
             1622  LOAD_METHOD              stats
             1624  LOAD_STR                 'mv'
             1626  CALL_METHOD_1         1  '1 positional argument'
             1628  STORE_FAST               'st'

 L.2131      1630  LOAD_FAST                'st'
             1632  LOAD_CONST               0
             1634  BINARY_SUBSCR    
             1636  STORE_FAST               'm'

 L.2132      1638  LOAD_FAST                'st'
             1640  LOAD_CONST               1
             1642  BINARY_SUBSCR    
             1644  LOAD_CONST               0.5
             1646  BINARY_POWER     
             1648  LOAD_FAST                'm'
             1650  BINARY_TRUE_DIVIDE
             1652  STORE_FAST               'acv'

 L.2134      1654  LOAD_FAST                'sev_mean'
             1656  LOAD_CONST               0
             1658  COMPARE_OP               >
         1660_1662  POP_JUMP_IF_FALSE  1704  'to 1704'
             1664  LOAD_GLOBAL              np
             1666  LOAD_METHOD              isclose
             1668  LOAD_FAST                'sev_mean'
             1670  LOAD_FAST                'sev_loc'
             1672  BINARY_ADD       
             1674  LOAD_FAST                'm'
             1676  CALL_METHOD_2         2  '2 positional arguments'
         1678_1680  POP_JUMP_IF_TRUE   1704  'to 1704'

 L.2135      1682  LOAD_GLOBAL              print
             1684  LOAD_STR                 'WARNING target mean '
             1686  LOAD_FAST                'sev_mean'
             1688  FORMAT_VALUE          0  ''
             1690  LOAD_STR                 ' and achieved mean '
             1692  LOAD_FAST                'm'
             1694  FORMAT_VALUE          0  ''
             1696  LOAD_STR                 ' not close'
             1698  BUILD_STRING_5        5 
             1700  CALL_FUNCTION_1       1  '1 positional argument'
             1702  POP_TOP          
           1704_0  COME_FROM          1678  '1678'
           1704_1  COME_FROM          1660  '1660'

 L.2137      1704  LOAD_FAST                'sev_cv'
             1706  LOAD_CONST               0
             1708  COMPARE_OP               >
         1710_1712  POP_JUMP_IF_FALSE  1762  'to 1762'
             1714  LOAD_GLOBAL              np
             1716  LOAD_METHOD              isclose
             1718  LOAD_FAST                'sev_cv'
             1720  LOAD_FAST                'sev_mean'
             1722  BINARY_MULTIPLY  
             1724  LOAD_FAST                'sev_mean'
             1726  LOAD_FAST                'sev_loc'
             1728  BINARY_ADD       
             1730  BINARY_TRUE_DIVIDE
             1732  LOAD_FAST                'acv'
             1734  CALL_METHOD_2         2  '2 positional arguments'
         1736_1738  POP_JUMP_IF_TRUE   1762  'to 1762'

 L.2138      1740  LOAD_GLOBAL              print
             1742  LOAD_STR                 'WARNING target cv '
             1744  LOAD_FAST                'sev_cv'
             1746  FORMAT_VALUE          0  ''
             1748  LOAD_STR                 ' and achieved cv '
             1750  LOAD_FAST                'acv'
             1752  FORMAT_VALUE          0  ''
             1754  LOAD_STR                 ' not close'
             1756  BUILD_STRING_5        5 
             1758  CALL_FUNCTION_1       1  '1 positional argument'
             1760  POP_TOP          
           1762_0  COME_FROM          1736  '1736'
           1762_1  COME_FROM          1710  '1710'

 L.2141      1762  LOAD_GLOBAL              logger
             1764  LOAD_METHOD              info

 L.2142      1766  LOAD_STR                 'Severity.__init__ | parameters '
             1768  LOAD_FAST                'sev_a'
             1770  FORMAT_VALUE          0  ''
             1772  LOAD_STR                 ', '
             1774  LOAD_FAST                'sev_scale'
             1776  FORMAT_VALUE          0  ''
             1778  LOAD_STR                 ': target/actual '
             1780  LOAD_FAST                'sev_mean'
             1782  FORMAT_VALUE          0  ''
             1784  LOAD_STR                 ' vs '
             1786  LOAD_FAST                'm'
             1788  FORMAT_VALUE          0  ''
             1790  LOAD_STR                 ';  '
             1792  LOAD_FAST                'sev_cv'
             1794  FORMAT_VALUE          0  ''
             1796  LOAD_STR                 ' vs '
             1798  LOAD_FAST                'acv'
             1800  FORMAT_VALUE          0  ''
             1802  BUILD_STRING_12      12 
             1804  CALL_METHOD_1         1  '1 positional argument'
             1806  POP_TOP          
           1808_0  COME_FROM          1614  '1614'

 L.2145      1808  LOAD_FAST                'exp_limit'
             1810  LOAD_GLOBAL              np
             1812  LOAD_ATTR                inf
             1814  COMPARE_OP               <
         1816_1818  POP_JUMP_IF_TRUE   1830  'to 1830'
             1820  LOAD_FAST                'exp_attachment'
             1822  LOAD_CONST               0
             1824  COMPARE_OP               >
         1826_1828  POP_JUMP_IF_FALSE  1878  'to 1878'
           1830_0  COME_FROM          1816  '1816'

 L.2146      1830  LOAD_FAST                'exp_limit'
             1832  LOAD_GLOBAL              np
             1834  LOAD_ATTR                inf
             1836  COMPARE_OP               !=
         1838_1840  POP_JUMP_IF_FALSE  1854  'to 1854'
             1842  LOAD_STR                 '['
             1844  LOAD_FAST                'exp_limit'
             1846  LOAD_STR                 ',.0f'
             1848  FORMAT_VALUE_ATTR     4  ''
             1850  BUILD_STRING_2        2 
             1852  JUMP_FORWARD       1856  'to 1856'
           1854_0  COME_FROM          1838  '1838'
             1854  LOAD_STR                 'Unlimited'
           1856_0  COME_FROM          1852  '1852'
             1856  STORE_FAST               'layer_text'

 L.2147      1858  LOAD_FAST                'layer_text'
             1860  LOAD_STR                 ' xs '
             1862  LOAD_FAST                'exp_attachment'
             1864  LOAD_STR                 ',.0f'
             1866  FORMAT_VALUE_ATTR     4  ''
             1868  LOAD_STR                 ']'
             1870  BUILD_STRING_3        3 
             1872  INPLACE_ADD      
             1874  STORE_FAST               'layer_text'
             1876  JUMP_FORWARD       1882  'to 1882'
           1878_0  COME_FROM          1826  '1826'

 L.2149      1878  LOAD_STR                 ''
             1880  STORE_FAST               'layer_text'
           1882_0  COME_FROM          1876  '1876'

 L.2150      1882  SETUP_EXCEPT       1926  'to 1926'

 L.2151      1884  LOAD_FAST                'name'
             1886  FORMAT_VALUE          0  ''
             1888  LOAD_STR                 ': '
             1890  LOAD_FAST                'sev_name'
             1892  FORMAT_VALUE          0  ''
             1894  LOAD_STR                 '('
             1896  LOAD_FAST                'self'
             1898  LOAD_ATTR                fz
             1900  LOAD_ATTR                arg_dict
             1902  LOAD_CONST               0
             1904  BINARY_SUBSCR    
             1906  LOAD_STR                 '.2f'
             1908  FORMAT_VALUE_ATTR     4  ''
             1910  LOAD_STR                 ')'
             1912  LOAD_FAST                'layer_text'
             1914  FORMAT_VALUE          0  ''
             1916  BUILD_STRING_7        7 
             1918  LOAD_FAST                'self'
             1920  STORE_ATTR               long_name
             1922  POP_BLOCK        
             1924  JUMP_FORWARD       1958  'to 1958'
           1926_0  COME_FROM_EXCEPT   1882  '1882'

 L.2152      1926  POP_TOP          
             1928  POP_TOP          
             1930  POP_TOP          

 L.2154      1932  LOAD_FAST                'name'
             1934  FORMAT_VALUE          0  ''
             1936  LOAD_STR                 ': '
             1938  LOAD_FAST                'sev_name'
             1940  FORMAT_VALUE          0  ''
             1942  LOAD_FAST                'layer_text'
             1944  FORMAT_VALUE          0  ''
             1946  BUILD_STRING_4        4 
             1948  LOAD_FAST                'self'
             1950  STORE_ATTR               long_name
             1952  POP_EXCEPT       
             1954  JUMP_FORWARD       1958  'to 1958'
             1956  END_FINALLY      
           1958_0  COME_FROM          1954  '1954'
           1958_1  COME_FROM          1924  '1924'

 L.2156      1958  LOAD_FAST                'self'
             1960  LOAD_ATTR                fz
             1962  LOAD_CONST               None
             1964  COMPARE_OP               is-not
         1966_1968  POP_JUMP_IF_TRUE   1974  'to 1974'
             1970  LOAD_ASSERT              AssertionError
             1972  RAISE_VARARGS_1       1  'exception instance'
           1974_0  COME_FROM          1966  '1966'

Parse error at or near `COME_FROM' instruction at offset 1360_0

    def __repr__(self):
        return f"{super(Severity, self).__repr__()} of type {self.sev_name}"

    def cv_to_shape(self, cv, hint=1):
        """
        create a frozen object of type dist_name with given cv

        lognormal, gamma, inverse gamma and inverse gaussian solved analytically.

        Other distributions solved numerically and may be unstable.

        :param cv:
        :param hint:
        :return:
        """
        if self.sev_name == 'lognorm':
            shape = np.sqrt(np.log(cv * cv + 1))
            fz = ss.lognorm(shape)
            return (shape, fz)
        if self.sev_name == 'gamma':
            shape = 1 / (cv * cv)
            fz = ss.gamma(shape)
            return (shape, fz)
        if self.sev_name == 'invgamma':
            shape = 1 / cv ** 2 + 2
            fz = ss.invgamma(shape)
            return (shape, fz)
        if self.sev_name == 'invgauss':
            shape = cv ** 2
            fz = ss.invgauss(shape)
            return (shape, fz)
        gen = getattr(ss, self.sev_name)

        def f(shape):
            fz0 = gen(shape)
            temp = fz0.stats('mv')
            return cv - temp[1] ** 0.5 / temp[0]

        try:
            ans = newton(f, hint)
        except RuntimeError:
            logger.error(f"cv_to_shape | error for {self.sev_name}, {cv}")
            ans = np.inf
            return (ans, None)
        else:
            fz = gen(ans)
            return (ans, fz)

    def mean_to_scale(self, shape, mean, loc=0):
        """
        adjust scale of fz to have desired mean
        return frozen instance

        :param shape:
        :param mean:
        :param loc: location parameter (note: location is added to the mean...)
        :return:
        """
        gen = getattr(ss, self.sev_name)
        fz = gen(shape)
        m = fz.stats('m')
        scale = mean / m
        fz = gen(shape, scale=scale, loc=loc)
        return (scale, fz)

    def __enter__(self):
        """ Support with Severity as f: """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self

    def _pdf(self, x, *args):
        if self.conditional:
            return np.where(x > self.limit, 0, np.where(x == self.limit, np.inf if self.pdetach > 0 else 0, self.fz.pdf(x + self.attachment) / self.pattach))
        if self.pattach < 1:
            return np.where(x < 0, 0, np.where(x == 0, np.inf, np.where(x == self.detachment, np.inf, np.where(x > self.detachment, 0, (self.fz.pdf)(x + self.attachment, *args)))))
        return np.where(x < 0, 0, np.where(x == self.detachment, np.inf, np.where(x > self.detachment, 0, (self.fz.pdf)(x + self.attachment, *args))))

    def _cdf(self, x, *args):
        if self.conditional:
            return np.where(x > self.limit, 1, np.where(x < 0, 0, (self.fz.cdf(x + self.attachment) - (1 - self.pattach)) / self.pattach))
        return np.where(x < 0, 0, np.where(x == 0, 1 - self.pattach, np.where(x > self.limit, 1, (self.fz.cdf)(x + self.attachment, *args))))

    def _sf(self, x, *args):
        if self.conditional:
            return np.where(x > self.limit, 0, np.where(x < 0, 1, (self.fz.sf)(x + self.attachment, *args) / self.pattach))
        return np.where(x < 0, 1, np.where(x == 0, self.pattach, np.where(x > self.limit, 0, (self.fz.sf)(x + self.attachment, *args))))

    def _isf(self, q, *args):
        if self.conditional:
            return np.where(q < self.pdetach / self.pattach, self.limit, self.fz.isf(q * self.pattach) - self.attachment)
        return np.where(q >= self.pattach, 0, np.where(q < self.pdetach, self.limit, (self.fz.isf)(q, *args) - self.attachment))

    def _ppf(self, q, *args):
        if self.conditional:
            return np.where(q > 1 - self.pdetach / self.pattach, self.limit, self.fz.ppf(1 - self.pattach * (1 - q)) - self.attachment)
        return np.where(q <= 1 - self.pattach, 0, np.where(q > 1 - self.pdetach, self.limit, (self.fz.ppf)(q, *args) - self.attachment))

    def _stats(self, *args, **kwds):
        ex1, ex2, ex3 = self.moms()
        var = ex2 - ex1 ** 2
        skew = (ex3 - 3 * ex1 * ex2 + 2 * ex1 ** 3) / var ** 1.5
        return np.array([ex1, var, skew, np.nan])

    def _munp(self, n, *args):
        print('wow, called munp')

    def moms--- This code section failed: ---

 L.2322         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                fz
                4  LOAD_METHOD              isf
                6  LOAD_CONST               0.5
                8  CALL_METHOD_1         1  '1 positional argument'
               10  STORE_DEREF              'median'

 L.2324        12  LOAD_CLOSURE             'median'
               14  LOAD_CLOSURE             'self'
               16  BUILD_TUPLE_2         2 
               18  LOAD_CODE                <code_object safe_integrate>
               20  LOAD_STR                 'Severity.moms.<locals>.safe_integrate'
               22  MAKE_FUNCTION_8          'closure'
               24  STORE_FAST               'safe_integrate'

 L.2339        26  LOAD_FAST                'safe_integrate'
               28  LOAD_CLOSURE             'self'
               30  BUILD_TUPLE_1         1 
               32  LOAD_LAMBDA              '<code_object <lambda>>'
               34  LOAD_STR                 'Severity.moms.<locals>.<lambda>'
               36  MAKE_FUNCTION_8          'closure'
               38  LOAD_CONST               1
               40  CALL_FUNCTION_2       2  '2 positional arguments'
               42  STORE_FAST               'ex1'

 L.2340        44  LOAD_FAST                'safe_integrate'
               46  LOAD_CLOSURE             'self'
               48  BUILD_TUPLE_1         1 
               50  LOAD_LAMBDA              '<code_object <lambda>>'
               52  LOAD_STR                 'Severity.moms.<locals>.<lambda>'
               54  MAKE_FUNCTION_8          'closure'
               56  LOAD_CONST               2
               58  CALL_FUNCTION_2       2  '2 positional arguments'
               60  STORE_FAST               'ex2'

 L.2341        62  LOAD_FAST                'safe_integrate'
               64  LOAD_CLOSURE             'self'
               66  BUILD_TUPLE_1         1 
               68  LOAD_LAMBDA              '<code_object <lambda>>'
               70  LOAD_STR                 'Severity.moms.<locals>.<lambda>'
               72  MAKE_FUNCTION_8          'closure'
               74  LOAD_CONST               3
               76  CALL_FUNCTION_2       2  '2 positional arguments'
               78  STORE_FAST               'ex3'

 L.2344        80  LOAD_CONST               1e-05
               82  STORE_FAST               'eps'

 L.2345        84  LOAD_FAST                'ex1'
               86  LOAD_CONST               1
               88  BINARY_SUBSCR    
               90  LOAD_FAST                'ex1'
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  BINARY_TRUE_DIVIDE
               98  LOAD_FAST                'eps'
              100  COMPARE_OP               <
              102  POP_JUMP_IF_TRUE    116  'to 116'
              104  LOAD_FAST                'ex1'
              106  LOAD_CONST               1
              108  BINARY_SUBSCR    
              110  LOAD_CONST               0.0001
              112  COMPARE_OP               <
              114  POP_JUMP_IF_FALSE   184  'to 184'
            116_0  COME_FROM           102  '102'

 L.2346       116  LOAD_FAST                'ex2'
              118  LOAD_CONST               1
              120  BINARY_SUBSCR    
              122  LOAD_FAST                'ex2'
              124  LOAD_CONST               0
              126  BINARY_SUBSCR    
              128  BINARY_TRUE_DIVIDE
              130  LOAD_FAST                'eps'
              132  COMPARE_OP               <
              134  POP_JUMP_IF_TRUE    148  'to 148'
              136  LOAD_FAST                'ex2'
              138  LOAD_CONST               1
              140  BINARY_SUBSCR    
              142  LOAD_CONST               0.0001
              144  COMPARE_OP               <
              146  POP_JUMP_IF_FALSE   184  'to 184'
            148_0  COME_FROM           134  '134'

 L.2347       148  LOAD_FAST                'ex3'
              150  LOAD_CONST               1
              152  BINARY_SUBSCR    
              154  LOAD_FAST                'ex3'
              156  LOAD_CONST               0
              158  BINARY_SUBSCR    
              160  BINARY_TRUE_DIVIDE
              162  LOAD_FAST                'eps'
              164  COMPARE_OP               <
          166_168  POP_JUMP_IF_TRUE    278  'to 278'
              170  LOAD_FAST                'ex3'
              172  LOAD_CONST               1
              174  BINARY_SUBSCR    
              176  LOAD_CONST               1e-06
              178  COMPARE_OP               <
          180_182  POP_JUMP_IF_TRUE    278  'to 278'
            184_0  COME_FROM           146  '146'
            184_1  COME_FROM           114  '114'

 L.2348       184  LOAD_GLOBAL              logger
              186  LOAD_METHOD              info
              188  LOAD_STR                 'Severity.moms | **DOUBTFUL** convergence of integrals, abs errs \t'
              190  LOAD_FAST                'ex1'
              192  LOAD_CONST               1
              194  BINARY_SUBSCR    
              196  FORMAT_VALUE          0  ''
              198  LOAD_STR                 '\t'
              200  LOAD_FAST                'ex2'
              202  LOAD_CONST               1
              204  BINARY_SUBSCR    
              206  FORMAT_VALUE          0  ''
              208  LOAD_STR                 '\t'
              210  LOAD_FAST                'ex3'
              212  LOAD_CONST               1
              214  BINARY_SUBSCR    
              216  FORMAT_VALUE          0  ''
              218  LOAD_STR                 ' \trel errors \t'
              220  LOAD_FAST                'ex1'
              222  LOAD_CONST               1
              224  BINARY_SUBSCR    
              226  LOAD_FAST                'ex1'
              228  LOAD_CONST               0
              230  BINARY_SUBSCR    
              232  BINARY_TRUE_DIVIDE
              234  FORMAT_VALUE          0  ''
              236  LOAD_STR                 '\t'
              238  LOAD_FAST                'ex2'
              240  LOAD_CONST               1
              242  BINARY_SUBSCR    
              244  LOAD_FAST                'ex2'
              246  LOAD_CONST               0
              248  BINARY_SUBSCR    
              250  BINARY_TRUE_DIVIDE
              252  FORMAT_VALUE          0  ''
              254  LOAD_STR                 '\t'
              256  LOAD_FAST                'ex3'
              258  LOAD_CONST               1
              260  BINARY_SUBSCR    
              262  LOAD_FAST                'ex3'
              264  LOAD_CONST               0
              266  BINARY_SUBSCR    
              268  BINARY_TRUE_DIVIDE
              270  FORMAT_VALUE          0  ''
              272  BUILD_STRING_12      12 
              274  CALL_METHOD_1         1  '1 positional argument'
              276  POP_TOP          
            278_0  COME_FROM           180  '180'
            278_1  COME_FROM           166  '166'

 L.2358       278  LOAD_FAST                'ex1'
              280  LOAD_CONST               0
              282  BINARY_SUBSCR    
              284  STORE_FAST               'ex1'

 L.2359       286  LOAD_FAST                'ex2'
              288  LOAD_CONST               0
              290  BINARY_SUBSCR    
              292  STORE_FAST               'ex2'

 L.2360       294  LOAD_FAST                'ex3'
              296  LOAD_CONST               0
              298  BINARY_SUBSCR    
              300  STORE_FAST               'ex3'

 L.2362       302  LOAD_DEREF               'self'
              304  LOAD_ATTR                conditional
          306_308  POP_JUMP_IF_FALSE   340  'to 340'

 L.2363       310  LOAD_FAST                'ex1'
              312  LOAD_DEREF               'self'
              314  LOAD_ATTR                pattach
              316  INPLACE_TRUE_DIVIDE
              318  STORE_FAST               'ex1'

 L.2364       320  LOAD_FAST                'ex2'
              322  LOAD_DEREF               'self'
              324  LOAD_ATTR                pattach
              326  INPLACE_TRUE_DIVIDE
              328  STORE_FAST               'ex2'

 L.2365       330  LOAD_FAST                'ex3'
              332  LOAD_DEREF               'self'
              334  LOAD_ATTR                pattach
              336  INPLACE_TRUE_DIVIDE
              338  STORE_FAST               'ex3'
            340_0  COME_FROM           306  '306'

 L.2367       340  LOAD_FAST                'ex1'
              342  LOAD_FAST                'ex2'
              344  LOAD_FAST                'ex3'
              346  BUILD_TUPLE_3         3 
              348  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 278_0

    def plot(self, N=100, axiter=None):
        """
        quick plot

        :param axiter:
        :param N:
        :return:
        """
        ps = np.linspace(0, 1, N, endpoint=False)
        xs = np.linspace(0, self._isf(0.0001), N)
        do_tight = axiter is None
        axiter = axiter_factory(None, 4)
        ax = next(axiter)
        ys = self._pdf(xs)
        ax.plot(xs, ys)
        ax.grid(which='major', axis='both', linestyle='-', linewidth='0.1', color='blue', alpha=0.5)
        ax.set_title('PDF')
        ys = self._cdf(xs)
        ax = next(axiter)
        ax.plot(xs, ys, drawstyle='steps-post', lw=1)
        ax.grid(which='major', axis='both', linestyle='-', linewidth='0.1', color='blue', alpha=0.5)
        ax.set(title='CDF', ylim=(0, 1))
        ys = self._isf(ps)
        ax = next(axiter)
        ax.plot(ps, ys, drawstyle='steps-post', lw=1)
        ax.grid(which='major', axis='both', linestyle='-', linewidth='0.1', color='blue', alpha=0.5)
        ax.set(title='ISF', xlim=(0, 1))
        ax = next(axiter)
        ax.plot((1 - ps), ys, drawstyle='steps-post', lw=1)
        ax.grid(which='major', axis='both', linestyle='-', linewidth='0.1', color='blue', alpha=0.5)
        ax.set(title='Lee diagram', xlim=(0, 1))
        if do_tight:
            axiter.tidy()
            suptitle_and_tight(self.long_name)


class CarefulInverse(object):
    __doc__ = '\n    from SRM_Examples Noise: careful inverse functions\n\n    '

    @staticmethod
    def make1d(xs, ys, agg_fun=None, kind='linear', **kwargs):
        """
        Wrapper to make a reasonable 1d interpolation function with reasonable extrapolation
        Does NOT handle inverse functions, for those use dist_inv1d
        :param xs:
        :param ys:
        :param agg_fun:
        :param kind:
        :param kwargs:
        :return:
        """
        temp = pd.DataFrame(dict(x=xs, y=ys))
        if agg_fun:
            temp = temp.groupby('x').agg(agg_fun)
            fill_value = (temp.y.iloc[0], temp.y.iloc[(-1)])
            f = (interpolate.interp1d)(temp.index, temp.y, kind=kind, bounds_error=False, fill_value=fill_value, **kwargs)
        else:
            fill_value = (
             temp.y.iloc[0], temp.y.iloc[(-1)])
            f = (interpolate.interp1d)(temp.x, temp.y, kind=kind, bounds_error=False, fill_value=fill_value, **kwargs)
        return f

    @staticmethod
    def dist_inv1d(xs, fx, kind='linear', max_Fx=1.0):
        """
        from SRM_Examples Noise
        Careful inverse of distribution function with jumps. Assumes xs is evenly spaced.
        Assumes that if there are two or more xs values between changes in dist it is a jump,
        otherwise is is a continuous part. Puts in -eps values to make steps around jumps.
        :param xs:
        :param fx:  density
        :param kind:
        :param max_Fx: what is the max allowable value of F(x)?
        """
        df = pd.DataFrame(dict(x=xs, fx=fx))
        df['fx'] = np.where(np.abs(df.fx) < 1e-16, 0, df.fx)
        df['Fx'] = df.fx.cumsum()
        gs = df.groupby('Fx').agg({'x': [np.min, np.max, len]})
        gs.columns = ['mn', 'mx', 'n']
        gs['jump'] = 0
        gs.loc[(gs.n > 1, 'jump')] = 1
        gs = gs.reset_index(drop=False)
        gs['nextFx'] = gs.Fx.shift((-1), fill_value=1)
        ans = np.zeros((2 * len(gs), 2))
        rn = 0
        eps = 1e-10
        max_Fx -= eps / 100
        for n, r in gs.iterrows():
            ans[(rn, 0)] = r.Fx
            ans[(rn, 1)] = r.mn if r.Fx >= max_Fx else r.mx
            rn += 1
            if r.Fx >= max_Fx:
                break
            if r.jump:
                if r.nextFx >= max_Fx:
                    break
                ans[(rn, 0)] = r.nextFx - eps
                ans[(rn, 1)] = r.mx
                rn += 1

        ans = ans[:rn, :]
        fv = (
         ans[(0, 1)], ans[(-1, 1)])
        ff = interpolate.interp1d((ans[:, 0]), (ans[:, 1]), bounds_error=False, fill_value=fv, kind=kind)
        return ff