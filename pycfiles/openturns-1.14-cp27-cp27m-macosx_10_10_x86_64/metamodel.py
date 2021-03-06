# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lib/python2.7/site-packages/openturns/metamodel.py
# Compiled at: 2019-11-13 10:37:10
"""Meta-modelling."""
from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')
if __package__ or '.' in __name__:
    from . import _metamodel
else:
    import _metamodel
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
    __swig_destroy__ = _metamodel.delete_SwigPyIterator

    def value(self):
        return _metamodel.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _metamodel.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _metamodel.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _metamodel.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _metamodel.SwigPyIterator_equal(self, x)

    def copy(self):
        return _metamodel.SwigPyIterator_copy(self)

    def next(self):
        return _metamodel.SwigPyIterator_next(self)

    def __next__(self):
        return _metamodel.SwigPyIterator___next__(self)

    def previous(self):
        return _metamodel.SwigPyIterator_previous(self)

    def advance(self, n):
        return _metamodel.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _metamodel.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _metamodel.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _metamodel.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _metamodel.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _metamodel.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _metamodel.SwigPyIterator___sub__(self, *args)

    def __iter__(self):
        return self


_metamodel.SwigPyIterator_swigregister(SwigPyIterator)

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


import openturns.base, openturns.common, openturns.typ, openturns.statistics, openturns.graph, openturns.func, openturns.geom, openturns.diff, openturns.optim, openturns.experiment, openturns.solver, openturns.algo, openturns.model_copula, openturns.weightedexperiment, openturns.orthogonalbasis, openturns.randomvector

class MetaModelResult(openturns.common.PersistentObject):
    r"""
    Data structure containing a metamodel.

    Available constructor:
        MetaModelResult(model, metaModel, residuals, relativeErrors)

    Parameters
    ----------
    model : :class:`~openturns.Function`
        Physical model approximated by a metamodel.
    metaModel : :class:`~openturns.Function`
        Definition of the response surface(s) of the model's output(s).
    residuals : sequence of float
        The residual values defined as follows for each output of the model:
        :math:`\displaystyle \frac{\sqrt{\sum_{i=1}^N (y_i - \hat{y_i})^2}}{N}`
        with :math:`y_i` the :math:`N` model's values and :math:`\hat{y_i}` the
        metamodel's values.
    relativeErrors : sequence of float
        The relative errors defined as follows for each output of the model:
        :math:`\displaystyle \frac{\sum_{i=1}^N (y_i - \hat{y_i})^2}{N \Var{\vect{Y}}}`
        with :math:`\vect{Y}` the vector of the :math:`N` model's values
        :math:`y_i` and :math:`\hat{y_i}` the metamodel's values.

    Notes
    -----
    Structure created by the method run() of :class:`~openturns.KrigingAlgorithm`
    or :class:`~openturns.FunctionalChaosAlgorithm` and obtained thanks to the
    method getResult() of these classes.

    See also
    --------
    FunctionalChaosResult
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
        return _metamodel.MetaModelResult_getClassName(self)

    def setModel(self, model):
        """
        Accessor to the model.

        Parameters
        ----------
        model : :class:`~openturns.Function`
            Physical model approximated by a metamodel.
        """
        return _metamodel.MetaModelResult_setModel(self, model)

    def getModel(self):
        """
        Accessor to the model.

        Returns
        -------
        model : :class:`~openturns.Function`
            Physical model approximated by a metamodel.
        """
        return _metamodel.MetaModelResult_getModel(self)

    def setMetaModel(self, metaModel):
        """
        Accessor to the metamodel.

        Parameters
        ----------
        metaModel : :class:`~openturns.Function`
            Metamodel.
        """
        return _metamodel.MetaModelResult_setMetaModel(self, metaModel)

    def getMetaModel(self):
        """
        Accessor to the metamodel.

        Returns
        -------
        metaModel : :class:`~openturns.Function`
            Metamodel.
        """
        return _metamodel.MetaModelResult_getMetaModel(self)

    def setResiduals(self, residuals):
        r"""
        Accessor to the residuals.

        Parameters
        ----------
        residuals : sequence of float
            The residual values defined as follows for each output of the model:
            :math:`\displaystyle \frac{\sqrt{\sum_{i=1}^N (y_i - \hat{y_i})^2}}{N}`
            with :math:`y_i` the :math:`N` model's values and :math:`\hat{y_i}` the
            metamodel's values.
        """
        return _metamodel.MetaModelResult_setResiduals(self, residuals)

    def getResiduals(self):
        r"""
        Accessor to the residuals.

        Returns
        -------
        residuals : :class:`~openturns.Point`
            The residual values defined as follows for each output of the model:
            :math:`\displaystyle \frac{\sqrt{\sum_{i=1}^N (y_i - \hat{y_i})^2}}{N}`
            with :math:`y_i` the :math:`N` model's values and :math:`\hat{y_i}` the
            metamodel's values.
        """
        return _metamodel.MetaModelResult_getResiduals(self)

    def setRelativeErrors(self, relativeErrors):
        r"""
        Accessor to the relative errors.

        Parameters
        ----------
        relativeErrors : sequence of float
            The relative errors defined as follows for each output of the model:
            :math:`\displaystyle \frac{\sum_{i=1}^N (y_i - \hat{y_i})^2}{N \Var{\vect{Y}}}`
            with :math:`\vect{Y}` the vector of the :math:`N` model's values
            :math:`y_i` and :math:`\hat{y_i}` the metamodel's values.
        """
        return _metamodel.MetaModelResult_setRelativeErrors(self, relativeErrors)

    def getRelativeErrors(self):
        r"""
        Accessor to the relative errors.

        Returns
        -------
        relativeErrors : :class:`~openturns.Point`
            The relative errors  defined as follows for each output of the model:
            :math:`\displaystyle \frac{\sum_{i=1}^N (y_i - \hat{y_i})^2}{N \Var{\vect{Y}}}`
            with :math:`\vect{Y}` the vector of the :math:`N` model's values
            :math:`y_i` and :math:`\hat{y_i}` the metamodel's values.
        """
        return _metamodel.MetaModelResult_getRelativeErrors(self)

    def __repr__(self):
        return _metamodel.MetaModelResult___repr__(self)

    def __init__(self, *args):
        _metamodel.MetaModelResult_swiginit(self, _metamodel.new_MetaModelResult(*args))

    __swig_destroy__ = _metamodel.delete_MetaModelResult


_metamodel.MetaModelResult_swigregister(MetaModelResult)

class KrigingResult(MetaModelResult):
    r"""
    Kriging result.

    Available constructors:
        KrigingResult(*inputSample, outputSample, metaModel, residuals, relativeErrors, basis, trendCoefficients, covarianceModel, covarianceCoefficients*)

        KrigingResult(*inputSample, outputSample, metaModel, residuals, relativeErrors, basis, trendCoefficients, covarianceModel, covarianceCoefficients, covarianceCholeskyFactor, covarianceHMatrix*)

    Parameters
    ----------
    inputSample, outputSample : 2-d sequence of float
        The samples :math:`(\vect{x}_k)_{1 \leq k \leq N} \in \Rset^d` and :math:`(\vect{y}_k)_{1 \leq k \leq N}\in \Rset^p`.
    metaModel : :class:`~openturns.Function`
        The meta model: :math:`\tilde{\cM}: \Rset^d \rightarrow \Rset^p`, defined in :eq:`metaModelKrigFinal`.
    residuals : :class:`~openturns.Point`
        The residual errors.
    relativeErrors : :class:`~openturns.Point`
        The relative errors.
    basis : collection of :class:`~openturns.Basis`
        Collection of the  :math:`p` functional basis: :math:`(\varphi_j^l)_{1 \leq j \leq n_l}` for each :math:`l \in [1, p]` with :math:`\varphi_j^l: \Rset^d \rightarrow \Rset`.
        Its size must be equal to zero if the trend is not estimated.
    trendCoefficients : collection of :class:`~openturns.Point`
       The trend coeffient vectors :math:`(\vect{\alpha}^1, \dots, \vect{\alpha}^p)`.
    covarianceModel : :class:`~openturns.CovarianceModel`
        Covariance function of the Gaussian process.
    covarianceCoefficients : 2-d sequence of float
        The :math:`\vect{\gamma}` defined in :eq:`gammaEq`.
    covarianceCholeskyFactor : :class:`~openturns.TriangularMatrix`
        The Cholesky factor :math:`\mat{L}` of :math:`\mat{C}`.
    covarianceHMatrix :  :class:`~openturns.HMatrix`
        The *hmat* implementation of :math:`\mat{L}`.

    Notes
    -----
    The Kriging meta model :math:`\tilde{\cM}` is defined by:

    .. math::
        :label: metaModelKrig

        \tilde{\cM}(\vect{x}) =  \vect{\mu}(\vect{x}) + \Expect{\vect{Y}(\omega, \vect{x})\,| \,\cC}

    where :math:`\cC` is the condition :math:`\vect{Y}(\omega, \vect{x}_k) = \vect{y}_k` for each :math:`k \in [1, N]`.

    Equation :eq:`metaModelKrig` writes:

    .. math::

        \tilde{\cM}(\vect{x}) = \vect{\mu}(\vect{x}) + \Cov{\vect{Y}(\omega, \vect{x}), (\vect{Y}(\omega,\vect{x}_1),\dots,\vect{Y}(\omega, \vect{x}_N))}\vect{\gamma}

    where 

    .. math::

        \Cov{\vect{Y}(\omega, \vect{x}), (\vect{Y}(\omega, \vect{x}_1),\dots,\vect{Y}(\omega, \vect{x}_N))} = \left(\mat{C}(\vect{x},\vect{x}_1)|\dots|\mat{C}(\vect{x},\vect{x}_N)\right)\in \cM_{p,NP}(\Rset)

    and 

    .. math::
        :label: gammaEq

        \vect{\gamma} = \mat{C}^{-1}(\vect{y}-\vect{m})

    At the end, the meta model writes:

    .. math::
        :label: metaModelKrigFinal

        \tilde{\cM}(\vect{x}) = \vect{\mu}(\vect{x}) + \sum_{i=1}^N \gamma_i  \mat{C}(\vect{x},\vect{x}_i)

    Examples
    --------
    Create the model :math:`\cM: \Rset \mapsto \Rset` and the samples:

    >>> import openturns as ot
    >>> f = ot.SymbolicFunction(['x'],  ['x * sin(x)'])
    >>> sampleX = [[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]]
    >>> sampleY = f(sampleX)

    Create the algorithm:

    >>> basis = ot.Basis([ot.SymbolicFunction(['x'], ['x']), ot.SymbolicFunction(['x'], ['x^2'])])
    >>> covarianceModel = ot.GeneralizedExponential([2.0], 2.0)
    >>> algoKriging = ot.KrigingAlgorithm(sampleX, sampleY, covarianceModel, basis)
    >>> algoKriging.run()

    Get the result:

    >>> resKriging = algoKriging.getResult()

    Get the meta model:

    >>> metaModel = resKriging.getMetaModel()

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
        return _metamodel.KrigingResult_getClassName(self)

    def __repr__(self):
        return _metamodel.KrigingResult___repr__(self)

    def __str__(self, *args):
        return _metamodel.KrigingResult___str__(self, *args)

    def getInputSample(self):
        """
        Accessor to the input sample.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            The input sample.
        """
        return _metamodel.KrigingResult_getInputSample(self)

    def getOutputSample(self):
        """
        Accessor to the output sample.

        Returns
        -------
        outputSample : :class:`~openturns.Sample`
            The output sample.
        """
        return _metamodel.KrigingResult_getOutputSample(self)

    def getBasisCollection(self):
        r"""
        Accessor to the collection of basis.

        Returns
        -------
        basisCollection : collection of :class:`~openturns.Basis`
            Collection of the :math:`p` function basis: :math:`(\varphi_j^l)_{1 \leq j \leq n_l}` for each :math:`l \in [1, p]` with :math:`\varphi_j^l: \Rset^d \rightarrow \Rset`.

        Notes
        -----
        If the trend is not estimated, the collection is empty. 

        """
        return _metamodel.KrigingResult_getBasisCollection(self)

    def getTrendCoefficients(self):
        r"""
        Accessor to the trend coefficients.

        Returns
        -------
        trendCoef : collection of :class:`~openturns.Point`
            The trend coefficients vectors :math:`(\vect{\alpha}^1, \dots, \vect{\alpha}^p)`

        """
        return _metamodel.KrigingResult_getTrendCoefficients(self)

    def getCovarianceModel(self):
        """
        Accessor to the covariance model.

        Returns
        -------
        covModel : :class:`~openturns.CovarianceModel`
            The covariance model of the Gaussian process *W* with its optimized parameters.

        """
        return _metamodel.KrigingResult_getCovarianceModel(self)

    def getCovarianceCoefficients(self):
        r"""
        Accessor to the covariance coefficients.

        Returns
        -------
        covCoeff : :class:`~openturns.Sample`
            The :math:`\vect{\gamma}` defined in :eq:`gammaEq`.

        """
        return _metamodel.KrigingResult_getCovarianceCoefficients(self)

    def getTransformation(self):
        """
        Accessor to the normalizing transformation.

        Returns
        -------
        transformation : :class:`~openturns.Function`
            The transformation *T* that normalizes the input sample.
        """
        return _metamodel.KrigingResult_getTransformation(self)

    def setTransformation(self, transformation):
        """
        Accessor to the normalizing transformation.

        Parameters
        ----------
        transformation : :class:`~openturns.Function`
            The transformation *T* that normalizes the input sample.
        """
        return _metamodel.KrigingResult_setTransformation(self, transformation)

    def getConditionalMean(self, *args):
        r"""
        Compute the expected mean of the Gaussian process on a point or a sample of points.

        Available usages:
            getConditionalMean(x)

            getConditionalMean(sampleX)

        Parameters
        ----------
        x : sequence of float
            The point :math:`\vect{x}` where the conditional mean of the output has to be evaluated.
        sampleX : 2-d sequence of float
             The sample :math:`(\vect{\xi}_1, \dots, \vect{\xi}_M)` where the conditional mean of the output has to be evaluated (*M* can be equal to 1).

        Returns
        -------
        condMean : :class:`~openturns.Point`
            The conditional mean :math:`\Expect{\vect{Y}(\omega, \vect{x})\, | \,  \cC}` at point :math:`\vect{x}`.
            Or the conditional mean matrix at the sample :math:`(\vect{\xi}_1, \dots, \vect{\xi}_M)`:

            .. math::

                \left(
                  \begin{array}{l}
                    \Expect{\vect{Y}(\omega, \vect{\xi}_1)\, | \,  \cC}\\
                    \dots  \\
                    \Expect{\vect{Y}(\omega, \vect{\xi}_M)\, | \,  \cC}
                  \end{array}
                \right)

        """
        return _metamodel.KrigingResult_getConditionalMean(self, *args)

    def getConditionalCovariance(self, *args):
        r"""
        Compute the expected covariance of the Gaussian process on a point (or several points).

        Available usages:
            getConditionalCovariance(x)

            getConditionalCovariance(sampleX)

        Parameters
        ----------
        x : sequence of float
            The point :math:`\vect{x}` where the conditional covariance of the output has to be evaluated.
        sampleX : 2-d sequence of float
             The sample :math:`(\vect{\xi}_1, \dots, \vect{\xi}_M)` where the conditional covariance of the output has to be evaluated (*M* can be equal to 1).

        Returns
        -------
        condCov : :class:`~openturns.CovarianceMatrix`
            The conditional covariance :math:`\Cov{\vect{Y}(\omega, \vect{x})\, | \,  \cC}` at point :math:`\vect{x}`.
            Or the conditional covariance matrix at the sample :math:`(\vect{\xi}_1, \dots, \vect{\xi}_M)`:

            .. math::

                \left(
                  \begin{array}{lcl}
                    \Sigma_{11} & \dots & \Sigma_{1M} \\
                    \dots  \\
                    \Sigma_{M1} & \dots & \Sigma_{MM}
                  \end{array}
                \right)

            where :math:`\Sigma_{ij} = \Cov{\vect{Y}(\omega, \vect{\xi}_i), \vect{Y}(\omega, \vect{\xi}_j)\, | \,  \cC}`.
        """
        return _metamodel.KrigingResult_getConditionalCovariance(self, *args)

    def getConditionalMarginalCovariance(self, *args):
        r"""
        Compute the expected covariance of the Gaussian process on a point (or several points).

        Available usages:
            getConditionalMarginalCovariance(x)

            getConditionalMarginalCovariance(sampleX)

        Parameters
        ----------
        x : sequence of float
            The point :math:`\vect{x}` where the conditional marginal covariance of the output has to be evaluated.
        sampleX : 2-d sequence of float
             The sample :math:`(\vect{\xi}_1, \dots, \vect{\xi}_M)` where the conditional marginal covariance of the output has to be evaluated (*M* can be equal to 1).

        Returns
        -------
        condCov : :class:`~openturns.CovarianceMatrix`
            The conditional covariance :math:`\Cov{\vect{Y}(\omega, \vect{x})\, | \,  \cC}` at point :math:`\vect{x}`.

        condCov : :class:`~openturns.CovarianceMatrixCollection`
            The collection of conditional covariance matrices :math:`\Cov{\vect{Y}(\omega, \vect{\xi})\, | \,  \cC}` at
            each point of the sample :math:`(\vect{\xi}_1, \dots, \vect{\xi}_M)`:

        Notes
        -----
        In case input parameter is a of type :class:`~openturns.Sample`, each element of the collection corresponds to the conditional
        covariance with respect to the input learning set (pointwise evaluation of the getConditionalCovariance).
        """
        return _metamodel.KrigingResult_getConditionalMarginalCovariance(self, *args)

    def getConditionalMarginalVariance(self, *args):
        r"""
        Compute the expected variance of the Gaussian process on a point (or several points).

        Available usages:
            getConditionalMarginalVariance(x, marginalIndex)

            getConditionalMarginalVariance(sampleX, marginalIndex)

            getConditionalMarginalVariance(x, marginalIndices)

            getConditionalMarginalVariance(sampleX, marginalIndices)

        Parameters
        ----------
        x : sequence of float
            The point :math:`\vect{x}` where the conditional variance of the output has to be evaluated.
        sampleX : 2-d sequence of float
             The sample :math:`(\vect{\xi}_1, \dots, \vect{\xi}_M)` where the conditional variance of the output has to be evaluated (*M* can be equal to 1).
        marginalIndex : int
            Marginal of interest (for multiple outputs).
            Default value is 0
        marginalIndices : sequence of int
            Marginals of interest (for multiple outputs).

        Returns
        -------
        var : float
              Variance of interest.
              float if one point (x) and one marginal of interest (x, marginalIndex)

        varPoint : sequence of float
            The marginal variances

        Notes
        -----
        In case of fourth usage, the sequence of float is given as the concatenation of marginal variances 
        for each point in sampleX.
        """
        return _metamodel.KrigingResult_getConditionalMarginalVariance(self, *args)

    def __call__(self, *args):
        return _metamodel.KrigingResult___call__(self, *args)

    def __init__(self, *args):
        _metamodel.KrigingResult_swiginit(self, _metamodel.new_KrigingResult(*args))

    __swig_destroy__ = _metamodel.delete_KrigingResult


_metamodel.KrigingResult_swigregister(KrigingResult)

class LinearModelResult(MetaModelResult):
    """
    Result of a LinearModelAlgorithm.

    Parameters
    ----------
    inputSample : 2-d sequence of float
        The input sample of a model.
    basis : :class:`~openturns.Basis`
        Functional basis to estimate the trend.
    design : :class:`~openturns.Matrix`
        The design matrix :math:`X`.
    outputSample : 2-d sequence of float
       The output sample of a model.
    metaModel : :class:`~openturns.Function`
        The meta model.
    trendCoefficients : sequence of float
        The trend coeffients associated to the linearmodel. 
    formula : str
         The formula description. 
    coefficientsNames : sequence of str
         The coefficients names of the basis.  
    sampleResiduals : 2-d sequence of float
        The residual errors.
    standardizedSampleResiduals : 2-d sequence of float
        The normalized residual errors.
    diagonalGramInverse : sequence of float
        The diagonal of the Gram inverse matrix.
    leverages : sequence of float
        The leverage score. 
    cookDistances : sequence of float
        The cook's distances.
    sigma2 : float
        The unbiased noise variance.

    See Also
    --------
    LinearModelAlgorithm

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
        return _metamodel.LinearModelResult_getClassName(self)

    def __repr__(self):
        return _metamodel.LinearModelResult___repr__(self)

    def getBasis(self):
        """
        Accessor to the basis.

        Returns
        -------
        basis : :class:`~openturns.Basis`
            The basis which had been passed to the constructor.
        """
        return _metamodel.LinearModelResult_getBasis(self)

    def getInputSample(self):
        """
        Accessor to the input sample.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            The Xsample which had been passed to the constructor.
        """
        return _metamodel.LinearModelResult_getInputSample(self)

    def getOutputSample(self):
        """
        Accessor to the output sample.

        Returns
        -------
        outputSample : :class:`~openturns.Sample`
            The Ysample which had been passed to the constructor.
        """
        return _metamodel.LinearModelResult_getOutputSample(self)

    def getFittedSample(self):
        """
        Accessor to the fitted sample.

        Returns
        -------
        outputSample : :class:`~openturns.Sample`

        """
        return _metamodel.LinearModelResult_getFittedSample(self)

    def getCoefficients(self):
        """
        Accessor to the coefficients of the linear model of the trend.

        Returns
        -------
        beta : :class:`~openturns.Point`

        """
        return _metamodel.LinearModelResult_getCoefficients(self)

    def getCoefficientsStandardErrors(self):
        """
        Accessor to the coefficients of standard error.

        Returns
        -------
        standardErrors : :class:`~openturns.Point`

        """
        return _metamodel.LinearModelResult_getCoefficientsStandardErrors(self)

    def getFormula(self):
        """
        Accessor to the formula.

        Returns
        -------
        condensedFormula : str

        """
        return _metamodel.LinearModelResult_getFormula(self)

    def getCoefficientsNames(self):
        """
        Accessor to the coefficients names.

        Returns
        -------
        coefficientsNames : :class:`~openturns.Description`

        """
        return _metamodel.LinearModelResult_getCoefficientsNames(self)

    def getSampleResiduals(self):
        """
        Accessor to the residuals.

        Returns
        -------
        sampleResiduals : :class:`~openturns.Sample`

        """
        return _metamodel.LinearModelResult_getSampleResiduals(self)

    def getNoiseDistribution(self):
        """
        Accessor to the noise distribution, ie the underlying distribution of the residual.

        Returns
        -------
        noiseDistribution : :class:`~openturns.Distribution`

        """
        return _metamodel.LinearModelResult_getNoiseDistribution(self)

    def getStandardizedResiduals(self):
        """
        Accessor to the standardized residuals.

        Returns
        -------
        standardizedResiduals : :class:`~openturns.Sample`

        """
        return _metamodel.LinearModelResult_getStandardizedResiduals(self)

    def getDegreesOfFreedom(self):
        """
        Accessor to the degrees of freedom.

        Returns
        -------
        dof : int

        """
        return _metamodel.LinearModelResult_getDegreesOfFreedom(self)

    def getLeverages(self):
        """
        Accessor to the leverages.

        Returns
        -------
        leverages : :class:`~openturns.Point`

        """
        return _metamodel.LinearModelResult_getLeverages(self)

    def getDiagonalGramInverse(self):
        """
        Accessor to the diagonal gram inverse matrix.

        Returns
        -------
        diagonalGramInverse : :class:`~openturns.Point`

        """
        return _metamodel.LinearModelResult_getDiagonalGramInverse(self)

    def getCookDistances(self):
        """
        Accessor to the cook's distances.

        Returns
        -------
        cookDistances : :class:`~openturns.Point`

        """
        return _metamodel.LinearModelResult_getCookDistances(self)

    def getRSquared(self):
        """
        Accessor to the R-squared test.

        Returns
        -------
        rSquared : float

        """
        return _metamodel.LinearModelResult_getRSquared(self)

    def getAdjustedRSquared(self):
        """
        Accessor to the Adjusted R-squared test.

        Returns
        -------
        adjustedRSquared : float

        """
        return _metamodel.LinearModelResult_getAdjustedRSquared(self)

    def __init__(self, *args):
        _metamodel.LinearModelResult_swiginit(self, _metamodel.new_LinearModelResult(*args))

    __swig_destroy__ = _metamodel.delete_LinearModelResult


_metamodel.LinearModelResult_swigregister(LinearModelResult)

class MetaModelAlgorithm(openturns.common.PersistentObject):
    """
    Base class to compute a metamodel.

    Available constructor:
        MetaModelAlgorithm(*distribution, model*)

    Parameters
    ----------
    distribution : :class:`~openturns.Distribution`
        Joint probability density function of the physical input vector.
    model : :class:`~openturns.Function`
        Physical model to be approximated by a metamodel.

    Notes
    -----
    A MetaModelAlgorithm object can be used only through its derived classes:

    - :class:`~openturns.KrigingAlgorithm`

    - :class:`~openturns.FunctionalChaosAlgorithm`
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
        return _metamodel.MetaModelAlgorithm_getClassName(self)

    def __repr__(self):
        return _metamodel.MetaModelAlgorithm___repr__(self)

    def setDistribution(self, distribution):
        """
        Accessor to the joint probability density function of the physical input vector.

        Parameters
        ----------
        distribution : :class:`~openturns.Distribution`
            Joint probability density function of the physical input vector.
        """
        return _metamodel.MetaModelAlgorithm_setDistribution(self, distribution)

    def getDistribution(self):
        """
        Accessor to the joint probability density function of the physical input vector.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Joint probability density function of the physical input vector.
        """
        return _metamodel.MetaModelAlgorithm_getDistribution(self)

    def run(self):
        """
        Compute the response surfaces.

        Notes
        -----
        It computes the response surfaces and creates a
        :class:`~openturns.MetaModelResult` structure containing all the results.
        """
        return _metamodel.MetaModelAlgorithm_run(self)

    def getInputSample(self):
        """
        Accessor to the input sample.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            Input sample of a model evaluated apart.
        """
        return _metamodel.MetaModelAlgorithm_getInputSample(self)

    def getOutputSample(self):
        """
        Accessor to the output sample.

        Returns
        -------
        outputSample : :class:`~openturns.Sample`
            Output sample of a model evaluated apart.
        """
        return _metamodel.MetaModelAlgorithm_getOutputSample(self)

    def __init__(self, *args):
        _metamodel.MetaModelAlgorithm_swiginit(self, _metamodel.new_MetaModelAlgorithm(*args))

    __swig_destroy__ = _metamodel.delete_MetaModelAlgorithm


_metamodel.MetaModelAlgorithm_swigregister(MetaModelAlgorithm)

class LinearTaylor(openturns.common.PersistentObject):
    r"""
    First order polynomial response surface by Taylor expansion.

    Available constructors:
        LinearTaylor(*center, function*)

    Parameters
    ----------
    center : sequence of float
        Point :math:`\vect{x}_0` where the Taylor expansion of the function
        :math:`h` is performed.
    function : :class:`~openturns.Function`
        Function :math:`h` to be approximated.

    Notes
    -----
    The approximation of the model response :math:`\vect{y} = h(\vect{x})` around a
    specific set :math:`\vect{x}_0 = (x_{0,1},\dots,x_{0,n_{X}})` of input
    parameters may be of interest. One may then substitute :math:`h` for its Taylor
    expansion at point :math:`\vect{x}_0`. Hence :math:`h` is replaced with a first
    or second-order polynomial :math:`\widehat{h}` whose evaluation is inexpensive,
    allowing the analyst to apply the uncertainty anaysis methods.

    We consider here the first order Taylor expansion around :math:`\ux=\vect{x}_0`.

    .. math::

        \vect{y} \, \approx \, \widehat{h}(\vect{x}) \,
          = \, h(\vect{x}_0) \, +
            \, \sum_{i=1}^{n_{X}} \; \frac{\partial h}{\partial x_i}(\vect{x}_0).\left(x_i - x_{0,i} \right)

    Introducing a vector notation, the previous equation rewrites:

    .. math::

        \vect{y} \, \approx \, \vect{y}_0 \, + \, \vect{\vect{L}} \: \left(\vect{x}-\vect{x}_0\right)

    where:

    - :math:`\vect{y_0} = (y_{0,1} , \dots, y_{0,n_Y})^{\textsf{T}} = h(\vect{x}_0)`
      is the vector model response evaluated at :math:`\vect{x}_0`;
    - :math:`\vect{x}` is the current set of input parameters;
    - :math:`\vect{\vect{L}} = \left( \frac{\partial y_{0,j}}{\partial x_i} \,,\, i=1,\ldots, n_X \,,\, j=1,\ldots, n_Y \right)`
      is the transposed Jacobian matrix evaluated at :math:`\vect{x}_0`.

    See also
    --------
    QuadraticTaylor, LinearLeastSquares, QuadraticLeastSquares

    Examples
    --------
    >>> import openturns as ot
    >>> formulas = ['x1 * sin(x2)', 'cos(x1 + x2)', '(x2 + 1) * exp(x1 - 2 * x2)']
    >>> myFunc = ot.SymbolicFunction(['x1', 'x2'], formulas)
    >>> myTaylor = ot.LinearTaylor([1, 2], myFunc)
    >>> myTaylor.run()
    >>> responseSurface = myTaylor.getMetaModel()
    >>> print(responseSurface([1.2,1.9]))
    [1.13277,-1.0041,0.204127]
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
        return _metamodel.LinearTaylor_getClassName(self)

    def __repr__(self):
        return _metamodel.LinearTaylor___repr__(self)

    def run(self):
        r"""Perform the Linear Taylor expansion around :math:`\vect{x}_0`."""
        return _metamodel.LinearTaylor_run(self)

    def getCenter(self):
        r"""
        Get the center.

        Returns
        -------
        center : :class:`~openturns.Point`
            Point :math:`\vect{x}_0` where the Taylor expansion of the function is
            performed.
        """
        return _metamodel.LinearTaylor_getCenter(self)

    def getConstant(self):
        """
        Get the constant vector of the approximation.

        Returns
        -------
        constantVector : :class:`~openturns.Point`
            Constant vector of the approximation, equal to :math:`h(x_0)`.
        """
        return _metamodel.LinearTaylor_getConstant(self)

    def getLinear(self):
        r"""
        Get the gradient of the function at :math:`\vect{x}_0`.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            Gradient of the function :math:`h` at the point :math:`\vect{x}_0` (the
            transposition of the jacobian matrix).
        """
        return _metamodel.LinearTaylor_getLinear(self)

    def getInputFunction(self):
        """
        Get the function.

        Returns
        -------
        function : :class:`~openturns.Function`
            Function :math:`h` to be approximated.
        """
        return _metamodel.LinearTaylor_getInputFunction(self)

    def getMetaModel(self):
        r"""
        Get an approximation of the function.

        Returns
        -------
        approximation : :class:`~openturns.Function`
            An approximation of the function :math:`h` by a Linear Taylor expansion at
            the point :math:`\vect{x}_0`.
        """
        return _metamodel.LinearTaylor_getMetaModel(self)

    def __init__(self, *args):
        _metamodel.LinearTaylor_swiginit(self, _metamodel.new_LinearTaylor(*args))

    __swig_destroy__ = _metamodel.delete_LinearTaylor


_metamodel.LinearTaylor_swigregister(LinearTaylor)

class QuadraticTaylor(openturns.common.PersistentObject):
    r"""
    Second order polynomial response surface by Taylor expansion.

    Available constructors:
        QuadraticTaylor(*center, function*)

    Parameters
    ----------
    center : sequence of float
        Point :math:`\vect{x}_0` where the Taylor expansion of the function
        :math:`h` is performed.
    function : :class:`~openturns.Function`
        Function :math:`h` to be approximated.

    Notes
    -----
    The approximation of the model response :math:`\vect{y} = h(\vect{x})` around a
    specific set :math:`\vect{x}_0 = (x_{0,1},\dots,x_{0,n_{X}})` of input
    parameters may be of interest. One may then substitute :math:`h` for its Taylor
    expansion at point :math:`\vect{x}_0`. Hence :math:`h` is replaced with a first
    or second-order polynomial :math:`\widehat{h}` whose evaluation is inexpensive,
    allowing the analyst to apply the uncertainty anaysis methods.

    We consider here the second order Taylor expansion around :math:`\ux=\vect{x}_0`.

    .. math::

        \vect{y} \, \approx \, \widehat{h}(\vect{x}) \, = \,
         h(\vect{x}_0) \, + \, \sum_{i=1}^{n_{X}} \;
          \frac{\partial h}{\partial x_i}(\vect{x}_0).\left(x_i - x_{0,i} \right) \, +
         \, \frac{1}{2} \; \sum_{i,j=1}^{n_X} \;
          \frac{\partial^2 h}{\partial x_i \partial x_j}(\vect{x}_0).\left(x_i - x_{0,i} \right).\left(x_j - x_{0,j} \right)

    Introducing a vector notation, the previous equation rewrites:

    .. math::

        \vect{y} \, \approx \,
         \vect{y}_0 \, +
         \, \vect{\vect{L}} \: \left(\vect{x}-\vect{x}_0\right) \, +
         \, \frac{1}{2} \; \left\langle \left\langle\vect{\vect{\vect{Q}}}\:,
                                                          \vect{x}-\vect{x}_0 \right\rangle,
                                                    \:\vect{x}-\vect{x}_0 \right\rangle

    where

    - :math:`\vect{y_0} = (y_{0,1} , \dots, y_{0,n_Y})^{\textsf{T}} = h(\vect{x}_0)`
      is the vector model response evaluated at :math:`\vect{x}_0` ;
    - :math:`\vect{x}` is the current set of input parameters ;
    - :math:`\vect{\vect{L}} = \left( \frac{\partial y_{0,j}}{\partial x_i} \,,\, i=1,\ldots, n_X \,,\, j=1,\ldots, n_Y \right)`
      is the transposed Jacobian matrix evaluated at :math:`\vect{x}_0` ;
    - :math:`\vect{\vect{Q}} = \left\{ \frac{\partial^2 y_{0,k}}{\partial x_i \partial x_j} \, \, , \, \, i,j=1,\ldots, n_X \, \, , \, \, k=1, \ldots, n_Y \right\}`
      is the transposed Hessian matrix.

    See also
    --------
    LinearTaylor, LinearLeastSquares, QuadraticLeastSquares

    Examples
    --------
    >>> import openturns as ot
    >>> formulas = ['x1 * sin(x2)', 'cos(x1 + x2)', '(x2 + 1) * exp(x1 - 2 * x2)']
    >>> myFunc = ot.SymbolicFunction(['x1', 'x2'], formulas)
    >>> myTaylor = ot.QuadraticTaylor([1, 2], myFunc)
    >>> myTaylor.run()
    >>> responseSurface = myTaylor.getMetaModel()
    >>> print(responseSurface([1.2,1.9]))
    [1.13655,-0.999155,0.214084]
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
        return _metamodel.QuadraticTaylor_getClassName(self)

    def __repr__(self):
        return _metamodel.QuadraticTaylor___repr__(self)

    def run(self):
        r"""Perform the Quadratic Taylor expansion around :math:`\vect{x}_0`."""
        return _metamodel.QuadraticTaylor_run(self)

    def getCenter(self):
        r"""
        Get the center.

        Returns
        -------
        center : :class:`~openturns.Point`
            Point :math:`\vect{x}_0` where the Taylor expansion of the function is
            performed.
        """
        return _metamodel.QuadraticTaylor_getCenter(self)

    def getConstant(self):
        """
        Get the constant vector of the approximation.

        Returns
        -------
        constantVector : :class:`~openturns.Point`
            Constant vector of the approximation, equal to :math:`h(x_0)`.
        """
        return _metamodel.QuadraticTaylor_getConstant(self)

    def getLinear(self):
        r"""
        Get the gradient of the function at :math:`\vect{x}_0`.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            Gradient of the function :math:`h` at the point :math:`\vect{x}_0` (the
            transposition of the jacobian matrix).
        """
        return _metamodel.QuadraticTaylor_getLinear(self)

    def getQuadratic(self):
        r"""
        Get the hessian of the function at :math:`\vect{x}_0`.

        Returns
        -------
        tensor : :class:`~openturns.SymmetricTensor`
            Hessian of the function :math:`h` at the point :math:`\vect{x}_0`.
        """
        return _metamodel.QuadraticTaylor_getQuadratic(self)

    def getInputFunction(self):
        """
        Get the function.

        Returns
        -------
        function : :class:`~openturns.Function`
            Function :math:`h` to be approximated.
        """
        return _metamodel.QuadraticTaylor_getInputFunction(self)

    def getMetaModel(self):
        r"""
        Get an approximation of the function.

        Returns
        -------
        approximation : :class:`~openturns.Function`
            An approximation of the function :math:`h` by a Quadratic Taylor expansion
            at the point :math:`\vect{x}_0`.
        """
        return _metamodel.QuadraticTaylor_getMetaModel(self)

    def __init__(self, *args):
        _metamodel.QuadraticTaylor_swiginit(self, _metamodel.new_QuadraticTaylor(*args))

    __swig_destroy__ = _metamodel.delete_QuadraticTaylor


_metamodel.QuadraticTaylor_swigregister(QuadraticTaylor)

class LinearLeastSquares(openturns.common.PersistentObject):
    r"""
    First order polynomial response surface by least squares.

    Available constructors:
        LinearLeastSquares(*dataIn, function*)

        LinearLeastSquares(*dataIn, dataOut*)

    Parameters
    ----------
    dataIn : 2-d sequence of float
        Input data.
    function : :class:`~openturns.Function`
        Function :math:`h` to be approximated.
    dataOut : 2-d sequence of float
        Output data. If not specified, this sample is computed such as:
        :math:`dataOut = h(dataIn)`.

    Notes
    -----
    Instead of replacing the model response :math:`h(\vect{x})` for a *local*
    approximation around a given set :math:`\vect{x}_0` of input parameters as in
    Taylor approximations, one may seek a *global* approximation of
    :math:`h(\vect{x})` over its whole domain of definition. A common choice to
    this end is global polynomial approximation.

    We consider here a global approximation of the model response using  a linear
    function:

    .. math::

        \vect{y} \, \approx \, \widehat{h}(\vect{x}) \,
                          = \, \sum_{j=0}^{n_X} \; a_j \; \psi_j(\vect{x})

    where :math:`(a_j  \, , \, j=0, \cdots,n_X)` is a set of unknown coefficients
    and the family :math:`(\psi_j,j=0,\cdots, n_X)` gathers the constant monomial
    :math:`1` and the monomials of degree one :math:`x_i`. Using the vector
    notation :math:`\vect{a} \, = \, (a_{0} , \cdots , a_{n_X} )^{\textsf{T}}` and
    :math:`\vect{\psi}(\vect{x}) \, = \, (\psi_0(\vect{x}), \cdots, \psi_{n_X}(\vect{x}) )^{\textsf{T}}`,
    this rewrites:

    .. math::

        \vect{y} \, \approx \, \widehat{h}(\vect{x}) \,
                          = \, \vect{a}^{\textsf{T}} \; \vect{\psi}(\vect{x})

    A *global* approximation of the model response over its whole definition domain
    is sought. To this end, the coefficients :math:`a_j` may be computed using a
    least squares regression approach. In this context, an experimental design
    :math:`\vect{\cX} =(x^{(1)},\cdots,x^{(N)})`, i.e. a set of realizations of
    input parameters is required, as well as the corresponding model evaluations
    :math:`\vect{\cY} =(y^{(1)},\cdots,y^{(N)})`.

    The following minimization problem has to be solved:

    .. math::

        \mbox{Find} \quad \widehat{\vect{a}} \quad \mbox{that minimizes}
          \quad \cJ(\vect{a}) \, = \, \sum_{i=1}^N \;
                                    \left(
                                    y^{(i)} \; - \;
                                    \vect{a}^{\textsf{T}} \vect{\psi}(\vect{x}^{(i)})
                                    \right)^2

    The solution is given by:

    .. math::

        \widehat{\vect{a}} \, = \, \left(
                                   \vect{\vect{\Psi}}^{\textsf{T}} \vect{\vect{\Psi}}
                                   \right)^{-1} \;
                                   \vect{\vect{\Psi}}^{\textsf{T}}  \; \vect{\cY}

    where:

    .. math::

        \vect{\vect{\Psi}} \, = \, (\psi_{j}(\vect{x}^{(i)}) \; , \; i=1,\cdots,N \; , \; j = 0,\cdots,n_X)

    See also
    --------
    QuadraticLeastSquares, LinearTaylor, QuadraticTaylor

    Examples
    --------
    >>> import openturns as ot
    >>> formulas = ['cos(x1 + x2)', '(x2 + 1) * exp(x1 - 2 * x2)']
    >>> myFunc = ot.SymbolicFunction(['x1', 'x2'], formulas)
    >>> data  = [[0.5,0.5], [-0.5,-0.5], [-0.5,0.5], [0.5,-0.5]]
    >>> data += [[0.25,0.25], [-0.25,-0.25], [-0.25,0.25], [0.25,-0.25]]
    >>> myLeastSquares = ot.LinearLeastSquares(data, myFunc)
    >>> myLeastSquares.run()
    >>> responseSurface = myLeastSquares.getMetaModel()
    >>> print(responseSurface([0.1,0.1]))
    [0.854471,1.06031]
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
        return _metamodel.LinearLeastSquares_getClassName(self)

    def __repr__(self):
        return _metamodel.LinearLeastSquares___repr__(self)

    def run(self):
        """Perform the least squares approximation."""
        return _metamodel.LinearLeastSquares_run(self)

    def getConstant(self):
        """
        Get the constant vector of the approximation.

        Returns
        -------
        constantVector : :class:`~openturns.Point`
            Constant vector of the approximation, equal to :math:`a_0`.
        """
        return _metamodel.LinearLeastSquares_getConstant(self)

    def getLinear(self):
        """
        Get the linear matrix of the approximation.

        Returns
        -------
        linearMatrix : :class:`~openturns.Matrix`
            Linear matrix of the approximation of the function :math:`h`.
        """
        return _metamodel.LinearLeastSquares_getLinear(self)

    def getInputFunction(self):
        """
        Get the function.

        Returns
        -------
        function : :class:`~openturns.Function`
            Function :math:`h` to be approximated.
        """
        return _metamodel.LinearLeastSquares_getInputFunction(self)

    def getMetaModel(self):
        """
        Get an approximation of the function.

        Returns
        -------
        approximation : :class:`~openturns.Function`
            An approximation of the function :math:`h` by Linear Least Squares.
        """
        return _metamodel.LinearLeastSquares_getMetaModel(self)

    def getDataIn(self):
        """
        Get the input data.

        Returns
        -------
        dataIn : :class:`~openturns.Sample`
            Input data.
        """
        return _metamodel.LinearLeastSquares_getDataIn(self)

    def setDataOut(self, dataOut):
        """
        Set the output data.

        Parameters
        ----------
        dataOut : 2-d sequence of float
            Output data.
        """
        return _metamodel.LinearLeastSquares_setDataOut(self, dataOut)

    def getDataOut(self):
        """
        Get the output data.

        Returns
        -------
        dataOut : :class:`~openturns.Sample`
            Output data. If not specified in the constructor, the sample is computed
            such as: :math:`dataOut = h(dataIn)`.
        """
        return _metamodel.LinearLeastSquares_getDataOut(self)

    def __init__(self, *args):
        _metamodel.LinearLeastSquares_swiginit(self, _metamodel.new_LinearLeastSquares(*args))

    __swig_destroy__ = _metamodel.delete_LinearLeastSquares


_metamodel.LinearLeastSquares_swigregister(LinearLeastSquares)

class QuadraticLeastSquares(openturns.common.PersistentObject):
    r"""
    Second order polynomial response surface by least squares.

    Available constructors:
        QuadraticLeastSquares(*dataIn, function*)

        QuadraticLeastSquares(*dataIn, dataOut*)

    Parameters
    ----------
    dataIn : 2-d sequence of float
        Input data.
    function : :class:`~openturns.Function`
        Function :math:`h` to be approximated.
    dataOut : 2-d sequence of float
        Output data. If not specified, this sample is computed such as:
        :math:`dataOut = h(dataIn)`.

    Notes
    -----
    Instead of replacing the model response :math:`h(\vect{x})` for a *local*
    approximation around a given set :math:`\vect{x}_0` of input parameters as in
    Taylor approximations, one may seek a *global* approximation of
    :math:`h(\vect{x})` over its whole domain of definition. A common choice to
    this end is global polynomial approximation.

    We consider here a global approximation of the model response using  a
    quadratic function:

    .. math::

        \vect{y} \, \approx \, \widehat{h}(\vect{x}) \,
                          = \, \sum_{j=0}^{P-1} \; a_j \; \psi_j(\vect{x})

    where :math:`P = 1+2n_X +n_X (n_X -1)/2` denotes the number of terms,
    :math:`(a_j  \, , \, j=0, \cdots,P-1)` is a set of unknown coefficients and the
    family :math:`(\psi_j,j=0,\cdots, P-1)` gathers the constant monomial :math:`1`,
    the monomials of degree one :math:`x_i`, the cross-terms :math:`x_i x_j` as
    well as the monomials of degree two :math:`x_i^2`. Using the vector notation
    :math:`\vect{a} \, = \, (a_{0} , \cdots , a_{P-1} )^{\textsf{T}}` and
    :math:`\vect{\psi}(\vect{x}) \, = \, (\psi_0(\vect{x}), \cdots, \psi_{P-1}(\vect{x}) )^{\textsf{T}}`,
    this rewrites:

    .. math::

        \vect{y} \, \approx \, \widehat{h}(\vect{x}) \,
                          = \, \vect{a}^{\textsf{T}} \; \vect{\psi}(\vect{x})

    A *global* approximation of the model response over its whole definition domain
    is sought. To this end, the coefficients :math:`a_j` may be computed using a
    least squares regression approach. In this context, an experimental design
    :math:`\vect{\cX} =(x^{(1)},\cdots,x^{(N)})`, i.e. a set of realizations of
    input parameters is required, as well as the corresponding model evaluations
    :math:`\vect{\cY} =(y^{(1)},\cdots,y^{(N)})`.

    The following minimization problem has to be solved:

    .. math::

        \mbox{Find} \quad \widehat{\vect{a}} \quad \mbox{that minimizes}
          \quad \cJ(\vect{a}) \, = \, \sum_{i=1}^N \;
                                    \left(
                                    y^{(i)} \; - \;
                                    \Tr{\vect{a}} \vect{\psi}(\vect{x}^{(i)})
                                    \right)^2

    The solution is given by:

    .. math::

        \widehat{\vect{a}} \, = \, \left(
                                   \Tr{\mat{\Psi}} \mat{\Psi}
                                   \right)^{-1} \;
                                   \Tr{\mat{\Psi}}  \; \vect{\cY}

    where:

    .. math::

        \mat{\Psi} \, = \, (\psi_{j}(\vect{x}^{(i)}) \; , \; i=1,\cdots,N \; , \; j = 0,\cdots,n_X)

    See also
    --------
    LinearLeastSquares, LinearTaylor, QuadraticTaylor

    Examples
    --------
    >>> import openturns as ot
    >>> formulas = ['x1 * sin(x2)', 'cos(x1 + x2)', '(x2 + 1) * exp(x1 - 2 * x2)']
    >>> myFunc = ot.SymbolicFunction(['x1', 'x2'], formulas)
    >>> data  = [[0.5,0.5], [-0.5,-0.5], [-0.5,0.5], [0.5,-0.5]]
    >>> data += [[0.25,0.25], [-0.25,-0.25], [-0.25,0.25], [0.25,-0.25]]
    >>> myLeastSquares = ot.QuadraticLeastSquares(data, myFunc)
    >>> myLeastSquares.run()
    >>> responseSurface = myLeastSquares.getMetaModel()
    >>> print(responseSurface([0.1,0.1]))
    [0.00960661,0.976781,1.0138]
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
        return _metamodel.QuadraticLeastSquares_getClassName(self)

    def __repr__(self):
        return _metamodel.QuadraticLeastSquares___repr__(self)

    def run(self):
        """Perform the least squares approximation."""
        return _metamodel.QuadraticLeastSquares_run(self)

    def getConstant(self):
        """
        Get the constant vector of the approximation.

        Returns
        -------
        constantVector : :class:`~openturns.Point`
            Constant vector of the approximation, equal to :math:`a_0`.
        """
        return _metamodel.QuadraticLeastSquares_getConstant(self)

    def getLinear(self):
        """
        Get the linear matrix of the approximation.

        Returns
        -------
        linearMatrix : :class:`~openturns.Matrix`
            Linear matrix of the approximation of the function :math:`h`.
        """
        return _metamodel.QuadraticLeastSquares_getLinear(self)

    def getQuadratic(self):
        """
        Get the quadratic term of the approximation.

        Returns
        -------
        tensor : :class:`~openturns.SymmetricTensor`
            Quadratic term of the approximation of the function :math:`h`.
        """
        return _metamodel.QuadraticLeastSquares_getQuadratic(self)

    def getInputFunction(self):
        """
        Get the function.

        Returns
        -------
        function : :class:`~openturns.Function`
            Function :math:`h` to be approximated.
        """
        return _metamodel.QuadraticLeastSquares_getInputFunction(self)

    def getMetaModel(self):
        """
        Get an approximation of the function.

        Returns
        -------
        approximation : :class:`~openturns.Function`
            An approximation of the function :math:`h` by Quadratic Least Squares.
        """
        return _metamodel.QuadraticLeastSquares_getMetaModel(self)

    def getDataIn(self):
        """
        Get the input data.

        Returns
        -------
        dataIn : :class:`~openturns.Sample`
            Input data.
        """
        return _metamodel.QuadraticLeastSquares_getDataIn(self)

    def setDataOut(self, dataOut):
        """
        Set the output data.

        Parameters
        ----------
        dataOut : 2-d sequence of float
            Output data.
        """
        return _metamodel.QuadraticLeastSquares_setDataOut(self, dataOut)

    def getDataOut(self):
        """
        Get the output data.

        Returns
        -------
        dataOut : :class:`~openturns.Sample`
            Output data. If not specified in the constructor, the sample is computed
            such as: :math:`dataOut = h(dataIn)`.
        """
        return _metamodel.QuadraticLeastSquares_getDataOut(self)

    def __init__(self, *args):
        _metamodel.QuadraticLeastSquares_swiginit(self, _metamodel.new_QuadraticLeastSquares(*args))

    __swig_destroy__ = _metamodel.delete_QuadraticLeastSquares


_metamodel.QuadraticLeastSquares_swigregister(QuadraticLeastSquares)

class AdaptiveStrategyImplementation(openturns.common.PersistentObject):
    r"""
    Base class for the construction of the truncated multivariate orthogonal basis.

    Available constructors:
        AdaptiveStrategy(*orthogonalBasis, dimension*)

        AdaptiveStrategy(*adaptiveStrategyImplementation*)

    Parameters
    ----------
    orthogonalBasis : :class:`~openturns.OrthogonalBasis`
        An OrthogonalBasis.
    dimension : positive int
        Number of terms of the basis. This first usage has the same implementation
        as the second with a :class:`~openturns.FixedStrategy`. 
    adaptiveStrategyImplementation : AdaptiveStrategyImplementation
        Adaptive strategy implementation which is a :class:`~openturns.FixedStrategy`, 
        :class:`~openturns.SequentialStrategy` or a :class:`~openturns.CleaningStrategy`.

    See also
    --------
    FunctionalChaosAlgorithm, FixedStrategy, SequentialStrategy, CleaningStrategy

    Notes
    -----
    A strategy must be chosen for the selection of the different terms of the
    multivariate basis in which the response surface by functional chaos is expressed.
    The selected terms are regrouped in the finite subset :math:`K` of :math:`\Nset`.

    There are three different strategies available:

    - :class:`~openturns.FixedStrategy`,
    - :class:`~openturns.SequentialStrategy`,
    - :class:`~openturns.CleaningStrategy`.

    These strategies are conceived in such a way to be adapted for other orthogonal
    expansions (other than polynomial). For the moment, their implementation are
    only useful for the polynomial chaos expansion.
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
        return _metamodel.AdaptiveStrategyImplementation_getClassName(self)

    def setMaximumDimension(self, maximumDimension):
        """
        Accessor to the maximum dimension of the orthogonal basis.

        Parameters
        ----------
        P : integer
            Maximum dimension of the truncated basis.
        """
        return _metamodel.AdaptiveStrategyImplementation_setMaximumDimension(self, maximumDimension)

    def getMaximumDimension(self):
        """
        Accessor to the maximum dimension of the orthogonal basis.

        Returns
        -------
        P : integer
            Maximum dimension of the truncated basis.
        """
        return _metamodel.AdaptiveStrategyImplementation_getMaximumDimension(self)

    def computeInitialBasis(self):
        """
        Compute initial basis for the approximation.

        See also
        --------
        getPsi
        """
        return _metamodel.AdaptiveStrategyImplementation_computeInitialBasis(self)

    def updateBasis(self, alpha_k, residual, relativeError):
        """
        Update the basis for the next iteration of approximation.

        Notes
        -----
        No changes are made to the basis in the fixed strategy.
        """
        return _metamodel.AdaptiveStrategyImplementation_updateBasis(self, alpha_k, residual, relativeError)

    def __repr__(self):
        return _metamodel.AdaptiveStrategyImplementation___repr__(self)

    def getBasis(self):
        """
        Accessor to the underlying orthogonal basis.

        Returns
        -------
        basis : :class:`~openturns.OrthogonalBasis`
            Orthogonal basis of which the adaptive strategy is based.
        """
        return _metamodel.AdaptiveStrategyImplementation_getBasis(self)

    def getPsi(self):
        """
        Accessor to the orthogonal polynomials of the basis.

        Returns
        -------
        polynomials : list of polynomials
            Sequence of :math:`P` analytical polynomials.

        Notes
        -----
        The method :meth:`computeInitialBasis` must be applied first.

        Examples
        --------
        >>> import openturns as ot
        >>> productBasis = ot.OrthogonalProductPolynomialFactory([ot.HermiteFactory()])
        >>> adaptiveStrategy = ot.FixedStrategy(productBasis, 3)
        >>> adaptiveStrategy.computeInitialBasis()
        >>> print(adaptiveStrategy.getPsi())
        [1,x0,-0.707107 + 0.707107 * x0^2]
        """
        return _metamodel.AdaptiveStrategyImplementation_getPsi(self)

    def __init__(self, *args):
        _metamodel.AdaptiveStrategyImplementation_swiginit(self, _metamodel.new_AdaptiveStrategyImplementation(*args))

    __swig_destroy__ = _metamodel.delete_AdaptiveStrategyImplementation


_metamodel.AdaptiveStrategyImplementation_swigregister(AdaptiveStrategyImplementation)

class FixedStrategy(AdaptiveStrategyImplementation):
    r"""
    Fixed truncation strategy.

    Available constructors:
        FixedStrategy(*orthogonalBasis, dimension*)

    Parameters
    ----------
    orthogonalBasis : :class:`~openturns.OrthogonalBasis`
        An OrthogonalBasis.
    dimension : positive int
        Number of terms of the basis.

    See also
    --------
    AdaptiveStrategy, SequentialStrategy, CleaningStrategy

    Notes
    -----
    The so-called fixed strategy simply consists in retaining the first :math:`P`
    elements of the PC basis, the latter being ordered according to a given
    :class:`~openturns.EnumerateFunction` (hyperbolic or not). The retained set is
    built in a single pass. The truncated PC expansion is given by:

    .. math::

        \hat{h} (\uX) = \sum_{j=0}^{P-1} \vect{a}_j \Psi_j (\uX)

    In case of a :class:`~openturns.LinearEnumerateFunction`, for a given natural
    integer :math:`p`, a usual choice is to set :math:`P` equals to:

    .. math::

        P = \binom{n_X + p}{p} = \frac{(n_X + p)!}{n_X!\,p!}

    This way the set of retained basis functions :math:`\{\Psi_j, j = 0, \ldots, P-1\}`
    gathers all the polynomials with total degree not greater than :math:`p`.
    The number of terms :math:`P` grows polynomially both in :math:`n_X` and :math:`p`
    though, which may lead to difficulties in terms of computational efficiency and
    memory requirements when dealing with high-dimensional problems.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> # Define the model
    >>> inputDim = 1
    >>> model = ot.SymbolicFunction(['x'], ['x*sin(x)'])
    >>> # Create the input distribution
    >>> distribution = ot.ComposedDistribution([ot.Uniform()]*inputDim)
    >>> # Construction of the multivariate orthonormal basis
    >>> polyColl = [0.0]*inputDim
    >>> for i in range(distribution.getDimension()):
    ...     polyColl[i] = ot.StandardDistributionPolynomialFactory(distribution.getMarginal(i))
    >>> enumerateFunction = ot.LinearEnumerateFunction(inputDim)
    >>> productBasis = ot.OrthogonalProductPolynomialFactory(polyColl, enumerateFunction)
    >>> # Truncature strategy of the multivariate orthonormal basis
    >>> # We choose all the polynomials of degree <= 4
    >>> degree = 4
    >>> indexMax = enumerateFunction.getStrataCumulatedCardinal(degree)
    >>> print(indexMax)
    5
    >>> # We keep all the polynomials of degree <= 4
    >>> # which corresponds to the 5 first ones
    >>> adaptiveStrategy = ot.FixedStrategy(productBasis, indexMax)
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
        return _metamodel.FixedStrategy_getClassName(self)

    def computeInitialBasis(self):
        """
        Compute initial basis for the approximation.

        See also
        --------
        getPsi
        """
        return _metamodel.FixedStrategy_computeInitialBasis(self)

    def updateBasis(self, alpha_k, residual, relativeError):
        """
        Update the basis for the next iteration of approximation.

        Notes
        -----
        No changes are made to the basis in the fixed strategy.
        """
        return _metamodel.FixedStrategy_updateBasis(self, alpha_k, residual, relativeError)

    def __repr__(self):
        return _metamodel.FixedStrategy___repr__(self)

    def __init__(self, *args):
        _metamodel.FixedStrategy_swiginit(self, _metamodel.new_FixedStrategy(*args))

    __swig_destroy__ = _metamodel.delete_FixedStrategy


_metamodel.FixedStrategy_swigregister(FixedStrategy)

class SequentialStrategy(AdaptiveStrategyImplementation):
    r"""
    Sequential truncation strategy.

    Available constructors:
        SequentialStrategy(*orthogonalBasis, maximumDimension*)

    Parameters
    ----------
    orthogonalBasis : :class:`~openturns.OrthogonalBasis`
        An OrthogonalBasis.
    maximumDimension : positive int
        Maximum number of terms of the basis.

    See also
    --------
    AdaptiveStrategy, SequentialStrategy, CleaningStrategy

    Notes
    -----
    The sequential strategy consists in constructing the basis of the truncated PC
    iteratively. Precisely, one begins with the first term :math:`\Psi_0`, that is
    :math:`K_0 = \{0\}`, and one complements the current basis as follows:
    :math:`K_{k+1} = K_k \cup \{\Psi_{k+1}\}`. The construction process is
    stopped when a given accuracy criterion, defined in the
    :class:`~openturns.ProjectionStrategy`, is reached, or when :math:`k` is equal to
    a prescribed maximum basis size :math:`P`.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> # Define the model
    >>> inputDim = 1
    >>> model = ot.SymbolicFunction(['x'], ['x*sin(x)'])
    >>> # Create the input distribution
    >>> distribution = ot.ComposedDistribution([ot.Uniform()]*inputDim)
    >>> # Construction of the multivariate orthonormal basis
    >>> polyColl = [0.0]*inputDim
    >>> for i in range(distribution.getDimension()):
    ...     polyColl[i] = ot.StandardDistributionPolynomialFactory(distribution.getMarginal(i))
    >>> enumerateFunction = ot.LinearEnumerateFunction(inputDim)
    >>> productBasis = ot.OrthogonalProductPolynomialFactory(polyColl, enumerateFunction)
    >>> # Truncature strategy of the multivariate orthonormal basis
    >>> # We want to select among the maximumDimension = 20 first polynomials of the
    >>> # multivariate basis those verifying the convergence criterion.
    >>> maximumDimension = 20
    >>> adaptiveStrategy = ot.SequentialStrategy(productBasis, maximumDimension)
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
        return _metamodel.SequentialStrategy_getClassName(self)

    def computeInitialBasis(self):
        """
        Compute initial basis for the approximation.

        See also
        --------
        getPsi
        """
        return _metamodel.SequentialStrategy_computeInitialBasis(self)

    def updateBasis(self, alpha_k, residual, relativeError):
        """
        Update the basis for the next iteration of approximation.

        Notes
        -----
        No changes are made to the basis in the fixed strategy.
        """
        return _metamodel.SequentialStrategy_updateBasis(self, alpha_k, residual, relativeError)

    def __repr__(self):
        return _metamodel.SequentialStrategy___repr__(self)

    def __init__(self, *args):
        _metamodel.SequentialStrategy_swiginit(self, _metamodel.new_SequentialStrategy(*args))

    __swig_destroy__ = _metamodel.delete_SequentialStrategy


_metamodel.SequentialStrategy_swigregister(SequentialStrategy)

class CleaningStrategy(AdaptiveStrategyImplementation):
    r"""
    Cleaning truncation strategy.

    Available constructors:
        CleaningStrategy(*orthogonalBasis, maximumDimension*)

        CleaningStrategy(*orthogonalBasis, maximumDimension, verbose*)

        CleaningStrategy(*orthogonalBasis, maximumDimension, maximumSize, 
        significanceFactor*)

        CleaningStrategy(*orthogonalBasis, maximumDimension, maximumSize, 
        significanceFactor, verbose*)

    Parameters
    ----------
    orthogonalBasis : :class:`~openturns.OrthogonalBasis`
        An OrthogonalBasis.
    maximumDimension : positive int
        Maximum index that can be used by the :class:`~openturns.EnumerateFunction`
        to determine the last term of the basis.
    maximumSize : positve int
        Parameter that characterizes the cleaning strategy. It represents the 
        number of efficient coefficients of the basis. Its default value is set to 
        20.
    significanceFactor : float 
        Parameter used as a threshold for selecting the efficient coefficients of
        the basis. The real threshold represents the multiplication of the
        significanceFactor with the maximum magnitude of the current determined 
        coefficients. Its default value is equal to :math:`1e^{-4}`.
    verbose : bool
        Used for the online monitoring of the current basis updates (removed or
        added coefficients).

    See also
    --------
    AdaptiveStrategy, FixedStrategy, SequentialStrategy

    Notes
    -----
    The cleaning strategy aims at building a PC expansion containing at most
    :math:`P` significant coefficients, i.e. at most :math:`P` significant basis
    functions. It proceeds as follows:

    - Generate an initial PC basis made of the :math:`P` first polynomials
      (according to the adopted :class:`~openturns.EnumerateFunction`), or
      equivalently an initial set of indices :math:`K = \{0, \ldots, P-1\}`.

    - Discard from the basis all those polynomials :math:`\Psi_j` associated with 
      insignificance coefficients, i.e. the coefficients that satisfy:

    .. math::

        |a_j| \leq \epsilon \times \max_{ k \in K } |a_k|

    where :math:`\epsilon` is the significance factor, default is
    :math:`\epsilon = 10^{-4}`.

    - Add the next basis term :math:`\Psi_{k+1}` to the current basis :math:`K`.
    - Reiterate the procedure until either :math:`P` terms have been retained or if
      the given maximum index :math:`P_{max}` has been reached.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> # Define the model
    >>> inputDim = 1
    >>> model = ot.SymbolicFunction(['x'], ['x*sin(x)'])
    >>> # Create the input distribution
    >>> distribution = ot.ComposedDistribution([ot.Uniform()]*inputDim)
    >>> # Construction of the multivariate orthonormal basis
    >>> polyColl = [0.0]*inputDim
    >>> for i in range(distribution.getDimension()):
    ...     polyColl[i] = ot.StandardDistributionPolynomialFactory(distribution.getMarginal(i))
    >>> enumerateFunction = ot.LinearEnumerateFunction(inputDim)
    >>> productBasis = ot.OrthogonalProductPolynomialFactory(polyColl, enumerateFunction)
    >>> # Truncature strategy of the multivariate orthonormal basis
    >>> # We want to select, among the maximumDimension = 100 first polynomials of
    >>> # the multivariate basis, those which have the maximumSize = 20 most 
    >>> # significant contribution (greatest coefficients), with respect to the 
    >>> # significance factor = 10^-4.
    >>> maximumDimension = 100
    >>> maximumSize = 20
    >>> significanceFactor = 1e-4
    >>> adaptiveStrategy = ot.CleaningStrategy(productBasis, maximumDimension,
    ...                                          maximumSize, significanceFactor)
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
        return _metamodel.CleaningStrategy_getClassName(self)

    def computeInitialBasis(self):
        """
        Compute initial basis for the approximation.

        See also
        --------
        getPsi
        """
        return _metamodel.CleaningStrategy_computeInitialBasis(self)

    def updateBasis(self, alpha_k, residual, relativeError):
        """
        Update the basis for the next iteration of approximation.

        Notes
        -----
        No changes are made to the basis in the fixed strategy.
        """
        return _metamodel.CleaningStrategy_updateBasis(self, alpha_k, residual, relativeError)

    def __repr__(self):
        return _metamodel.CleaningStrategy___repr__(self)

    def getCurrentVectorIndex(self):
        """
        Accessor to the current vector index.

        Returns
        -------
        index : integer
            Current index of the basis term.
        """
        return _metamodel.CleaningStrategy_getCurrentVectorIndex(self)

    def getMaximumSize(self):
        """
        Accessor to the maximum size of the orthogonal basis.

        Returns
        -------
        size : integer
            Maximum number of significant terms of the basis.

        See also
        --------
        setMaximumSize
        """
        return _metamodel.CleaningStrategy_getMaximumSize(self)

    def setMaximumSize(self, maximumSize):
        """
        Accessor to the maximum size of the orthogonal basis.

        Parameters
        ----------
        size : integer
            Maximum number of significant terms of the basis.

        See also
        --------
        getMaximumSize
        """
        return _metamodel.CleaningStrategy_setMaximumSize(self, maximumSize)

    def getSignificanceFactor(self):
        """
        Accessor to the significance factor.

        Returns
        -------
        factor : float
            Value of the significance factor.

        See also
        --------
        setSignificanceFactor
        """
        return _metamodel.CleaningStrategy_getSignificanceFactor(self)

    def setSignificanceFactor(self, significanceFactor):
        """
        Accessor to the significance factor.

        Parameters
        ----------
        factor : float
            Value of the significance factor.

        See also
        --------
        getSignificanceFactor
        """
        return _metamodel.CleaningStrategy_setSignificanceFactor(self, significanceFactor)

    def getVerbose(self):
        """
        Accessor to the verbose.

        Returns
        -------
        verbose : bool
            Return if the online monitoring of the current basis updates is enabled or not.

        See also
        --------
        setVerbose
        """
        return _metamodel.CleaningStrategy_getVerbose(self)

    def setVerbose(self, verbose):
        """
        Accessor to the verbose.

        Parameters
        ----------
        verbose : bool
            Enable the online monitoring of the current basis updates or not.

        See also
        --------
        getVerbose
        """
        return _metamodel.CleaningStrategy_setVerbose(self, verbose)

    def __init__(self, *args):
        _metamodel.CleaningStrategy_swiginit(self, _metamodel.new_CleaningStrategy(*args))

    __swig_destroy__ = _metamodel.delete_CleaningStrategy


_metamodel.CleaningStrategy_swigregister(CleaningStrategy)

class AdaptiveStrategyImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _metamodel.AdaptiveStrategyImplementationTypedInterfaceObject_swiginit(self, _metamodel.new_AdaptiveStrategyImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _metamodel.AdaptiveStrategyImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _metamodel.AdaptiveStrategyImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _metamodel.AdaptiveStrategyImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _metamodel.AdaptiveStrategyImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _metamodel.AdaptiveStrategyImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _metamodel.delete_AdaptiveStrategyImplementationTypedInterfaceObject


_metamodel.AdaptiveStrategyImplementationTypedInterfaceObject_swigregister(AdaptiveStrategyImplementationTypedInterfaceObject)

class AdaptiveStrategy(AdaptiveStrategyImplementationTypedInterfaceObject):
    r"""
    Base class for the construction of the truncated multivariate orthogonal basis.

    Available constructors:
        AdaptiveStrategy(*orthogonalBasis, dimension*)

        AdaptiveStrategy(*adaptiveStrategyImplementation*)

    Parameters
    ----------
    orthogonalBasis : :class:`~openturns.OrthogonalBasis`
        An OrthogonalBasis.
    dimension : positive int
        Number of terms of the basis. This first usage has the same implementation
        as the second with a :class:`~openturns.FixedStrategy`. 
    adaptiveStrategyImplementation : AdaptiveStrategyImplementation
        Adaptive strategy implementation which is a :class:`~openturns.FixedStrategy`, 
        :class:`~openturns.SequentialStrategy` or a :class:`~openturns.CleaningStrategy`.

    See also
    --------
    FunctionalChaosAlgorithm, FixedStrategy, SequentialStrategy, CleaningStrategy

    Notes
    -----
    A strategy must be chosen for the selection of the different terms of the
    multivariate basis in which the response surface by functional chaos is expressed.
    The selected terms are regrouped in the finite subset :math:`K` of :math:`\Nset`.

    There are three different strategies available:

    - :class:`~openturns.FixedStrategy`,
    - :class:`~openturns.SequentialStrategy`,
    - :class:`~openturns.CleaningStrategy`.

    These strategies are conceived in such a way to be adapted for other orthogonal
    expansions (other than polynomial). For the moment, their implementation are
    only useful for the polynomial chaos expansion.
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
        return _metamodel.AdaptiveStrategy_getClassName(self)

    def setMaximumDimension(self, maximumDimension):
        """
        Accessor to the maximum dimension of the orthogonal basis.

        Parameters
        ----------
        P : integer
            Maximum dimension of the truncated basis.
        """
        return _metamodel.AdaptiveStrategy_setMaximumDimension(self, maximumDimension)

    def getMaximumDimension(self):
        """
        Accessor to the maximum dimension of the orthogonal basis.

        Returns
        -------
        P : integer
            Maximum dimension of the truncated basis.
        """
        return _metamodel.AdaptiveStrategy_getMaximumDimension(self)

    def computeInitialBasis(self):
        """
        Compute initial basis for the approximation.

        See also
        --------
        getPsi
        """
        return _metamodel.AdaptiveStrategy_computeInitialBasis(self)

    def updateBasis(self, alpha_k, residual, relativeError):
        """
        Update the basis for the next iteration of approximation.

        Notes
        -----
        No changes are made to the basis in the fixed strategy.
        """
        return _metamodel.AdaptiveStrategy_updateBasis(self, alpha_k, residual, relativeError)

    def getBasis(self):
        """
        Accessor to the underlying orthogonal basis.

        Returns
        -------
        basis : :class:`~openturns.OrthogonalBasis`
            Orthogonal basis of which the adaptive strategy is based.
        """
        return _metamodel.AdaptiveStrategy_getBasis(self)

    def getPsi(self):
        """
        Accessor to the orthogonal polynomials of the basis.

        Returns
        -------
        polynomials : list of polynomials
            Sequence of :math:`P` analytical polynomials.

        Notes
        -----
        The method :meth:`computeInitialBasis` must be applied first.

        Examples
        --------
        >>> import openturns as ot
        >>> productBasis = ot.OrthogonalProductPolynomialFactory([ot.HermiteFactory()])
        >>> adaptiveStrategy = ot.FixedStrategy(productBasis, 3)
        >>> adaptiveStrategy.computeInitialBasis()
        >>> print(adaptiveStrategy.getPsi())
        [1,x0,-0.707107 + 0.707107 * x0^2]
        """
        return _metamodel.AdaptiveStrategy_getPsi(self)

    def __repr__(self):
        return _metamodel.AdaptiveStrategy___repr__(self)

    def __str__(self, *args):
        return _metamodel.AdaptiveStrategy___str__(self, *args)

    def __init__(self, *args):
        _metamodel.AdaptiveStrategy_swiginit(self, _metamodel.new_AdaptiveStrategy(*args))

    __swig_destroy__ = _metamodel.delete_AdaptiveStrategy


_metamodel.AdaptiveStrategy_swigregister(AdaptiveStrategy)

class ProjectionStrategyImplementation(openturns.common.PersistentObject):
    r"""
    Base class for the evaluation strategies of the approximation coefficients.

    Available constructors:
        ProjectionStrategy(*projectionStrategy*)

    Parameters
    ----------
    projectionStrategy : :class:`~openturns.ProjectionStrategy`
        A projection strategy which is a :class:`~openturns.LeastSquaresStrategy` or
        an :class:`~openturns.IntegrationStrategy`.

    See also
    --------
    FunctionalChaosAlgorithm, LeastSquaresStrategy, IntegrationStrategy

    Notes
    -----
    Consider :math:`\vect{Y} = g(\vect{X})` with :math:`g: \Rset^d \rightarrow \Rset^p`,
    :math:`\vect{X} \sim \cL_{\vect{X}}` and :math:`\vect{Y}` with finite variance:
    :math:`g\in L_{\cL_{\vect{X}}}^2(\Rset^d, \Rset^p)`.

    The functional chaos  expansion approximates :math:`\vect{Y}` using an isoprobabilistic 
    transformation *T* and an orthonormal multivariate basis :math:`(\Psi_k)_{k \in \Nset}` 
    of :math:`L^2_{\mu}(\Rset^d,\Rset)`. See :class:`~openturns.FunctionalChaosAlgorithm` 
    to get more details. 

    The meta model of :math:`g`, based on the functional chaos decomposition of 
    :math:`f = g \circ T^{-1}` writes:

    .. math::

        \tilde{g} = \sum_{k \in K} \vect{\alpha}_k \Psi_k  \circ T

    where *K* is a non empty finite set of indices, whose cardinality is denoted by *P*.

    We detail the case where :math:`p=1`.

    The vector  :math:`\vect{\alpha} = (\alpha_k)_{k \in K}`  is  equivalently defined by:

    .. math::
        :label: defArgMin

        \vect{\alpha} = \argmin_{\vect{\alpha} \in \Rset^K} \Expect{ \left( g \circ T^{-1}(\vect{Z}) -  \sum_{k \in K} \alpha_k \Psi_k (\vect{Z})\right)^2 }

    and:

    .. math::
        :label: defEsp

        \alpha_k =  <g \circ T^{-1}(\vect{Z}), \Psi_k (\vect{Z})>_{\mu} = \Expect{  g \circ T^{-1}(\vect{Z}) \Psi_k (\vect{Z}) }

    where :math:`\vect{Z} = T(\vect{X})` and the mean :math:`\Expect{.}` is evaluated with respect to the measure :math:`\mu`.

    It corresponds to two points of view: 

        - relation :eq:`defArgMin`  means that the coefficients 
          :math:`(\alpha_k)_{k \in K}` minimize the quadratic error between  the model and 
          the polynomial approximation. Use :class:`~openturns.LeastSquaresStrategy`.

        - relation :eq:`defEsp` means that :math:`\alpha_k` is the scalar product of the 
          model with the *k-th* element of the orthonormal basis :math:`(\Psi_k)_{k \in \Nset}`.
          Use :class:`~openturns.IntegrationStrategy`.

    In both cases, the mean :math:`\Expect{.}` is approximated by a linear quadrature formula:

    .. math::
        :label: approxEsp

        \Expect{ f(\vect{Z})} \simeq \sum_{i \in I} \omega_i f(\Xi_i)

    where *f* is a function in :math:`L^1(\mu)`. 

    In the approximation :eq:`approxEsp`, the set *I*, the points :math:`(\Xi_i)_{i \in I}` 
    and the weights :math:`(\omega_i)_{i \in I}` are evaluated from different methods 
    implemented in the :class:`~openturns.WeightedExperiment`.

    The convergence criterion used to evaluate the coefficients is based on the residual value 
    defined in the :class:`~openturns.FunctionalChaosAlgorithm`.
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
        return _metamodel.ProjectionStrategyImplementation_getClassName(self)

    def __repr__(self):
        return _metamodel.ProjectionStrategyImplementation___repr__(self)

    def setMeasure(self, measure):
        r"""
        Accessor to the measure.

        Parameters
        ----------
        m : Distribution
            Measure :math:`\mu` defining the scalar product.
        """
        return _metamodel.ProjectionStrategyImplementation_setMeasure(self, measure)

    def getMeasure(self):
        r"""
        Accessor to the measure.

        Returns
        -------
        mu : Distribution
            Measure :math:`\mu` defining the scalar product.
        """
        return _metamodel.ProjectionStrategyImplementation_getMeasure(self)

    def setInputSample(self, inputSample):
        """
        Accessor to the input sample.

        Parameters
        ----------
        X : :class:`~openturns.Sample`
            Input Sample.
        """
        return _metamodel.ProjectionStrategyImplementation_setInputSample(self, inputSample)

    def getInputSample(self):
        """
        Accessor to the input sample.

        Returns
        -------
        X : :class:`~openturns.Sample`
            Input Sample.
        """
        return _metamodel.ProjectionStrategyImplementation_getInputSample(self)

    def setOutputSample(self, outputSample):
        """
        Accessor to the output sample.

        Parameters
        ----------
        Y : :class:`~openturns.Sample`
            Output Sample.
        """
        return _metamodel.ProjectionStrategyImplementation_setOutputSample(self, outputSample)

    def getOutputSample(self):
        """
        Accessor to the output sample.

        Returns
        -------
        Y : :class:`~openturns.Sample`
            Output Sample.
        """
        return _metamodel.ProjectionStrategyImplementation_getOutputSample(self)

    def setWeights(self, weights):
        """
        Accessor to the weights.

        Parameters
        ----------
        w : :class:`~openturns.Point`
            Weights of the design of experiments.
        """
        return _metamodel.ProjectionStrategyImplementation_setWeights(self, weights)

    def getWeights(self):
        """
        Accessor to the weights.

        Returns
        -------
        w : :class:`~openturns.Point`
            Weights of the design of experiments.
        """
        return _metamodel.ProjectionStrategyImplementation_getWeights(self)

    def getResidual(self):
        """
        Accessor to the residual.

        Returns
        -------
        er : float
            Residual error.
        """
        return _metamodel.ProjectionStrategyImplementation_getResidual(self)

    def getRelativeError(self):
        """
        Accessor to the relative error.

        Returns
        -------
        e : float
            Relative error.
        """
        return _metamodel.ProjectionStrategyImplementation_getRelativeError(self)

    def getCoefficients(self):
        r"""
        Accessor to the coefficients.

        Returns
        -------
        coef : :class:`~openturns.Point`
            Coefficients :math:`(\alpha_k)_{k \in K}`.
        """
        return _metamodel.ProjectionStrategyImplementation_getCoefficients(self)

    def setExperiment(self, weightedExperiment):
        """
        Accessor to the design of experiment.

        Parameters
        ----------
        exp : :class:`~openturns.WeightedExperiment`
            Weighted design of experiment.
        """
        return _metamodel.ProjectionStrategyImplementation_setExperiment(self, weightedExperiment)

    def getExperiment(self):
        """
        Accessor to the experiments.

        Returns
        -------
        exp : :class:`~openturns.WeightedExperiment`
            Weighted experiment used to evaluate the coefficients.
        """
        return _metamodel.ProjectionStrategyImplementation_getExperiment(self)

    def computeCoefficients(self, function, basis, indices, addedRanks, conservedRanks, removedRanks, marginalIndex=0):
        return _metamodel.ProjectionStrategyImplementation_computeCoefficients(self, function, basis, indices, addedRanks, conservedRanks, removedRanks, marginalIndex)

    def __init__(self, *args):
        _metamodel.ProjectionStrategyImplementation_swiginit(self, _metamodel.new_ProjectionStrategyImplementation(*args))

    __swig_destroy__ = _metamodel.delete_ProjectionStrategyImplementation


_metamodel.ProjectionStrategyImplementation_swigregister(ProjectionStrategyImplementation)

class LeastSquaresStrategy(ProjectionStrategyImplementation):
    r"""
    Least squares strategy for the approximation coefficients.

    Available constructors:
        LeastSquaresStrategy(*weightedExp*)

        LeastSquaresStrategy(*weightedExp, approxAlgoImpFact*)

        LeastSquaresStrategy(*measure, approxAlgoImpFact*)

        LeastSquaresStrategy(*measure, weightedExp, approxAlgoImpFact*)

        LeastSquaresStrategy(*inputSample, outputSample, approxAlgoImpFact*)

        LeastSquaresStrategy(*inputSample, weights, outputSample, approxAlgoImpFact*)

    Parameters
    ----------
    weightedExp : :class:`~openturns.WeightedExperiment`
        Experimental design used for the transformed input data.
        By default the class :class:`~openturns.MonteCarloExperiment` is used.
    approxAlgoImpFact : ApproximationAlgorithmImplementationFactory
        The factory that builds the desired :class:`~openturns.ApproximationAlgorithm`.
        By default the class :class:`~openturns.PenalizedLeastSquaresAlgorithmFactory` is used.
    measure : :class:`~openturns.Distribution`
        Distribution :math:`\mu` with respect to which the basis is orthonormal.
        By default, the limit measure defined within the class
        :class:`~openturns.WeightedExperiment` is used.
    inputSample, outputSample : 2-d sequence of float
        The input random variables :math:`\vect{X}=(X_1, \dots, X_{n_X})^T`
        and the output samples :math:`\vect{Y}` that describe the model.
    weights : sequence of float
        Numerical point that are the weights associated to the input sample points
        such that the corresponding weighted experiment is a good approximation of
        :math:`\mu`. If not precised, all weights are equals to 
        :math:`\omega_i = \frac{1}{size}`, where :math:`size` is the size of the
        sample.

    See also
    --------
    FunctionalChaosAlgorithm, ProjectionStrategy, IntegrationStrategy

    Notes
    -----
    This class is not usable because it has sense only within the
    :class:`~openturns.FunctionalChaosAlgorithm` : the least squares strategy
    evaluates the coefficients :math:`(a_k)_{k \in K}` of the polynomials
    decomposition as follows:

    .. math::

        \vect{a} = \argmin_{\vect{b} \in \Rset^P} E_{\mu} \left[ \left( g \circ T^{-1}
                (\vect{U}) - \vect{b}^{\intercal} \vect{\Psi}(\vect{U}) \right)^2 \right]

    where :math:`\vect{U} = T(\vect{X})`.

    The mean expectation :math:`E_{\mu}` is approximated by a relation of type:

    .. math::

        E_{\mu} \left[ f(\vect{U}) \right] \approx \sum_{i \in I} \omega_i f(\Xi_i)

    where is a function :math:`L_1(\mu)` defined as:

    .. math::

        f(\vect{U} = \left( g \circ T^{-1} (\vect{U}) - \vect{b}^{\intercal}
                                     \vect{\Psi}(\vect{U}) \right)^2 

    In the approximation of the mean expectation, the set *I*, the points 
    :math:`(\Xi_i)_{i \in I}` and the weights :math:`(\omega_i)_{i \in I}` are
    evaluated from methods implemented in the :class:`~openturns.WeightedExperiment`.
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
        return _metamodel.LeastSquaresStrategy_getClassName(self)

    def __repr__(self):
        return _metamodel.LeastSquaresStrategy___repr__(self)

    def computeCoefficients(self, function, basis, indices, addedRanks, conservedRanks, removedRanks, marginalIndex=0):
        return _metamodel.LeastSquaresStrategy_computeCoefficients(self, function, basis, indices, addedRanks, conservedRanks, removedRanks, marginalIndex)

    def __init__(self, *args):
        _metamodel.LeastSquaresStrategy_swiginit(self, _metamodel.new_LeastSquaresStrategy(*args))

    __swig_destroy__ = _metamodel.delete_LeastSquaresStrategy


_metamodel.LeastSquaresStrategy_swigregister(LeastSquaresStrategy)

class IntegrationStrategy(ProjectionStrategyImplementation):
    r"""
    Integration strategy for the approximation coefficients.

    Available constructors:
        LeastSquaresStrategy(*measure*)

        LeastSquaresStrategy(*weightedExp*)

        LeastSquaresStrategy(*measure, weightedExp*)

        LeastSquaresStrategy(*inputSample, outputSample*)

        LeastSquaresStrategy(*inputSample, weights, outputSample*)

    Parameters
    ----------
    weightedExp : :class:`~openturns.WeightedExperiment`
        Experimental design used for the transformed input data. When not precised,
        OpenTURNS uses a :class:`~openturns.MonteCarloExperiment`.
    measure : :class:`~openturns.Distribution`
        Distribution :math:`\mu` with respect to which the basis is orthonormal.
        When not precised, OpenTURNS uses the limit measure defined within the
        :class:`~openturns.WeightedExperiment`.
    inputSample, outputSample : 2-d sequence of float
        The input random variables :math:`\vect{X}=(X_1, \dots, X_{n_X})^T`
        and the output samples :math:`\vect{Y}` that describe the model.
    weights : sequence of float
        Numerical point that are the weights associated to the input sample points
        such that the corresponding weighted experiment is a good approximation of
        :math:`\mu`. If not precised, all weights are equals to 
        :math:`\omega_i = \frac{1}{size}`, where :math:`size` is the size of the
        sample.

    See also
    --------
    FunctionalChaosAlgorithm, ProjectionStrategy, LeastSquaresStrategy

    Notes
    -----
    This class is not usable because it has sense only within the
    :class:`~openturns.FunctionalChaosAlgorithm` : the integration strategy
    evaluates the coefficients :math:`(a_k)_{k \in K}` of the polynomials
    decomposition as follows:

    .. math::

        \vect{a} = E_{\mu} \left[ g \circ T^{-1} (\vect{U}) \vect{\Psi}(\vect{U}) \right]

    where :math:`\vect{U} = T(\vect{X})`.

    The mean expectation :math:`E_{\mu}` is approximated by a relation of type:

    .. math::

        E_{\mu} \left[ f(\vect{U}) \right] \approx \sum_{i \in I} \omega_i f(\Xi_i)

    where is a function :math:`L_1(\mu)` defined as:

    .. math::

        f(\vect{U} = g \circ T^{-1} (\vect{U}) \vect{\Psi}(\vect{U})

    In the approximation of the mean expectation, the set *I*, the points 
    :math:`(\Xi_i)_{i \in I}` and the weights :math:`(\omega_i)_{i \in I}` are
    evaluated from methods implemented in the :class:`~openturns.WeightedExperiment`.
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
        return _metamodel.IntegrationStrategy_getClassName(self)

    def __repr__(self):
        return _metamodel.IntegrationStrategy___repr__(self)

    def computeCoefficients(self, function, basis, indices, addedRanks, conservedRanks, removedRanks, marginalIndex=0):
        return _metamodel.IntegrationStrategy_computeCoefficients(self, function, basis, indices, addedRanks, conservedRanks, removedRanks, marginalIndex)

    def __init__(self, *args):
        _metamodel.IntegrationStrategy_swiginit(self, _metamodel.new_IntegrationStrategy(*args))

    __swig_destroy__ = _metamodel.delete_IntegrationStrategy


_metamodel.IntegrationStrategy_swigregister(IntegrationStrategy)

class ProjectionStrategyImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _metamodel.ProjectionStrategyImplementationTypedInterfaceObject_swiginit(self, _metamodel.new_ProjectionStrategyImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _metamodel.ProjectionStrategyImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _metamodel.ProjectionStrategyImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _metamodel.ProjectionStrategyImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _metamodel.ProjectionStrategyImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _metamodel.ProjectionStrategyImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _metamodel.delete_ProjectionStrategyImplementationTypedInterfaceObject


_metamodel.ProjectionStrategyImplementationTypedInterfaceObject_swigregister(ProjectionStrategyImplementationTypedInterfaceObject)

class ProjectionStrategy(ProjectionStrategyImplementationTypedInterfaceObject):
    r"""
    Base class for the evaluation strategies of the approximation coefficients.

    Available constructors:
        ProjectionStrategy(*projectionStrategy*)

    Parameters
    ----------
    projectionStrategy : :class:`~openturns.ProjectionStrategy`
        A projection strategy which is a :class:`~openturns.LeastSquaresStrategy` or
        an :class:`~openturns.IntegrationStrategy`.

    See also
    --------
    FunctionalChaosAlgorithm, LeastSquaresStrategy, IntegrationStrategy

    Notes
    -----
    Consider :math:`\vect{Y} = g(\vect{X})` with :math:`g: \Rset^d \rightarrow \Rset^p`,
    :math:`\vect{X} \sim \cL_{\vect{X}}` and :math:`\vect{Y}` with finite variance:
    :math:`g\in L_{\cL_{\vect{X}}}^2(\Rset^d, \Rset^p)`.

    The functional chaos  expansion approximates :math:`\vect{Y}` using an isoprobabilistic 
    transformation *T* and an orthonormal multivariate basis :math:`(\Psi_k)_{k \in \Nset}` 
    of :math:`L^2_{\mu}(\Rset^d,\Rset)`. See :class:`~openturns.FunctionalChaosAlgorithm` 
    to get more details. 

    The meta model of :math:`g`, based on the functional chaos decomposition of 
    :math:`f = g \circ T^{-1}` writes:

    .. math::

        \tilde{g} = \sum_{k \in K} \vect{\alpha}_k \Psi_k  \circ T

    where *K* is a non empty finite set of indices, whose cardinality is denoted by *P*.

    We detail the case where :math:`p=1`.

    The vector  :math:`\vect{\alpha} = (\alpha_k)_{k \in K}`  is  equivalently defined by:

    .. math::
        :label: defArgMin

        \vect{\alpha} = \argmin_{\vect{\alpha} \in \Rset^K} \Expect{ \left( g \circ T^{-1}(\vect{Z}) -  \sum_{k \in K} \alpha_k \Psi_k (\vect{Z})\right)^2 }

    and:

    .. math::
        :label: defEsp

        \alpha_k =  <g \circ T^{-1}(\vect{Z}), \Psi_k (\vect{Z})>_{\mu} = \Expect{  g \circ T^{-1}(\vect{Z}) \Psi_k (\vect{Z}) }

    where :math:`\vect{Z} = T(\vect{X})` and the mean :math:`\Expect{.}` is evaluated with respect to the measure :math:`\mu`.

    It corresponds to two points of view: 

        - relation :eq:`defArgMin`  means that the coefficients 
          :math:`(\alpha_k)_{k \in K}` minimize the quadratic error between  the model and 
          the polynomial approximation. Use :class:`~openturns.LeastSquaresStrategy`.

        - relation :eq:`defEsp` means that :math:`\alpha_k` is the scalar product of the 
          model with the *k-th* element of the orthonormal basis :math:`(\Psi_k)_{k \in \Nset}`.
          Use :class:`~openturns.IntegrationStrategy`.

    In both cases, the mean :math:`\Expect{.}` is approximated by a linear quadrature formula:

    .. math::
        :label: approxEsp

        \Expect{ f(\vect{Z})} \simeq \sum_{i \in I} \omega_i f(\Xi_i)

    where *f* is a function in :math:`L^1(\mu)`. 

    In the approximation :eq:`approxEsp`, the set *I*, the points :math:`(\Xi_i)_{i \in I}` 
    and the weights :math:`(\omega_i)_{i \in I}` are evaluated from different methods 
    implemented in the :class:`~openturns.WeightedExperiment`.

    The convergence criterion used to evaluate the coefficients is based on the residual value 
    defined in the :class:`~openturns.FunctionalChaosAlgorithm`.
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
        return _metamodel.ProjectionStrategy_getClassName(self)

    def setMeasure(self, measure):
        r"""
        Accessor to the measure.

        Parameters
        ----------
        m : Distribution
            Measure :math:`\mu` defining the scalar product.
        """
        return _metamodel.ProjectionStrategy_setMeasure(self, measure)

    def getMeasure(self):
        r"""
        Accessor to the measure.

        Returns
        -------
        mu : Distribution
            Measure :math:`\mu` defining the scalar product.
        """
        return _metamodel.ProjectionStrategy_getMeasure(self)

    def setInputSample(self, inputSample):
        """
        Accessor to the input sample.

        Parameters
        ----------
        X : :class:`~openturns.Sample`
            Input Sample.
        """
        return _metamodel.ProjectionStrategy_setInputSample(self, inputSample)

    def getInputSample(self):
        """
        Accessor to the input sample.

        Returns
        -------
        X : :class:`~openturns.Sample`
            Input Sample.
        """
        return _metamodel.ProjectionStrategy_getInputSample(self)

    def setOutputSample(self, outputSample):
        """
        Accessor to the output sample.

        Parameters
        ----------
        Y : :class:`~openturns.Sample`
            Output Sample.
        """
        return _metamodel.ProjectionStrategy_setOutputSample(self, outputSample)

    def getOutputSample(self):
        """
        Accessor to the output sample.

        Returns
        -------
        Y : :class:`~openturns.Sample`
            Output Sample.
        """
        return _metamodel.ProjectionStrategy_getOutputSample(self)

    def setWeights(self, weights):
        """
        Accessor to the weights.

        Parameters
        ----------
        w : :class:`~openturns.Point`
            Weights of the design of experiments.
        """
        return _metamodel.ProjectionStrategy_setWeights(self, weights)

    def getWeights(self):
        """
        Accessor to the weights.

        Returns
        -------
        w : :class:`~openturns.Point`
            Weights of the design of experiments.
        """
        return _metamodel.ProjectionStrategy_getWeights(self)

    def getResidual(self):
        """
        Accessor to the residual.

        Returns
        -------
        er : float
            Residual error.
        """
        return _metamodel.ProjectionStrategy_getResidual(self)

    def getRelativeError(self):
        """
        Accessor to the relative error.

        Returns
        -------
        e : float
            Relative error.
        """
        return _metamodel.ProjectionStrategy_getRelativeError(self)

    def getCoefficients(self):
        r"""
        Accessor to the coefficients.

        Returns
        -------
        coef : :class:`~openturns.Point`
            Coefficients :math:`(\alpha_k)_{k \in K}`.
        """
        return _metamodel.ProjectionStrategy_getCoefficients(self)

    def setExperiment(self, weightedExperiment):
        """
        Accessor to the design of experiment.

        Parameters
        ----------
        exp : :class:`~openturns.WeightedExperiment`
            Weighted design of experiment.
        """
        return _metamodel.ProjectionStrategy_setExperiment(self, weightedExperiment)

    def getExperiment(self):
        """
        Accessor to the experiments.

        Returns
        -------
        exp : :class:`~openturns.WeightedExperiment`
            Weighted experiment used to evaluate the coefficients.
        """
        return _metamodel.ProjectionStrategy_getExperiment(self)

    def computeCoefficients(self, function, basis, indices, addedRanks, conservedRanks, removedRanks, marginalIndex=0):
        return _metamodel.ProjectionStrategy_computeCoefficients(self, function, basis, indices, addedRanks, conservedRanks, removedRanks, marginalIndex)

    def __repr__(self):
        return _metamodel.ProjectionStrategy___repr__(self)

    def __str__(self, *args):
        return _metamodel.ProjectionStrategy___str__(self, *args)

    def __init__(self, *args):
        _metamodel.ProjectionStrategy_swiginit(self, _metamodel.new_ProjectionStrategy(*args))

    __swig_destroy__ = _metamodel.delete_ProjectionStrategy


_metamodel.ProjectionStrategy_swigregister(ProjectionStrategy)

class FunctionalChaosResult(MetaModelResult):
    """
    Functional chaos result.

    Notes
    -----
    Structure created by the method run() of
    :class:`~openturns.FunctionalChaosAlgorithm`, and obtained thanks to the method
    getResult().
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
        return _metamodel.FunctionalChaosResult_getClassName(self)

    def __repr__(self):
        return _metamodel.FunctionalChaosResult___repr__(self)

    def __str__(self, *args):
        return _metamodel.FunctionalChaosResult___str__(self, *args)

    def getDistribution(self):
        r"""
        Get the input distribution.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Distribution of the  input random vector :math:`\vect{X}`.
        """
        return _metamodel.FunctionalChaosResult_getDistribution(self)

    def getTransformation(self):
        r"""
        Get the isoprobabilistic transformation.

        Returns
        -------
        transformation : :class:`~openturns.Function`
            Transformation :math:`T` such that :math:`T(\vect{X}) = \vect{Z}`.
        """
        return _metamodel.FunctionalChaosResult_getTransformation(self)

    def getInverseTransformation(self):
        r"""
        Get the inverse isoprobabilistic transformation.

        Returns
        -------
        invTransf : :class:`~openturns.Function`
             :math:`T^{-1}` such that :math:`T(\vect{X}) = \vect{Z}`.
        """
        return _metamodel.FunctionalChaosResult_getInverseTransformation(self)

    def getComposedModel(self):
        r"""
        Get the composed model.

        Returns
        -------
        composedModel : :class:`~openturns.Function`
            :math:`f = g\circ T^{-1}`.
        """
        return _metamodel.FunctionalChaosResult_getComposedModel(self)

    def getOrthogonalBasis(self):
        """
        Get the orthogonal basis.

        Returns
        -------
        basis : :class:`~openturns.OrthogonalBasis`
            Factory of the orthogonal basis.
        """
        return _metamodel.FunctionalChaosResult_getOrthogonalBasis(self)

    def getIndices(self):
        """
        Get the indices of the final basis.

        Returns
        -------
        indices : :class:`~openturns.Indices`
            Indices of the elements of the multivariate basis used in the decomposition.
        """
        return _metamodel.FunctionalChaosResult_getIndices(self)

    def getCoefficients(self):
        r"""
        Get the coefficients.

        Returns
        -------
        coefficients : 2-d sequence of float
            Coefficients :math:`(\vect{\alpha_k})_{k \in K}`.
        """
        return _metamodel.FunctionalChaosResult_getCoefficients(self)

    def getReducedBasis(self):
        r"""
        Get the reduced basis.

        Returns
        -------
        basis : list of :class:`~openturns.Function`
            Collection of the *K* functions  :math:`(\Psi_k)_{k\in K}`  used in the 
            decomposition.
        """
        return _metamodel.FunctionalChaosResult_getReducedBasis(self)

    def getComposedMetaModel(self):
        r"""
        Get the composed metamodel.

        Returns
        -------
        composedMetamodel : :class:`~openturns.Function`
            :math:`\tilde{f} =  \sum_{k \in K} \vect{\alpha}_k \Psi_k`
        """
        return _metamodel.FunctionalChaosResult_getComposedMetaModel(self)

    def __init__(self, *args):
        _metamodel.FunctionalChaosResult_swiginit(self, _metamodel.new_FunctionalChaosResult(*args))

    __swig_destroy__ = _metamodel.delete_FunctionalChaosResult


_metamodel.FunctionalChaosResult_swigregister(FunctionalChaosResult)

class FunctionalChaosAlgorithm(MetaModelAlgorithm):
    r"""
    Functional chaos algorithm.

    Refer to :ref:`functional_chaos`, :ref:`polynomial_least_squares`.

    Available constructors:
        FunctionalChaosAlgorithm(*inputSample, outputSample*)

        FunctionalChaosAlgorithm(*inputSample, outputSample, distribution, adaptiveStrategy*)

        FunctionalChaosAlgorithm(*inputSample, outputSample, distribution, adaptiveStrategy, projectionStrategy*)

        FunctionalChaosAlgorithm(*model, distribution, adaptiveStrategy*)

        FunctionalChaosAlgorithm(*model, distribution, adaptiveStrategy, projectionStrategy*)

        FunctionalChaosAlgorithm(*inputSample, weights, outputSample, distribution, adaptiveStrategy*)

        FunctionalChaosAlgorithm(*inputSample, weights, outputSample, distribution, adaptiveStrategy, projectionStrategy*)

    Parameters
    ----------
    inputSample, outputSample : 2-d sequence of float
        Sample of the input - output random vectors
    model : :class:`~openturns.Function`
        Model :math:`g` such as :math:`\vect{Y} = g(\vect{X})`.
    distribution : :class:`~openturns.Distribution`
        Distribution of the random vector :math:`\vect{X}`
    adaptiveStrategy : :class:`~openturns.AdaptiveStrategy`
        Strategy of selection of the different terms of the multivariate basis.
    projectionStrategy : :class:`~openturns.ProjectionStrategy`
        Strategy of evaluation of the coefficients :math:`\alpha_k`
    weights : sequence of float
        Weights :math:`\omega_i` associated to the data base

        Default values are :math:`\omega_i = \frac{1}{N}` where 
        *N=inputSample.getSize()*

    See also
    --------
    FunctionalChaosResult

    Notes
    -----
    Consider :math:`\vect{Y} = g(\vect{X})` with :math:`g: \Rset^d \rightarrow \Rset^p`, 
    :math:`\vect{X} \sim \cL_{\vect{X}}` and :math:`\vect{Y}` with finite variance: 
    :math:`g\in L_{\cL_{\vect{X}}}^2(\Rset^d, \Rset^p)`.

    When  :math:`p>1`, the functional chaos algorithm is used on each marginal 
    of :math:`\vect{Y}`, using the same multivariate orthonormal basis for all the marginals. 
    Thus, the algorithm is detailed here for a scalar output :math:`Y` and 
    :math:`g: \Rset^d \rightarrow \Rset`.

    Let :math:`T: \Rset^d \rightarrow \Rset^d` be an isoprobabilistic transformation
    such that :math:`\vect{Z} = T(\vect{X}) \sim \mu`. We note :math:`f = g \circ T^{-1}`, then :math:`f \in L_{\mu}^2(\Rset^d, \Rset)`.

    Let :math:`(\Psi_k)_{k \in \Nset}` be an orthonormal multivariate basis of 
    :math:`L^2_{\mu}(\Rset^d,\Rset)`.

    Then the functional chaos decomposition of *f* writes:

    .. math::

        f = g\circ T^{-1} = \sum_{k=0}^{\infty} \vect{\alpha}_k \Psi_k 

    which can be truncated to the finite set :math:`K \in \Nset`:

    .. math::

        \tilde{f} =  \sum_{k \in K} \vect{\alpha}_k \Psi_k 

    The approximation :math:`\tilde{f}` can be used to build an efficient random 
    generator of :math:`Y` based on the random vector :math:`\vect{Z}`. 
    It writes:

    .. math::

        \tilde{Y} = \tilde{f}(\vect{Z})

    For more details, see :class:`~openturns.FunctionalChaosRandomVector`.

    The functional chaos decomposition can be used to build a meta model of *g*, 
    which writes:

    .. math::

        \tilde{g} = \tilde{f} \circ T

    If the basis :math:`(\Psi_k)_{k \in \Nset}` has been obtained by tensorisation of
    univariate orthonormal basis, then the distribution :math:`\mu` writes  
    :math:`\mu = \prod_{i=1}^d \mu_i`. In that case only, the Sobol indices can
    easily be deduced from the coefficients :math:`\alpha_k`.

    We detail here all the steps required in order to create a functional chaos 
    algorithm.

    **Step 1 - Construction of the multivariate orthonormal basis**: the
    multivariate orthonornal basis :math:`(\Psi_k(\vect{x}))_{k \in \Nset}` is built
    as the tensor product of orthonormal univariate families.

    The univariate bases may be:

        - *polynomials*: the associated distribution :math:`\mu_i` is continuous or discrete. 
          Note that it is possible to build the polynomial family orthonormal to any univariate 
          distribution :math:`\mu_i` under some conditions. 
          For more details, see :class:`~openturns.StandardDistributionPolynomialFactory`;

        - Haar wavelets: they enable to approximate functions with discontinuities.
          For more details, see :class:`~openturns.HaarWaveletFactory`,;

        - Fourier series: for more details, see :class:`~openturns.FourierSeriesFactory`.

    Furthermore, the numerotation of the multivariate orthonormal basis :math:`(\Psi_k(\vect{z}))_k` 
    is given by an enumerate function which defines a regular way to generate the collection of degres 
    used for the univariate polynomials : an enumerate function represents a bijection 
    :math:`\Nset \rightarrow \Nset^d`. See :class:`~openturns.LinearEnumerateFunction` or :class:`~openturns.HyperbolicAnisotropicEnumerateFunction` 
    for more details.

    **Step 2 - Truncation strategy of the multivariate orthonormal basis**: a
    strategy must be chosen for the selection of the different terms of the
    multivariate basis. The selected terms are gathered in the subset *K*.

    For more details on the possible strategies, see :class:`~openturns.FixedStrategy`,
    :class:`~openturns.SequentialStrategy` and :class:`~openturns.CleaningStrategy`.

    **Step 3 -  Evaluation strategy of the coefficients**: a
    strategy must be chosen for the estimation of te coefficients :math:`\alpha_k`. 
    The vector :math:`\vect{\alpha} = (\alpha_k)_{k \in K}` is equivalently defined by:

    .. math::
        :label: quadEr

        \vect{\alpha} = \argmin_{\vect{\alpha} \in \Rset^K}\Expect{\left( g \circ T^{-1}(\vect{Z}) - \sum_{k \in K} \alpha_k \Psi_k (\vect{Z})\right)^2}

    or

    .. math::
        :label: scalProd

        \alpha_k =  <g \circ T^{-1}(\vect{Z}), \Psi_k (\vect{Z})>_{\mu} = \Expect{  g \circ T^{-1}(\vect{Z}) \Psi_k (\vect{Z}) }

    where the mean :math:`\Expect{.}` is evaluated with respect to the measure :math:`\mu`.

    Relation :eq:`quadEr` means that the coefficients :math:`(\alpha_k)_{k \in K}`
    minimize the quadratic error between the model and the polynomial approximation.
    For more details, see :class:`~openturns.LeastSquaresStrategy`.

    Relation  :eq:`scalProd` means that :math:`\alpha_k` is the scalar product of the
    model with the *k-th* element of the orthonormal basis :math:`(\Psi_k)_{k \in \Nset}`.
    For more details, see :class:`~openturns.IntegrationStrategy`.

    Examples
    --------
    Create the model:

    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> inputDim = 1
    >>> model = ot.SymbolicFunction(['x'], ['x*sin(x)'])
    >>> distribution = ot.ComposedDistribution([ot.Uniform()]*inputDim)

    Build the multivariate orthonormal basis:

    >>> polyColl = [0.0]*inputDim
    >>> for i in range(distribution.getDimension()):
    ...     polyColl[i] = ot.StandardDistributionPolynomialFactory(distribution.getMarginal(i))
    >>> enumerateFunction = ot.LinearEnumerateFunction(inputDim)
    >>> productBasis = ot.OrthogonalProductPolynomialFactory(polyColl, enumerateFunction)

    Define the  strategy to truncate the multivariate orthonormal basis:
    We choose all the polynomials of degree <= 4

    >>> degree = 4
    >>> indexMax = enumerateFunction.getStrataCumulatedCardinal(degree)
    >>> print(indexMax)
    5

    We keep all the polynomials of degree <= 4 (which corresponds to the 5 first ones):

    >>> adaptiveStrategy = ot.FixedStrategy(productBasis, indexMax)

    Define the evaluation strategy of the  coefficients:

    >>> samplingSize = 50
    >>> experiment = ot.MonteCarloExperiment(samplingSize)
    >>> projectionStrategy = ot.LeastSquaresStrategy(experiment)

    Create the Functional Chaos Algorithm:

    >>> algo = ot.FunctionalChaosAlgorithm(model, distribution, adaptiveStrategy,
    ...                                    projectionStrategy)
    >>> algo.run()

    Get the result:

    >>> functionalChaosResult = algo.getResult()
    >>> metamodel = functionalChaosResult.getMetaModel()

    Test it:

    >>> X = [0.5]
    >>> print(model(X))
    [0.239713]
    >>> print(metamodel(X))
    [0.239514]
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
        return _metamodel.FunctionalChaosAlgorithm_getClassName(self)

    def __repr__(self):
        return _metamodel.FunctionalChaosAlgorithm___repr__(self)

    def setMaximumResidual(self, residual):
        """
        Set the maximum residual.

        Parameters
        ----------
        residual : float
            Residual value needed in the projection strategy. 

            Default value is :math:`0`.
        """
        return _metamodel.FunctionalChaosAlgorithm_setMaximumResidual(self, residual)

    def getMaximumResidual(self):
        """
        Get the maximum residual.

        Returns
        -------
        residual : float
            Residual value needed in the projection strategy. 

            Default value is :math:`0`.
        """
        return _metamodel.FunctionalChaosAlgorithm_getMaximumResidual(self)

    def setProjectionStrategy(self, projectionStrategy):
        r"""
        Set the projection strategy.

        Parameters
        ----------
        strategy : :class:`~openturns.ProjectionStrategy`
            Strategy to estimate the coefficients :math:`\alpha_k`.
        """
        return _metamodel.FunctionalChaosAlgorithm_setProjectionStrategy(self, projectionStrategy)

    def getProjectionStrategy(self):
        """
        Get the projection strategy.

        Returns
        -------
        strategy : :class:`~openturns.ProjectionStrategy`
            Projection strategy.

        Notes
        -----
        The projection strategy selects the different terms of the
        multivariate basis to define the subset *K*.
        """
        return _metamodel.FunctionalChaosAlgorithm_getProjectionStrategy(self)

    def getAdaptiveStrategy(self):
        """
        Get the adaptive strategy.

        Returns
        -------
        adaptiveStrategy : :class:`~openturns.AdaptiveStrategy`
            Strategy of selection of the different terms of the multivariate basis.
        """
        return _metamodel.FunctionalChaosAlgorithm_getAdaptiveStrategy(self)

    def run(self):
        """
        Compute the metamodel.

        Notes
        -----
        Evaluates the metamodel and stores all the results in a result structure.
        """
        return _metamodel.FunctionalChaosAlgorithm_run(self)

    def getResult(self):
        """
        Get the results of the metamodel computation.

        Returns
        -------
        result : :class:`~openturns.FunctionalChaosResult`
            Result structure, created by the method :py:meth:`run`.
        """
        return _metamodel.FunctionalChaosAlgorithm_getResult(self)

    def getInputSample(self):
        """
        Accessor to the input sample.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            Input sample of a model evaluated apart.
        """
        return _metamodel.FunctionalChaosAlgorithm_getInputSample(self)

    def getOutputSample(self):
        """
        Accessor to the output sample.

        Returns
        -------
        outputSample : :class:`~openturns.Sample`
            Output sample of a model evaluated apart.
        """
        return _metamodel.FunctionalChaosAlgorithm_getOutputSample(self)

    @staticmethod
    def BuildDistribution(inputSample):
        """
        Recover the distribution, with metamodel performance in mind.

        For each marginal, find the best 1-d continuous parametric model,
        else fallback to the use of :class:`~openturns.KernelSmoothing`.
        For the copula, the Spearman independance test is used on each component pair
        to decide whether an independent copula can be used,
        else use a :class:`~openturns.NormalCopula`.

        Parameters
        ----------
        sample : :class:`~openturns.Sample`
            Input sample.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Input distribution.
        """
        return _metamodel.FunctionalChaosAlgorithm_BuildDistribution(inputSample)

    def __init__(self, *args):
        _metamodel.FunctionalChaosAlgorithm_swiginit(self, _metamodel.new_FunctionalChaosAlgorithm(*args))

    __swig_destroy__ = _metamodel.delete_FunctionalChaosAlgorithm


_metamodel.FunctionalChaosAlgorithm_swigregister(FunctionalChaosAlgorithm)

def FunctionalChaosAlgorithm_BuildDistribution(inputSample):
    """
    Recover the distribution, with metamodel performance in mind.

    For each marginal, find the best 1-d continuous parametric model,
    else fallback to the use of :class:`~openturns.KernelSmoothing`.
    For the copula, the Spearman independance test is used on each component pair
    to decide whether an independent copula can be used,
    else use a :class:`~openturns.NormalCopula`.

    Parameters
    ----------
    sample : :class:`~openturns.Sample`
        Input sample.

    Returns
    -------
    distribution : :class:`~openturns.Distribution`
        Input distribution.
    """
    return _metamodel.FunctionalChaosAlgorithm_BuildDistribution(inputSample)


class FunctionalChaosSobolIndices(openturns.common.PersistentObject):
    """
    Sensitivity analysis based on functional chaos expansion.

    Available constructors:
        FunctionalChaosSobolIndices(functionalChaosResult)

    Parameters
    ----------
    functionalChaosResult : :class:`~openturns.FunctionalChaosResult`
        A functional chaos result resulting from a polynomial chaos decomposition.

    See also
    --------
    FunctionalChaosAlgorithm, FunctionalChaosResult

    Notes
    -----
    This structure is created from a FunctionalChaosResult in order to evaluate the
    Sobol indices associated to the polynomial chaos decomposition of the model. 
    The SobolIndicesAlgorithm.DrawSobolIndices static method can be used to 
    draw the indices.

    Examples
    --------
    Create a polynomial chaos for the Ishigami function:

    >>> import openturns as ot
    >>> from math import pi
    >>> import openturns.viewer as otv

    Create the function:

    >>> ot.RandomGenerator.SetSeed(0)
    >>> formula = ['sin(X1) + 7. * sin(X2)^2 + 0.1 * X3^4 * sin(X1)']
    >>> input_names = ['X1', 'X2', 'X3']
    >>> g = ot.SymbolicFunction(input_names, formula)

    Create the probabilistic model:

    >>> distributionList = [ot.Uniform(-pi, pi)] * 3
    >>> distribution = ot.ComposedDistribution(distributionList)

    Create a training sample
    >>> N = 100 
    >>> inputTrain = distribution.getSample(N)
    >>> outputTrain = g(inputTrain)

    Create the chaos:

    >>> chaosalgo = ot.FunctionalChaosAlgorithm(inputTrain, outputTrain)
    >>> chaosalgo.run()
    >>> result = chaosalgo.getResult()

    Print Sobol' indices :

    >>> chaosSI = ot.FunctionalChaosSobolIndices(result) 
    >>> #print( chaosSI.summary() )

    Get first order Sobol' indices for X0:

    >>> chaosSI.getSobolIndex(0)
    0.3400236...

    Get total order Sobol' indices for X0:

    >>> chaosSI.getSobolTotalIndex(0)
    0.4940954...

    Get first order Sobol' indices for group [X0,X1]:

    >>> chaosSI.getSobolGroupedIndex([0,1])
    0.7882764...

    Get total order Sobol' indices for group [X1,X2]:

    >>> chaosSI.getSobolGroupedTotalIndex([1,2])
    0.6599763...
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
        return _metamodel.FunctionalChaosSobolIndices_getClassName(self)

    def __repr__(self):
        return _metamodel.FunctionalChaosSobolIndices___repr__(self)

    def summary(self):
        """
        Summary accessor.

        Returns
        -------
        summary : str
            A text summary of the sensitivity analysis to be shown in a console.
        """
        return _metamodel.FunctionalChaosSobolIndices_summary(self)

    def getSobolIndex(self, *args):
        r"""
        Get the Sobol indices.

        Parameters
        ----------
        i : int or sequence of int, :math:`0 \leq i < d - 1`
            Indice(s) of the variable(s) we want the associated Sobol indices. :math:`d`
            is the dimension of the input variables.
        out_marginal : int
            Output marginal
            Default value is 0

        Returns
        -------
        s : float
            The Sobol indice.
        """
        return _metamodel.FunctionalChaosSobolIndices_getSobolIndex(self, *args)

    def getSobolTotalIndex(self, *args):
        r"""
        Get the total Sobol indices.

        Parameters
        ----------
        i : int or sequence of int, :math:`0 \leq i < d - 1`
            Indice(s) of the variable(s) we want the associated total Sobol indices.
            :math:`d` is the dimension of the input variables.
        out_marginal : int
            Output marginal
            Default value is 0

        Returns
        -------
        s : float
            The total Sobol indice.
        """
        return _metamodel.FunctionalChaosSobolIndices_getSobolTotalIndex(self, *args)

    def getSobolGroupedIndex(self, *args):
        r"""
        Get the grouped Sobol first order indices.

        Parameters
        ----------
        i : int or sequence of int, :math:`0 \leq i < d - 1`
            Indice(s) of the variable(s) we want the associated grouped Sobol indices.
            :math:`d` is the dimension of the input variables.

        Returns
        -------
        s : float
            The grouped Sobol first order indice.
        """
        return _metamodel.FunctionalChaosSobolIndices_getSobolGroupedIndex(self, *args)

    def getSobolGroupedTotalIndex(self, *args):
        r"""
        Get the grouped Sobol total order indices.

        Parameters
        ----------
        i : int or sequence of int, :math:`0 \leq i < d - 1`
            Indice(s) of the variable(s) we want the associated grouped Sobol indices.
            :math:`d` is the dimension of the input variables.

        Returns
        -------
        s : float
            The grouped Sobol total order indice.
        """
        return _metamodel.FunctionalChaosSobolIndices_getSobolGroupedTotalIndex(self, *args)

    def getFunctionalChaosResult(self):
        """
        Accessor to the functional chaos result.

        Returns
        -------
        functionalChaosResult : :class:`~openturns.FunctionalChaosResult`
            The functional chaos result resulting from a polynomial chaos decomposition.
        """
        return _metamodel.FunctionalChaosSobolIndices_getFunctionalChaosResult(self)

    def __init__(self, *args):
        _metamodel.FunctionalChaosSobolIndices_swiginit(self, _metamodel.new_FunctionalChaosSobolIndices(*args))

    __swig_destroy__ = _metamodel.delete_FunctionalChaosSobolIndices


_metamodel.FunctionalChaosSobolIndices_swigregister(FunctionalChaosSobolIndices)

class MetaModelValidation(openturns.common.PersistentObject):
    """
    Base class to score a metamodel and perform validations.

    Refer to :ref:`cross_validation`.

    Available constructor:
        MetaModelValidation(*inputValidationSample, outputValidationSample, metaModel*)

    Parameters
    ----------
    inputValidationSample, outputValidationSample : 2-d sequence of float
        The input and output validation samples, not used during the learning step.

    metaModel : :class:`~openturns.Function`
        Metamodel to validate.

    Notes
    -----
    A MetaModelValidation object is used for the validation process of a metamodel.
    For that purpose, a dataset independent of the learning step, is used to score the surrogate model.
    Its main functionalities are :

    - To compute the predictivity factor :math:`Q_2`
    - To get the residual sample, its non parametric distribution
    - To draw a `model vs metamodel` validation graph.

    Currently only one dimensional output models are available.

    Examples
    --------
    >>> import openturns as ot
    >>> from math import pi
    >>> dist = ot.Uniform(-pi/2, pi/2)
    >>> # Model here is sin(x)
    >>> model = ot.SymbolicFunction(['x'], ['sin(x)'])
    >>> # We can build several types of models (kriging, pc, ...)
    >>> # We use a Taylor developement (order 5) and compare the metamodel with the model
    >>> metaModel = ot.SymbolicFunction(['x'], ['x - x^3/6.0 + x^5/120.0'])
    >>> x = dist.getSample(10)
    >>> y = model(x)
    >>> # Validation of the model
    >>> val = ot.MetaModelValidation(x, y, metaModel)
    >>> # Compute the first indicator : q2
    >>> q2 = val.computePredictivityFactor()
    >>> # Get the residual
    >>> residual = val.getResidualSample()
    >>> # Get the histogram of residual
    >>> histoResidual = val.getResidualDistribution(False)
    >>> # Draw the validation graph
    >>> graph = val.drawValidation()

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
        return _metamodel.MetaModelValidation_getClassName(self)

    def __repr__(self):
        return _metamodel.MetaModelValidation___repr__(self)

    def getInputSample(self):
        """
        Accessor to the input sample.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            Input sample of a model evaluated apart.
        """
        return _metamodel.MetaModelValidation_getInputSample(self)

    def getOutputSample(self):
        """
        Accessor to the output sample.

        Returns
        -------
        outputSample : :class:`~openturns.Sample`
            Output sample of a model evaluated apart.
        """
        return _metamodel.MetaModelValidation_getOutputSample(self)

    def computePredictivityFactor(self):
        r"""
        Compute the predictivity factor.

        Returns
        -------
        q2 : float
            The predictivity factor

        Notes
        -----
        The predictivity factor :math:`Q_2` is given by :

        .. math::
            Q_2 = 1 - \frac{\sum_{l=1}^{N} (Y_{l} -\hat{f}(X_l))^2}{Var(Y)}
        """
        return _metamodel.MetaModelValidation_computePredictivityFactor(self)

    def getResidualSample(self):
        r"""
        Compute the residual sample.

        Returns
        -------
        residual : :class:`~openturns.Sample`
            The residual sample.

        Notes
        -----
        The residual sample is given by :

        .. math::
            \epsilon_{l} = Y_{l} -\hat{f}(X_l)
        """
        return _metamodel.MetaModelValidation_getResidualSample(self)

    def getResidualDistribution(self, smooth=True):
        """
        Compute the non parametric distribution of the residual sample.

        Parameters
        ----------
        smooth : bool
            Tells if distribution is smooth (true) or not.
            Default argument is true.

        Returns
        -------
        residualDistribution : :class:`~openturns.Distribution`
            The residual distribution.

        Notes
        -----
        The residual distribution is built thanks to :class:`~openturns.KernelSmoothing` if `smooth` argument is true. Otherwise, an histogram distribution is returned, thanks to :class:`~openturns.HistogramFactory`.
        """
        return _metamodel.MetaModelValidation_getResidualDistribution(self, smooth)

    def drawValidation(self):
        """
        Plot a model vs metamodel graph for visual validation.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            The visual validation graph.
        """
        return _metamodel.MetaModelValidation_drawValidation(self)

    def __init__(self, *args):
        _metamodel.MetaModelValidation_swiginit(self, _metamodel.new_MetaModelValidation(*args))

    __swig_destroy__ = _metamodel.delete_MetaModelValidation


_metamodel.MetaModelValidation_swigregister(MetaModelValidation)

class GeneralLinearModelResult(MetaModelResult):
    r"""
    General linear model result.

    Available constructors:
        GeneralLinearModelResult(*inputSample, outputSample, metaModel, residuals, relativeErrors, basis, trendCoefficients, covarianceModel, optimalLogLikelihood*)

        GeneralLinearModelResult(*inputSample, outputSample, metaModel, residuals, relativeErrors, basis, trendCoefficients, covarianceModel, covarianceCholeskyFactor, covarianceHMatrix, optimalLogLikelihood*)

    Parameters
    ----------
    inputSample, outputSample : :class:`~openturns.Sample`
        The samples :math:`(\vect{x}_k)_{1 \leq k \leq N} \in \Rset^d` and :math:`(\vect{y}_k)_{1 \leq k \leq N}\in \Rset^p`.
    metaModel : :class:`~openturns.Function`
        The meta model: :math:`\tilde{\cM}: \Rset^d \rightarrow \Rset^p`, defined in :eq:metaModel.
    residuals : :class:`~openturns.Point`
        The residual errors.
    relativeErrors : :class:`~openturns.Point`
        The relative errors.
    basis : collection of :class:`~openturns.Basis`
        Collection of the  :math:`p` functional basis: :math:`(\varphi_j^l: \Rset^d \rightarrow \Rset)_{1 \leq j \leq n_l}` for each :math:`l \in [1, p]`.
        Its size should be equal to zero if the trend is not estimated.
    trendCoefficients : collection of :class:`~openturns.Point`
       The trend coefficients vectors :math:`(\vect{\alpha}^1, \dots, \vect{\alpha}^p)`.
    covarianceModel : :class:`~openturns.CovarianceModel`
        Covariance function of the Gaussian process with its optimized parameters.
    covarianceCholeskyFactor : :class:`~openturns.TriangularMatrix`
        The Cholesky factor :math:`\mat{L}` of :math:`\mat{C}`.
    covarianceHMatrix :  :class:`~openturns.HMatrix`
        The *hmat* implementation of :math:`\mat{L}`.
    optimalLogLikelihood : float
        The maximum log-likelihood corresponding to the model.

    Notes
    -----
    The structure is usually created by the method *run()* of a :class:`~openturns.GeneralLinearModelAlgorithm`, and obtained thanks to the *getResult()* method.

    The meta model :math:`\tilde{\cM}: \Rset^d \rightarrow \Rset^p` is defined by:

    .. math::
        :label: metaModel

        \tilde{\cM}(\vect{x}) = \left(
          \begin{array}{l}
            \mu_1(\vect{x}) \\
            \dots  \\
            \mu_p(\vect{x}) 
           \end{array}
         \right)

    where :math:`\mu_l(\vect{x}) = \sum_{j=1}^{n_l} \alpha_j^l \varphi_j^l(\vect{x})` and :math:`\varphi_j^l: \Rset^d \rightarrow \Rset` are the trend functions.

    If a normalizing transformation *T* has been used, the meta model is built on the inputs :math:`\vect{z}_k = T(\vect{x}_k)` and the meta model writes:

    .. math::
        :label: metaModelWithT

        \tilde{\cM}(\vect{x}) = \left(
          \begin{array}{l}
            \mu_1\circ T(\vect{x}) \\
            \dots  \\
            \mu_p\circ T(\vect{x}) 
           \end{array}
         \right)

    Examples
    --------
    Create the model :math:`\cM: \Rset \mapsto \Rset` and the samples:

    >>> import openturns as ot
    >>> f = ot.SymbolicFunction(['x'],  ['x * sin(x)'])
    >>> sampleX = [[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]]
    >>> sampleY = f(sampleX)

    Create the algorithm:

    >>> basis = ot.Basis([ot.SymbolicFunction(['x'], ['x']), ot.SymbolicFunction(['x'], ['x^2'])])
    >>> covarianceModel = ot.GeneralizedExponential([2.0], 2.0)
    >>> algo = ot.GeneralLinearModelAlgorithm(sampleX, sampleY, covarianceModel, basis)
    >>> algo.run()

    Get the result:

    >>> result = algo.getResult()

    Get the meta model:

    >>> metaModel = result.getMetaModel()
    >>> graph = metaModel.draw(0.0, 7.0)
    >>> cloud = ot.Cloud(sampleX, sampleY)
    >>> cloud.setPointStyle('fcircle')
    >>> graph = ot.Graph()
    >>> graph.add(cloud)
    >>> graph.add(f.draw(0.0, 7.0))
    >>> graph.setColors(['black', 'blue', 'red'])

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
        return _metamodel.GeneralLinearModelResult_getClassName(self)

    def __repr__(self):
        return _metamodel.GeneralLinearModelResult___repr__(self)

    def __str__(self, *args):
        return _metamodel.GeneralLinearModelResult___str__(self, *args)

    def getBasisCollection(self):
        r"""
        Accessor to the collection of basis.

        Returns
        -------
        basisCollection : collection of :class:`~openturns.Basis`
            Collection of the :math:`p` function basis: :math:`(\varphi_j^l: \Rset^d \rightarrow \Rset)_{1 \leq j \leq n_l}` for each :math:`l \in [1, p]`.

        Notes
        -----
        If the trend is not estimated, the collection is empty. 

        """
        return _metamodel.GeneralLinearModelResult_getBasisCollection(self)

    def getTrendCoefficients(self):
        r"""
        Accessor to the trend coefficients.

        Returns
        -------
        trendCoef : collection of :class:`~openturns.Point`
            The trend coefficients vectors :math:`(\vect{\alpha}^1, \dots, \vect{\alpha}^p)`

        """
        return _metamodel.GeneralLinearModelResult_getTrendCoefficients(self)

    def getCovarianceModel(self):
        """
        Accessor to the covariance model.

        Returns
        -------
        covModel : :class:`~openturns.CovarianceModel`
            The covariance model of the Gaussian process *W*.

        """
        return _metamodel.GeneralLinearModelResult_getCovarianceModel(self)

    def getTransformation(self):
        """
        Accessor to the normalizing transformation.

        Returns
        -------
        transformation : :class:`~openturns.Function`
            The transformation *T* that normalizes the input sample.

        """
        return _metamodel.GeneralLinearModelResult_getTransformation(self)

    def setTransformation(self, transformation):
        """
        Set accessor to the normalizing transformation.

        Parameters
        ----------
        transformation : :class:`~openturns.Function`
            The transformation *T* that normalizes the input sample.

        """
        return _metamodel.GeneralLinearModelResult_setTransformation(self, transformation)

    def getNoise(self):
        """
        Accessor to the Gaussian process.

        Returns
        -------
        process : :class:`~openturns.Process`
            Returns the Gaussian process :math:`W` with the optimized parameters.

        """
        return _metamodel.GeneralLinearModelResult_getNoise(self)

    def getOptimalLogLikelihood(self):
        """
        Accessor to the optimal log-likelihood of the model.

        Returns
        -------
        optimalLogLikelihood : float
            The value of the log-likelihood corresponding to the model.

        """
        return _metamodel.GeneralLinearModelResult_getOptimalLogLikelihood(self)

    def __init__(self, *args):
        _metamodel.GeneralLinearModelResult_swiginit(self, _metamodel.new_GeneralLinearModelResult(*args))

    __swig_destroy__ = _metamodel.delete_GeneralLinearModelResult


_metamodel.GeneralLinearModelResult_swigregister(GeneralLinearModelResult)

class GeneralLinearModelAlgorithm(MetaModelAlgorithm):
    r"""
    Algorithm for the evaluation of general linear models.

    Available constructors:
        GeneralLinearModelAlgorithm(*inputSample, outputSample, covarianceModel, basis, normalize=True, keepCovariance=True*)

        GeneralLinearModelAlgorithm(*inputSample, outputSample, covarianceModel, basisCollection, normalize=True, keepCovariance=True*)

    Parameters
    ----------
    inputSample, outputSample : :class:`~openturns.Sample` or 2d-array
        The samples :math:`(\vect{x}_k)_{1 \leq k \leq N} \in \Rset^n` and :math:`(\vect{y}_k)_{1 \leq k \leq N}\in \Rset^d`.

    basis : :class:`~openturns.Basis`
        Functional basis to estimate the trend: :math:`(\varphi_j)_{1 \leq j \leq n_1}: \Rset^n \rightarrow \Rset`. 

        If :math:`d>1`, the same basis is used for each marginal output.
    basisCollection : collection of :class:`~openturns.Basis`
        Collection of :math:`d` functional basis: one basis for each marginal output.

        An empty collection means that no trend is estimated.
    covarianceModel : :class:`~openturns.CovarianceModel`
        Covariance model of the Gaussian process. See notes for the details.

    normalize : bool, optional
        Indicates whether the input sample has to be normalized.
        If True, input sample is centered & reduced.
        Default is set in resource map key `GeneralLinearModelAlgorithm-NormalizeData`

    keepCovariance : bool, optional
        Indicates whether the covariance matrix has to be stored in the result structure *GeneralLinearModelResult*.
        Default value is set in resource map key `GeneralLinearModelAlgorithm-KeepCovariance`

    Notes
    -----
    We suppose we have a sample :math:`(\vect{x}_k, \vect{y}_k)_{1 \leq k \leq N}` where :math:`\vect{y}_k = \cM(\vect{x}_k)` for all :math:`k`, with :math:`\cM:\Rset^n \mapsto \Rset^d` a given function.

    The objective is to build a metamodel :math:`\tilde{\cM}`, using a **general linear model**: the sample :math:`(\vect{y}_k)_{1 \leq k \leq N}` is considered as the restriction of a Gaussian process :math:`\vect{Y}(\omega, \vect{x})` on :math:`(\vect{x}_k)_{1 \leq k \leq N}`. The Gaussian process :math:`\vect{Y}(\omega, \vect{x})` is defined by:

    .. math::

        \vect{Y}(\omega, \vect{x}) = \vect{\mu}(\vect{x}) + \vect{W}(\omega, \vect{x})

    where:

    .. math::

        \vect{\mu}(\vect{x}) = \left(
          \begin{array}{l}
            \mu_1(\vect{x}) \\
            \dots  \\
            \mu_d(\vect{x}) 
           \end{array}
         \right)

    with :math:`\mu_\ell(\vect{x}) = \sum_{j=1}^{n_\ell} \beta_j^\ell \varphi_j^\ell(\vect{x})` and :math:`\varphi_j^\ell: \Rset^n \rightarrow \Rset` the trend functions.

    :math:`\vect{W}` is a Gaussian process of dimension :math:`d` with zero mean and covariance function :math:`C = C(\vect{\theta}, \vect{\sigma}, \mat{R}, \vect{\lambda})` (see :class:`~openturns.CovarianceModel` for the notations).

    We note:

    .. math::

        \vect{\beta}^\ell = \left(
          \begin{array}{l}
            \beta_1^\ell \\
            \dots  \\
            \beta_{n_\ell}^\ell
           \end{array}
         \right) \in \Rset^{n_\ell}
         \quad \mbox{ and } \quad 
         \vect{\beta} = \left(
          \begin{array}{l}
             \vect{\beta}^1\\
            \dots  \\
             \vect{\beta}^d
           \end{array}
         \right)\in \Rset^{\sum_{\ell=1}^p n_\ell}

    The *GeneralLinearModelAlgorithm* class estimates the coefficients :math:`\beta_j^\ell` and :math:`\vect{p}` where :math:`\vect{p}` is the vector of parameters of the covariance model (a subset of :math:`\vect{\theta}, \vect{\sigma}, \mat{R}, \vect{\lambda}`) that has been declared as *active* (by default, the full vectors :math:`\vect{\theta}` and :math:`\vect{\sigma}`).

    The estimation is done by maximizing the *reduced* log-likelihood of the model, see its expression below.

    If a normalizing transformation :math:`T` has been used, the meta model is built on the inputs :math:`\vect{z}_k = T(\vect{x}_k)`.

    **Estimation of the parameters** :math:`\beta_j^\ell` and :math:`\vect{p}`

    We note:

    .. math::

        \vect{y} = \left(
          \begin{array}{l}
            \vect{y}_1 \\
            \dots  \\
            \vect{y}_N
           \end{array}
         \right) \in \Rset^{dN},
         \quad 
         \vect{m}_{\vect{\beta}} = \left(
          \begin{array}{l}
            \vect{\mu}(\vect{x}_1) \\
            \dots  \\
            \vect{\mu}(\vect{x}_N)
           \end{array}
         \right) \in \Rset^{dN}

     and 

    .. math::

        \mat{C}_{\vect{p}} = \left(
          \begin{array}{lcl}
            \mat{C}_{11} & \dots &  \mat{C}_{1N}\\
            \dots & \dots & \\
            \mat{C}_{N1} & \dots &  \mat{C}_{NN}
           \end{array}
         \right) \in \cS_{dN}^+(\Rset)

    where :math:`\mat{C}_{ij} = C_{\vect{p}}(\vect{x}_i, \vect{x}_j)`. 

    The model likelihood writes:

    .. math::

        \cL(\vect{\beta}, \vect{p};(\vect{x}_k, \vect{y}_k)_{1 \leq k \leq N}) = \dfrac{1}{(2\pi)^{dN/2} |\det \mat{C}_{\vect{p}}|^{1/2}} \exp\left[ -\dfrac{1}{2}\Tr{\left( \vect{y}-\vect{m} \right)} \mat{C}_{\vect{p}}^{-1}  \left( \vect{y}-\vect{m} \right)  \right]

    If :math:`\mat{L}` is the Cholesky factor of :math:`\mat{C}`, ie the lower triangular matrix with positive diagonal such that :math:`\mat{L}\,\Tr{\mat{L}} = \mat{C}`, then:

    .. math::
        :label: logLikelihood

        \log \cL(\vect{\beta}, \vect{p};(\vect{x}_k, \vect{y}_k)_{1 \leq k \leq N}) = cste - \log \det \mat{L}_{\vect{p}} -\dfrac{1}{2}  \| \mat{L}_{\vect{p}}^{-1}(\vect{y}-\vect{m}_{\vect{\beta}}) \|^2

    The maximization of :eq:`logLikelihood` leads to the following optimality condition for :math:`\vect{\beta}`:

    .. math::

        \vect{\beta}^*(\vect{p}^*)=\argmin_{\vect{\beta}} \| \mat{L}_{\vect{p}^*}^{-1}(\vect{y}-\vect{m}_{\vect{\beta}}) \|^2

    This expression of :math:`\vect{\beta}^*` as a function of :math:`\vect{p}^*` is taken as a general relation between :math:`\vect{\beta}` and :math:`\vect{p}` and is substituted into :eq:`logLikelihood`, leading to a *reduced log-likelihood* function depending solely on :math:`\vect{p}`.

    In the particular case where :math:`d=\dim(\vect{\sigma})=1` and :math:`\sigma` is a part of :math:`\vect{p}`, then a further reduction is possible. In this case, if :math:`\vect{q}` is the vector :math:`\vect{p}` in which :math:`\sigma` has been substituted by 1, then:

    .. math::

        \| \mat{L}_{\vect{p}}^{-1}(\vect{y}-\vect{m}_{\vect{\beta}}) \|^2=\| \mat{L}_{\vect{q}}^{-1}(\vect{y}-\vect{m}_{\vect{\beta}}) \|^2/\sigma^2

    showing that :math:`\vect{\beta}^*` is a function of :math:`\vect{q}^*` only, and the optimality condition for :math:`\sigma` reads:

    .. math::

        \vect{\sigma}^*(\vect{q}^*)=\dfrac{1}{N}\| \mat{L}_{\vect{q}^*}^{-1}(\vect{y}-\vect{m}_{\vect{\beta}^*(\vect{q}^*)}) \|^2

    which leads to a further reduction of the log-likelihood function where both :math:`\vect{\beta}` and :math:`\sigma` are replaced by their expression in terms of :math:`\vect{q}`.

    The default optimizer is :class:`~openturns.TNC` and can be changed thanks to the *setOptimizationAlgorithm* method.
    User could also change the default optimization solver by setting the `GeneralLinearModelAlgorithm-DefaultOptimizationAlgorithm` resource map key to one of the :class:`~openturns.NLopt` solver names.

    It is also possible to proceed as follows:

        - ask for the reduced log-likelihood function of the *GeneralLinearModelAlgorithm* thanks to the *getObjectiveFunction()* method
        - optimize it with respect to the parameters :math:`\vect{\theta}` and  :math:`\vect{\sigma}` using any optimization algorithms (that can take into account some additional constraints if needed)
        - set the optimal parameter value into the covariance model used in the *GeneralLinearModelAlgorithm*
        - tell the algorithm not to optimize the parameter using *setOptimizeParameters*

    The behaviour of the reduction is controlled by the following keys in :class:`~openturns.ResourceMap`:
        - *ResourceMap.SetAsBool('GeneralLinearModelAlgorithm-UseAnalyticalAmplitudeEstimate', true)* to use the reduction associated to :math:`\sigma`. It has no effect if :math:`d>1` or if :math:`d=1` and :math:`\sigma` is not part of :math:`\vect{p}`
        - *ResourceMap.SetAsBool('GeneralLinearModelAlgorithm-UnbiasedVariance', true)* allows to use the *unbiased* estimate of :math:`\sigma` where :math:`\dfrac{1}{N}` is replaced by :math:`\dfrac{1}{N-p}` in the optimality condition for :math:`\sigma`.

    With huge samples, the `hierarchical matrix <http://en.wikipedia.org/wiki/Hierarchical_matrix>`_  implementation could be used if OpenTURNS had been compiled with `hmat-oss` support.

    This implementation, which is based on a compressed representation of an approximated covariance matrix (and its Cholesky factor), has a better complexity both in terms of memory requirements and floating point operations. To use it, the `GeneralLinearModelAlgorithm-LinearAlgebra` resource map key should be instancied to `HMAT`. Default value of the key is `LAPACK`.

    A known centered gaussian observation noise :math:`\epsilon_k` can be taken into account
    with :func:`setNoise()`:

    .. math:: \hat{\vect{y}}_k = \vect{y}_k + \epsilon_k, \epsilon_k \sim \mathcal{N}(0, \tau_k^2)

    Examples
    --------
    Create the model :math:`\cM: \Rset \mapsto \Rset` and the samples:

    >>> import openturns as ot
    >>> f = ot.SymbolicFunction(['x'], ['x+x * sin(x)'])
    >>> inputSample = ot.Sample([[1.0], [3.0], [5.0], [6.0], [7.0], [8.0]])
    >>> outputSample = f(inputSample)

    Create the algorithm:

    >>> f1 = ot.SymbolicFunction(['x'], ['sin(x)'])
    >>> f2 = ot.SymbolicFunction(['x'], ['x'])
    >>> f3 = ot.SymbolicFunction(['x'], ['cos(x)'])
    >>> basis = ot.Basis([f1,f2, f3])
    >>> covarianceModel = ot.SquaredExponential([1.0])
    >>> covarianceModel.setActiveParameter([])
    >>> algo = ot.GeneralLinearModelAlgorithm(inputSample, outputSample, covarianceModel, basis)
    >>> algo.run()

    Get the resulting meta model:

    >>> result = algo.getResult()
    >>> metamodel = result.getMetaModel()
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
        return _metamodel.GeneralLinearModelAlgorithm_getClassName(self)

    def __repr__(self):
        return _metamodel.GeneralLinearModelAlgorithm___repr__(self)

    def run(self):
        """
        Compute the response surface.

        Notes
        -----
        It computes the response surface and creates a
        :class:`~openturns.GeneralLinearModelResult` structure containing all the results.
        """
        return _metamodel.GeneralLinearModelAlgorithm_run(self)

    def setInputTransformation(self, inputTransformation):
        """
        Set the function normalizing the input.

        Parameters
        ----------
        transformation : :class:`~openturns.Function`
            Function that normalizes the input.
            The input dimension should be the same as input's sample dimension, output dimension
            should be output sample's dimension
        """
        return _metamodel.GeneralLinearModelAlgorithm_setInputTransformation(self, inputTransformation)

    def getInputTransformation(self):
        """
        Get the function normalizing the input.

        Returns
        -------
        transformation : :class:`~openturns.Function`
            Function *T* that normalizes the input.
        """
        return _metamodel.GeneralLinearModelAlgorithm_getInputTransformation(self)

    def getInputSample(self):
        r"""
        Accessor to the input sample.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            The input sample :math:`(\vect{x}_k)_{1 \leq k \leq N}`.
        """
        return _metamodel.GeneralLinearModelAlgorithm_getInputSample(self)

    def getOutputSample(self):
        r"""
        Accessor to the output sample.

        Returns
        -------
        outputSample : :class:`~openturns.Sample`
            The output sample :math:`(\vect{y}_k)_{1 \leq k \leq N}` .
        """
        return _metamodel.GeneralLinearModelAlgorithm_getOutputSample(self)

    def getResult(self):
        """
        Get the results of the metamodel computation.

        Returns
        -------
        result : :class:`~openturns.GeneralLinearModelResult`
            Structure containing all the results obtained after computation
            and created by the method :py:meth:`run`.

        """
        return _metamodel.GeneralLinearModelAlgorithm_getResult(self)

    def getObjectiveFunction(self):
        r"""
        Accessor to the log-likelihood function that writes as argument of the covariance's model parameters.

        Returns
        -------
        logLikelihood : :class:`~openturns.Function`
            The log-likelihood function degined in :eq:`logLikelihood` as a function of :math:`(\vect{\theta}, \vect{\sigma})`.

        Notes
        -----
        The log-likelihood function may be useful for some postprocessing: maximization using external optimizers for example.

        Examples
        --------
        Create the model :math:`\cM: \Rset \mapsto \Rset` and the samples:

        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x0'], ['x0 * sin(x0)'])
        >>> inputSample = ot.Sample([[1.0], [3.0], [5.0], [6.0], [7.0], [8.0]])
        >>> outputSample = f(inputSample)

        Create the algorithm:

        >>> basis = ot.ConstantBasisFactory().build()
        >>> covarianceModel = ot.SquaredExponential(1)
        >>> algo = ot.GeneralLinearModelAlgorithm(inputSample, outputSample, covarianceModel, basis)
        >>> algo.run()

        Get the log-likelihood function:

        >>> likelihoodFunction = algo.getObjectiveFunction()

        """
        return _metamodel.GeneralLinearModelAlgorithm_getObjectiveFunction(self)

    def getOptimizationAlgorithm(self):
        """
        Accessor to solver used to optimize the covariance model parameters.

        Returns
        -------
        algorithm : :class:`~openturns.OptimizationAlgorithm`
            Solver used to optimize the covariance model parameters.
            Default optimizer is :class:`~openturns.TNC`
        """
        return _metamodel.GeneralLinearModelAlgorithm_getOptimizationAlgorithm(self)

    def setOptimizationAlgorithm(self, solver):
        """
        Accessor to the solver used to optimize the covariance model parameters.

        Parameters
        ----------
        algorithm : :class:`~openturns.OptimizationAlgorithm`
            Solver used to optimize the covariance model parameters.
        """
        return _metamodel.GeneralLinearModelAlgorithm_setOptimizationAlgorithm(self, solver)

    def getOptimizeParameters(self):
        """
        Accessor to the covariance model parameters optimization flag.

        Returns
        -------
        optimizeParameters : bool
            Whether to optimize the covariance model parameters.
        """
        return _metamodel.GeneralLinearModelAlgorithm_getOptimizeParameters(self)

    def setOptimizeParameters(self, optimizeParameters):
        """
        Accessor to the covariance model parameters optimization flag.

        Parameters
        ----------
        optimizeParameters : bool
            Whether to optimize the covariance model parameters.
        """
        return _metamodel.GeneralLinearModelAlgorithm_setOptimizeParameters(self, optimizeParameters)

    def setOptimizationBounds(self, optimizationBounds):
        """
        Optimization bounds accessor.

        Parameters
        ----------
        bounds : :class:`~openturns.Interval`
            Bounds for covariance model parameter optimization.

        Notes
        -----
        Parameters involved by this method are:

         - Scale parameters,
         - Amplitude parameters if output dimension is greater than one or
           analytical sigma disabled,
         - Additional parameters.

        Lower & upper bounds are defined in resource map.
        Default lower upper bounds value for all parameters is
        :math:`10^{-2}` and defined thanks to the
        `GeneralLinearModelAlgorithm-DefaultOptimizationLowerBound`
        resource map key.

        For scale parameters, default upper bounds are set as :math:`2`
        times the difference between the max and min values of `X` for
        each coordinate, `X` being the (transformed) input sample.
        The value :math:`2` is defined in resource map
        (`GeneralLinearModelAlgorithm-DefaultOptimizationScaleFactor`).

        Finally for other parameters (amplitude,...), default upper bound is set
        to :math:`100` (corresponding resource map key is
        `GeneralLinearModelAlgorithm-DefaultOptimizationUpperBound`)

        """
        return _metamodel.GeneralLinearModelAlgorithm_setOptimizationBounds(self, optimizationBounds)

    def getOptimizationBounds(self):
        """
        Optimization bounds accessor.

        Returns
        -------
        bounds : :class:`~openturns.Interval`
            Bounds for covariance model parameter optimization.
        """
        return _metamodel.GeneralLinearModelAlgorithm_getOptimizationBounds(self)

    def setNoise(self, noise):
        r"""
        Observation noise variance accessor.

        Parameters
        ----------
        noise : sequence of positive float
            The noise variance :math:`\tau_k^2` of each output value.
        """
        return _metamodel.GeneralLinearModelAlgorithm_setNoise(self, noise)

    def getNoise(self):
        r"""
        Observation noise variance accessor.

        Parameters
        ----------
        noise : sequence of positive float
            The noise variance :math:`\tau_k^2` of each output value.
        """
        return _metamodel.GeneralLinearModelAlgorithm_getNoise(self)

    def __init__(self, *args):
        _metamodel.GeneralLinearModelAlgorithm_swiginit(self, _metamodel.new_GeneralLinearModelAlgorithm(*args))

    __swig_destroy__ = _metamodel.delete_GeneralLinearModelAlgorithm


_metamodel.GeneralLinearModelAlgorithm_swigregister(GeneralLinearModelAlgorithm)

class KrigingAlgorithm(MetaModelAlgorithm):
    r"""
    Kriging algorithm.

    Refer to :ref:`kriging`.

    Available constructors:
        KrigingAlgorithm(*inputSample, outputSample, covarianceModel, basis, normalize=True*)

        KrigingAlgorithm(*inputSample, outputSample, covarianceModel, basisCollection, normalize=True*)

    Parameters
    ----------
    inputSample, outputSample : 2-d sequence of float
        The samples :math:`(\vect{x}_k)_{1 \leq k \leq N} \in \Rset^d` and :math:`(\vect{y}_k)_{1 \leq k \leq N}\in \Rset^p` upon which the meta-model is built.
    covarianceModel : :class:`~openturns.CovarianceModel`
        Covariance model used for the underlying Gaussian process assumption.
    basis : :class:`~openturns.Basis`
        Functional basis to estimate the trend (universal kriging): :math:`(\varphi_j)_{1 \leq j \leq n_1}: \Rset^d \rightarrow \Rset`.

        If :math:`p>1`, the same basis is used for each marginal output.
    basisCollection : sequence of :class:`~openturns.Basis`
        Collection of :math:`p` functional basis: one basis for each marginal output: :math:`\left[(\varphi_j^1)_{1 \leq j \leq n_1}, \dots, (\varphi_j^p)_{1 \leq j \leq n_p}\right]`. If the sequence is empty, no trend coefficient is estimated (simple kriging).

    normalize : bool, optional
        Indicates whether the input sample has to be normalized.

        Default value is True. It implies working on centered & reduced input sample.

    Notes
    -----
    We suppose we have a sample :math:`(\vect{x}_k, \vect{y}_k)_{1 \leq k \leq N}` where :math:`\vect{y}_k = \cM(\vect{x}_k)` for all *k*, with :math:`\cM:\Rset^d \mapsto \Rset^p` the model.

    The meta model *Kriging* is based on the same principles as those of the general linear model: it assumes that the sample :math:`(\vect{y}_k)_{1 \leq k \leq N}` is considered as the trace of a Gaussian process :math:`\vect{Y}(\omega, \vect{x})` on :math:`(\vect{x}_k)_{1 \leq k \leq N}`. The Gaussian process :math:`\vect{Y}(\omega, \vect{x})` is defined by:

    .. math::
        :label: metaModelKrigAlgo

        \vect{Y}(\omega, \vect{x}) = \vect{\mu}(\vect{x}) + W(\omega, \vect{x})

    where:

    .. math::

        \vect{\mu}(\vect{x}) = \left(
          \begin{array}{l}
            \mu_1(\vect{x}) \\
            \dots  \\
            \mu_p(\vect{x}) 
           \end{array}
         \right)

    with :math:`\mu_l(\vect{x}) = \sum_{j=1}^{n_l} \beta_j^l \varphi_j^l(\vect{x})` and :math:`\varphi_j^l: \Rset^d \rightarrow \Rset` the trend functions.

    :math:`W` is a Gaussian process of dimension *p* with zero mean and covariance function :math:`C = C(\vect{\theta}, \vect{\sigma}, \mat{R}, \vect{\lambda})` (see :class:`~openturns.CovarianceModel` for the notations).

    The estimation of the all parameters (the trend coefficients :math:`\beta_j^l`, the scale :math:`\vect{\theta}` and the amplitude :math:`\vect{\sigma}`) are made by the :class:`~openturns.GeneralLinearModelAlgorithm` class.

    The Kriging algorithm makes the general linear model interpolary on the input samples. The Kriging meta model :math:`\tilde{\cM}` is defined by:

    .. math::

        \tilde{\cM}(\vect{x}) =  \vect{\mu}(\vect{x}) + \Expect{\vect{Y}(\omega, \vect{x})\, | \,  \cC}

    where :math:`\cC` is the condition :math:`\vect{Y}(\omega, \vect{x}_k) = \vect{y}_k` for each :math:`k \in [1, N]`.

    :eq:`metaModelKrigAlgo` writes:

    .. math::

        \tilde{\cM}(\vect{x}) = \vect{\mu}(\vect{x}) + \Cov{\vect{Y}(\omega, \vect{x}), (\vect{Y}(\omega, \vect{x}_1), \dots, \vect{Y}(\omega, \vect{x}_N))} \vect{\gamma}

    where :math:`\Cov{\vect{Y}(\omega, \vect{x}), (\vect{Y}(\omega, \vect{x}_1), \dots, \vect{Y}(\omega, \vect{x}_N))} = \left( \mat{C}( \vect{x},  \vect{x}_1) | \dots | \mat{C}( \vect{x},  \vect{x}_N)  \right)` is a matrix in :math:`\cM_{p,NP}(\Rset)` and :math:`\vect{\gamma} = \mat{C}^{-1}(\vect{y}-\vect{m})`.

    A known centered gaussian observation noise :math:`\epsilon_k` can be taken into account
    with :func:`setNoise()`:

    .. math:: \hat{\vect{y}}_k = \vect{y}_k + \epsilon_k, \epsilon_k \sim \mathcal{N}(0, \tau_k^2)

    Examples
    --------
    Create the model :math:`\cM: \Rset \mapsto \Rset` and the samples:

    >>> import openturns as ot
    >>> f = ot.SymbolicFunction(['x'],  ['x * sin(x)'])
    >>> sampleX = [[1.0], [2.0], [3.0], [4.0], [5.0], [6.0], [7.0], [8.0]]
    >>> sampleY = f(sampleX)

    Create the algorithm:

    >>> basis = ot.Basis([ot.SymbolicFunction(['x'], ['x']), ot.SymbolicFunction(['x'], ['x^2'])])
    >>> covarianceModel = ot.SquaredExponential([1.0])
    >>> covarianceModel.setActiveParameter([])
    >>> algo = ot.KrigingAlgorithm(sampleX, sampleY, covarianceModel, basis)
    >>> algo.run()

    Get the resulting meta model:

    >>> result = algo.getResult()
    >>> metamodel = result.getMetaModel()
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
        return _metamodel.KrigingAlgorithm_getClassName(self)

    def __repr__(self):
        return _metamodel.KrigingAlgorithm___repr__(self)

    def run(self):
        """
        Compute the response surface.

        Notes
        -----
        It computes the kriging response surface and creates a
        :class:`~openturns.KrigingResult` structure containing all the results.
        """
        return _metamodel.KrigingAlgorithm_run(self)

    def getInputSample(self):
        r"""
        Accessor to the input sample.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            The input sample :math:`(\vect{x}_k)_{1 \leq k \leq N}`.

        """
        return _metamodel.KrigingAlgorithm_getInputSample(self)

    def getOutputSample(self):
        r"""
        Accessor to the output sample.

        Returns
        -------
        outputSample : :class:`~openturns.Sample`
            The output sample :math:`(\vect{y}_k)_{1 \leq k \leq N}` .

        """
        return _metamodel.KrigingAlgorithm_getOutputSample(self)

    def getResult(self):
        """
        Get the results of the metamodel computation.

        Returns
        -------
        result : :class:`~openturns.KrigingResult`
            Structure containing all the results obtained after computation
            and created by the method :py:meth:`run`.

        """
        return _metamodel.KrigingAlgorithm_getResult(self)

    def getOptimizationAlgorithm(self):
        """
        Accessor to solver used to optimize the covariance model parameters.

        Returns
        -------
        algorithm : :class:`~openturns.OptimizationAlgorithm`
            Solver used to optimize the covariance model parameters.
        """
        return _metamodel.KrigingAlgorithm_getOptimizationAlgorithm(self)

    def setOptimizationAlgorithm(self, solver):
        r"""
        Accessor to the solver used to optimize the covariance model parameters.

        Parameters
        ----------
        algorithm : :class:`~openturns.OptimizationAlgorithm`
            Solver used to optimize the covariance model parameters.

        Examples
        --------
        Create the model :math:`\cM: \Rset \mapsto \Rset` and the samples:

        >>> import openturns as ot
        >>> input_data = ot.Uniform(-1.0, 2.0).getSample(10)
        >>> model = ot.SymbolicFunction(['x'], ['x-1+sin(pi_*x/(1+0.25*x^2))'])
        >>> output_data = model(input_data)

        Create the Kriging algorithm with the optimizer option:

        >>> basis = ot.Basis([ot.SymbolicFunction(['x'], ['0.0'])])
        >>> thetaInit = 1.0
        >>> covariance = ot.GeneralizedExponential([thetaInit], 2.0)
        >>> bounds = ot.Interval(1e-2,1e2)
        >>> algo = ot.KrigingAlgorithm(input_data, output_data, covariance, basis)
        >>> algo.setOptimizationBounds(bounds)

        """
        return _metamodel.KrigingAlgorithm_setOptimizationAlgorithm(self, solver)

    def setOptimizationBounds(self, optimizationBounds):
        """
        Accessor to the optimization bounds.

        Parameters
        ----------
        bounds : :class:`~openturns.Interval`
            The bounds used for numerical optimization of the likelihood.

        Notes
        -----
        See :class:`~openturns.GeneralLinearModelAlgorithm` class for more details,
        particularly :meth:`~openturns.GeneralLinearModelAlgorithm.setOptimizationBounds`.
        """
        return _metamodel.KrigingAlgorithm_setOptimizationBounds(self, optimizationBounds)

    def getOptimizationBounds(self):
        """
        Accessor to the optimization bounds.

        Returns
        -------
        problem : :class:`~openturns.Interval`
            The bounds used for numerical optimization of the likelihood.
        """
        return _metamodel.KrigingAlgorithm_getOptimizationBounds(self)

    def getReducedLogLikelihoodFunction(self):
        r"""
        Accessor to the reduced log-likelihood function that writes as argument of the covariance's model parameters.

        Returns
        -------
        reducedLogLikelihood : :class:`~openturns.Function`
            The *potentially* reduced log-likelihood function.

        Notes
        -----
        We use the same notations as in :class:`~openturns.CovarianceModel` and :class:`~openturns.GeneralLinearModelAlgorithm` : :math:`\vect{\theta}` refers to the scale parameters and
        :math:`\vect{\sigma}` the amplitude. We can consider three situtations here:

          - Output dimension is :math:`\geq 2`. In that case, we get the **full** log-likelihood function :math:`\mathcal{L}(\vect{\theta}, \vect{\sigma})`.

          - Output dimension is **1** and the `GeneralLinearModelAlgorithm-UseAnalyticalAmplitudeEstimate` key of :class:`~openturns.ResourceMap` is set to *True*.
            The amplitude parameter of the covariance model :math:`\vect{\theta}` is in the active set of parameters and thus we get the **reduced**
            log-likelihood function :math:`\mathcal{L}(\vect{\theta})`.

          - Output dimension is **1** and the `GeneralLinearModelAlgorithm-UseAnalyticalAmplitudeEstimate` key of :class:`~openturns.ResourceMap` is set to *False*.
            In that case, we get the **full** log-likelihood :math:`\mathcal{L}(\vect{\theta}, \vect{\sigma})`.

        The reduced log-likelihood function may be useful for some pre/postprocessing: vizualisation of the maximizer, use of an external optimizers to maximize the reduced log-likelihood etc.

        Examples
        --------
        Create the model :math:`\cM: \Rset \mapsto \Rset` and the samples:

        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x0'], ['x0 * sin(x0)'])
        >>> inputSample = ot.Sample([[1.0], [3.0], [5.0], [6.0], [7.0], [8.0]])
        >>> outputSample = f(inputSample)

        Create the algorithm:

        >>> basis = ot.ConstantBasisFactory().build()
        >>> covarianceModel = ot.SquaredExponential(1)
        >>> algo = ot.KrigingAlgorithm(inputSample, outputSample, covarianceModel, basis)
        >>> algo.run()

        Get the reduced log-likelihood function:

        >>> reducedLogLikelihoodFunction = algo.getReducedLogLikelihoodFunction()

        """
        return _metamodel.KrigingAlgorithm_getReducedLogLikelihoodFunction(self)

    def getOptimizeParameters(self):
        """
        Accessor to the covariance model parameters optimization flag.

        Returns
        -------
        optimizeParameters : bool
            Whether to optimize the covariance model parameters.
        """
        return _metamodel.KrigingAlgorithm_getOptimizeParameters(self)

    def setOptimizeParameters(self, optimizeParameters):
        """
        Accessor to the covariance model parameters optimization flag.

        Parameters
        ----------
        optimizeParameters : bool
            Whether to optimize the covariance model parameters.
        """
        return _metamodel.KrigingAlgorithm_setOptimizeParameters(self, optimizeParameters)

    def setNoise(self, noise):
        r"""
        Observation noise variance accessor.

        Parameters
        ----------
        noise : sequence of positive float
            The noise variance :math:`\tau_k^2` of each output value.
        """
        return _metamodel.KrigingAlgorithm_setNoise(self, noise)

    def getNoise(self):
        r"""
        Observation noise variance accessor.

        Returns
        -------
        noise : sequence of positive float
            The noise variance :math:`\tau_k^2` of each output value.
        """
        return _metamodel.KrigingAlgorithm_getNoise(self)

    def __init__(self, *args):
        _metamodel.KrigingAlgorithm_swiginit(self, _metamodel.new_KrigingAlgorithm(*args))

    __swig_destroy__ = _metamodel.delete_KrigingAlgorithm


_metamodel.KrigingAlgorithm_swigregister(KrigingAlgorithm)

class LinearModelStepwiseAlgorithm(openturns.common.PersistentObject):
    r"""
    Class used to create a linear model from numerical samples.

    **Available usages**:

        LinearModelStepwiseAlgorithm(*inputSample, basis, outputSample, minimalIndices, isForward, penalty, maximumIterationNumber*)

        LinearModelStepwiseAlgorithm(*inputSample, basis, outputSample, minimalIndices, startIndices, penalty, maximumIterationNumber*)

    Parameters
    ----------
    inputSample, outputSample : 2-d sequence of float
        The input and output samples of a model.
    basis : :class:`~openturns.Basis`
        Functional basis to estimate the trend.
    minimalIndices : sequence of int
        The indices of minimal model
    isForward : bool
          the boolean value used for the stepwise regression method direction FORWARD and BACKWARD.
    startIndices : sequence of int
         The indices of start model used for the stepwise regression method direction BOTH.
    penalty : float
         The multiple of the degrees of freedom used for the penalty of the stepwise regression method:

         - 2      Akaike   information criterion (AIC)
         - log(n) Bayesian information criterion (BIC)
    maximumIterationNumber : int
         The maximum number of iterations of the stepwise regression method.

    See Also
    --------
    LinearModel, LinearModelResult

    Notes
    -----
    This class is used in order to create a linear model from numerical samples, by using
    the stepwise method. The linear regression model between the scalar variable :math:`Y`
    and the :math:`n`-dimensional one :math:`\vect{X} = (X_i)_{i \leq n}` writes as follows:

    .. math::

        \tilde{Y} = a_0 + \sum_{i=1}^n a_i X_i + \epsilon

    where :math:`\epsilon` is the residual, supposed to follow the standard Normal
    distribution.

    Each coefficient :math:`a_i` is evaluated from both samples :math:`Ysample` and
    :math:`Xsample` and is accompagnied by a confidence interval and a p-value (which
    tests if they are significantly different from 0.0).

    By default, input sample is normalized.  It is possible to set Resource key
    (``LinearModelStepwiseAlgorithm-normalize``) to *False* in order to discard
    this normalization.

    This class enables to test the quality of the model. It provides only numerical
    tests. If :math:`X` is scalar, a graphical validation test exists, that draws
    the residual couples :math:`(\epsilon_i, \epsilon_{i+1})`, where the residual
    :math:`\epsilon_i` is evaluated on the samples :math:`(Xsample, Ysample)`:
    :math:`\epsilon_i  = Ysample_i - \tilde{Y}_i` with
    :math:`\tilde{Y}_i = a_0 + a_1 + Xsample_i`. The method is
    :class:`~openturns.VisualTest_DrawLinearModelResidual`.

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
        return _metamodel.LinearModelStepwiseAlgorithm_getClassName(self)

    BACKWARD = _metamodel.LinearModelStepwiseAlgorithm_BACKWARD
    BOTH = _metamodel.LinearModelStepwiseAlgorithm_BOTH
    FORWARD = _metamodel.LinearModelStepwiseAlgorithm_FORWARD

    def __repr__(self):
        return _metamodel.LinearModelStepwiseAlgorithm___repr__(self)

    def __str__(self, *args):
        return _metamodel.LinearModelStepwiseAlgorithm___str__(self, *args)

    def getInputSample(self):
        """
        Accessor to the input sample.

        Returns
        -------
        input_sample : :class:`~openturns.Sample`
            Input sample.
        """
        return _metamodel.LinearModelStepwiseAlgorithm_getInputSample(self)

    def getOutputSample(self):
        """
        Accessor to the output sample.

        Returns
        -------
        output_sample : :class:`~openturns.Sample`
            Output sample.
        """
        return _metamodel.LinearModelStepwiseAlgorithm_getOutputSample(self)

    def getDirection(self):
        """
        Accessor to the direction.

        Returns
        -------
        direction : int
            Direction.
        """
        return _metamodel.LinearModelStepwiseAlgorithm_getDirection(self)

    def getPenalty(self):
        """
        Accessor to the penalty.

        Returns
        -------
        penalty : float
            Penalty.
        """
        return _metamodel.LinearModelStepwiseAlgorithm_getPenalty(self)

    def getMaximumIterationNumber(self):
        """
        Accessor to the maximum iteration number.

        Returns
        -------
        maximum_iteration : int
            Maximum number of iterations.
        """
        return _metamodel.LinearModelStepwiseAlgorithm_getMaximumIterationNumber(self)

    def getFormula(self):
        """
        Accessor to the formula.

        Returns
        -------
        formula : str
            Formula.
        """
        return _metamodel.LinearModelStepwiseAlgorithm_getFormula(self)

    def run(self):
        """Run the algorithm."""
        return _metamodel.LinearModelStepwiseAlgorithm_run(self)

    def getResult(self):
        """
        Accessor to the result.

        Returns
        -------
        result : :class:`~openturns.LinearModelResult`
            Result.
        """
        return _metamodel.LinearModelStepwiseAlgorithm_getResult(self)

    def __init__(self, *args):
        _metamodel.LinearModelStepwiseAlgorithm_swiginit(self, _metamodel.new_LinearModelStepwiseAlgorithm(*args))

    __swig_destroy__ = _metamodel.delete_LinearModelStepwiseAlgorithm


_metamodel.LinearModelStepwiseAlgorithm_swigregister(LinearModelStepwiseAlgorithm)

class LinearModelAlgorithm(MetaModelAlgorithm):
    r"""
    Class used to create a linear model from numerical samples.

    **Available usages**:

        LinearModelAlgorithm(Xsample, Ysample)

        LinearModelAlgorithm(Xsample, basis, Ysample)

    Parameters
    ----------
    XSample : 2-d sequence of float
        The input samples of a model.

    YSample : 2-d sequence of float
        The output samples of a model, must be of dimension 1.

    basis : :class:`~openturns.Basis`
        The :math:`\phi` basis .

    See Also
    --------
    LinearModelResult

    Notes
    -----
    This class is used in order to create a linear model from data samples. The
    linear regression model between the scalar variable :math:`Y` and the :math:`n`
    -dimensional vector :math:`\vect{X} = (X_i)_{i \leq n}` writes as follows:

    .. math::

        \tilde{Y} = \sum_{i=0}^p a_i \phi_i(X) + \epsilon

    where :math:`\epsilon` is the residual, supposed to follow the standard Normal
    distribution, :math:`\phi` a functional basis.
    The algorithm class enables to estimate the coefficients of the linear expansion.

    If basis is not specified, the underlying model is :

    .. math::

        \tilde{Y} = a_0 + \sum_{i=1}^n a_i X_i + \epsilon

    The coefficients :math:`a_i` are evaluated using a least squares method. Default
     method is `QR`. User might choose also `SVD` or `Cholesky` (usefull if basis
     is orthogonal) and large dataset.

    The evaluation of the coefficients is completed by some usefull parameters that could
    help the diagnostic of the linearity.
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
        return _metamodel.LinearModelAlgorithm_getClassName(self)

    def __repr__(self):
        return _metamodel.LinearModelAlgorithm___repr__(self)

    def getInputSample(self):
        """
        Accessor to the input sample.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            The Xsample which had been passed to the constructor.
        """
        return _metamodel.LinearModelAlgorithm_getInputSample(self)

    def getOutputSample(self):
        """
        Accessor to the output sample.

        Returns
        -------
        outputSample : :class:`~openturns.Sample`
            The Ysample which had been passed to the constructor.
        """
        return _metamodel.LinearModelAlgorithm_getOutputSample(self)

    def getBasis(self):
        """
        Accessor to the input basis.

        Returns
        -------
        basis : :class:`~openturns.Basis`
            The basis which had been passed to the constructor.
        """
        return _metamodel.LinearModelAlgorithm_getBasis(self)

    def run(self):
        """
        Compute the response surfaces.

        Notes
        -----
        It computes the response surfaces and creates a
        :class:`~openturns.MetaModelResult` structure containing all the results.
        """
        return _metamodel.LinearModelAlgorithm_run(self)

    def getResult(self):
        """
        Accessor to the computed linear model.

        Returns
        -------
        result : :class:`~openturns.LinearModelResult`
            The linear model built from numerical samples, along with other useful informations.
        """
        return _metamodel.LinearModelAlgorithm_getResult(self)

    def __init__(self, *args):
        _metamodel.LinearModelAlgorithm_swiginit(self, _metamodel.new_LinearModelAlgorithm(*args))

    __swig_destroy__ = _metamodel.delete_LinearModelAlgorithm


_metamodel.LinearModelAlgorithm_swigregister(LinearModelAlgorithm)

class LinearModelAnalysis(openturns.common.PersistentObject):
    """
    Analyse a linear model.

    Available constructors:
        LinearModelAnalysis(linearModelResult)

    Parameters
    ----------
    linearModelResult : :class:`~openturns.LinearModelResult`
        A linear model result.

    See Also
    --------
    LinearModelResult

    Notes
    -----
    This class relies on a linear model result structure and performs diagnostic 
    of linearity. This diagnostic mainly relies on graphics and a `summary` like
    function (pretty-print)

    By default, on graphs, labels of the 3 most significant points are displayed.
    This number can be changed by modifying the ResourceMap key
    (``LinearModelAnalysis-Identifiers``).

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> Xsample = distribution.getSample(30)
    >>> func = ot.SymbolicFunction(['x'], ['2 * x + 1'])
    >>> Ysample = func(Xsample) + ot.Normal().getSample(30)
    >>> algo = ot.LinearModelAlgorithm(Ysample, Xsample)
    >>> result = algo.getResult()
    >>> analysis = ot.LinearModelAnalysis(result)

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
        return _metamodel.LinearModelAnalysis_getClassName(self)

    def __repr__(self):
        return _metamodel.LinearModelAnalysis___repr__(self)

    def __str__(self, *args):
        return _metamodel.LinearModelAnalysis___str__(self, *args)

    def getLinearModelResult(self):
        """
        Accessor to the linear model result.

        Returns
        -------
        linearModelResult : :class:`~openturns.LinearModelResult`
            The  linear model result which had been passed to the constructor.
        """
        return _metamodel.LinearModelAnalysis_getLinearModelResult(self)

    def getCoefficientsTScores(self):
        """
        Accessor to the coefficients of linear expansion over their standard error.

        Returns
        -------
        tScores : :class:`~openturns.Point`

        """
        return _metamodel.LinearModelAnalysis_getCoefficientsTScores(self)

    def getCoefficientsPValues(self):
        """
        Accessor to the coefficients of the p values.

        Returns
        -------
        pValues : :class:`~openturns.Point`

        """
        return _metamodel.LinearModelAnalysis_getCoefficientsPValues(self)

    def getCoefficientsConfidenceInterval(self, level=0.95):
        r"""
        Accessor to the confidence interval of level :math:`\alpha` for the coefficients
        of the linear expansion

        Returns
        -------
        confidenceInterval : :class:`~openturns.Interval`

        """
        return _metamodel.LinearModelAnalysis_getCoefficientsConfidenceInterval(self, level)

    def getFisherScore(self):
        """
        Accessor to the Fisher test.

        Returns
        -------
        fisherScore : float

        """
        return _metamodel.LinearModelAnalysis_getFisherScore(self)

    def getFisherPValue(self):
        """
        Accessor to the Fisher p value.

        Returns
        -------
        fisherPValue : float

        """
        return _metamodel.LinearModelAnalysis_getFisherPValue(self)

    def getNormalityTestResultKolmogorovSmirnov(self):
        """
        Performs Kolmogorov test.

        Performs Kolmogorov test to check Gaussian assumption of the model (null hypothesis).

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Test result class.

        Notes
        -----
        We check that the residual is Gaussian thanks to :class:`~openturns.FittingTest::Kolmogorov`.
        """
        return _metamodel.LinearModelAnalysis_getNormalityTestResultKolmogorovSmirnov(self)

    def getNormalityTestResultAndersonDarling(self):
        """
        Performs Anderson-Darling test.
        The statistical test checks the Gaussian assumption of the model (null hypothesis).

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Test result class.

        Notes
        -----
        We check that the residual is Gaussian thanks to :class:`~openturns.NormalityTest::AndersonDarling`.
        """
        return _metamodel.LinearModelAnalysis_getNormalityTestResultAndersonDarling(self)

    def getNormalityTestResultChiSquared(self):
        """
        Performs Chi-Square test.
        The statistical test checks the Gaussian assumption of the model (null hypothesis).

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Test result class.

        Notes
        -----
        The Chi-Square test is a goodness of fit test which objective is to check the
        normality assumption (null hypothesis) of residuals (and thus the model).

        Usually, Chi-Square test applies for discrete distributions. Here we rely on
        the :class:`~openturns.FittingTest_ChiSquared` to check the normality.

        """
        return _metamodel.LinearModelAnalysis_getNormalityTestResultChiSquared(self)

    def getNormalityTestCramerVonMises(self):
        """
        Performs Cramer-Von Mises test.

        The statistical test checks the Gaussian assumption of the model (null hypothesis).

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Test result class.

        Notes
        -----
        We check that the residual is Gaussian thanks to :class:`~openturns.NormalityTest::CramerVonMisesNormal`.
        """
        return _metamodel.LinearModelAnalysis_getNormalityTestCramerVonMises(self)

    def drawModelVsFitted(self):
        """
        Accessor to plot of model versus fitted values.

        Returns
        -------
        graph : :class:`~openturns.Graph`

        """
        return _metamodel.LinearModelAnalysis_drawModelVsFitted(self)

    def drawResidualsVsFitted(self):
        """
        Accessor to plot of residuals versus fitted values.

        Returns
        -------
        graph : :class:`~openturns.Graph`

        """
        return _metamodel.LinearModelAnalysis_drawResidualsVsFitted(self)

    def drawScaleLocation(self):
        """
        Accessor to a Scale-Location plot of sqrt(abs(residuals)) versus fitted values.

        Returns
        -------
        graph : :class:`~openturns.Graph`

        """
        return _metamodel.LinearModelAnalysis_drawScaleLocation(self)

    def drawQQplot(self):
        """
        Accessor to plot a Normal quantiles-quantiles plot of standardized residuals.

        Returns
        -------
        graph : :class:`~openturns.Graph`

        """
        return _metamodel.LinearModelAnalysis_drawQQplot(self)

    def drawCookDistance(self):
        """
        Accessor to plot of Cook's distances versus row labels.

        Returns
        -------
        graph : :class:`~openturns.Graph`

        """
        return _metamodel.LinearModelAnalysis_drawCookDistance(self)

    def drawResidualsVsLeverages(self):
        """
        Accessor to plot of residuals versus leverages that adds bands corresponding to Cook's distances of 0.5 and 1.

        Returns
        -------
        graph : :class:`~openturns.Graph`

        """
        return _metamodel.LinearModelAnalysis_drawResidualsVsLeverages(self)

    def drawCookVsLeverages(self):
        """
        Accessor to plot of Cook's distances versus leverage/(1-leverage). 

        Returns
        -------
        graph : :class:`~openturns.Graph`

        """
        return _metamodel.LinearModelAnalysis_drawCookVsLeverages(self)

    def __init__(self, *args):
        _metamodel.LinearModelAnalysis_swiginit(self, _metamodel.new_LinearModelAnalysis(*args))

    __swig_destroy__ = _metamodel.delete_LinearModelAnalysis


_metamodel.LinearModelAnalysis_swigregister(LinearModelAnalysis)

class LinearModelTest(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr

    @staticmethod
    def LinearModelFisher(*args):
        r"""
        Test the nullity of the linear regression model coefficients.

        **Available usages**:

            LinearModelTest.LinearModelFisher(*firstSample, secondSample*)

            LinearModelTest.LinearModelFisher(*firstSample, secondSample, level*)

            LinearModelTest.LinearModelFisher(*firstSample, secondSample, linearModelResult*)

            LinearModelTest.LinearModelFisher(*firstSample, secondSample, linearModelResult, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample, of dimension 1.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        linearModelResult : :class:`~openturns.LinearModelResult`
            A linear model. If not provided, it is built using the given samples.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        LinearModelTest_LinearModelResidualMean

        Notes
        -----
        The LinearModelTest class is used through its static methods in order to evaluate
        the quality of the linear regression model between two samples.
        The linear regression model between the
        scalar variable :math:`Y` and the :math:`n`-dimensional one
        :math:`\vect{X} = (X_i)_{i \leq n}` is as follows:

        .. math::

            \tilde{Y} = a_0 + \sum_{i=1}^n a_i X_i + \epsilon

        where :math:`\epsilon` is the residual, supposed to follow the standard Normal
        distribution.

        The LinearModelFisher test checks the nullity of the regression linear model
        coefficients (Fisher distribution is used).

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> func = ot.SymbolicFunction('x', '2 * x + 1')
        >>> firstSample = sample
        >>> secondSample = func(sample) + ot.Normal().getSample(30)
        >>> test_result = ot.LinearModelTest.LinearModelFisher(firstSample, secondSample)
        >>> print(test_result.getPValue())
        5.1...e-12

        """
        return _metamodel.LinearModelTest_LinearModelFisher(*args)

    @staticmethod
    def LinearModelResidualMean(*args):
        r"""
        Test zero mean value of the residual of the linear regression model.

        **Available usages**:

            LinearModelTest.LinearModelResidualMean(*firstSample, secondSample*)

            LinearModelTest.LinearModelResidualMean(*firstSample, secondSample, level*)

            LinearModelTest.LinearModelResidualMean(*firstSample, secondSample, linearModelResult*)

            LinearModelTest.LinearModelResidualMean(*firstSample, secondSample, linearModelResult, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample, of dimension 1.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        linearModelResult : :class:`~openturns.LinearModelResult`
            A linear model. If not provided, it is built using the given samples.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        LinearModelTest_LinearModelFisher, LinearModelTest_LinearModelHarrisonMcCabe

        Notes
        -----
        The LinearModelTest class is used through its static methods in order to evaluate
        the quality of the linear regression model between two samples.
        The linear regression model between the
        scalar variable :math:`Y` and the :math:`n`-dimensional one
        :math:`\vect{X} = (X_i)_{i \leq n}` is as follows:

        .. math::

            \tilde{Y} = a_0 + \sum_{i=1}^n a_i X_i + \epsilon

        where :math:`\epsilon` is the residual, supposed to follow the standard Normal
        distribution.

        The LinearModelResidualMean Test checks, under the hypothesis of a gaussian
        sample, if the mean of the residual is equal to zero. It is based on the Student
        test (equality of mean for two gaussian samples).

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> func = ot.SymbolicFunction('x', '2 * x + 1')
        >>> firstSample = sample
        >>> secondSample = func(sample) + ot.Normal().getSample(30)
        >>> test_result = ot.LinearModelTest.LinearModelResidualMean(firstSample, secondSample)

        """
        return _metamodel.LinearModelTest_LinearModelResidualMean(*args)

    @staticmethod
    def LinearModelHarrisonMcCabe(*args):
        r"""
        Test the homoskedasticity of the linear regression model residuals.

        **Available usages**:

            LinearModelTest.LinearModelHarrisonMcCabe(*firstSample, secondSample*)

            LinearModelTest.LinearModelHarrisonMcCabe(*firstSample, secondSample, linearModelResult*)

            LinearModelTest.LinearModelHarrisonMcCabe(*firstSample, secondSample, level, breakPoint, simulationSize*)

            LinearModelTest.LinearModelHarrisonMcCabe(*firstSample, secondSample, linearModelResult, level, breakPoint, simulationSize*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample, of dimension 1.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        linearModelResult : :class:`~openturns.LinearModelResult`
            A linear model. If not provided, it is built using the given samples.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.
        breakPoint : positive float :math:`< 1`
            Percentage of data to be taken as breakPoint in the variances. It must be
            :math:`< 1`, equal to 0.5 by default.
        simulationSize : positive int
            Size of the sample used to compute the p-value. Default is 1000.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        LinearModelTest_LinearModelBreuschPagan, LinearModelTest_LinearModelResidualMean,
        LinearModelTest_LinearModelDurbinWatson

        Notes
        -----
        The LinearModelTest class is used through its static methods in order to evaluate
        the quality of the linear regression model between two samples.
        The linear regression model between the
        scalar variable :math:`Y` and the :math:`n`-dimensional one
        :math:`\vect{X} = (X_i)_{i \leq n}` is as follows:

        .. math::

            \tilde{Y} = a_0 + \sum_{i=1}^n a_i X_i + \epsilon

        where :math:`\epsilon` is the residual.

        The Harrison-McCabe test checks the heteroskedasticity of the residuals. The
        breakpoint in the variances is set by default to the half of the sample. The
        p-value is estimed using simulation. If the binary quality measure is false, then
        the homoskedasticity hypothesis can be rejected with respect to the given level.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> func = ot.SymbolicFunction('x', '2 * x + 1')
        >>> firstSample = sample
        >>> secondSample = func(sample) + ot.Normal().getSample(30)
        >>> test_result = ot.LinearModelTest.LinearModelHarrisonMcCabe(firstSample, secondSample)
        >>> print(test_result)
        class=TestResult name=Unnamed type=HarrisonMcCabe binaryQualityMeasure=true p-value threshold=0.05 p-value=0.142 statistic=0.373225 description=[]

        """
        return _metamodel.LinearModelTest_LinearModelHarrisonMcCabe(*args)

    @staticmethod
    def LinearModelBreuschPagan(*args):
        r"""
        Test the homoskedasticity of the linear regression model residuals.

        **Available usages**:

            LinearModelTest.LinearModelBreuschPagan(*firstSample, secondSample*)

            LinearModelTest.LinearModelBreuschPagan(*firstSample, secondSample, linearModelResult*)

            LinearModelTest.LinearModelBreuschPagan(*firstSample, secondSample, level*)

            LinearModelTest.LinearModelBreuschPagan(*firstSample, secondSample, linearModelResult, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample, of dimension 1.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        linearModelResult : :class:`~openturns.LinearModelResult`
            A linear model. If not provided, it is built using the given samples.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        LinearModelTest_LinearModelHarrisonMcCabe, LinearModelTest_LinearModelResidualMean,
        LinearModelTest_LinearModelDurbinWatson

        Notes
        -----
        The LinearModelTest class is used through its static methods in order to evaluate
        the quality of the linear regression model between two samples.
        The linear regression model between the
        scalar variable :math:`Y` and the :math:`n`-dimensional one
        :math:`\vect{X} = (X_i)_{i \leq n}` is as follows:

        .. math::

            \tilde{Y} = a_0 + \sum_{i=1}^n a_i X_i + \epsilon

        where :math:`\epsilon` is the residual.

        The Breusch-Pagan test checks the heteroskedasticity of the residuals. A linear
        regression model is fitted on the squared residuals. The statistic is computed
        using the Studendized version with the chi-squared distribution. If the binary
        quality measure is false, then the homoskedasticity hypothesis can be rejected
        with respect to the given level.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> func = ot.SymbolicFunction('x', '2 * x + 1')
        >>> firstSample = sample
        >>> secondSample = func(sample) + ot.Normal().getSample(30)
        >>> test_result = ot.LinearModelTest.LinearModelBreuschPagan(firstSample, secondSample)
        >>> print(test_result)
        class=TestResult name=Unnamed type=BreuschPagan binaryQualityMeasure=true p-value threshold=0.05 p-value=0.700772 statistic=0.14767 description=[]

        """
        return _metamodel.LinearModelTest_LinearModelBreuschPagan(*args)

    @staticmethod
    def LinearModelDurbinWatson(*args):
        r"""
        Test the autocorrelation of the linear regression model residuals.

        **Available usages**:

            LinearModelTest.LinearModelDurbinWatson(*firstSample, secondSample*)

            LinearModelTest.LinearModelDurbinWatson(*firstSample, secondSample, hypothesis, level*)

            LinearModelTest.LinearModelDurbinWatson(*firstSample, secondSample, linearModelResult*)

            LinearModelTest.LinearModelDurbinWatson(*firstSample, secondSample, linearModelResult, hypothesis, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        linearModelResult : :class:`~openturns.LinearModelResult`
            A linear model. If not provided, it is built using the given samples.
        hypothesis : str
            Hypothesis H0 for the residuals. It can be : 'Equal' to 0, 'Less' than 0 or
            'Greater' than 0. Default is set to 'Equal' to 0.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        LinearModelTest_LinearModelBreuschPagan, LinearModelTest_LinearModelHarrisonMcCabe, LinearModelTest_LinearModelResidualMean

        Notes
        -----
        The LinearModelTest class is used through its static methods in order to evaluate
        the quality of the linear regression model between two samples.
        The linear regression model between the
        scalar variable :math:`Y` and the :math:`n`-dimensional one
        :math:`\vect{X} = (X_i)_{i \leq n}` is as follows:

        .. math::

            \tilde{Y} = a_0 + \sum_{i=1}^n a_i X_i + \epsilon

        where :math:`\epsilon` is the residual.

        The Durbin-Watson test checks the autocorrelation of the residuals. It is possible
        to test is the autocorrelation is equal to 0, and less or greater than 0. The
        p-value is computed using a normal approximation with mean and variance of the
        Durbin-Watson test statistic. If the binary quality measure is false, then the
        given autocorrelation hypothesis can be rejected with respect to the given level.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> func = ot.SymbolicFunction('x', '2 * x + 1')
        >>> firstSample = sample
        >>> secondSample = func(sample) + ot.Normal().getSample(30)
        >>> test_result = ot.LinearModelTest.LinearModelDurbinWatson(firstSample, secondSample)
        >>> print(test_result)
        class=TestResult name=Unnamed type=DurbinWatson binaryQualityMeasure=true p-value threshold=0.05 p-value=0.653603 statistic=0.448763 description=[H0: auto.cor=0]

        """
        return _metamodel.LinearModelTest_LinearModelDurbinWatson(*args)

    @staticmethod
    def PartialRegression(firstSample, secondSample, selection, level=0.05):
        r"""
        Test whether two discrete samples are independent.

        **Available usages**:

            LinearModelTest.PartialRegression(*firstSample, secondSample, selection*)

            LinearModelTest.PartialRegression(*firstSample, secondSample, selection, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample, of dimension :math:`n \geq 1`.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        selection : sequence of int, maximum integer value :math:`< n`
            List of indices selecting which subsets of the first sample will successively
            be tested with the second sample through the regression test.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResults : Collection of :class:`~openturns.TestResult`
            Results for each component of the linear model including intercept.

        See Also
        --------
        LinearModelTest_FullRegression, LinearModelTest_LinearModelFisher

        Notes
        -----
        The Partial Regression Test is used to assess the linearity between a subset of
        components of *firstSample* and *secondSample*.
        The parameter *selection* enables to select specific subsets of the
        *firstSample* to be tested.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> dim = 3
        >>> distCol = [ot.Normal()] * dim
        >>> S = ot.CorrelationMatrix(dim)
        >>> S[0, dim - 1] = 0.99
        >>> copula = ot.NormalCopula(S)
        >>> distribution = ot.ComposedDistribution(distCol, copula)
        >>> sample = distribution.getSample(30)
        >>> firstSample = sample[:, :2]
        >>> secondSample = sample[:, 2]
        >>> selection = [1]
        >>> test_result = ot.LinearModelTest.PartialRegression(firstSample, secondSample, selection)
        >>> print(test_result[1])
        class=TestResult name=Unnamed type=Regression binaryQualityMeasure=true p-value threshold=0.05 p-value=0.579638 statistic=-0.560438 description=[]
        """
        return _metamodel.LinearModelTest_PartialRegression(firstSample, secondSample, selection, level)

    @staticmethod
    def FullRegression(firstSample, secondSample, level=0.05):
        r"""
        Test whether two discrete samples are not linear.

        **Available usages**:

            LinearModelTest.FullRegression(*firstSample, secondSample*)

            LinearModelTest.FullRegression(*firstSample, secondSample, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample, of dimension :math:`n \geq 1`.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResults : Collection of :class:`~openturns.TestResult`
            Results for each component of the linear model including intercept.

        See Also
        --------
        LinearModelTest_PartialRegression, LinearModelTest_LinearModelFisher

        Notes
        -----
        The Full Regression Test is used to check the quality of the linear regression
        model between two samples: *firstSample* of dimension *n* and *secondSample* of
        dimension 1. If *firstSample[i]* is the sample extracted from
        *firstSample* (:math:`i^{th}` coordinate of each point of the sample),
        FullRegression performs the linear regression test on all
        *firstSample[i]* and *secondSample*. The linear regression test tests if the
        linear regression model between two scalar samples is not significant.
        It is based on the deviation analysis of the regression.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> dim = 3
        >>> distCol = [ot.Normal()] * dim
        >>> S = ot.CorrelationMatrix(dim)
        >>> S[0, dim - 1] = 0.99
        >>> copula = ot.NormalCopula(S)
        >>> distribution = ot.ComposedDistribution(distCol, copula)
        >>> sample = distribution.getSample(30)
        >>> firstSample = sample[:, :2]
        >>> secondSample = sample[:, 2]
        >>> test_result = ot.LinearModelTest.FullRegression(firstSample, secondSample)
        >>> print(test_result)
        [class=TestResult name=Unnamed type=Regression binaryQualityMeasure=true p-value threshold=0.05 p-value=0.605 statistic=-0.52335 description=[],class=TestResult name=Unnamed type=Regression binaryQualityMeasure=false p-value threshold=0.05 p-value=9.70282e-27 statistic=44.256 description=[],class=TestResult name=Unnamed type=Regression binaryQualityMeasure=true p-value threshold=0.05 p-value=0.11352 statistic=1.63564 description=[]]
        """
        return _metamodel.LinearModelTest_FullRegression(firstSample, secondSample, level)

    __swig_destroy__ = _metamodel.delete_LinearModelTest


_metamodel.LinearModelTest_swigregister(LinearModelTest)

def LinearModelTest_LinearModelFisher(*args):
    r"""
    Test the nullity of the linear regression model coefficients.

    **Available usages**:

        LinearModelTest.LinearModelFisher(*firstSample, secondSample*)

        LinearModelTest.LinearModelFisher(*firstSample, secondSample, level*)

        LinearModelTest.LinearModelFisher(*firstSample, secondSample, linearModelResult*)

        LinearModelTest.LinearModelFisher(*firstSample, secondSample, linearModelResult, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample, of dimension 1.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    linearModelResult : :class:`~openturns.LinearModelResult`
        A linear model. If not provided, it is built using the given samples.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    LinearModelTest_LinearModelResidualMean

    Notes
    -----
    The LinearModelTest class is used through its static methods in order to evaluate
    the quality of the linear regression model between two samples.
    The linear regression model between the
    scalar variable :math:`Y` and the :math:`n`-dimensional one
    :math:`\vect{X} = (X_i)_{i \leq n}` is as follows:

    .. math::

        \tilde{Y} = a_0 + \sum_{i=1}^n a_i X_i + \epsilon

    where :math:`\epsilon` is the residual, supposed to follow the standard Normal
    distribution.

    The LinearModelFisher test checks the nullity of the regression linear model
    coefficients (Fisher distribution is used).

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> func = ot.SymbolicFunction('x', '2 * x + 1')
    >>> firstSample = sample
    >>> secondSample = func(sample) + ot.Normal().getSample(30)
    >>> test_result = ot.LinearModelTest.LinearModelFisher(firstSample, secondSample)
    >>> print(test_result.getPValue())
    5.1...e-12

    """
    return _metamodel.LinearModelTest_LinearModelFisher(*args)


def LinearModelTest_LinearModelResidualMean(*args):
    r"""
    Test zero mean value of the residual of the linear regression model.

    **Available usages**:

        LinearModelTest.LinearModelResidualMean(*firstSample, secondSample*)

        LinearModelTest.LinearModelResidualMean(*firstSample, secondSample, level*)

        LinearModelTest.LinearModelResidualMean(*firstSample, secondSample, linearModelResult*)

        LinearModelTest.LinearModelResidualMean(*firstSample, secondSample, linearModelResult, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample, of dimension 1.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    linearModelResult : :class:`~openturns.LinearModelResult`
        A linear model. If not provided, it is built using the given samples.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    LinearModelTest_LinearModelFisher, LinearModelTest_LinearModelHarrisonMcCabe

    Notes
    -----
    The LinearModelTest class is used through its static methods in order to evaluate
    the quality of the linear regression model between two samples.
    The linear regression model between the
    scalar variable :math:`Y` and the :math:`n`-dimensional one
    :math:`\vect{X} = (X_i)_{i \leq n}` is as follows:

    .. math::

        \tilde{Y} = a_0 + \sum_{i=1}^n a_i X_i + \epsilon

    where :math:`\epsilon` is the residual, supposed to follow the standard Normal
    distribution.

    The LinearModelResidualMean Test checks, under the hypothesis of a gaussian
    sample, if the mean of the residual is equal to zero. It is based on the Student
    test (equality of mean for two gaussian samples).

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> func = ot.SymbolicFunction('x', '2 * x + 1')
    >>> firstSample = sample
    >>> secondSample = func(sample) + ot.Normal().getSample(30)
    >>> test_result = ot.LinearModelTest.LinearModelResidualMean(firstSample, secondSample)

    """
    return _metamodel.LinearModelTest_LinearModelResidualMean(*args)


def LinearModelTest_LinearModelHarrisonMcCabe(*args):
    r"""
    Test the homoskedasticity of the linear regression model residuals.

    **Available usages**:

        LinearModelTest.LinearModelHarrisonMcCabe(*firstSample, secondSample*)

        LinearModelTest.LinearModelHarrisonMcCabe(*firstSample, secondSample, linearModelResult*)

        LinearModelTest.LinearModelHarrisonMcCabe(*firstSample, secondSample, level, breakPoint, simulationSize*)

        LinearModelTest.LinearModelHarrisonMcCabe(*firstSample, secondSample, linearModelResult, level, breakPoint, simulationSize*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample, of dimension 1.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    linearModelResult : :class:`~openturns.LinearModelResult`
        A linear model. If not provided, it is built using the given samples.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.
    breakPoint : positive float :math:`< 1`
        Percentage of data to be taken as breakPoint in the variances. It must be
        :math:`< 1`, equal to 0.5 by default.
    simulationSize : positive int
        Size of the sample used to compute the p-value. Default is 1000.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    LinearModelTest_LinearModelBreuschPagan, LinearModelTest_LinearModelResidualMean,
    LinearModelTest_LinearModelDurbinWatson

    Notes
    -----
    The LinearModelTest class is used through its static methods in order to evaluate
    the quality of the linear regression model between two samples.
    The linear regression model between the
    scalar variable :math:`Y` and the :math:`n`-dimensional one
    :math:`\vect{X} = (X_i)_{i \leq n}` is as follows:

    .. math::

        \tilde{Y} = a_0 + \sum_{i=1}^n a_i X_i + \epsilon

    where :math:`\epsilon` is the residual.

    The Harrison-McCabe test checks the heteroskedasticity of the residuals. The
    breakpoint in the variances is set by default to the half of the sample. The
    p-value is estimed using simulation. If the binary quality measure is false, then
    the homoskedasticity hypothesis can be rejected with respect to the given level.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> func = ot.SymbolicFunction('x', '2 * x + 1')
    >>> firstSample = sample
    >>> secondSample = func(sample) + ot.Normal().getSample(30)
    >>> test_result = ot.LinearModelTest.LinearModelHarrisonMcCabe(firstSample, secondSample)
    >>> print(test_result)
    class=TestResult name=Unnamed type=HarrisonMcCabe binaryQualityMeasure=true p-value threshold=0.05 p-value=0.142 statistic=0.373225 description=[]

    """
    return _metamodel.LinearModelTest_LinearModelHarrisonMcCabe(*args)


def LinearModelTest_LinearModelBreuschPagan(*args):
    r"""
    Test the homoskedasticity of the linear regression model residuals.

    **Available usages**:

        LinearModelTest.LinearModelBreuschPagan(*firstSample, secondSample*)

        LinearModelTest.LinearModelBreuschPagan(*firstSample, secondSample, linearModelResult*)

        LinearModelTest.LinearModelBreuschPagan(*firstSample, secondSample, level*)

        LinearModelTest.LinearModelBreuschPagan(*firstSample, secondSample, linearModelResult, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample, of dimension 1.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    linearModelResult : :class:`~openturns.LinearModelResult`
        A linear model. If not provided, it is built using the given samples.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    LinearModelTest_LinearModelHarrisonMcCabe, LinearModelTest_LinearModelResidualMean,
    LinearModelTest_LinearModelDurbinWatson

    Notes
    -----
    The LinearModelTest class is used through its static methods in order to evaluate
    the quality of the linear regression model between two samples.
    The linear regression model between the
    scalar variable :math:`Y` and the :math:`n`-dimensional one
    :math:`\vect{X} = (X_i)_{i \leq n}` is as follows:

    .. math::

        \tilde{Y} = a_0 + \sum_{i=1}^n a_i X_i + \epsilon

    where :math:`\epsilon` is the residual.

    The Breusch-Pagan test checks the heteroskedasticity of the residuals. A linear
    regression model is fitted on the squared residuals. The statistic is computed
    using the Studendized version with the chi-squared distribution. If the binary
    quality measure is false, then the homoskedasticity hypothesis can be rejected
    with respect to the given level.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> func = ot.SymbolicFunction('x', '2 * x + 1')
    >>> firstSample = sample
    >>> secondSample = func(sample) + ot.Normal().getSample(30)
    >>> test_result = ot.LinearModelTest.LinearModelBreuschPagan(firstSample, secondSample)
    >>> print(test_result)
    class=TestResult name=Unnamed type=BreuschPagan binaryQualityMeasure=true p-value threshold=0.05 p-value=0.700772 statistic=0.14767 description=[]

    """
    return _metamodel.LinearModelTest_LinearModelBreuschPagan(*args)


def LinearModelTest_LinearModelDurbinWatson(*args):
    r"""
    Test the autocorrelation of the linear regression model residuals.

    **Available usages**:

        LinearModelTest.LinearModelDurbinWatson(*firstSample, secondSample*)

        LinearModelTest.LinearModelDurbinWatson(*firstSample, secondSample, hypothesis, level*)

        LinearModelTest.LinearModelDurbinWatson(*firstSample, secondSample, linearModelResult*)

        LinearModelTest.LinearModelDurbinWatson(*firstSample, secondSample, linearModelResult, hypothesis, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    linearModelResult : :class:`~openturns.LinearModelResult`
        A linear model. If not provided, it is built using the given samples.
    hypothesis : str
        Hypothesis H0 for the residuals. It can be : 'Equal' to 0, 'Less' than 0 or
        'Greater' than 0. Default is set to 'Equal' to 0.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    LinearModelTest_LinearModelBreuschPagan, LinearModelTest_LinearModelHarrisonMcCabe, LinearModelTest_LinearModelResidualMean

    Notes
    -----
    The LinearModelTest class is used through its static methods in order to evaluate
    the quality of the linear regression model between two samples.
    The linear regression model between the
    scalar variable :math:`Y` and the :math:`n`-dimensional one
    :math:`\vect{X} = (X_i)_{i \leq n}` is as follows:

    .. math::

        \tilde{Y} = a_0 + \sum_{i=1}^n a_i X_i + \epsilon

    where :math:`\epsilon` is the residual.

    The Durbin-Watson test checks the autocorrelation of the residuals. It is possible
    to test is the autocorrelation is equal to 0, and less or greater than 0. The
    p-value is computed using a normal approximation with mean and variance of the
    Durbin-Watson test statistic. If the binary quality measure is false, then the
    given autocorrelation hypothesis can be rejected with respect to the given level.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> func = ot.SymbolicFunction('x', '2 * x + 1')
    >>> firstSample = sample
    >>> secondSample = func(sample) + ot.Normal().getSample(30)
    >>> test_result = ot.LinearModelTest.LinearModelDurbinWatson(firstSample, secondSample)
    >>> print(test_result)
    class=TestResult name=Unnamed type=DurbinWatson binaryQualityMeasure=true p-value threshold=0.05 p-value=0.653603 statistic=0.448763 description=[H0: auto.cor=0]

    """
    return _metamodel.LinearModelTest_LinearModelDurbinWatson(*args)


def LinearModelTest_PartialRegression(firstSample, secondSample, selection, level=0.05):
    r"""
    Test whether two discrete samples are independent.

    **Available usages**:

        LinearModelTest.PartialRegression(*firstSample, secondSample, selection*)

        LinearModelTest.PartialRegression(*firstSample, secondSample, selection, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample, of dimension :math:`n \geq 1`.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    selection : sequence of int, maximum integer value :math:`< n`
        List of indices selecting which subsets of the first sample will successively
        be tested with the second sample through the regression test.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResults : Collection of :class:`~openturns.TestResult`
        Results for each component of the linear model including intercept.

    See Also
    --------
    LinearModelTest_FullRegression, LinearModelTest_LinearModelFisher

    Notes
    -----
    The Partial Regression Test is used to assess the linearity between a subset of
    components of *firstSample* and *secondSample*.
    The parameter *selection* enables to select specific subsets of the
    *firstSample* to be tested.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> dim = 3
    >>> distCol = [ot.Normal()] * dim
    >>> S = ot.CorrelationMatrix(dim)
    >>> S[0, dim - 1] = 0.99
    >>> copula = ot.NormalCopula(S)
    >>> distribution = ot.ComposedDistribution(distCol, copula)
    >>> sample = distribution.getSample(30)
    >>> firstSample = sample[:, :2]
    >>> secondSample = sample[:, 2]
    >>> selection = [1]
    >>> test_result = ot.LinearModelTest.PartialRegression(firstSample, secondSample, selection)
    >>> print(test_result[1])
    class=TestResult name=Unnamed type=Regression binaryQualityMeasure=true p-value threshold=0.05 p-value=0.579638 statistic=-0.560438 description=[]
    """
    return _metamodel.LinearModelTest_PartialRegression(firstSample, secondSample, selection, level)


def LinearModelTest_FullRegression(firstSample, secondSample, level=0.05):
    r"""
    Test whether two discrete samples are not linear.

    **Available usages**:

        LinearModelTest.FullRegression(*firstSample, secondSample*)

        LinearModelTest.FullRegression(*firstSample, secondSample, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample, of dimension :math:`n \geq 1`.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResults : Collection of :class:`~openturns.TestResult`
        Results for each component of the linear model including intercept.

    See Also
    --------
    LinearModelTest_PartialRegression, LinearModelTest_LinearModelFisher

    Notes
    -----
    The Full Regression Test is used to check the quality of the linear regression
    model between two samples: *firstSample* of dimension *n* and *secondSample* of
    dimension 1. If *firstSample[i]* is the sample extracted from
    *firstSample* (:math:`i^{th}` coordinate of each point of the sample),
    FullRegression performs the linear regression test on all
    *firstSample[i]* and *secondSample*. The linear regression test tests if the
    linear regression model between two scalar samples is not significant.
    It is based on the deviation analysis of the regression.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> dim = 3
    >>> distCol = [ot.Normal()] * dim
    >>> S = ot.CorrelationMatrix(dim)
    >>> S[0, dim - 1] = 0.99
    >>> copula = ot.NormalCopula(S)
    >>> distribution = ot.ComposedDistribution(distCol, copula)
    >>> sample = distribution.getSample(30)
    >>> firstSample = sample[:, :2]
    >>> secondSample = sample[:, 2]
    >>> test_result = ot.LinearModelTest.FullRegression(firstSample, secondSample)
    >>> print(test_result)
    [class=TestResult name=Unnamed type=Regression binaryQualityMeasure=true p-value threshold=0.05 p-value=0.605 statistic=-0.52335 description=[],class=TestResult name=Unnamed type=Regression binaryQualityMeasure=false p-value threshold=0.05 p-value=9.70282e-27 statistic=44.256 description=[],class=TestResult name=Unnamed type=Regression binaryQualityMeasure=true p-value threshold=0.05 p-value=0.11352 statistic=1.63564 description=[]]
    """
    return _metamodel.LinearModelTest_FullRegression(firstSample, secondSample, level)


class VisualTest(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr

    @staticmethod
    def DrawQQplot(*args):
        r"""
        Draw a QQ-plot.

        Refer to :ref:`qqplot_graph`.

        Available usages:
            VisualTest.DrawQQplot(*sample1, sample2, n_points*)

            VisualTest.DrawQQplot(*sample1, distribution*);

        Parameters
        ----------
        sample1, sample2 : 2-d sequences of float
            Tested samples.
        ditribution : :class:`~openturns.Distribution`
            Tested model.
        n_points : int, optional
            The number of points that is used for interpolating the empirical CDF of
            the two samples (with possibly different sizes).

            It will default to *DistributionImplementation-DefaultPointNumber* from
            the :class:`~openturns.ResourceMap`.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            The graph object

        Notes
        -----
        The QQ-plot is a visual fitting test for univariate distributions. It
        opposes the sample quantiles to those of the tested quantity (either a
        distribution or another sample) by plotting the following points cloud:

        .. math::

            \left(x^{(i)},
                  \theta\left(\widehat{F}\left(x^{(i)}\right)\right)
            \right), \quad i = 1, \ldots, m

        where :math:`\widehat{F}` denotes the empirical CDF of the (first) tested
        sample and :math:`\theta` denotes either the quantile function of the tested
        distribution or the empirical quantile function of the second tested sample.

        If the given sample fits to the tested distribution or sample, then the points
        should be close to be aligned (up to the uncertainty associated with the
        estimation of the empirical probabilities) with the **first bissector**  whose
        equation reads:

        .. math::

            y = x, \quad x \in \Rset

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View

        Generate a random sample from a Normal distribution:

        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.WeibullMin(2.0, 0.5)
        >>> sample = distribution.getSample(30)
        >>> sample.setDescription(['Sample'])

        Draw a QQ-plot against a given (inferred) distribution:

        >>> tested_distribution = ot.WeibullMinFactory().build(sample)
        >>> QQ_plot = ot.VisualTest.DrawQQplot(sample, tested_distribution)
        >>> View(QQ_plot).show()

        Draw a two-sample QQ-plot:

        >>> another_sample = distribution.getSample(50)
        >>> another_sample.setDescription(['Another sample'])
        >>> QQ_plot = ot.VisualTest.DrawQQplot(sample, another_sample)
        >>> View(QQ_plot).show()
        """
        return _metamodel.VisualTest_DrawQQplot(*args)

    @staticmethod
    def DrawCDFplot(*args):
        r"""
        Draw a CDF-plot.

        Refer to :ref:`qqplot_graph`.

        Available usages:
            VisualTest.DrawCDFplot(*sample1, sample2*)

            VisualTest.DrawCDFplot(*sample1, distribution*);

        Parameters
        ----------
        sample1, sample2 : 2-d sequences of float
            Tested samples.
        ditribution : :class:`~openturns.Distribution`
            Tested model.

        Returns
        -------
        graph : class:`~openturns.Graph`
            The graph object

        Notes
        -----
        The CDF-plot is a visual fitting test for univariate distributions. It
        opposes the normalized sample ranks to those of the tested quantity (either a
        distribution or another sample) by plotting the following points cloud:

        .. math::

            \left(\dfrac{i+1/2}{m},
                  F(x^{(i)})
            \right), \quad i = 1, \ldots, m

        where :math:`F` denotes either the CDF function of the tested
        distribution or the empirical CDF of the second tested sample.

        If the given sample fits to the tested distribution or sample, then the points
        should be close to be aligned (up to the uncertainty associated with the
        estimation of the empirical probabilities) with the **first bissector**  whose
        equation reads:

        .. math::

            y = x, \quad x \in [0,1]

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View

        Generate a random sample from a Normal distribution:

        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.WeibullMin(2.0, 0.5)
        >>> sample = distribution.getSample(30)
        >>> sample.setDescription(['Sample'])

        Draw a CDF-plot against a given (inferred) distribution:

        >>> tested_distribution = ot.WeibullMinFactory().build(sample)
        >>> CDF_plot = ot.VisualTest.DrawCDFplot(sample, tested_distribution)
        >>> View(CDF_plot).show()

        Draw a two-sample CDF-plot:

        >>> another_sample = distribution.getSample(50)
        >>> another_sample.setDescription(['Another sample'])
        >>> CDF_plot = ot.VisualTest.DrawCDFplot(sample, another_sample)
        >>> View(CDF_plot).show()
        """
        return _metamodel.VisualTest_DrawCDFplot(*args)

    @staticmethod
    def DrawHenryLine(*args):
        r"""
        Draw an Henry plot.

        Refer to :ref:`graphical_fitting_test`.

        Parameters
        ----------
        sample : 2-d sequence of float
            Tested (univariate) sample.
        normal_distribution : :class:`~openturns.Normal`, optional
            Tested (univariate) normal distribution.

            If not given, this will build a :class:`~openturns.Normal` distribution
            from the given sample using the :class:`~openturns.NormalFactory`.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            The graph object

        Notes
        -----
        The Henry plot is a visual fitting test for the normal distribution. It
        opposes the sample quantiles to those of the standard normal distribution
        (the one with zero mean and unit variance) by plotting the following points
        could:

        .. math::

            \left(x^{(i)},
                  \Phi^{-1}\left(\widehat{F}\left(x^{(i)}\right)\right)
            \right), \quad i = 1, \ldots, m

        where :math:`\widehat{F}` denotes the empirical CDF of the sample and
        :math:`\Phi^{-1}` denotes the quantile function of the standard normal
        distribution.

        If the given sample fits to the tested normal distribution (with mean
        :math:`\mu` and standard deviation :math:`\sigma`), then the points should be
        close to be aligned (up to the uncertainty associated with the estimation
        of the empirical probabilities) on the **Henry line** whose equation reads:

        .. math::

            y = \frac{x - \mu}{\sigma}, \quad x \in \Rset

        The Henry plot is a special case of the more general QQ-plot.

        See Also
        --------
        VisualTest_DrawQQplot, FittingTest_Kolmogorov

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View

        Generate a random sample from a Normal distribution:

        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal(2.0, 0.5)
        >>> sample = distribution.getSample(30)

        Draw an Henry plot against a given (wrong) Normal distribution:

        >>> henry_graph = ot.VisualTest.DrawHenryLine(sample, distribution)
        >>> henry_graph.setTitle('Henry plot against given %s' % ot.Normal(3.0, 1.0))
        >>> View(henry_graph).show()

        Draw an Henry plot against an inferred Normal distribution:

        >>> henry_graph = ot.VisualTest.DrawHenryLine(sample)
        >>> henry_graph.setTitle('Henry plot against inferred Normal distribution')
        >>> View(henry_graph).show()
        """
        return _metamodel.VisualTest_DrawHenryLine(*args)

    @staticmethod
    def DrawLinearModel(sample1, sample2, linearModelResult):
        """
        Draw a linear model plot.

        Parameters
        ----------
        sample1, sample2 : 2-d sequence of float
            Samples to draw.
        linearModelResult : :class:`~openturns.LinearModelResult`
            Linear model to plot.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            The graph object

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> ot.RandomGenerator.SetSeed(0)
        >>> dimension = 2
        >>> R = ot.CorrelationMatrix(dimension)
        >>> R[0, 1] = 0.8
        >>> distribution = ot.Normal([3.0] * dimension, [2.0]* dimension, R)
        >>> size = 100
        >>> sample2D = distribution.getSample(size)
        >>> firstSample = ot.Sample(size, 1)
        >>> secondSample = ot.Sample(size, 1)
        >>> for i in range(size):
        ...     firstSample[i] = ot.Point(1, sample2D[i, 0])
        ...     secondSample[i] = ot.Point(1, sample2D[i, 1])
        >>> lmtest = ot.LinearModelAlgorithm(firstSample, secondSample).getResult()
        >>> drawLinearModelVTest = ot.VisualTest.DrawLinearModel(firstSample, secondSample, lmtest)
        >>> View(drawLinearModelVTest).show()
        """
        return _metamodel.VisualTest_DrawLinearModel(sample1, sample2, linearModelResult)

    @staticmethod
    def DrawLinearModelResidual(sample1, sample2, linearModelResult):
        """
        Draw a linear model residual plot.

        Parameters
        ----------
        sample1, sample2 : 2-d sequence of float
            Samples to draw.
        linearModelResult : :class:`~openturns.LinearModelResult`
            Linear model to plot.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            The graph object

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> ot.RandomGenerator.SetSeed(0)
        >>> dimension = 2
        >>> R = ot.CorrelationMatrix(dimension)
        >>> R[0, 1] = 0.8
        >>> distribution = ot.Normal([3.0] * dimension, [2.0]* dimension, R)
        >>> size = 100
        >>> sample2D = distribution.getSample(size)
        >>> firstSample = ot.Sample(size, 1)
        >>> secondSample = ot.Sample(size, 1)
        >>> for i in range(size):
        ...     firstSample[i] = ot.Point(1, sample2D[i, 0])
        ...     secondSample[i] = ot.Point(1, sample2D[i, 1])
        >>> lmtest = ot.LinearModelAlgorithm(firstSample, secondSample).getResult()
        >>> drawLinearModelVTest = ot.VisualTest.DrawLinearModelResidual(firstSample, secondSample, lmtest)
        >>> View(drawLinearModelVTest).show()
        """
        return _metamodel.VisualTest_DrawLinearModelResidual(sample1, sample2, linearModelResult)

    @staticmethod
    def DrawCobWeb(inputSample, outputSample, minValue, maxValue, color, quantileScale=True):
        r"""
        Draw a Cobweb plot.

        Available usages:
            VisualTest.DrawCobWeb(*inputSample, outputSample, min, max, color, quantileScale=True*)

        Parameters
        ----------
        inputSample : 2-d sequence of float of dimension :math:`n`
            Input sample :math:`\vect{X}`.
        outputSample : 2-d sequence of float of dimension :math:`1`
            Output sample :math:`Y`.
        Ymin, Ymax : float such that *Ymax > Ymin*
            Values to select lines which will colore in *color*. Must be in
            :math:`[0,1]` if *quantileScale=True*.
        color : str
            Color of the specified curves.
        quantileScale : bool
            Flag indicating the scale of the *Ymin* and *Ymax*. If
            *quantileScale=True*, they are expressed in the rank based scale;
            otherwise, they are expressed in the :math:`Y`-values scale.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            The graph object

        Notes
        -----
        Let's suppose a model :math:`f: \Rset^n \mapsto \Rset`, where
        :math:`f(\vect{X})=Y`.
        The Cobweb graph enables to visualize all the combinations of the input
        variables which lead to a specific range of the output variable.

        Each column represents one component :math:`X_i` of the input vector
        :math:`\vect{X}`. The last column represents the scalar output variable
        :math:`Y`.

        For each point :math:`\vect{X}^j` of *inputSample*, each component :math:`X_i^j`
        is noted on its respective axe and the last mark is the one which corresponds
        to the associated :math:`Y^j`. A line joins all the marks. Thus, each point of
        the sample corresponds to a particular line on the graph.

        The scale of the axes are quantile based : each axe runs between 0 and 1 and
        each value is represented by its quantile with respect to its marginal
        empirical distribution.

        It is interesting to select, among those lines, the ones which correspond to a
        specific range of the output variable. These particular lines selected are
        colored differently in *color*. This specific range is defined with *Ymin* and
        *Ymax* in the quantile based scale of :math:`Y` or in its specific scale. In
        that second case, the range is automatically converted into a quantile based
        scale range.

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View

        Generate a random sample from a Normal distribution:

        >>> ot.RandomGenerator.SetSeed(0)
        >>> inputSample = ot.Normal(2).getSample(15)
        >>> inputSample.setDescription(['X0', 'X1'])
        >>> formula = ['cos(X0)+cos(2*X1)']
        >>> model = ot.SymbolicFunction(['X0', 'X1'], formula)
        >>> outputSample = model(inputSample)

        Draw a Cobweb plot:

        >>> cobweb = ot.VisualTest.DrawCobWeb(inputSample, outputSample, 1.0, 2.0, 'red', False)
        >>> View(cobweb).show()
        """
        return _metamodel.VisualTest_DrawCobWeb(inputSample, outputSample, minValue, maxValue, color, quantileScale)

    @staticmethod
    def DrawKendallPlot(*args):
        """
        Draw kendall plot.

        Refer to :ref:`graphical_fitting_test`.

        Available usages:
            VisualTest.DrawKendallPlot(*sample, distribution*)

            VisualTest.DrawKendallPlot(*sample, sample2*)

        Parameters
        ----------
        sample, sample2 : 2-d sequence of float
            Samples to draw.
        distribution : :class:`~openturns.Distribution`
            Distribution used to plot the second cloud

        Returns
        -------
        graph : :class:`~openturns.Graph`
            The graph object

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> ot.RandomGenerator.SetSeed(0)
        >>> size = 100
        >>> copula1 = ot.FrankCopula(1.5)
        >>> copula2 = ot.GumbelCopula(4.5)
        >>> sample1 = copula1.getSample(size)
        >>> sample1.setName('data 1')
        >>> sample2 = copula2.getSample(size)
        >>> sample2.setName('data 2')
        >>> kendallPlot1 = ot.VisualTest.DrawKendallPlot(sample1, copula2)
        >>> View(kendallPlot1).show()
        """
        return _metamodel.VisualTest_DrawKendallPlot(*args)

    __swig_destroy__ = _metamodel.delete_VisualTest


_metamodel.VisualTest_swigregister(VisualTest)

def VisualTest_DrawQQplot(*args):
    r"""
    Draw a QQ-plot.

    Refer to :ref:`qqplot_graph`.

    Available usages:
        VisualTest.DrawQQplot(*sample1, sample2, n_points*)

        VisualTest.DrawQQplot(*sample1, distribution*);

    Parameters
    ----------
    sample1, sample2 : 2-d sequences of float
        Tested samples.
    ditribution : :class:`~openturns.Distribution`
        Tested model.
    n_points : int, optional
        The number of points that is used for interpolating the empirical CDF of
        the two samples (with possibly different sizes).

        It will default to *DistributionImplementation-DefaultPointNumber* from
        the :class:`~openturns.ResourceMap`.

    Returns
    -------
    graph : :class:`~openturns.Graph`
        The graph object

    Notes
    -----
    The QQ-plot is a visual fitting test for univariate distributions. It
    opposes the sample quantiles to those of the tested quantity (either a
    distribution or another sample) by plotting the following points cloud:

    .. math::

        \left(x^{(i)},
              \theta\left(\widehat{F}\left(x^{(i)}\right)\right)
        \right), \quad i = 1, \ldots, m

    where :math:`\widehat{F}` denotes the empirical CDF of the (first) tested
    sample and :math:`\theta` denotes either the quantile function of the tested
    distribution or the empirical quantile function of the second tested sample.

    If the given sample fits to the tested distribution or sample, then the points
    should be close to be aligned (up to the uncertainty associated with the
    estimation of the empirical probabilities) with the **first bissector**  whose
    equation reads:

    .. math::

        y = x, \quad x \in \Rset

    Examples
    --------
    >>> import openturns as ot
    >>> from openturns.viewer import View

    Generate a random sample from a Normal distribution:

    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.WeibullMin(2.0, 0.5)
    >>> sample = distribution.getSample(30)
    >>> sample.setDescription(['Sample'])

    Draw a QQ-plot against a given (inferred) distribution:

    >>> tested_distribution = ot.WeibullMinFactory().build(sample)
    >>> QQ_plot = ot.VisualTest.DrawQQplot(sample, tested_distribution)
    >>> View(QQ_plot).show()

    Draw a two-sample QQ-plot:

    >>> another_sample = distribution.getSample(50)
    >>> another_sample.setDescription(['Another sample'])
    >>> QQ_plot = ot.VisualTest.DrawQQplot(sample, another_sample)
    >>> View(QQ_plot).show()
    """
    return _metamodel.VisualTest_DrawQQplot(*args)


def VisualTest_DrawCDFplot(*args):
    r"""
    Draw a CDF-plot.

    Refer to :ref:`qqplot_graph`.

    Available usages:
        VisualTest.DrawCDFplot(*sample1, sample2*)

        VisualTest.DrawCDFplot(*sample1, distribution*);

    Parameters
    ----------
    sample1, sample2 : 2-d sequences of float
        Tested samples.
    ditribution : :class:`~openturns.Distribution`
        Tested model.

    Returns
    -------
    graph : class:`~openturns.Graph`
        The graph object

    Notes
    -----
    The CDF-plot is a visual fitting test for univariate distributions. It
    opposes the normalized sample ranks to those of the tested quantity (either a
    distribution or another sample) by plotting the following points cloud:

    .. math::

        \left(\dfrac{i+1/2}{m},
              F(x^{(i)})
        \right), \quad i = 1, \ldots, m

    where :math:`F` denotes either the CDF function of the tested
    distribution or the empirical CDF of the second tested sample.

    If the given sample fits to the tested distribution or sample, then the points
    should be close to be aligned (up to the uncertainty associated with the
    estimation of the empirical probabilities) with the **first bissector**  whose
    equation reads:

    .. math::

        y = x, \quad x \in [0,1]

    Examples
    --------
    >>> import openturns as ot
    >>> from openturns.viewer import View

    Generate a random sample from a Normal distribution:

    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.WeibullMin(2.0, 0.5)
    >>> sample = distribution.getSample(30)
    >>> sample.setDescription(['Sample'])

    Draw a CDF-plot against a given (inferred) distribution:

    >>> tested_distribution = ot.WeibullMinFactory().build(sample)
    >>> CDF_plot = ot.VisualTest.DrawCDFplot(sample, tested_distribution)
    >>> View(CDF_plot).show()

    Draw a two-sample CDF-plot:

    >>> another_sample = distribution.getSample(50)
    >>> another_sample.setDescription(['Another sample'])
    >>> CDF_plot = ot.VisualTest.DrawCDFplot(sample, another_sample)
    >>> View(CDF_plot).show()
    """
    return _metamodel.VisualTest_DrawCDFplot(*args)


def VisualTest_DrawHenryLine(*args):
    r"""
    Draw an Henry plot.

    Refer to :ref:`graphical_fitting_test`.

    Parameters
    ----------
    sample : 2-d sequence of float
        Tested (univariate) sample.
    normal_distribution : :class:`~openturns.Normal`, optional
        Tested (univariate) normal distribution.

        If not given, this will build a :class:`~openturns.Normal` distribution
        from the given sample using the :class:`~openturns.NormalFactory`.

    Returns
    -------
    graph : :class:`~openturns.Graph`
        The graph object

    Notes
    -----
    The Henry plot is a visual fitting test for the normal distribution. It
    opposes the sample quantiles to those of the standard normal distribution
    (the one with zero mean and unit variance) by plotting the following points
    could:

    .. math::

        \left(x^{(i)},
              \Phi^{-1}\left(\widehat{F}\left(x^{(i)}\right)\right)
        \right), \quad i = 1, \ldots, m

    where :math:`\widehat{F}` denotes the empirical CDF of the sample and
    :math:`\Phi^{-1}` denotes the quantile function of the standard normal
    distribution.

    If the given sample fits to the tested normal distribution (with mean
    :math:`\mu` and standard deviation :math:`\sigma`), then the points should be
    close to be aligned (up to the uncertainty associated with the estimation
    of the empirical probabilities) on the **Henry line** whose equation reads:

    .. math::

        y = \frac{x - \mu}{\sigma}, \quad x \in \Rset

    The Henry plot is a special case of the more general QQ-plot.

    See Also
    --------
    VisualTest_DrawQQplot, FittingTest_Kolmogorov

    Examples
    --------
    >>> import openturns as ot
    >>> from openturns.viewer import View

    Generate a random sample from a Normal distribution:

    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal(2.0, 0.5)
    >>> sample = distribution.getSample(30)

    Draw an Henry plot against a given (wrong) Normal distribution:

    >>> henry_graph = ot.VisualTest.DrawHenryLine(sample, distribution)
    >>> henry_graph.setTitle('Henry plot against given %s' % ot.Normal(3.0, 1.0))
    >>> View(henry_graph).show()

    Draw an Henry plot against an inferred Normal distribution:

    >>> henry_graph = ot.VisualTest.DrawHenryLine(sample)
    >>> henry_graph.setTitle('Henry plot against inferred Normal distribution')
    >>> View(henry_graph).show()
    """
    return _metamodel.VisualTest_DrawHenryLine(*args)


def VisualTest_DrawLinearModel(sample1, sample2, linearModelResult):
    """
    Draw a linear model plot.

    Parameters
    ----------
    sample1, sample2 : 2-d sequence of float
        Samples to draw.
    linearModelResult : :class:`~openturns.LinearModelResult`
        Linear model to plot.

    Returns
    -------
    graph : :class:`~openturns.Graph`
        The graph object

    Examples
    --------
    >>> import openturns as ot
    >>> from openturns.viewer import View
    >>> ot.RandomGenerator.SetSeed(0)
    >>> dimension = 2
    >>> R = ot.CorrelationMatrix(dimension)
    >>> R[0, 1] = 0.8
    >>> distribution = ot.Normal([3.0] * dimension, [2.0]* dimension, R)
    >>> size = 100
    >>> sample2D = distribution.getSample(size)
    >>> firstSample = ot.Sample(size, 1)
    >>> secondSample = ot.Sample(size, 1)
    >>> for i in range(size):
    ...     firstSample[i] = ot.Point(1, sample2D[i, 0])
    ...     secondSample[i] = ot.Point(1, sample2D[i, 1])
    >>> lmtest = ot.LinearModelAlgorithm(firstSample, secondSample).getResult()
    >>> drawLinearModelVTest = ot.VisualTest.DrawLinearModel(firstSample, secondSample, lmtest)
    >>> View(drawLinearModelVTest).show()
    """
    return _metamodel.VisualTest_DrawLinearModel(sample1, sample2, linearModelResult)


def VisualTest_DrawLinearModelResidual(sample1, sample2, linearModelResult):
    """
    Draw a linear model residual plot.

    Parameters
    ----------
    sample1, sample2 : 2-d sequence of float
        Samples to draw.
    linearModelResult : :class:`~openturns.LinearModelResult`
        Linear model to plot.

    Returns
    -------
    graph : :class:`~openturns.Graph`
        The graph object

    Examples
    --------
    >>> import openturns as ot
    >>> from openturns.viewer import View
    >>> ot.RandomGenerator.SetSeed(0)
    >>> dimension = 2
    >>> R = ot.CorrelationMatrix(dimension)
    >>> R[0, 1] = 0.8
    >>> distribution = ot.Normal([3.0] * dimension, [2.0]* dimension, R)
    >>> size = 100
    >>> sample2D = distribution.getSample(size)
    >>> firstSample = ot.Sample(size, 1)
    >>> secondSample = ot.Sample(size, 1)
    >>> for i in range(size):
    ...     firstSample[i] = ot.Point(1, sample2D[i, 0])
    ...     secondSample[i] = ot.Point(1, sample2D[i, 1])
    >>> lmtest = ot.LinearModelAlgorithm(firstSample, secondSample).getResult()
    >>> drawLinearModelVTest = ot.VisualTest.DrawLinearModelResidual(firstSample, secondSample, lmtest)
    >>> View(drawLinearModelVTest).show()
    """
    return _metamodel.VisualTest_DrawLinearModelResidual(sample1, sample2, linearModelResult)


def VisualTest_DrawCobWeb(inputSample, outputSample, minValue, maxValue, color, quantileScale=True):
    r"""
    Draw a Cobweb plot.

    Available usages:
        VisualTest.DrawCobWeb(*inputSample, outputSample, min, max, color, quantileScale=True*)

    Parameters
    ----------
    inputSample : 2-d sequence of float of dimension :math:`n`
        Input sample :math:`\vect{X}`.
    outputSample : 2-d sequence of float of dimension :math:`1`
        Output sample :math:`Y`.
    Ymin, Ymax : float such that *Ymax > Ymin*
        Values to select lines which will colore in *color*. Must be in
        :math:`[0,1]` if *quantileScale=True*.
    color : str
        Color of the specified curves.
    quantileScale : bool
        Flag indicating the scale of the *Ymin* and *Ymax*. If
        *quantileScale=True*, they are expressed in the rank based scale;
        otherwise, they are expressed in the :math:`Y`-values scale.

    Returns
    -------
    graph : :class:`~openturns.Graph`
        The graph object

    Notes
    -----
    Let's suppose a model :math:`f: \Rset^n \mapsto \Rset`, where
    :math:`f(\vect{X})=Y`.
    The Cobweb graph enables to visualize all the combinations of the input
    variables which lead to a specific range of the output variable.

    Each column represents one component :math:`X_i` of the input vector
    :math:`\vect{X}`. The last column represents the scalar output variable
    :math:`Y`.

    For each point :math:`\vect{X}^j` of *inputSample*, each component :math:`X_i^j`
    is noted on its respective axe and the last mark is the one which corresponds
    to the associated :math:`Y^j`. A line joins all the marks. Thus, each point of
    the sample corresponds to a particular line on the graph.

    The scale of the axes are quantile based : each axe runs between 0 and 1 and
    each value is represented by its quantile with respect to its marginal
    empirical distribution.

    It is interesting to select, among those lines, the ones which correspond to a
    specific range of the output variable. These particular lines selected are
    colored differently in *color*. This specific range is defined with *Ymin* and
    *Ymax* in the quantile based scale of :math:`Y` or in its specific scale. In
    that second case, the range is automatically converted into a quantile based
    scale range.

    Examples
    --------
    >>> import openturns as ot
    >>> from openturns.viewer import View

    Generate a random sample from a Normal distribution:

    >>> ot.RandomGenerator.SetSeed(0)
    >>> inputSample = ot.Normal(2).getSample(15)
    >>> inputSample.setDescription(['X0', 'X1'])
    >>> formula = ['cos(X0)+cos(2*X1)']
    >>> model = ot.SymbolicFunction(['X0', 'X1'], formula)
    >>> outputSample = model(inputSample)

    Draw a Cobweb plot:

    >>> cobweb = ot.VisualTest.DrawCobWeb(inputSample, outputSample, 1.0, 2.0, 'red', False)
    >>> View(cobweb).show()
    """
    return _metamodel.VisualTest_DrawCobWeb(inputSample, outputSample, minValue, maxValue, color, quantileScale)


def VisualTest_DrawKendallPlot(*args):
    """
    Draw kendall plot.

    Refer to :ref:`graphical_fitting_test`.

    Available usages:
        VisualTest.DrawKendallPlot(*sample, distribution*)

        VisualTest.DrawKendallPlot(*sample, sample2*)

    Parameters
    ----------
    sample, sample2 : 2-d sequence of float
        Samples to draw.
    distribution : :class:`~openturns.Distribution`
        Distribution used to plot the second cloud

    Returns
    -------
    graph : :class:`~openturns.Graph`
        The graph object

    Examples
    --------
    >>> import openturns as ot
    >>> from openturns.viewer import View
    >>> ot.RandomGenerator.SetSeed(0)
    >>> size = 100
    >>> copula1 = ot.FrankCopula(1.5)
    >>> copula2 = ot.GumbelCopula(4.5)
    >>> sample1 = copula1.getSample(size)
    >>> sample1.setName('data 1')
    >>> sample2 = copula2.getSample(size)
    >>> sample2.setName('data 2')
    >>> kendallPlot1 = ot.VisualTest.DrawKendallPlot(sample1, copula2)
    >>> View(kendallPlot1).show()
    """
    return _metamodel.VisualTest_DrawKendallPlot(*args)


class PythonRandomVector(object):
    """
    Allow to overload RandomVector from Python.

    Parameters
    ----------
    dim : positive int
        Vector dimension.
        Default is 0.

    See also
    --------
    RandomVector

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)

    Overload RandomVector from Python:

    >>> class RVEC(ot.PythonRandomVector):
    ...    def __init__(self):
    ...        super(RVEC, self).__init__(2)
    ...        self.setDescription(['R', 'S'])
    ...
    ...    def getRealization(self):
    ...        X = [ot.RandomGenerator.Generate(), 2 + ot.RandomGenerator.Generate()]
    ...        return X
    ...
    ...    def getSample(self, size):
    ...        X = []
    ...        for i in range(size):
    ...            X.append([ot.RandomGenerator.Generate(), 2 + ot.RandomGenerator.Generate()])
    ...        return X
    ...
    ...    def getMean(self):
    ...        return [0.5, 2.5]
    ...
    ...    def getCovariance(self):
    ...        return [[0.0833333, 0.], [0., 0.0833333]]

    Use the overloaded class:

    >>> R = RVEC()
    >>> # Instance creation
    >>> myRV = ot.RandomVector(R)
    >>> # Realization
    >>> print(myRV.getRealization())
    [0.629877,2.88281]
    >>> # Sample
    >>> print(myRV.getSample(5))
    0 : [ 0.135276  2.0325    ]
    1 : [ 0.347057  2.96942   ]
    2 : [ 0.92068   2.50304   ]
    3 : [ 0.0632061 2.29276   ]
    4 : [ 0.714382  2.38336   ]
    >>> # Mean
    >>> print(myRV.getMean())
    [0.5,2.5]
    >>> # Covariance
    >>> print(myRV.getCovariance())
    [[ 0.0833333 0         ]
     [ 0         0.0833333 ]]

    """

    def __init__(self, dim=0):
        self.__dim = dim
        self.__desc = [ 'x' + str(i) for i in range(dim) ]

    def __str__(self):
        return 'PythonRandomVector -> %s #%d' % (self.__desc, self.__dim)

    def __repr__(self):
        return self.__str__()

    def getDimension(self):
        """
        Get the dimension.

        Returns
        -------
        dim : positive int
            Dimension of the RandomVector.
        """
        return self.__dim

    def setDescription(self, desc):
        """
        Set the description.

        Parameters
        ----------
        desc : sequence of str
            *desc* describes the components of the RandomVector.
            Its size must be equal to the dimension of the RandomVector.
        """
        if len(desc) != self.__dim:
            raise ValueError('Description size does NOT match dimension')
        self.__desc = desc

    def getDescription(self):
        """
        Get the description.

        Returns
        -------
        desc : :class:`~openturns.Description`
            *desc* describes the components of the RandomVector.
        """
        return self.__desc

    def getRealization(self):
        """
        Get a realization of the random vector.

        Returns
        -------
        realization : :class:`~openturns.Point`
            Sequence of values randomly determined from the RandomVector definition.
        """
        raise RuntimeError('You must define a method getRealization() -> X, where X is a Point')

    def getMean(self):
        """
        Get the mean.

        Returns
        -------
        mean : :class:`~openturns.Point`
            Mean of the RandomVector.
        """
        raise RuntimeError('You must define a method mean -> X, where X is a Point')

    def getCovariance(self):
        """
        Get the covariance.

        Returns
        -------
        covariance : :class:`~openturns.CovarianceMatrix`
            Covariance of the RandomVector.
        """
        raise RuntimeError('You must define a method var -> M, where M is a CovarianceMatrix')


class RandomVectorImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _metamodel.RandomVectorImplementationTypedInterfaceObject_swiginit(self, _metamodel.new_RandomVectorImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _metamodel.RandomVectorImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _metamodel.RandomVectorImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _metamodel.RandomVectorImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _metamodel.RandomVectorImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _metamodel.RandomVectorImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _metamodel.delete_RandomVectorImplementationTypedInterfaceObject


_metamodel.RandomVectorImplementationTypedInterfaceObject_swigregister(RandomVectorImplementationTypedInterfaceObject)

class RandomVector(RandomVectorImplementationTypedInterfaceObject):
    """
    Random vectors.

    Parameters
    ----------
    distribution : :class:`~openturns.Distribution`
        Distribution of the :class:`~openturns.UsualRandomVector` to define.

    Notes
    -----
    A :class:`~openturns.RandomVector` provides at least a way to generate realizations.

    See also
    --------
    UsualRandomVector, CompositeRandomVector, ConditionalRandomVector,
    ConstantRandomVector, FunctionalChaosRandomVector, Event,
    PythonRandomVector
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
        return _metamodel.RandomVector_getClassName(self)

    def __repr__(self):
        return _metamodel.RandomVector___repr__(self)

    def __str__(self, *args):
        return _metamodel.RandomVector___str__(self, *args)

    def setDescription(self, description):
        """
        Accessor to the description of the RandomVector.

        Parameters
        ----------
        description : str or sequence of str
            Describes the components of the RandomVector.
        """
        return _metamodel.RandomVector_setDescription(self, description)

    def getDescription(self):
        """
        Accessor to the description of the RandomVector.

        Returns
        -------
        description : :class:`~openturns.Description`
            Describes the components of the RandomVector.
        """
        return _metamodel.RandomVector_getDescription(self)

    def isComposite(self):
        """
        Accessor to know if the RandomVector is a composite one.

        Returns
        -------
        isComposite : bool
            Indicates if the RandomVector is of type Composite or not.
        """
        return _metamodel.RandomVector_isComposite(self)

    def getDimension(self):
        """
        Accessor to the dimension of the RandomVector.

        Returns
        -------
        dimension : positive int
            Dimension of the RandomVector.
        """
        return _metamodel.RandomVector_getDimension(self)

    def getRealization(self):
        """
        Compute one realization of the RandomVector.

        Returns
        -------
        aRealization : :class:`~openturns.Point`
            Sequence of values randomly determined from the RandomVector definition.
            In the case of an event: one realization of the event (considered as a
            Bernoulli variable) which is a boolean value (1 for the realization of the
            event and 0 else).

        See also
        --------
        getSample

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getRealization())
        [0.608202,-1.26617]
        >>> print(randomVector.getRealization())
        [-0.438266,1.20548]
        """
        return _metamodel.RandomVector_getRealization(self)

    def getSample(self, size):
        r"""
        Compute realizations of the RandomVector.

        Parameters
        ----------
        n : int, :math:`n \geq 0`
            Number of realizations needed.

        Returns
        -------
        realizations : :class:`~openturns.Sample`
            n sequences of values randomly determined from the RandomVector definition.
            In the case of an event: n realizations of the event (considered as a
            Bernoulli variable) which are boolean values (1 for the realization of the
            event and 0 else).

        See also
        --------
        getRealization

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getSample(3))
            [ X0        X1        ]
        0 : [  0.608202 -1.26617  ]
        1 : [ -0.438266  1.20548  ]
        2 : [ -2.18139   0.350042 ]
        """
        return _metamodel.RandomVector_getSample(self, size)

    def getMarginal(self, *args):
        r"""
        Get the random vector corresponding to the :math:`i^{th}` marginal component(s).

        Parameters
        ----------
        i : int or list of ints, :math:`0\leq i < dim`
            Indicates the component(s) concerned. :math:`dim` is the dimension of the
            RandomVector.

        Returns
        -------
        vector :  :class:`~openturns.RandomVector`
            RandomVector restricted to the concerned components.

        Notes
        -----
        Let's note :math:`\vect{Y}=\Tr{(Y_1,\dots,Y_n)}` a random vector and
        :math:`I \in [1,n]` a set of indices. If :math:`\vect{Y}` is a
        :class:`~openturns.UsualRandomVector`, the subvector is defined by
        :math:`\tilde{\vect{Y}}=\Tr{(Y_i)}_{i \in I}`. If :math:`\vect{Y}` is a
        :class:`~openturns.CompositeRandomVector`, defined by
        :math:`\vect{Y}=f(\vect{X})` with :math:`f=(f_1,\dots,f_n)`,
        :math:`f_i` some scalar functions, the subvector is
        :math:`\tilde{\vect{Y}}=(f_i(\vect{X}))_{i \in I}`.

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getMarginal(1).getRealization())
        [0.608202]
        >>> print(randomVector.getMarginal(1).getDistribution())
        Normal(mu = 0, sigma = 1)
        """
        return _metamodel.RandomVector_getMarginal(self, *args)

    def getMean(self):
        """
        Accessor to the mean of the RandomVector.

        Returns
        -------
        mean : :class:`~openturns.Point`
            Mean of the considered :class:`~openturns.UsualRandomVector`.

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.5], [1.0, 1.5], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getMean())
        [0,0.5]
        """
        return _metamodel.RandomVector_getMean(self)

    def getCovariance(self):
        """
        Accessor to the covariance of the RandomVector.

        Returns
        -------
        covariance : :class:`~openturns.CovarianceMatrix`
            Covariance of the considered :class:`~openturns.UsualRandomVector`.

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.5], [1.0, 1.5], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getCovariance())
        [[ 1    0    ]
         [ 0    2.25 ]]
        """
        return _metamodel.RandomVector_getCovariance(self)

    def getAntecedent(self):
        r"""
        Accessor to the antecedent RandomVector in case of a composite RandomVector.

        Returns
        -------
        antecedent : :class:`~openturns.RandomVector`
            Antecedent RandomVector :math:`\vect{X}` in case of a
            :class:`~openturns.CompositeRandomVector` such as:
            :math:`\vect{Y}=f(\vect{X})`.
        """
        return _metamodel.RandomVector_getAntecedent(self)

    def getFunction(self):
        r"""
        Accessor to the Function in case of a composite RandomVector.

        Returns
        -------
        function : :class:`~openturns.Function`
            Function used to define a :class:`~openturns.CompositeRandomVector` as the
            image through this function of the antecedent :math:`\vect{X}`:
            :math:`\vect{Y}=f(\vect{X})`.
        """
        return _metamodel.RandomVector_getFunction(self)

    def getDistribution(self):
        """
        Accessor to the distribution of the RandomVector.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Distribution of the considered :class:`~openturns.UsualRandomVector`.

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getDistribution())
        Normal(mu = [0,0], sigma = [1,1], R = [[ 1 0 ]
         [ 0 1 ]])
        """
        return _metamodel.RandomVector_getDistribution(self)

    def getOperator(self):
        """
        Accessor to the comparaison operator of the Event.

        Returns
        -------
        operator : :class:`~openturns.ComparisonOperator`
            Comparaison operator used to define the :class:`~openturns.RandomVector`.
        """
        return _metamodel.RandomVector_getOperator(self)

    def getThreshold(self):
        """
        Accessor to the threshold of the Event.

        Returns
        -------
        threshold : float
            Threshold of the :class:`~openturns.RandomVector`.
        """
        return _metamodel.RandomVector_getThreshold(self)

    def getDomain(self):
        """
        Accessor to the domain of the Event.

        Returns
        -------
        domain : :class:`~openturns.Domain`
            Describes the domain of an event.
        """
        return _metamodel.RandomVector_getDomain(self)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _metamodel.RandomVector_getParameter(self)

    def setParameter(self, parameters):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _metamodel.RandomVector_setParameter(self, parameters)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _metamodel.RandomVector_getParameterDescription(self)

    def isEvent(self):
        """
        Whether the random vector is an event.

        Returns
        -------
        isEvent : bool
            Whether it takes it values in {0, 1}.
        """
        return _metamodel.RandomVector_isEvent(self)

    def intersect(self, other):
        """
        Intersection of two events.

        Parameters
        ----------
        event : :class:`~openturns.RandomVector`
            A composite event

        Returns
        -------
        event : :class:`~openturns.RandomVector`
            Intersection event
        """
        return _metamodel.RandomVector_intersect(self, other)

    def join(self, other):
        """
        Union of two events.

        Parameters
        ----------
        event : :class:`~openturns.RandomVector`
            A composite event

        Returns
        -------
        event : :class:`~openturns.RandomVector`
            Union event
        """
        return _metamodel.RandomVector_join(self, other)

    def __init__(self, *args):
        _metamodel.RandomVector_swiginit(self, _metamodel.new_RandomVector(*args))

    __swig_destroy__ = _metamodel.delete_RandomVector


_metamodel.RandomVector_swigregister(RandomVector)

class CompositeRandomVector(openturns.randomvector.RandomVectorImplementation):
    """
    Random Vector obtained by applying a function.

    Allows to define the random variable :math:`Y=f(X)` from a function :math:`f`
    and another random variable :math:`X`.

    Parameters
    ----------
    f : :class:`~openturns.Function`
        Function to apply to the antecedent.
    X : :class:`~openturns.RandomVector`
        Random vector of the antecedent.

    Examples
    --------
    >>> import openturns as ot
    >>> X = ot.RandomVector(ot.Normal())
    >>> f = ot.SymbolicFunction(['x'], ['x^2*sin(x)'])
    >>> Y = ot.CompositeRandomVector(f, X)

    Draw a sample:

    >>> sample = Y.getSample(5)
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
        return _metamodel.CompositeRandomVector_getClassName(self)

    def __repr__(self):
        return _metamodel.CompositeRandomVector___repr__(self)

    def isComposite(self):
        """
        Accessor to know if the RandomVector is a composite one.

        Returns
        -------
        isComposite : bool
            Indicates if the RandomVector is of type Composite or not.
        """
        return _metamodel.CompositeRandomVector_isComposite(self)

    def getDimension(self):
        """
        Accessor to the dimension of the RandomVector.

        Returns
        -------
        dimension : positive int
            Dimension of the RandomVector.
        """
        return _metamodel.CompositeRandomVector_getDimension(self)

    def getRealization(self):
        """
        Compute one realization of the RandomVector.

        Returns
        -------
        aRealization : :class:`~openturns.Point`
            Sequence of values randomly determined from the RandomVector definition.
            In the case of an event: one realization of the event (considered as a
            Bernoulli variable) which is a boolean value (1 for the realization of the
            event and 0 else).

        See also
        --------
        getSample

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getRealization())
        [0.608202,-1.26617]
        >>> print(randomVector.getRealization())
        [-0.438266,1.20548]
        """
        return _metamodel.CompositeRandomVector_getRealization(self)

    def getSample(self, size):
        r"""
        Compute realizations of the RandomVector.

        Parameters
        ----------
        n : int, :math:`n \geq 0`
            Number of realizations needed.

        Returns
        -------
        realizations : :class:`~openturns.Sample`
            n sequences of values randomly determined from the RandomVector definition.
            In the case of an event: n realizations of the event (considered as a
            Bernoulli variable) which are boolean values (1 for the realization of the
            event and 0 else).

        See also
        --------
        getRealization

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getSample(3))
            [ X0        X1        ]
        0 : [  0.608202 -1.26617  ]
        1 : [ -0.438266  1.20548  ]
        2 : [ -2.18139   0.350042 ]
        """
        return _metamodel.CompositeRandomVector_getSample(self, size)

    def getMarginal(self, *args):
        r"""
        Get the random vector corresponding to the :math:`i^{th}` marginal component(s).

        Parameters
        ----------
        i : int or list of ints, :math:`0\leq i < dim`
            Indicates the component(s) concerned. :math:`dim` is the dimension of the
            RandomVector.

        Returns
        -------
        vector :  :class:`~openturns.RandomVector`
            RandomVector restricted to the concerned components.

        Notes
        -----
        Let's note :math:`\vect{Y}=\Tr{(Y_1,\dots,Y_n)}` a random vector and
        :math:`I \in [1,n]` a set of indices. If :math:`\vect{Y}` is a
        :class:`~openturns.UsualRandomVector`, the subvector is defined by
        :math:`\tilde{\vect{Y}}=\Tr{(Y_i)}_{i \in I}`. If :math:`\vect{Y}` is a
        :class:`~openturns.CompositeRandomVector`, defined by
        :math:`\vect{Y}=f(\vect{X})` with :math:`f=(f_1,\dots,f_n)`,
        :math:`f_i` some scalar functions, the subvector is
        :math:`\tilde{\vect{Y}}=(f_i(\vect{X}))_{i \in I}`.

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getMarginal(1).getRealization())
        [0.608202]
        >>> print(randomVector.getMarginal(1).getDistribution())
        Normal(mu = 0, sigma = 1)
        """
        return _metamodel.CompositeRandomVector_getMarginal(self, *args)

    def getAntecedent(self):
        r"""
        Accessor to the antecedent RandomVector in case of a composite RandomVector.

        Returns
        -------
        antecedent : :class:`~openturns.RandomVector`
            Antecedent RandomVector :math:`\vect{X}` in case of a
            :class:`~openturns.CompositeRandomVector` such as:
            :math:`\vect{Y}=f(\vect{X})`.
        """
        return _metamodel.CompositeRandomVector_getAntecedent(self)

    def getFunction(self):
        r"""
        Accessor to the Function in case of a composite RandomVector.

        Returns
        -------
        function : :class:`~openturns.Function`
            Function used to define a :class:`~openturns.CompositeRandomVector` as the
            image through this function of the antecedent :math:`\vect{X}`:
            :math:`\vect{Y}=f(\vect{X})`.
        """
        return _metamodel.CompositeRandomVector_getFunction(self)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _metamodel.CompositeRandomVector_getParameter(self)

    def setParameter(self, parameters):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _metamodel.CompositeRandomVector_setParameter(self, parameters)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _metamodel.CompositeRandomVector_getParameterDescription(self)

    def __init__(self, *args):
        _metamodel.CompositeRandomVector_swiginit(self, _metamodel.new_CompositeRandomVector(*args))

    __swig_destroy__ = _metamodel.delete_CompositeRandomVector


_metamodel.CompositeRandomVector_swigregister(CompositeRandomVector)

class ThresholdEvent(RandomVector):
    r"""
    Random vector defined from a comparison operator and a threshold.

    The event occurs when the realization of the underlying random vector exceeds the threshold.

    Parameters
    ----------
    antecedent : :class:`~openturns.RandomVector` of dimension 1
        Output variable of interest.
    comparisonOperator : :class:`~openturns.ComparisonOperator`
        Comparison operator used to compare *antecedent* with *threshold*.
    threshold : float
        *threshold* we want to compare to *antecedent*.

    See also
    --------
    ProcessEvent, DomainEvent

    Notes
    -----
    An event is defined as follows:

    .. math::

        \cD_f = \{\vect{X} \in \Rset^n \, / \, g(\vect{X},\vect{d}) \le 0\}

    where :math:`\vect{X}` denotes a random input vector, representing the sources
    of uncertainties, :math:`\vect{d}` is a determinist vector, representing the
    fixed variables and :math:`g(\vect{X},\vect{d})` is the limit state function of
    the model.
    The probability content of the event :math:`\cD_f` is :math:`P_f`:

    .. math::

        P_f = \int_{g(\vect{X},\vect{d})\le 0}f_\vect{X}(\vect{x})\di{\vect{x}}

    Here, the event considered is explicited directly from the limit state function
    :math:`g(\vect{X}\,,\,\vect{d})` : this is the classical structural reliability
    formulation. However, if the event is a threshold exceedance, it is useful to
    explicite the variable of interest :math:`Z=\tilde{g}(\vect{X}\,,\,\vect{d})`,
    evaluated from the model :math:`\tilde{g}(.)`. In that case, the event
    considered, associated to the threshold :math:`z_s` has the formulation:

    .. math::

        \cD_f = \{ \vect{X} \in \Rset^n \, / \, Z=\tilde{g}(\vect{X}\,,\,\vect{d}) > z_s \}

    and the limit state function is:

    .. math::

        g(\vect{X}\,,\,\vect{d}) &= z_s - Z \\
                                 &= z_s - \tilde{g}(\vect{X}\,,\,\vect{d})

    :math:`P_f` is the threshold exceedance probability, defined as:

    .. math::

        P_f &= P(Z \geq z_s) \\
            &= \int_{g(\vect{X}, \vect{d}) \le 0} \pdf\di{\vect{x}}

    Examples
    --------
    >>> import openturns as ot
    >>> dim = 2
    >>> X = ot.RandomVector(ot.Normal(dim))
    >>> model = ot.SymbolicFunction(['x1', 'x2'], ['x1+x2'])
    >>> Y = ot.CompositeRandomVector(model, X)
    >>> event = ot.ThresholdEvent(Y, ot.Less(), 1.0)

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
        return _metamodel.ThresholdEvent_getClassName(self)

    def __repr__(self):
        return _metamodel.ThresholdEvent___repr__(self)

    def __str__(self, *args):
        return _metamodel.ThresholdEvent___str__(self, *args)

    def __init__(self, *args):
        _metamodel.ThresholdEvent_swiginit(self, _metamodel.new_ThresholdEvent(*args))

    __swig_destroy__ = _metamodel.delete_ThresholdEvent


_metamodel.ThresholdEvent_swigregister(ThresholdEvent)

class DomainEvent(CompositeRandomVector):
    """
    Event defined from a domain.

    The event occurs when a realization of the underlying random vector belongs to the domain.

    Parameters
    ----------
    antecedent : :class:`~openturns.RandomVector` of dimension 1
        Antecedent.
    domain : :class:`~openturns.Domain`
        Domain, of same dimension.

    See also
    --------
    ProcessEvent, ThresholdEvent

    Examples
    --------
    >>> import openturns as ot
    >>> dim = 2
    >>> X = ot.RandomVector(ot.Normal(dim))
    >>> model = ot.SymbolicFunction(['x1', 'x2'], ['x1+x2', '2*x1'])
    >>> Y = ot.CompositeRandomVector(model, X)
    >>> domain = ot.Interval(dim)
    >>> event = ot.DomainEvent(Y, domain)
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
        return _metamodel.DomainEvent_getClassName(self)

    def __repr__(self):
        return _metamodel.DomainEvent___repr__(self)

    def getDimension(self):
        """
        Accessor to the dimension of the RandomVector.

        Returns
        -------
        dimension : positive int
            Dimension of the RandomVector.
        """
        return _metamodel.DomainEvent_getDimension(self)

    def getDomain(self):
        """
        Accessor to the domain of the Event.

        Returns
        -------
        domain : :class:`~openturns.Domain`
            Describes the domain of an event.
        """
        return _metamodel.DomainEvent_getDomain(self)

    def getRealization(self):
        """
        Compute one realization of the RandomVector.

        Returns
        -------
        aRealization : :class:`~openturns.Point`
            Sequence of values randomly determined from the RandomVector definition.
            In the case of an event: one realization of the event (considered as a
            Bernoulli variable) which is a boolean value (1 for the realization of the
            event and 0 else).

        See also
        --------
        getSample

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getRealization())
        [0.608202,-1.26617]
        >>> print(randomVector.getRealization())
        [-0.438266,1.20548]
        """
        return _metamodel.DomainEvent_getRealization(self)

    def getSample(self, size):
        r"""
        Compute realizations of the RandomVector.

        Parameters
        ----------
        n : int, :math:`n \geq 0`
            Number of realizations needed.

        Returns
        -------
        realizations : :class:`~openturns.Sample`
            n sequences of values randomly determined from the RandomVector definition.
            In the case of an event: n realizations of the event (considered as a
            Bernoulli variable) which are boolean values (1 for the realization of the
            event and 0 else).

        See also
        --------
        getRealization

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getSample(3))
            [ X0        X1        ]
        0 : [  0.608202 -1.26617  ]
        1 : [ -0.438266  1.20548  ]
        2 : [ -2.18139   0.350042 ]
        """
        return _metamodel.DomainEvent_getSample(self, size)

    def isEvent(self):
        """
        Whether the random vector is an event.

        Returns
        -------
        isEvent : bool
            Whether it takes it values in {0, 1}.
        """
        return _metamodel.DomainEvent_isEvent(self)

    def __init__(self, *args):
        _metamodel.DomainEvent_swiginit(self, _metamodel.new_DomainEvent(*args))

    __swig_destroy__ = _metamodel.delete_DomainEvent


_metamodel.DomainEvent_swigregister(DomainEvent)

class ProcessEvent(openturns.randomvector.RandomVectorImplementation):
    """
    Event defined from a process and a domain.

    The event occurs when the process enters the specified domain.

    Parameters
    ----------
    process : :class:`~openturns.Process`
        Process.
    domain : :class:`~openturns.Domain`
        Domain, of same dimension.

    See also
    --------
    DomainEvent, ThresholdEvent

    Examples
    --------
    >>> import openturns as ot
    >>> dim = 2
    >>> dist = ot.Normal(dim)
    >>> X = ot.WhiteNoise(dist)
    >>> domain = ot.Interval(dim)
    >>> event = ot.ProcessEvent(X, domain)
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
        return _metamodel.ProcessEvent_getClassName(self)

    def __repr__(self):
        return _metamodel.ProcessEvent___repr__(self)

    def getDimension(self):
        """
        Accessor to the dimension of the RandomVector.

        Returns
        -------
        dimension : positive int
            Dimension of the RandomVector.
        """
        return _metamodel.ProcessEvent_getDimension(self)

    def getDomain(self):
        """
        Accessor to the domain of the Event.

        Returns
        -------
        domain : :class:`~openturns.Domain`
            Describes the domain of an event.
        """
        return _metamodel.ProcessEvent_getDomain(self)

    def getProcess(self):
        """
        Get the stochastic process.

        Returns
        -------
        process : :class:`~openturns.Process`
            Stochastic process used to define the :class:`~openturns.RandomVector`.
        """
        return _metamodel.ProcessEvent_getProcess(self)

    def getRealization(self):
        """
        Compute one realization of the RandomVector.

        Returns
        -------
        aRealization : :class:`~openturns.Point`
            Sequence of values randomly determined from the RandomVector definition.
            In the case of an event: one realization of the event (considered as a
            Bernoulli variable) which is a boolean value (1 for the realization of the
            event and 0 else).

        See also
        --------
        getSample

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getRealization())
        [0.608202,-1.26617]
        >>> print(randomVector.getRealization())
        [-0.438266,1.20548]
        """
        return _metamodel.ProcessEvent_getRealization(self)

    def isEvent(self):
        """
        Whether the random vector is an event.

        Returns
        -------
        isEvent : bool
            Whether it takes it values in {0, 1}.
        """
        return _metamodel.ProcessEvent_isEvent(self)

    def __init__(self, *args):
        _metamodel.ProcessEvent_swiginit(self, _metamodel.new_ProcessEvent(*args))

    __swig_destroy__ = _metamodel.delete_ProcessEvent


_metamodel.ProcessEvent_swigregister(ProcessEvent)

class ConditionalRandomVector(openturns.randomvector.RandomVectorImplementation):
    r"""
    Conditional random vector.

    Helper class for defining the random vector :math:`\vect{X}` such that  :math:`\vect{X}|\vect{\Theta}` follows the distribution :math:`\mathcal{L}_{\vect{X}|\vect{\Theta}}`, with :math:`\vect{\Theta}` a random vector of dimension the dimension of :math:`\vect{\Theta}`.

    Available constructors:
       ConditionalRandomVector(*conditionedDist, randomParameters*)

    Parameters
    ----------

    conditionedDist : :class:`~openturns.Distribution`, the distribution of :math:`\vect{X}|\vect{\Theta}`, whose parameters will be overwritten by :math:`\vect{\Theta}`.

    randomParameters : :class:`~openturns.RandomVector`, the random parameters :math:`\vect{\Theta}` of the `conditionedDist` distribution. 

    Notes
    -----
    Its probability density function is defined as:

    .. math::

        f_{\vect{X}}(\vect{x}) = \int f_{\vect{X}|\vect{\Theta}=\vect{\theta}}(\vect{x}|\vect{\theta}) f_{\vect{\Theta}}(\vect{\theta})\di{\vect{\theta}}

    with  :math:`f_{\vect{X}|\vect{\Theta}=\vect{\theta}}` the PDF of the distribution of :math:`\vect{X}|\vect{\Theta}`, where :math:`\vect{\Theta}` has been replaced by :math:`\vect{\theta}`, :math:`f_{\vect{\Theta}}` the PDF of :math:`\vect{\Theta}`.

    Note that there exist other (quasi) equivalent modellings using a combination of the classes :class:`~openturns.ConditionalDistribution` and :class:`~openturns.RandomVector` (see the Use Cases Guide).

    Examples
    --------
    Create a random vector:

    >>> import openturns as ot
    >>> distXgivenT = ot.Exponential()
    >>> distGamma = ot.Uniform(1.0, 2.0)
    >>> distAlpha = ot.Uniform(0.0, 0.1)
    >>> distTheta = ot.ComposedDistribution([distGamma, distAlpha])
    >>> rvTheta = ot.RandomVector(distTheta)
    >>> rvX = ot.ConditionalRandomVector(distXgivenT, rvTheta)

    Draw a sample:

    >>> sample = rvX.getSample(5)
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
        return _metamodel.ConditionalRandomVector_getClassName(self)

    def __repr__(self):
        return _metamodel.ConditionalRandomVector___repr__(self)

    def getDimension(self):
        """
        Accessor to the dimension of the RandomVector.

        Returns
        -------
        dimension : positive int
            Dimension of the RandomVector.
        """
        return _metamodel.ConditionalRandomVector_getDimension(self)

    def getRealization(self, *args):
        """
        Compute one realization of the RandomVector.

        Returns
        -------
        aRealization : :class:`~openturns.Point`
            Sequence of values randomly determined from the RandomVector definition.
            In the case of an event: one realization of the event (considered as a
            Bernoulli variable) which is a boolean value (1 for the realization of the
            event and 0 else).

        See also
        --------
        getSample

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getRealization())
        [0.608202,-1.26617]
        >>> print(randomVector.getRealization())
        [-0.438266,1.20548]
        """
        return _metamodel.ConditionalRandomVector_getRealization(self, *args)

    def getDistribution(self):
        r"""
        Accessor to the distribution's conditioned distribution parameter `conditionedDistribution`.

        Returns
        -------
        conditionedDistribution : :class:`~openturns.Distribution`, the distribution of :math:`\vect{X}|\vect{\Theta}=\vect{\theta}`, where the parameters :math:`\vect{\theta}` are equal to the  values used to generate the last realization of :math:`\vect{X}`.

        """
        return _metamodel.ConditionalRandomVector_getDistribution(self)

    def getRandomParameters(self):
        r"""
        Accessor to the distribution's random parameter `randomParameters`.

        Returns
        -------
        randomParameters : :class:`~openturns.RandomVector`, the random parameters :math:`\vect{\Theta}`.

        """
        return _metamodel.ConditionalRandomVector_getRandomParameters(self)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _metamodel.ConditionalRandomVector_getParameter(self)

    def setParameter(self, parameters):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _metamodel.ConditionalRandomVector_setParameter(self, parameters)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _metamodel.ConditionalRandomVector_getParameterDescription(self)

    def __init__(self, *args):
        _metamodel.ConditionalRandomVector_swiginit(self, _metamodel.new_ConditionalRandomVector(*args))

    __swig_destroy__ = _metamodel.delete_ConditionalRandomVector


_metamodel.ConditionalRandomVector_swigregister(ConditionalRandomVector)

class Event(RandomVector):
    """
    Event base class.

    See also
    --------
    ThresholdEvent, ProcessEvent, DomainEvent

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
        return _metamodel.Event_getClassName(self)

    def __repr__(self):
        return _metamodel.Event___repr__(self)

    def __str__(self, *args):
        return _metamodel.Event___str__(self, *args)

    def __init__(self, *args):
        _metamodel.Event_swiginit(self, _metamodel.new_Event(*args))

    __swig_destroy__ = _metamodel.delete_Event


_metamodel.Event_swigregister(Event)

class StandardEvent(RandomVector):
    r"""
    Event defined in the standard space.

    Available constructor:
        StandardEvent(*antecedent, comparisonOperator, threshold*)

        StandardEvent(*event*)

    Parameters
    ----------
    antecedent : :class:`~openturns.RandomVector` of dimension 1
        Output variable of interest.
    comparisonOperator : :class:`~openturns.ComparisonOperator`
        Comparison operator used to compare *antecedent* with *threshold*.
    threshold : float
        *threshold* we want to compare to *antecedent*.
    event : :class:`~openturns.RandomVector`
        Physical event associated with the standard event to be created.

    Notes
    -----
    An event is defined as follows:

    .. math::

        \cD_f = \{\vect{X} \in \Rset^n \, / \, g(\vect{X},\vect{d}) \le 0\}

    where :math:`\vect{X}` denotes a random input vector, representing the sources
    of uncertainties, :math:`\vect{d}` is a determinist vector, representing the
    fixed variables and :math:`g(\vect{X},\vect{d})` is the limit state function of
    the model.

    One way to evaluate the probability content :math:`P_f` of the event :math:`\cD_f`:

    .. math::

        P_f = \int_{g(\vect{X},\vect{d})\le 0}f_\vect{X}(\vect{x})\di{\vect{x}}

    is to use an isoprobabilistic transformation to move from the physical space
    to a standard normal space (U-space) where distributions are spherical
    (invariant by rotation by definition), with zero mean, unit variance and unit
    correlation matrix. The usual isoprobabilistic transformations are the
    Generalized Nataf transformation and the Rosenblatt one.

    In that new U-space, the event has the new expression defined
    from the transformed limit state function of the model
    :math:`G : \cD_f = \{\vect{U} \in \Rset^n \, | \, G(\vect{U}\,,\,\vect{d}) \le 0\}`
    and its boundary :
    :math:`\{\vect{U} \in \Rset^n \, | \,G(\vect{U}\,,\,\vect{d}) = 0\}`.

    See also
    --------
    Analytical, SORM, FORM, SORMResult, FORMResult, StrongMaximumTest

    Examples
    --------

    A StandardEvent created from a limit state function :

    >>> import openturns as ot
    >>> myFunction = ot.SymbolicFunction(['E', 'F', 'L', 'I'], ['-F*L^3/(3*E*I)'])
    >>> myDistribution = ot.Normal(4)
    >>> vect = ot.RandomVector(myDistribution)
    >>> output = ot.CompositeRandomVector(myFunction, vect)
    >>> myStandardEvent = ot.StandardEvent(output, ot.Less(), 1.0)

    A StandardEvent based on an event :

    >>> myEvent = ot.ThresholdEvent(output, ot.Less(), 1.0)
    >>> myStandardEvent = ot.StandardEvent(myEvent)
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
        return _metamodel.StandardEvent_getClassName(self)

    def __init__(self, *args):
        _metamodel.StandardEvent_swiginit(self, _metamodel.new_StandardEvent(*args))

    __swig_destroy__ = _metamodel.delete_StandardEvent


_metamodel.StandardEvent_swigregister(StandardEvent)

class RandomVectorCollection(object):
    """
    Collection.

    Examples
    --------
    >>> import openturns as ot

    - Collection of **real values**:

    >>> ot.ScalarCollection(2)
    [0,0]
    >>> ot.ScalarCollection(2, 3.25)
    [3.25,3.25]
    >>> vector = ot.ScalarCollection([2.0, 1.5, 2.6])
    >>> vector
    [2,1.5,2.6]
    >>> vector[1] = 4.2
    >>> vector
    [2,4.2,2.6]
    >>> vector.add(3.8)
    >>> vector
    [2,4.2,2.6,3.8]

    - Collection of **complex values**:

    >>> ot.ComplexCollection(2)
    [(0,0),(0,0)]
    >>> ot.ComplexCollection(2, 3+4j)
    [(3,4),(3,4)]
    >>> vector = ot.ComplexCollection([2+3j, 1-4j, 3.0])
    >>> vector
    [(2,3),(1,-4),(3,0)]
    >>> vector[1] = 4+3j
    >>> vector
    [(2,3),(4,3),(3,0)]
    >>> vector.add(5+1j)
    >>> vector
    [(2,3),(4,3),(3,0),(5,1)]

    - Collection of **booleans**:

    >>> ot.BoolCollection(3)
    [0,0,0]
    >>> ot.BoolCollection(3, 1)
    [1,1,1]
    >>> vector = ot.BoolCollection([0, 1, 0])
    >>> vector
    [0,1,0]
    >>> vector[1] = 0
    >>> vector
    [0,0,0]
    >>> vector.add(1)
    >>> vector
    [0,0,0,1]

    - Collection of **distributions**:

    >>> print(ot.DistributionCollection(2))
    [Uniform(a = -1, b = 1),Uniform(a = -1, b = 1)]
    >>> print(ot.DistributionCollection(2, ot.Gamma(2.75, 1.0)))
    [Gamma(k = 2.75, lambda = 1, gamma = 0),Gamma(k = 2.75, lambda = 1, gamma = 0)]
    >>> vector = ot.DistributionCollection([ot.Normal(), ot.Uniform()])
    >>> print(vector)
    [Normal(mu = 0, sigma = 1),Uniform(a = -1, b = 1)]
    >>> vector[1] = ot.Uniform(-0.5, 1)
    >>> print(vector)
    [Normal(mu = 0, sigma = 1),Uniform(a = -0.5, b = 1)]
    >>> vector.add(ot.Gamma(2.75, 1.0))
    >>> print(vector)
    [Normal(mu = 0, sigma = 1),Uniform(a = -0.5, b = 1),Gamma(k = 2.75, lambda = 1, gamma = 0)]
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __swig_destroy__ = _metamodel.delete_RandomVectorCollection

    def clear(self):
        """
        Reset the collection to zero dimension.

        Examples
        --------
        >>> import openturns as ot
        >>> x = ot.Point(2)
        >>> x.clear()
        >>> x
        class=Point name=Unnamed dimension=0 values=[]
        """
        return _metamodel.RandomVectorCollection_clear(self)

    def __len__(self):
        return _metamodel.RandomVectorCollection___len__(self)

    def __eq__(self, rhs):
        return _metamodel.RandomVectorCollection___eq__(self, rhs)

    def __contains__(self, val):
        return _metamodel.RandomVectorCollection___contains__(self, val)

    def __getitem__(self, i):
        return _metamodel.RandomVectorCollection___getitem__(self, i)

    def __setitem__(self, i, val):
        return _metamodel.RandomVectorCollection___setitem__(self, i, val)

    def __delitem__(self, i):
        return _metamodel.RandomVectorCollection___delitem__(self, i)

    def at(self, *args):
        """
        Access to an element of the collection.

        Parameters
        ----------
        index : positive int
            Position of the element to access.

        Returns
        -------
        element : type depends on the type of the collection
            Element of the collection at the position *index*.
        """
        return _metamodel.RandomVectorCollection_at(self, *args)

    def add(self, *args):
        """
        Append a component (in-place).

        Parameters
        ----------
        value : type depends on the type of the collection.
            The component to append.

        Examples
        --------
        >>> import openturns as ot
        >>> x = ot.Point(2)
        >>> x.add(1.)
        >>> print(x)
        [0,0,1]
        """
        return _metamodel.RandomVectorCollection_add(self, *args)

    def getSize(self):
        """
        Get the collection's dimension (or size).

        Returns
        -------
        n : int
            The number of components in the collection.
        """
        return _metamodel.RandomVectorCollection_getSize(self)

    def resize(self, newSize):
        """
        Change the size of the collection.

        Parameters
        ----------
        newSize : positive int
            New size of the collection.

        Notes
        -----
        If the new size is smaller than the older one, the last elements are thrown
        away, else the new elements are set to the default value of the element type.

        Examples
        --------
        >>> import openturns as ot
        >>> x = ot.Point(2, 4)
        >>> print(x)
        [4,4]
        >>> x.resize(1)
        >>> print(x)
        [4]
        >>> x.resize(4)
        >>> print(x)
        [4,0,0,0]
        """
        return _metamodel.RandomVectorCollection_resize(self, newSize)

    def isEmpty(self):
        """
        Tell if the collection is empty.

        Returns
        -------
        isEmpty : bool
            *True* if there is no element in the collection.

        Examples
        --------
        >>> import openturns as ot
        >>> x = ot.Point(2)
        >>> x.isEmpty()
        False
        >>> x.clear()
        >>> x.isEmpty()
        True
        """
        return _metamodel.RandomVectorCollection_isEmpty(self)

    def __repr__(self):
        return _metamodel.RandomVectorCollection___repr__(self)

    def __str__(self, *args):
        return _metamodel.RandomVectorCollection___str__(self, *args)

    def __init__(self, *args):
        _metamodel.RandomVectorCollection_swiginit(self, _metamodel.new_RandomVectorCollection(*args))


_metamodel.RandomVectorCollection_swigregister(RandomVectorCollection)

class IntersectionEvent(openturns.randomvector.RandomVectorImplementation):
    r"""
    Event defined as the intersection of several events.

    The occurence of all the events is necessary for the system event to occur (parallel system):

    .. math::

        E_{sys} = \bigcap_{i=1}^N E_i

    Parameters
    ----------
    coll : sequence of :class:`~openturns.RandomVector`
        Collection of events

    See also
    --------
    Event

    Examples
    --------
    >>> import openturns as ot
    >>> dim = 2
    >>> X = ot.RandomVector(ot.Normal(dim))
    >>> f1 = ot.SymbolicFunction(['x1', 'x2'], ['x1'])
    >>> f2 = ot.SymbolicFunction(['x1', 'x2'], ['x2'])
    >>> Y1 = ot.CompositeRandomVector(f1, X)
    >>> Y2 = ot.CompositeRandomVector(f2, X)
    >>> e1 = ot.ThresholdEvent(Y1, ot.Less(), 0.0)
    >>> e2 = ot.ThresholdEvent(Y2, ot.Greater(), 0.0)
    >>> event = ot.IntersectionEvent([e1, e2])

    Then it can be used for sampling (or with simulation algorithms):

    >>> p = event.getSample(1000).computeMean()
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
        return _metamodel.IntersectionEvent_getClassName(self)

    def __repr__(self):
        return _metamodel.IntersectionEvent___repr__(self)

    def getDimension(self):
        """
        Accessor to the dimension of the RandomVector.

        Returns
        -------
        dimension : positive int
            Dimension of the RandomVector.
        """
        return _metamodel.IntersectionEvent_getDimension(self)

    def setEventCollection(self, collection):
        """
        Accessor to sub events.

        Parameters
        ----------
        events : sequence of :class:`~openturns.RandomVector`
            List of sub events.
        """
        return _metamodel.IntersectionEvent_setEventCollection(self, collection)

    def getEventCollection(self):
        """
        Accessor to sub events.

        Returns
        -------
        events : :class:`~openturns.RandomVectorCollection`
            List of sub events.
        """
        return _metamodel.IntersectionEvent_getEventCollection(self)

    def getRealization(self):
        """
        Compute one realization of the RandomVector.

        Returns
        -------
        aRealization : :class:`~openturns.Point`
            Sequence of values randomly determined from the RandomVector definition.
            In the case of an event: one realization of the event (considered as a
            Bernoulli variable) which is a boolean value (1 for the realization of the
            event and 0 else).

        See also
        --------
        getSample

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getRealization())
        [0.608202,-1.26617]
        >>> print(randomVector.getRealization())
        [-0.438266,1.20548]
        """
        return _metamodel.IntersectionEvent_getRealization(self)

    def isEvent(self):
        """
        Whether the random vector is an event.

        Returns
        -------
        isEvent : bool
            Whether it takes it values in {0, 1}.
        """
        return _metamodel.IntersectionEvent_isEvent(self)

    def isComposite(self):
        """
        Accessor to know if the RandomVector is a composite one.

        Returns
        -------
        isComposite : bool
            Indicates if the RandomVector is of type Composite or not.
        """
        return _metamodel.IntersectionEvent_isComposite(self)

    def getAntecedent(self):
        """
        Accessor to the antecedent random vector.

        Returns
        -------
        antecedent : :class:`~openturns.RandomVector`
            Defined as the root cause.
        """
        return _metamodel.IntersectionEvent_getAntecedent(self)

    def getFunction(self):
        """
        Accessor to the function.

        Returns
        -------
        function : :class:`~openturns.Function`
            Composed function.
        """
        return _metamodel.IntersectionEvent_getFunction(self)

    def getDomain(self):
        """
        Accessor to the domain of the Event.

        Returns
        -------
        domain : :class:`~openturns.Domain`
            Describes the domain of an event.
        """
        return _metamodel.IntersectionEvent_getDomain(self)

    def getOperator(self):
        """
        Accessor to the comparaison operator of the Event.

        Returns
        -------
        operator : :class:`~openturns.ComparisonOperator`
            Comparaison operator used to define the :class:`~openturns.RandomVector`.
        """
        return _metamodel.IntersectionEvent_getOperator(self)

    def getThreshold(self):
        """
        Accessor to the threshold of the Event.

        Returns
        -------
        threshold : float
            Threshold of the :class:`~openturns.RandomVector`.
        """
        return _metamodel.IntersectionEvent_getThreshold(self)

    def getComposedEvent(self):
        """
        Accessor to the composed event.

        Returns
        -------
        composed : :class:`~openturns.RandomVector`
            Composed event.
        """
        return _metamodel.IntersectionEvent_getComposedEvent(self)

    def __init__(self, *args):
        _metamodel.IntersectionEvent_swiginit(self, _metamodel.new_IntersectionEvent(*args))

    __swig_destroy__ = _metamodel.delete_IntersectionEvent


_metamodel.IntersectionEvent_swigregister(IntersectionEvent)

class UnionEvent(openturns.randomvector.RandomVectorImplementation):
    r"""
    Event defined as the intersection of several events.

    An occurence of one single event :math:`E_i` yields the occurence of the system event (series system):

    .. math::

        E_{sys} = \bigcup_{i=1}^N E_i

    Parameters
    ----------
    coll : sequence of :class:`~openturns.RandomVector`
        Collection of events

    See also
    --------
    Event

    Examples
    --------
    >>> import openturns as ot
    >>> dim = 2
    >>> X = ot.RandomVector(ot.Normal(dim))
    >>> f1 = ot.SymbolicFunction(['x1', 'x2'], ['x1'])
    >>> f2 = ot.SymbolicFunction(['x1', 'x2'], ['x2'])
    >>> Y1 = ot.CompositeRandomVector(f1, X)
    >>> Y2 = ot.CompositeRandomVector(f2, X)
    >>> e1 = ot.ThresholdEvent(Y1, ot.Less(), 0.0)
    >>> e2 = ot.ThresholdEvent(Y2, ot.Greater(), 0.0)
    >>> event = ot.UnionEvent([e1, e2])

    Then it can be used for sampling (or with simulation algorithms):

    >>> p = event.getSample(1000).computeMean()
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
        return _metamodel.UnionEvent_getClassName(self)

    def __repr__(self):
        return _metamodel.UnionEvent___repr__(self)

    def getDimension(self):
        """
        Accessor to the dimension of the RandomVector.

        Returns
        -------
        dimension : positive int
            Dimension of the RandomVector.
        """
        return _metamodel.UnionEvent_getDimension(self)

    def setEventCollection(self, collection):
        """
        Accessor to sub events.

        Parameters
        ----------
        events : sequence of :class:`~openturns.RandomVector`
            List of sub events.
        """
        return _metamodel.UnionEvent_setEventCollection(self, collection)

    def getEventCollection(self):
        """
        Accessor to sub events.

        Returns
        -------
        events : :class:`~openturns.RandomVectorCollection`
            List of sub events.
        """
        return _metamodel.UnionEvent_getEventCollection(self)

    def getRealization(self):
        """
        Compute one realization of the RandomVector.

        Returns
        -------
        aRealization : :class:`~openturns.Point`
            Sequence of values randomly determined from the RandomVector definition.
            In the case of an event: one realization of the event (considered as a
            Bernoulli variable) which is a boolean value (1 for the realization of the
            event and 0 else).

        See also
        --------
        getSample

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.0], [1.0, 1.0], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getRealization())
        [0.608202,-1.26617]
        >>> print(randomVector.getRealization())
        [-0.438266,1.20548]
        """
        return _metamodel.UnionEvent_getRealization(self)

    def isEvent(self):
        """
        Whether the random vector is an event.

        Returns
        -------
        isEvent : bool
            Whether it takes it values in {0, 1}.
        """
        return _metamodel.UnionEvent_isEvent(self)

    def isComposite(self):
        """
        Accessor to know if the RandomVector is a composite one.

        Returns
        -------
        isComposite : bool
            Indicates if the RandomVector is of type Composite or not.
        """
        return _metamodel.UnionEvent_isComposite(self)

    def getAntecedent(self):
        """
        Accessor to the antecedent random vector.

        Returns
        -------
        antecedent : :class:`~openturns.RandomVector`
            Defined as the root cause.
        """
        return _metamodel.UnionEvent_getAntecedent(self)

    def getFunction(self):
        """
        Accessor to the function.

        Returns
        -------
        function : :class:`~openturns.Function`
            Composed function.
        """
        return _metamodel.UnionEvent_getFunction(self)

    def getDomain(self):
        """
        Get the domain.

        Returns
        -------
        domain : :class:`~openturns.Domain`
            Composed domain.
        """
        return _metamodel.UnionEvent_getDomain(self)

    def getOperator(self):
        """
        Accessor to the comparaison operator of the Event.

        Returns
        -------
        operator : :class:`~openturns.ComparisonOperator`
            Comparaison operator used to define the :class:`~openturns.RandomVector`.
        """
        return _metamodel.UnionEvent_getOperator(self)

    def getThreshold(self):
        """
        Accessor to the threshold of the Event.

        Returns
        -------
        threshold : float
            Threshold of the :class:`~openturns.RandomVector`.
        """
        return _metamodel.UnionEvent_getThreshold(self)

    def getComposedEvent(self):
        """
        Accessor to the composed event.

        Returns
        -------
        composed : :class:`~openturns.RandomVector`
            Composed event.
        """
        return _metamodel.UnionEvent_getComposedEvent(self)

    def __init__(self, *args):
        _metamodel.UnionEvent_swiginit(self, _metamodel.new_UnionEvent(*args))

    __swig_destroy__ = _metamodel.delete_UnionEvent


_metamodel.UnionEvent_swigregister(UnionEvent)

class FunctionalChaosRandomVector(CompositeRandomVector):
    """
    Functional chaos random vector used to evaluate the Sobol indices.

    Available constructors:
        FunctionalChaosRandomVector(functionalChaosResult)

    Parameters
    ----------
    functionalChaosResult : :class:`~openturns.FunctionalChaosResult`
        A functional chaos result resulting from a polynomial chaos decomposition.

    See also
    --------
    FunctionalChaosAlgorithm, FunctionalChaosResult

    Notes
    -----
    This structure is created from a FunctionalChaosResult in order to evaluate the
    Sobol indices associated to the polynomial chaos decomposition of the model.

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
        return _metamodel.FunctionalChaosRandomVector_getClassName(self)

    def __repr__(self):
        return _metamodel.FunctionalChaosRandomVector___repr__(self)

    def getMean(self):
        """
        Accessor to the mean of the RandomVector.

        Returns
        -------
        mean : :class:`~openturns.Point`
            Mean of the considered :class:`~openturns.UsualRandomVector`.

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.5], [1.0, 1.5], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getMean())
        [0,0.5]
        """
        return _metamodel.FunctionalChaosRandomVector_getMean(self)

    def getCovariance(self):
        """
        Accessor to the covariance of the RandomVector.

        Returns
        -------
        covariance : :class:`~openturns.CovarianceMatrix`
            Covariance of the considered :class:`~openturns.UsualRandomVector`.

        Examples
        --------
        >>> import openturns as ot
        >>> distribution = ot.Normal([0.0, 0.5], [1.0, 1.5], ot.CorrelationMatrix(2))
        >>> randomVector = ot.RandomVector(distribution)
        >>> ot.RandomGenerator.SetSeed(0)
        >>> print(randomVector.getCovariance())
        [[ 1    0    ]
         [ 0    2.25 ]]
        """
        return _metamodel.FunctionalChaosRandomVector_getCovariance(self)

    def getFunctionalChaosResult(self):
        """
        Accessor to the functional chaos result.

        Returns
        -------
        functionalChaosResult : :class:`~openturns.FunctionalChaosResult`
            The functional chaos result resulting from a polynomial chaos decomposition.
        """
        return _metamodel.FunctionalChaosRandomVector_getFunctionalChaosResult(self)

    def __init__(self, *args):
        _metamodel.FunctionalChaosRandomVector_swiginit(self, _metamodel.new_FunctionalChaosRandomVector(*args))

    __swig_destroy__ = _metamodel.delete_FunctionalChaosRandomVector


_metamodel.FunctionalChaosRandomVector_swigregister(FunctionalChaosRandomVector)

class KrigingRandomVector(openturns.randomvector.UsualRandomVector):
    r"""
    KrigingRandom vector, a conditioned Gaussian process.

    Parameters
    ----------
    krigingResult : :class:`~openturns.KrigingResult`
        Structure that contains elements of computation of a kriging algorithm
    points : 1-d or 2-d sequence of float
        Sequence of values defining a :class:`~openturns.Point` or a :class:`~openturns.Sample`.

    Notes
    -----
    KrigingRandomVector helps to create Gaussian random vector, :math:`Y: \Rset^n \mapsto \Rset^d`, with stationary covariance function  :math:`\cC^{stat}: \Rset^n \mapsto \cM_{d \times d}(\Rset)`, conditionally to some observations.

    Let :math:`Y(x=x_1)=y_1,\cdots,Y(x=x_n)=y_n` be the observations of the Gaussian process. We assume the same Gaussian prior as in the :class:`~openturns.KrigingAlgorithm`:

    .. math::

        Y(\vect{x}) = \Tr{\vect{f}(\vect{x})} \vect{\beta} + Z(\vect{x})

    with :math:`\Tr{\vect{f}(\vect{x})} \vect{\beta}` a general linear model, :math:`Z(\vect{x})` a zero-mean Gaussian process with a stationary autocorrelation function :math:`\cC^{stat}`:

    .. math::

        \mathbb{E}[Z(\vect{x}), Z(\vect{\tilde{x}})] = \sigma^2 \cC^{stat}_{\theta}(\vect{x} - \vect{\tilde{x}})

    The objective is to generate realizations of the random vector :math:`Y`, on new points :math:`\vect{\tilde{x}}`, conditionally to these observations. For that purpose, :class:`~openturns.KrigingAlgorithm` build such a prior and stores results in a :class:`~openturns.KrigingResult` structure on a first step. This structure is given as input argument.

    Then, in a second step, both the prior and the covariance on input points :math:`\vect{\tilde{x}}`, conditionally to the previous observations, are evaluated (respectively :math:`Y(\vect{\tilde{x}})` and :math:`\cC^{stat}_{\theta}(\vect{\tilde{x}})`).

    Finally realizations are randomly generated by the Gaussian distribution :math:`\cN ( Y(\vect{\tilde{x}}), \cC^{stat}_{\theta}(\vect{\tilde{x}}) )`

    KrigingRandomVector class inherits from :class:`~openturns.UsualRandomVector`. Thus it stores the previous distribution and returns elements thanks to that distribution (realization, mean, covariance, sample...)

    Examples
    --------
    Create the model :math:`\cM: \Rset \mapsto \Rset` and the samples:

    >>> import openturns as ot
    >>> f = ot.SymbolicFunction(['x'],  ['x * sin(x)'])
    >>> sampleX = [[1.0], [2.0], [3.0], [4.0], [5.0], [6.0], [7.0], [8.0]]
    >>> sampleY = f(sampleX)

    Create the algorithm:

    >>> basis = ot.Basis([ot.SymbolicFunction(['x'], ['x']), ot.SymbolicFunction(['x'], ['x^2'])])
    >>> covarianceModel = ot.SquaredExponential([1.0])
    >>> covarianceModel.setActiveParameter([])
    >>> algo = ot.KrigingAlgorithm(sampleX, sampleY, covarianceModel, basis)
    >>> algo.run()

    Get the results:

    >>> result = algo.getResult()
    >>> rvector = ot.KrigingRandomVector(result, [[0.0]])

    Get a sample of the random vector:

    >>> sample = rvector.getSample(5)
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
        return _metamodel.KrigingRandomVector_getClassName(self)

    def __repr__(self):
        return _metamodel.KrigingRandomVector___repr__(self)

    def getRealization(self):
        """
        Compute a realization of the conditional Gaussian process (conditional on the learning set).

        The realization predicts the value on the given input *points*.

        Returns
        -------
        realization : :class:`~openturns.Point`
            Sequence of values of the Gaussian process.

        See also
        --------
        getSample
        """
        return _metamodel.KrigingRandomVector_getRealization(self)

    def getSample(self, *args):
        """
        Compute a sample of realizations of the conditional Gaussian process (conditional on the learning set).

        The realization predicts the value on the given input *points*.

        Returns
        -------
        realizations : :class:`~openturns.Sample`
            2-d float sequence of values of the Gaussian process.

        See also
        --------
        getRealization
        """
        return _metamodel.KrigingRandomVector_getSample(self, *args)

    def getKrigingResult(self):
        """
        Return the kriging result structure.

        Returns
        -------
        krigResult : :class:`~openturns.KrigingResult`
            The structure containing the elements of a KrigingAlgorithm.
        """
        return _metamodel.KrigingRandomVector_getKrigingResult(self)

    def __init__(self, *args):
        _metamodel.KrigingRandomVector_swiginit(self, _metamodel.new_KrigingRandomVector(*args))

    __swig_destroy__ = _metamodel.delete_KrigingRandomVector


_metamodel.KrigingRandomVector_swigregister(KrigingRandomVector)

class TensorApproximationResult(MetaModelResult):
    """
    Functional chaos result.

    Notes
    -----
    Structure created by the method run() of
    :class:`~openturns.TensorApproximationAlgorithm`, and obtained thanks to the method
    getResult().
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
        return _metamodel.TensorApproximationResult_getClassName(self)

    def __repr__(self):
        return _metamodel.TensorApproximationResult___repr__(self)

    def __str__(self, *args):
        return _metamodel.TensorApproximationResult___str__(self, *args)

    def getDistribution(self):
        r"""
        Get the input distribution.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Distribution of the  input random vector :math:`\vect{X}`.
        """
        return _metamodel.TensorApproximationResult_getDistribution(self)

    def getTransformation(self):
        r"""
        Get the isoprobabilistic transformation.

        Returns
        -------
        transformation : :class:`~openturns.Function`
            Transformation :math:`T` such that :math:`T(\vect{X}) = \vect{Z}`.
        """
        return _metamodel.TensorApproximationResult_getTransformation(self)

    def getInverseTransformation(self):
        r"""
        Get the inverse isoprobabilistic transformation.

        Returns
        -------
        invTransf : :class:`~openturns.Function`
             :math:`T^{-1}` such that :math:`T(\vect{X}) = \vect{Z}`.
        """
        return _metamodel.TensorApproximationResult_getInverseTransformation(self)

    def getComposedModel(self):
        r"""
        Get the composed model.

        Returns
        -------
        composedModel : :class:`~openturns.Function`
            :math:`f = g\circ T^{-1}`.
        """
        return _metamodel.TensorApproximationResult_getComposedModel(self)

    def getComposedMetaModel(self):
        r"""
        Get the composed metamodel.

        Returns
        -------
        composedMetamodel : :class:`~openturns.Function`
            :math:`\tilde{f} =  \sum_{k \in K} \vect{\alpha}_k \Psi_k`
        """
        return _metamodel.TensorApproximationResult_getComposedMetaModel(self)

    def getTensor(self, marginalIndex=0):
        """
        Accessor to the tensor.

        Parameters
        ----------
        marginalIndex : int
            Index of the marginal

        Returns
        -------
        tensor : :class:`~openturns.CanonicalTensorEvaluation`
            Tensor data.
        """
        return _metamodel.TensorApproximationResult_getTensor(self, marginalIndex)

    def __init__(self, *args):
        _metamodel.TensorApproximationResult_swiginit(self, _metamodel.new_TensorApproximationResult(*args))

    __swig_destroy__ = _metamodel.delete_TensorApproximationResult


_metamodel.TensorApproximationResult_swigregister(TensorApproximationResult)

class TensorApproximationAlgorithm(MetaModelAlgorithm):
    r"""
    Tensor approximation algorithm.

    Available constructors:
        TensorApproximationAlgorithm(*inputSample, outputSample, distribution, functionFactory, nk*)

    Parameters
    ----------
    inputSample, outputSample : 2-d sequence of float
        The input random variables :math:`\vect{X}=(X_1, \dots, X_{n_X})^T`
        and the output samples :math:`\vect{Y}` of a model evaluated apart.
    distribution : :class:`~openturns.Distribution`
        Joint probability density function :math:`f_{\vect{X}}(\vect{x})`
        of the physical input vector :math:`\vect{X}`.
    functionFactory : :class:`~openturns.OrthogonalProductFunctionFactory`
        The basis factory.
    degrees : sequence of int
        The size of the basis for each component
        Of size equal to the input dimension.
    maxRank : int, optional (default=1)
        The maximum rank

    See also
    --------
    FunctionalChaosAlgorithm, KrigingAlgorithm

    Notes
    -----
    TensorApproximationAlgorithm allows to perform a low-rank approximation in the canonical
    tensor format (refer to [rai2015]_ for other tensor formats and more details).

    The canonical tensor approximation of rank :math:`1` reads:

    .. math::

        f(X_1, \dots, X_d) = \prod_{j=1}^d v_j^{(1)} (x_j)

    The available alternating least-squares algorithm consists in successive approximations
    of the coefficients in the basis of the j-th component:

    .. math::

        v_j^{(i)} (x_j) = \sum_{k=1}^{n_j} \beta_{j,k}^{(i)} \phi_{j,k} (x_j)

    The full canonical tensor approximation of rank :math:`m` reads:

    .. math::

        f(X_1, \dots, X_d) = \sum_{i=1}^m \prod_{j=1}^d v_j^{(i)} (x_j)

    The decomposition algorithm can be tweaked using the key
    `TensorApproximationAlgorithm-DecompositionMethod`.

    Examples
    --------
    >>> import openturns as ot
    >>> dim = 1
    >>> f = ot.SymbolicFunction(['x'], ['x*sin(x)'])
    >>> uniform = ot.Uniform(0.0, 10.0)
    >>> distribution = ot.ComposedDistribution([uniform]*dim)
    >>> factoryCollection = [ot.OrthogonalUniVariateFunctionFamily(ot.OrthogonalUniVariatePolynomialFunctionFactory(ot.StandardDistributionPolynomialFactory(uniform)))] * dim
    >>> functionFactory = ot.OrthogonalProductFunctionFactory(factoryCollection)
    >>> size = 10
    >>> sampleX = [[1.0], [2.0], [3.0], [4.0], [5.0], [6.0], [7.0], [8.0]]
    >>> sampleY = f(sampleX)
    >>> nk = [5] * dim
    >>> maxRank = 1
    >>> algo = ot.TensorApproximationAlgorithm(sampleX, sampleY, distribution, functionFactory, nk, maxRank)
    >>> algo.run()

    Get the resulting meta model:

    result = algo.getResult()
    metamodel = result.getMetaModel()
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
        return _metamodel.TensorApproximationAlgorithm_getClassName(self)

    def __repr__(self):
        return _metamodel.TensorApproximationAlgorithm___repr__(self)

    def run(self):
        """Compute the response surface."""
        return _metamodel.TensorApproximationAlgorithm_run(self)

    def getResult(self):
        """
        Result accessor.

        Returns
        -------
        result : :class:`~openturns.TensorApproximationResult`
            The result of the approximation.
        """
        return _metamodel.TensorApproximationAlgorithm_getResult(self)

    def getInputSample(self):
        """
        Accessor to the input sample.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            Input sample of a model evaluated apart.
        """
        return _metamodel.TensorApproximationAlgorithm_getInputSample(self)

    def getOutputSample(self):
        """
        Accessor to the output sample.

        Returns
        -------
        outputSample : :class:`~openturns.Sample`
            Output sample of a model evaluated apart.
        """
        return _metamodel.TensorApproximationAlgorithm_getOutputSample(self)

    def setMaximumAlternatingLeastSquaresIteration(self, maximumAlternatingLeastSquaresIteration):
        """
        Maximum ALS algorithm iteration accessor.

        Parameters
        ----------
        maxALSIteration : int
            The maximum number of iterations for the alternating least-squares
            algorithm used for the rank-1 approximation.
        """
        return _metamodel.TensorApproximationAlgorithm_setMaximumAlternatingLeastSquaresIteration(self, maximumAlternatingLeastSquaresIteration)

    def getMaximumAlternatingLeastSquaresIteration(self):
        """
        Maximum ALS algorithm iteration accessor.

        Returns
        -------
        maxALSIteration : int
            The maximum number of iterations for the alternating least-squares
            algorithm used for the rank-1 approximation.
        """
        return _metamodel.TensorApproximationAlgorithm_getMaximumAlternatingLeastSquaresIteration(self)

    def setMaximumRadiusError(self, maximumRadiusError):
        """
        Maximum radius error accessor.

        Parameters
        ----------
        maxRadiusError : float
            Convergence criterion on the radius during alternating least-squares
            algorithm used for the rank-1 approximation.
        """
        return _metamodel.TensorApproximationAlgorithm_setMaximumRadiusError(self, maximumRadiusError)

    def getMaximumRadiusError(self):
        """
        Maximum radius error accessor.

        Returns
        -------
        maxRadiusError : float
            Convergence criterion on the radius during alternating least-squares
            algorithm used for the rank-1 approximation.
        """
        return _metamodel.TensorApproximationAlgorithm_getMaximumRadiusError(self)

    def setMaximumResidualError(self, maximumResidualError):
        """
        Maximum residual error accessor.

        Parameters
        ----------
        maxResErr : float
            Convergence criterion on the residual during alternating least-squares
            algorithm used for the rank-1 approximation.
        """
        return _metamodel.TensorApproximationAlgorithm_setMaximumResidualError(self, maximumResidualError)

    def getMaximumResidualError(self):
        """
        Maximum residual error accessor.

        Returns
        -------
        maxResErr : float
            Convergence criterion on the residual during alternating least-squares
            algorithm used for the rank-1 approximation.
        """
        return _metamodel.TensorApproximationAlgorithm_getMaximumResidualError(self)

    def __init__(self, *args):
        _metamodel.TensorApproximationAlgorithm_swiginit(self, _metamodel.new_TensorApproximationAlgorithm(*args))

    __swig_destroy__ = _metamodel.delete_TensorApproximationAlgorithm


_metamodel.TensorApproximationAlgorithm_swigregister(TensorApproximationAlgorithm)