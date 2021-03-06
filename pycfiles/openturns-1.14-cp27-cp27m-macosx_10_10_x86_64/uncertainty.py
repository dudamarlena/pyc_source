# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lib/python2.7/site-packages/openturns/uncertainty.py
# Compiled at: 2019-11-13 10:36:39
"""Probabilistic meta-package."""
from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')
if __package__ or '.' in __name__:
    from . import _uncertainty
else:
    import _uncertainty
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
    __swig_destroy__ = _uncertainty.delete_SwigPyIterator

    def value(self):
        return _uncertainty.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _uncertainty.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _uncertainty.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _uncertainty.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _uncertainty.SwigPyIterator_equal(self, x)

    def copy(self):
        return _uncertainty.SwigPyIterator_copy(self)

    def next(self):
        return _uncertainty.SwigPyIterator_next(self)

    def __next__(self):
        return _uncertainty.SwigPyIterator___next__(self)

    def previous(self):
        return _uncertainty.SwigPyIterator_previous(self)

    def advance(self, n):
        return _uncertainty.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _uncertainty.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _uncertainty.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _uncertainty.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _uncertainty.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _uncertainty.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _uncertainty.SwigPyIterator___sub__(self, *args)

    def __iter__(self):
        return self


_uncertainty.SwigPyIterator_swigregister(SwigPyIterator)

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


import openturns.base, openturns.common, openturns.typ, openturns.statistics, openturns.graph, openturns.func, openturns.geom, openturns.diff, openturns.optim, openturns.experiment, openturns.solver, openturns.algo, openturns.model_copula, openturns.randomvector, openturns.dist_bundle1, openturns.dist_bundle2, openturns.weightedexperiment, openturns.classification, openturns.orthogonalbasis, openturns.metamodel

class TaylorExpansionMoments(openturns.common.PersistentObject):
    r"""
    First and second order Taylor expansion formulas.

    Refer to :ref:`taylor_importance_factors`.

    Parameters
    ----------
    limitStateVariable : :class:`~openturns.RandomVector`
        It must be of type *Composite*, which means it must have
        been defined with the class :class:`~openturns.CompositeRandomVector`.

    Notes
    -----
    In a probabilistic approach the Taylor expansion can be used
    propagate the uncertainties of the input variables :math:`\uX` through the
    model :math:`h` towards the output variables :math:`\uY`. It enables to access
    the central dispersion (Expectation, Variance) of the output variables.

    This method is based on a Taylor decomposition of the output variable
    :math:`\uY` towards the :math:`\uX` random vectors around the mean point
    :math:`\muX`. Depending on the order of the Taylor decomposition (classically
    first order or second order), one can obtain different formulas introduced
    hereafter.

    As :math:`\uY=h(\uX)`, the Taylor decomposition around :math:`\ux = \muX` at
    the second order yields to:

    .. math::

        \uY = h(\muX) + <\vect{\vect{\nabla}}h(\muX) , \: \uX - \muX> + \frac{1}{2}<<\vect{\vect{\vect{\nabla }}}^2 h(\muX,\: \vect{\mu}_{\:X}),\: \uX - \muX>,\: \uX - \muX> + o(\Cov \uX)

    where:

    - :math:`\muX = \Expect{\uX}` is the vector of the input variables at the mean
      values of each component.

    - :math:`\Cov \uX` is the covariance matrix of the random vector `\uX`. The
      elements are the followings :
      :math:`(\Cov \uX)_{ij} = \Expect{\left(X^i - \Expect{X^i} \right)^2}`

    - :math:`\vect{\vect{\nabla}} h(\muX) = \: \Tr{\left( \frac{\partial y^i}{\partial x^j}\right)}_{\ux\: =\: \muX} = \: \Tr{\left( \frac{\partial h^i(\ux)}{\partial x^j}\right)}_{\ux\: =\: \muX}`
      is the transposed Jacobian matrix with :math:`i=1,\ldots,n_Y` and
      :math:`j=1,\ldots,n_X`.

    - :math:`\vect{\vect{\vect{\nabla^2}}} h(\ux\:,\ux)` is a tensor of order 3. It
      is composed by the second order derivative towards the :math:`i^\textrm{th}`
      and :math:`j^\textrm{th}` components of :math:`\ux` of the
      :math:`k^\textrm{th}` component of the output vector :math:`h(\ux)`. It
      yields to:
      :math:`\left( \nabla^2 h(\ux) \right)_{ijk} = \frac{\partial^2 (h^k(\ux))}{\partial x^i \partial x^j}`

    - :math:`<\vect{\vect{\nabla}}h(\muX) , \: \uX - \muX> = \sum_{j=1}^{n_X} \left( \frac{\partial {\uy}}{\partial {x^j}}\right)_{\ux = \muX} . \left( X^j-\muX^j \right)`

    -
      .. math::

          <<\vect{\vect{\vect{\nabla }}}^2 h(\muX,\: \vect{\mu}_{X}),\: \uX - \muX>,\: \uX - \muX> = \left( \Tr{(\uX^i - \muX^i)}. \left(\frac{\partial^2 y^k}{\partial x^i \partial x^k}\right)_{\ux = \muX}. (\uX^j - \muX^j) \right)_{ijk}

    **Approximation at the order 1:**

    Expectation:

    .. math::

        \Expect{\uY} \approx \vect{h}(\muX)

    Pay attention that :math:`\Expect{\uY}` is a vector. The :math:`k^\textrm{th}`
    component of this vector is equal to the :math:`k^\textrm{th}` component of the
    output vector computed by the model :math:`h` at the mean value.
    :math:`\Expect{\uY}` is thus the computation of the model at mean.

    Variance:

    .. math::

        \Cov \uY \approx \Tr{\vect{\vect{\nabla}}}\:\vect{h}(\muX).\Cov \uX.\vect{\vect{\nabla}}\:\vect{h}(\muX)

    **Approximation at the order 2:**

    Expectation:

    .. math::

        (\Expect{\uY})_k \approx (\vect{h}(\muX))_k +
                                  \left(
                                  \sum_{i=1}^{n_X}\frac{1}{2} (\Cov \uX)_{ii}.{(\nabla^2\:h(\uX))}_{iik} +
                                  \sum_{i=1}^{n_X} \sum_{j=1}^{i-1} (\Cov X)_{ij}.{(\nabla^2\:h(\uX))}_{ijk}
                                  \right)_k

    Variance:

    The decomposition of the variance at the order 2 is not implemented.
    It requires both the knowledge of higher order derivatives of the model and the
    knowledge of moments of order strictly greater than 2 of the PDF.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> myFunc = ot.SymbolicFunction(['x1', 'x2', 'x3', 'x4'],
    ...     ['(x1*x1+x2^3*x1)/(2*x3*x3+x4^4+1)', 'cos(x2*x2+x4)/(x1*x1+1+x3^4)'])
    >>> R = ot.CorrelationMatrix(4)
    >>> for i in range(4):
    ...     R[i, i - 1] = 0.25
    >>> distribution = ot.Normal([0.2]*4, [0.1, 0.2, 0.3, 0.4], R)
    >>> # We create a distribution-based RandomVector
    >>> X = ot.RandomVector(distribution)
    >>> # We create a composite RandomVector Y from X and myFunc
    >>> Y = ot.CompositeRandomVector(myFunc, X)
    >>> # We create a Taylor expansion method to approximate moments
    >>> myTaylorExpansionMoments = ot.TaylorExpansionMoments(Y)
    >>> print(myTaylorExpansionMoments.getMeanFirstOrder())
    [0.0384615,0.932544]
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
        return _uncertainty.TaylorExpansionMoments_getClassName(self)

    def __repr__(self):
        return _uncertainty.TaylorExpansionMoments___repr__(self)

    def getLimitStateVariable(self):
        """
        Get the limit state variable.

        Returns
        -------
        limitStateVariable : :class:`~openturns.RandomVector`
            Limit state variable.
        """
        return _uncertainty.TaylorExpansionMoments_getLimitStateVariable(self)

    def getMeanFirstOrder(self):
        """
        Get the approximation at the first order of the mean.

        Returns
        -------
        mean : :class:`~openturns.Point`
            Approximation at the first order of the mean of the random vector.
        """
        return _uncertainty.TaylorExpansionMoments_getMeanFirstOrder(self)

    def getMeanSecondOrder(self):
        """
        Get the approximation at the second order of the mean.

        Returns
        -------
        mean : :class:`~openturns.Point`
            Approximation at the second order of the mean of the random vector
            (it requires that the hessian of the Function has been defined).
        """
        return _uncertainty.TaylorExpansionMoments_getMeanSecondOrder(self)

    def getCovariance(self):
        """
        Get the approximation at the first order of the covariance matrix.

        Returns
        -------
        covariance : :class:`~openturns.CovarianceMatrix`
            Approximation at the first order of the covariance matrix of the random
            vector.
        """
        return _uncertainty.TaylorExpansionMoments_getCovariance(self)

    def getValueAtMean(self):
        """
        Get the value of the function.

        Returns
        -------
        value : :class:`~openturns.Point`
            Value of the Function which defines the random vector at
            the mean point of the input random vector.
        """
        return _uncertainty.TaylorExpansionMoments_getValueAtMean(self)

    def getGradientAtMean(self):
        """
        Get the gradient of the function.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            Gradient of the Function which defines the random vector at
            the mean point of the input random vector.
        """
        return _uncertainty.TaylorExpansionMoments_getGradientAtMean(self)

    def getHessianAtMean(self):
        """
        Get the hessian of the function.

        Returns
        -------
        hessian : :class:`~openturns.SymmetricTensor`
            Hessian of the Function which defines the random vector at
            the mean point of the input random vector.
        """
        return _uncertainty.TaylorExpansionMoments_getHessianAtMean(self)

    def getImportanceFactors(self):
        """
        Get the importance factors.

        Returns
        -------
        factors : :class:`~openturns.Point`
            Importance factors of the inputs : only when randVect is of dimension 1.
        """
        return _uncertainty.TaylorExpansionMoments_getImportanceFactors(self)

    def drawImportanceFactors(self):
        """
        Draw the importance factors.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            Graph containing the pie corresponding to the importance factors of the
            probabilistic variables.
        """
        return _uncertainty.TaylorExpansionMoments_drawImportanceFactors(self)

    def __init__(self, *args):
        _uncertainty.TaylorExpansionMoments_swiginit(self, _uncertainty.new_TaylorExpansionMoments(*args))

    __swig_destroy__ = _uncertainty.delete_TaylorExpansionMoments


_uncertainty.TaylorExpansionMoments_swigregister(TaylorExpansionMoments)

class EfficientGlobalOptimization(openturns.optim.OptimizationAlgorithmImplementation):
    r"""
    Efficient Global Optimization algorithm.

    The EGO algorithm [jones1998]_ is an adaptative optimization method based on
    kriging.
    An initial design of experiment is used to build a first metamodel.
    At each iteration a new point that maximizes a criterion is chosen as
    optimizer candidate.
    The criterion uses a tradeoff between the metamodel value and the conditional
    variance.
    Then the new point is evaluated using the original model and the metamodel is
    relearnt on the extended design of experiment.

    Available constructors:
        EfficientGlobalOptimization(*problem, krigingResult*)

    Parameters
    ----------
    problem : :class:`~openturns.OptimizationProblem`
        The optimization problem to solve
        optionally, a 2nd objective marginal can be used as noise
    krigingResult : :class:`~openturns.KrigingResult`
        The result of the meta-model on the first design of experiment

    Notes
    -----
    Each point added to the metamodel design seeks to improve the current minimum.
    We chose the point so as to maximize an improvement criterion based on the
    metamodel.

    .. math::

        I(x_{new}) = max(f_{min} - Y_{new}, 0)

    The default criteria is called EI (Expected Improvement) and aims at maximizing
    the mean improvement:

    .. math::

        \mathbb{E}\left[I(x_{new})\right] = \mathbb{E}\left[max(f_{min} - Y_{new}, 0)\right]

    This criterion is explicited using the kriging mean and variance:

    .. math::

        \mathbb{E}\left[I(x_{new})\right] = (f_{min} - m_K(x_{new})) \Phi\left( \frac{f_{min} - m_K(x_{new})}{s_K(x_{new})} \right) + s_K(x_{new}) \phi\left( \frac{f_{min} - m_K(x_{new})}{s_K(x_{new})} \right)

    An observation noise variance can be provided thanks to a 2nd objective marginal.

    .. math:: Y_{obs} = Y(x) + \sigma_{\epsilon}(x) \epsilon

    In that case the AEI (Augmented Expected Improvement) formulation is used.
    As we don't have access to the real minimum of the function anymore a quantile
    of the kriging prediction is used, with the constant :math:`c`:

    .. math:: u(x) = m_K(x) + c s_K(x)

    This criterion is minimized over the design points:

    .. math:: x_{min} = \argmax_{x_i} (u(x_i))

    The AEI criterion reads:

    .. math::

        AEI(x_{new}) = \mathbb{E}\left[max(m_K(x_{min}) - Y_{new}, 0)\right] \times \left(1 - \frac{\sigma_{\epsilon}(x_{new})}{\sqrt{\sigma_{\epsilon}^2(x_{new})+s^2_K(x_{new})}} \right)

    with

    .. math::

        \mathbb{E}\left[max(m_K(x_{min}) - Y_{new}, 0)\right] = (m_K(x_{min}) - m_K(x_{new})) \Phi\left( \frac{m_K(x_{min}) - m_K(x_{new})}{s_K(x_{new})} \right) + s_K(x_{new}) \phi\left( \frac{m_K(x_{min}) - m_K(x_{new})}{s_K(x_{new})} \right)

    A less computationally expensive noise function can be provided through
    :func:`setNoiseModel()` to evaluate :math:`\sigma^2_{\epsilon}(x)`
    for the improvement criterion optimization, the objective being only used to
    compute values and associated noise at design points.

    By default the criteria is minimized using :class:`~openturns.MultiStart`
    with starting points uniformly sampled in the optimization problem bounds,
    see :func:`setMultiStartExperimentSize` and :func:`setMultiStartNumber`.
    This behavior can be overridden by using another solver with :func:`setOptimizationAlgorithm`.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> dim = 4
    >>> model = ot.SymbolicFunction(['x1', 'x2', 'x3', 'x4'],
    ...     ['x1*x1+x2^3*x1+x3+x4'])
    >>> model = ot.MemoizeFunction(model)
    >>> bounds = ot.Interval([-5.0] * dim, [5.0] * dim)
    >>> problem = ot.OptimizationProblem()
    >>> problem.setObjective(model)
    >>> problem.setBounds(bounds)
    >>> experiment = ot.Composite([0.0] * dim, [1.0, 2.0, 4.0])
    >>> inputSample = experiment.generate()
    >>> outputSample = model(inputSample)
    >>> covarianceModel = ot.SquaredExponential([2.0] * dim, [0.1])
    >>> basis = ot.ConstantBasisFactory(dim).build()
    >>> kriging = ot.KrigingAlgorithm(inputSample, outputSample, covarianceModel, basis)
    >>> kriging.run()
    >>> algo = ot.EfficientGlobalOptimization(problem, kriging.getResult())
    >>> algo.setMaximumEvaluationNumber(2)
    >>> algo.run()
    >>> result = algo.getResult()
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
        return _uncertainty.EfficientGlobalOptimization_getClassName(self)

    def __repr__(self):
        return _uncertainty.EfficientGlobalOptimization___repr__(self)

    def run(self):
        """Launch the optimization."""
        return _uncertainty.EfficientGlobalOptimization_run(self)

    def setOptimizationAlgorithm(self, solver):
        """
        Expected improvement solver accessor.

        Parameters
        ----------
        solver : :class:`~openturns.OptimizationSolver`
            The solver used to optimize the expected improvement
        """
        return _uncertainty.EfficientGlobalOptimization_setOptimizationAlgorithm(self, solver)

    def getOptimizationAlgorithm(self):
        """
        Expected improvement solver accessor.

        Returns
        -------
        solver : :class:`~openturns.OptimizationSolver`
            The solver used to optimize the expected improvement
        """
        return _uncertainty.EfficientGlobalOptimization_getOptimizationAlgorithm(self)

    def getMultiStartExperimentSize(self):
        """
        Size of the design to draw starting points.

        Returns
        -------
        multiStartExperimentSize : int
            The size of the Monte Carlo design from which to select the best starting
            points.
        """
        return _uncertainty.EfficientGlobalOptimization_getMultiStartExperimentSize(self)

    def setMultiStartExperimentSize(self, multiStartExperimentSize):
        """
        Size of the design to draw starting points.

        Parameters
        ----------
        multiStartExperimentSize : int
            The size of the Monte Carlo design from which to select the best starting
            points.
            The default number can be tweaked with the
            `EfficientGlobalOptimization-DefaultMultiStartExperimentSize` key from
            :class:`~openturns.ResourceMap`.
        """
        return _uncertainty.EfficientGlobalOptimization_setMultiStartExperimentSize(self, multiStartExperimentSize)

    def getMultiStartNumber(self):
        """
        Number of starting points for the criterion optimization.

        Returns
        -------
        multiStartNumber : int
            The number of starting points for the criterion optimization.
        """
        return _uncertainty.EfficientGlobalOptimization_getMultiStartNumber(self)

    def setMultiStartNumber(self, multiStartNumberSize):
        """
        Number of starting points for the criterion optimization.

        Parameters
        ----------
        multiStartNumber : int
            The number of starting points for the criterion optimization.
            The default number can be tweaked with the
            `EfficientGlobalOptimization-DefaultMultiStartNumber` key from
            :class:`~openturns.ResourceMap`.
        """
        return _uncertainty.EfficientGlobalOptimization_setMultiStartNumber(self, multiStartNumberSize)

    def getParameterEstimationPeriod(self):
        """
        Parameter estimation period accessor.

        Returns
        -------
        period : int
            The number of iterations between covariance parameters re-learn.
            Default is 1 (each iteration). Can be set to 0 (never).
        """
        return _uncertainty.EfficientGlobalOptimization_getParameterEstimationPeriod(self)

    def setParameterEstimationPeriod(self, parameterEstimationPeriod):
        """
        Parameter estimation period accessor.

        Parameters
        ----------
        period : int
            The number of iterations between covariance parameters re-learn.
            Default is 1 (each iteration). Can be set to 0 (never).
            The default number can be tweaked with the
            `EfficientGlobalOptimization-DefaultParameterEstimationPeriod` key from
            :class:`~openturns.ResourceMap`.
        """
        return _uncertainty.EfficientGlobalOptimization_setParameterEstimationPeriod(self, parameterEstimationPeriod)

    def setImprovementFactor(self, improvementFactor):
        r"""
        Improvement criterion factor accessor.

        Parameters
        ----------
        a : float
            Used to define a stopping criterion on the improvement criterion:
            :math:`I_{max} < \alpha |Y_{min}|`
            with :math:`I_{max}` the current maximum of the improvement
            and :math:`Y_{min}` the current optimum.
        """
        return _uncertainty.EfficientGlobalOptimization_setImprovementFactor(self, improvementFactor)

    def getImprovementFactor(self):
        r"""
        Improvement criterion factor accessor.

        Returns
        -------
        a : float
            Used to define a stopping criterion on the improvement criterion:
            :math:`I_{max} < \alpha |Y_{min}|`
            with :math:`I_{max}` the current maximum of the improvement
            and :math:`Y_{min}` the current optimum.
        """
        return _uncertainty.EfficientGlobalOptimization_getImprovementFactor(self)

    def setCorrelationLengthFactor(self, b):
        r"""
        Correlation length stopping criterion factor accessor.

        When a correlation length becomes smaller than the minimal distance between
        design point for a single component that means the model tends to be noisy,
        and the EGO formulation is not adapted anymore.

        Parameters
        ----------
        b : float
            Used to define a stopping criterion on the minimum correlation length:
            :math:`\theta_i < \frac{\Delta_i^{min}}{b}`
            with :math:`\Delta^{min}` the minimum distance between design points.
        """
        return _uncertainty.EfficientGlobalOptimization_setCorrelationLengthFactor(self, b)

    def getCorrelationLengthFactor(self):
        r"""
        Correlation length stopping criterion factor accessor.

        When a correlation length becomes smaller than the minimal distance between
        design point for a single component that means the model tends to be noisy,
        and the EGO formulation is not adapted anymore.

        Returns
        -------
        b : float
            Used to define a stopping criterion on the minimum correlation length:
            :math:`\theta_i < \frac{\Delta_i^{min}}{b}`
            with :math:`\Delta^{min}` the minimum distance between design points.
        """
        return _uncertainty.EfficientGlobalOptimization_getCorrelationLengthFactor(self)

    def setAEITradeoff(self, c):
        """
        AEI tradeoff constant accessor.

        Parameters
        ----------
        c : float
            Used to define a quantile of the kriging prediction at the design points.
            :math:`u(x)=m_K(x)+c*s_K(x)`
        """
        return _uncertainty.EfficientGlobalOptimization_setAEITradeoff(self, c)

    def getAEITradeoff(self):
        """
        AEI tradeoff constant accessor.

        Returns
        -------
        c : float
            Used to define a quantile of the kriging prediction at the design points.
            :math:`u(x)=m_K(x)+c*s_K(x)`
        """
        return _uncertainty.EfficientGlobalOptimization_getAEITradeoff(self)

    def setNoiseModel(self, noiseModel):
        r"""
        Improvement noise model accessor.

        Parameters
        ----------
        noiseVariance : :class:`~openturns.Function`
            The noise variance :math:`\sigma^2_{\epsilon}(x)` used for the AEI
            criterion optimization only.
            Of same input dimension than the objective and 1-d output.
        """
        return _uncertainty.EfficientGlobalOptimization_setNoiseModel(self, noiseModel)

    def getNoiseModel(self):
        r"""
        Improvement noise model accessor.

        Returns
        -------
        noiseVariance : :class:`~openturns.Function`
            The noise variance :math:`\sigma^2_{\epsilon}(x)` used for the AEI
            criterion optimization only.
            Of same input dimension than the objective and 1-d output.
        """
        return _uncertainty.EfficientGlobalOptimization_getNoiseModel(self)

    def getExpectedImprovement(self):
        """
        Expected improvement values.

        Returns
        -------
        ei : :class:`~openturns.Sample`
            The expected improvement optimal values.
        """
        return _uncertainty.EfficientGlobalOptimization_getExpectedImprovement(self)

    def __init__(self, *args):
        _uncertainty.EfficientGlobalOptimization_swiginit(self, _uncertainty.new_EfficientGlobalOptimization(*args))

    __swig_destroy__ = _uncertainty.delete_EfficientGlobalOptimization


_uncertainty.EfficientGlobalOptimization_swigregister(EfficientGlobalOptimization)
import openturns.transformation, openturns.analytical, openturns.simulation, openturns.stattests, openturns.model_process