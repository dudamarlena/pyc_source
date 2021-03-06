# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lib/python2.7/site-packages/openturns/dist_bundle1.py
# Compiled at: 2019-11-13 10:36:51
"""Probabilistic distributions."""
from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')
if __package__ or '.' in __name__:
    from . import _dist_bundle1
else:
    import _dist_bundle1
try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = 'proxy of ' + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ''

    return '<%s.%s; %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


def _swig_setattr_nondynamic_instance_variable(set):

    def set_instance_attr(self, name, value):
        if name == 'thisown':
            self.this.own(value)
        elif name == 'this':
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError('You cannot add instance attributes to %s' % self)

    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):

    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError('You cannot add class attributes to %s' % cls)

    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""

    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())

    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined - class is abstract')

    __repr__ = _swig_repr
    __swig_destroy__ = _dist_bundle1.delete_SwigPyIterator

    def value(self):
        return _dist_bundle1.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _dist_bundle1.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _dist_bundle1.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _dist_bundle1.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _dist_bundle1.SwigPyIterator_equal(self, x)

    def copy(self):
        return _dist_bundle1.SwigPyIterator_copy(self)

    def next(self):
        return _dist_bundle1.SwigPyIterator_next(self)

    def __next__(self):
        return _dist_bundle1.SwigPyIterator___next__(self)

    def previous(self):
        return _dist_bundle1.SwigPyIterator_previous(self)

    def advance(self, n):
        return _dist_bundle1.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _dist_bundle1.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _dist_bundle1.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _dist_bundle1.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _dist_bundle1.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _dist_bundle1.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _dist_bundle1.SwigPyIterator___sub__(self, *args)

    def __iter__(self):
        return self


_dist_bundle1.SwigPyIterator_swigregister(SwigPyIterator)

class TestFailed():
    """TestFailed is used to raise an uniform exception in tests."""
    __type = 'TestFailed'

    def __init__(self, reason=''):
        self.reason = reason

    def type(self):
        return TestFailed.__type

    def what(self):
        return self.reason

    def __str__(self):
        return TestFailed.__type + ': ' + self.reason

    def __lshift__(self, ch):
        self.reason += ch
        return self


import openturns.base, openturns.common, openturns.typ, openturns.statistics, openturns.graph, openturns.func, openturns.geom, openturns.diff, openturns.optim, openturns.experiment, openturns.solver, openturns.algo, openturns.model_copula

class DistFunc(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    @staticmethod
    def pBeta(p1, p2, x, tail=False):
        return _dist_bundle1.DistFunc_pBeta(p1, p2, x, tail)

    @staticmethod
    def qBeta(p1, p2, p, tail=False):
        return _dist_bundle1.DistFunc_qBeta(p1, p2, p, tail)

    @staticmethod
    def rBeta(*args):
        return _dist_bundle1.DistFunc_rBeta(*args)

    @staticmethod
    def logdBinomial(n, p, k):
        r"""
        Logarithm of the probability function of a binomial distribution.

        Parameters
        ----------
        n : int, :math:`n>0`
            The number of trials
        p : float, :math:`0\leq p\leq 1`
            The success probability of each trial
        k : int
            The number of success.

        Returns
        -------
        logp : float
            The natural logarithm of the probability to get :math:`k` successes.

        Notes
        -----
        This method implements Loader's algorithm, the *fast* and *accurate* method
        described in [loader2000]_, with the further improvements mentioned
        in [dimitriadis2016]_.

        Examples
        --------
        >>> import openturns as ot
        >>> p = ot.DistFunc.logdBinomial(5, 0.2, 2)
        """
        return _dist_bundle1.DistFunc_logdBinomial(n, p, k)

    @staticmethod
    def dBinomial(n, p, k):
        r"""
        Probability function of a binomial distribution.

        Parameters
        ----------
        n : int, :math:`n>0`
            The number of trials
        p : float, :math:`0\leq p\leq 1`
            The success probability of each trial
        k : int
            The number of success.

        Returns
        -------
        probability : float
            The probability to get :math:`k` successes.

        Notes
        -----
        This method implements Loader's algorithm, the *fast* and *accurate* method
        described in [loader2000]_, with the further improvements mentioned
        in [dimitriadis2016]_.

        Examples
        --------
        >>> import openturns as ot
        >>> p = ot.DistFunc.dBinomial(5, 0.2, 2)
        """
        return _dist_bundle1.DistFunc_dBinomial(n, p, k)

    @staticmethod
    def rBinomial(*args):
        r"""
        Realization of a binomial distribution.

        Parameters
        ----------
        n : int, :math:`n>0`
            The number of trials
        p : float, :math:`0\leq p\leq 1`
            The success probability of each trial
        size : int
            The number of realizations to generate.

        Returns
        -------
        realizations : int or :class:`~openturns.Indices`
            The realizations of the discrete disctribution.

        Notes
        -----
        This method implements the rejection algorithm described in [hormann1993]_.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> r = ot.DistFunc.rBinomial(5, 0.3)
        >>> r = ot.DistFunc.rBinomial(5, 0.3, 10)
        """
        return _dist_bundle1.DistFunc_rBinomial(*args)

    @staticmethod
    def rDiscrete(*args):
        r"""
        Realization of a bounded integral discrete distribution.

        Parameters
        ----------
        probabilities : sequence of float
            The probabilities of the discrete distribution :math:`p_k=\Prob{X=k}`,
            where :math:`p_k\in[0,1]` and :math:`\sum_{k=1}^n p_k=1`.
        size : int
            The number of realizations to generate.

        Returns
        -------
        realizations : int or :class:`~openturns.Indices`
            The realizations of the discrete disctribution.

        Notes
        -----
        This method implements the *alias* method as described in [devroye1986]_,
        Chapter 3. It has an optimal space complexity of :math:`\cO(n)` and runtime CPU
        complexity of :math:`\cO(1)`.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> r = ot.DistFunc.rDiscrete([0.2, 0.3, 0.5])
        >>> r = ot.DistFunc.rDiscrete([0.2, 0.3, 0.5], 10)
        """
        return _dist_bundle1.DistFunc_rDiscrete(*args)

    @staticmethod
    def pGamma(k, x, tail=False):
        return _dist_bundle1.DistFunc_pGamma(k, x, tail)

    @staticmethod
    def qGamma(k, p, tail=False):
        return _dist_bundle1.DistFunc_qGamma(k, p, tail)

    @staticmethod
    def rGamma(*args):
        return _dist_bundle1.DistFunc_rGamma(*args)

    @staticmethod
    def dHypergeometric(n, k, m, x):
        r"""
        The probability function of an hypergeometric distribution.

        Parameters
        ----------
        n : int, :math:`n\geq 0`
            The population size
        k : int, :math:`0\leq k\leq n`
            The number of candidates in the population
        m : int, :math:`0\leq m\leq n`
            The number of individuals in a draw
        x : int, :math:`x\geq 0`
            The number of candidates in a draw

        Returns
        -------
        p : float
            The probability to get :math:`x` candidates in a draw.

        Notes
        -----
        This method is based on an algorithm similar to Loader's algorithm, the *fast*
        and *accurate* method described in [loader2000]_, with the further improvements
        mentioned in [dimitriadis2016]_.

        Examples
        --------
        >>> import openturns as ot
        >>> p = ot.DistFunc.dHypergeometric(10, 4, 7, 2)
        """
        return _dist_bundle1.DistFunc_dHypergeometric(n, k, m, x)

    @staticmethod
    def logdHypergeometric(n, k, m, x):
        r"""
        Logarithm of the probability function of an hypergeometric distribution.

        Parameters
        ----------
        n : int, :math:`n\geq 0`
            The population size
        k : int, :math:`0\leq k\leq n`
            The number of candidates in the population
        m : int, :math:`0\leq m\leq n`
            The number of individuals in a draw
        x : int, :math:`x\geq 0`
            The number of candidates in a draw

        Returns
        -------
        logp : float
            The natural logarithm of the probability to get :math:`x` candidates in a draw.

        Notes
        -----
        This method is based on an algorithm similar to Loader's algorithm, the *fast*
        and *accurate* method described in [loader2000]_, with the further improvements
        mentioned in [dimitriadis2016]_.

        Examples
        --------
        >>> import openturns as ot
        >>> p = ot.DistFunc.logdHypergeometric(10, 4, 7, 2)
        """
        return _dist_bundle1.DistFunc_logdHypergeometric(n, k, m, x)

    @staticmethod
    def pHypergeometric(n, k, m, x, tail=False):
        r"""
        The cumulative probability function of an hypergeometric distribution.

        Parameters
        ----------
        n : int, :math:`n\geq 0`
            The population size
        k : int, :math:`0\leq k\leq n`
            The number of candidates in the population
        m : int, :math:`0\leq m\leq n`
            The number of individuals in a draw
        x : int, :math:`x\geq 0`
            The number of candidates in a draw
        tail : bool
            Flag to tell if it is the CDF or its complement which is evaluated

        Returns
        -------
        p : float
            The probability to get at most :math:`x` candidates in a draw.

        Notes
        -----
        This method is based on a summation of the probability function toward the upper
        bound or the lower bound of the range depending on the position of :math:`x` wrt
        the mode :math:`\left\lfloor\dfrac{(k+1)(m+1)}{n+2}\right\rfloor` of the
        distribution, then take the complement if needed.

        Examples
        --------
        >>> import openturns as ot
        >>> p = ot.DistFunc.pHypergeometric(10, 4, 7, 2)
        >>> p = ot.DistFunc.pHypergeometric(10, 4, 7, 2, True)
        """
        return _dist_bundle1.DistFunc_pHypergeometric(n, k, m, x, tail)

    @staticmethod
    def rHypergeometric(*args):
        r"""
        Realization of an hypergeometric distribution.

        Parameters
        ----------
        n : int, :math:`n\geq 0`
            The population size
        k : int, :math:`0\leq k\leq n`
            The number of candidates in the population
        m : int, :math:`0\leq m\leq n`
            The number of individuals in a draw
        size : int
            The number of realizations to generate.

        Returns
        -------
        realizations : int or :class:`~openturns.Indices`
            The realizations of the discrete disctribution.

        Notes
        -----
        This method is based on the alias method.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> r = ot.DistFunc.rHypergeometric(10, 4, 7)
        >>> r = ot.DistFunc.rHypergeometric(10, 4, 7, 10)
        """
        return _dist_bundle1.DistFunc_rHypergeometric(*args)

    @staticmethod
    def pKolmogorov(n, x, tail=False):
        return _dist_bundle1.DistFunc_pKolmogorov(n, x, tail)

    @staticmethod
    def dNonCentralChiSquare(*args):
        return _dist_bundle1.DistFunc_dNonCentralChiSquare(*args)

    @staticmethod
    def pNonCentralChiSquare(*args):
        return _dist_bundle1.DistFunc_pNonCentralChiSquare(*args)

    @staticmethod
    def rNonCentralChiSquare(*args):
        return _dist_bundle1.DistFunc_rNonCentralChiSquare(*args)

    @staticmethod
    def dNonCentralStudent(nu, delta, x):
        return _dist_bundle1.DistFunc_dNonCentralStudent(nu, delta, x)

    @staticmethod
    def dNonCentralStudentAlt0(*args):
        return _dist_bundle1.DistFunc_dNonCentralStudentAlt0(*args)

    @staticmethod
    def pNonCentralStudent(nu, delta, x, tail=False):
        return _dist_bundle1.DistFunc_pNonCentralStudent(nu, delta, x, tail)

    @staticmethod
    def rNonCentralStudent(*args):
        return _dist_bundle1.DistFunc_rNonCentralStudent(*args)

    @staticmethod
    def pNormal(*args):
        """
        CDF of an unit-variance centered Normal distribution.

        Parameters
        ----------
        x : float
            Location
        tail : bool, default=False
            Tail flag

        Returns
        -------
        cdf : float

        Examples
        --------
        >>> import openturns as ot
        >>> cdf = ot.DistFunc.pNormal(0.9)
        """
        return _dist_bundle1.DistFunc_pNormal(*args)

    @staticmethod
    def pNormal2D(x1, x2, rho, tail=False):
        return _dist_bundle1.DistFunc_pNormal2D(x1, x2, rho, tail)

    @staticmethod
    def pNormal3D(x1, x2, x3, rho12, rho13, rho23, tail=False):
        return _dist_bundle1.DistFunc_pNormal3D(x1, x2, x3, rho12, rho13, rho23, tail)

    @staticmethod
    def qNormal(*args):
        """
        Quantile of an unit-variance centered Normal distribution.

        Parameters
        ----------
        prob : float

        Returns
        -------
        q : float

        Examples
        --------
        >>> import openturns as ot
        >>> q = ot.DistFunc.qNormal(0.95)
        """
        return _dist_bundle1.DistFunc_qNormal(*args)

    @staticmethod
    def rNormal(*args):
        """
        Realization of an unit-variance centered Normal distribution.

        Returns
        -------
        realization : float

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> r = ot.DistFunc.rNormal()
        """
        return _dist_bundle1.DistFunc_rNormal(*args)

    @staticmethod
    def logdPoisson(_lambda, k):
        r"""
        Logarithm of the probability function of a Poisson distribution.

        Parameters
        ----------
        lambda: float, :math:`\lambda\geq 0`
            The intensity of the Poisson distribution
        k : int
            The number of success.

        Returns
        -------
        logp : float
            The natural logarithm of the probability to get :math:`k` successes.

        Notes
        -----
        This method implements Loader's algorithm, the *fast* and *accurate* method
        described in [loader2000]_, with the further improvements mentioned
        in [dimitriadis2016]_.

        Examples
        --------
        >>> import openturns as ot
        >>> p = ot.DistFunc.logdPoisson(5.0, 2)
        """
        return _dist_bundle1.DistFunc_logdPoisson(_lambda, k)

    @staticmethod
    def dPoisson(_lambda, k):
        r"""
        Probability function of a Poisson distribution.

        Parameters
        ----------
        lambda: float, :math:`\lambda\geq 0`
            The intensity of the Poisson distribution
        k : int
            The number of success.

        Returns
        -------
        logp : float
            The natural logarithm of the probability to get :math:`k` successes.

        Notes
        -----
        This method implements Loader's algorithm, the *fast* and *accurate* method
        described in [loader2000]_, with the further improvements mentioned
        in [dimitriadis2016]_.

        Examples
        --------
        >>> import openturns as ot
        >>> p = ot.DistFunc.dPoisson(5.0, 2)
        """
        return _dist_bundle1.DistFunc_dPoisson(_lambda, k)

    @staticmethod
    def qPoisson(_lambda, p, tail=False):
        return _dist_bundle1.DistFunc_qPoisson(_lambda, p, tail)

    @staticmethod
    def rPoisson(*args):
        r"""
        Realization of a Poisson distribution.

        Parameters
        ----------
        lambda: float, :math:`\lambda\geq 0`
            The intensity of the Poisson distribution
        size : int
            The number of realizations to generate.

        Returns
        -------
        realizations : int or :class:`~openturns.Indices`
            The realizations of the discrete disctribution.

        Notes
        -----
        For the small values of :math:`\lambda`, we use the method of inversion by
        sequential search described in [devroye1986]_ and with the important errata in
        [devroye1986b]_. For the large values of :math:`\lambda`, we use the ratio of
        uniform method described in [stadlober1990]_.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> r = ot.DistFunc.rPoisson(5.0)
        >>> r = ot.DistFunc.rPoisson(5.0, 10)
        """
        return _dist_bundle1.DistFunc_rPoisson(*args)

    @staticmethod
    def pPearsonCorrelation(size, rho, tail=False):
        r"""
        Asymptotic probability function for the Pearson :math:`\rho` correlation.

        Parameters
        ----------
        n : int
            The size of the population

        rho : float :math:`-1<rho<1`
            The Pearson correlation coefficient

        tail : bool
            Tells if we consider to be in the critical region (tTrue)
            Default value is False

        Returns
        -------
        pvalue : float
            The probability to be in the region of interest

        Notes
        -----
        This method allows to compute the *asymptotic* distribution of the
        `Pearson` correlation coefficient issued from two univariate samples
        of size `n`. Basically, we want to measure how coefficient is significatly
        different from `0`. If `tail` is True, the issued value measures probability
        to be in the critical region.

        Examples
        --------
        >>> import openturns as ot
        >>> pval = ot.DistFunc.pPearsonCorrelation(100, 0.3, True)
        """
        return _dist_bundle1.DistFunc_pPearsonCorrelation(size, rho, tail)

    @staticmethod
    def pSpearmanCorrelation(size, rho, tail=False, ties=False):
        return _dist_bundle1.DistFunc_pSpearmanCorrelation(size, rho, tail, ties)

    @staticmethod
    def pStudent(*args):
        return _dist_bundle1.DistFunc_pStudent(*args)

    @staticmethod
    def qStudent(*args):
        return _dist_bundle1.DistFunc_qStudent(*args)

    @staticmethod
    def rStudent(*args):
        return _dist_bundle1.DistFunc_rStudent(*args)

    @staticmethod
    def rUniformTriangle(*args):
        return _dist_bundle1.DistFunc_rUniformTriangle(*args)

    @staticmethod
    def eZ1(n):
        return _dist_bundle1.DistFunc_eZ1(n)

    @staticmethod
    def kFactorPooled(n, m, p, alpha):
        r"""
        Exact margin factor for bilateral covering interval of pooled Normal populations.

        Parameters
        ----------
        n : int
            The size of the population

        m : int
            The size of the pool

        p : float :math:`0<p<1`
            The probability level of the covering interval

        alpha : float :math:`0<\alpha<1`
            The confidence level of the covering interval

        Returns
        -------
        k : float
            The margin factor

        Notes
        -----
        This method allows to compute the *exact* margin factor :math:`k` of a
        pool of :math:`m` Normal populations of size :math:`n` with unknown
        means :math:`\mu_i` and unknown common variance :math:`\sigma^2`.
        Let :math:`m_i=\dfrac{1}{n}\sum_{j=1}^nX_{ij}` be the empirical mean
        of the ith population :math:`(X_{i1},\dots,X_{in})` and
        :math:`\sigma^2_{mn}=\dfrac{}{}\sum_{i=1}^m\sum_{j=1}^n(X_{ij}-m_i)^2`
        the empirical *pooled* variance. The covering factor :math:`k` is such
        that the intervals :math:`[m_i-k\sigma_{mn},m_i+k\sigma_{mn}]` satisfy:

        .. math::
            \Prob{\Prob{X_i\in[m_i-k\sigma_{mn},m_i+k\sigma_{mn}]}\geq p}=\alpha

        for :math:`i\in\{1,\dots,m\}`. It reduces to find :math:`k` such that:

        .. math::
            \int_{\Rset}F(x,k;\nu_{m,n},p)\phi_{0,1/\sqrt{n}}(x)\,\di x = \alpha

        where :math:`phi_{0,1/\sqrt{n}}` is the density function of the normal
        distribution with a mean equals to 0 and a variance equals to
        :math:`1/n`, :math:`\nu_{m,n}=m(n-1)` and :math:`F(x,k;\nu_{m,n},p)`
        the function defined by:

        .. math::
            F(x,k;\nu_{m,n},p)=\bar{F}_{\chi^2_{\nu_{m,n}}}(\nu_{m,n} R^2(x;p)/k^2)

        where :math:`\bar{F}_{\chi^2_{\nu_{m,n}}}` is the complementary distribution
        function of a chi-square distribution with :math:`\nu_{m,n}` degrees
        of freedom and :math:`R(x;p)` the solution of:

        .. math::
            \Phi(x + R) - \Phi(x - R) = p

        Examples
        --------
        >>> import openturns as ot
        >>> k = ot.DistFunc.kFactorPooled(5, 3, 0.95, 0.9)
        """
        return _dist_bundle1.DistFunc_kFactorPooled(n, m, p, alpha)

    @staticmethod
    def kFactor(n, p, alpha):
        r"""
        Exact margin factor for bilateral covering interval of a Normal population.

        Parameters
        ----------
        n : int
            The size of the population

        p : float :math:`0<p<1`
            The probability level of the covering interval

        alpha : float :math:`0<\alpha<1`
            The confidence level of the covering interval

        Returns
        -------
        k : float
            The margin factor

        Notes
        -----
        This method allows to compute the *exact* margin factor :math:`k` of a
        Normal population of size :math:`n` with unknown
        means :math:`\mu_i` and unknown common variance :math:`\sigma^2`. It
        is equivalent to the pooled version with :math:`m=1`.

        Examples
        --------
        >>> import openturns as ot
        >>> k = ot.DistFunc.kFactor(5, 0.95, 0.9)
        """
        return _dist_bundle1.DistFunc_kFactor(n, p, alpha)

    @staticmethod
    def pDickeyFullerTrend(x, tail=False):
        return _dist_bundle1.DistFunc_pDickeyFullerTrend(x, tail)

    @staticmethod
    def pDickeyFullerConstant(x, tail=False):
        return _dist_bundle1.DistFunc_pDickeyFullerConstant(x, tail)

    @staticmethod
    def pDickeyFullerNoConstant(x, tail=False):
        return _dist_bundle1.DistFunc_pDickeyFullerNoConstant(x, tail)

    @staticmethod
    def qDickeyFullerTrend(p, tail=False):
        return _dist_bundle1.DistFunc_qDickeyFullerTrend(p, tail)

    @staticmethod
    def qDickeyFullerConstant(p, tail=False):
        return _dist_bundle1.DistFunc_qDickeyFullerConstant(p, tail)

    @staticmethod
    def qDickeyFullerNoConstant(p, tail=False):
        return _dist_bundle1.DistFunc_qDickeyFullerNoConstant(p, tail)

    def __init__(self):
        _dist_bundle1.DistFunc_swiginit(self, _dist_bundle1.new_DistFunc())

    __swig_destroy__ = _dist_bundle1.delete_DistFunc


_dist_bundle1.DistFunc_swigregister(DistFunc)
cvar = _dist_bundle1.cvar
DistFunc.NumberOfBandNormalZigurrat = _dist_bundle1.cvar.DistFunc_NumberOfBandNormalZigurrat
DistFunc.NormalZigguratTail = _dist_bundle1.cvar.DistFunc_NormalZigguratTail
DistFunc.NormalZigguratAbscissa = _dist_bundle1.cvar.DistFunc_NormalZigguratAbscissa
DistFunc.NormalZigguratRatio = _dist_bundle1.cvar.DistFunc_NormalZigguratRatio

def DistFunc_pBeta(p1, p2, x, tail=False):
    return _dist_bundle1.DistFunc_pBeta(p1, p2, x, tail)


def DistFunc_qBeta(p1, p2, p, tail=False):
    return _dist_bundle1.DistFunc_qBeta(p1, p2, p, tail)


def DistFunc_rBeta(*args):
    return _dist_bundle1.DistFunc_rBeta(*args)


def DistFunc_logdBinomial(n, p, k):
    r"""
    Logarithm of the probability function of a binomial distribution.

    Parameters
    ----------
    n : int, :math:`n>0`
        The number of trials
    p : float, :math:`0\leq p\leq 1`
        The success probability of each trial
    k : int
        The number of success.

    Returns
    -------
    logp : float
        The natural logarithm of the probability to get :math:`k` successes.

    Notes
    -----
    This method implements Loader's algorithm, the *fast* and *accurate* method
    described in [loader2000]_, with the further improvements mentioned
    in [dimitriadis2016]_.

    Examples
    --------
    >>> import openturns as ot
    >>> p = ot.DistFunc.logdBinomial(5, 0.2, 2)
    """
    return _dist_bundle1.DistFunc_logdBinomial(n, p, k)


def DistFunc_dBinomial(n, p, k):
    r"""
    Probability function of a binomial distribution.

    Parameters
    ----------
    n : int, :math:`n>0`
        The number of trials
    p : float, :math:`0\leq p\leq 1`
        The success probability of each trial
    k : int
        The number of success.

    Returns
    -------
    probability : float
        The probability to get :math:`k` successes.

    Notes
    -----
    This method implements Loader's algorithm, the *fast* and *accurate* method
    described in [loader2000]_, with the further improvements mentioned
    in [dimitriadis2016]_.

    Examples
    --------
    >>> import openturns as ot
    >>> p = ot.DistFunc.dBinomial(5, 0.2, 2)
    """
    return _dist_bundle1.DistFunc_dBinomial(n, p, k)


def DistFunc_rBinomial(*args):
    r"""
    Realization of a binomial distribution.

    Parameters
    ----------
    n : int, :math:`n>0`
        The number of trials
    p : float, :math:`0\leq p\leq 1`
        The success probability of each trial
    size : int
        The number of realizations to generate.

    Returns
    -------
    realizations : int or :class:`~openturns.Indices`
        The realizations of the discrete disctribution.

    Notes
    -----
    This method implements the rejection algorithm described in [hormann1993]_.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> r = ot.DistFunc.rBinomial(5, 0.3)
    >>> r = ot.DistFunc.rBinomial(5, 0.3, 10)
    """
    return _dist_bundle1.DistFunc_rBinomial(*args)


def DistFunc_rDiscrete(*args):
    r"""
    Realization of a bounded integral discrete distribution.

    Parameters
    ----------
    probabilities : sequence of float
        The probabilities of the discrete distribution :math:`p_k=\Prob{X=k}`,
        where :math:`p_k\in[0,1]` and :math:`\sum_{k=1}^n p_k=1`.
    size : int
        The number of realizations to generate.

    Returns
    -------
    realizations : int or :class:`~openturns.Indices`
        The realizations of the discrete disctribution.

    Notes
    -----
    This method implements the *alias* method as described in [devroye1986]_,
    Chapter 3. It has an optimal space complexity of :math:`\cO(n)` and runtime CPU
    complexity of :math:`\cO(1)`.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> r = ot.DistFunc.rDiscrete([0.2, 0.3, 0.5])
    >>> r = ot.DistFunc.rDiscrete([0.2, 0.3, 0.5], 10)
    """
    return _dist_bundle1.DistFunc_rDiscrete(*args)


def DistFunc_pGamma(k, x, tail=False):
    return _dist_bundle1.DistFunc_pGamma(k, x, tail)


def DistFunc_qGamma(k, p, tail=False):
    return _dist_bundle1.DistFunc_qGamma(k, p, tail)


def DistFunc_rGamma(*args):
    return _dist_bundle1.DistFunc_rGamma(*args)


def DistFunc_dHypergeometric(n, k, m, x):
    r"""
    The probability function of an hypergeometric distribution.

    Parameters
    ----------
    n : int, :math:`n\geq 0`
        The population size
    k : int, :math:`0\leq k\leq n`
        The number of candidates in the population
    m : int, :math:`0\leq m\leq n`
        The number of individuals in a draw
    x : int, :math:`x\geq 0`
        The number of candidates in a draw

    Returns
    -------
    p : float
        The probability to get :math:`x` candidates in a draw.

    Notes
    -----
    This method is based on an algorithm similar to Loader's algorithm, the *fast*
    and *accurate* method described in [loader2000]_, with the further improvements
    mentioned in [dimitriadis2016]_.

    Examples
    --------
    >>> import openturns as ot
    >>> p = ot.DistFunc.dHypergeometric(10, 4, 7, 2)
    """
    return _dist_bundle1.DistFunc_dHypergeometric(n, k, m, x)


def DistFunc_logdHypergeometric(n, k, m, x):
    r"""
    Logarithm of the probability function of an hypergeometric distribution.

    Parameters
    ----------
    n : int, :math:`n\geq 0`
        The population size
    k : int, :math:`0\leq k\leq n`
        The number of candidates in the population
    m : int, :math:`0\leq m\leq n`
        The number of individuals in a draw
    x : int, :math:`x\geq 0`
        The number of candidates in a draw

    Returns
    -------
    logp : float
        The natural logarithm of the probability to get :math:`x` candidates in a draw.

    Notes
    -----
    This method is based on an algorithm similar to Loader's algorithm, the *fast*
    and *accurate* method described in [loader2000]_, with the further improvements
    mentioned in [dimitriadis2016]_.

    Examples
    --------
    >>> import openturns as ot
    >>> p = ot.DistFunc.logdHypergeometric(10, 4, 7, 2)
    """
    return _dist_bundle1.DistFunc_logdHypergeometric(n, k, m, x)


def DistFunc_pHypergeometric(n, k, m, x, tail=False):
    r"""
    The cumulative probability function of an hypergeometric distribution.

    Parameters
    ----------
    n : int, :math:`n\geq 0`
        The population size
    k : int, :math:`0\leq k\leq n`
        The number of candidates in the population
    m : int, :math:`0\leq m\leq n`
        The number of individuals in a draw
    x : int, :math:`x\geq 0`
        The number of candidates in a draw
    tail : bool
        Flag to tell if it is the CDF or its complement which is evaluated

    Returns
    -------
    p : float
        The probability to get at most :math:`x` candidates in a draw.

    Notes
    -----
    This method is based on a summation of the probability function toward the upper
    bound or the lower bound of the range depending on the position of :math:`x` wrt
    the mode :math:`\left\lfloor\dfrac{(k+1)(m+1)}{n+2}\right\rfloor` of the
    distribution, then take the complement if needed.

    Examples
    --------
    >>> import openturns as ot
    >>> p = ot.DistFunc.pHypergeometric(10, 4, 7, 2)
    >>> p = ot.DistFunc.pHypergeometric(10, 4, 7, 2, True)
    """
    return _dist_bundle1.DistFunc_pHypergeometric(n, k, m, x, tail)


def DistFunc_rHypergeometric(*args):
    r"""
    Realization of an hypergeometric distribution.

    Parameters
    ----------
    n : int, :math:`n\geq 0`
        The population size
    k : int, :math:`0\leq k\leq n`
        The number of candidates in the population
    m : int, :math:`0\leq m\leq n`
        The number of individuals in a draw
    size : int
        The number of realizations to generate.

    Returns
    -------
    realizations : int or :class:`~openturns.Indices`
        The realizations of the discrete disctribution.

    Notes
    -----
    This method is based on the alias method.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> r = ot.DistFunc.rHypergeometric(10, 4, 7)
    >>> r = ot.DistFunc.rHypergeometric(10, 4, 7, 10)
    """
    return _dist_bundle1.DistFunc_rHypergeometric(*args)


def DistFunc_pKolmogorov(n, x, tail=False):
    return _dist_bundle1.DistFunc_pKolmogorov(n, x, tail)


def DistFunc_dNonCentralChiSquare(*args):
    return _dist_bundle1.DistFunc_dNonCentralChiSquare(*args)


def DistFunc_pNonCentralChiSquare(*args):
    return _dist_bundle1.DistFunc_pNonCentralChiSquare(*args)


def DistFunc_rNonCentralChiSquare(*args):
    return _dist_bundle1.DistFunc_rNonCentralChiSquare(*args)


def DistFunc_dNonCentralStudent(nu, delta, x):
    return _dist_bundle1.DistFunc_dNonCentralStudent(nu, delta, x)


def DistFunc_dNonCentralStudentAlt0(*args):
    return _dist_bundle1.DistFunc_dNonCentralStudentAlt0(*args)


def DistFunc_pNonCentralStudent(nu, delta, x, tail=False):
    return _dist_bundle1.DistFunc_pNonCentralStudent(nu, delta, x, tail)


def DistFunc_rNonCentralStudent(*args):
    return _dist_bundle1.DistFunc_rNonCentralStudent(*args)


def DistFunc_pNormal(*args):
    """
    CDF of an unit-variance centered Normal distribution.

    Parameters
    ----------
    x : float
        Location
    tail : bool, default=False
        Tail flag

    Returns
    -------
    cdf : float

    Examples
    --------
    >>> import openturns as ot
    >>> cdf = ot.DistFunc.pNormal(0.9)
    """
    return _dist_bundle1.DistFunc_pNormal(*args)


def DistFunc_pNormal2D(x1, x2, rho, tail=False):
    return _dist_bundle1.DistFunc_pNormal2D(x1, x2, rho, tail)


def DistFunc_pNormal3D(x1, x2, x3, rho12, rho13, rho23, tail=False):
    return _dist_bundle1.DistFunc_pNormal3D(x1, x2, x3, rho12, rho13, rho23, tail)


def DistFunc_qNormal(*args):
    """
    Quantile of an unit-variance centered Normal distribution.

    Parameters
    ----------
    prob : float

    Returns
    -------
    q : float

    Examples
    --------
    >>> import openturns as ot
    >>> q = ot.DistFunc.qNormal(0.95)
    """
    return _dist_bundle1.DistFunc_qNormal(*args)


def DistFunc_rNormal(*args):
    """
    Realization of an unit-variance centered Normal distribution.

    Returns
    -------
    realization : float

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> r = ot.DistFunc.rNormal()
    """
    return _dist_bundle1.DistFunc_rNormal(*args)


def DistFunc_logdPoisson(_lambda, k):
    r"""
    Logarithm of the probability function of a Poisson distribution.

    Parameters
    ----------
    lambda: float, :math:`\lambda\geq 0`
        The intensity of the Poisson distribution
    k : int
        The number of success.

    Returns
    -------
    logp : float
        The natural logarithm of the probability to get :math:`k` successes.

    Notes
    -----
    This method implements Loader's algorithm, the *fast* and *accurate* method
    described in [loader2000]_, with the further improvements mentioned
    in [dimitriadis2016]_.

    Examples
    --------
    >>> import openturns as ot
    >>> p = ot.DistFunc.logdPoisson(5.0, 2)
    """
    return _dist_bundle1.DistFunc_logdPoisson(_lambda, k)


def DistFunc_dPoisson(_lambda, k):
    r"""
    Probability function of a Poisson distribution.

    Parameters
    ----------
    lambda: float, :math:`\lambda\geq 0`
        The intensity of the Poisson distribution
    k : int
        The number of success.

    Returns
    -------
    logp : float
        The natural logarithm of the probability to get :math:`k` successes.

    Notes
    -----
    This method implements Loader's algorithm, the *fast* and *accurate* method
    described in [loader2000]_, with the further improvements mentioned
    in [dimitriadis2016]_.

    Examples
    --------
    >>> import openturns as ot
    >>> p = ot.DistFunc.dPoisson(5.0, 2)
    """
    return _dist_bundle1.DistFunc_dPoisson(_lambda, k)


def DistFunc_qPoisson(_lambda, p, tail=False):
    return _dist_bundle1.DistFunc_qPoisson(_lambda, p, tail)


def DistFunc_rPoisson(*args):
    r"""
    Realization of a Poisson distribution.

    Parameters
    ----------
    lambda: float, :math:`\lambda\geq 0`
        The intensity of the Poisson distribution
    size : int
        The number of realizations to generate.

    Returns
    -------
    realizations : int or :class:`~openturns.Indices`
        The realizations of the discrete disctribution.

    Notes
    -----
    For the small values of :math:`\lambda`, we use the method of inversion by
    sequential search described in [devroye1986]_ and with the important errata in
    [devroye1986b]_. For the large values of :math:`\lambda`, we use the ratio of
    uniform method described in [stadlober1990]_.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> r = ot.DistFunc.rPoisson(5.0)
    >>> r = ot.DistFunc.rPoisson(5.0, 10)
    """
    return _dist_bundle1.DistFunc_rPoisson(*args)


def DistFunc_pPearsonCorrelation(size, rho, tail=False):
    r"""
    Asymptotic probability function for the Pearson :math:`\rho` correlation.

    Parameters
    ----------
    n : int
        The size of the population

    rho : float :math:`-1<rho<1`
        The Pearson correlation coefficient

    tail : bool
        Tells if we consider to be in the critical region (tTrue)
        Default value is False

    Returns
    -------
    pvalue : float
        The probability to be in the region of interest

    Notes
    -----
    This method allows to compute the *asymptotic* distribution of the
    `Pearson` correlation coefficient issued from two univariate samples
    of size `n`. Basically, we want to measure how coefficient is significatly
    different from `0`. If `tail` is True, the issued value measures probability
    to be in the critical region.

    Examples
    --------
    >>> import openturns as ot
    >>> pval = ot.DistFunc.pPearsonCorrelation(100, 0.3, True)
    """
    return _dist_bundle1.DistFunc_pPearsonCorrelation(size, rho, tail)


def DistFunc_pSpearmanCorrelation(size, rho, tail=False, ties=False):
    return _dist_bundle1.DistFunc_pSpearmanCorrelation(size, rho, tail, ties)


def DistFunc_pStudent(*args):
    return _dist_bundle1.DistFunc_pStudent(*args)


def DistFunc_qStudent(*args):
    return _dist_bundle1.DistFunc_qStudent(*args)


def DistFunc_rStudent(*args):
    return _dist_bundle1.DistFunc_rStudent(*args)


def DistFunc_rUniformTriangle(*args):
    return _dist_bundle1.DistFunc_rUniformTriangle(*args)


def DistFunc_eZ1(n):
    return _dist_bundle1.DistFunc_eZ1(n)


def DistFunc_kFactorPooled(n, m, p, alpha):
    r"""
    Exact margin factor for bilateral covering interval of pooled Normal populations.

    Parameters
    ----------
    n : int
        The size of the population

    m : int
        The size of the pool

    p : float :math:`0<p<1`
        The probability level of the covering interval

    alpha : float :math:`0<\alpha<1`
        The confidence level of the covering interval

    Returns
    -------
    k : float
        The margin factor

    Notes
    -----
    This method allows to compute the *exact* margin factor :math:`k` of a
    pool of :math:`m` Normal populations of size :math:`n` with unknown
    means :math:`\mu_i` and unknown common variance :math:`\sigma^2`.
    Let :math:`m_i=\dfrac{1}{n}\sum_{j=1}^nX_{ij}` be the empirical mean
    of the ith population :math:`(X_{i1},\dots,X_{in})` and
    :math:`\sigma^2_{mn}=\dfrac{}{}\sum_{i=1}^m\sum_{j=1}^n(X_{ij}-m_i)^2`
    the empirical *pooled* variance. The covering factor :math:`k` is such
    that the intervals :math:`[m_i-k\sigma_{mn},m_i+k\sigma_{mn}]` satisfy:

    .. math::
        \Prob{\Prob{X_i\in[m_i-k\sigma_{mn},m_i+k\sigma_{mn}]}\geq p}=\alpha

    for :math:`i\in\{1,\dots,m\}`. It reduces to find :math:`k` such that:

    .. math::
        \int_{\Rset}F(x,k;\nu_{m,n},p)\phi_{0,1/\sqrt{n}}(x)\,\di x = \alpha

    where :math:`phi_{0,1/\sqrt{n}}` is the density function of the normal
    distribution with a mean equals to 0 and a variance equals to
    :math:`1/n`, :math:`\nu_{m,n}=m(n-1)` and :math:`F(x,k;\nu_{m,n},p)`
    the function defined by:

    .. math::
        F(x,k;\nu_{m,n},p)=\bar{F}_{\chi^2_{\nu_{m,n}}}(\nu_{m,n} R^2(x;p)/k^2)

    where :math:`\bar{F}_{\chi^2_{\nu_{m,n}}}` is the complementary distribution
    function of a chi-square distribution with :math:`\nu_{m,n}` degrees
    of freedom and :math:`R(x;p)` the solution of:

    .. math::
        \Phi(x + R) - \Phi(x - R) = p

    Examples
    --------
    >>> import openturns as ot
    >>> k = ot.DistFunc.kFactorPooled(5, 3, 0.95, 0.9)
    """
    return _dist_bundle1.DistFunc_kFactorPooled(n, m, p, alpha)


def DistFunc_kFactor(n, p, alpha):
    r"""
    Exact margin factor for bilateral covering interval of a Normal population.

    Parameters
    ----------
    n : int
        The size of the population

    p : float :math:`0<p<1`
        The probability level of the covering interval

    alpha : float :math:`0<\alpha<1`
        The confidence level of the covering interval

    Returns
    -------
    k : float
        The margin factor

    Notes
    -----
    This method allows to compute the *exact* margin factor :math:`k` of a
    Normal population of size :math:`n` with unknown
    means :math:`\mu_i` and unknown common variance :math:`\sigma^2`. It
    is equivalent to the pooled version with :math:`m=1`.

    Examples
    --------
    >>> import openturns as ot
    >>> k = ot.DistFunc.kFactor(5, 0.95, 0.9)
    """
    return _dist_bundle1.DistFunc_kFactor(n, p, alpha)


def DistFunc_pDickeyFullerTrend(x, tail=False):
    return _dist_bundle1.DistFunc_pDickeyFullerTrend(x, tail)


def DistFunc_pDickeyFullerConstant(x, tail=False):
    return _dist_bundle1.DistFunc_pDickeyFullerConstant(x, tail)


def DistFunc_pDickeyFullerNoConstant(x, tail=False):
    return _dist_bundle1.DistFunc_pDickeyFullerNoConstant(x, tail)


def DistFunc_qDickeyFullerTrend(p, tail=False):
    return _dist_bundle1.DistFunc_qDickeyFullerTrend(p, tail)


def DistFunc_qDickeyFullerConstant(p, tail=False):
    return _dist_bundle1.DistFunc_qDickeyFullerConstant(p, tail)


def DistFunc_qDickeyFullerNoConstant(p, tail=False):
    return _dist_bundle1.DistFunc_qDickeyFullerNoConstant(p, tail)


class Arcsine(openturns.model_copula.ContinuousDistribution):
    r"""
    Arcsine distribution.

    Available constructors:
        Arcsine(*a=-1.0, b=1.0*)

    Parameters
    ----------
    a : float
        lower bound.
    b : float
        upper bound, :math:`b > a`

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        f_X(x) = \frac{1}{\pi \sqrt{(x - a)(b - x)}},
                 \quad x \in [a, b]

    with :math:`a < b`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & \frac{a + b}{2} \\
            \Var{X} & = & \frac{(b - a)^2}{8}
        \end{eqnarray*}

    It is possible to create an Arcsine distribution from the alternative parametrization :math:`(\mu, \sigma)`: see  :class:`~openturns.ArcsineMuSigma`. In that case, all the results are presented in that new parametrization.

    In order to use the alternative  parametrization :math:`(\mu, \sigma)` only to create the distribution, see the example below: all the results will be presented in the native parametrization :math:`(a, b)`

    Examples
    --------
    Create a distribution from its native parameters :math:`(a, b)`:

    >>> import openturns as ot
    >>> myDist = ot.Arcsine(2.0, 3.0)

    Create a it from the alternative parametrization :math:`(\mu, \sigma)`:

    >>> myDist2 = ot.Arcsine()
    >>> myDist2.setParameter(ot.ArcsineMuSigma()([2.5, 0.35]))

    Create it from :math:`(\mu, \sigma)` and keep that parametrization for the remaining study: 

    >>> myParam = ot.ArcsineMuSigma(2.5, 0.35)
    >>> myDist3 = ot.ParametrizedDistribution(myParam)

    Draw a sample:

    >>> sample = myDist.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Arcsine_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Arcsine___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Arcsine___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Arcsine___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Arcsine_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Arcsine_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Arcsine_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.Arcsine_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Arcsine_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.Arcsine_computeComplementaryCDF(self, *args)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.Arcsine_computeCharacteristicFunction(self, x)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Arcsine_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Arcsine_computeCDFGradient(self, *args)

    def computeScalarQuantile(self, prob, tail=False):
        r"""
        Compute the quantile function for univariate distributions.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : float
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_X(p) = F_X^{-1}(p), \quad p \in [0; 1]

        See Also
        --------
        computeQuantile
        """
        return _dist_bundle1.Arcsine_computeScalarQuantile(self, prob, tail)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Arcsine_computeEntropy(self)

    def getRoughness(self):
        r"""
        Accessor to roughness of the distribution.

        Returns
        -------
        r : float
            Roughness of the distribution.

        Notes
        -----
        The roughness of the distribution is defined as the :math:`\cL^2`-norm of its
        PDF:

        .. math::

            r = \int_{\supp{\vect{X}}} f_{\vect{X}}(\vect{x})^2 \di{\vect{x}}

        See Also
        --------
        computePDF
        """
        return _dist_bundle1.Arcsine_getRoughness(self)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Arcsine_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Arcsine_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Arcsine_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.Arcsine_getStandardMoment(self, n)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _dist_bundle1.Arcsine_getStandardRepresentative(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Arcsine_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Arcsine_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Arcsine_getParameterDescription(self)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _dist_bundle1.Arcsine_isElliptical(self)

    def setA(self, a):
        """
        Accessor to the distribution's lower bound.

        Parameters
        ----------
        a : float, :math:`a < b`
            Lower bound.
        """
        return _dist_bundle1.Arcsine_setA(self, a)

    def getA(self):
        """
        Accessor to the distribution's lower bound.

        Returns
        -------
        a : float
            Lower bound.
        """
        return _dist_bundle1.Arcsine_getA(self)

    def setB(self, b):
        """
        Accessor to the distribution's upper bound.

        Parameters
        ----------
        b : float, :math:`a < b`
            Upper bound.
        """
        return _dist_bundle1.Arcsine_setB(self, b)

    def getB(self):
        """
        Accessor to the distribution's upper bound.

        Returns
        -------
        b : float
            Upper bound.
        """
        return _dist_bundle1.Arcsine_getB(self)

    def __init__(self, *args):
        _dist_bundle1.Arcsine_swiginit(self, _dist_bundle1.new_Arcsine(*args))

    __swig_destroy__ = _dist_bundle1.delete_Arcsine


_dist_bundle1.Arcsine_swigregister(Arcsine)

class ArcsineFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Arcsine factory.

    Available constructor:
        ArcsineFactory()

    The parameters are estimated by method of moments:

    .. math::
        :nowrap:

        \begin{eqnarray*}
          \displaystyle \Hat{a} = \Hat{\mu}_x - \Hat{\sigma}_x \sqrt{2}\\
          \displaystyle \Hat{b} = \Hat{\mu}_x + \Hat{\sigma}_x \sqrt{2}
        \end{eqnarray*}

    See also
    --------
    DistributionFactory, Arcsine
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.ArcsineFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.ArcsineFactory_build(self, *args)

    def buildEstimator(self, *args):
        r"""
        Build the distribution and the parameter distribution.

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        parameters : :class:`~openturns.DistributionParameters`
            Optional, the parametrization.

        Returns
        -------
        resDist : :class:`~openturns.DistributionFactoryResult`
            The results.

        Notes
        -----
        According to the way the native parameters of the distribution are estimated, the parameters distribution differs:

            - Moments method: the asymptotic parameters distribution is normal and estimated by Bootstrap on the initial data;
            - Maximum likelihood method with a regular model: the asymptotic parameters distribution is normal and its covariance matrix is the inverse Fisher information matrix;
            - Other methods: the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting (see :class:`~openturns.KernelSmoothing`).

        If another set of parameters is specified, the native parameters distribution is first estimated and the new distribution is determined from it:

            - if the native parameters distribution is normal and the transformation regular at the estimated parameters values: the asymptotic parameters distribution is normal and its covariance matrix determined from the inverse Fisher information matrix of the native parameters and the transformation;
            - in the other cases, the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting.

        Examples
        --------
        Create a sample from a Beta distribution:

        >>> import openturns as ot
        >>> sample = ot.Beta().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Beta distribution in the native parameters and create a :class:`~openturns.DistributionFactory`:

        >>> fittedRes = ot.BetaFactory().buildEstimator(sample)

        Fit a Beta distribution  in the alternative parametrization :math:`(\mu, \sigma, a, b)`:

        >>> fittedRes2 = ot.BetaFactory().buildEstimator(sample, ot.BetaMuSigma())
        """
        return _dist_bundle1.ArcsineFactory_buildEstimator(self, *args)

    def buildAsArcsine(self, *args):
        return _dist_bundle1.ArcsineFactory_buildAsArcsine(self, *args)

    def __init__(self, *args):
        _dist_bundle1.ArcsineFactory_swiginit(self, _dist_bundle1.new_ArcsineFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_ArcsineFactory


_dist_bundle1.ArcsineFactory_swigregister(ArcsineFactory)

class ArcsineMuSigma(openturns.model_copula.DistributionParametersImplementation):
    r"""
    Arcsine distribution parameters.

    Available constructors:
        ArcsineMuSigma(*mu=1.0, sigma=1.0*)

    Parameters
    ----------
    mu : float
        Mean.
    sigma : float
        Standard deviation :math:`\sigma > 0`.

    Notes
    -----
    The native parameters are defined as follows:

    .. math::

        a &= \mu - \sigma \sqrt{2} \\
        b &= \mu + \sigma \sqrt{2}

    See also
    --------
    Arcsine

    Examples
    --------
    Create the parameters of the Arcsine distribution:

    >>> import openturns as ot
    >>> parameters = ot.ArcsineMuSigma(8.4, 2.25)

    Convert parameters into the native parameters:

    >>> print(parameters.evaluate())
    [5.21802,11.582]

    The gradient of the transformation of the native parameters into the new
    parameters:

    >>> print(parameters.gradient())
    [[  1        1       ]
     [ -1.41421  1.41421 ]]
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.ArcsineMuSigma_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.ArcsineMuSigma___eq__(self, other)

    def getDistribution(self):
        """
        Build a distribution based on a set of native parameters.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Distribution built with the native parameters.
        """
        return _dist_bundle1.ArcsineMuSigma_getDistribution(self)

    def gradient(self):
        r"""
        Get the gradient.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The gradient of the transformation of the native parameters into the new
            parameters.

        Notes
        -----

        If we note :math:`(p_1, \dots, p_q)` the native parameters and :math:`(p'_1, \dots, p'_q)` the new ones, then the gradient matrix is :math:`\left( \dfrac{\partial p'_i}{\partial p_j} \right)_{1 \leq i,j \leq  q}`.
        """
        return _dist_bundle1.ArcsineMuSigma_gradient(self)

    def __call__(self, inP):
        return _dist_bundle1.ArcsineMuSigma___call__(self, inP)

    def inverse(self, inP):
        """
        Convert to native parameters.

        Parameters
        ----------
        inP : sequence of float
            The non-native parameters.

        Returns
        -------
        outP : :class:`~openturns.Point`
            The native parameters.
        """
        return _dist_bundle1.ArcsineMuSigma_inverse(self, inP)

    def setValues(self, values):
        """
        Accessor to the parameters values.

        Parameters
        ----------
        values : sequence of float
            List of parameters values.
        """
        return _dist_bundle1.ArcsineMuSigma_setValues(self, values)

    def getValues(self):
        """
        Accessor to the parameters values.

        Returns
        -------
        values : :class:`~openturns.Point`
            List of parameters values.
        """
        return _dist_bundle1.ArcsineMuSigma_getValues(self)

    def getDescription(self):
        """
        Get the description of the parameters.

        Returns
        -------
        collection : :class:`~openturns.Description`
            List of parameters names.
        """
        return _dist_bundle1.ArcsineMuSigma_getDescription(self)

    def __repr__(self):
        return _dist_bundle1.ArcsineMuSigma___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.ArcsineMuSigma___str__(self, *args)

    def __init__(self, *args):
        _dist_bundle1.ArcsineMuSigma_swiginit(self, _dist_bundle1.new_ArcsineMuSigma(*args))

    __swig_destroy__ = _dist_bundle1.delete_ArcsineMuSigma


_dist_bundle1.ArcsineMuSigma_swigregister(ArcsineMuSigma)

class Bernoulli(openturns.model_copula.DiscreteDistribution):
    r"""
    Bernoulli distribution.

    Available constructors:
        Bernoulli(*p=0.5*)

    Parameters
    ----------
    p : float, :math:`0 \leq p \leq 1`
        Success probability.

    Notes
    -----
    Its probability density function is defined as:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Prob{X = 1} & = & p \\
            \Prob{X = 0} & = & 1 - p
        \end{eqnarray*}

    with :math:`0 \leq p \leq 1`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & p \\
            \Var{X} & = & p\,(1 - p)
        \end{eqnarray*}

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.Bernoulli(0.2)

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Bernoulli_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Bernoulli___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Bernoulli___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Bernoulli___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Bernoulli_getRealization(self)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Bernoulli_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Bernoulli_computeCDF(self, *args)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Bernoulli_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Bernoulli_computeCDFGradient(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Bernoulli_computeEntropy(self)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.Bernoulli_computeCharacteristicFunction(self, x)

    def computeGeneratingFunction(self, z):
        r"""
        Compute the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        g : float
            Probability-generating function value at input :math:`X`.

        Notes
        -----
        The probability-generating function is defined as follows:

        .. math::

            G_X(z) = \Expect{z^X}, \quad z \in \Cset

        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete
        """
        return _dist_bundle1.Bernoulli_computeGeneratingFunction(self, z)

    def getSupport(self, *args):
        r"""
        Accessor to the support of the distribution.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval to intersect with the support of the discrete part of the distribution.

        Returns
        -------
        support : :class:`~openturns.Interval`
            The intersection of the support of the discrete part of the distribution with the given `interval`.

        Notes
        -----
        The mathematical support :math:`\supp{\vect{X}}` of the discrete part of a distribution is the collection of points with nonzero probability.

        This is yet implemented for discrete distributions only.

        See Also
        --------
        getRange
        """
        return _dist_bundle1.Bernoulli_getSupport(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Bernoulli_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Bernoulli_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Bernoulli_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.Bernoulli_getStandardMoment(self, n)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Bernoulli_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Bernoulli_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Bernoulli_getParameterDescription(self)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _dist_bundle1.Bernoulli_isElliptical(self)

    def setP(self, p):
        r"""
        Accessor to the distribution's *success probability* parameter.

        Parameters
        ----------
        p : float, :math:`0 \leq p \leq 1`
            Success probability.
        """
        return _dist_bundle1.Bernoulli_setP(self, p)

    def getP(self):
        """
        Accessor to the distribution's *success probability* parameter.

        Returns
        -------
        p : float
            Success probability.
        """
        return _dist_bundle1.Bernoulli_getP(self)

    def __init__(self, *args):
        _dist_bundle1.Bernoulli_swiginit(self, _dist_bundle1.new_Bernoulli(*args))

    __swig_destroy__ = _dist_bundle1.delete_Bernoulli


_dist_bundle1.Bernoulli_swigregister(Bernoulli)

class BernoulliFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Bernoulli factory.

    Available constructor:
        BernoulliFactory()

    We use the following estimator:

    .. math::
        :nowrap:

        \begin{eqnarray*}
          \displaystyle\Hat{p}_n = \bar{x}_n
        \end{eqnarray*}

    See also
    --------
    DistributionFactory, Bernoulli
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.BernoulliFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.BernoulliFactory_build(self, *args)

    def buildAsBernoulli(self, *args):
        return _dist_bundle1.BernoulliFactory_buildAsBernoulli(self, *args)

    def buildEstimator(self, sample):
        r"""
        Build the distribution and the parameter distribution.

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        parameters : :class:`~openturns.DistributionParameters`
            Optional, the parametrization.

        Returns
        -------
        resDist : :class:`~openturns.DistributionFactoryResult`
            The results.

        Notes
        -----
        According to the way the native parameters of the distribution are estimated, the parameters distribution differs:

            - Moments method: the asymptotic parameters distribution is normal and estimated by Bootstrap on the initial data;
            - Maximum likelihood method with a regular model: the asymptotic parameters distribution is normal and its covariance matrix is the inverse Fisher information matrix;
            - Other methods: the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting (see :class:`~openturns.KernelSmoothing`).

        If another set of parameters is specified, the native parameters distribution is first estimated and the new distribution is determined from it:

            - if the native parameters distribution is normal and the transformation regular at the estimated parameters values: the asymptotic parameters distribution is normal and its covariance matrix determined from the inverse Fisher information matrix of the native parameters and the transformation;
            - in the other cases, the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting.

        Examples
        --------
        Create a sample from a Beta distribution:

        >>> import openturns as ot
        >>> sample = ot.Beta().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Beta distribution in the native parameters and create a :class:`~openturns.DistributionFactory`:

        >>> fittedRes = ot.BetaFactory().buildEstimator(sample)

        Fit a Beta distribution  in the alternative parametrization :math:`(\mu, \sigma, a, b)`:

        >>> fittedRes2 = ot.BetaFactory().buildEstimator(sample, ot.BetaMuSigma())
        """
        return _dist_bundle1.BernoulliFactory_buildEstimator(self, sample)

    def __init__(self, *args):
        _dist_bundle1.BernoulliFactory_swiginit(self, _dist_bundle1.new_BernoulliFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_BernoulliFactory


_dist_bundle1.BernoulliFactory_swigregister(BernoulliFactory)

class EmpiricalBernsteinCopula(openturns.model_copula.ContinuousDistribution):
    r"""
    EmpiricalBernstein copula.

    Parameters
    ----------
    sample : :class:`~openturns.Sample`
        The sample of size :math:`N>0` and dimension :math:`d` from which the empirical copula sample is extracted. Default is *sample=[[0.0]]*.
    binNumber : int, :math:`0<binNumber\leq N`
        The number of cells into which each dimension of the unit cube :math:`[0, 1]^d` is divided to cluster the empirical copula sample. Default is *binNumber=1*.
    isCopulaSample : bool
        Flag to tell if the given sample is already an empirical copula sample. Default is *isCopulaSample=False*.

    Notes
    -----
    The empirical Bernstein copula is a copula based on the Bernstein approximation built upon a clustering of the empirical copula. It is defined by:

    .. math::

        C(\vect{u}) = \dfrac{1}{N}\sum_{i=1}^N\prod_{j=1}^d I_{r_j^i,s_j^i}(u_j)

    for :math:`\vect{u}\in[0,1]^d`, where :math:`r_j^i=\lceil binNumber U_j^i \rceil`, :math:`binNumber - r_j^i + 1`, :math:`(\vect{U}_i)_{i=1,\dots,N}` is the empirical copula sample associated to *sample* and :math:`I_{a,b}(x)` is the value of the regularized incomplete beta function of parameters :math:`a` and :math:`b` at :math:`x`, see :class:`~openturns.SpecFunc`.

    This construction leads to an actual copula if and only if :math:`N` is a multiple of :math:`binNumber`. If it is not the case, the last points of the sample are droped in order to fulfill this condition.

    See also
    --------
    BernsteincopulaFactory

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> copula = ot.EmpiricalBernsteinCopula(ot.Normal(2).getSample(10), 2, False)

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.EmpiricalBernsteinCopula___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.EmpiricalBernsteinCopula___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.EmpiricalBernsteinCopula___str__(self, *args)

    def setCopulaSample(self, copulaSample, isEmpiricalCopulaSample=False):
        """
        Set the sample of the copula.

        Parameters
        ----------
        sample : 2-d sequence of float
            The sample from which the empirical copula sample is deduced.
        isEmpiricalCopulaSample : bool
            Flag telling if the given sample is already an empirical copula sample. The default value is *False*.
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_setCopulaSample(self, copulaSample, isEmpiricalCopulaSample)

    def getCopulaSample(self):
        """
        Get the empirical copula sample.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            The empirical copula sample of the copula.
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_getCopulaSample(self)

    def setBinNumber(self, binNumber):
        """
        Set the bin number of the copula.

        Parameters
        ----------
        binNumber : int
            The bin number of the copula. It must be positive and not greater than the copula sample size.
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_setBinNumber(self, binNumber)

    def getBinNumber(self):
        """
        Get the bin number of the copula.

        Returns
        -------
        binNumber : int
            The bin number of the copula.
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_getBinNumber(self)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_getRealization(self)

    def getSample(self, size):
        """
        Accessor to a pseudo-random sample from the distribution.

        Parameters
        ----------
        size : int
            Sample size.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            A pseudo-random sample of the distribution.

        See Also
        --------
        getRealization, RandomGenerator
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_getSample(self, size)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_computeCDF(self, *args)

    def computeProbability(self, interval):
        r"""
        Compute the interval probability.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval, possibly multivariate.

        Returns
        -------
        P : float
            Interval probability.

        Notes
        -----
        This computes the probability that the random vector :math:`\vect{X}` lies in
        the hyper-rectangular region formed by the vectors :math:`\vect{a}` and
        :math:`\vect{b}`:

        .. math::

            \Prob{\bigcap\limits_{i=1}^n a_i < X_i \leq b_i} =
                \sum\limits_{\vect{c}} (-1)^{n(\vect{c})}
                    F_{\vect{X}}\left(\vect{c}\right)

        where the sum runs over the :math:`2^n` vectors such that
        :math:`\vect{c} = \Tr{(c_i, i = 1, \ldots, n)}` with :math:`c_i \in [a_i, b_i]`,
        and :math:`n(\vect{c})` is the number of components in
        :math:`\vect{c}` such that :math:`c_i = a_i`.
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_computeProbability(self, interval)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_getMarginal(self, *args)

    def getSpearmanCorrelation(self):
        r"""
        Accessor to the Spearman correlation matrix.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Spearman's correlation matrix.

        Notes
        -----
        Spearman's (rank) correlation is defined as the normalized covariance matrix
        of the copula (ie that of the uniform margins):

        .. math::

            \mat{\rho_S} = \left[\frac{\Cov{F_{X_i}(X_i), F_{X_j}(X_j)}}
                                      {\sqrt{\Var{F_{X_i}(X_i)} \Var{F_{X_j}(X_j)}}},
                                 \quad i,j = 1, \ldots, n\right]

        See Also
        --------
        getKendallTau
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_getSpearmanCorrelation(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_hasEllipticalCopula(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_hasIndependentCopula(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.EmpiricalBernsteinCopula_getParameter(self)

    def __init__(self, *args):
        _dist_bundle1.EmpiricalBernsteinCopula_swiginit(self, _dist_bundle1.new_EmpiricalBernsteinCopula(*args))

    __swig_destroy__ = _dist_bundle1.delete_EmpiricalBernsteinCopula


_dist_bundle1.EmpiricalBernsteinCopula_swigregister(EmpiricalBernsteinCopula)

class BernsteinCopulaFactory(openturns.model_copula.DistributionFactoryImplementation):
    """
    BernsteinCopula copula factory.

    This class allows to estimate a copula in a nonparametric way as an :class:`~openturns.EmpiricalBernsteinCopula`.

    See also
    --------
    DistributionFactory, EmpiricalBernsteinCopula
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.BernsteinCopulaFactory_getClassName(self)

    def build(self, *args):
        """
        Build the nonparametric Bernstein copula estimator based on the empirical copula.

        **Available usages**:

            build()

            build(*sample*)

            build(*sample, method, objective*)

            build(*sample, m*)

        Parameters
        ----------
        sample : 2-d sequence of float, of dimension *d*
            The sample of size :math:`n>0` from which the copula is estimated.
        method : str
            The name of thebin number selection method. Possible choices are *AMISE*, *LogLikelihood* and *PenalizedCsiszarDivergence*. Default is *LogLikelihood*, given by the *'BernsteinCopulaFactory-BinNumberSelection'* entry of :class:`~openturns.ResourceMap`.
        m : int
            The number of sub-intervals in which all the edges of the unit cube
            :math:`[0, 1]^d` are regularly partitioned.

        Returns
        -------
        copula : :class:`~openturns.Distribution`
            The estimated copula as a generic distribution.

        """
        return _dist_bundle1.BernsteinCopulaFactory_build(self, *args)

    def buildAsEmpiricalBernsteinCopula(self, *args):
        """
        Build the nonparametric Bernstein copula estimator based on the empirical copula.

        **Available usages**:

            buildAsEmpiricalBernsteinCopula()

            buildAsEmpiricalBernsteinCopula(*sample*)

            buildAsEmpiricalBernsteinCopula(*sample, method, objective*)

            buildAsEmpiricalBernsteinCopula(*sample, m*)

        Parameters
        ----------
        sample : 2-d sequence of float, of dimension *d*
            The sample of size :math:`n>0` from which the copula is estimated.
        method : str
            The name of thebin number selection method. Possible choices are *AMISE*, *LogLikelihood* and *PenalizedCsiszarDivergence*. Default is *LogLikelihood*, given by the *'BernsteinCopulaFactory-BinNumberSelection'* entry of :class:`~openturns.ResourceMap`.
        m : int
            The number of sub-intervals in which all the edges of the unit cube
            :math:`[0, 1]^d` are regularly partitioned.

        Returns
        -------
        copula : :class:`~openturns.EmpiricalBernsteinCopula`
            The estimated copula as an empirical Bernstein copula.

        """
        return _dist_bundle1.BernsteinCopulaFactory_buildAsEmpiricalBernsteinCopula(self, *args)

    @staticmethod
    def ComputeAMISEBinNumber(sample):
        r"""
        Compute the optimal AMISE number of bins.

        Parameters
        ----------
        sample : 2-d sequence of float, of dimension 1
            The sample from which the optimal AMISE bin number is computed.

        Notes
        -----
        The number of bins is computed by minimizing the asymptotic mean integrated squared error (AMISE), leading to

        .. math::

            m = 1+\left\lfloor n^{\dfrac{2}{4+d}} \right\rfloor

        where :math:`\lfloor x \rfloor` is the largest integer less than or equal to :math:`x`, :math:`n` the sample size and :math:`d` the sample dimension.

        """
        return _dist_bundle1.BernsteinCopulaFactory_ComputeAMISEBinNumber(sample)

    @staticmethod
    def ComputeLogLikelihoodBinNumber(*args):
        r"""
        Compute the optimal log-likelihood number of bins by cross-validation.

        Parameters
        ----------
        sample : 2-d sequence of float, of dimension 1
            The sample of size :math:`n` from which the optimal log-likelihood bin number is computed.
        kFraction : int, :math:`0<kFraction<n`
            The fraction of the sample used for the validation.

        Notes
        -----
        Let :math:`\cE=\left\{\vect{X}_1,\dots,\vect{X}_n\right\}` be the given sample. If :math:`kFraction=1`, the bin number :math:`m` is given by:

        .. math::

            m = \argmin_{M\in\{1,\dots,n\}}\dfrac{1}{n}\sum_{\vect{X}_i\in\cE}-\log c^{\cE}_{M}(\vect{X}_i)

        where :math:`c_M^{\cE}` is the density function of the :class:`~openturns.EmpiricalBernsteinCopula` associated to the sample :math:`\cE` and the bin number :math:`M`.

        If :math:`kFraction>1`, the bin number :math:`m` is given by:

        .. math::

            m = \argmin_{M\in\{1,\dots,n\}}\dfrac{1}{kFraction}\sum_{k=0}^{kFraction-1}\dfrac{1}{n}\sum_{\vect{X}_i\in\cE^V_k}-\log c^{\cE^L_k}_{M}(\vect{X}_i)

        where :math:`\cE^V_k=\left\{\vect{X}_i\in\cE\,|\,i\equiv k \mod kFraction\right\}` and :math:`\cE^L_k=\cE \backslash \cE^V_k`

        """
        return _dist_bundle1.BernsteinCopulaFactory_ComputeLogLikelihoodBinNumber(*args)

    @staticmethod
    def ComputePenalizedCsiszarDivergenceBinNumber(*args):
        r"""
        Compute the optimal penalized Csiszar divergence number of bins.

        Parameters
        ----------
        sample : 2-d sequence of float, of dimension 1
            The sample of size :math:`n` from which the optimal AMISE bin number is computed.
        f : :class:`~openturns.Function`
            The function defining the Csiszar divergence of interest.
        alpha : float, :math:`\alpha\geq 0`
            The penalization factor.

        Notes
        -----
        Let :math:`\cE=\left\{\vect{X}_1,\dots,\vect{X}_n\right\}` be the given sample. The bin number :math:`m` is given by:

        .. math::

            m = \argmin_{M\in\{1,\dots,n\}}\left[\hat{D}_f(c^{\cE}_{M})-\dfrac{1}{n}\sum_{\vect{X}_i\in\cE}f\left(\dfrac{1}{c^{\cE}_{M}(\vect{X}_i)}\right)\right]^2-[\rho_S(c^{\cE}_{M})-\rho_S({\cE}_{M})]^2

        where :math:`c_M^{\cE}` is the density function of the :class:`~openturns.EmpiricalBernsteinCopula` associated to the sample :math:`\cE` and the bin number :math:`M`, :math:`\hat{D}_f(c^{\cE}_{M})=\dfrac{1}{N}\sum_{j=1}^Nf\left(\dfrac{1}{\vect{U}_j}\right)` a Monte Carlo estimate of the Csiszar :math:`f` divergence, :math:`\rho_S(c^{\cE}_{M})` the exact Spearman correlation of the empirical Bernstein copula :math:`c^{\cE}_{M}` and :math:`\rho_S({\cE}_{M})` the empirical Spearman correlation of the sample :math:`{\cE}_{M}`.

        The parameter :math:`N` is controlled by the *'BernsteinCopulaFactory-SamplingSize'* key in :class:`~openturns.ResourceMap`.

        """
        return _dist_bundle1.BernsteinCopulaFactory_ComputePenalizedCsiszarDivergenceBinNumber(*args)

    @staticmethod
    def BuildCrossValidationSamples(sample, kFraction, learningCollection, validationCollection):
        return _dist_bundle1.BernsteinCopulaFactory_BuildCrossValidationSamples(sample, kFraction, learningCollection, validationCollection)

    def __init__(self, *args):
        _dist_bundle1.BernsteinCopulaFactory_swiginit(self, _dist_bundle1.new_BernsteinCopulaFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_BernsteinCopulaFactory


_dist_bundle1.BernsteinCopulaFactory_swigregister(BernsteinCopulaFactory)

def BernsteinCopulaFactory_ComputeAMISEBinNumber(sample):
    r"""
    Compute the optimal AMISE number of bins.

    Parameters
    ----------
    sample : 2-d sequence of float, of dimension 1
        The sample from which the optimal AMISE bin number is computed.

    Notes
    -----
    The number of bins is computed by minimizing the asymptotic mean integrated squared error (AMISE), leading to

    .. math::

        m = 1+\left\lfloor n^{\dfrac{2}{4+d}} \right\rfloor

    where :math:`\lfloor x \rfloor` is the largest integer less than or equal to :math:`x`, :math:`n` the sample size and :math:`d` the sample dimension.

    """
    return _dist_bundle1.BernsteinCopulaFactory_ComputeAMISEBinNumber(sample)


def BernsteinCopulaFactory_ComputeLogLikelihoodBinNumber(*args):
    r"""
    Compute the optimal log-likelihood number of bins by cross-validation.

    Parameters
    ----------
    sample : 2-d sequence of float, of dimension 1
        The sample of size :math:`n` from which the optimal log-likelihood bin number is computed.
    kFraction : int, :math:`0<kFraction<n`
        The fraction of the sample used for the validation.

    Notes
    -----
    Let :math:`\cE=\left\{\vect{X}_1,\dots,\vect{X}_n\right\}` be the given sample. If :math:`kFraction=1`, the bin number :math:`m` is given by:

    .. math::

        m = \argmin_{M\in\{1,\dots,n\}}\dfrac{1}{n}\sum_{\vect{X}_i\in\cE}-\log c^{\cE}_{M}(\vect{X}_i)

    where :math:`c_M^{\cE}` is the density function of the :class:`~openturns.EmpiricalBernsteinCopula` associated to the sample :math:`\cE` and the bin number :math:`M`.

    If :math:`kFraction>1`, the bin number :math:`m` is given by:

    .. math::

        m = \argmin_{M\in\{1,\dots,n\}}\dfrac{1}{kFraction}\sum_{k=0}^{kFraction-1}\dfrac{1}{n}\sum_{\vect{X}_i\in\cE^V_k}-\log c^{\cE^L_k}_{M}(\vect{X}_i)

    where :math:`\cE^V_k=\left\{\vect{X}_i\in\cE\,|\,i\equiv k \mod kFraction\right\}` and :math:`\cE^L_k=\cE \backslash \cE^V_k`

    """
    return _dist_bundle1.BernsteinCopulaFactory_ComputeLogLikelihoodBinNumber(*args)


def BernsteinCopulaFactory_ComputePenalizedCsiszarDivergenceBinNumber(*args):
    r"""
    Compute the optimal penalized Csiszar divergence number of bins.

    Parameters
    ----------
    sample : 2-d sequence of float, of dimension 1
        The sample of size :math:`n` from which the optimal AMISE bin number is computed.
    f : :class:`~openturns.Function`
        The function defining the Csiszar divergence of interest.
    alpha : float, :math:`\alpha\geq 0`
        The penalization factor.

    Notes
    -----
    Let :math:`\cE=\left\{\vect{X}_1,\dots,\vect{X}_n\right\}` be the given sample. The bin number :math:`m` is given by:

    .. math::

        m = \argmin_{M\in\{1,\dots,n\}}\left[\hat{D}_f(c^{\cE}_{M})-\dfrac{1}{n}\sum_{\vect{X}_i\in\cE}f\left(\dfrac{1}{c^{\cE}_{M}(\vect{X}_i)}\right)\right]^2-[\rho_S(c^{\cE}_{M})-\rho_S({\cE}_{M})]^2

    where :math:`c_M^{\cE}` is the density function of the :class:`~openturns.EmpiricalBernsteinCopula` associated to the sample :math:`\cE` and the bin number :math:`M`, :math:`\hat{D}_f(c^{\cE}_{M})=\dfrac{1}{N}\sum_{j=1}^Nf\left(\dfrac{1}{\vect{U}_j}\right)` a Monte Carlo estimate of the Csiszar :math:`f` divergence, :math:`\rho_S(c^{\cE}_{M})` the exact Spearman correlation of the empirical Bernstein copula :math:`c^{\cE}_{M}` and :math:`\rho_S({\cE}_{M})` the empirical Spearman correlation of the sample :math:`{\cE}_{M}`.

    The parameter :math:`N` is controlled by the *'BernsteinCopulaFactory-SamplingSize'* key in :class:`~openturns.ResourceMap`.

    """
    return _dist_bundle1.BernsteinCopulaFactory_ComputePenalizedCsiszarDivergenceBinNumber(*args)


def BernsteinCopulaFactory_BuildCrossValidationSamples(sample, kFraction, learningCollection, validationCollection):
    return _dist_bundle1.BernsteinCopulaFactory_BuildCrossValidationSamples(sample, kFraction, learningCollection, validationCollection)


class Beta(openturns.model_copula.ContinuousDistribution):
    r"""
    Beta distribution.

    Parameters
    ----------
    alpha : float
        Shape parameter :math:`\alpha > 0`
    beta : float
        Shape parameter :math:`\beta > 0`
    a : float
        Lower bound
    b : float, :math:`b > a`
        Upper bound

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        f_X(x) = \frac{(x - a)^{\alpha - 1} (b - x)^{\beta - 1}}
                      {(b - a)^{\alpha + \beta - 1} {\rm B}(\alpha, \beta)},
                      \quad x \in [a, b]

    with :math:`\alpha, \beta > 0` and :math:`a < b` and where :math:`\rm B` denotes
    Euler's beta function :class:`~openturns.SpecFunc_Beta`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & a + (b - a)\frac{\alpha}{\alpha + \beta} \\
            \Var{X} & = & (b - a)^2 \frac{\alpha \beta}{(\alpha + \beta)^2(\alpha + \beta + 1)}
        \end{eqnarray*}

    It is possible to create a Beta distribution from the alternative parametrization :math:`(\mu, \sigma, a, b)`: see  :class:`~openturns.BetaMuSigma`. In that case, all the results are presented in that new parametrization.

    In order to use the alternative  parametrization :math:`(\mu, \sigma, a, b)` only to create the distribution, see the example below: all the results will be presented in the native parametrization :math:`(\alpha, \beta, a, b)`.

    Examples
    --------
    Create a distribution from its native parameters :math:`(\alpha, \beta, a, b)`:

    >>> import openturns as ot
    >>> myDist = ot.Beta(1.0, 2.0, 1.0, 5.0)

    Create it from the alternative parametrization :math:`(\mu, \sigma, a, b)`:

    >>> myDist2 = ot.Beta()
    >>> myDist2.setParameter(ot.BetaMuSigma()([3.0, 1.15, 1.0, 5.0]))

    Create it from :math:`(\mu, \sigma, a, b)` and keep that parametrization for the remaining study: 

    >>> myParam = ot.BetaMuSigma(3.0, 1.15, 1.0, 5.0)
    >>> myDist3 = ot.ParametrizedDistribution(myParam)

    Draw a sample:

    >>> sample = myDist.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Beta_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Beta___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Beta___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Beta___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Beta_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Beta_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Beta_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.Beta_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Beta_computeCDF(self, *args)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Beta_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Beta_computeCDFGradient(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Beta_computeEntropy(self)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.Beta_computeCharacteristicFunction(self, x)

    def getRoughness(self):
        r"""
        Accessor to roughness of the distribution.

        Returns
        -------
        r : float
            Roughness of the distribution.

        Notes
        -----
        The roughness of the distribution is defined as the :math:`\cL^2`-norm of its
        PDF:

        .. math::

            r = \int_{\supp{\vect{X}}} f_{\vect{X}}(\vect{x})^2 \di{\vect{x}}

        See Also
        --------
        computePDF
        """
        return _dist_bundle1.Beta_getRoughness(self)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Beta_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Beta_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Beta_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.Beta_getStandardMoment(self, n)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _dist_bundle1.Beta_getStandardRepresentative(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Beta_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Beta_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Beta_getParameterDescription(self)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _dist_bundle1.Beta_isElliptical(self)

    def setAlpha(self, alpha):
        r"""
        Accessor to the distribution's shape parameter :math:`\alpha`.

        Parameters
        ----------
        alpha : float, :math:`\alpha > 0`
            Shape parameter :math:`\alpha`.
        """
        return _dist_bundle1.Beta_setAlpha(self, alpha)

    def getAlpha(self):
        r"""
        Accessor to the distribution's shape parameter :math:`\alpha`.

        Returns
        -------
        alpha : float
            Shape parameter :math:`\alpha`.
        """
        return _dist_bundle1.Beta_getAlpha(self)

    def setBeta(self, beta):
        r"""
        Accessor to the distribution's shape parameter :math:`\beta`.

        Parameters
        ----------
        beta : float, :math:`\beta > 0`
            Shape parameter :math:`\beta`.
        """
        return _dist_bundle1.Beta_setBeta(self, beta)

    def getBeta(self):
        r"""
        Accessor to the distribution's shape parameter :math:`\beta`.

        Returns
        -------
        beta : float
            Shape parameter :math:`\beta`.
        """
        return _dist_bundle1.Beta_getBeta(self)

    def setR(self, r):
        return _dist_bundle1.Beta_setR(self, r)

    def getR(self):
        return _dist_bundle1.Beta_getR(self)

    def setT(self, t):
        return _dist_bundle1.Beta_setT(self, t)

    def getT(self):
        return _dist_bundle1.Beta_getT(self)

    def setA(self, a):
        """
        Accessor to the distribution's lower bound.

        Parameters
        ----------
        a : float, :math:`a < b`
            Lower bound.
        """
        return _dist_bundle1.Beta_setA(self, a)

    def getA(self):
        """
        Accessor to the distribution's lower bound.

        Returns
        -------
        a : float
            Lower bound.
        """
        return _dist_bundle1.Beta_getA(self)

    def setB(self, b):
        """
        Accessor to the distribution's upper bound.

        Parameters
        ----------
        b : float, :math:`b > a`
            Upper bound.
        """
        return _dist_bundle1.Beta_setB(self, b)

    def getB(self):
        """
        Accessor to the distribution's upper bound.

        Returns
        -------
        b : float
            Upper bound.
        """
        return _dist_bundle1.Beta_getB(self)

    def __init__(self, *args):
        _dist_bundle1.Beta_swiginit(self, _dist_bundle1.new_Beta(*args))

    __swig_destroy__ = _dist_bundle1.delete_Beta


_dist_bundle1.Beta_swigregister(Beta)

class BetaFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Beta factory.

    Available constructor:
        BetaFactory()

    The parameters are estimated by method of moments:

    .. math::
        :nowrap:

        \begin{eqnarray*}
          \displaystyle\Hat{a}_n=(1-\mathrm{sign}(x_{(1,n)})/(2+n))x_{(1,n)}\\
          \displaystyle\Hat{b}_n=(1+\mathrm{sign}(x_{(n,n)})/(2+n))x_{(n,n)}\\
          \displaystyle\Hat{t}_n=\frac{(\Hat{b}_n-\bar{x}_n)(\bar{x}_n-\Hat{a}_n)}{(\sigma_n^X)^2-1}\\
          \displaystyle\Hat{r}_n=\frac{t(\bar{x}_n-\Hat{a}_n)}{\Hat{b}_n-\Hat{a}_n}
        \end{eqnarray*}

    See also
    --------
    DistributionFactory, Beta
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.BetaFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.BetaFactory_build(self, *args)

    def buildAsBeta(self, *args):
        return _dist_bundle1.BetaFactory_buildAsBeta(self, *args)

    def __init__(self, *args):
        _dist_bundle1.BetaFactory_swiginit(self, _dist_bundle1.new_BetaFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_BetaFactory


_dist_bundle1.BetaFactory_swigregister(BetaFactory)

class BetaMuSigma(openturns.model_copula.DistributionParametersImplementation):
    r"""
    Beta distribution parameters.

    Parameters
    ----------
    mu : float
        Mean.
    sigma : float
        Standard deviation :math:`\sigma > 0`.
    a : float
        Lower bound.
    b : float, :math:`b > a`
        Upper bound.

    Notes
    -----
    The native parameters  :math:`(\alpha, \beta, a, b)` are defined as follows:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \alpha & = & \left(\dfrac{\mu-a}{b-a}\right) \left( \dfrac{(b-\mu)(\mu-a)}{\sigma^2}-1\right) \\
            \beta & = &  \left( \dfrac{b-\mu}{\mu-a}\right) \alpha
        \end{eqnarray*}

    See also
    --------
    Beta

    Examples
    --------
    Create the parameters  :math:`(\mu, \sigma, a, b)` of the Beta distribution:

    >>> import openturns as ot
    >>> parameters = ot.BetaMuSigma(0.2, 0.6, -1, 2)

    Convert parameters into the native parameters :math:`(\alpha, \beta, a, b)`:

    >>> print(parameters.evaluate())
    [2,3,-1,2]
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.BetaMuSigma_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.BetaMuSigma___eq__(self, other)

    def getDistribution(self):
        """
        Build a distribution based on a set of native parameters.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Distribution built with the native parameters.
        """
        return _dist_bundle1.BetaMuSigma_getDistribution(self)

    def gradient(self):
        r"""
        Get the gradient.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The gradient of the transformation of the native parameters into the new
            parameters.

        Notes
        -----

        If we note :math:`(p_1, \dots, p_q)` the native parameters and :math:`(p'_1, \dots, p'_q)` the new ones, then the gradient matrix is :math:`\left( \dfrac{\partial p'_i}{\partial p_j} \right)_{1 \leq i,j \leq  q}`.
        """
        return _dist_bundle1.BetaMuSigma_gradient(self)

    def __call__(self, inP):
        return _dist_bundle1.BetaMuSigma___call__(self, inP)

    def inverse(self, inP):
        """
        Convert to native parameters.

        Parameters
        ----------
        inP : sequence of float
            The non-native parameters.

        Returns
        -------
        outP : :class:`~openturns.Point`
            The native parameters.
        """
        return _dist_bundle1.BetaMuSigma_inverse(self, inP)

    def setValues(self, values):
        """
        Accessor to the parameters values.

        Parameters
        ----------
        values : sequence of float
            List of parameters values.
        """
        return _dist_bundle1.BetaMuSigma_setValues(self, values)

    def getValues(self):
        """
        Accessor to the parameters values.

        Returns
        -------
        values : :class:`~openturns.Point`
            List of parameters values.
        """
        return _dist_bundle1.BetaMuSigma_getValues(self)

    def getDescription(self):
        """
        Get the description of the parameters.

        Returns
        -------
        collection : :class:`~openturns.Description`
            List of parameters names.
        """
        return _dist_bundle1.BetaMuSigma_getDescription(self)

    def isElliptical(self):
        return _dist_bundle1.BetaMuSigma_isElliptical(self)

    def __repr__(self):
        return _dist_bundle1.BetaMuSigma___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.BetaMuSigma___str__(self, *args)

    def __init__(self, *args):
        _dist_bundle1.BetaMuSigma_swiginit(self, _dist_bundle1.new_BetaMuSigma(*args))

    __swig_destroy__ = _dist_bundle1.delete_BetaMuSigma


_dist_bundle1.BetaMuSigma_swigregister(BetaMuSigma)

class Binomial(openturns.model_copula.DiscreteDistribution):
    r"""
    Binomial distribution.

    Available constructors:
        Binomial(*n=1, p=0.5*)

    Parameters
    ----------
    n : int, :math:`n \in \Nset`
        The number of Bernoulli trials.
    p : float, :math:`0 \leq p \leq 1`
        The success probability of the Bernoulli trial.

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        \Prob{X = k} = C_n^k p^k (1-p)^{n-k},
                       \quad \forall k \in \{0, \ldots, n\}

    with :math:`n \in \Nset` and :math:`0 \leq p \leq 1`. It is evaluated using  Loader's algorithm, the *fast* and *accurate* method described in [loader2000]_, with the further improvements mentioned in [dimitriadis2016]_, see :class:`~openturns.DistFunc.dBinomial`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & n\,p \\
            \Var{X} & = & n\,p\,(1-p)
        \end{eqnarray*}

    The sampling is done using the rejection algorithm described in [hormann1993]_, see :class:`~openturns.DistFunc.rBinomial`.

    See Also
    --------
    Bernoulli

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.Binomial(10, 0.5)

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Binomial_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Binomial___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Binomial___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Binomial___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Binomial_getRealization(self)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Binomial_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.Binomial_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Binomial_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.Binomial_computeComplementaryCDF(self, *args)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Binomial_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Binomial_computeCDFGradient(self, *args)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.Binomial_computeCharacteristicFunction(self, x)

    def computeLogCharacteristicFunction(self, x):
        """
        Compute the logarithm of the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Logarithm of the characteristic function value at input :math:`t`.

        Notes
        -----
        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.

        See Also
        --------
        computeCharacteristicFunction
        """
        return _dist_bundle1.Binomial_computeLogCharacteristicFunction(self, x)

    def computeGeneratingFunction(self, z):
        r"""
        Compute the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        g : float
            Probability-generating function value at input :math:`X`.

        Notes
        -----
        The probability-generating function is defined as follows:

        .. math::

            G_X(z) = \Expect{z^X}, \quad z \in \Cset

        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete
        """
        return _dist_bundle1.Binomial_computeGeneratingFunction(self, z)

    def computeLogGeneratingFunction(self, z):
        """
        Compute the logarithm of the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        lg : float
            Logarithm of the probability-generating function value at input :math:`X`.

        Notes
        -----
        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete, computeGeneratingFunction
        """
        return _dist_bundle1.Binomial_computeLogGeneratingFunction(self, z)

    def getSupport(self, *args):
        r"""
        Accessor to the support of the distribution.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval to intersect with the support of the discrete part of the distribution.

        Returns
        -------
        support : :class:`~openturns.Interval`
            The intersection of the support of the discrete part of the distribution with the given `interval`.

        Notes
        -----
        The mathematical support :math:`\supp{\vect{X}}` of the discrete part of a distribution is the collection of points with nonzero probability.

        This is yet implemented for discrete distributions only.

        See Also
        --------
        getRange
        """
        return _dist_bundle1.Binomial_getSupport(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Binomial_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Binomial_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Binomial_getKurtosis(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Binomial_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Binomial_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Binomial_getParameterDescription(self)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _dist_bundle1.Binomial_isElliptical(self)

    def setP(self, p):
        r"""
        Accessor to the success probability parameter.

        Parameters
        ----------
        p : float, :math:`0 \leq p \leq 1`
            The success probability of the Bernoulli trial.
        """
        return _dist_bundle1.Binomial_setP(self, p)

    def getP(self):
        """
        Accessor to the success probability parameter.

        Returns
        -------
        p : float
            The success probability of the Bernoulli trial.
        """
        return _dist_bundle1.Binomial_getP(self)

    def setN(self, n):
        r"""
        Accessor to the number of trials.

        Parameters
        ----------
        n : int, :math:`n \in \Nset`
            The number of Bernoulli trials.
        """
        return _dist_bundle1.Binomial_setN(self, n)

    def getN(self):
        """
        Accessor to the number of trials.

        Returns
        -------
        n : int
            The number of Bernoulli trials.
        """
        return _dist_bundle1.Binomial_getN(self)

    def __init__(self, *args):
        _dist_bundle1.Binomial_swiginit(self, _dist_bundle1.new_Binomial(*args))

    __swig_destroy__ = _dist_bundle1.delete_Binomial


_dist_bundle1.Binomial_swigregister(Binomial)

class BinomialFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Binomial factory.

    Available constructor:
        BinomialFactory()

    Notes
    -----
    The estimation is done by maximizing the likelihood of the sample.

    | We initialize the value of :math:`(n,p_n)` to
      :math:`\displaystyle\left(\left\lceil\frac{\Hat{x}_n^2}{\Hat{x}_n-\Hat{\sigma}_n^2}\right\rceil, \frac{\Hat{x}_n}{n}\right)`
      where :math:`\Hat{x}_n` is the empirical mean of the sample
      :math:`(x_1, \hdots, x_n)`, and :math:`\Hat{\sigma}_n^2` its unbiaised
      empirical variance.
    | Then, we evaluate the likelihood of the sample with respect to the
      Binomial distribution parameterized with
      :math:`\displaystyle\left(\left\lceil\frac{\Hat{x}_n^2}{\Hat{x}_n-\Hat{\sigma}_n^2}\right\rceil, \frac{\Hat{x}_n}{n}\right)`.
      By testing successively :math:`n+1` and :math:`n-1` instead of
      :math:`n`, we determine the variation of the likelihood of the sample
      with respect to the Binomial distribution parameterized with
      :math:`(n+1,p_{n+1})` and :math:`(n-1,p_{n-1})`. We then iterate in
      the direction that makes the likelihood decrease, until the likelihood
      stops decreasing. The last couple is the one selected.

    See also
    --------
    DistributionFactory, Binomial
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.BinomialFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.BinomialFactory_build(self, *args)

    def buildAsBinomial(self, *args):
        return _dist_bundle1.BinomialFactory_buildAsBinomial(self, *args)

    def __init__(self, *args):
        _dist_bundle1.BinomialFactory_swiginit(self, _dist_bundle1.new_BinomialFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_BinomialFactory


_dist_bundle1.BinomialFactory_swigregister(BinomialFactory)

class Burr(openturns.model_copula.ContinuousDistribution):
    r"""
    Burr distribution.

    Available constructors:
        Burr(*c=1.0, k=1.0*)

    Parameters
    ----------
    c : float, :math:`c > 0`
    k : float, :math:`k > 0`

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        f_X(x) = c k \frac{x^{c - 1}}{(1 + x^c)^{k + 1}}, \quad x \in \Rset^{+*}

    with :math:`c, k > 0`.

    Its only, first-order moment is:

    .. math::

        \Expect{X} = k {\rm B}(k - 1 / c, 1 + 1 / c)

    where :math:`\rm B` denotes Euler's beta function.

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.Burr(2.0, 3.0)

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Burr_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Burr___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Burr___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Burr___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Burr_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Burr_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Burr_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.Burr_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Burr_computeCDF(self, *args)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Burr_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Burr_computeCDFGradient(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Burr_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Burr_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Burr_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.Burr_getStandardMoment(self, n)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Burr_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Burr_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Burr_getParameterDescription(self)

    def setC(self, c):
        """
        Accessor to the parameter :math:`c`.

        Parameters
        ----------
        c : float, :math:`c > 0`
        """
        return _dist_bundle1.Burr_setC(self, c)

    def getC(self):
        """
        Accessor to the parameter :math:`c`.

        Returns
        -------
        c : float
        """
        return _dist_bundle1.Burr_getC(self)

    def setK(self, k):
        """
        Accessor to the parameter :math:`k`.

        Parameters
        ----------
        k : float, :math:`k > 0`
        """
        return _dist_bundle1.Burr_setK(self, k)

    def getK(self):
        """
        Accessor to the parameter :math:`k`.

        Returns
        -------
        k : float
        """
        return _dist_bundle1.Burr_getK(self)

    def __init__(self, *args):
        _dist_bundle1.Burr_swiginit(self, _dist_bundle1.new_Burr(*args))

    __swig_destroy__ = _dist_bundle1.delete_Burr


_dist_bundle1.Burr_swigregister(Burr)

class BurrFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Burr factory.

    Available constructor:
        BurrFactory()

    :math:`\Hat{c}_n` is the solution of the non linear equation

    .. math::

        \displaystyle 1+\frac{c}{n}\left[ SR - \frac{n}{\sum_{i=1}^n \log(1+x_i^c)}SSR\right] = 0

    where :math:`\displaystyle SR = \displaystyle \sum_{i=1}^n \frac{ \log(x_i)}{1+x_i^c}`
    and :math:`\displaystyle SSR = \displaystyle \sum_{i=1}^n \frac{ x_i^c\log(x_i)}{1+x_i^c}`

    Then

    .. math::

        \Hat{k}_n =  \frac{n}{\sum_{i=1}^n \log(1+x_i^c)}

    See also
    --------
    DistributionFactory, Burr
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.BurrFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.BurrFactory_build(self, *args)

    def buildAsBurr(self, *args):
        return _dist_bundle1.BurrFactory_buildAsBurr(self, *args)

    def __init__(self, *args):
        _dist_bundle1.BurrFactory_swiginit(self, _dist_bundle1.new_BurrFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_BurrFactory


_dist_bundle1.BurrFactory_swigregister(BurrFactory)

class Chi(openturns.model_copula.ContinuousDistribution):
    r"""
    :math:`\chi` distribution.

    Available constructors:
        Chi(*nu=1.0*)

    Parameters
    ----------
    nu : float, :math:`\nu > 0`
        Degrees of freedom.

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        f_X(x) = \frac{2^{1 - \nu / 2} x^{\nu - 1} \exp(- x^2 / 2)}
                      {\Gamma(\nu / 2)}, \quad x \in \Rset^{+*}

    with :math:`\nu > 0`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & \sqrt{2}\,\frac{\Gamma((\nu + 1) / 2)}
                                            {\Gamma(\nu / 2)} \\
            \Var{X} & = & \nu - \mu^2
        \end{eqnarray*}

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.Chi(2.0)

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Chi_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Chi___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Chi___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Chi___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Chi_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Chi_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Chi_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.Chi_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Chi_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.Chi_computeComplementaryCDF(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Chi_computeEntropy(self)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.Chi_computeCharacteristicFunction(self, x)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Chi_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Chi_computeCDFGradient(self, *args)

    def computeScalarQuantile(self, prob, tail=False):
        r"""
        Compute the quantile function for univariate distributions.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : float
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_X(p) = F_X^{-1}(p), \quad p \in [0; 1]

        See Also
        --------
        computeQuantile
        """
        return _dist_bundle1.Chi_computeScalarQuantile(self, prob, tail)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Chi_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Chi_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Chi_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.Chi_getStandardMoment(self, n)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Chi_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Chi_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Chi_getParameterDescription(self)

    def setNu(self, nu):
        r"""
        Accessor to the degrees of freedom parameter.

        Parameters
        ----------
        nu : float, :math:`\nu > 0`
            Degrees of freedom.
        """
        return _dist_bundle1.Chi_setNu(self, nu)

    def getNu(self):
        """
        Accessor to the degrees of freedom parameter.

        Returns
        -------
        nu : float
            Degrees of freedom.
        """
        return _dist_bundle1.Chi_getNu(self)

    def __init__(self, *args):
        _dist_bundle1.Chi_swiginit(self, _dist_bundle1.new_Chi(*args))

    __swig_destroy__ = _dist_bundle1.delete_Chi


_dist_bundle1.Chi_swigregister(Chi)

class ChiFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Chi factory.

    Available constructor:
        ChiFactory()

    The parameters are estimated by method of moments:

    .. math::
        :nowrap:

        \begin{eqnarray*}
          \displaystyle \Hat{\nu}_n=\bar{x^2}_n
        \end{eqnarray*}

    See also
    --------
    DistributionFactory, Chi
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.ChiFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.ChiFactory_build(self, *args)

    def buildAsChi(self, *args):
        return _dist_bundle1.ChiFactory_buildAsChi(self, *args)

    def __init__(self, *args):
        _dist_bundle1.ChiFactory_swiginit(self, _dist_bundle1.new_ChiFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_ChiFactory


_dist_bundle1.ChiFactory_swigregister(ChiFactory)

class ChiSquare(openturns.model_copula.ContinuousDistribution):
    r"""
    :math:`\chi^2` distribution.

    Available constructors:
        ChiSquare(*nu=1.0*)

    Parameters
    ----------
    nu : float, :math:`\nu > 0`
        Degrees of freedom.

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        f_X(x) = \frac{2^{- \nu / 2} x^{\nu / 2 - 1} \exp(- x / 2)}
                      {\Gamma(\nu / 2)}, \quad x \in \Rset^{+*}

    with :math:`\nu > 0`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & \nu \\
            \Var{X} & = & 2 \nu
        \end{eqnarray*}

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.ChiSquare(2.0)

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.ChiSquare_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.ChiSquare___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.ChiSquare___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.ChiSquare___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.ChiSquare_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.ChiSquare_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.ChiSquare_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.ChiSquare_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.ChiSquare_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.ChiSquare_computeComplementaryCDF(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.ChiSquare_computeEntropy(self)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.ChiSquare_computeCharacteristicFunction(self, x)

    def computeLogCharacteristicFunction(self, x):
        """
        Compute the logarithm of the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Logarithm of the characteristic function value at input :math:`t`.

        Notes
        -----
        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.

        See Also
        --------
        computeCharacteristicFunction
        """
        return _dist_bundle1.ChiSquare_computeLogCharacteristicFunction(self, x)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.ChiSquare_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.ChiSquare_computeCDFGradient(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.ChiSquare_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.ChiSquare_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.ChiSquare_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.ChiSquare_getStandardMoment(self, n)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.ChiSquare_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.ChiSquare_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.ChiSquare_getParameterDescription(self)

    def setNu(self, nu):
        r"""
        Accessor to the degrees of freedom parameter.

        Parameters
        ----------
        nu : float, :math:`\nu > 0`
            Degrees of freedom.
        """
        return _dist_bundle1.ChiSquare_setNu(self, nu)

    def getNu(self):
        """
        Accessor to the degrees of freedom parameter.

        Returns
        -------
        nu : float
            Degrees of freedom.
        """
        return _dist_bundle1.ChiSquare_getNu(self)

    def __init__(self, *args):
        _dist_bundle1.ChiSquare_swiginit(self, _dist_bundle1.new_ChiSquare(*args))

    __swig_destroy__ = _dist_bundle1.delete_ChiSquare


_dist_bundle1.ChiSquare_swigregister(ChiSquare)

class ChiSquareFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Chi-Square factory.

    Available constructor:
        ChiSquareFactory()

    The parameters are estimated by method of moments:

    .. math::
        :nowrap:

        \begin{eqnarray*}
          \displaystyle \Hat{\nu} = \bar{x}
        \end{eqnarray*}

    See also
    --------
    DistributionFactory, ChiSquare
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.ChiSquareFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.ChiSquareFactory_build(self, *args)

    def buildEstimator(self, *args):
        r"""
        Build the distribution and the parameter distribution.

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        parameters : :class:`~openturns.DistributionParameters`
            Optional, the parametrization.

        Returns
        -------
        resDist : :class:`~openturns.DistributionFactoryResult`
            The results.

        Notes
        -----
        According to the way the native parameters of the distribution are estimated, the parameters distribution differs:

            - Moments method: the asymptotic parameters distribution is normal and estimated by Bootstrap on the initial data;
            - Maximum likelihood method with a regular model: the asymptotic parameters distribution is normal and its covariance matrix is the inverse Fisher information matrix;
            - Other methods: the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting (see :class:`~openturns.KernelSmoothing`).

        If another set of parameters is specified, the native parameters distribution is first estimated and the new distribution is determined from it:

            - if the native parameters distribution is normal and the transformation regular at the estimated parameters values: the asymptotic parameters distribution is normal and its covariance matrix determined from the inverse Fisher information matrix of the native parameters and the transformation;
            - in the other cases, the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting.

        Examples
        --------
        Create a sample from a Beta distribution:

        >>> import openturns as ot
        >>> sample = ot.Beta().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Beta distribution in the native parameters and create a :class:`~openturns.DistributionFactory`:

        >>> fittedRes = ot.BetaFactory().buildEstimator(sample)

        Fit a Beta distribution  in the alternative parametrization :math:`(\mu, \sigma, a, b)`:

        >>> fittedRes2 = ot.BetaFactory().buildEstimator(sample, ot.BetaMuSigma())
        """
        return _dist_bundle1.ChiSquareFactory_buildEstimator(self, *args)

    def buildAsChiSquare(self, *args):
        return _dist_bundle1.ChiSquareFactory_buildAsChiSquare(self, *args)

    def __init__(self, *args):
        _dist_bundle1.ChiSquareFactory_swiginit(self, _dist_bundle1.new_ChiSquareFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_ChiSquareFactory


_dist_bundle1.ChiSquareFactory_swigregister(ChiSquareFactory)

class CompositeDistribution(openturns.model_copula.DistributionImplementation):
    r"""
    Composite distribution.

    Helper class for defining the push-forward distribution of a given univariate
    distribution by a given scalar function.

    Available constructors:
        CompositeDistribution(*g=Function('x', 'x'), distX=Uniform(0.0,1.0)*)

        CompositeDistribution(*g, distX, a, v*)

    Parameters
    ----------
    g : :class:`~openturns.Function`, :math:`\Rset \rightarrow \Rset`
    distX : :class:`~openturns.Distribution`, univariate
    a : sequence of float of dimension :math:`N+1`, :math:`a[0]=\inf \supp{distX}`, :math:`a[N]=\sup \supp{distX}`
        The bounds of the intervals on which :math:`g` is monotone, sorted in
        ascending order.
    v : sequence of float of dimension :math:`N+1`,
        The values taken by :math:`g` on each bound: :math:`v[k]=g(a[k])`.

    Returns
    -------
    distY : :class:`~openturns.Distribution`, univariate
        :math:`distY` is the push-forward distribution of :math:`distX` by :math:`g`.

    Notes
    -----
    We note :math:`X` a scalar random variable which distribution is :math:`distX`,
    which probability density function is :math:`f_X`.

    Then :math:`distY` is the distribution of the scalar random variable
    :math:`Y=g(X)`, which probability density function :math:`f_Y` is defined as:

    .. math::

        \displaystyle f_Y(y) = \sum_{k =0}^{k=N} \frac{f_X (g^{-1}(y))}{|g'\circ g^{-1}(y)|}1_{y \in g^{-1}([a_k, a_{k+1}))}

    with :math:`a_0=\inf \supp{f_X}`, :math:`a_N=\sup \supp{f_X}` and
    :math:`(a_1, \dots, a_N)` such that :math:`g` is monotone over
    :math:`[a_k, a_{k+1})` for :math:`0 \leq k \leq N`.

    Its first moments are obtained by numerical integration.

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> g = ot.SymbolicFunction(['x'], ['sin(x) + cos(x)'])
    >>> distY = ot.CompositeDistribution(g, ot.Normal(1.0, 0.5))

    >>> g = ot.SymbolicFunction(['x'], ['abs(x)'])
    >>> a = [-1.0, 0.0, 2.0]
    >>> v = [1.0, 0.0, 2.0]
    >>> distZ = ot.CompositeDistribution(g, ot.Uniform(-1.0, 2.0), a, v)

    >>> distX = ot.Normal(0.0, 1.0)
    >>> a0 = distX.getRange().getLowerBound()
    >>> aN = distX.getRange().getUpperBound()
    >>> a = [a0[0], 0.0, 0.0, aN[0]]
    >>> g = ot.SymbolicFunction(['x'], ['1.0/x'])
    >>> v = [g(a0)[0], -ot.SpecFunc.MaxScalar, ot.SpecFunc.MaxScalar, g(aN)[0]]
    >>> distT = ot.CompositeDistribution(g, distX, a, v)

    Draw a sample:

    >>> sample = distT.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.CompositeDistribution_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.CompositeDistribution___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.CompositeDistribution___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.CompositeDistribution___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.CompositeDistribution_getRealization(self)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.CompositeDistribution_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.CompositeDistribution_computeCDF(self, *args)

    def computeMinimumVolumeIntervalWithMarginalProbability(self, prob):
        r"""
        Compute the confidence interval with minimum volume.

        Refer to :func:`computeMinimumVolumeInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence interval of the native parameters at level 0.9 with minimum volume:

        >>> ot.ResourceMap.SetAsUnsignedInteger('Distribution-MinimumVolumeLevelSetSamplingSize', 1000)
        >>> confInt, marginalProb = paramDist.computeMinimumVolumeIntervalWithMarginalProbability(0.9)

        """
        return _dist_bundle1.CompositeDistribution_computeMinimumVolumeIntervalWithMarginalProbability(self, prob)

    def computeMinimumVolumeLevelSetWithThreshold(self, prob):
        r"""
        Compute the confidence domain with minimum volume.

        Refer to :func:`computeMinimumVolumeLevelSet()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        levelSet : :class:`~openturns.LevelSet`
            The minimum volume domain of measure :math:`\alpha`.
        level : float
            The value :math:`p_{\alpha}` of the density function defining the frontier of the domain.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence region of minimum volume of the native parameters at level 0.9 with PDF threshold:

        >>> levelSet, threshold = paramDist.computeMinimumVolumeLevelSetWithThreshold(0.9)

        """
        return _dist_bundle1.CompositeDistribution_computeMinimumVolumeLevelSetWithThreshold(self, prob)

    def getSingularities(self):
        """
        Accessor to the singularities of the PDF function.

        It is defined for univariate distributions only, and gives all the singularities (ie discontinuities of any order) strictly inside of the range of the distribution.

        Returns
        -------
        singularities : :class:`~openturns.Point`
            The singularities of the PDF of an univariate distribution.
        """
        return _dist_bundle1.CompositeDistribution_getSingularities(self)

    def getParametersCollection(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _dist_bundle1.CompositeDistribution_getParametersCollection(self)

    def setParametersCollection(self, *args):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _dist_bundle1.CompositeDistribution_setParametersCollection(self, *args)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.CompositeDistribution_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.CompositeDistribution_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.CompositeDistribution_getParameterDescription(self)

    def setFunction(self, function):
        r"""
        Fix the function through wich the distribution is push-forwarded.

        Parameters
        ----------
        g :  :class:`~openturns.Function`, :math:`\Rset \rightarrow \Rset`
            the function :math:`g`.
        """
        return _dist_bundle1.CompositeDistribution_setFunction(self, function)

    def getFunction(self):
        r"""
        Accessor to the function.

        Returns
        -------
        g :  :class:`~openturns.Function`, :math:`\Rset \rightarrow \Rset`
            the function :math:`g`.
        """
        return _dist_bundle1.CompositeDistribution_getFunction(self)

    def setAntecedent(self, antecedent):
        """
        Fix the antecedent distribution which is push-forwarded.

        Parameters
        ----------
        distX : :class:`~openturns.Distribution`, univariate
           Distribution of the antecedent :math:`distX`.
        """
        return _dist_bundle1.CompositeDistribution_setAntecedent(self, antecedent)

    def getAntecedent(self):
        """
        Accessor to the antecedent distribution.

        Returns
        -------
        distX : :class:`~openturns.Distribution`, univariate
            Antecedent distribution :math:`distX`.
        """
        return _dist_bundle1.CompositeDistribution_getAntecedent(self)

    def isContinuous(self):
        """
        Test whether the distribution is continuous or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _dist_bundle1.CompositeDistribution_isContinuous(self)

    def isDiscrete(self):
        """
        Test whether the distribution is discrete or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _dist_bundle1.CompositeDistribution_isDiscrete(self)

    def setSolver(self, solver):
        return _dist_bundle1.CompositeDistribution_setSolver(self, solver)

    def getSolver(self):
        return _dist_bundle1.CompositeDistribution_getSolver(self)

    def computeShiftedMomentContinuous(self, n, shift):
        return _dist_bundle1.CompositeDistribution_computeShiftedMomentContinuous(self, n, shift)

    def __init__(self, *args):
        _dist_bundle1.CompositeDistribution_swiginit(self, _dist_bundle1.new_CompositeDistribution(*args))

    __swig_destroy__ = _dist_bundle1.delete_CompositeDistribution


_dist_bundle1.CompositeDistribution_swigregister(CompositeDistribution)

class Dirac(openturns.model_copula.DiscreteDistribution):
    r"""
    Dirac distribution.

    A possible usage is the modelling of deterministic parameters.

    Available constructors:
        Dirac(*x=0.*)

    Parameters
    ----------
    x : float, sequence of float, :math:`\vect{x} \in \Rset^n`
        The deterministic value.

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        \Prob{\vect{X} = \vect{x}} = 1

    with :math:`\vect{x} \in \Rset^n`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{\vect{X}} & = & \vect{x} \\
            \Var{X_i} & = & 0, \quad i = 1, \ldots, n
        \end{eqnarray*}

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.Dirac([1.0, 2.0, 3.0])

    Draw a sample:

    >>> sample = distribution.getSample(2)
    >>> sample[0] == sample[1]
    True
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Dirac_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Dirac___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Dirac___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Dirac___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Dirac_getRealization(self)

    def getSample(self, size):
        """
        Accessor to a pseudo-random sample from the distribution.

        Parameters
        ----------
        size : int
            Sample size.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            A pseudo-random sample of the distribution.

        See Also
        --------
        getRealization, RandomGenerator
        """
        return _dist_bundle1.Dirac_getSample(self, size)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Dirac_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Dirac_computeCDF(self, *args)

    def computeQuantile(self, *args):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _dist_bundle1.Dirac_computeQuantile(self, *args)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Dirac_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Dirac_computeCDFGradient(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Dirac_computeEntropy(self)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.Dirac_computeCharacteristicFunction(self, x)

    def computeLogCharacteristicFunction(self, x):
        """
        Compute the logarithm of the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Logarithm of the characteristic function value at input :math:`t`.

        Notes
        -----
        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.

        See Also
        --------
        computeCharacteristicFunction
        """
        return _dist_bundle1.Dirac_computeLogCharacteristicFunction(self, x)

    def computeGeneratingFunction(self, z):
        r"""
        Compute the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        g : float
            Probability-generating function value at input :math:`X`.

        Notes
        -----
        The probability-generating function is defined as follows:

        .. math::

            G_X(z) = \Expect{z^X}, \quad z \in \Cset

        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete
        """
        return _dist_bundle1.Dirac_computeGeneratingFunction(self, z)

    def computeLogGeneratingFunction(self, z):
        """
        Compute the logarithm of the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        lg : float
            Logarithm of the probability-generating function value at input :math:`X`.

        Notes
        -----
        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete, computeGeneratingFunction
        """
        return _dist_bundle1.Dirac_computeLogGeneratingFunction(self, z)

    def getSupport(self, *args):
        r"""
        Accessor to the support of the distribution.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval to intersect with the support of the discrete part of the distribution.

        Returns
        -------
        support : :class:`~openturns.Interval`
            The intersection of the support of the discrete part of the distribution with the given `interval`.

        Notes
        -----
        The mathematical support :math:`\supp{\vect{X}}` of the discrete part of a distribution is the collection of points with nonzero probability.

        This is yet implemented for discrete distributions only.

        See Also
        --------
        getRange
        """
        return _dist_bundle1.Dirac_getSupport(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Dirac_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Dirac_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Dirac_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.Dirac_getStandardMoment(self, n)

    def getParametersCollection(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _dist_bundle1.Dirac_getParametersCollection(self)

    def setParametersCollection(self, *args):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _dist_bundle1.Dirac_setParametersCollection(self, *args)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Dirac_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Dirac_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Dirac_getParameterDescription(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _dist_bundle1.Dirac_hasEllipticalCopula(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _dist_bundle1.Dirac_hasIndependentCopula(self)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _dist_bundle1.Dirac_isElliptical(self)

    def setPoint(self, point):
        r"""
        Accessor to the distribution's unique value.

        Parameters
        ----------
        x : float, sequence of float, :math:`\vect{x} \in \Rset^n`
            The deterministic value.
        """
        return _dist_bundle1.Dirac_setPoint(self, point)

    def getPoint(self):
        """
        Accessor to the distribution's unique value.

        Returns
        -------
        x : float, :class:`~openturns.Point`
            The deterministic value.
        """
        return _dist_bundle1.Dirac_getPoint(self)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _dist_bundle1.Dirac_getMarginal(self, *args)

    def __init__(self, *args):
        _dist_bundle1.Dirac_swiginit(self, _dist_bundle1.new_Dirac(*args))

    __swig_destroy__ = _dist_bundle1.delete_Dirac


_dist_bundle1.Dirac_swigregister(Dirac)

class DiracFactory(openturns.model_copula.DistributionFactoryImplementation):
    """
    Dirac factory.

    Available constructor:
        DiracFactory()

    Notes
    -----
    Can only estimate the parameter from a sample that contains the same point.

    See also
    --------
    DistributionFactory, Dirac
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.DiracFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.DiracFactory_build(self, *args)

    def buildAsDirac(self, *args):
        return _dist_bundle1.DiracFactory_buildAsDirac(self, *args)

    def __init__(self, *args):
        _dist_bundle1.DiracFactory_swiginit(self, _dist_bundle1.new_DiracFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_DiracFactory


_dist_bundle1.DiracFactory_swigregister(DiracFactory)

class Dirichlet(openturns.model_copula.ContinuousDistribution):
    r"""
    Dirichlet distribution.

    Available constructors:
        Dirichlet(*theta=[1.0, 1.0]*)

    Parameters
    ----------
    theta : sequence of float, :math:`\theta_i > 0, i = 1, \ldots, n+1`
            theta must be at least bidimensional.

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        f_{\vect{X}}(\vect{x}) = \frac{\Gamma(|\vect{\theta}|_1)}
                                      {\prod_{j=1}^{n + 1} \Gamma(\theta_j)}
                                 \left[1 - \sum_{j=1}^{n} x_j
                                       \right]^{\theta_{n+1} - 1}
                                 \prod_{j=1}^n x_j^{\theta_j - 1},
                                 \quad \vect{x} \in \Delta(\vect{X})

    with :math:`\Delta(\vect{X}) = \{ \vect{x} \in \Rset^n : x_i \geq 0, \sum_{i=1}^n x_i \leq 1, i = 1, \ldots, n \}`
    and :math:`\theta_i > 0, i = 1, \ldots, n+1` and where :math:`|\vect{\theta}|_1 = \sum_{i=1}^{n+1} \theta_i`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{\vect{X}} & = & \Tr{(\theta_i/|\vect{\theta}|_1,
                                         \quad i = 1, \ldots, n)} \\
            \Cov{\vect{X}} & = & \left[- \frac{\theta_i \theta_j}
                                              {|\vect{\theta}|_1^2
                                               (|\vect{\theta}|_1+1)},
                                       \quad i,j = 1, \ldots, n \right]
        \end{eqnarray*}

    .. warning::
        The present implementation does not model the :math:`n+1`-th component of
        the Dirichlet distribution as it is fixed:

        .. math::

            X_{n + 1} = 1 - \sum_{i=1}^{n} X_i

    See Also
    --------
    Multinomial

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.Dirichlet([1.0, 1.0, 1.0])

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Dirichlet_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Dirichlet___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Dirichlet___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Dirichlet___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Dirichlet_getRealization(self)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Dirichlet_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.Dirichlet_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Dirichlet_computeCDF(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Dirichlet_computeEntropy(self)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Dirichlet_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Dirichlet_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Dirichlet_getKurtosis(self)

    def getParametersCollection(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _dist_bundle1.Dirichlet_getParametersCollection(self)

    def setParametersCollection(self, *args):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _dist_bundle1.Dirichlet_setParametersCollection(self, *args)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Dirichlet_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Dirichlet_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Dirichlet_getParameterDescription(self)

    def setTheta(self, theta):
        r"""
        Accessor to the distribution's vector parameter.

        Parameters
        ----------
        theta : float, sequence of float, :math:`\theta_i > 0, i = 1, \ldots, n+1`
        """
        return _dist_bundle1.Dirichlet_setTheta(self, theta)

    def getTheta(self):
        """
        Accessor to the distribution's vector parameter.

        Returns
        -------
        theta : float, :class:`~openturns.Point`
        """
        return _dist_bundle1.Dirichlet_getTheta(self)

    def computeConditionalPDF(self, *args):
        """
        Compute the conditional probability density function.

        Conditional PDF of the last component with respect to the other fixed components.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional PDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional PDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computePDF, computeConditionalCDF
        """
        return _dist_bundle1.Dirichlet_computeConditionalPDF(self, *args)

    def computeSequentialConditionalPDF(self, x):
        r"""
        Compute the sequential conditional probability density function.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the PDF.

        Returns
        -------
        pdf : sequence of float
            Conditional PDF values at input.

        Notes
        -----
        The sequential conditional density function is defined as follows:

        .. math::

            pdf^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\dfrac{d}{d\,x_n}\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional PDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\dfrac{d}{d\,x_1}\Prob{X_1 \leq x_1}`, ie the PDF of the first component at :math:`x_1`.
        """
        return _dist_bundle1.Dirichlet_computeSequentialConditionalPDF(self, x)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _dist_bundle1.Dirichlet_computeConditionalCDF(self, *args)

    def computeSequentialConditionalCDF(self, x):
        r"""
        Compute the sequential conditional cumulative distribution functions.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the CDF.

        Returns
        -------
        F : sequence of float
            Conditional CDF values at input.

        Notes
        -----
        The sequential conditional cumulative distribution function is defined as follows:

        .. math::

            F^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional CDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\Prob{X_1 \leq x_1}`, ie the CDF of the first component at :math:`x_1`.
        """
        return _dist_bundle1.Dirichlet_computeSequentialConditionalCDF(self, x)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _dist_bundle1.Dirichlet_computeConditionalQuantile(self, *args)

    def computeSequentialConditionalQuantile(self, q):
        r"""
        Compute the conditional quantile function of the last component.

        Parameters
        ----------
        q : sequence of float in :math:`[0,1]`, with size :math:`d`
            Values to be taken sequentially as the argument of the conditional quantile.

        Returns
        -------
        Q : sequence of float
            Conditional quantiles values at input.

        Notes
        -----
        The sequential conditional quantile function is defined as follows:

        .. math::

            Q^{seq}_{X_1,\ldots,X_d}(q_1,\ldots,q_d) = \left(F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1}\right)_{i=1,\ldots,d}

        where :math:`x_1,\ldots,x_{n-1}` are defined recursively as :math:`x_1=F_1^{-1}(q_1)` and given :math:`(x_i)_{i=1,\ldots,n-1}`, :math:`x_n=F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1})`: the conditioning part is the set of already computed conditional quantiles.
        """
        return _dist_bundle1.Dirichlet_computeSequentialConditionalQuantile(self, q)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _dist_bundle1.Dirichlet_getMarginal(self, *args)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _dist_bundle1.Dirichlet_hasIndependentCopula(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _dist_bundle1.Dirichlet_hasEllipticalCopula(self)

    def getSpearmanCorrelation(self):
        r"""
        Accessor to the Spearman correlation matrix.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Spearman's correlation matrix.

        Notes
        -----
        Spearman's (rank) correlation is defined as the normalized covariance matrix
        of the copula (ie that of the uniform margins):

        .. math::

            \mat{\rho_S} = \left[\frac{\Cov{F_{X_i}(X_i), F_{X_j}(X_j)}}
                                      {\sqrt{\Var{F_{X_i}(X_i)} \Var{F_{X_j}(X_j)}}},
                                 \quad i,j = 1, \ldots, n\right]

        See Also
        --------
        getKendallTau
        """
        return _dist_bundle1.Dirichlet_getSpearmanCorrelation(self)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _dist_bundle1.Dirichlet_getKendallTau(self)

    def __init__(self, *args):
        _dist_bundle1.Dirichlet_swiginit(self, _dist_bundle1.new_Dirichlet(*args))

    __swig_destroy__ = _dist_bundle1.delete_Dirichlet


_dist_bundle1.Dirichlet_swigregister(Dirichlet)

class DirichletFactory(openturns.model_copula.DistributionFactoryImplementation):
    """
    Dirichlet factory.

    Available constructor:
        DirichletFactory()

    Notes
    -----
    The estimation is done by maximizing the likelihood of the sample,
    using the algorithm described in [minka2012]_.

    See also
    --------
    DistributionFactory, Dirichlet
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.DirichletFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.DirichletFactory_build(self, *args)

    def buildAsDirichlet(self, *args):
        return _dist_bundle1.DirichletFactory_buildAsDirichlet(self, *args)

    def __init__(self, *args):
        _dist_bundle1.DirichletFactory_swiginit(self, _dist_bundle1.new_DirichletFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_DirichletFactory


_dist_bundle1.DirichletFactory_swigregister(DirichletFactory)

class DiscreteCompoundDistribution(openturns.model_copula.DiscreteDistribution):
    r"""
    Discrete compound distribution.

    Parameters
    ----------
    base_distribution : :class:`~openturns.Distribution`
        Integer-valued distribution of the summed independent random variables
    compound_distribution : :class:`~openturns.Distribution`
        Integer-valued distribution of the number of summed terms :math:`N`

    Notes
    -----
    Probability distribution of the random variable :math:`Y(\omega)` defined as:

    .. math::

        Y(\omega) = \sum_{k=1}^{N(\omega)} X_i(\omega)

    where the :math:`X_i \; (i \in \mathbb{N}\setminus{0})` are independent
    identically distribution random variables following base_distribution
    and :math:`N` is a random variable following compound_distribution that is
    independent from all :math:`X_i \; (i \in \mathbb{N}\setminus{0})`.

    See Also
    --------
    Poisson

    Examples
    --------
    Create a discrete compound distribution from a Bernoulli distribution with parameter :math:`p=0.5`
    and a Poisson distribution with parameter :math:`\lambda=10`.
    This is mathematically equivalent to a Poisson distribution with parameter :math:`\lambda=5`.

    >>> import openturns as ot
    >>> distribution = ot.DiscreteCompoundDistribution(ot.Bernoulli(0.5), ot.Poisson(10.0))

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.DiscreteCompoundDistribution_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.DiscreteCompoundDistribution___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.DiscreteCompoundDistribution___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.DiscreteCompoundDistribution___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.DiscreteCompoundDistribution_getRealization(self)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.DiscreteCompoundDistribution_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.DiscreteCompoundDistribution_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.DiscreteCompoundDistribution_computeComplementaryCDF(self, *args)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.DiscreteCompoundDistribution_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.DiscreteCompoundDistribution_computeCDFGradient(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.DiscreteCompoundDistribution_computeEntropy(self)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.DiscreteCompoundDistribution_computeCharacteristicFunction(self, x)

    def computeGeneratingFunction(self, z):
        r"""
        Compute the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        g : float
            Probability-generating function value at input :math:`X`.

        Notes
        -----
        The probability-generating function is defined as follows:

        .. math::

            G_X(z) = \Expect{z^X}, \quad z \in \Cset

        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete
        """
        return _dist_bundle1.DiscreteCompoundDistribution_computeGeneratingFunction(self, z)

    def getSupport(self, *args):
        r"""
        Accessor to the support of the distribution.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval to intersect with the support of the discrete part of the distribution.

        Returns
        -------
        support : :class:`~openturns.Interval`
            The intersection of the support of the discrete part of the distribution with the given `interval`.

        Notes
        -----
        The mathematical support :math:`\supp{\vect{X}}` of the discrete part of a distribution is the collection of points with nonzero probability.

        This is yet implemented for discrete distributions only.

        See Also
        --------
        getRange
        """
        return _dist_bundle1.DiscreteCompoundDistribution_getSupport(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.DiscreteCompoundDistribution_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.DiscreteCompoundDistribution_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.DiscreteCompoundDistribution_getKurtosis(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.DiscreteCompoundDistribution_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.DiscreteCompoundDistribution_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.DiscreteCompoundDistribution_getParameterDescription(self)

    def getBaseDistribution(self):
        """
        Base distribution accessor.

        Returns
        -------
        base_distribution : :class:`~openturns.Distribution`
            Integer-valued distribution of the summed independent random variables
        """
        return _dist_bundle1.DiscreteCompoundDistribution_getBaseDistribution(self)

    def getCompoundDistribution(self):
        """
        Compound distribution accessor.

        Returns
        -------
        compound_distribution : :class:`~openturns.Distribution`
            Integer-valued distribution of the number of summed terms :math:`N`
        """
        return _dist_bundle1.DiscreteCompoundDistribution_getCompoundDistribution(self)

    def __init__(self, *args):
        _dist_bundle1.DiscreteCompoundDistribution_swiginit(self, _dist_bundle1.new_DiscreteCompoundDistribution(*args))

    __swig_destroy__ = _dist_bundle1.delete_DiscreteCompoundDistribution


_dist_bundle1.DiscreteCompoundDistribution_swigregister(DiscreteCompoundDistribution)

class Epanechnikov(openturns.model_copula.ContinuousDistribution):
    r"""
    Epanechnikov distribution.

    Available constructor:
        Epanechnikov()

    Notes
    -----

    Its probability density function is defined as:

    .. math::

        f_X(x) = \frac{3}{4}\,(1 - x^2), \quad x \in [-1; 1]

    It has no parameters and is intended to be used as a kernel within a
    :class:`~openturns.KernelSmoothing`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & 0 \\
            \Var{X} & = & \frac{1}{5}
        \end{eqnarray*}

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.Epanechnikov()

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Epanechnikov_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Epanechnikov___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Epanechnikov___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Epanechnikov___str__(self, *args)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Epanechnikov_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Epanechnikov_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Epanechnikov_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.Epanechnikov_computeComplementaryCDF(self, *args)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Epanechnikov_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Epanechnikov_computeCDFGradient(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Epanechnikov_computeEntropy(self)

    def getRoughness(self):
        r"""
        Accessor to roughness of the distribution.

        Returns
        -------
        r : float
            Roughness of the distribution.

        Notes
        -----
        The roughness of the distribution is defined as the :math:`\cL^2`-norm of its
        PDF:

        .. math::

            r = \int_{\supp{\vect{X}}} f_{\vect{X}}(\vect{x})^2 \di{\vect{x}}

        See Also
        --------
        computePDF
        """
        return _dist_bundle1.Epanechnikov_getRoughness(self)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Epanechnikov_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Epanechnikov_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Epanechnikov_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.Epanechnikov_getStandardMoment(self, n)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _dist_bundle1.Epanechnikov_isElliptical(self)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Epanechnikov_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Epanechnikov_getParameterDescription(self)

    def __init__(self, *args):
        _dist_bundle1.Epanechnikov_swiginit(self, _dist_bundle1.new_Epanechnikov(*args))

    __swig_destroy__ = _dist_bundle1.delete_Epanechnikov


_dist_bundle1.Epanechnikov_swigregister(Epanechnikov)

class Exponential(openturns.model_copula.ContinuousDistribution):
    r"""
    Exponential distribution.

    Parameters
    ----------
    lambda : float, :math:`\lambda > 0`
        Rate parameter.
    gamma : float, optional
        Location parameter :math:`\gamma`.

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        f_X(x) = \lambda \exp\left(- \lambda\,(x - \gamma)\right),
                 \quad x \in [\gamma; +\infty[

    with :math:`\lambda > 0` and :math:`\gamma \in \Rset`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & \gamma + \frac{1}{\lambda} \\
            \Var{X} & = & \frac{1}{\lambda^2}
        \end{eqnarray*}

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.Exponential(1.0)

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Exponential_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Exponential___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Exponential___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Exponential___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Exponential_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Exponential_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Exponential_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.Exponential_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Exponential_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.Exponential_computeComplementaryCDF(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Exponential_computeEntropy(self)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.Exponential_computeCharacteristicFunction(self, x)

    def computeLogCharacteristicFunction(self, x):
        """
        Compute the logarithm of the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Logarithm of the characteristic function value at input :math:`t`.

        Notes
        -----
        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.

        See Also
        --------
        computeCharacteristicFunction
        """
        return _dist_bundle1.Exponential_computeLogCharacteristicFunction(self, x)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Exponential_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Exponential_computeCDFGradient(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Exponential_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Exponential_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Exponential_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.Exponential_getStandardMoment(self, n)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _dist_bundle1.Exponential_getStandardRepresentative(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Exponential_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Exponential_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Exponential_getParameterDescription(self)

    def setLambda(self, _lambda):
        r"""
        Accessor to the rate parameter.

        Parameters
        ----------
        lambda : float, :math:`\lambda > 0`
            Failure rate parameter.
        """
        return _dist_bundle1.Exponential_setLambda(self, _lambda)

    def getLambda(self):
        """
        Accessor to the rate parameter.

        Returns
        -------
        lambda : float
            Rate parameter.
        """
        return _dist_bundle1.Exponential_getLambda(self)

    def setGamma(self, gamma):
        r"""
        Accessor to the location parameter.

        Parameters
        ----------
        gamma : float, :math:`\gamma \in \Rset`
            Shift parameter.
        """
        return _dist_bundle1.Exponential_setGamma(self, gamma)

    def getGamma(self):
        """
        Accessor to the location parameter.

        Returns
        -------
        gamma : float
            Shift parameter.
        """
        return _dist_bundle1.Exponential_getGamma(self)

    def __init__(self, *args):
        _dist_bundle1.Exponential_swiginit(self, _dist_bundle1.new_Exponential(*args))

    __swig_destroy__ = _dist_bundle1.delete_Exponential


_dist_bundle1.Exponential_swigregister(Exponential)

class ExponentialFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Exponential factory.

    Available constructor:
        ExponentialFactory()

    The parameters are estimated by method of moments:

    .. math::
        :nowrap:

        \begin{eqnarray*}
          \displaystyle \Hat{\gamma}_n = x_{(1,n)} - \frac{|x_{(1,n)}|}{2+n}\\
          \displaystyle \Hat{\lambda}_n= \frac{1}{\bar{x}_n-\Hat{\gamma}_n}
        \end{eqnarray*}

    See also
    --------
    DistributionFactory, Exponential
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.ExponentialFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.ExponentialFactory_build(self, *args)

    def buildAsExponential(self, *args):
        return _dist_bundle1.ExponentialFactory_buildAsExponential(self, *args)

    def __init__(self, *args):
        _dist_bundle1.ExponentialFactory_swiginit(self, _dist_bundle1.new_ExponentialFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_ExponentialFactory


_dist_bundle1.ExponentialFactory_swigregister(ExponentialFactory)

class ExtremeValueCopula(openturns.model_copula.CopulaImplementation):
    r"""
    ExtremeValue copula.

    Parameters
    ----------
    pickandFunction : :class:`~openturns.Function`
        Parameter :math:`A`, the Pickand function defining the extreme value copula. Default is the constant function equal to 1.

    Notes
    -----
    The ExtremeValue copula is a bivariate copula defined by:

    .. math::

        C(u_1, u_2) = \exp\left[\log(u_1u_2)A\left(\dfrac{\log u_2}{\log u_1u_2}\right)\right]

    for :math:`(u_1, u_2) \in [0, 1]^2`

    Where :math:`A` is a convex function satisfying :math:`A(0)=A(1)=1`, :math:`\max(t, 1-t)\leq A(t)\leq 1`.

    See also
    --------
    Distribution

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> copula = ot.ExtremeValueCopula(ot.SymbolicFunction('t', '1'))

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.ExtremeValueCopula_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.ExtremeValueCopula___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.ExtremeValueCopula___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.ExtremeValueCopula___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.ExtremeValueCopula_getRealization(self)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.ExtremeValueCopula_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.ExtremeValueCopula_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.ExtremeValueCopula_computeCDF(self, *args)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _dist_bundle1.ExtremeValueCopula_computeConditionalCDF(self, *args)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _dist_bundle1.ExtremeValueCopula_computeConditionalQuantile(self, *args)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _dist_bundle1.ExtremeValueCopula_hasIndependentCopula(self)

    def setPickandFunction(self, *args):
        r"""
        Set the Pickand function :math:`A`.

        Parameters
        ----------
        A : :class:`~openturns.Function`
            The Pickand function of the copula. It must be a convex function :math:`A` such that :math:`\forall t\in[0,1],\:\max(t, 1-t)\leq A(t)\leq 1`.
        check : bool
            Flag to tell if the properties of a Pickand function are verified by the given function. Default value is *True*, given by the *ExtremeValueCopula-CheckPickandFunction* entry in the :class:`~openturns.ResourceMap`, and the test is done pointwise on a regular grid of size given by the *ExtremeValueCopula-CheckGridSize* entry in the :class:`~openturns.ResourceMap`.

        """
        return _dist_bundle1.ExtremeValueCopula_setPickandFunction(self, *args)

    def getPickandFunction(self):
        """
        Get the Pickand function :math:`A`.

        Returns
        -------
        A : :class:`~openturns.Function`
            The Pickand function :math:`A` of the copula.
        """
        return _dist_bundle1.ExtremeValueCopula_getPickandFunction(self)

    def __init__(self, *args):
        _dist_bundle1.ExtremeValueCopula_swiginit(self, _dist_bundle1.new_ExtremeValueCopula(*args))

    __swig_destroy__ = _dist_bundle1.delete_ExtremeValueCopula


_dist_bundle1.ExtremeValueCopula_swigregister(ExtremeValueCopula)

class JoeCopula(ExtremeValueCopula):
    r"""
    Joe copula.

    Parameters
    ----------
    theta : float
        Parameter :math:`\theta > 0`. Default is :math:`\theta=0.5`.
    psi1 : float
        Parameter :math:`\psi_1 \in [0, 1]`. Default is :math:`\psi_1=0.5`.
    psi2 : float
        Parameter :math:`\psi_2 \in [0, 1]`. Default is :math:`\psi_2=0.5`.

    Notes
    -----
    The Joe copula is a bivariate copula defined by:

    .. math::

        C(u_1, u_2) = \exp\left[\log(u_1u_2)A\left(\dfrac{\log u_2}{\log u_1u_2}\right)\right]

    for :math:`(u_1, u_2) \in [0, 1]^2`

    Where :math:`A` is the following Pickand function 
    :math:`t \in [0,1]`, :math:`A(t) = 1 - [ (\psi_1 (1-t))^{-1/ \theta} + (\psi_2 t)^{-1/ \theta} ]^{- \theta}`

    See also
    --------
    ExtremeValueCopula

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> copula = ot.JoeCopula(0.5)

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.JoeCopula_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.JoeCopula___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.JoeCopula___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.JoeCopula___str__(self, *args)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.JoeCopula_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.JoeCopula_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.JoeCopula_getParameterDescription(self)

    def setTheta(self, theta):
        r"""
        Set the Joe copula parameter :math:`\theta`.

        Parameters
        ----------
        theta : float
            The scalar parameter :math:`\theta > 0`.

        """
        return _dist_bundle1.JoeCopula_setTheta(self, theta)

    def getTheta(self):
        r"""
        Get the Joe copula parameter :math:`\theta`.

        Returns
        -------
        theta : float
            The scalar parameter :math:`\theta > 0`.

        """
        return _dist_bundle1.JoeCopula_getTheta(self)

    def setPsi1(self, psi1):
        r"""
        Set the Joe copula parameter :math:`\psi_1`.

        Parameters
        ----------
        psi1 : float
            The scalar parameter :math:`\psi_1 \in [0, 1]`.

        """
        return _dist_bundle1.JoeCopula_setPsi1(self, psi1)

    def getPsi1(self):
        r"""
        Get the Joe copula parameter :math:`\psi_1`.

        Returns
        -------
        psi1 : float
            The scalar parameter :math:`\psi_1 \in [0, 1]`.

        """
        return _dist_bundle1.JoeCopula_getPsi1(self)

    def setPsi2(self, psi2):
        r"""
        Set the Joe copula parameter :math:`\psi_2`.

        Parameters
        ----------
        psi2 : float
            The scalar parameter :math:`\psi_2 \in [0, 1]`.

        """
        return _dist_bundle1.JoeCopula_setPsi2(self, psi2)

    def getPsi2(self):
        r"""
        Get the Joe copula parameter :math:`\psi_2`.

        Returns
        -------
        psi2 : float
            The scalar parameter :math:`\psi_2 \in [0, 1]`.

        """
        return _dist_bundle1.JoeCopula_getPsi2(self)

    def __init__(self, *args):
        _dist_bundle1.JoeCopula_swiginit(self, _dist_bundle1.new_JoeCopula(*args))

    __swig_destroy__ = _dist_bundle1.delete_JoeCopula


_dist_bundle1.JoeCopula_swigregister(JoeCopula)

class FisherSnedecor(openturns.model_copula.ContinuousDistribution):
    r"""
    Fisher-Snedecor distribution.

    Available constructors:
        FisherSnedecor(*d1=1.0, d2=5.0*)

    Parameters
    ----------
    d1 : float, :math:`d_1 > 0`
        First :class:`~openturns.ChiSquare` degrees of freedom (numerator).
    d2 : float, :math:`d_2 > 0`
        Second :class:`~openturns.ChiSquare` degrees of freedom (denominator).

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        f_X(x) = \frac{1}{x {\rm B}(d_1 / 2, d_2 / 2)}
                 \left[\left(\frac{d_1 x}{d_1 x + d_2}\right)^{d_1 / 2}
                       \left(1 - \frac{d_1 x}{d_1 x + d_2}\right)^{d_2 / 2}\right],
                 \quad x \in \Rset^{+*}

    with :math:`d_1, d_2 > 0` and where :math:`\rm B` denotes Euler's beta
    function.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & \frac{d_2}{d_2 - 2} \textrm{ if } d_2>2\\
            \Var{X} & = & \frac{2d_2^2(d_1+d_2-2)}{d_1(d_2-2)^2(d_2-4)} \textrm{ if } d_2>4
        \end{eqnarray*}

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.FisherSnedecor(2.0, 3.0)

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.FisherSnedecor_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.FisherSnedecor___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.FisherSnedecor___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.FisherSnedecor___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.FisherSnedecor_getRealization(self)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.FisherSnedecor_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.FisherSnedecor_computeLogPDF(self, *args)

    def computeLogPDFGradient(self, *args):
        """
        Compute the gradient of the log probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the logPDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.FisherSnedecor_computeLogPDFGradient(self, *args)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.FisherSnedecor_computePDFGradient(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.FisherSnedecor_computeCDF(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.FisherSnedecor_computeEntropy(self)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.FisherSnedecor_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.FisherSnedecor_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.FisherSnedecor_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.FisherSnedecor_getStandardMoment(self, n)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.FisherSnedecor_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.FisherSnedecor_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.FisherSnedecor_getParameterDescription(self)

    def setD1(self, d1):
        """
        Accessor to the parameter :math:`d_1`.

        Parameters
        ----------
        d1 : float, :math:`d_1 > 0`
            First :class:`~openturns.ChiSquare` degrees of freedom (numerator).
        """
        return _dist_bundle1.FisherSnedecor_setD1(self, d1)

    def getD1(self):
        """
        Accessor to the parameter :math:`d_1`.

        Returns
        -------
        d1 : float
            First :class:`~openturns.ChiSquare` degrees of freedom (numerator).
        """
        return _dist_bundle1.FisherSnedecor_getD1(self)

    def setD2(self, d2):
        """
        Accessor to the parameter :math:`d_2`.

        Parameters
        ----------
        d2 : float, :math:`d_2 > 0`
            Second :class:`~openturns.ChiSquare` degrees of freedom (denominator).
        """
        return _dist_bundle1.FisherSnedecor_setD2(self, d2)

    def getD2(self):
        """
        Accessor to the parameter :math:`d_2`.

        Returns
        -------
        d2 : float
            Second :class:`~openturns.ChiSquare` degrees of freedom (denominator).
        """
        return _dist_bundle1.FisherSnedecor_getD2(self)

    def __init__(self, *args):
        _dist_bundle1.FisherSnedecor_swiginit(self, _dist_bundle1.new_FisherSnedecor(*args))

    __swig_destroy__ = _dist_bundle1.delete_FisherSnedecor


_dist_bundle1.FisherSnedecor_swigregister(FisherSnedecor)

class FisherSnedecorFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Fisher-Snedecor factory.

    Available constructor:
        FisherSnedecorFactory()

    Notes
    -----
    Several estimators to build a FisherSnedecor distribution from a scalar sample
    are proposed.

    **Maximum likelihood estimator:**

    The parameters are estimated by numerical maximum likelihood estimation. 
    The starting point of the optimization algorithm is based on the moment based 
    estimator. 

    The optimization sets lower bounds for the :math:`d_1` and :math:`d_2` parameters 
    in order to ensure that :math:`d_1>0` and :math:`d_2>0`. 
    The default values for these lower bounds are from the :class:`~openturns.ResourceMap` 
    keys `FisherSnedecorFactory-D1LowerBound` and `FisherSnedecorFactory-D2LowerBound`. 

    **Moment based estimator:**

    Lets denote:

    - :math:`\displaystyle \overline{x}_n = \frac{1}{n} \sum_{i=1}^n x_i` the empirical
      mean of the sample, 
    - :math:`\displaystyle s_n^2 = \frac{1}{n-1} \sum_{i=1}^n (x_i - \overline{x}_n)^2`
      its empirical variance,

    We first compute :math:`d_2`:

    .. math::

        d_2 = \frac{2 \overline{x}_n}{\overline{x}_n-1}

    if :math:`\overline{x}_n>1` (otherwise, the moment based estimator fails). 

    Then we compute :math:`d_1`:

    .. math::

        d_1 = \frac{2 d_2^2 (d_2-2)}{(d_2-2)^2 (d_2-4)s_n^2 - 2d_2^2}

    if :math:`s_n^2>0` (otherwise, the moment based estimator fails). 

    See also
    --------
    DistributionFactory, FisherSnedecor
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.FisherSnedecorFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.FisherSnedecorFactory_build(self, *args)

    def buildMethodOfMoments(self, sample):
        return _dist_bundle1.FisherSnedecorFactory_buildMethodOfMoments(self, sample)

    def buildEstimator(self, *args):
        r"""
        Build the distribution and the parameter distribution.

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        parameters : :class:`~openturns.DistributionParameters`
            Optional, the parametrization.

        Returns
        -------
        resDist : :class:`~openturns.DistributionFactoryResult`
            The results.

        Notes
        -----
        According to the way the native parameters of the distribution are estimated, the parameters distribution differs:

            - Moments method: the asymptotic parameters distribution is normal and estimated by Bootstrap on the initial data;
            - Maximum likelihood method with a regular model: the asymptotic parameters distribution is normal and its covariance matrix is the inverse Fisher information matrix;
            - Other methods: the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting (see :class:`~openturns.KernelSmoothing`).

        If another set of parameters is specified, the native parameters distribution is first estimated and the new distribution is determined from it:

            - if the native parameters distribution is normal and the transformation regular at the estimated parameters values: the asymptotic parameters distribution is normal and its covariance matrix determined from the inverse Fisher information matrix of the native parameters and the transformation;
            - in the other cases, the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting.

        Examples
        --------
        Create a sample from a Beta distribution:

        >>> import openturns as ot
        >>> sample = ot.Beta().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Beta distribution in the native parameters and create a :class:`~openturns.DistributionFactory`:

        >>> fittedRes = ot.BetaFactory().buildEstimator(sample)

        Fit a Beta distribution  in the alternative parametrization :math:`(\mu, \sigma, a, b)`:

        >>> fittedRes2 = ot.BetaFactory().buildEstimator(sample, ot.BetaMuSigma())
        """
        return _dist_bundle1.FisherSnedecorFactory_buildEstimator(self, *args)

    def buildAsFisherSnedecor(self, *args):
        return _dist_bundle1.FisherSnedecorFactory_buildAsFisherSnedecor(self, *args)

    def __init__(self, *args):
        _dist_bundle1.FisherSnedecorFactory_swiginit(self, _dist_bundle1.new_FisherSnedecorFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_FisherSnedecorFactory


_dist_bundle1.FisherSnedecorFactory_swigregister(FisherSnedecorFactory)

class Frechet(openturns.model_copula.ContinuousDistribution):
    r"""
    Frechet distribution.

    Parameters
    ----------
    beta : float, :math:`\beta > 0`
        Scale parameter
    alpha : float, :math:`\alpha > 0`
        Shape parameter
    gamma : float, optional
        Location parameter

    Notes
    -----
    Its cumulative and probability density functions are defined as:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            F_X(x) & = & \exp\left(-\left(\frac{x-\gamma}{\beta}\right)^{-\alpha}\right), \quad x \in [ \gamma; +\infty) \\
            f_X(x) & = & \frac{\alpha}{\beta}\left(\frac{x-\gamma}{\beta}\right)^{-1-\alpha}\exp\left(-\left(\frac{x-\gamma}{\beta}\right)^{-\alpha}\right),
                 \quad x \in [ \gamma; +\infty)
        \end{eqnarray*}

    with :math:`\beta > 0` and :math:`\alpha > 0`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & \gamma + \beta \,\Gamma\left(1 - \frac{1}{\alpha}\right)
                            \quad \text{ if } \alpha > 1\\
                       & = & +\infty  \quad\text{ if } \alpha \leq 1\\
            \Var{X} & = & \beta^2 \left( \Gamma \left( 1 - \frac{2}{\alpha} \right) -
                         \Gamma^2 \left( 1 - \frac{1}{\alpha} \right) \right) \quad \text{ if } \alpha > 2\\
                       & = & +\infty  \quad \text{ if } \alpha \leq 2\\
        \end{eqnarray*}

    where :math:`\Gamma` denotes Euler's Gamma function
    :class:`~openturns.SpecFunc_Gamma`.

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.Frechet(1.0, 3.0, 0.0)

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Frechet_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Frechet___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Frechet___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Frechet___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Frechet_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Frechet_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Frechet_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.Frechet_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Frechet_computeCDF(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Frechet_computeEntropy(self)

    def computeMinimumVolumeLevelSetWithThreshold(self, prob):
        r"""
        Compute the confidence domain with minimum volume.

        Refer to :func:`computeMinimumVolumeLevelSet()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        levelSet : :class:`~openturns.LevelSet`
            The minimum volume domain of measure :math:`\alpha`.
        level : float
            The value :math:`p_{\alpha}` of the density function defining the frontier of the domain.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence region of minimum volume of the native parameters at level 0.9 with PDF threshold:

        >>> levelSet, threshold = paramDist.computeMinimumVolumeLevelSetWithThreshold(0.9)

        """
        return _dist_bundle1.Frechet_computeMinimumVolumeLevelSetWithThreshold(self, prob)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Frechet_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Frechet_computeCDFGradient(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Frechet_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Frechet_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Frechet_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.Frechet_getStandardMoment(self, n)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _dist_bundle1.Frechet_getStandardRepresentative(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Frechet_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Frechet_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Frechet_getParameterDescription(self)

    def setAlpha(self, alpha):
        r"""
        Accessor to the shape parameter.

        Parameters
        ----------
        alpha : float, :math:`\alpha > 0`
            Shape parameter.
        """
        return _dist_bundle1.Frechet_setAlpha(self, alpha)

    def getAlpha(self):
        """
        Accessor to the shape parameter.

        Returns
        -------
        alpha : float
            Shape parameter.
        """
        return _dist_bundle1.Frechet_getAlpha(self)

    def setBeta(self, beta):
        r"""
        Accessor to the scale parameter.

        Parameters
        ----------
        beta : float, :math:`\beta > 0`
            Scale parameter.
        """
        return _dist_bundle1.Frechet_setBeta(self, beta)

    def getBeta(self):
        """
        Accessor to the scale parameter.

        Returns
        -------
        beta : float
            Scale parameter.
        """
        return _dist_bundle1.Frechet_getBeta(self)

    def setGamma(self, gamma):
        r"""
        Accessor to the location parameter.

        Parameters
        ----------
        gamma : float, :math:`\gamma > 0`
            Location parameter.
        """
        return _dist_bundle1.Frechet_setGamma(self, gamma)

    def getGamma(self):
        """
        Accessor to the location parameter.

        Returns
        -------
        gamma : float
            Location parameter.
        """
        return _dist_bundle1.Frechet_getGamma(self)

    def __init__(self, *args):
        _dist_bundle1.Frechet_swiginit(self, _dist_bundle1.new_Frechet(*args))

    __swig_destroy__ = _dist_bundle1.delete_Frechet


_dist_bundle1.Frechet_swigregister(Frechet)

class FrechetFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Frechet factory.

    Available constructor:
        FrechetFactory()

    The parameters are estimated by likelihood maximization. The starting point is obtained from the estimation of a Gumbel distribution based on the logarithm of the shifted observations:

    .. math::
        :nowrap:

        \begin{eqnarray*}
          \displaystyle\Hat{\alpha} & = & \frac{\pi}{\Hat{\sigma}_y\sqrt{6}} \\
          \displaystyle\Hat{\beta} & = & \exp\left\{\bar{y}_n-\frac{\gamma\sqrt{6}}{\pi}\Hat{\sigma}_y\right\} \\
          \displaystyle\Hat{\gamma} & = & x_{(1)} - \frac{|x_{(1)}|}{n+2}
        \end{eqnarray*}

    with :math:`\gamma \simeq 0.57721` as Euler's constant (not to be confused with the location parameter of the Frechet distribution!), :math:`x_{(1)}=\min_{i=1,\dots,n}x_i` and :math:`y_i=x_i-\Hat{\gamma}`.

    See also
    --------
    DistributionFactory, Frechet
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.FrechetFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.FrechetFactory_build(self, *args)

    def buildAsFrechet(self, *args):
        return _dist_bundle1.FrechetFactory_buildAsFrechet(self, *args)

    def buildEstimator(self, *args):
        r"""
        Build the distribution and the parameter distribution.

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        parameters : :class:`~openturns.DistributionParameters`
            Optional, the parametrization.

        Returns
        -------
        resDist : :class:`~openturns.DistributionFactoryResult`
            The results.

        Notes
        -----
        According to the way the native parameters of the distribution are estimated, the parameters distribution differs:

            - Moments method: the asymptotic parameters distribution is normal and estimated by Bootstrap on the initial data;
            - Maximum likelihood method with a regular model: the asymptotic parameters distribution is normal and its covariance matrix is the inverse Fisher information matrix;
            - Other methods: the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting (see :class:`~openturns.KernelSmoothing`).

        If another set of parameters is specified, the native parameters distribution is first estimated and the new distribution is determined from it:

            - if the native parameters distribution is normal and the transformation regular at the estimated parameters values: the asymptotic parameters distribution is normal and its covariance matrix determined from the inverse Fisher information matrix of the native parameters and the transformation;
            - in the other cases, the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting.

        Examples
        --------
        Create a sample from a Beta distribution:

        >>> import openturns as ot
        >>> sample = ot.Beta().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Beta distribution in the native parameters and create a :class:`~openturns.DistributionFactory`:

        >>> fittedRes = ot.BetaFactory().buildEstimator(sample)

        Fit a Beta distribution  in the alternative parametrization :math:`(\mu, \sigma, a, b)`:

        >>> fittedRes2 = ot.BetaFactory().buildEstimator(sample, ot.BetaMuSigma())
        """
        return _dist_bundle1.FrechetFactory_buildEstimator(self, *args)

    def __init__(self, *args):
        _dist_bundle1.FrechetFactory_swiginit(self, _dist_bundle1.new_FrechetFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_FrechetFactory


_dist_bundle1.FrechetFactory_swigregister(FrechetFactory)

class Gamma(openturns.model_copula.ContinuousDistribution):
    r"""
    Gamma distribution.

    Parameters
    ----------
    k : float
        Shape parameter :math:`k > 0` with :math:`k = (\mu - \gamma)^2 / \sigma^2`.
    lambda : float
        Rate parameter :math:`\lambda > 0` with :math:`\lambda = (\mu - \gamma) / \sigma^2`.
    gamma : float, optional
        Location parameter :math:`\gamma`.

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        f_X(x) = \frac{\lambda}{\Gamma(k)}
                 \left(\lambda (x - \gamma)\right)^{k - 1}
                 \exp\left(- \lambda (x - \gamma)\right),
                 \quad x \in [\gamma; +\infty[

    with :math:`k, \lambda > 0` and :math:`\gamma \in \Rset`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & \frac{k}{\lambda} + \gamma \\
            \Var{X} & = & \frac{\sqrt{k}}{\lambda}
        \end{eqnarray*}

    It is possible to create a Gamma distribution from the alternative parametrization :math:`(\mu, \sigma, \gamma)`: see  :class:`~openturns.GammaMuSigma`. In that case, all the results are presented in that new parametrization.

    In order to use the alternative  parametrization :math:`(\mu, \sigma, \gamma)` only to create the distribution, see the example below: all the results will be presented in the native parametrization :math:`(k, \lambda, \gamma)`.

    Examples
    --------
    Create a distribution from its native parameters :math:`(k, \lambda, \gamma)`:

    >>> import openturns as ot
    >>> myDist = ot.Gamma(1.0, 1.0, 0.0)

    Create a it from the alternative parametrization :math:`(\mu, \lambda, \gamma)`:

    >>> myDist2 = ot.Gamma()
    >>> myDist2.setParameter(ot.GammaMuSigma()([1.0, 1.0, 0.0]))

    Create it from :math:`(\mu, \lambda, \gamma)` and keep that parametrization for the remaining study: 

    >>> myParam = ot.GammaMuSigma(1.5, 2.5, -0.5)
    >>> myDist3 = ot.ParametrizedDistribution(myParam)

    Draw a sample:

    >>> sample = myDist.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Gamma_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Gamma___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Gamma___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Gamma___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Gamma_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Gamma_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Gamma_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.Gamma_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Gamma_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.Gamma_computeComplementaryCDF(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Gamma_computeEntropy(self)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.Gamma_computeCharacteristicFunction(self, x)

    def computeLogCharacteristicFunction(self, x):
        """
        Compute the logarithm of the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Logarithm of the characteristic function value at input :math:`t`.

        Notes
        -----
        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.

        See Also
        --------
        computeCharacteristicFunction
        """
        return _dist_bundle1.Gamma_computeLogCharacteristicFunction(self, x)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Gamma_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Gamma_computeCDFGradient(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Gamma_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Gamma_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Gamma_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.Gamma_getStandardMoment(self, n)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _dist_bundle1.Gamma_getStandardRepresentative(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Gamma_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Gamma_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Gamma_getParameterDescription(self)

    def setK(self, k):
        """
        Accessor to the distribution's shape parameter :math:`k`.

        Parameters
        ----------
        k : float, :math:`k > 0`
            Shape parameter :math:`k`.
        """
        return _dist_bundle1.Gamma_setK(self, k)

    def getK(self):
        """
        Accessor to the distribution's shape parameter :math:`k`.

        Returns
        -------
        k : float
            Shape parameter :math:`k`.
        """
        return _dist_bundle1.Gamma_getK(self)

    def setLambda(self, _lambda):
        r"""
        Accessor to the distribution's rate parameter :math:`\lambda`.

        Parameters
        ----------
        lambda : float, :math:`\lambda > 0`
            Rate parameter :math:`\lambda`.
        """
        return _dist_bundle1.Gamma_setLambda(self, _lambda)

    def getLambda(self):
        r"""
        Accessor to the distribution's rate parameter :math:`\lambda`.

        Returns
        -------
        lambda : float
            Rate parameter :math:`\lambda`.
        """
        return _dist_bundle1.Gamma_getLambda(self)

    def setKLambda(self, k, _lambda):
        r"""
        Set the distribution's parameters.

        For rate parameter :math:`\lambda` and shape parameter :math:`k`.

        Parameters
        ----------
        k : float, :math:`k > 0`
            Shape parameter :math:`k`.
        lambda : float, :math:`\lambda > 0`
            Rate parameter :math:`\lambda`.
        """
        return _dist_bundle1.Gamma_setKLambda(self, k, _lambda)

    def setGamma(self, gamma):
        r"""
        Accessor to the distribution's location parameter :math:`\gamma`.

        Parameters
        ----------
        gamma : float, :math:`\gamma \in \Rset`
            Location parameter :math:`\gamma`.
        """
        return _dist_bundle1.Gamma_setGamma(self, gamma)

    def getGamma(self):
        r"""
        Accessor to the distribution's location parameter :math:`\gamma`.

        Returns
        -------
        gamma : float
            Location parameter :math:`\gamma`.
        """
        return _dist_bundle1.Gamma_getGamma(self)

    def __init__(self, *args):
        _dist_bundle1.Gamma_swiginit(self, _dist_bundle1.new_Gamma(*args))

    __swig_destroy__ = _dist_bundle1.delete_Gamma


_dist_bundle1.Gamma_swigregister(Gamma)

class GammaFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Gamma factory.

    Available constructor:
        GammaFactory()

    The parameters are estimated by maximum likelihood:

    .. math::
        :nowrap:

        \begin{eqnarray*}
          \displaystyle\Hat{k}_n= \frac{(\bar{x}_n-\Hat{\gamma}_n)^2}{(\sigma_n^X)^2}\\
          \displaystyle\Hat{\lambda}_n= \frac{\bar{x}_n-\Hat{\gamma}_n}{(\sigma_n^X)^2}\\
          \displaystyle\Hat{\gamma}_n = (1-\mathrm{sign}(x_{(1,n)})/(2+n))x_{(1,n)}
        \end{eqnarray*}

    See also
    --------
    DistributionFactory, Gamma
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.GammaFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.GammaFactory_build(self, *args)

    def buildAsGamma(self, *args):
        return _dist_bundle1.GammaFactory_buildAsGamma(self, *args)

    def __init__(self, *args):
        _dist_bundle1.GammaFactory_swiginit(self, _dist_bundle1.new_GammaFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_GammaFactory


_dist_bundle1.GammaFactory_swigregister(GammaFactory)

class GammaMuSigma(openturns.model_copula.DistributionParametersImplementation):
    r"""
    Gamma distribution parameters.

    Available constructors:
        GammaMuSigma(*mu=1.0, sigma=1.0, gamma=0.0*)

    Parameters
    ----------
    mu : float
        Mean.
    sigma : float
        Standard deviation :math:`\sigma > 0`.
    gamma : float, optional
        Shift parameter.

    Notes
    -----
    The native parameters are defined as follows:

    .. math::

        k &= \left( \frac{\mu-\gamma}{\sigma} \right)^2 \\
        \lambda &= \frac{\mu-\gamma}{\sigma^2}

    See also
    --------
    Gamma

    Examples
    --------
    Create the parameters of the Gamma distribution:

    >>> import openturns as ot
    >>> parameters = ot.GammaMuSigma(1.5, 2.5, -0.5)

    Convert parameters into the native parameters:

    >>> print(parameters.evaluate())
    [0.64,0.32,-0.5]

    The gradient of the transformation of the native parameters into the new
    parameters:

    >>> print(parameters.gradient())
    [[  0.64   0.16   0     ]
     [ -0.512 -0.256  0     ]
     [ -0.64  -0.16   1     ]]
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.GammaMuSigma_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.GammaMuSigma___eq__(self, other)

    def getDistribution(self):
        """
        Build a distribution based on a set of native parameters.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Distribution built with the native parameters.
        """
        return _dist_bundle1.GammaMuSigma_getDistribution(self)

    def gradient(self):
        r"""
        Get the gradient.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The gradient of the transformation of the native parameters into the new
            parameters.

        Notes
        -----

        If we note :math:`(p_1, \dots, p_q)` the native parameters and :math:`(p'_1, \dots, p'_q)` the new ones, then the gradient matrix is :math:`\left( \dfrac{\partial p'_i}{\partial p_j} \right)_{1 \leq i,j \leq  q}`.
        """
        return _dist_bundle1.GammaMuSigma_gradient(self)

    def __call__(self, inP):
        return _dist_bundle1.GammaMuSigma___call__(self, inP)

    def inverse(self, inP):
        """
        Convert to native parameters.

        Parameters
        ----------
        inP : sequence of float
            The non-native parameters.

        Returns
        -------
        outP : :class:`~openturns.Point`
            The native parameters.
        """
        return _dist_bundle1.GammaMuSigma_inverse(self, inP)

    def setValues(self, values):
        """
        Accessor to the parameters values.

        Parameters
        ----------
        values : sequence of float
            List of parameters values.
        """
        return _dist_bundle1.GammaMuSigma_setValues(self, values)

    def getValues(self):
        """
        Accessor to the parameters values.

        Returns
        -------
        values : :class:`~openturns.Point`
            List of parameters values.
        """
        return _dist_bundle1.GammaMuSigma_getValues(self)

    def getDescription(self):
        """
        Get the description of the parameters.

        Returns
        -------
        collection : :class:`~openturns.Description`
            List of parameters names.
        """
        return _dist_bundle1.GammaMuSigma_getDescription(self)

    def __repr__(self):
        return _dist_bundle1.GammaMuSigma___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.GammaMuSigma___str__(self, *args)

    def __init__(self, *args):
        _dist_bundle1.GammaMuSigma_swiginit(self, _dist_bundle1.new_GammaMuSigma(*args))

    __swig_destroy__ = _dist_bundle1.delete_GammaMuSigma


_dist_bundle1.GammaMuSigma_swigregister(GammaMuSigma)

class Pareto(openturns.model_copula.ContinuousDistribution):
    r"""
    Pareto distribution.

    Parameters
    ----------
    beta : float
        Scale parameter :math:`\beta > 0`.
    alpha : float, :math:`\alpha > 0`
        Shape parameter :math:`\alpha`.
    gamma : float
        Location parameter :math:`\gamma`.

    Notes
    -----
    Its cumulative and probability distribution functions are defined as:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            F_X(x) & = & 1 - \left( \frac{x- \gamma}{\beta} \right) ^{-\alpha},  \quad \forall x \geq \gamma + \beta \\
            p_X(x) & = & \dfrac{\alpha}{\beta} \left( \frac{x- \gamma}{\beta} \right) ^{-\alpha-1},  \quad \forall x \geq \gamma + \beta
        \end{eqnarray*}

    with :math:`\alpha > 0` and :math:`\beta >0`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & \gamma + \frac{\alpha}{\alpha + 1}\beta
                             \quad \text{ if } \alpha > 1 \\
            \Var{X} & = & \dfrac{\alpha}{\alpha-2}\left(\dfrac{\beta}{\alpha - 1} \right)^2 \quad \text{ if } \alpha > 2 \\
            Skew[X] & = & \dfrac{2(1+\alpha)}{\alpha-3}\sqrt{\dfrac{\alpha-2}{\alpha}} \quad \text{ if } \alpha > 3
        \end{eqnarray*}

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.Pareto(1.0, 1.0, 0.0)

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Pareto_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Pareto___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Pareto___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Pareto___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Pareto_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Pareto_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Pareto_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.Pareto_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Pareto_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.Pareto_computeComplementaryCDF(self, *args)

    def computeMinimumVolumeIntervalWithMarginalProbability(self, prob):
        r"""
        Compute the confidence interval with minimum volume.

        Refer to :func:`computeMinimumVolumeInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence interval of the native parameters at level 0.9 with minimum volume:

        >>> ot.ResourceMap.SetAsUnsignedInteger('Distribution-MinimumVolumeLevelSetSamplingSize', 1000)
        >>> confInt, marginalProb = paramDist.computeMinimumVolumeIntervalWithMarginalProbability(0.9)

        """
        return _dist_bundle1.Pareto_computeMinimumVolumeIntervalWithMarginalProbability(self, prob)

    def computeMinimumVolumeLevelSetWithThreshold(self, prob):
        r"""
        Compute the confidence domain with minimum volume.

        Refer to :func:`computeMinimumVolumeLevelSet()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        levelSet : :class:`~openturns.LevelSet`
            The minimum volume domain of measure :math:`\alpha`.
        level : float
            The value :math:`p_{\alpha}` of the density function defining the frontier of the domain.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence region of minimum volume of the native parameters at level 0.9 with PDF threshold:

        >>> levelSet, threshold = paramDist.computeMinimumVolumeLevelSetWithThreshold(0.9)

        """
        return _dist_bundle1.Pareto_computeMinimumVolumeLevelSetWithThreshold(self, prob)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Pareto_computeEntropy(self)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Pareto_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Pareto_computeCDFGradient(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Pareto_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Pareto_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Pareto_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.Pareto_getStandardMoment(self, n)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _dist_bundle1.Pareto_getStandardRepresentative(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Pareto_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Pareto_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Pareto_getParameterDescription(self)

    def setBeta(self, beta):
        r"""
        Accessor to the distribution's scale parameter :math:`\beta`.

        Parameters
        ----------
        beta : float, :math:`\alpha \in \Rset`
            Scale parameter :math:`\beta`.
        """
        return _dist_bundle1.Pareto_setBeta(self, beta)

    def getBeta(self):
        r"""
        Accessor to the distribution's scale parameter :math:`\beta`.

        Returns
        -------
        sigma : float
            Scale parameter :math:`\beta`.
        """
        return _dist_bundle1.Pareto_getBeta(self)

    def setAlpha(self, alpha):
        r"""
        Accessor to the distribution's shape parameter :math:`\alpha`.

        Parameters
        ----------
        alpha : float, :math:`\alpha > 0`
            Shape parameter :math:`\alpha`.
        """
        return _dist_bundle1.Pareto_setAlpha(self, alpha)

    def getAlpha(self):
        r"""
        Accessor to the distribution's shape parameter :math:`\alpha`.

        Returns
        -------
        alpha : float
            Shape parameter :math:`\alpha`.
        """
        return _dist_bundle1.Pareto_getAlpha(self)

    def setGamma(self, gamma):
        r"""
        Accessor to the distribution's location parameter :math:`\gamma`.

        Parameters
        ----------
        gamma : float, :math:`u \in \Rset`
            Gamma parameter :math:`\gamma`.
        """
        return _dist_bundle1.Pareto_setGamma(self, gamma)

    def getGamma(self):
        r"""
        Accessor to the distribution's location parameter :math:`\gamma`.

        Returns
        -------
        gamma : float
            Gamma parameter :math:`\gamma`.
        """
        return _dist_bundle1.Pareto_getGamma(self)

    def __init__(self, *args):
        _dist_bundle1.Pareto_swiginit(self, _dist_bundle1.new_Pareto(*args))

    __swig_destroy__ = _dist_bundle1.delete_Pareto


_dist_bundle1.Pareto_swigregister(Pareto)

class ParetoFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Pareto factory.

    See also
    --------
    DistributionFactory, Pareto

    Notes
    -----
    Several estimators to build a Pareto distribution from a scalar sample
    are proposed.

    **Moments based estimator:**

    Lets denote:

    - :math:`\displaystyle \overline{x}_n = \frac{1}{n} \sum_{i=1}^n x_i` the empirical mean of the sample, 
    - :math:`\displaystyle s_n^2 = \frac{1}{n-1} \sum_{i=1}^n (x_i - \overline{x}_n)^2` its empirical variance,
    - :math:`\displaystyle skew_n` the empirical skewness of the sample

    The estimator :math:`(\hat{\beta}_n, \hat{\alpha}_n, \hat{\gamma}_n)` of
    :math:`(\beta, \alpha, \gamma)` is defined as follows :

    The parameter :math:`\hat{\alpha}_n` is solution of the equation: 

    .. math::
        :nowrap:

        \begin{eqnarray*}
            skew_n & =  & \dfrac{ 2(1+\hat{\alpha}_n) }{ \hat{\alpha}_n-3 } \sqrt{ \dfrac{ \hat{\alpha}_n-2 }{ \hat{\alpha}_n } } 
        \end{eqnarray*}

    There exists a symbolic solution. If :math:`\hat{\alpha}_n >3`, then we get :math:`(\hat{\beta}_n, \hat{\gamma}_n)` as follows: 

    .. math::
        :nowrap:

        \begin{eqnarray*}
           \hat{\beta}_n & = & (\hat{\alpha}_n-1) \sqrt{\dfrac{\hat{\alpha}_n-2}{\hat{\alpha}_n}}s_n \\
           \hat{\gamma}_n & = & \overline{x}_n - \dfrac{\hat{\alpha}_n}{\hat{\alpha}_n+1} \hat{\beta}_n
        \end{eqnarray*}

    **Maximum likelihood based estimator:**

    The likelihood of the sample is defined by:

    .. math::

        \ell(\alpha, \beta, \gamma|  x_1, \dots, x_n) = n\log \alpha + n\alpha \log \beta - (\alpha+1) \sum_{i=1}^n \log(x_i-\gamma)

    The maximum likelihood based estimator :math:`(\hat{\beta}_n, \hat{\alpha}_n, \hat{\gamma}_n)` of :math:`(\beta, \alpha, \gamma)` maximizes the likelihood:

    .. math::

        (\hat{\beta}_n, \hat{\alpha}_n, \hat{\gamma}_n) = \argmax_{\alpha, \beta, \gamma} \ell(\alpha, \beta, \gamma|  x_1, \dots, x_n)

    The following strategy is to be implemented soon: 
    For a given :math:`\gamma`, the likelihood of the sample is defined by:

    .. math::

        \ell(\alpha(\gamma), \beta(\gamma)|  x_1, \dots, x_n, \gamma) = n\log \alpha(\gamma) + n\alpha(\gamma) \log \beta(\gamma) - (\alpha(\gamma)+1) \sum_{i=1}^n \log(x_i-\gamma)

    We get :math:`(\hat{\beta}_n( \gamma), \hat{\alpha}_n( \gamma))` which maximizes :math:`\ell(\alpha, \beta|  x_1, \dots, x_n, \gamma)` :

    .. math::

        (\hat{\beta}_n( \gamma), \hat{\alpha}_n( \gamma)) = \argmax_{\alpha, \beta}   \ell(\alpha(\gamma), \beta(\gamma)|  x_1, \dots, x_n, \gamma) \text{ under the constraint } \gamma + \hat{\beta}_n(\gamma) \leq x_{(1,n)}

    We get:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \hat{\beta}_n( \gamma) & = & x_{(1,n)} - \gamma \\
             \hat{\alpha}_n( \gamma) & = & \dfrac{n}{\sum_{i=1}^n \log\left( \dfrac{x_i - \gamma}{\hat{\beta}_n( \gamma)}\right)}
        \end{eqnarray*}

    Then the parameter :math:`\gamma` is obtained by maximizing the likelihood :math:`\ell(\hat{\beta}_n( \gamma), \hat{\alpha}_n( \gamma), \gamma)`:

    .. math::

        \hat{\gamma}_n = \argmax_{\gamma}  \ell(\hat{\beta}_n( \gamma), \hat{\alpha}_n( \gamma), \gamma)

    The initial point of the optimisation problem is :math:`\gamma_0 = x_{(1,n)} - |x_{(1,n)}|/(2+n)`.

    **Least squares estimator:**

    The least squares estimator  :math:`(\hat{\alpha}_n, \hat{\beta}_n, \hat{\gamma}_n)` is defined by:

    .. math::

      (\hat{\alpha}_n, \hat{\beta}_n, \hat{\gamma}_n) = \argmin_{\alpha, \beta, \gamma} \sum_{i=1}^n (\hat{F}_n(x_i) - F_{\alpha, \beta, \gamma}(x_i))^2

    where :math:`\hat{F}_n` is the empirical cumulative distribution function of the sample.

    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.ParetoFactory_getClassName(self)

    def build(self, *args):
        """
        Estimate the distribution using the default strategy.

        Parameters
        ----------
        sample : :class:`~openturns.Sample`
            Data

        Returns
        -------
        distribution : :class:`~openturns.Pareto`
            The estimated distribution

        Notes
        -----
        The default strategy is using the least squares estimators.
        """
        return _dist_bundle1.ParetoFactory_build(self, *args)

    def buildAsPareto(self, *args):
        """
        Estimate the distribution as native distribution.

        Parameters
        ----------
        sample : :class:`~openturns.Sample`
            Data

        Returns
        -------
        distribution : :class:`~openturns.Pareto`
            The estimated distribution
        """
        return _dist_bundle1.ParetoFactory_buildAsPareto(self, *args)

    def buildMethodOfMoments(self, sample):
        """
        Method of moments estimator.

        Parameters
        ----------
        sample : :class:`~openturns.Sample`
            Data

        Returns
        -------
        distribution : :class:`~openturns.Pareto`
            The estimated distribution
        """
        return _dist_bundle1.ParetoFactory_buildMethodOfMoments(self, sample)

    def buildMethodOfLikelihoodMaximization(self, sample):
        """
        Method of likelihood maximization.

        Refer to :class:`~openturns.MaximumLikelihoodFactory`.

        Parameters
        ----------
        sample : :class:`~openturns.Sample`
            Data

        Returns
        -------
        distribution : :class:`~openturns.Pareto`
            The estimated distribution
        """
        return _dist_bundle1.ParetoFactory_buildMethodOfLikelihoodMaximization(self, sample)

    def buildMethodOfLeastSquares(self, sample):
        return _dist_bundle1.ParetoFactory_buildMethodOfLeastSquares(self, sample)

    def __init__(self, *args):
        _dist_bundle1.ParetoFactory_swiginit(self, _dist_bundle1.new_ParetoFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_ParetoFactory


_dist_bundle1.ParetoFactory_swigregister(ParetoFactory)

class GeneralizedPareto(openturns.model_copula.ContinuousDistribution):
    r"""
    Generalized Pareto distribution.

    Available constructors:
        GeneralizedPareto(*sigma=1.0, xi=0.0, u=0.0*)

        GeneralizedPareto(*pareto*)

    Parameters
    ----------
    sigma : float, :math:`\sigma > 0`
        Scale parameter :math:`\sigma`.
    xi : float
        Shape parameter :math:`\xi`.
    u : float
        Location parameter :math:`u`.
    pareto : :class:`~openturns.Pareto`
        Pareto distribution.

    Notes
    -----
    Its cumulative and probability distribution functions are defined as:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            F_X(x) &  = & 1-t(x), \quad \forall x \in \cS \\
            p_X(x) & = & -t'(x), \quad \forall x \in \cS
        \end{eqnarray*}

    where 

    .. math::
        :nowrap:

        \begin{eqnarray*}
            t(x) &  = & \left(1+\xi \dfrac{x-\mu}{\sigma}\right)^{-1/\xi} \quad \text{ if } \xi \neq 0\\
            t(x) &  = & \exp(-\dfrac{x-u}{\sigma}) \quad \text{ if } \xi= 0
        \end{eqnarray*}

    and 

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \cS &  = &  [u, +\infty) \quad \text{ if } \xi \geq 0\\
                &  = &  [u, u-\sigma/\xi] \quad \text{ if } \xi < 0
        \end{eqnarray*}

    with :math:`\sigma > 0` and :math:`\xi \in \Rset`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & u + \frac{\sigma}{1 - \xi}
                             \quad \text{ if } \xi < 1 \\
            \Var{X} & = & \frac{\sigma^2}{(1 - 2 \xi) (1 - \xi)^2}
                          \quad \text{ if } \xi < \frac{1}{2}
        \end{eqnarray*}

    When the constructor from a :class:`~openturns.Pareto`:math:`(\beta, \alpha, \gamma)` distribution is used,  then it creates :class:`~openturns.GeneralizedPareto`:math:`(\sigma, \xi, u)` where:

    .. math::
        :nowrap:

        \begin{eqnarray*}
           u & = & \gamma + \beta \\
           \sigma & = & \dfrac{\beta}{\alpha} \\
           \xi & = & \dfrac{1}{\alpha}
        \end{eqnarray*}

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> dist1 = ot.GeneralizedPareto(1.0, 0.0, 0.0)

    Create it from a Pareto distribution:

    >>> myPareto = Pareto(1.0, 2.0, 3.0)
    >>> dist1 = ot.GeneralizedPareto(myPareto)

    Draw a sample:

    >>> sample = dist1.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.GeneralizedPareto_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.GeneralizedPareto___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.GeneralizedPareto___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.GeneralizedPareto___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.GeneralizedPareto_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.GeneralizedPareto_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.GeneralizedPareto_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.GeneralizedPareto_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.GeneralizedPareto_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.GeneralizedPareto_computeComplementaryCDF(self, *args)

    def computeMinimumVolumeIntervalWithMarginalProbability(self, prob):
        r"""
        Compute the confidence interval with minimum volume.

        Refer to :func:`computeMinimumVolumeInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence interval of the native parameters at level 0.9 with minimum volume:

        >>> ot.ResourceMap.SetAsUnsignedInteger('Distribution-MinimumVolumeLevelSetSamplingSize', 1000)
        >>> confInt, marginalProb = paramDist.computeMinimumVolumeIntervalWithMarginalProbability(0.9)

        """
        return _dist_bundle1.GeneralizedPareto_computeMinimumVolumeIntervalWithMarginalProbability(self, prob)

    def computeMinimumVolumeLevelSetWithThreshold(self, prob):
        r"""
        Compute the confidence domain with minimum volume.

        Refer to :func:`computeMinimumVolumeLevelSet()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        levelSet : :class:`~openturns.LevelSet`
            The minimum volume domain of measure :math:`\alpha`.
        level : float
            The value :math:`p_{\alpha}` of the density function defining the frontier of the domain.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence region of minimum volume of the native parameters at level 0.9 with PDF threshold:

        >>> levelSet, threshold = paramDist.computeMinimumVolumeLevelSetWithThreshold(0.9)

        """
        return _dist_bundle1.GeneralizedPareto_computeMinimumVolumeLevelSetWithThreshold(self, prob)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.GeneralizedPareto_computeEntropy(self)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.GeneralizedPareto_computeCharacteristicFunction(self, x)

    def computeLogCharacteristicFunction(self, x):
        """
        Compute the logarithm of the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Logarithm of the characteristic function value at input :math:`t`.

        Notes
        -----
        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.

        See Also
        --------
        computeCharacteristicFunction
        """
        return _dist_bundle1.GeneralizedPareto_computeLogCharacteristicFunction(self, x)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.GeneralizedPareto_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.GeneralizedPareto_computeCDFGradient(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.GeneralizedPareto_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.GeneralizedPareto_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.GeneralizedPareto_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.GeneralizedPareto_getStandardMoment(self, n)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _dist_bundle1.GeneralizedPareto_getStandardRepresentative(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.GeneralizedPareto_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.GeneralizedPareto_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.GeneralizedPareto_getParameterDescription(self)

    def setSigma(self, sigma):
        r"""
        Accessor to the distribution's scale parameter :math:`\sigma`.

        Parameters
        ----------
        sigma : float, :math:`\sigma > 0`
            Scale parameter :math:`\sigma`.
        """
        return _dist_bundle1.GeneralizedPareto_setSigma(self, sigma)

    def getSigma(self):
        r"""
        Accessor to the distribution's scale parameter :math:`\sigma`.

        Returns
        -------
        sigma : float
            Scale parameter :math:`\sigma`.
        """
        return _dist_bundle1.GeneralizedPareto_getSigma(self)

    def setXi(self, xi):
        r"""
        Accessor to the distribution's shape parameter :math:`\xi`.

        Parameters
        ----------
        xi : float, :math:`\xi \in \Rset`
            Shape parameter :math:`\xi`.
        """
        return _dist_bundle1.GeneralizedPareto_setXi(self, xi)

    def getXi(self):
        r"""
        Accessor to the distribution's shape parameter :math:`\xi`.

        Returns
        -------
        xi : float
            Shape parameter :math:`\xi`.
        """
        return _dist_bundle1.GeneralizedPareto_getXi(self)

    def setU(self, location):
        r"""
        Accessor to the distribution's location parameter :math:`u`.

        Parameters
        ----------
        u : float, :math:`u \in \Rset`
            Location parameter :math:`u`.
        """
        return _dist_bundle1.GeneralizedPareto_setU(self, location)

    def getU(self):
        """
        Accessor to the distribution's location parameter :math:`u`.

        Returns
        -------
        u : float
            Location parameter :math:`u`.
        """
        return _dist_bundle1.GeneralizedPareto_getU(self)

    def asPareto(self):
        r"""
        Pareto distribution conversion.

        Returns
        -------
        pareto : :class:`~openturns.Pareto`
            Pareto distribution.

        Notes
        -----
        The Pareto associated to the :class:`~openturns.GeneralizedPareto`:math:`(\sigma, \xi, u)` is a  :class:`~openturns.Pareto`:math:`(\beta, \alpha, \gamma)` such that: 

        .. math::
            :nowrap:

            \begin{eqnarray*}
               \beta & = & \dfrac{\sigma}{\xi} \\
               \alpha & = & \dfrac{1}{\xi} \\
               \gamma & = & u-\dfrac{\sigma}{\xi}
            \end{eqnarray*}

        """
        return _dist_bundle1.GeneralizedPareto_asPareto(self)

    def __init__(self, *args):
        _dist_bundle1.GeneralizedPareto_swiginit(self, _dist_bundle1.new_GeneralizedPareto(*args))

    __swig_destroy__ = _dist_bundle1.delete_GeneralizedPareto


_dist_bundle1.GeneralizedPareto_swigregister(GeneralizedPareto)

class GeneralizedParetoFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Generalized Pareto factory.

    Available constructor:
        GeneralizedParetoFactory()

    Notes
    -----
    OpenTURNS proposes several estimators to build a GeneralizedPareto distribution
    from a scalar sample (see [matthys2003]_ for the theory).

    **Moments based estimator:**

    Lets denote:

    - :math:`\displaystyle \overline{x}_n = \frac{1}{n} \sum_{i=1}^n x_i` the empirical
      mean of the sample, 
    - :math:`\displaystyle s_n^2 = \frac{1}{n-1} \sum_{i=1}^n (x_i - \overline{x}_n)^2`
      its empirical variance.

    Then we estimate :math:`(\hat{\sigma}_n, \hat{\xi}_n)` using:

    .. math::
        :nowrap:
        :label: gpd_moment_estimator

        \begin{eqnarray*}
            \hat{\xi}_n &= \dfrac{1}{2}\left(\dfrac{\overline{x}_n^2}{s_n^2}-1\right) \\
            \hat{\sigma}_n &= \dfrac{\overline{x}_n}{2}\left(\dfrac{\overline{x}_n^2}{s_n^2}+1\right)
        \end{eqnarray*}

    This estimator is well-defined only if :math:`\hat{\xi}>-1/4`, otherwise the second moment does not exist.

    **Probability weighted moments based estimator:**

    Lets denote:

    - :math:`\left(x_{(i)}\right)_{i\in\{1,\dots,n\}}` the sample sorted in ascending order
    - :math:`m=\dfrac{1}{n}\sum_{i=1}^n\left(1-\dfrac{i-7/20}{n}\right)x_{(i)}`
    - :math:`\rho=\dfrac{m}{\overline{x}_n}`

    Then we estimate :math:`(\hat{\sigma}, \hat{\xi})`
    using:

    .. math::
        :nowrap:
        :label: gpd_probability_weighted_moment_estimator

        \begin{eqnarray*}
            \hat{\xi}_n &= \dfrac{1-4\rho}{1-2\rho} \\
            \hat{\sigma}_n &= \dfrac{2\overline{x}_n}{1-2\rho}
        \end{eqnarray*}

    This estimator is well-defined only if :math:`\hat{\xi}_n>-1/2`, otherwise the first moment does not exist.

    **Maximum likelihood based estimator:**

    These estimators are not yet implemented.

    For a given :math:`u < x_{(1,n)}`, we get :math:`(\hat{\sigma}_n(u),  \hat{\xi}_n(u)` by maximizing the likelihood of the sample :math:`\ell(\sigma(u),  \xi(u),u)`:

    .. math::

        (\hat{\sigma}_n(u), \hat{\xi}_n(u)) = \argmax_{\sigma, \xi}   \ell(\sigma(u), \xi(u)|  x_1, \dots, x_n, u) 

    The threshold :math:`u` is obtained by maximizing the optimal likelihood :math:`\ell(\hat{\sigma}_n(u),  \hat{\xi}_n(u), u)`

    .. math::

        \hat{u}_n = \argmax_{u} \ell(\hat{\sigma}_n(u),  \hat{\xi}_n(u),u) \text{ under the constraint } u < x_{(1,n)}

    The initial point of the optimisation problem is :math:`u_0 = x_{(1,n)} - |x_{(1,n)}|/(2+n)`.

    **Exponential regression based estimator:**

    Lets denote:

    - :math:`y_{i}=i\log\left(\dfrac{x_{(n-i)}-x_{(1)}}{x_{(n-i-1)}-x_{(1)}}\right)` for :math:`i\in\{1,n-3\}`

    Then we estimate :math:`(\hat{\sigma}, \hat{\xi})`
    using:

    .. math::
        :label: gpd_exponential_estimator

        \hat{\xi} &= \xi^* \\
        \hat{\sigma} &= \dfrac{2\overline{x}_n}{1-2\rho}

    Where :math:`\xi^*` maximizes:

    .. math::
        :label: gpd_xi_relation

        \sum_{i=1}^{n-2}\log\left(\dfrac{1-(j/n)^{\xi}}{\xi}\right)-\dfrac{1-(j/n)^{\xi}}{\xi}y_i

    under the constraint :math:`-1 \leq \xi \leq 1`.

    See also
    --------
    DistributionFactory, GeneralizedPareto
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.GeneralizedParetoFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build()

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float, of dimension 1
            The sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Notes
        -----
        In the first usage, the default :class:`~openturns.GeneralizedPareto` distribution is built.

        In the second usage, the parameters are evaluated according the following strategy:

        - If the sample size is less or equal to `GeneralizedParetoFactory-SmallSize` from :class:`~openturns.ResourceMap`, then the method of probability weighted moments is used. If it fails, the method of exponential regression is used.
        - Otherwise, the first method tried is the method of exponential regression, then the method of probability weighted moments if the first one fails.

        In the third usage, a :class:`~openturns.GeneralizedPareto` distribution corresponding to the given parameters is built.
        """
        return _dist_bundle1.GeneralizedParetoFactory_build(self, *args)

    def buildAsGeneralizedPareto(self, *args):
        """
        Build the distribution as a GeneralizedPareto type.

        **Available usages**:

            build()

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float, of dimension 1
            The sample from which the distribution parameters are estimated.
        param : sequence of float
            A vector of parameters of the distribution.

        """
        return _dist_bundle1.GeneralizedParetoFactory_buildAsGeneralizedPareto(self, *args)

    def getOptimizationAlgorithm(self):
        """
        Accessor to the solver.

        Returns
        -------
        solver : :class:`~openturns.OptimizationAlgorithm`
            The solver used for numerical optimization of the likelihood.
        """
        return _dist_bundle1.GeneralizedParetoFactory_getOptimizationAlgorithm(self)

    def setOptimizationAlgorithm(self, solver):
        """
        Accessor to the solver.

        Parameters
        ----------
        solver : :class:`~openturns.OptimizationAlgorithm`
            The solver used for numerical optimization of the likelihood.
        """
        return _dist_bundle1.GeneralizedParetoFactory_setOptimizationAlgorithm(self, solver)

    def buildMethodOfMoments(self, sample):
        """
        Build the distribution based on the method of moments estimator.

        Parameters
        ----------
        sample : 2-d sequence of float, of dimension 1
            The sample from which the distribution parameters are estimated.
        """
        return _dist_bundle1.GeneralizedParetoFactory_buildMethodOfMoments(self, sample)

    def buildMethodOfExponentialRegression(self, sample):
        """
        Build the distribution based on the exponential regression estimator.

        Parameters
        ----------
        sample : 2-d sequence of float, of dimension 1
            The sample from which the distribution parameters are estimated.
        """
        return _dist_bundle1.GeneralizedParetoFactory_buildMethodOfExponentialRegression(self, sample)

    def buildMethodOfProbabilityWeightedMoments(self, sample):
        """
        Build the distribution based on the probability weighted moments estimator.

        Parameters
        ----------
        sample : 2-d sequence of float, of dimension 1
            The sample from which the distribution parameters are estimated.
        """
        return _dist_bundle1.GeneralizedParetoFactory_buildMethodOfProbabilityWeightedMoments(self, sample)

    def __init__(self, *args):
        _dist_bundle1.GeneralizedParetoFactory_swiginit(self, _dist_bundle1.new_GeneralizedParetoFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_GeneralizedParetoFactory


_dist_bundle1.GeneralizedParetoFactory_swigregister(GeneralizedParetoFactory)

class Geometric(openturns.model_copula.DiscreteDistribution):
    r"""
    Geometric distribution.

    Available constructors:
        Geometric(*p=0.5*)

    Parameters
    ----------
    p : float, :math:`0 < p \leq 1`
        Success probability of the Bernoulli trial.

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        \Prob{X = k} = p (1 - p)^{k - 1},
                       \quad \forall k \in \Nset^*

    with :math:`0 < p \leq 1`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & \frac{1}{p} \\
            \Var{X} & = & \frac{1 - p}{p^2}
        \end{eqnarray*}

    See Also
    --------
    Bernoulli

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> distribution = ot.Geometric(0.5)

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Geometric_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Geometric___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Geometric___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Geometric___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Geometric_getRealization(self)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Geometric_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Geometric_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.Geometric_computeComplementaryCDF(self, *args)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Geometric_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Geometric_computeCDFGradient(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Geometric_computeEntropy(self)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.Geometric_computeCharacteristicFunction(self, x)

    def computeGeneratingFunction(self, z):
        r"""
        Compute the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        g : float
            Probability-generating function value at input :math:`X`.

        Notes
        -----
        The probability-generating function is defined as follows:

        .. math::

            G_X(z) = \Expect{z^X}, \quad z \in \Cset

        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete
        """
        return _dist_bundle1.Geometric_computeGeneratingFunction(self, z)

    def getSupport(self, *args):
        r"""
        Accessor to the support of the distribution.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval to intersect with the support of the discrete part of the distribution.

        Returns
        -------
        support : :class:`~openturns.Interval`
            The intersection of the support of the discrete part of the distribution with the given `interval`.

        Notes
        -----
        The mathematical support :math:`\supp{\vect{X}}` of the discrete part of a distribution is the collection of points with nonzero probability.

        This is yet implemented for discrete distributions only.

        See Also
        --------
        getRange
        """
        return _dist_bundle1.Geometric_getSupport(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Geometric_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Geometric_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Geometric_getKurtosis(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Geometric_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Geometric_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Geometric_getParameterDescription(self)

    def setP(self, p):
        r"""
        Accessor to the success probability parameter.

        Parameters
        ----------
        p : float, :math:`0 < p \leq 1`
            The success probability of the Bernoulli trial.
        """
        return _dist_bundle1.Geometric_setP(self, p)

    def getP(self):
        """
        Accessor to the success probability parameter.

        Returns
        -------
        p : float
            The success probability of the Bernoulli trial.
        """
        return _dist_bundle1.Geometric_getP(self)

    def __init__(self, *args):
        _dist_bundle1.Geometric_swiginit(self, _dist_bundle1.new_Geometric(*args))

    __swig_destroy__ = _dist_bundle1.delete_Geometric


_dist_bundle1.Geometric_swigregister(Geometric)

class GeometricFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Geometric factory.

    Available constructor:
        GeometricFactory()

    We use the following estimator:

    .. math::
        :nowrap:

        \begin{eqnarray*}
          \displaystyle\Hat{p}_n = \frac{1}{\bar{x}_n}
        \end{eqnarray*}

    See also
    --------
    DistributionFactory, Geometric
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.GeometricFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.GeometricFactory_build(self, *args)

    def buildAsGeometric(self, *args):
        return _dist_bundle1.GeometricFactory_buildAsGeometric(self, *args)

    def __init__(self, *args):
        _dist_bundle1.GeometricFactory_swiginit(self, _dist_bundle1.new_GeometricFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_GeometricFactory


_dist_bundle1.GeometricFactory_swigregister(GeometricFactory)

class Gumbel(openturns.model_copula.ContinuousDistribution):
    r"""
    Gumbel distribution.

    Parameters
    ----------
    beta : float
        scale parameter :math:`\beta > 0`.
    gamma : float
        position parameter :math:`\gamma`.

    Notes
    -----
    Its cumulative and probability density functions are defined as:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            F_X(x) & = & \exp \left( -  \exp \left( -\dfrac{x-\gamma}{\beta} \right) \right), \quad x \in \Rset \\
            f_X(x) & = & \dfrac{1}{\beta} \exp \left(- \dfrac{x-\gamma}{\beta} - \exp \left(- \dfrac{x-\gamma}{\beta} \right) \right), \quad x \in \Rset
        \end{eqnarray*}

    with :math:`\beta > 0` and :math:`\gamma \in \Rset`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & \gamma + \gamma_e \beta \\
            \Var{X} & = & \frac{1}{6} \pi^2 \beta^2
        \end{eqnarray*}

    where :math:`\gamma_e` is the Euler-Mascheroni constant.

    It is possible to create a Gumbel distribution from the alternative parametrizations :math:`(\mu, \sigma)`: see  :class:`~openturns.GumbelMuSigma` or :math:`(\lambda,\gamma)`: see  :class:`~openturns.GumbelLambdaGamma`. In that case, all the results are presented in that new parametrization.

    In order to use the alternative  parametrization only to create the distribution, see the example below: all the results will be presented in the native parametrization :math:`(\beta, \gamma)`.

    Examples
    --------
    Create a distribution in its native parameters :math:`(\beta, \gamma)`:

    >>> import openturns as ot
    >>> myDist = ot.Gumbel(1.0, 0.0)

    Create it from the alternative parametrization :math:`(\mu, \sigma)`:

    >>> myDist2 = ot.Gumbel()
    >>> myDist2.setParameter(ot.GumbelMuSigma()([0.58, 1.28]))

    Create it from the alternative parametrization :math:`(\lambda, \gamma)`:

    >>> myDist3 = ot.Gumbel()
    >>> myDist3.setParameter(ot.GumbelLambdaGamma()([1.0, 1.0]))

    Create it from :math:`(\mu, \sigma)` and keep that parametrization for the remaining study: 

    >>> myParam = ot.GumbelMuSigma(0.58, 1.28)
    >>> myDist4 = ot.ParametrizedDistribution(myParam)

    Create it from :math:`(\lambda, \gamma)` and keep that parametrization for the remaining study: 

    >>> myParam = ot.GumbelLambdaGamma(1.0, 1.0)
    >>> myDist5 = ot.ParametrizedDistribution(myParam)

    Draw a sample:

    >>> sample = myDist.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.Gumbel_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.Gumbel___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.Gumbel___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.Gumbel___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.Gumbel_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Gumbel_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Gumbel_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.Gumbel_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.Gumbel_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.Gumbel_computeComplementaryCDF(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.Gumbel_computeEntropy(self)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.Gumbel_computeCharacteristicFunction(self, x)

    def computeLogCharacteristicFunction(self, x):
        """
        Compute the logarithm of the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Logarithm of the characteristic function value at input :math:`t`.

        Notes
        -----
        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.

        See Also
        --------
        computeCharacteristicFunction
        """
        return _dist_bundle1.Gumbel_computeLogCharacteristicFunction(self, x)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Gumbel_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.Gumbel_computeCDFGradient(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.Gumbel_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Gumbel_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.Gumbel_getKurtosis(self)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _dist_bundle1.Gumbel_getStandardRepresentative(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.Gumbel_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.Gumbel_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.Gumbel_getParameterDescription(self)

    def setAlpha(self, alpha):
        return _dist_bundle1.Gumbel_setAlpha(self, alpha)

    def getAlpha(self):
        return _dist_bundle1.Gumbel_getAlpha(self)

    def setBeta(self, beta):
        r"""
        Accessor to the distribution's scale parameter :math:`\beta`.

        Parameters
        ----------
        beta : float, :math:`\beta > 0`
            Scale parameter :math:`\beta`.
        """
        return _dist_bundle1.Gumbel_setBeta(self, beta)

    def getBeta(self):
        r"""
        Accessor to the distribution's scale parameter :math:`\beta`.

        Returns
        -------
        beta : float
            Scale parameter :math:`\beta`.
        """
        return _dist_bundle1.Gumbel_getBeta(self)

    def setGamma(self, gamma):
        r"""
        Accessor to the distribution's position parameter :math:`\gamma`.

        Parameters
        ----------
        gamma : float, :math:`\beta \in \Rset`
            Scale parameter :math:`\gamma`.
        """
        return _dist_bundle1.Gumbel_setGamma(self, gamma)

    def getGamma(self):
        r"""
        Accessor to the distribution's position parameter :math:`\gamma`.

        Returns
        -------
        gamma : float
            Scale parameter :math:`\gamma`.
        """
        return _dist_bundle1.Gumbel_getGamma(self)

    def __init__(self, *args):
        _dist_bundle1.Gumbel_swiginit(self, _dist_bundle1.new_Gumbel(*args))

    __swig_destroy__ = _dist_bundle1.delete_Gumbel


_dist_bundle1.Gumbel_swigregister(Gumbel)

class WeibullMax(openturns.model_copula.ContinuousDistribution):
    r"""
    WeibullMax distribution.

    Parameters
    ----------
    beta : float
        Scale parameter :math:`\beta > 0`.
    alpha : float
        Shape parameter :math:`\alpha > 0`.
    gamma : float, optional
        Location parameter.

    Notes
    -----
    Its cumulative and probability density functions are defined as:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            F_X(x) & = &  \exp \left(-\left(-\frac{x - \gamma}{\beta}\right)^{\alpha}\right), \quad \forall x \in ( - \infty; \gamma] \\
            f_X(x) &  = & \frac{\alpha}{\beta}
                 \left(-\frac{x - \gamma}{\beta} \right) ^ {\alpha-1}
                 \exp \left(-\left(-\frac{x - \gamma}{\beta}\right)^{\alpha}\right),
                 \quad x \in ( - \infty; \gamma]
        \end{eqnarray*}

    with :math:`\beta > 0` and :math:`\alpha > 0`.

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \Expect{X} & = & \gamma - \beta \,\Gamma \left( 1 + \frac{1}{\alpha} \right) \\
            \Var{X} & = & \beta^2 \left( \Gamma  \left( 1 + \frac{2}{\alpha} \right) -
                         \Gamma^2  \left( 1 + \frac{1}{\alpha} \right) \right)
        \end{eqnarray*}

    where :math:`\Gamma` denotes Euler's Gamma function
    :class:`~openturns.SpecFunc_Gamma`.

    It is possible to create a WeibullMax distribution from the alternative parametrization :math:`(\mu, \sigma, \gamma)`: see  :class:`~openturns.WeibullMaxMuSigma`. In that case, all the results are presented in that new parametrization.

    In order to use the alternative  parametrization :math:`(\mu, \sigma, \gamma)` only to create the distribution, see the example below: all the results will be presented in the native parametrization :math:`(\beta, \alpha, \gamma)`.

    Note that if :math:`X` follows a WeibullMax :math:`(\beta, \alpha, \gamma)` distribution, then  :math:`(-X)` follows a WeibullMin :math:`(\beta, \alpha, -\gamma)` distribution.

    See also
    --------
    WeibullMin

    Examples
    --------
    Create a distribution from its native parameters :math:`(\beta, \alpha, \gamma)`:

    >>> import openturns as ot
    >>> myDist = ot.WeibullMax(2.0, 1.5, 3.0)

    Create it from the alternative parametrization :math:`(\mu, \sigma, \gamma)`:

    >>> myDist2 = ot.WeibullMin()
    >>> myDist2.setParameter(ot.WeibullMaxMuSigma()([2.8, 1.2, 4.6]))

    Create it from :math:`(\mu, \sigma, \gamma)` and keep that parametrization for the remaining study: 

    >>> myParam = ot.WeibullMaxMuSigma(2.8, 1.2, 4.6)
    >>> myDist3 = ot.ParametrizedDistribution(myParam)

    Draw a sample:

    >>> sample = myDist.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.WeibullMax_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.WeibullMax___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.WeibullMax___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.WeibullMax___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.WeibullMax_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.WeibullMax_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.WeibullMax_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.WeibullMax_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.WeibullMax_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.WeibullMax_computeComplementaryCDF(self, *args)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.WeibullMax_computeCharacteristicFunction(self, x)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.WeibullMax_computeEntropy(self)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.WeibullMax_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.WeibullMax_computeCDFGradient(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.WeibullMax_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.WeibullMax_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.WeibullMax_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _dist_bundle1.WeibullMax_getStandardMoment(self, n)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _dist_bundle1.WeibullMax_getStandardRepresentative(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.WeibullMax_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.WeibullMax_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.WeibullMax_getParameterDescription(self)

    def setBeta(self, beta):
        r"""
        Accessor to the distribution's scale parameter :math:`\beta`.

        Parameters
        ----------
        beta : float, :math:`\beta > 0`
            Scale parameter :math:`\beta`.
        """
        return _dist_bundle1.WeibullMax_setBeta(self, beta)

    def getBeta(self):
        r"""
        Accessor to the distribution's scale parameter :math:`\beta`.

        Returns
        -------
        beta : float
            Scale parameter :math:`\beta`.
        """
        return _dist_bundle1.WeibullMax_getBeta(self)

    def setAlpha(self, alpha):
        r"""
        Accessor to the distribution's shape parameter :math:`\alpha`.

        Parameters
        ----------
        alpha : float, :math:`\alpha > 0`
            Shape parameter :math:`\alpha`.
        """
        return _dist_bundle1.WeibullMax_setAlpha(self, alpha)

    def getAlpha(self):
        r"""
        Accessor to the distribution's shape parameter :math:`\alpha`.

        Returns
        -------
        alpha : float
            Shape parameter :math:`\alpha`.
        """
        return _dist_bundle1.WeibullMax_getAlpha(self)

    def setGamma(self, gamma):
        r"""
        Accessor to the distribution's location parameter :math:`\gamma`.

        Parameters
        ----------
        gamma : float
            Location parameter :math:`\gamma`.
        """
        return _dist_bundle1.WeibullMax_setGamma(self, gamma)

    def getGamma(self):
        r"""
        Accessor to the distribution's location parameter :math:`\gamma`.

        Returns
        -------
        gamma : float
            Location parameter :math:`\gamma`.
        """
        return _dist_bundle1.WeibullMax_getGamma(self)

    def __init__(self, *args):
        _dist_bundle1.WeibullMax_swiginit(self, _dist_bundle1.new_WeibullMax(*args))

    __swig_destroy__ = _dist_bundle1.delete_WeibullMax


_dist_bundle1.WeibullMax_swigregister(WeibullMax)

def Weibull(alpha=1.0, beta=1.0, gamma=0.0):
    openturns.common.Log.Warn('class Weibull is deprecated in favor of WeibullMax')
    scale, scale = alpha, beta
    return openturns.dist_bundle3.WeibullMax(scale, shape, gamma)


class WeibullMaxFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    WeibullMax factory.

    See also
    --------
    DistributionFactory, WeibullMax

    Notes
    -----
    Note that if :math:`X` follows a WeibullMax :math:`(\beta, \alpha, \gamma)` distribution, then  :math:`(-X)`follows a WeibullMin :math:`(\beta, \alpha, -\gamma)` distribution.
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.WeibullMaxFactory_getClassName(self)

    def build(self, *args):
        r"""
        Estimate the distribution using the default strategy.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : :class:`~openturns.Sample`
            Data
        param : Collection of  :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        distribution : :class:`~openturns.WeibullMax`
            The estimated distribution

        Notes
        -----
        Note that if :math:`X` follows a WeibullMax :math:`(\beta, \alpha, \gamma)` distribution, then  :math:`(-X)`follows a WeibullMin :math:`(\beta, \alpha, -\gamma)` distribution.
        The sample is transformed into its opposite and a WeibullMin :math:`(\beta, \alpha, \gamma)` is fitted on it. We return the WeibullMax :math:`(\beta, \alpha, -\gamma)` distribution.
        We use the default strategy of  :class:`~openturns.WeibullMinFactory`.
        """
        return _dist_bundle1.WeibullMaxFactory_build(self, *args)

    def buildAsWeibullMax(self, *args):
        """
        Estimate the distribution as native distribution.

        Parameters
        ----------
        sample : :class:`~openturns.Sample`
            Data

        Returns
        -------
        distribution : :class:`~openturns.WeibullMax`
            The estimated distribution
        """
        return _dist_bundle1.WeibullMaxFactory_buildAsWeibullMax(self, *args)

    def __init__(self, *args):
        _dist_bundle1.WeibullMaxFactory_swiginit(self, _dist_bundle1.new_WeibullMaxFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_WeibullMaxFactory


_dist_bundle1.WeibullMaxFactory_swigregister(WeibullMaxFactory)

class WeibullMaxMuSigma(openturns.model_copula.DistributionParametersImplementation):
    r"""
    WeibullMax distribution parameters.

    Parameters
    ----------
    mu : float
        Mean.
    sigma : float
        Standard deviation :math:`\sigma > 0`.
    gamma : float, optional
        Shift parameter :math:`\gamma > \mu`.

    Notes
    -----
    The native parameters :math:`\alpha` and :math:`\beta` are searched such as:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \mu & = & \gamma - \beta \,\Gamma\left(1 + \frac{1}{\alpha}\right)\\
            \sigma^2 & = & \beta^2 \left( \Gamma \left( 1 + \frac{2}{\alpha} \right) -
                         \Gamma^2 \left( 1 + \frac{1}{\alpha} \right) \right)
        \end{eqnarray*}

    The :math:`\gamma` parameter is the same.

    See also
    --------
    WeibullMax

    Examples
    --------
    Create the parameters :math:`(\mu, \sigma, \gamma)` of the WeibullMax distribution:

    >>> import openturns as ot
    >>> parameters = ot.WeibullMaxMuSigma(1.3, 1.23, 3.1)

    Convert parameters into the native parameters :math:`(\beta, \alpha, \gamma)`:

    >>> print(parameters.evaluate())
    [1.99222,1.48961,3.1]
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.WeibullMaxMuSigma_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.WeibullMaxMuSigma___eq__(self, other)

    def getDistribution(self):
        """
        Build a distribution based on a set of native parameters.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Distribution built with the native parameters.
        """
        return _dist_bundle1.WeibullMaxMuSigma_getDistribution(self)

    def gradient(self):
        r"""
        Get the gradient.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The gradient of the transformation of the native parameters into the new
            parameters.

        Notes
        -----

        If we note :math:`(p_1, \dots, p_q)` the native parameters and :math:`(p'_1, \dots, p'_q)` the new ones, then the gradient matrix is :math:`\left( \dfrac{\partial p'_i}{\partial p_j} \right)_{1 \leq i,j \leq  q}`.
        """
        return _dist_bundle1.WeibullMaxMuSigma_gradient(self)

    def __call__(self, inP):
        return _dist_bundle1.WeibullMaxMuSigma___call__(self, inP)

    def inverse(self, inP):
        """
        Convert to native parameters.

        Parameters
        ----------
        inP : sequence of float
            The non-native parameters.

        Returns
        -------
        outP : :class:`~openturns.Point`
            The native parameters.
        """
        return _dist_bundle1.WeibullMaxMuSigma_inverse(self, inP)

    def setValues(self, values):
        """
        Accessor to the parameters values.

        Parameters
        ----------
        values : sequence of float
            List of parameters values.
        """
        return _dist_bundle1.WeibullMaxMuSigma_setValues(self, values)

    def getValues(self):
        """
        Accessor to the parameters values.

        Returns
        -------
        values : :class:`~openturns.Point`
            List of parameters values.
        """
        return _dist_bundle1.WeibullMaxMuSigma_getValues(self)

    def getDescription(self):
        """
        Get the description of the parameters.

        Returns
        -------
        collection : :class:`~openturns.Description`
            List of parameters names.
        """
        return _dist_bundle1.WeibullMaxMuSigma_getDescription(self)

    def __repr__(self):
        return _dist_bundle1.WeibullMaxMuSigma___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.WeibullMaxMuSigma___str__(self, *args)

    def __init__(self, *args):
        _dist_bundle1.WeibullMaxMuSigma_swiginit(self, _dist_bundle1.new_WeibullMaxMuSigma(*args))

    __swig_destroy__ = _dist_bundle1.delete_WeibullMaxMuSigma


_dist_bundle1.WeibullMaxMuSigma_swigregister(WeibullMaxMuSigma)

class GeneralizedExtremeValue(openturns.model_copula.ContinuousDistribution):
    r"""
    Generalized ExtremeValue distribution.

    Available constructors:
        GeneralizedExtremeValue(*mu=0.0, sigma=1.0, xi=0.0*)

        GeneralizedExtremeValue(*distribution*)

    Parameters
    ----------
    mu : float
        Position parameter :math:`\mu`.
    sigma : float, :math:`\sigma > 0`
        Scale parameter :math:`\sigma >0`.
    xi : float
        Shape parameter :math:`\xi`.
    distribution : :class:`~openturns.WeibullMax`, :class:`~openturns.Frechet` or :class:`~openturns.Gumbel`
        The underlying distribution.

    Notes
    -----
    Its cumulative and probability distribution functions are defined as:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            F_X(x) &  = & \exp(-t(x)), \quad \forall x \in \cS \\
            p_X(x) & = & \dfrac{1}{\sigma}t^{1+\xi} \exp(-t(x)), \quad \forall x \in \cS
        \end{eqnarray*}

    where 

    .. math::
        :nowrap:

        \begin{eqnarray*}
            t(x) &  = & \left(1+\xi \dfrac{x-\mu}{\sigma}\right)^{-1/\xi} \quad \text{ if } \xi \neq 0\\
            t(x) &  = & \exp \left(- \dfrac{x-\mu}{\sigma}\right) \quad \text{ if } \xi= 0
        \end{eqnarray*}

    and 

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \cS &  = &  [\mu-\sigma/\xi, +\infty) \quad \text{ if } \xi > 0\\
                &  = &  \Rset \quad \text{ if } \xi = 0\\
                &  = &  (-\infty,\mu-\sigma/\xi] \quad \text{ if } \xi < 0
        \end{eqnarray*}

    Its first moments are:

    .. math::
        :nowrap:

        \begin{eqnarray*}
        \Expect{X} & = & \mu+\dfrac{\sigma}{\xi}\left(\Gamma(1-\xi)-1\right) \quad \text{ if } \xi < 1, \xi\neq 0 \\
                   & = &     \mu + \sigma\gamma_e \quad \text{ if } \xi= 0 \\
                   & = &    \infty  \quad \text{ if } \xi \geq 1
        \end{eqnarray*}

        \begin{eqnarray*}
            \Var{X} & = &  \dfrac{\sigma^2}{\xi^2}\left(\Gamma(1-2\xi)-\Gamma^2(1-\xi)\right) \quad \text{ if } \xi < 1/2, \xi\neq 0 \\
                    & = & \dfrac{1}{6} \sigma^2\pi^2 \quad \text{ if } \xi= 0 \\
                    & = & \infty \quad \text{ if } \xi \geq 1/2
        \end{eqnarray*}

    where :math:`\gamma_e` is Euler's constant.

    When the constructor from a :class:`~openturns.WeibullMax`:math:`(\beta, \alpha, \gamma)` distribution is used,  then it creates :class:`~openturns.GeneralizedExtremeValue`:math:`(\mu, \sigma, \xi)` where:

    .. math::
        :nowrap:

        \begin{eqnarray*}
           \mu & = & \gamma - \beta \\
           \sigma & = & \dfrac{\beta}{\alpha} \\
           \xi & = & -\dfrac{1}{\alpha}
        \end{eqnarray*}

    When the constructor from a :class:`~openturns.Frechet`:math:`(\beta, \alpha, \gamma)` distribution is used,  then it creates :class:`~openturns.GeneralizedExtremeValue`:math:`(\mu, \sigma, \xi)` where:

    .. math::
        :nowrap:

        \begin{eqnarray*}
           \mu & = & \gamma - \beta \\
           \sigma & = & \dfrac{\beta}{\alpha} \\
           \xi & = & \dfrac{1}{\alpha}
        \end{eqnarray*}

    When the constructor from a :class:`~openturns.Gumbel`:math:`(\beta, \gamma)` distribution is used,  then it creates :class:`~openturns.GeneralizedExtremeValue`:math:`(\mu, \sigma, \xi)` where:

    .. math::
        :nowrap:

        \begin{eqnarray*}
           \mu & = & \gamma  \\
           \sigma & = & \beta \\
           \xi & = & 0.0
        \end{eqnarray*}

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> dist1 = ot.GeneralizedExtremeValue(1.0, 2.0, -0.2)

    Create it from a Frechet distribution:

    >>> myFrechet = Frechet(1.0, 2.0, 3.0)
    >>> dist1 = ot.GeneralizedExtremeValue(myFrechet)

    Draw a sample:

    >>> sample = dist1.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.GeneralizedExtremeValue_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.GeneralizedExtremeValue___eq__(self, other)

    def __repr__(self):
        return _dist_bundle1.GeneralizedExtremeValue___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.GeneralizedExtremeValue___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _dist_bundle1.GeneralizedExtremeValue_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.GeneralizedExtremeValue_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.GeneralizedExtremeValue_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _dist_bundle1.GeneralizedExtremeValue_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _dist_bundle1.GeneralizedExtremeValue_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _dist_bundle1.GeneralizedExtremeValue_computeComplementaryCDF(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _dist_bundle1.GeneralizedExtremeValue_computeEntropy(self)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _dist_bundle1.GeneralizedExtremeValue_computeCharacteristicFunction(self, x)

    def computeLogCharacteristicFunction(self, x):
        """
        Compute the logarithm of the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Logarithm of the characteristic function value at input :math:`t`.

        Notes
        -----
        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.

        See Also
        --------
        computeCharacteristicFunction
        """
        return _dist_bundle1.GeneralizedExtremeValue_computeLogCharacteristicFunction(self, x)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.GeneralizedExtremeValue_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _dist_bundle1.GeneralizedExtremeValue_computeCDFGradient(self, *args)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _dist_bundle1.GeneralizedExtremeValue_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.GeneralizedExtremeValue_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _dist_bundle1.GeneralizedExtremeValue_getKurtosis(self)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _dist_bundle1.GeneralizedExtremeValue_getStandardRepresentative(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _dist_bundle1.GeneralizedExtremeValue_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _dist_bundle1.GeneralizedExtremeValue_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _dist_bundle1.GeneralizedExtremeValue_getParameterDescription(self)

    def setMu(self, mu):
        r"""
        Accessor to the distribution's position parameter :math:`\mu`.

        Parameters
        ----------
        mu : float
            Position parameter :math:`\mu`.
        """
        return _dist_bundle1.GeneralizedExtremeValue_setMu(self, mu)

    def getMu(self):
        r"""
        Accessor to the distribution's position parameter :math:`\mu`.

        Returns
        -------
        mu : float
            Position parameter :math:`\mu`.
        """
        return _dist_bundle1.GeneralizedExtremeValue_getMu(self)

    def setSigma(self, sigma):
        r"""
        Accessor to the distribution's scale parameter :math:`\sigma`.

        Parameters
        ----------
        sigma : float, :math:`\sigma > 0`
            Scale parameter :math:`\sigma`.
        """
        return _dist_bundle1.GeneralizedExtremeValue_setSigma(self, sigma)

    def getSigma(self):
        r"""
        Accessor to the distribution's scale parameter :math:`\sigma`.

        Returns
        -------
        sigma : float
            Scale parameter :math:`\sigma`.
        """
        return _dist_bundle1.GeneralizedExtremeValue_getSigma(self)

    def setXi(self, xi):
        r"""
        Accessor to the distribution's shape parameter :math:`\xi`.

        Parameters
        ----------
        xi : float, :math:`\xi \in \Rset`
            Shape parameter :math:`\xi`.
        """
        return _dist_bundle1.GeneralizedExtremeValue_setXi(self, xi)

    def getXi(self):
        r"""
        Accessor to the distribution's shape parameter :math:`\xi`.

        Returns
        -------
        xi : float
            Shape parameter :math:`\xi`.
        """
        return _dist_bundle1.GeneralizedExtremeValue_getXi(self)

    def setActualDistribution(self, distribution):
        """
        Accessor to the internal distribution.

        Parameters
        ----------
        distribution : :class:`~openturns.Distribution`
             The actual distribution in charge of the computation (:class:`~openturns.WeibullMax`, :class:`~openturns.Frechet`, :class:`~openturns.Gumbel`).
        """
        return _dist_bundle1.GeneralizedExtremeValue_setActualDistribution(self, distribution)

    def getActualDistribution(self):
        """
        Accessor to the internal distribution.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
             The actual distribution in charge of the computation (:class:`~openturns.WeibullMax`, :class:`~openturns.Frechet`, :class:`~openturns.Gumbel`).
        """
        return _dist_bundle1.GeneralizedExtremeValue_getActualDistribution(self)

    def asFrechet(self):
        r"""
        Temptative conversion to the underlying Frechet distribution.

        Returns
        -------
        distribution : :class:`~openturns.Frechet`
             The underlying Frechet distribution.

        Notes
        -----
        If :math:`\xi >0` then the :class:`~openturns.GeneralizedExtremeValue`:math:`(\mu, \sigma, \xi)` is actually a :class:`~openturns.Frechet`:math:`(\beta, \alpha, \gamma)` distribution where:

        .. math::
            :nowrap:

            \begin{eqnarray*}
               \beta & = & \dfrac{\sigma}{\xi} \\
               \alpha & = & \dfrac{1}{\xi} \\
               \gamma & = & \mu - \dfrac{\sigma}{\xi}
            \end{eqnarray*}

        """
        return _dist_bundle1.GeneralizedExtremeValue_asFrechet(self)

    def asWeibullMax(self):
        r"""
        Temptative conversion to the underlying WeibullMax distribution.

        Returns
        -------
        distribution : :class:`~openturns.WeibullMax`
             The underlying WeibullMax  distribution.

        Notes
        -----
        If :math:`\xi <0` then the :class:`~openturns.GeneralizedExtremeValue`:math:`(\mu, \sigma, \xi)` is actually a :class:`~openturns.WeibullMax`:math:`(\beta, \alpha, \gamma)` distribution where:

        .. math::
            :nowrap:

            \begin{eqnarray*}
               \beta & = & -\dfrac{\sigma}{\xi} \\
               \alpha & = & -\dfrac{1}{\xi} \\
               \gamma & = & \mu - \dfrac{\sigma}{\xi}
            \end{eqnarray*}

        """
        return _dist_bundle1.GeneralizedExtremeValue_asWeibullMax(self)

    def asGumbel(self):
        r"""
        Temptative conversion to the underlying Gumbel distribution.

        Returns
        -------
        distribution : :class:`~openturns.Gumbel`
             The underlying Gumbel distribution.

        Notes
        -----
        If :math:`\xi =0` then the :class:`~openturns.GeneralizedExtremeValue`:math:`(\mu, \sigma, 0.0)` is actually a :class:`~openturns.Gumbel`:math:`(\beta, \gamma)` distribution where:

        .. math::
            :nowrap:

            \begin{eqnarray*}
               \beta & = & \sigma \\
               \gamma & = & \mu 
            \end{eqnarray*}

        """
        return _dist_bundle1.GeneralizedExtremeValue_asGumbel(self)

    def __init__(self, *args):
        _dist_bundle1.GeneralizedExtremeValue_swiginit(self, _dist_bundle1.new_GeneralizedExtremeValue(*args))

    __swig_destroy__ = _dist_bundle1.delete_GeneralizedExtremeValue


_dist_bundle1.GeneralizedExtremeValue_swigregister(GeneralizedExtremeValue)

class GeneralizedExtremeValueFactory(openturns.model_copula.DistributionFactoryImplementation):
    """
    GeneralizedExtremeValue factory.

    Returns the best model among the Frechet, Gumbel and Weibull estimates
    according to the BIC criterion.

    See also
    --------
    DistributionFactory, GeneralizedExtremeValue, FrechetFactory, GumbelFactory, WeibullMaxFactory
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.GeneralizedExtremeValueFactory_getClassName(self)

    def build(self, *args):
        """
         Estimate the distribution using the default strategy.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float, of dimension 1
            Data.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        distribution : :class:`~openturns.GeneralizedExtremeValueFactory`
            The estimated distribution

        Notes
        -----
        The default strategy is trying to fit the three models :class:`~openturns.Frechet`, :class:`~openturns.Gumbel` and :class:`~openturns.WeibullMax`. Then the three models are classified w.r.t. the BIC criterion. The best one is returned.
        """
        return _dist_bundle1.GeneralizedExtremeValueFactory_build(self, *args)

    def buildEstimator(self, *args):
        r"""
        Build the distribution and the parameter distribution.

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        parameters : :class:`~openturns.DistributionParameters`
            Optional, the parametrization.

        Returns
        -------
        resDist : :class:`~openturns.DistributionFactoryResult`
            The results.

        Notes
        -----
        According to the way the native parameters of the distribution are estimated, the parameters distribution differs:

            - Moments method: the asymptotic parameters distribution is normal and estimated by Bootstrap on the initial data;
            - Maximum likelihood method with a regular model: the asymptotic parameters distribution is normal and its covariance matrix is the inverse Fisher information matrix;
            - Other methods: the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting (see :class:`~openturns.KernelSmoothing`).

        If another set of parameters is specified, the native parameters distribution is first estimated and the new distribution is determined from it:

            - if the native parameters distribution is normal and the transformation regular at the estimated parameters values: the asymptotic parameters distribution is normal and its covariance matrix determined from the inverse Fisher information matrix of the native parameters and the transformation;
            - in the other cases, the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting.

        Examples
        --------
        Create a sample from a Beta distribution:

        >>> import openturns as ot
        >>> sample = ot.Beta().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Beta distribution in the native parameters and create a :class:`~openturns.DistributionFactory`:

        >>> fittedRes = ot.BetaFactory().buildEstimator(sample)

        Fit a Beta distribution  in the alternative parametrization :math:`(\mu, \sigma, a, b)`:

        >>> fittedRes2 = ot.BetaFactory().buildEstimator(sample, ot.BetaMuSigma())
        """
        return _dist_bundle1.GeneralizedExtremeValueFactory_buildEstimator(self, *args)

    def buildAsGeneralizedExtremeValue(self, *args):
        return _dist_bundle1.GeneralizedExtremeValueFactory_buildAsGeneralizedExtremeValue(self, *args)

    def __init__(self, *args):
        _dist_bundle1.GeneralizedExtremeValueFactory_swiginit(self, _dist_bundle1.new_GeneralizedExtremeValueFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_GeneralizedExtremeValueFactory


_dist_bundle1.GeneralizedExtremeValueFactory_swigregister(GeneralizedExtremeValueFactory)

class GumbelFactory(openturns.model_copula.DistributionFactoryImplementation):
    r"""
    Gumbel factory.

    Available constructor:
        GumbelFactory()

    The parameters are estimated by method of moments:

    .. math::
        :nowrap:

        \begin{eqnarray*}
          \displaystyle\Hat{\alpha} =\frac{\pi}{\Hat{\sigma}_x\sqrt{6}}\\
          \displaystyle\Hat{\beta} =\bar{x}_n-\frac{\gamma\sqrt{6}}{\pi}\Hat{\sigma}_x\\
        \end{eqnarray*}

    with :math:`\gamma \simeq 0.57721` as Euler's constant.

    See also
    --------
    DistributionFactory, Gumbel
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.GumbelFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _dist_bundle1.GumbelFactory_build(self, *args)

    def buildEstimator(self, *args):
        r"""
        Build the distribution and the parameter distribution.

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        parameters : :class:`~openturns.DistributionParameters`
            Optional, the parametrization.

        Returns
        -------
        resDist : :class:`~openturns.DistributionFactoryResult`
            The results.

        Notes
        -----
        According to the way the native parameters of the distribution are estimated, the parameters distribution differs:

            - Moments method: the asymptotic parameters distribution is normal and estimated by Bootstrap on the initial data;
            - Maximum likelihood method with a regular model: the asymptotic parameters distribution is normal and its covariance matrix is the inverse Fisher information matrix;
            - Other methods: the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting (see :class:`~openturns.KernelSmoothing`).

        If another set of parameters is specified, the native parameters distribution is first estimated and the new distribution is determined from it:

            - if the native parameters distribution is normal and the transformation regular at the estimated parameters values: the asymptotic parameters distribution is normal and its covariance matrix determined from the inverse Fisher information matrix of the native parameters and the transformation;
            - in the other cases, the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting.

        Examples
        --------
        Create a sample from a Beta distribution:

        >>> import openturns as ot
        >>> sample = ot.Beta().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Beta distribution in the native parameters and create a :class:`~openturns.DistributionFactory`:

        >>> fittedRes = ot.BetaFactory().buildEstimator(sample)

        Fit a Beta distribution  in the alternative parametrization :math:`(\mu, \sigma, a, b)`:

        >>> fittedRes2 = ot.BetaFactory().buildEstimator(sample, ot.BetaMuSigma())
        """
        return _dist_bundle1.GumbelFactory_buildEstimator(self, *args)

    def buildAsGumbel(self, *args):
        return _dist_bundle1.GumbelFactory_buildAsGumbel(self, *args)

    def __init__(self, *args):
        _dist_bundle1.GumbelFactory_swiginit(self, _dist_bundle1.new_GumbelFactory(*args))

    __swig_destroy__ = _dist_bundle1.delete_GumbelFactory


_dist_bundle1.GumbelFactory_swigregister(GumbelFactory)

class GumbelAB(openturns.model_copula.DistributionParametersImplementation):
    r"""
    Gumbel distribution parameters.

    Parameters
    ----------
    a : float
        Location parameter.
    b : float
        Scale parameter :math:`b > 0`.

    Notes
    -----
    The native parameters  :math:`(\beta, \gamma)` are defined as follows:

    .. math::

        \beta &= b \\
        \gamma &= a

    See also
    --------
    Gumbel

    Examples
    --------
    Create the parameters :math:`(a, b)`  of the Gumbel distribution:

    >>> import openturns as ot
    >>> parameters = ot.GumbelAB(-0.5, 0.5)

    Convert parameters into the native parameters :math:`(\beta, \gamma)`:

    >>> print(parameters.evaluate())
    [0.5,-0.5]
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.GumbelAB_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.GumbelAB___eq__(self, other)

    def getDistribution(self):
        """
        Build a distribution based on a set of native parameters.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Distribution built with the native parameters.
        """
        return _dist_bundle1.GumbelAB_getDistribution(self)

    def gradient(self):
        r"""
        Get the gradient.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The gradient of the transformation of the native parameters into the new
            parameters.

        Notes
        -----

        If we note :math:`(p_1, \dots, p_q)` the native parameters and :math:`(p'_1, \dots, p'_q)` the new ones, then the gradient matrix is :math:`\left( \dfrac{\partial p'_i}{\partial p_j} \right)_{1 \leq i,j \leq  q}`.
        """
        return _dist_bundle1.GumbelAB_gradient(self)

    def __call__(self, inP):
        return _dist_bundle1.GumbelAB___call__(self, inP)

    def inverse(self, inP):
        """
        Convert to native parameters.

        Parameters
        ----------
        inP : sequence of float
            The non-native parameters.

        Returns
        -------
        outP : :class:`~openturns.Point`
            The native parameters.
        """
        return _dist_bundle1.GumbelAB_inverse(self, inP)

    def setValues(self, values):
        """
        Accessor to the parameters values.

        Parameters
        ----------
        values : sequence of float
            List of parameters values.
        """
        return _dist_bundle1.GumbelAB_setValues(self, values)

    def getValues(self):
        """
        Accessor to the parameters values.

        Returns
        -------
        values : :class:`~openturns.Point`
            List of parameters values.
        """
        return _dist_bundle1.GumbelAB_getValues(self)

    def getDescription(self):
        """
        Get the description of the parameters.

        Returns
        -------
        collection : :class:`~openturns.Description`
            List of parameters names.
        """
        return _dist_bundle1.GumbelAB_getDescription(self)

    def __repr__(self):
        return _dist_bundle1.GumbelAB___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.GumbelAB___str__(self, *args)

    def __init__(self, *args):
        _dist_bundle1.GumbelAB_swiginit(self, _dist_bundle1.new_GumbelAB(*args))

    __swig_destroy__ = _dist_bundle1.delete_GumbelAB


_dist_bundle1.GumbelAB_swigregister(GumbelAB)

class GumbelLambdaGamma(openturns.model_copula.DistributionParametersImplementation):
    r"""
    Gumbel rate/location parametrization.

    Parameters
    ----------
    lambda : float
        Rate parameter :math:`\lambda > 0`.
    gamma : float
        Location parameter.

    Notes
    -----
    The native parameters :math:`(\beta, \gamma)` are defined as follows:

    .. math::

       \beta &= \frac{1}{\lambda} \\

    The :math:`\gamma` parameter is the same.

    See also
    --------
    Gumbel

    Examples
    --------
    Create the parameters :math:`(\lambda, \gamma)` of the Gumbel distribution:

    >>> import openturns as ot
    >>> parameters = ot.GumbelLambdaGamma(2.0, 0.5)

    Convert parameters into the native parameters :math:`(\beta, \gamma)`:

    >>> print(parameters.evaluate())
    [0.5,0.5]
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.GumbelLambdaGamma_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.GumbelLambdaGamma___eq__(self, other)

    def getDistribution(self):
        """
        Build a distribution based on a set of native parameters.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Distribution built with the native parameters.
        """
        return _dist_bundle1.GumbelLambdaGamma_getDistribution(self)

    def gradient(self):
        r"""
        Get the gradient.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The gradient of the transformation of the native parameters into the new
            parameters.

        Notes
        -----

        If we note :math:`(p_1, \dots, p_q)` the native parameters and :math:`(p'_1, \dots, p'_q)` the new ones, then the gradient matrix is :math:`\left( \dfrac{\partial p'_i}{\partial p_j} \right)_{1 \leq i,j \leq  q}`.
        """
        return _dist_bundle1.GumbelLambdaGamma_gradient(self)

    def __call__(self, inP):
        return _dist_bundle1.GumbelLambdaGamma___call__(self, inP)

    def inverse(self, inP):
        """
        Convert to native parameters.

        Parameters
        ----------
        inP : sequence of float
            The non-native parameters.

        Returns
        -------
        outP : :class:`~openturns.Point`
            The native parameters.
        """
        return _dist_bundle1.GumbelLambdaGamma_inverse(self, inP)

    def setValues(self, values):
        """
        Accessor to the parameters values.

        Parameters
        ----------
        values : sequence of float
            List of parameters values.
        """
        return _dist_bundle1.GumbelLambdaGamma_setValues(self, values)

    def getValues(self):
        """
        Accessor to the parameters values.

        Returns
        -------
        values : :class:`~openturns.Point`
            List of parameters values.
        """
        return _dist_bundle1.GumbelLambdaGamma_getValues(self)

    def getDescription(self):
        """
        Get the description of the parameters.

        Returns
        -------
        collection : :class:`~openturns.Description`
            List of parameters names.
        """
        return _dist_bundle1.GumbelLambdaGamma_getDescription(self)

    def __repr__(self):
        return _dist_bundle1.GumbelLambdaGamma___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.GumbelLambdaGamma___str__(self, *args)

    def __init__(self, *args):
        _dist_bundle1.GumbelLambdaGamma_swiginit(self, _dist_bundle1.new_GumbelLambdaGamma(*args))

    __swig_destroy__ = _dist_bundle1.delete_GumbelLambdaGamma


_dist_bundle1.GumbelLambdaGamma_swigregister(GumbelLambdaGamma)

class GumbelMuSigma(openturns.model_copula.DistributionParametersImplementation):
    r"""
    Gumbel distribution parameters.

    Parameters
    ----------
    mu : float
        Mean.
    sigma : float
        Standard deviation :math:`\sigma > 0`.

    Notes
    -----
    The native parameters  :math:`(\beta, \gamma)` are defined as follows:

    .. math::
        :nowrap:

        \begin{eqnarray*}
            \mu & = & \gamma + \gamma_e \beta \\
            \sigma^2 & = & \frac{1}{6} \pi^2 \beta^2
        \end{eqnarray*}

    where :math:`\gamma_e` is the Euler-Mascheroni constant.

    See also
    --------
    Gumbel

    Examples
    --------
    Create the parameters :math:`(\mu, \sigma)` of the Gumbel distribution:

    >>> import openturns as ot
    >>> parameters = ot.GumbelMuSigma(1.5, 1.3)

    Convert parameters into the native parameters :math:`(\beta, \gamma)`:

    >>> print(parameters.evaluate())
    [1.01361,0.914931]
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _dist_bundle1.GumbelMuSigma_getClassName(self)

    def __eq__(self, other):
        return _dist_bundle1.GumbelMuSigma___eq__(self, other)

    def getDistribution(self):
        """
        Build a distribution based on a set of native parameters.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Distribution built with the native parameters.
        """
        return _dist_bundle1.GumbelMuSigma_getDistribution(self)

    def gradient(self):
        r"""
        Get the gradient.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The gradient of the transformation of the native parameters into the new
            parameters.

        Notes
        -----

        If we note :math:`(p_1, \dots, p_q)` the native parameters and :math:`(p'_1, \dots, p'_q)` the new ones, then the gradient matrix is :math:`\left( \dfrac{\partial p'_i}{\partial p_j} \right)_{1 \leq i,j \leq  q}`.
        """
        return _dist_bundle1.GumbelMuSigma_gradient(self)

    def __call__(self, inP):
        return _dist_bundle1.GumbelMuSigma___call__(self, inP)

    def inverse(self, inP):
        """
        Convert to native parameters.

        Parameters
        ----------
        inP : sequence of float
            The non-native parameters.

        Returns
        -------
        outP : :class:`~openturns.Point`
            The native parameters.
        """
        return _dist_bundle1.GumbelMuSigma_inverse(self, inP)

    def setValues(self, values):
        """
        Accessor to the parameters values.

        Parameters
        ----------
        values : sequence of float
            List of parameters values.
        """
        return _dist_bundle1.GumbelMuSigma_setValues(self, values)

    def getValues(self):
        """
        Accessor to the parameters values.

        Returns
        -------
        values : :class:`~openturns.Point`
            List of parameters values.
        """
        return _dist_bundle1.GumbelMuSigma_getValues(self)

    def getDescription(self):
        """
        Get the description of the parameters.

        Returns
        -------
        collection : :class:`~openturns.Description`
            List of parameters names.
        """
        return _dist_bundle1.GumbelMuSigma_getDescription(self)

    def __repr__(self):
        return _dist_bundle1.GumbelMuSigma___repr__(self)

    def __str__(self, *args):
        return _dist_bundle1.GumbelMuSigma___str__(self, *args)

    def __init__(self, *args):
        _dist_bundle1.GumbelMuSigma_swiginit(self, _dist_bundle1.new_GumbelMuSigma(*args))

    __swig_destroy__ = _dist_bundle1.delete_GumbelMuSigma


_dist_bundle1.GumbelMuSigma_swigregister(GumbelMuSigma)