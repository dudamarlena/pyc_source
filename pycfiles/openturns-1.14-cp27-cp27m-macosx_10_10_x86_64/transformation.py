# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lib/python2.7/site-packages/openturns/transformation.py
# Compiled at: 2019-11-13 10:35:04
"""Transformations."""
from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')
if __package__ or '.' in __name__:
    from . import _transformation
else:
    import _transformation
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
    __swig_destroy__ = _transformation.delete_SwigPyIterator

    def value(self):
        return _transformation.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _transformation.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _transformation.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _transformation.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _transformation.SwigPyIterator_equal(self, x)

    def copy(self):
        return _transformation.SwigPyIterator_copy(self)

    def next(self):
        return _transformation.SwigPyIterator_next(self)

    def __next__(self):
        return _transformation.SwigPyIterator___next__(self)

    def previous(self):
        return _transformation.SwigPyIterator_previous(self)

    def advance(self, n):
        return _transformation.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _transformation.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _transformation.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _transformation.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _transformation.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _transformation.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _transformation.SwigPyIterator___sub__(self, *args)

    def __iter__(self):
        return self


_transformation.SwigPyIterator_swigregister(SwigPyIterator)

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

class MarginalTransformationEvaluation(openturns.func.EvaluationImplementation):
    r"""
    Marginal transformation evaluation.

    Available constructors:
        MarginalTransformationEvaluation(*distCol*)

        MarginalTransformationEvaluation(*distCol, direction, standardMarginal*)

        MarginalTransformationEvaluation(*distCol, outputDistCol*)

    Parameters
    ----------
    distCol : :class:`~openturns.DistributionCollection`
        A collection of distributions.
    direction : integer
        Flag for the direction of the transformation, either integer or 
        *MarginalTransformationEvaluation.FROM* (associated to the integer 0) or 
        *MarginalTransformationEvaluation.TO* (associated to the integer 1).
        Default is 0.
    standardMarginal : :class:`~openturns.Distribution`
        Target distribution marginal
        Default is Uniform(0, 1)
    outputDistCol : :class:`~openturns.DistributionCollection`
        A collection of distributions.

    Notes
    -----
    This class contains a :class:`~openturns.Function` which can be
    evaluated in one point but which proposes no gradient nor hessian implementation.

    - In the two first usage, if :math:`direction = 0`, the created operator
      transforms a :class:`~openturns.Point` into its rank according to the
      marginal distributions described in *distCol*. Let
      :math:`(F_{X_1}, \ldots, F_{X_n})` be the CDF of the distributions contained
      in *distCol*, then the created operator works as follows:

      .. math::

          (x_1, \ldots, x_n) \rightarrow (F_{X_1}(x_1), \ldots, F_{X_n}(x_n))

      If :math:`direction = 1`, the created operator works in the opposite direction:

      .. math::

          (x_1, \ldots, x_n) \rightarrow (F^{-1}_{X_1}(x_1), \ldots, F^{-1}_{X_n}(x_n))

      In that case, it requires that all the values :math:`x_i` be in :math:`[0, 1]`.

    - In the third usage, the created operator transforms a
      :class:`~openturns.Point` into the following one, where *outputDistCol*
      contains the :math:`(F_{Y_1}, \ldots, F_{Y_n})` distributions:

      .. math::

          (x_1, \ldots, x_n) \rightarrow (F^{-1}_{Y_1} \circ F_{X_1}(x_1), \ldots, F^{-1}_{Y_n} \circ F_{X_n}(x_n))

    Examples
    --------
    >>> import openturns as ot
    >>> distCol = [ot.Normal(), ot.LogNormal()]
    >>> margTransEval = ot.MarginalTransformationEvaluation(distCol, 0)
    >>> print(margTransEval([1, 3]))
    [0.841345,0.864031]
    >>> margTransEvalInverse = ot.MarginalTransformationEvaluation(distCol, 1)
    >>> print(margTransEvalInverse([0.84, 0.86]))
    [0.994458,2.94562]
    >>> outputDistCol = [ot.WeibullMin(), ot.Exponential()]
    >>> margTransEvalComposed = ot.MarginalTransformationEvaluation(distCol, outputDistCol)
    >>> print(margTransEvalComposed([1, 3]))
    [1.84102,1.99533]

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
        return _transformation.MarginalTransformationEvaluation_getClassName(self)

    FROM = _transformation.MarginalTransformationEvaluation_FROM
    TO = _transformation.MarginalTransformationEvaluation_TO

    def __call__(self, *args):
        return _transformation.MarginalTransformationEvaluation___call__(self, *args)

    def parameterGradient(self, inP):
        """
        Gradient against the parameters.

        Parameters
        ----------
        x : sequence of float
            Input point

        Returns
        -------
        parameter_gradient : :class:`~openturns.Matrix`
            The parameters gradient computed at x.
        """
        return _transformation.MarginalTransformationEvaluation_parameterGradient(self, inP)

    def setParameter(self, parameter):
        """
        Accessor to the parameter values.

        Parameters
        ----------
        parameter : sequence of float
            The parameter values.
        """
        return _transformation.MarginalTransformationEvaluation_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter values.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            The parameter values.
        """
        return _transformation.MarginalTransformationEvaluation_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description.

        Returns
        -------
        parameter : :class:`~openturns.Description`
            The parameter description.
        """
        return _transformation.MarginalTransformationEvaluation_getParameterDescription(self)

    def setParameterDescription(self, description):
        """
        Accessor to the parameter description.

        Parameters
        ----------
        parameter : :class:`~openturns.Description`
            The parameter description.
        """
        return _transformation.MarginalTransformationEvaluation_setParameterDescription(self, description)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getInputDimension())
        2
        """
        return _transformation.MarginalTransformationEvaluation_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getOutputDimension())
        1
        """
        return _transformation.MarginalTransformationEvaluation_getOutputDimension(self)

    def setInputDistributionCollection(self, inputDistributionCollection):
        """
        Accessor to the input distribution collection.

        Parameters
        ----------
        inputDistCol : :class:`~openturns.DistributionCollection`
            The input distribution collection.
        """
        return _transformation.MarginalTransformationEvaluation_setInputDistributionCollection(self, inputDistributionCollection)

    def getInputDistributionCollection(self):
        """
        Accessor to the input distribution collection.

        Returns
        -------
        inputDistCol : :class:`~openturns.DistributionCollection`
            The input distribution collection.
        """
        return _transformation.MarginalTransformationEvaluation_getInputDistributionCollection(self)

    def setOutputDistributionCollection(self, outputDistributionCollection):
        """
        Accessor to the output distribution collection.

        Parameters
        ----------
        outputDistCol : :class:`~openturns.DistributionCollection`
            The output distribution collection.
        """
        return _transformation.MarginalTransformationEvaluation_setOutputDistributionCollection(self, outputDistributionCollection)

    def getOutputDistributionCollection(self):
        """
        Accessor to the output distribution collection.

        Returns
        -------
        outputDistCol : :class:`~openturns.DistributionCollection`
            The output distribution collection.
        """
        return _transformation.MarginalTransformationEvaluation_getOutputDistributionCollection(self)

    def getSimplifications(self):
        """Try to simplify the transformations if it is possible."""
        return _transformation.MarginalTransformationEvaluation_getSimplifications(self)

    def getExpressions(self):
        """
        Accessor to the numerical math function.

        Returns
        -------
        listFunction : :class:`~openturns.FunctionCollection`
            The collection of numerical math functions if the analytical expressions 
            exist.
        """
        return _transformation.MarginalTransformationEvaluation_getExpressions(self)

    def __repr__(self):
        return _transformation.MarginalTransformationEvaluation___repr__(self)

    def __str__(self, *args):
        return _transformation.MarginalTransformationEvaluation___str__(self, *args)

    def __init__(self, *args):
        _transformation.MarginalTransformationEvaluation_swiginit(self, _transformation.new_MarginalTransformationEvaluation(*args))

    __swig_destroy__ = _transformation.delete_MarginalTransformationEvaluation


_transformation.MarginalTransformationEvaluation_swigregister(MarginalTransformationEvaluation)

class MarginalTransformationGradient(openturns.func.GradientImplementation):
    """Proxy of C++ OT::MarginalTransformationGradient."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.MarginalTransformationGradient_getClassName(self)

    def gradient(self, inP):
        """
        Return the Jacobian transposed matrix of the implementation at a point.

        Parameters
        ----------
        point : sequence of float
            Point where the Jacobian transposed matrix is calculated.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The Jacobian transposed matrix of the function at *point*.
        """
        return _transformation.MarginalTransformationGradient_gradient(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.
        """
        return _transformation.MarginalTransformationGradient_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.
        """
        return _transformation.MarginalTransformationGradient_getOutputDimension(self)

    def __repr__(self):
        return _transformation.MarginalTransformationGradient___repr__(self)

    def __str__(self, *args):
        return _transformation.MarginalTransformationGradient___str__(self, *args)

    def __init__(self, *args):
        _transformation.MarginalTransformationGradient_swiginit(self, _transformation.new_MarginalTransformationGradient(*args))

    __swig_destroy__ = _transformation.delete_MarginalTransformationGradient


_transformation.MarginalTransformationGradient_swigregister(MarginalTransformationGradient)

class MarginalTransformationHessian(openturns.func.HessianImplementation):
    """Proxy of C++ OT::MarginalTransformationHessian."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.MarginalTransformationHessian_getClassName(self)

    def hessian(self, inP):
        """
        Return the Jacobian transposed matrix of the implementation at a point.

        Parameters
        ----------
        point : sequence of float
            Point where the Jacobian transposed matrix is calculated.

        Returns
        -------
        hessian : :class:`~openturns.Matrix`
            The Jacobian transposed matrix of the function at *point*.
        """
        return _transformation.MarginalTransformationHessian_hessian(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.
        """
        return _transformation.MarginalTransformationHessian_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.
        """
        return _transformation.MarginalTransformationHessian_getOutputDimension(self)

    def __repr__(self):
        return _transformation.MarginalTransformationHessian___repr__(self)

    def __str__(self, *args):
        return _transformation.MarginalTransformationHessian___str__(self, *args)

    def __init__(self, *args):
        _transformation.MarginalTransformationHessian_swiginit(self, _transformation.new_MarginalTransformationHessian(*args))

    __swig_destroy__ = _transformation.delete_MarginalTransformationHessian


_transformation.MarginalTransformationHessian_swigregister(MarginalTransformationHessian)

class NatafEllipticalCopulaEvaluation(openturns.func.EvaluationImplementation):
    """Proxy of C++ OT::NatafEllipticalCopulaEvaluation."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.NatafEllipticalCopulaEvaluation_getClassName(self)

    def __call__(self, inP):
        return _transformation.NatafEllipticalCopulaEvaluation___call__(self, inP)

    def parameterGradient(self, inP):
        """
        Gradient against the parameters.

        Parameters
        ----------
        x : sequence of float
            Input point

        Returns
        -------
        parameter_gradient : :class:`~openturns.Matrix`
            The parameters gradient computed at x.
        """
        return _transformation.NatafEllipticalCopulaEvaluation_parameterGradient(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getInputDimension())
        2
        """
        return _transformation.NatafEllipticalCopulaEvaluation_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getOutputDimension())
        1
        """
        return _transformation.NatafEllipticalCopulaEvaluation_getOutputDimension(self)

    def __repr__(self):
        return _transformation.NatafEllipticalCopulaEvaluation___repr__(self)

    def __str__(self, offset):
        return _transformation.NatafEllipticalCopulaEvaluation___str__(self, offset)

    def __init__(self, *args):
        _transformation.NatafEllipticalCopulaEvaluation_swiginit(self, _transformation.new_NatafEllipticalCopulaEvaluation(*args))

    __swig_destroy__ = _transformation.delete_NatafEllipticalCopulaEvaluation


_transformation.NatafEllipticalCopulaEvaluation_swigregister(NatafEllipticalCopulaEvaluation)

class NatafEllipticalCopulaGradient(openturns.func.GradientImplementation):
    """Proxy of C++ OT::NatafEllipticalCopulaGradient."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.NatafEllipticalCopulaGradient_getClassName(self)

    def gradient(self, inP):
        """
        Return the Jacobian transposed matrix of the implementation at a point.

        Parameters
        ----------
        point : sequence of float
            Point where the Jacobian transposed matrix is calculated.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The Jacobian transposed matrix of the function at *point*.
        """
        return _transformation.NatafEllipticalCopulaGradient_gradient(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.
        """
        return _transformation.NatafEllipticalCopulaGradient_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.
        """
        return _transformation.NatafEllipticalCopulaGradient_getOutputDimension(self)

    def __repr__(self):
        return _transformation.NatafEllipticalCopulaGradient___repr__(self)

    def __init__(self, *args):
        _transformation.NatafEllipticalCopulaGradient_swiginit(self, _transformation.new_NatafEllipticalCopulaGradient(*args))

    __swig_destroy__ = _transformation.delete_NatafEllipticalCopulaGradient


_transformation.NatafEllipticalCopulaGradient_swigregister(NatafEllipticalCopulaGradient)

class NatafEllipticalCopulaHessian(openturns.func.HessianImplementation):
    """Proxy of C++ OT::NatafEllipticalCopulaHessian."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.NatafEllipticalCopulaHessian_getClassName(self)

    def hessian(self, inP):
        """
        Return the Jacobian transposed matrix of the implementation at a point.

        Parameters
        ----------
        point : sequence of float
            Point where the Jacobian transposed matrix is calculated.

        Returns
        -------
        hessian : :class:`~openturns.Matrix`
            The Jacobian transposed matrix of the function at *point*.
        """
        return _transformation.NatafEllipticalCopulaHessian_hessian(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.
        """
        return _transformation.NatafEllipticalCopulaHessian_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.
        """
        return _transformation.NatafEllipticalCopulaHessian_getOutputDimension(self)

    def __repr__(self):
        return _transformation.NatafEllipticalCopulaHessian___repr__(self)

    def __init__(self, *args):
        _transformation.NatafEllipticalCopulaHessian_swiginit(self, _transformation.new_NatafEllipticalCopulaHessian(*args))

    __swig_destroy__ = _transformation.delete_NatafEllipticalCopulaHessian


_transformation.NatafEllipticalCopulaHessian_swigregister(NatafEllipticalCopulaHessian)

class InverseNatafEllipticalCopulaEvaluation(openturns.func.EvaluationImplementation):
    """Proxy of C++ OT::InverseNatafEllipticalCopulaEvaluation."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.InverseNatafEllipticalCopulaEvaluation_getClassName(self)

    def __call__(self, inP):
        return _transformation.InverseNatafEllipticalCopulaEvaluation___call__(self, inP)

    def parameterGradient(self, inP):
        """
        Gradient against the parameters.

        Parameters
        ----------
        x : sequence of float
            Input point

        Returns
        -------
        parameter_gradient : :class:`~openturns.Matrix`
            The parameters gradient computed at x.
        """
        return _transformation.InverseNatafEllipticalCopulaEvaluation_parameterGradient(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getInputDimension())
        2
        """
        return _transformation.InverseNatafEllipticalCopulaEvaluation_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getOutputDimension())
        1
        """
        return _transformation.InverseNatafEllipticalCopulaEvaluation_getOutputDimension(self)

    def __repr__(self):
        return _transformation.InverseNatafEllipticalCopulaEvaluation___repr__(self)

    def __str__(self, offset):
        return _transformation.InverseNatafEllipticalCopulaEvaluation___str__(self, offset)

    def __init__(self, *args):
        _transformation.InverseNatafEllipticalCopulaEvaluation_swiginit(self, _transformation.new_InverseNatafEllipticalCopulaEvaluation(*args))

    __swig_destroy__ = _transformation.delete_InverseNatafEllipticalCopulaEvaluation


_transformation.InverseNatafEllipticalCopulaEvaluation_swigregister(InverseNatafEllipticalCopulaEvaluation)

class InverseNatafEllipticalCopulaGradient(openturns.func.GradientImplementation):
    """Proxy of C++ OT::InverseNatafEllipticalCopulaGradient."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.InverseNatafEllipticalCopulaGradient_getClassName(self)

    def gradient(self, inP):
        """
        Return the Jacobian transposed matrix of the implementation at a point.

        Parameters
        ----------
        point : sequence of float
            Point where the Jacobian transposed matrix is calculated.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The Jacobian transposed matrix of the function at *point*.
        """
        return _transformation.InverseNatafEllipticalCopulaGradient_gradient(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.
        """
        return _transformation.InverseNatafEllipticalCopulaGradient_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.
        """
        return _transformation.InverseNatafEllipticalCopulaGradient_getOutputDimension(self)

    def __repr__(self):
        return _transformation.InverseNatafEllipticalCopulaGradient___repr__(self)

    def __init__(self, *args):
        _transformation.InverseNatafEllipticalCopulaGradient_swiginit(self, _transformation.new_InverseNatafEllipticalCopulaGradient(*args))

    __swig_destroy__ = _transformation.delete_InverseNatafEllipticalCopulaGradient


_transformation.InverseNatafEllipticalCopulaGradient_swigregister(InverseNatafEllipticalCopulaGradient)

class InverseNatafEllipticalCopulaHessian(openturns.func.HessianImplementation):
    """Proxy of C++ OT::InverseNatafEllipticalCopulaHessian."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.InverseNatafEllipticalCopulaHessian_getClassName(self)

    def hessian(self, inP):
        """
        Return the Jacobian transposed matrix of the implementation at a point.

        Parameters
        ----------
        point : sequence of float
            Point where the Jacobian transposed matrix is calculated.

        Returns
        -------
        hessian : :class:`~openturns.Matrix`
            The Jacobian transposed matrix of the function at *point*.
        """
        return _transformation.InverseNatafEllipticalCopulaHessian_hessian(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.
        """
        return _transformation.InverseNatafEllipticalCopulaHessian_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.
        """
        return _transformation.InverseNatafEllipticalCopulaHessian_getOutputDimension(self)

    def __repr__(self):
        return _transformation.InverseNatafEllipticalCopulaHessian___repr__(self)

    def __init__(self, *args):
        _transformation.InverseNatafEllipticalCopulaHessian_swiginit(self, _transformation.new_InverseNatafEllipticalCopulaHessian(*args))

    __swig_destroy__ = _transformation.delete_InverseNatafEllipticalCopulaHessian


_transformation.InverseNatafEllipticalCopulaHessian_swigregister(InverseNatafEllipticalCopulaHessian)

class NatafIndependentCopulaEvaluation(openturns.func.EvaluationImplementation):
    """Proxy of C++ OT::NatafIndependentCopulaEvaluation."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.NatafIndependentCopulaEvaluation_getClassName(self)

    def __call__(self, inP):
        return _transformation.NatafIndependentCopulaEvaluation___call__(self, inP)

    def parameterGradient(self, inP):
        """
        Gradient against the parameters.

        Parameters
        ----------
        x : sequence of float
            Input point

        Returns
        -------
        parameter_gradient : :class:`~openturns.Matrix`
            The parameters gradient computed at x.
        """
        return _transformation.NatafIndependentCopulaEvaluation_parameterGradient(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getInputDimension())
        2
        """
        return _transformation.NatafIndependentCopulaEvaluation_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getOutputDimension())
        1
        """
        return _transformation.NatafIndependentCopulaEvaluation_getOutputDimension(self)

    def __repr__(self):
        return _transformation.NatafIndependentCopulaEvaluation___repr__(self)

    def __str__(self, offset):
        return _transformation.NatafIndependentCopulaEvaluation___str__(self, offset)

    def __init__(self, *args):
        _transformation.NatafIndependentCopulaEvaluation_swiginit(self, _transformation.new_NatafIndependentCopulaEvaluation(*args))

    __swig_destroy__ = _transformation.delete_NatafIndependentCopulaEvaluation


_transformation.NatafIndependentCopulaEvaluation_swigregister(NatafIndependentCopulaEvaluation)

class NatafIndependentCopulaGradient(openturns.func.GradientImplementation):
    """Proxy of C++ OT::NatafIndependentCopulaGradient."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.NatafIndependentCopulaGradient_getClassName(self)

    def gradient(self, inP):
        """
        Return the Jacobian transposed matrix of the implementation at a point.

        Parameters
        ----------
        point : sequence of float
            Point where the Jacobian transposed matrix is calculated.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The Jacobian transposed matrix of the function at *point*.
        """
        return _transformation.NatafIndependentCopulaGradient_gradient(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.
        """
        return _transformation.NatafIndependentCopulaGradient_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.
        """
        return _transformation.NatafIndependentCopulaGradient_getOutputDimension(self)

    def __repr__(self):
        return _transformation.NatafIndependentCopulaGradient___repr__(self)

    def __init__(self, *args):
        _transformation.NatafIndependentCopulaGradient_swiginit(self, _transformation.new_NatafIndependentCopulaGradient(*args))

    __swig_destroy__ = _transformation.delete_NatafIndependentCopulaGradient


_transformation.NatafIndependentCopulaGradient_swigregister(NatafIndependentCopulaGradient)

class NatafIndependentCopulaHessian(openturns.func.HessianImplementation):
    """Proxy of C++ OT::NatafIndependentCopulaHessian."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.NatafIndependentCopulaHessian_getClassName(self)

    def hessian(self, inP):
        """
        Return the Jacobian transposed matrix of the implementation at a point.

        Parameters
        ----------
        point : sequence of float
            Point where the Jacobian transposed matrix is calculated.

        Returns
        -------
        hessian : :class:`~openturns.Matrix`
            The Jacobian transposed matrix of the function at *point*.
        """
        return _transformation.NatafIndependentCopulaHessian_hessian(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.
        """
        return _transformation.NatafIndependentCopulaHessian_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.
        """
        return _transformation.NatafIndependentCopulaHessian_getOutputDimension(self)

    def __repr__(self):
        return _transformation.NatafIndependentCopulaHessian___repr__(self)

    def __init__(self, *args):
        _transformation.NatafIndependentCopulaHessian_swiginit(self, _transformation.new_NatafIndependentCopulaHessian(*args))

    __swig_destroy__ = _transformation.delete_NatafIndependentCopulaHessian


_transformation.NatafIndependentCopulaHessian_swigregister(NatafIndependentCopulaHessian)

class InverseNatafIndependentCopulaEvaluation(openturns.func.EvaluationImplementation):
    """Proxy of C++ OT::InverseNatafIndependentCopulaEvaluation."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.InverseNatafIndependentCopulaEvaluation_getClassName(self)

    def __call__(self, inP):
        return _transformation.InverseNatafIndependentCopulaEvaluation___call__(self, inP)

    def parameterGradient(self, inP):
        """
        Gradient against the parameters.

        Parameters
        ----------
        x : sequence of float
            Input point

        Returns
        -------
        parameter_gradient : :class:`~openturns.Matrix`
            The parameters gradient computed at x.
        """
        return _transformation.InverseNatafIndependentCopulaEvaluation_parameterGradient(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getInputDimension())
        2
        """
        return _transformation.InverseNatafIndependentCopulaEvaluation_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getOutputDimension())
        1
        """
        return _transformation.InverseNatafIndependentCopulaEvaluation_getOutputDimension(self)

    def __repr__(self):
        return _transformation.InverseNatafIndependentCopulaEvaluation___repr__(self)

    def __str__(self, offset):
        return _transformation.InverseNatafIndependentCopulaEvaluation___str__(self, offset)

    def __init__(self, *args):
        _transformation.InverseNatafIndependentCopulaEvaluation_swiginit(self, _transformation.new_InverseNatafIndependentCopulaEvaluation(*args))

    __swig_destroy__ = _transformation.delete_InverseNatafIndependentCopulaEvaluation


_transformation.InverseNatafIndependentCopulaEvaluation_swigregister(InverseNatafIndependentCopulaEvaluation)

class InverseNatafIndependentCopulaGradient(openturns.func.GradientImplementation):
    """Proxy of C++ OT::InverseNatafIndependentCopulaGradient."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.InverseNatafIndependentCopulaGradient_getClassName(self)

    def gradient(self, inP):
        """
        Return the Jacobian transposed matrix of the implementation at a point.

        Parameters
        ----------
        point : sequence of float
            Point where the Jacobian transposed matrix is calculated.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The Jacobian transposed matrix of the function at *point*.
        """
        return _transformation.InverseNatafIndependentCopulaGradient_gradient(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.
        """
        return _transformation.InverseNatafIndependentCopulaGradient_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.
        """
        return _transformation.InverseNatafIndependentCopulaGradient_getOutputDimension(self)

    def __repr__(self):
        return _transformation.InverseNatafIndependentCopulaGradient___repr__(self)

    def __init__(self, *args):
        _transformation.InverseNatafIndependentCopulaGradient_swiginit(self, _transformation.new_InverseNatafIndependentCopulaGradient(*args))

    __swig_destroy__ = _transformation.delete_InverseNatafIndependentCopulaGradient


_transformation.InverseNatafIndependentCopulaGradient_swigregister(InverseNatafIndependentCopulaGradient)

class InverseNatafIndependentCopulaHessian(openturns.func.HessianImplementation):
    """Proxy of C++ OT::InverseNatafIndependentCopulaHessian."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.InverseNatafIndependentCopulaHessian_getClassName(self)

    def hessian(self, inP):
        """
        Return the Jacobian transposed matrix of the implementation at a point.

        Parameters
        ----------
        point : sequence of float
            Point where the Jacobian transposed matrix is calculated.

        Returns
        -------
        hessian : :class:`~openturns.Matrix`
            The Jacobian transposed matrix of the function at *point*.
        """
        return _transformation.InverseNatafIndependentCopulaHessian_hessian(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.
        """
        return _transformation.InverseNatafIndependentCopulaHessian_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.
        """
        return _transformation.InverseNatafIndependentCopulaHessian_getOutputDimension(self)

    def __repr__(self):
        return _transformation.InverseNatafIndependentCopulaHessian___repr__(self)

    def __init__(self, *args):
        _transformation.InverseNatafIndependentCopulaHessian_swiginit(self, _transformation.new_InverseNatafIndependentCopulaHessian(*args))

    __swig_destroy__ = _transformation.delete_InverseNatafIndependentCopulaHessian


_transformation.InverseNatafIndependentCopulaHessian_swigregister(InverseNatafIndependentCopulaHessian)

class NatafEllipticalDistributionEvaluation(openturns.func.LinearEvaluation):
    """Proxy of C++ OT::NatafEllipticalDistributionEvaluation."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.NatafEllipticalDistributionEvaluation_getClassName(self)

    def parameterGradient(self, inP):
        """
        Gradient against the parameters.

        Parameters
        ----------
        x : sequence of float
            Input point

        Returns
        -------
        parameter_gradient : :class:`~openturns.Matrix`
            The parameters gradient computed at x.
        """
        return _transformation.NatafEllipticalDistributionEvaluation_parameterGradient(self, inP)

    def __repr__(self):
        return _transformation.NatafEllipticalDistributionEvaluation___repr__(self)

    def __init__(self, *args):
        _transformation.NatafEllipticalDistributionEvaluation_swiginit(self, _transformation.new_NatafEllipticalDistributionEvaluation(*args))

    __swig_destroy__ = _transformation.delete_NatafEllipticalDistributionEvaluation


_transformation.NatafEllipticalDistributionEvaluation_swigregister(NatafEllipticalDistributionEvaluation)

class NatafEllipticalDistributionGradient(openturns.func.ConstantGradient):
    """Proxy of C++ OT::NatafEllipticalDistributionGradient."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.NatafEllipticalDistributionGradient_getClassName(self)

    def __repr__(self):
        return _transformation.NatafEllipticalDistributionGradient___repr__(self)

    def __init__(self, *args):
        _transformation.NatafEllipticalDistributionGradient_swiginit(self, _transformation.new_NatafEllipticalDistributionGradient(*args))

    __swig_destroy__ = _transformation.delete_NatafEllipticalDistributionGradient


_transformation.NatafEllipticalDistributionGradient_swigregister(NatafEllipticalDistributionGradient)

class NatafEllipticalDistributionHessian(openturns.func.ConstantHessian):
    """Proxy of C++ OT::NatafEllipticalDistributionHessian."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.NatafEllipticalDistributionHessian_getClassName(self)

    def __repr__(self):
        return _transformation.NatafEllipticalDistributionHessian___repr__(self)

    def __init__(self, *args):
        _transformation.NatafEllipticalDistributionHessian_swiginit(self, _transformation.new_NatafEllipticalDistributionHessian(*args))

    __swig_destroy__ = _transformation.delete_NatafEllipticalDistributionHessian


_transformation.NatafEllipticalDistributionHessian_swigregister(NatafEllipticalDistributionHessian)

class InverseNatafEllipticalDistributionEvaluation(openturns.func.LinearEvaluation):
    """Proxy of C++ OT::InverseNatafEllipticalDistributionEvaluation."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.InverseNatafEllipticalDistributionEvaluation_getClassName(self)

    def parameterGradient(self, inP):
        """
        Gradient against the parameters.

        Parameters
        ----------
        x : sequence of float
            Input point

        Returns
        -------
        parameter_gradient : :class:`~openturns.Matrix`
            The parameters gradient computed at x.
        """
        return _transformation.InverseNatafEllipticalDistributionEvaluation_parameterGradient(self, inP)

    def __repr__(self):
        return _transformation.InverseNatafEllipticalDistributionEvaluation___repr__(self)

    def __init__(self, *args):
        _transformation.InverseNatafEllipticalDistributionEvaluation_swiginit(self, _transformation.new_InverseNatafEllipticalDistributionEvaluation(*args))

    __swig_destroy__ = _transformation.delete_InverseNatafEllipticalDistributionEvaluation


_transformation.InverseNatafEllipticalDistributionEvaluation_swigregister(InverseNatafEllipticalDistributionEvaluation)

class InverseNatafEllipticalDistributionGradient(openturns.func.ConstantGradient):
    """Proxy of C++ OT::InverseNatafEllipticalDistributionGradient."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.InverseNatafEllipticalDistributionGradient_getClassName(self)

    def __repr__(self):
        return _transformation.InverseNatafEllipticalDistributionGradient___repr__(self)

    def __init__(self, *args):
        _transformation.InverseNatafEllipticalDistributionGradient_swiginit(self, _transformation.new_InverseNatafEllipticalDistributionGradient(*args))

    __swig_destroy__ = _transformation.delete_InverseNatafEllipticalDistributionGradient


_transformation.InverseNatafEllipticalDistributionGradient_swigregister(InverseNatafEllipticalDistributionGradient)

class InverseNatafEllipticalDistributionHessian(openturns.func.ConstantHessian):
    """Proxy of C++ OT::InverseNatafEllipticalDistributionHessian."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.InverseNatafEllipticalDistributionHessian_getClassName(self)

    def __repr__(self):
        return _transformation.InverseNatafEllipticalDistributionHessian___repr__(self)

    def __init__(self, *args):
        _transformation.InverseNatafEllipticalDistributionHessian_swiginit(self, _transformation.new_InverseNatafEllipticalDistributionHessian(*args))

    __swig_destroy__ = _transformation.delete_InverseNatafEllipticalDistributionHessian


_transformation.InverseNatafEllipticalDistributionHessian_swigregister(InverseNatafEllipticalDistributionHessian)

class RosenblattEvaluation(openturns.func.EvaluationImplementation):
    """Proxy of C++ OT::RosenblattEvaluation."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.RosenblattEvaluation_getClassName(self)

    def __call__(self, inP):
        return _transformation.RosenblattEvaluation___call__(self, inP)

    def parameterGradient(self, inP):
        """
        Gradient against the parameters.

        Parameters
        ----------
        x : sequence of float
            Input point

        Returns
        -------
        parameter_gradient : :class:`~openturns.Matrix`
            The parameters gradient computed at x.
        """
        return _transformation.RosenblattEvaluation_parameterGradient(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getInputDimension())
        2
        """
        return _transformation.RosenblattEvaluation_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getOutputDimension())
        1
        """
        return _transformation.RosenblattEvaluation_getOutputDimension(self)

    def __repr__(self):
        return _transformation.RosenblattEvaluation___repr__(self)

    def __str__(self, offset):
        return _transformation.RosenblattEvaluation___str__(self, offset)

    def __init__(self, *args):
        _transformation.RosenblattEvaluation_swiginit(self, _transformation.new_RosenblattEvaluation(*args))

    __swig_destroy__ = _transformation.delete_RosenblattEvaluation


_transformation.RosenblattEvaluation_swigregister(RosenblattEvaluation)

class InverseRosenblattEvaluation(openturns.func.EvaluationImplementation):
    """Proxy of C++ OT::InverseRosenblattEvaluation."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _transformation.InverseRosenblattEvaluation_getClassName(self)

    def __call__(self, inP):
        return _transformation.InverseRosenblattEvaluation___call__(self, inP)

    def parameterGradient(self, inP):
        """
        Gradient against the parameters.

        Parameters
        ----------
        x : sequence of float
            Input point

        Returns
        -------
        parameter_gradient : :class:`~openturns.Matrix`
            The parameters gradient computed at x.
        """
        return _transformation.InverseRosenblattEvaluation_parameterGradient(self, inP)

    def getInputDimension(self):
        """
        Accessor to the number of the inputs.

        Returns
        -------
        number_inputs : int
            Number of inputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getInputDimension())
        2
        """
        return _transformation.InverseRosenblattEvaluation_getInputDimension(self)

    def getOutputDimension(self):
        """
        Accessor to the number of the outputs.

        Returns
        -------
        number_outputs : int
            Number of outputs.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x1', 'x2'],
        ...                         ['2 * x1^2 + x1 + 8 * x2 + 4 * cos(x1) * x2 + 6'])
        >>> print(f.getOutputDimension())
        1
        """
        return _transformation.InverseRosenblattEvaluation_getOutputDimension(self)

    def __repr__(self):
        return _transformation.InverseRosenblattEvaluation___repr__(self)

    def __str__(self, offset):
        return _transformation.InverseRosenblattEvaluation___str__(self, offset)

    def __init__(self, *args):
        _transformation.InverseRosenblattEvaluation_swiginit(self, _transformation.new_InverseRosenblattEvaluation(*args))

    __swig_destroy__ = _transformation.delete_InverseRosenblattEvaluation


_transformation.InverseRosenblattEvaluation_swigregister(InverseRosenblattEvaluation)

class DistributionTransformation(openturns.func.Function):
    """
    Isoprobabilistic transformation.

    Available constructor:
        DistributionTransformation(*left, right*)

    Parameters
    ----------
    left, right : :class:`~openturns.Distribution`
        The transformation that maps *left* into *right*.
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
        return _transformation.DistributionTransformation_getClassName(self)

    def __eq__(self, other):
        return _transformation.DistributionTransformation___eq__(self, other)

    def inverse(self):
        """
        Inverse isoprobabilistic transformation.

        Returns
        -------
        inverseT : :class:`~openturns.DistributionTransformation`
            The inverse transformation.
        """
        return _transformation.DistributionTransformation_inverse(self)

    def __repr__(self):
        return _transformation.DistributionTransformation___repr__(self)

    def __str__(self, *args):
        return _transformation.DistributionTransformation___str__(self, *args)

    def __init__(self, *args):
        _transformation.DistributionTransformation_swiginit(self, _transformation.new_DistributionTransformation(*args))

    __swig_destroy__ = _transformation.delete_DistributionTransformation


_transformation.DistributionTransformation_swigregister(DistributionTransformation)
import openturns.metamodel, openturns.weightedexperiment, openturns.orthogonalbasis, openturns.randomvector

class BoxCoxFactory(openturns.common.PersistentObject):
    r"""
    BoxCox transformation estimator.

    Notes
    -----
    The class :class:`~openturns.BoxCoxFactory` enables to build a Box Cox transformation from data.

    The Box Cox transformation :math:`h_{\vect{\lambda}, \vect{\alpha}}: \Rset^d \rightarrow \Rset^d` maps a sample into a new sample following a normal distribution with independent components. That sample may be the realization of a process as well as the realization of a distribution.

    In the multivariate case, we proceed component by component: :math:`h_{\lambda_i, \alpha_i}: \Rset \rightarrow \Rset` which writes:

    .. math::

        h_{\lambda_i, \alpha_i}(x) = 
        \left\{
        \begin{array}{ll}
        \dfrac{(x+\alpha_i)^\lambda-1}{\lambda_i} & \lambda_i \neq 0 \\
        \log(x+\alpha_i)                        & \lambda_i = 0
        \end{array}
        \right.

    for all :math:`x+\alpha_i >0`.

    |

    BoxCox transformation could alse be performed in the case of the estimation of a general linear model through :class:`~openturns.GeneralLinearModelAlgorithm`.
    The objective is to estimate the most likely surrogate model (general linear model) which links input data :math:`x` and :math:`h_{\vect{\lambda}, \vect{\alpha}}(y)`. :math:`\vect{\lambda}` are to be calibrated such as maximizing the general linear model's likelihood function. In that context, a :class:`~openturns.CovarianceModel` and a :class:`~openturns.Basis` have to be fixed

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
        return _transformation.BoxCoxFactory_getClassName(self)

    def __repr__(self):
        return _transformation.BoxCoxFactory___repr__(self)

    def __str__(self, *args):
        return _transformation.BoxCoxFactory___str__(self, *args)

    def build(self, *args):
        r"""
        Estimate the Box Cox transformation.

        Available usages:
            build(*myTimeSeries*)

            build(*myTimeSeries, shift*)

            build(*myTimeSeries, shift, likelihoodGraph*)

            build(*mySample*)

            build(*mySample, shift*)

            build(*mySample, shift, likelihoodGraph*)

            build(*inputSample, outputSample, covarianceModel, basis, shift, generalLinearModelResult*)

            build(*inputSample, outputSample, covarianceModel, shift, generalLinearModelResult*)

        Parameters
        ----------
        myTimeSeries : :class:`~openturns.TimeSeries`
            One realization of a  process.
        mySample : :class:`~openturns.Sample`
            A set of *iid* values.
        shift : :class:`~openturns.Point`
            It ensures that when shifted, the data are all positive.
            By default the opposite of the min vector of the data is used if some data are negative.
        likelihoodGraph : :class:`~openturns.Graph`
            An empty graph that is fulfilled later with the log-likelihood of the mapped variables with respect to the :math:`lambda` parameter for each component.
        inputSample, outputSample : :class:`~openturns.Sample` or 2d-array
            The input and output samples of a model evaluated apart.
        basis : :class:`~openturns.Basis`
            Functional basis to estimate the trend.
            If the output dimension is greater than 1, the same basis is used for all marginals.
        multivariateBasis : collection of :class:`~openturns.Basis`
            Collection of functional basis: one basis for each marginal output.
            If the trend is not estimated, the collection must be empty.
        covarianceModel : :class:`~openturns.CovarianceModel`
            Covariance model.
            Should have input dimension equal to input sample's dimension and dimension equal to output sample's dimension.
            See note for some particular applications.
        generalLinearModelResult : :class:`~openturns.GeneralLinearModelResult`
            Empty structure that contains results of general linear model algorithm.

        Returns
        -------
        myBoxCoxTransform : :class:`~openturns.BoxCoxTransform`
            The estimated Box Cox transformation.

        Notes
        -----

        We describe the estimation in the univariate case, in the case of no surrogate model estimate. Only the parameter :math:`\lambda` is estimated. To clarify the notations, we omit the mention of :math:`\alpha` in :math:`h_\lambda`.

        We note :math:`(x_0, \dots, x_{N-1})` a sample of :math:`X`. We suppose that :math:`h_\lambda(X) \sim \cN(\beta , \sigma^2 )`.

        The parameters :math:`(\beta,\sigma,\lambda)` are  estimated by the maximum likelihood estimators. We note :math:`\Phi_{\beta, \sigma}` and :math:`\phi_{\beta, \sigma}` respectively the cumulative distribution function and the density probability function of the :math:`\cN(\beta , \sigma^2)` distribution.

        We have :

        .. math::

            \begin{array}{lcl}
              \forall v \geq 0, \, \Prob{ X \leq v } & = & \Prob{ h_\lambda(X) \leq h_\lambda(v) } \\
              & = & \Phi_{\beta, \sigma} \left(h_\lambda(v)\right)
            \end{array}

        from which we derive the  density probability function *p* of :math:`X`:

        .. math::

            \begin{array}{lcl}
              p(v) & = & h_\lambda'(v)\phi_{\beta, \sigma}(v) = v^{\lambda - 1}\phi_{\beta, \sigma}(v)
            \end{array}

        which enables to write the likelihood of the values :math:`(x_0, \dots, x_{N-1})`:

        .. math::

            \begin{array}{lcl}
              L(\beta,\sigma,\lambda)
              & = &
              \underbrace{ \frac{1}{(2\pi)^{N/2}}
                \times
                \frac{1}{(\sigma^2)^{N/2}}
                \times
                \exp\left[
                  -\frac{1}{2\sigma^2}
                  \sum_{k=0}^{N-1}
                  \left(
                  h_\lambda(x_k)-\beta
                  \right)^2
                  \right]
              }_{\Psi(\beta, \sigma)}
              \times
              \prod_{k=0}^{N-1} x_k^{\lambda - 1}
            \end{array}

        We notice that for each fixed :math:`\lambda`, the likelihood equation is proportional to the likelihood equation which estimates  :math:`(\beta, \sigma^2)`.

        Thus, the maximum likelihood estimators for :math:`(\beta(\lambda), \sigma^2(\lambda))` for a given :math:`\lambda`  are :

        .. math::

            \begin{array}{lcl}
             \hat{\beta}(\lambda) & = & \frac{1}{N} \sum_{k=0}^{N-1} h_{\lambda}(x_k) \\
             \hat{\sigma}^2(\lambda)  & = &  \frac{1}{N} \sum_{k=0}^{N-1} (h_{\lambda}(x_k) - \beta(\lambda))^2
            \end{array}

        Substituting these expressions in the likelihood equation and taking the :math:`\log-` likelihood leads to:

        .. math::

            \begin{array}{lcl}
              \ell(\lambda) = \log L( \hat{\beta}(\lambda), \hat{\sigma}(\lambda),\lambda ) & = & C -
              \frac{N}{2}
              \log\left[\hat{\sigma}^2(\lambda)\right]
              \;+\;
              \left(\lambda - 1 \right) \sum_{k=0}^{N-1} \log(x_i)\,,%\qquad mbox{where :math:`C` is a constant.}
            \end{array}

        The parameter :math:`\hat{\lambda}` is the one maximising :math:`\ell(\lambda)`.

        When the empty graph *likelihoodGraph* is precised, it is fulfilled with the evolution of the likelihood with respect to the value of :math:`\lambda` for each component  *i*. It enables to graphically detect the optimal values.

        |

        In the case of surrogate model estimate, we note :math:`(x_0, \dots, x_{N-1})` the input sample of :math:`X`, :math:`(y_0, \dots, y_{N-1})` the input sample of :math:`Y`.
        We suppose the general linear model link :math:`h_\lambda(Y) = \vect{F}^t(\vect{x}) \vect{\beta} + \vect{Z}` with :math:`\mat{F} \in \mathcal{M}_{np, M}(\Rset)`:

        .. math::
            \mat{F}(\vect{x}) = \left(
              \begin{array}{lcl}
                \vect{f}_1(\vect{x}_1) & \dots & \vect{f}_M(\vect{x}_1) \\
                \dots & \dots & \\
                \vect{f}_1(\vect{x}_n) & \dots & \vect{f}_M(\vect{x}_n)
               \end{array}
             \right)

        :math:`(f_1, \dots, f_M)` is a functional basis with :math:`f_i: \Rset^d \mapsto \Rset^p` for all *i*, :math:`\beta` are the coefficients of the linear combination and :math:`Z` is a zero-mean gaussian process with a stationary covariance function :math:`C_{\vect{\sigma}, \vect{\theta}}`
        Thus implies that :math:`h_\lambda(Y) \sim \cN(\vect{F}^t(\vect{x}) \vect{\beta}, C_{\vect{\sigma}, \vect{\theta}})`.

        The likelihood function to be maximized writes as follows:

        .. math::

            \begin{array}{lcl}
              \ell_{glm}(\lambda) = \log L(\lambda ) & = & C - \log\left( |C^{\lambda}_{\vect{\sigma}, \vect{\theta}} | \right)
              \;-\;
            \left( h_\lambda(Y) - \vect{F}^t(\vect{x}) \vect{\beta} \right) {C^{\lambda}_{\vect{\sigma}, \vect{\theta}}}^{-1}
            \left( h_\lambda(Y) - \vect{F}^t(\vect{x}) \vect{\beta} \right)^t
            \end{array}

        where :math:`C^{\lambda}_{\vect{\sigma}, \vect{\theta}}` is the matrix resulted from the discretization of the covariance model over :math:`X`.
        The parameter :math:`\hat{\lambda}` is the one maximising :math:`\ell_{glm}(\lambda)`.

        Examples
        --------
        Estimate the Box Cox transformation from a sample:

        >>> import openturns as ot
        >>> mySample = ot.Exponential(2).getSample(10)
        >>> myBoxCoxFactory = ot.BoxCoxFactory()
        >>> myModelTransform = myBoxCoxFactory.build(mySample)
        >>> estimatedLambda = myModelTransform.getLambda()

        Estimate the Box Cox transformation from a field:

        >>> myIndices= ot.Indices([10, 5])
        >>> myMesher=ot.IntervalMesher(myIndices)
        >>> myInterval = ot.Interval([0.0, 0.0], [2.0, 1.0])
        >>> myMesh=myMesher.build(myInterval)
        >>> amplitude=[1.0]
        >>> scale=[0.2, 0.2]
        >>> myCovModel=ot.ExponentialModel(scale, amplitude)
        >>> myXproc=ot.GaussianProcess(myCovModel, myMesh)
        >>> g = ot.SymbolicFunction(['x1'],  ['exp(x1)'])
        >>> myDynTransform = ot.ValueFunction(g, myMesh)
        >>> myXtProcess = ot.CompositeProcess(myDynTransform, myXproc)

        >>> myField = myXtProcess.getRealization()
        >>> myModelTransform = ot.BoxCoxFactory().build(myField)

        Estimation of a general linear model:

        >>> inputSample = ot.Uniform(-1.0, 1.0).getSample(20)
        >>> outputSample = ot.Sample(inputSample)
        >>> # Evaluation of y = ax + b (a: scale, b: translate)
        >>> outputSample = outputSample * [3] + [3.1]
        >>> # inverse transfo + small noise
        >>> def f(x): import math; return [math.exp(x[0])]
        >>> inv_transfo = ot.PythonFunction(1,1, f)
        >>> outputSample = inv_transfo(outputSample) + ot.Normal(0, 1.0e-2).getSample(20)
        >>> # Estimation
        >>> result = ot.GeneralLinearModelResult()
        >>> basis = ot.LinearBasisFactory(1).build()
        >>> covarianceModel = ot.DiracCovarianceModel()
        >>> shift = [1.0e-1]
        >>> myBoxCox = ot.BoxCoxFactory().build(inputSample, outputSample, covarianceModel, basis, shift, result)

        """
        return _transformation.BoxCoxFactory_build(self, *args)

    def getOptimizationAlgorithm(self):
        return _transformation.BoxCoxFactory_getOptimizationAlgorithm(self)

    def setOptimizationAlgorithm(self, solver):
        return _transformation.BoxCoxFactory_setOptimizationAlgorithm(self, solver)

    def __init__(self, *args):
        _transformation.BoxCoxFactory_swiginit(self, _transformation.new_BoxCoxFactory(*args))

    __swig_destroy__ = _transformation.delete_BoxCoxFactory


_transformation.BoxCoxFactory_swigregister(BoxCoxFactory)

class TrendFactory(openturns.common.PersistentObject):
    r"""
    Trend estimator.

    Refer to :ref:`trend_transform`.

    Available constructors:
        TrendFactory(*basisSequenceFactory=LARS(), fittingAlgorithm=CorrectedLeaveOneOut()*)

    Parameters
    ----------
    basisSequenceFactory : :class:`~openturns.BasisSequenceFactory`
        The  regression strategy that provides the estimation of the  coefficients associated to the best model among the  basis functions.

        Default is the *least angle regression* (LARS) method for the choice of sparse models: :class:`~openturns.LARS`.
    fittingAlgorithm : :class:`~openturns.FittingAlgorithm`
        The fitting algorithm that estimates the empirical error on each sub-basis.

        Default is the *leave one out* strategy: :class:`~openturns.CorrectedLeaveOneOut`.

    Notes
    -----
    A multivariate stochastic  process :math:`X: \Omega \times \cD \rightarrow \Rset^d` of dimension *d* where :math:`\cD \in \Rset^n` can write as the sum of a trend function :math:`f_{trend}: \Rset^n \rightarrow \Rset^d` and a stationary multivariate stochastic process :math:`X_{stat}: \Omega \times \cD \rightarrow \Rset^d` of dimension *d* as follows:

    .. math::

       X(\omega,\vect{t}) = X_{stat}(\omega,\vect{t}) + f_{trend}(\vect{t})

    The  :class:`~openturns.TrendFactory` enables to identify the trend  function :math:`f_{trend}` from a given field of the process *X* and then to remove this last one from the initial field. The resulting field is a realization of the process :math:`X_{stat}`.

    We consider the functional basis :math:`\cB = (f_1, f_2, \ldots, f_K)` with :math:`f_j : \Rset^n \longrightarrow \Rset^d`. The trend function :math:`f_{trend}` writes:

    .. math::

        f_{trend}(\vect{t}) = \sum_{j=1}^{K} \alpha_j f_j(\vect{t})

    The coefficients :math:`\alpha_j \in \Rset` have to be computed. In the case where the number of available data is of the same order as *K*, the least square system is ill-posed and a  more complex algorithm should be used. Some algorithms combine cross validation techniques and advanced regression strategies, in order to provide the estimation of the  coefficients associated to the best model among the  basis functions (sparse model). For example, we can use the *least angle regression* (LARS) method for the choice of sparse models.  Then, some fitting algorithms like the *leave one out*, coupled to the regression strategy, assess the error on the prediction and enable the selection of the best sparse model.

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
        return _transformation.TrendFactory_getClassName(self)

    def getBasisSequenceFactory(self):
        r"""
        Accessor to functional basis.

        Returns
        -------
        myBasisSequenceFactory : :class:`~openturns.BasisSequenceFactory`
            The functional basis :math:`\cB`.

        """
        return _transformation.TrendFactory_getBasisSequenceFactory(self)

    def setBasisSequenceFactory(self, basisSequenceFactory):
        r"""
        Accessor to functional basis.

        Parameters
        ----------
        myBasisSequenceFactory : :class:`~openturns.BasisSequenceFactory`
            The functional basis :math:`\cB`.

        """
        return _transformation.TrendFactory_setBasisSequenceFactory(self, basisSequenceFactory)

    def getFittingAlgorithm(self):
        """
        Accessor to fitting algorithm  basis.

        Returns
        -------
        myFittingAlgorithm : :class:`~openturns.FittingAlgorithm`
            The fitting algorithm that estimates the empirical error on each sub-basis.

        """
        return _transformation.TrendFactory_getFittingAlgorithm(self)

    def setFittingAlgorithm(self, fittingAlgorithm):
        """
        Accessor to fitting algorithm  basis.

        Parameters
        ----------
        myFittingAlgorithm : :class:`~openturns.FittingAlgorithm`
            The fitting algorithm that estimates the empirical error on each sub-basis.

        """
        return _transformation.TrendFactory_setFittingAlgorithm(self, fittingAlgorithm)

    def __repr__(self):
        return _transformation.TrendFactory___repr__(self)

    def __str__(self, *args):
        return _transformation.TrendFactory___str__(self, *args)

    def build(self, field, basis):
        r"""
        Estimate the trend of a process.

        Available usages:
            build(*field, basis*)

        Parameters
        ----------
        field : :class:`~openturns.Field`
            One realization of the process.
        basis : :class:`~openturns.Basis`
            A collection of functions composing the functional basis.

        Returns
        -------
        myTrendTransform : :class:`~openturns.TrendTransform`
            The estimated trend function.

        Examples
        --------
        Define a scalar temporal Gaussian process on a mesh of dimension 1:

        >>> import openturns as ot
        >>> myGrid = ot.RegularGrid(0.0, 1.0, 100)
        >>> amplitude=[5.0]
        >>> scale=[0.2]
        >>> myCovModel=ot.ExponentialModel(scale, amplitude)
        >>> myXProcess=ot.GaussianProcess(myCovModel, myGrid)

        Create a trend function: :math:`f_{trend} : \Rset \mapsto \Rset` where :math:`f_{trend}(t)=1+2t+t^2`:

        >>> fTrend = ot.SymbolicFunction(['t'], ['1+2*t+t^2'])
        >>> fTemp = ot.TrendTransform(fTrend, myGrid)

        Add the trend to the initial process and get a field:

        >>> myYProcess = ot.CompositeProcess(fTemp, myXProcess)
        >>> myYField = myYProcess.getRealization()

        Estimate the trend function from the field:

        >>> myBasisSequenceFactory = ot.LARS()
        >>> myFittingAlgorithm = ot.KFold()
        >>> func1 = ot.SymbolicFunction(['t'], ['1'])
        >>> func2 = ot.SymbolicFunction(['t'], ['t'])
        >>> func3 = ot.SymbolicFunction(['t'], ['t^2'])
        >>> myBasis = ot.Basis([func1, func2, func3])

        >>> myTrendFactory = ot.TrendFactory(myBasisSequenceFactory, myFittingAlgorithm)
        >>> myTrendTransform =  myTrendFactory.build(myYField, myBasis)

        >>> graph = myTrendTransform.getTrendFunction().draw(0.0, 10)
        >>> graph.add(fTrend.draw(0.0, 10))
        >>> graph.add(ot.Cloud(myYField.getMesh().getVertices(), myYField.getValues()))
        >>> graph.setColors(['red', 'blue', 'black'])
        >>> graph.setLegends(['estimated trend', 'actual trend', 'sample'])
        >>> graph.setLegendPosition('topleft')
        >>> graph.setTitle('Trend estimation from a field')
        >>> graph.setYTitle('values')

        """
        return _transformation.TrendFactory_build(self, field, basis)

    def __init__(self, *args):
        _transformation.TrendFactory_swiginit(self, _transformation.new_TrendFactory(*args))

    __swig_destroy__ = _transformation.delete_TrendFactory


_transformation.TrendFactory_swigregister(TrendFactory)