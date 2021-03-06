# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lib/python2.7/site-packages/openturns/algo.py
# Compiled at: 2019-11-13 10:36:02
"""Approximation algorithms."""
from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')
if __package__ or '.' in __name__:
    from . import _algo
else:
    import _algo
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
    __swig_destroy__ = _algo.delete_SwigPyIterator

    def value(self):
        return _algo.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _algo.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _algo.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _algo.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _algo.SwigPyIterator_equal(self, x)

    def copy(self):
        return _algo.SwigPyIterator_copy(self)

    def next(self):
        return _algo.SwigPyIterator_next(self)

    def __next__(self):
        return _algo.SwigPyIterator___next__(self)

    def previous(self):
        return _algo.SwigPyIterator_previous(self)

    def advance(self, n):
        return _algo.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _algo.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _algo.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _algo.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _algo.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _algo.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _algo.SwigPyIterator___sub__(self, *args)

    def __iter__(self):
        return self


_algo.SwigPyIterator_swigregister(SwigPyIterator)

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


import openturns.common, openturns.typ, openturns.func, openturns.geom, openturns.graph, openturns.statistics

class ApproximationAlgorithmImplementation(openturns.common.PersistentObject):
    """
    Approximation algorithm.

    See also
    --------
    LeastSquaresStrategy, ApproximationAlgorithmImplementationFactory,
    LeastSquaresMetaModelSelectionFactory

    Notes
    -----
    The ApproximationAlgorithm is built from an approximation algorithm
    implementation factory which is a
    :class:`~openturns.ApproximationAlgorithmImplementationFactory` or a
    :class:`~openturns.LeastSquaresMetaModelSelectionFactory`.

    This class is not usable because it has sense only whithin the
    :class:`~openturns.FunctionalChaosAlgorithm`.
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
        return _algo.ApproximationAlgorithmImplementation_getClassName(self)

    def getX(self):
        """
        Accessor to the input sample.

        Returns
        -------
        x : :class:`~openturns.Sample`
            Input sample
        """
        return _algo.ApproximationAlgorithmImplementation_getX(self)

    def getY(self):
        """
        Accessor to the output sample.

        Returns
        -------
        y : :class:`~openturns.Sample`
            Input sample
        """
        return _algo.ApproximationAlgorithmImplementation_getY(self)

    def getWeight(self):
        """
        Accessor to the weights.

        Returns
        -------
        weight : :class:`~openturns.Point`
            Output weights
        """
        return _algo.ApproximationAlgorithmImplementation_getWeight(self)

    def getPsi(self):
        """
        Accessor to the basis.

        Returns
        -------
        coefficients : :class:`~openturns.Basis`
            The basis
        """
        return _algo.ApproximationAlgorithmImplementation_getPsi(self)

    def __repr__(self):
        return _algo.ApproximationAlgorithmImplementation___repr__(self)

    def __str__(self, *args):
        return _algo.ApproximationAlgorithmImplementation___str__(self, *args)

    def run(self):
        """Run the algorithm."""
        return _algo.ApproximationAlgorithmImplementation_run(self)

    def getCoefficients(self):
        """
        Accessor to the coefficients.

        Returns
        -------
        coefficients : :class:`~openturns.Point`
            The coefficients
        """
        return _algo.ApproximationAlgorithmImplementation_getCoefficients(self)

    def getResidual(self):
        """
        Accessor to the coefficients.

        Returns
        -------
        coefficients : float
            The residual
        """
        return _algo.ApproximationAlgorithmImplementation_getResidual(self)

    def getRelativeError(self):
        """
        Accessor to the coefficients.

        Returns
        -------
        relativeError : float
            The relative error
        """
        return _algo.ApproximationAlgorithmImplementation_getRelativeError(self)

    def setVerbose(self, verbose):
        """
        Accessor to the verbosity flag.

        Parameters
        ----------
        v : bool
            Enable or disable the verbosity.
        """
        return _algo.ApproximationAlgorithmImplementation_setVerbose(self, verbose)

    def getVerbose(self):
        """
        Accessor to the verbosity flag.

        Returns
        -------
        v : bool.
            Verbosity
        """
        return _algo.ApproximationAlgorithmImplementation_getVerbose(self)

    def __init__(self, *args):
        _algo.ApproximationAlgorithmImplementation_swiginit(self, _algo.new_ApproximationAlgorithmImplementation(*args))

    __swig_destroy__ = _algo.delete_ApproximationAlgorithmImplementation


_algo.ApproximationAlgorithmImplementation_swigregister(ApproximationAlgorithmImplementation)

class ApproximationAlgorithmImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _algo.ApproximationAlgorithmImplementationTypedInterfaceObject_swiginit(self, _algo.new_ApproximationAlgorithmImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _algo.ApproximationAlgorithmImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _algo.ApproximationAlgorithmImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _algo.ApproximationAlgorithmImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _algo.ApproximationAlgorithmImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _algo.ApproximationAlgorithmImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _algo.delete_ApproximationAlgorithmImplementationTypedInterfaceObject


_algo.ApproximationAlgorithmImplementationTypedInterfaceObject_swigregister(ApproximationAlgorithmImplementationTypedInterfaceObject)

class ApproximationAlgorithm(ApproximationAlgorithmImplementationTypedInterfaceObject):
    """
    Approximation algorithm.

    See also
    --------
    LeastSquaresStrategy, ApproximationAlgorithmImplementationFactory,
    LeastSquaresMetaModelSelectionFactory

    Notes
    -----
    The ApproximationAlgorithm is built from an approximation algorithm
    implementation factory which is a
    :class:`~openturns.ApproximationAlgorithmImplementationFactory` or a
    :class:`~openturns.LeastSquaresMetaModelSelectionFactory`.

    This class is not usable because it has sense only whithin the
    :class:`~openturns.FunctionalChaosAlgorithm`.
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
        return _algo.ApproximationAlgorithm_getClassName(self)

    def getX(self):
        """
        Accessor to the input sample.

        Returns
        -------
        x : :class:`~openturns.Sample`
            Input sample
        """
        return _algo.ApproximationAlgorithm_getX(self)

    def getY(self):
        """
        Accessor to the output sample.

        Returns
        -------
        y : :class:`~openturns.Sample`
            Input sample
        """
        return _algo.ApproximationAlgorithm_getY(self)

    def getWeight(self):
        """
        Accessor to the weights.

        Returns
        -------
        weight : :class:`~openturns.Point`
            Output weights
        """
        return _algo.ApproximationAlgorithm_getWeight(self)

    def getPsi(self):
        """
        Accessor to the basis.

        Returns
        -------
        coefficients : :class:`~openturns.Basis`
            The basis
        """
        return _algo.ApproximationAlgorithm_getPsi(self)

    def setVerbose(self, verbose):
        """
        Accessor to the verbosity flag.

        Parameters
        ----------
        v : bool
            Enable or disable the verbosity.
        """
        return _algo.ApproximationAlgorithm_setVerbose(self, verbose)

    def getVerbose(self):
        """
        Accessor to the verbosity flag.

        Returns
        -------
        v : bool.
            Verbosity
        """
        return _algo.ApproximationAlgorithm_getVerbose(self)

    def __repr__(self):
        return _algo.ApproximationAlgorithm___repr__(self)

    def __str__(self, *args):
        return _algo.ApproximationAlgorithm___str__(self, *args)

    def run(self):
        """Run the algorithm."""
        return _algo.ApproximationAlgorithm_run(self)

    def getCoefficients(self):
        """
        Accessor to the coefficients.

        Returns
        -------
        coefficients : :class:`~openturns.Point`
            The coefficients
        """
        return _algo.ApproximationAlgorithm_getCoefficients(self)

    def getResidual(self):
        """
        Accessor to the coefficients.

        Returns
        -------
        coefficients : float
            The residual
        """
        return _algo.ApproximationAlgorithm_getResidual(self)

    def getRelativeError(self):
        """
        Accessor to the coefficients.

        Returns
        -------
        relativeError : float
            The relative error
        """
        return _algo.ApproximationAlgorithm_getRelativeError(self)

    def __init__(self, *args):
        _algo.ApproximationAlgorithm_swiginit(self, _algo.new_ApproximationAlgorithm(*args))

    __swig_destroy__ = _algo.delete_ApproximationAlgorithm


_algo.ApproximationAlgorithm_swigregister(ApproximationAlgorithm)

class ApproximationAlgorithmImplementationFactory(openturns.common.PersistentObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _algo.ApproximationAlgorithmImplementationFactory_getClassName(self)

    def build(self, *args):
        return _algo.ApproximationAlgorithmImplementationFactory_build(self, *args)

    def __repr__(self):
        return _algo.ApproximationAlgorithmImplementationFactory___repr__(self)

    def __init__(self, *args):
        _algo.ApproximationAlgorithmImplementationFactory_swiginit(self, _algo.new_ApproximationAlgorithmImplementationFactory(*args))

    __swig_destroy__ = _algo.delete_ApproximationAlgorithmImplementationFactory


_algo.ApproximationAlgorithmImplementationFactory_swigregister(ApproximationAlgorithmImplementationFactory)

class ClassifierImplementation(openturns.common.PersistentObject):
    """
    Classifier.

    Available constructors:
        Classifier(*classifierImp*)

    Parameters
    ----------
    classifierImp : classifier implementation
        A classifier implementation. It can be a :class:`~openturns.MixtureClassifier`.

    See also
    --------
    MixtureClassifier, ExpertMixture

    Notes
    -----
    The classifier enables to define rules that assign a vector to a particular
    class.
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
        return _algo.ClassifierImplementation_getClassName(self)

    def getNumberOfClasses(self):
        """
        Accessor to the number of classes.

        Returns
        -------
        n_classes : int
            The number of classes
        """
        return _algo.ClassifierImplementation_getNumberOfClasses(self)

    def classify(self, *args):
        """
        Classify points according to the classifier.

        Parameters
        ----------
        input : sequence of float or 2-d a sequence of float
            A point or set of points to classify.

        Returns
        -------
        cls : int or :class:`~openturns.Indices`
            The class index of the input points, or indices of the classes of each points.
        """
        return _algo.ClassifierImplementation_classify(self, *args)

    def grade(self, *args):
        """
        Grade points according to the classifier.

        Parameters
        ----------
        inputPoint : sequence of float or 2-d a sequence of float
            A point or set of points to grade.
        k : int or sequence of int
            The class index, or class indices.

        Returns
        -------
        grade : float or :class:`~openturns.Point`
            Grade or list of grades of each input point with respect to each class index
        """
        return _algo.ClassifierImplementation_grade(self, *args)

    def __repr__(self):
        return _algo.ClassifierImplementation___repr__(self)

    def __str__(self, *args):
        return _algo.ClassifierImplementation___str__(self, *args)

    def setVerbose(self, verbose):
        """
        Accessor to the verbosity.

        Parameters
        ----------
        verb : bool
            Logical value telling if the verbose mode has been activated.
        """
        return _algo.ClassifierImplementation_setVerbose(self, verbose)

    def getVerbose(self):
        """
        Accessor to the verbosity.

        Returns
        -------
        verb : bool
            Logical value telling if the verbose mode has been activated.
        """
        return _algo.ClassifierImplementation_getVerbose(self)

    def getDimension(self):
        """
        Accessor to the dimension.

        Returns
        -------
        dim : int
            The dimension of the classifier.
        """
        return _algo.ClassifierImplementation_getDimension(self)

    def setParallel(self, flag):
        """
        Accessor to the parallel flag.

        Parameters
        ----------
        flag : bool
            Logical value telling if the classification and grading are done in parallel. 

        """
        return _algo.ClassifierImplementation_setParallel(self, flag)

    def isParallel(self):
        """
        Accessor to the parallel flag.

        Returns
        -------
        flag : bool
            Logical value telling if the parallel mode has been activated.

        """
        return _algo.ClassifierImplementation_isParallel(self)

    def __init__(self, *args):
        _algo.ClassifierImplementation_swiginit(self, _algo.new_ClassifierImplementation(*args))

    __swig_destroy__ = _algo.delete_ClassifierImplementation


_algo.ClassifierImplementation_swigregister(ClassifierImplementation)

class ClassifierImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _algo.ClassifierImplementationTypedInterfaceObject_swiginit(self, _algo.new_ClassifierImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _algo.ClassifierImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _algo.ClassifierImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _algo.ClassifierImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _algo.ClassifierImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _algo.ClassifierImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _algo.delete_ClassifierImplementationTypedInterfaceObject


_algo.ClassifierImplementationTypedInterfaceObject_swigregister(ClassifierImplementationTypedInterfaceObject)

class Classifier(ClassifierImplementationTypedInterfaceObject):
    """
    Classifier.

    Available constructors:
        Classifier(*classifierImp*)

    Parameters
    ----------
    classifierImp : classifier implementation
        A classifier implementation. It can be a :class:`~openturns.MixtureClassifier`.

    See also
    --------
    MixtureClassifier, ExpertMixture

    Notes
    -----
    The classifier enables to define rules that assign a vector to a particular
    class.
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
        return _algo.Classifier_getClassName(self)

    def getNumberOfClasses(self):
        """
        Accessor to the number of classes.

        Returns
        -------
        n_classes : int
            The number of classes
        """
        return _algo.Classifier_getNumberOfClasses(self)

    def classify(self, *args):
        """
        Classify points according to the classifier.

        Parameters
        ----------
        input : sequence of float or 2-d a sequence of float
            A point or set of points to classify.

        Returns
        -------
        cls : int or :class:`~openturns.Indices`
            The class index of the input points, or indices of the classes of each points.
        """
        return _algo.Classifier_classify(self, *args)

    def grade(self, *args):
        """
        Grade points according to the classifier.

        Parameters
        ----------
        inputPoint : sequence of float or 2-d a sequence of float
            A point or set of points to grade.
        k : int or sequence of int
            The class index, or class indices.

        Returns
        -------
        grade : float or :class:`~openturns.Point`
            Grade or list of grades of each input point with respect to each class index
        """
        return _algo.Classifier_grade(self, *args)

    def setParallel(self, flag):
        """
        Accessor to the parallel flag.

        Parameters
        ----------
        flag : bool
            Logical value telling if the classification and grading are done in parallel. 

        """
        return _algo.Classifier_setParallel(self, flag)

    def isParallel(self):
        """
        Accessor to the parallel flag.

        Returns
        -------
        flag : bool
            Logical value telling if the parallel mode has been activated.

        """
        return _algo.Classifier_isParallel(self)

    def getDimension(self):
        """
        Accessor to the dimension.

        Returns
        -------
        dim : int
            The dimension of the classifier.
        """
        return _algo.Classifier_getDimension(self)

    def setVerbose(self, verbose):
        """
        Accessor to the verbosity.

        Parameters
        ----------
        verb : bool
            Logical value telling if the verbose mode has been activated.
        """
        return _algo.Classifier_setVerbose(self, verbose)

    def getVerbose(self):
        """
        Accessor to the verbosity.

        Returns
        -------
        verb : bool
            Logical value telling if the verbose mode has been activated.
        """
        return _algo.Classifier_getVerbose(self)

    def __repr__(self):
        return _algo.Classifier___repr__(self)

    def __str__(self, *args):
        return _algo.Classifier___str__(self, *args)

    def __init__(self, *args):
        _algo.Classifier_swiginit(self, _algo.new_Classifier(*args))

    __swig_destroy__ = _algo.delete_Classifier


_algo.Classifier_swigregister(Classifier)

class FittingAlgorithmImplementation(openturns.common.PersistentObject):
    """
    Fitting algorithm.

    Available constructors:
        FittingAlgorithm(*fittingAlgoImp*)

    Parameters
    ----------
    fittingAlgoImp : a FittingAlgorithmImplementation
        A fitting algorithm implementation which is the
        :class:`~openturns.CorrectedLeaveOneOut` or :class:`~openturns.KFold`.

    See also
    --------
    CorrectedLeaveOneOut, KFold

    Notes
    -----
    FittingAlgorithm is the interface of the FittingAlgorithmImplementation.
    This class is not usable because it has sense only within the
    :class:`~openturns.FunctionalChaosAlgorithm`.
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
        return _algo.FittingAlgorithmImplementation_getClassName(self)

    def __repr__(self):
        return _algo.FittingAlgorithmImplementation___repr__(self)

    def run(self, *args):
        """
        Run the algorithm.

        Parameters
        ----------
        x : 2-d sequence of float
            Input sample
        y : 2-d sequence of float
            Output sample
        weight : sequence of float
            Weights associated to the outputs
        psi : sequence of :class:`~openturns.Function`
            Basis
        indices : sequence of int
            Indices of the basis

        Returns
        -------
        measure : float
            Fitting measure
        """
        return _algo.FittingAlgorithmImplementation_run(self, *args)

    def __init__(self, *args):
        _algo.FittingAlgorithmImplementation_swiginit(self, _algo.new_FittingAlgorithmImplementation(*args))

    __swig_destroy__ = _algo.delete_FittingAlgorithmImplementation


_algo.FittingAlgorithmImplementation_swigregister(FittingAlgorithmImplementation)

class FittingAlgorithmImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _algo.FittingAlgorithmImplementationTypedInterfaceObject_swiginit(self, _algo.new_FittingAlgorithmImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _algo.FittingAlgorithmImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _algo.FittingAlgorithmImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _algo.FittingAlgorithmImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _algo.FittingAlgorithmImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _algo.FittingAlgorithmImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _algo.delete_FittingAlgorithmImplementationTypedInterfaceObject


_algo.FittingAlgorithmImplementationTypedInterfaceObject_swigregister(FittingAlgorithmImplementationTypedInterfaceObject)

class FittingAlgorithm(FittingAlgorithmImplementationTypedInterfaceObject):
    """
    Fitting algorithm.

    Available constructors:
        FittingAlgorithm(*fittingAlgoImp*)

    Parameters
    ----------
    fittingAlgoImp : a FittingAlgorithmImplementation
        A fitting algorithm implementation which is the
        :class:`~openturns.CorrectedLeaveOneOut` or :class:`~openturns.KFold`.

    See also
    --------
    CorrectedLeaveOneOut, KFold

    Notes
    -----
    FittingAlgorithm is the interface of the FittingAlgorithmImplementation.
    This class is not usable because it has sense only within the
    :class:`~openturns.FunctionalChaosAlgorithm`.
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
        return _algo.FittingAlgorithm_getClassName(self)

    def __repr__(self):
        return _algo.FittingAlgorithm___repr__(self)

    def __str__(self, *args):
        return _algo.FittingAlgorithm___str__(self, *args)

    def run(self, *args):
        """
        Run the algorithm.

        Parameters
        ----------
        x : 2-d sequence of float
            Input sample
        y : 2-d sequence of float
            Output sample
        weight : sequence of float
            Weights associated to the outputs
        psi : sequence of :class:`~openturns.Function`
            Basis
        indices : sequence of int
            Indices of the basis

        Returns
        -------
        measure : float
            Fitting measure
        """
        return _algo.FittingAlgorithm_run(self, *args)

    def __init__(self, *args):
        _algo.FittingAlgorithm_swiginit(self, _algo.new_FittingAlgorithm(*args))

    __swig_destroy__ = _algo.delete_FittingAlgorithm


_algo.FittingAlgorithm_swigregister(FittingAlgorithm)

class KDTree(openturns.func.NearestNeighbourAlgorithmImplementation):
    """
    Partition tree data structure.

    Allows to store and search points fast.

    Available constructors:
        KDTree(*sample*)

    Parameters
    ----------
    sample : 2-d sequence of float
        Points.

    See also
    --------
    NearestNeighbourAlgorithm

    Examples
    --------
    >>> import openturns as ot
    >>> sample = ot.Normal(2).getSample(10)
    >>> tree = ot.KDTree(sample)
    >>> neighbour = sample[tree.query([0.1, 0.2])]
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
        return _algo.KDTree_getClassName(self)

    def getSample(self):
        """
        Get the points which have been used to build this nearest neighbour algorithm.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            Input points.
        """
        return _algo.KDTree_getSample(self)

    def setSample(self, sample):
        """
        Build a NearestNeighbourAlgorithm from these points.

        Parameters
        ----------
        sample : :class:`~openturns.Sample`
            Input points.
        """
        return _algo.KDTree_setSample(self, sample)

    def __repr__(self):
        return _algo.KDTree___repr__(self)

    def __str__(self, *args):
        return _algo.KDTree___str__(self, *args)

    def query(self, *args):
        """
        Get the index of the nearest neighbour of the given point.

        Available usages:
            query(*point*)

            query(*sample*)

        Parameters
        ----------
        point : sequence of float
            Given point.
        sample : 2-d sequence of float
            Given points.

        Returns
        -------
        index : int
            Index of the nearest neighbour of the given point.
        indices : :class:`openturns.Indices`
            Index of the nearest neighbour of the given points.
        """
        return _algo.KDTree_query(self, *args)

    def queryK(self, x, k, sorted=False):
        """
        Get the indices of nearest neighbours of the given point.

        Parameters
        ----------
        x : sequence of float
            Given point.
        k : int
            Number of indices to return.
        sorted : bool, optional
            Boolean to tell whether returned indices are sorted according to
            the distance to the given point.

        Returns
        -------
        indices : sequence of int
            Indices of the `k` nearest neighbours of the given point.
        """
        return _algo.KDTree_queryK(self, x, k, sorted)

    def __init__(self, *args):
        _algo.KDTree_swiginit(self, _algo.new_KDTree(*args))

    __swig_destroy__ = _algo.delete_KDTree


_algo.KDTree_swigregister(KDTree)

class RegularGridNearestNeighbour(openturns.func.NearestNeighbourAlgorithmImplementation):
    """
    Partition tree data structure.

    Allows to store and search points fast.

    Parameters
    ----------
    grid : :class:`~openturns.RegularGrid`
        Regular grid

    See also
    --------
    NearestNeighbourAlgorithm

    Examples
    --------
    >>> import openturns as ot
    >>> myRegularGrid = ot.RegularGrid(0.0, 0.1, 100)
    >>> tree = ot.RegularGridNearestNeighbour(myRegularGrid)
    >>> neighbour = tree.queryScalar(0.1)
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
        return _algo.RegularGridNearestNeighbour_getClassName(self)

    def __repr__(self):
        return _algo.RegularGridNearestNeighbour___repr__(self)

    def getSample(self):
        """
        Get the points which have been used to build this nearest neighbour algorithm.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            Input points.
        """
        return _algo.RegularGridNearestNeighbour_getSample(self)

    def setSample(self, sample):
        """
        Build a NearestNeighbourAlgorithm from these points.

        Parameters
        ----------
        sample : :class:`~openturns.Sample`
            Input points.
        """
        return _algo.RegularGridNearestNeighbour_setSample(self, sample)

    def query(self, *args):
        """
        Get the index of the nearest neighbour of the given point.

        Available usages:
            query(*point*)

            query(*sample*)

        Parameters
        ----------
        point : sequence of float
            Given point.
        sample : 2-d sequence of float
            Given points.

        Returns
        -------
        index : int
            Index of the nearest neighbour of the given point.
        indices : :class:`openturns.Indices`
            Index of the nearest neighbour of the given points.
        """
        return _algo.RegularGridNearestNeighbour_query(self, *args)

    def queryScalar(self, *args):
        """
        Accessor to the nearest neighbour index.

        Available usages:
            queryScalar(*x*)

            queryScalar(*point*)

        Parameters
        ----------
        x : float
            Given 1D point.
        point : sequence of float
            Sequence of 1D points.

        Returns
        -------
        index : int
            Index of the nearest neighbour.
        indices : :class:`openturns.Indices`
            Index of the nearest neighbour of the given points.
        """
        return _algo.RegularGridNearestNeighbour_queryScalar(self, *args)

    def queryK(self, x, k, sorted=False):
        """
        Get the indices of nearest neighbours of the given point.

        Parameters
        ----------
        x : sequence of float
            Given point.
        k : int
            Number of indices to return.
        sorted : bool, optional
            Boolean to tell whether returned indices are sorted according to
            the distance to the given point.

        Returns
        -------
        indices : sequence of int
            Indices of the `k` nearest neighbours of the given point.
        """
        return _algo.RegularGridNearestNeighbour_queryK(self, x, k, sorted)

    def queryScalarK(self, x, k, sorted=False):
        """
        Accessor to the nearest neighbours indices.

        Parameters
        ----------
        x : float
            Given 1D point.
        k : int
            Number of indices to return.
        sorted : bool
            Boolean to tell whether returned indices are sorted according to
            the distance to the given point.

        Returns
        -------
        indices : :class:`~openturns.Indices`
            Indices of the k nearest neighbours.
        """
        return _algo.RegularGridNearestNeighbour_queryScalarK(self, x, k, sorted)

    def __init__(self, *args):
        _algo.RegularGridNearestNeighbour_swiginit(self, _algo.new_RegularGridNearestNeighbour(*args))

    __swig_destroy__ = _algo.delete_RegularGridNearestNeighbour


_algo.RegularGridNearestNeighbour_swigregister(RegularGridNearestNeighbour)

class NearestNeighbour1D(openturns.func.NearestNeighbourAlgorithmImplementation):
    """
    Partition tree data structure for 1D points.

    Allows to store and search 1D points fast, by using
    dichotomy on sorted points.

    Parameters
    ----------
    sample : :class:`~openturns.Sample`
        1D points

    See also
    --------
    NearestNeighbourAlgorithm

    Examples
    --------
    >>> import openturns as ot
    >>> myRegularGrid = ot.RegularGrid(0.0, 0.1, 100)
    >>> tree = ot.NearestNeighbour1D([[x] for x in myRegularGrid.getValues()])
    >>> neighbour = tree.queryScalar(0.1)
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
        return _algo.NearestNeighbour1D_getClassName(self)

    def getSample(self):
        """
        Get the points which have been used to build this nearest neighbour algorithm.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            Input points.
        """
        return _algo.NearestNeighbour1D_getSample(self)

    def setSample(self, sample):
        """
        Build a NearestNeighbourAlgorithm from these points.

        Parameters
        ----------
        sample : :class:`~openturns.Sample`
            Input points.
        """
        return _algo.NearestNeighbour1D_setSample(self, sample)

    def __repr__(self):
        return _algo.NearestNeighbour1D___repr__(self)

    def __str__(self, *args):
        return _algo.NearestNeighbour1D___str__(self, *args)

    def query(self, *args):
        """
        Get the index of the nearest neighbour of the given point.

        Available usages:
            query(*point*)

            query(*sample*)

        Parameters
        ----------
        point : sequence of float
            Given point.
        sample : 2-d sequence of float
            Given points.

        Returns
        -------
        index : int
            Index of the nearest neighbour of the given point.
        indices : :class:`openturns.Indices`
            Index of the nearest neighbour of the given points.
        """
        return _algo.NearestNeighbour1D_query(self, *args)

    def queryScalar(self, *args):
        """
        Accessor to the nearest neighbour index.

        Available usages:
            queryScalar(*x*)

            queryScalar(*point*)

        Parameters
        ----------
        x : float
            Given 1D point.
        point : sequence of float
            Sequence of 1D points.

        Returns
        -------
        index : int
            Index of the nearest neighbour.
        indices : :class:`openturns.Indices`
            Index of the nearest neighbour of the given points.
        """
        return _algo.NearestNeighbour1D_queryScalar(self, *args)

    def queryK(self, x, k, sorted=False):
        """
        Get the indices of nearest neighbours of the given point.

        Parameters
        ----------
        x : sequence of float
            Given point.
        k : int
            Number of indices to return.
        sorted : bool, optional
            Boolean to tell whether returned indices are sorted according to
            the distance to the given point.

        Returns
        -------
        indices : sequence of int
            Indices of the `k` nearest neighbours of the given point.
        """
        return _algo.NearestNeighbour1D_queryK(self, x, k, sorted)

    def queryScalarK(self, x, k, sorted=False):
        """
        Accessor to the nearest neighbours indices.

        Parameters
        ----------
        x : float
            Given 1D point.
        k : int
            Number of indices to return.
        sorted : bool
            Boolean to tell whether returned indices are sorted according to
            the distance to the given point.

        Returns
        -------
        indices : :class:`~openturns.Indices`
            Indices of the k nearest neighbours.
        """
        return _algo.NearestNeighbour1D_queryScalarK(self, x, k, sorted)

    def __init__(self, *args):
        _algo.NearestNeighbour1D_swiginit(self, _algo.new_NearestNeighbour1D(*args))

    __swig_destroy__ = _algo.delete_NearestNeighbour1D


_algo.NearestNeighbour1D_swigregister(NearestNeighbour1D)

class NaiveNearestNeighbour(openturns.func.NearestNeighbourAlgorithmImplementation):
    """
    Brute force algorithm for nearest-neighbour lookup.

    Parameters
    ----------
    sample : 2-d sequence of float
        Points.

    See also
    --------
    NearestNeighbourAlgorithm

    Notes
    -----

    This algorithm compares distance to all points in input sample.
    It can be used when sample size is very small, or in high dimension.
    In other cases, KDTree is much faster.

    Examples
    --------
    >>> import openturns as ot
    >>> sample = ot.Normal(2).getSample(10)
    >>> tree = ot.NaiveNearestNeighbour(sample)
    >>> neighbour = sample[tree.query([0.1, 0.2])]
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
        return _algo.NaiveNearestNeighbour_getClassName(self)

    def getSample(self):
        """
        Get the points which have been used to build this nearest neighbour algorithm.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            Input points.
        """
        return _algo.NaiveNearestNeighbour_getSample(self)

    def setSample(self, sample):
        """
        Build a NearestNeighbourAlgorithm from these points.

        Parameters
        ----------
        sample : :class:`~openturns.Sample`
            Input points.
        """
        return _algo.NaiveNearestNeighbour_setSample(self, sample)

    def __repr__(self):
        return _algo.NaiveNearestNeighbour___repr__(self)

    def __str__(self, *args):
        return _algo.NaiveNearestNeighbour___str__(self, *args)

    def query(self, *args):
        """
        Get the index of the nearest neighbour of the given point.

        Available usages:
            query(*point*)

            query(*sample*)

        Parameters
        ----------
        point : sequence of float
            Given point.
        sample : 2-d sequence of float
            Given points.

        Returns
        -------
        index : int
            Index of the nearest neighbour of the given point.
        indices : :class:`openturns.Indices`
            Index of the nearest neighbour of the given points.
        """
        return _algo.NaiveNearestNeighbour_query(self, *args)

    def queryK(self, x, k, sorted=False):
        """
        Get the indices of nearest neighbours of the given point.

        Parameters
        ----------
        x : sequence of float
            Given point.
        k : int
            Number of indices to return.
        sorted : bool, optional
            Boolean to tell whether returned indices are sorted according to
            the distance to the given point.

        Returns
        -------
        indices : sequence of int
            Indices of the `k` nearest neighbours of the given point.
        """
        return _algo.NaiveNearestNeighbour_queryK(self, x, k, sorted)

    def __init__(self, *args):
        _algo.NaiveNearestNeighbour_swiginit(self, _algo.new_NaiveNearestNeighbour(*args))

    __swig_destroy__ = _algo.delete_NaiveNearestNeighbour


_algo.NaiveNearestNeighbour_swigregister(NaiveNearestNeighbour)

class NaiveEnclosingSimplex(openturns.geom.EnclosingSimplexAlgorithmImplementation):
    """
    Naive implementation of point location.

    This class implements a naive implementation of point location,
    by looking into all its simplices.  It works well for convex
    domains, but may be slow otherwise.

    Available constructors:
        NaiveEnclosingSimplex(*vertices, simplices*)

    Parameters
    ----------
    vertices : :class:`~openturns.Sample`
        Vertices.

    simplices : :class:`~openturns.IndicesCollection`
        Simplices.

    Notes
    -----

    In order to speed-up point location, a first pass is performed
    by looping over all simplices containing the nearest point.  If
    query point is not found in those simplices, then all simplices
    are looked for.

    See also
    --------
    EnclosingSimplexAlgorithm

    Examples
    --------
    >>> import openturns as ot
    >>> mesher = ot.IntervalMesher([5, 10])
    >>> lowerbound = [0.0, 0.0]
    >>> upperBound = [2.0, 4.0]
    >>> interval = ot.Interval(lowerbound, upperBound)
    >>> mesh = mesher.build(interval)
    >>> locator = ot.NaiveEnclosingSimplex(mesh.getVertices(), mesh.getSimplices())
    >>> simplex = locator.query([0.1, 0.2])
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
        return _algo.NaiveEnclosingSimplex_getClassName(self)

    def setVerticesAndSimplices(self, vertices, simplices):
        """
        Rebuild a new data structure for these vertices and simplices.

        Parameters
        ----------
        vertices : :class:`~openturns.Sample`
            Vertices.

        simplices : :class:`~openturns.IndicesCollection`
            Simplices.
        """
        return _algo.NaiveEnclosingSimplex_setVerticesAndSimplices(self, vertices, simplices)

    def getNearestNeighbourAlgorithm(self):
        """
        Accessor to the nearest neighbour algorithm.

        Returns
        -------
        nearestNeighbour : :class:`~openturns.NearestNeighbourAlgorithm`
            Algorithm used during first pass to locate the nearest point.
        """
        return _algo.NaiveEnclosingSimplex_getNearestNeighbourAlgorithm(self)

    def setNearestNeighbourAlgorithm(self, nearestNeighbour):
        """
        Accessor to the nearest neighbour algorithm.

        Parameters
        ----------
        nearestNeighbour : :class:`~openturns.NearestNeighbourAlgorithm`
            Algorithm to use during first pass to locate the nearest point.
        """
        return _algo.NaiveEnclosingSimplex_setNearestNeighbourAlgorithm(self, nearestNeighbour)

    def query(self, *args):
        """
        Get the index of the enclosing simplex of the given point.

        Available usages:
            query(*point*)

            query(*sample*)

        Parameters
        ----------
        point : sequence of float
            Given point.
        sample : 2-d sequence of float
            Given points.

        Returns
        -------
        index : int
            If point is enclosed in a simplex, return its index; otherwise return an
            int which is at least greater than the number of simplices.
        indices : :class:`openturns.Indices`
            Index of enclosing simplex of each point of the sample.  If there is no
            enclosing simplex, value is an int which is at least greater than the
            number of simplices.
        """
        return _algo.NaiveEnclosingSimplex_query(self, *args)

    def __repr__(self):
        return _algo.NaiveEnclosingSimplex___repr__(self)

    def __str__(self, *args):
        return _algo.NaiveEnclosingSimplex___str__(self, *args)

    def __init__(self, *args):
        _algo.NaiveEnclosingSimplex_swiginit(self, _algo.new_NaiveEnclosingSimplex(*args))

    __swig_destroy__ = _algo.delete_NaiveEnclosingSimplex


_algo.NaiveEnclosingSimplex_swigregister(NaiveEnclosingSimplex)

class EnclosingSimplexMonotonic1D(openturns.geom.EnclosingSimplexAlgorithmImplementation):
    """
    Specialized point location algorithm for monotonic 1D  meshes.

    Available constructors:
        EnclosingSimplexMonotonic1D(*points*)

    Parameters
    ----------
    points : 2-d sequence of float
        Points.

    See also
    --------
    EnclosingSimplexAlgorithm

    Examples
    --------
    >>> import openturns as ot
    >>> mesh = ot.Mesh([[0.0], [0.04],[0.1], [0.2],[0.5], [1.0]])
    >>> locator = ot.EnclosingSimplexMonotonic1D(mesh.getVertices())
    >>> simplex = locator.query([0.62])
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
        return _algo.EnclosingSimplexMonotonic1D_getClassName(self)

    def setVerticesAndSimplices(self, vertices, simplices):
        """
        Rebuild a new data structure for these vertices and simplices.

        Parameters
        ----------
        vertices : :class:`~openturns.Sample`
            Vertices.

        simplices : :class:`~openturns.IndicesCollection`
            Simplices.
        """
        return _algo.EnclosingSimplexMonotonic1D_setVerticesAndSimplices(self, vertices, simplices)

    def query(self, *args):
        """
        Get the index of the enclosing simplex of the given point.

        Available usages:
            query(*point*)

            query(*sample*)

        Parameters
        ----------
        point : sequence of float
            Given point.
        sample : 2-d sequence of float
            Given points.

        Returns
        -------
        index : int
            If point is enclosed in a simplex, return its index; otherwise return an
            int which is at least greater than the number of simplices.
        indices : :class:`openturns.Indices`
            Index of enclosing simplex of each point of the sample.  If there is no
            enclosing simplex, value is an int which is at least greater than the
            number of simplices.
        """
        return _algo.EnclosingSimplexMonotonic1D_query(self, *args)

    def queryScalar(self, *args):
        """
        Accessor to the enclosing simplex index.

        Available usages:
            queryScalar(*x*)

            queryScalar(*point*)

        Parameters
        ----------
        x : float
            Given point.
        point : sequence of float
            Sequence of 1D points.

        Returns
        -------
        index : int
            If *x* is inside RegularGrid bounds, return the index of the interval
            in  which it is contained; otherwise return an int which is at least
            greater than the number of intervals.
        indices : :class:`openturns.Indices`
            Index of the enclosing simplex of the given 1D points.
        """
        return _algo.EnclosingSimplexMonotonic1D_queryScalar(self, *args)

    def __repr__(self):
        return _algo.EnclosingSimplexMonotonic1D___repr__(self)

    def __str__(self, *args):
        return _algo.EnclosingSimplexMonotonic1D___str__(self, *args)

    def __init__(self, *args):
        _algo.EnclosingSimplexMonotonic1D_swiginit(self, _algo.new_EnclosingSimplexMonotonic1D(*args))

    __swig_destroy__ = _algo.delete_EnclosingSimplexMonotonic1D


_algo.EnclosingSimplexMonotonic1D_swigregister(EnclosingSimplexMonotonic1D)

class RegularGridEnclosingSimplex(openturns.geom.EnclosingSimplexAlgorithmImplementation):
    """
    Specialized point location algorithm on RegularGrid.

    Available constructors:
        RegularGridEnclosingSimplex(*regularGrid*)

    Parameters
    ----------
    regularGrid : :class:`~openturns.RegularGrid`
        Points

    See also
    --------
    EnclosingSimplexAlgorithm

    Examples
    --------
    >>> import openturns as ot
    >>> grid = ot.RegularGrid(0, 0.1, 20)
    >>> locator = ot.RegularGridEnclosingSimplex(grid)
    >>> simplex = locator.query([0.12])
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
        return _algo.RegularGridEnclosingSimplex_getClassName(self)

    def setVerticesAndSimplices(self, vertices, simplices):
        """
        Rebuild a new data structure for these vertices and simplices.

        Parameters
        ----------
        vertices : :class:`~openturns.Sample`
            Vertices.

        simplices : :class:`~openturns.IndicesCollection`
            Simplices.
        """
        return _algo.RegularGridEnclosingSimplex_setVerticesAndSimplices(self, vertices, simplices)

    def query(self, *args):
        """
        Get the index of the enclosing simplex of the given point.

        Available usages:
            query(*point*)

            query(*sample*)

        Parameters
        ----------
        point : sequence of float
            Given point.
        sample : 2-d sequence of float
            Given points.

        Returns
        -------
        index : int
            If point is enclosed in a simplex, return its index; otherwise return an
            int which is at least greater than the number of simplices.
        indices : :class:`openturns.Indices`
            Index of enclosing simplex of each point of the sample.  If there is no
            enclosing simplex, value is an int which is at least greater than the
            number of simplices.
        """
        return _algo.RegularGridEnclosingSimplex_query(self, *args)

    def queryScalar(self, *args):
        """
        Accessor to the enclosing simplex index.

        Available usages:
            queryScalar(*x*)

            queryScalar(*point*)

        Parameters
        ----------
        x : float
            Given point.
        point : sequence of float
            Sequence of 1D points.

        Returns
        -------
        index : int
            If *x* is inside RegularGrid bounds, return the index of the interval
            in  which it is contained; otherwise return an int which is at least
            greater than the number of intervals.
        indices : :class:`openturns.Indices`
            Index of the enclosing simplex of the given 1D points.
        """
        return _algo.RegularGridEnclosingSimplex_queryScalar(self, *args)

    def __repr__(self):
        return _algo.RegularGridEnclosingSimplex___repr__(self)

    def __str__(self, *args):
        return _algo.RegularGridEnclosingSimplex___str__(self, *args)

    def __init__(self, *args):
        _algo.RegularGridEnclosingSimplex_swiginit(self, _algo.new_RegularGridEnclosingSimplex(*args))

    __swig_destroy__ = _algo.delete_RegularGridEnclosingSimplex


_algo.RegularGridEnclosingSimplex_swigregister(RegularGridEnclosingSimplex)

class BoundingVolumeHierarchy(openturns.geom.EnclosingSimplexAlgorithmImplementation):
    """
    Bounding Volume Hierarchy to speed-up point location.

    This spatial data structure helps to find the simplex
    containing a given point.

    Available constructors:
        BoundingVolumeHierarchy(*points, simplices*)

        BoundingVolumeHierarchy(*points, simplices, binNumber*)

        BoundingVolumeHierarchy(*points, simplices, binNumber, strategy*)

    Parameters
    ----------
    points : 2-d sequence of float
        Points.

    simplices : :class:`~openturns.IndicesCollection`
        Simplices.

    binNumber : int
        Maximum number of simplices stored in tree leaves.
        By default, it is equal to the value defined through the key
        BoundingVolumeHierarchy-BinNumber of the
        :class:`~openturns.ResourceMap`.

    strategy : str
        Node splitting strategy.  Valid values are: `Mean` and `Median`.
        By default, it is equal to the value defined through the key
        BoundingVolumeHierarchy-Strategy of the
        :class:`~openturns.ResourceMap` (`Mean`).

    See also
    --------
    EnclosingSimplexAlgorithm

    Examples
    --------
    >>> import openturns as ot
    >>> mesher = ot.IntervalMesher([5, 10])
    >>> lowerbound = [0.0, 0.0]
    >>> upperBound = [2.0, 4.0]
    >>> interval = ot.Interval(lowerbound, upperBound)
    >>> mesh = mesher.build(interval)
    >>> locator = ot.BoundingVolumeHierarchy(mesh.getVertices(), mesh.getSimplices())
    >>> simplex = locator.query([0.1, 0.2])
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
        return _algo.BoundingVolumeHierarchy_getClassName(self)

    def setVerticesAndSimplices(self, vertices, simplices):
        """
        Rebuild a new data structure for these vertices and simplices.

        Parameters
        ----------
        vertices : :class:`~openturns.Sample`
            Vertices.

        simplices : :class:`~openturns.IndicesCollection`
            Simplices.
        """
        return _algo.BoundingVolumeHierarchy_setVerticesAndSimplices(self, vertices, simplices)

    def query(self, *args):
        """
        Get the index of the enclosing simplex of the given point.

        Available usages:
            query(*point*)

            query(*sample*)

        Parameters
        ----------
        point : sequence of float
            Given point.
        sample : 2-d sequence of float
            Given points.

        Returns
        -------
        index : int
            If point is enclosed in a simplex, return its index; otherwise return an
            int which is at least greater than the number of simplices.
        indices : :class:`openturns.Indices`
            Index of enclosing simplex of each point of the sample.  If there is no
            enclosing simplex, value is an int which is at least greater than the
            number of simplices.
        """
        return _algo.BoundingVolumeHierarchy_query(self, *args)

    def __repr__(self):
        return _algo.BoundingVolumeHierarchy___repr__(self)

    def __str__(self, *args):
        return _algo.BoundingVolumeHierarchy___str__(self, *args)

    def __init__(self, *args):
        _algo.BoundingVolumeHierarchy_swiginit(self, _algo.new_BoundingVolumeHierarchy(*args))

    __swig_destroy__ = _algo.delete_BoundingVolumeHierarchy


_algo.BoundingVolumeHierarchy_swigregister(BoundingVolumeHierarchy)

class KFold(FittingAlgorithmImplementation):
    """
    K-fold.

    Available constructors:
        KFold()

        KFold(*k*)

    Parameters
    ----------
    k : positive integer
        Number of folds in which the sample is splitted. If not provided, default is
        :math:`k = 10`.

    See also
    --------
    FittingAlgorithm, CorrectedLeaveOneOut

    Notes
    -----
    KFold inherits from :class:`~openturns.FittingAlgorithm`.

    This class is not usable because it has sense only whithin the
    :class:`~openturns.FunctionalChaosAlgorithm`.
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
        return _algo.KFold_getClassName(self)

    def __repr__(self):
        return _algo.KFold___repr__(self)

    def run(self, x, y, weight, basis, indices):
        """
        Run the algorithm.

        Parameters
        ----------
        x : 2-d sequence of float
            Input sample
        y : 2-d sequence of float
            Output sample
        weight : sequence of float
            Weights associated to the outputs
        psi : sequence of :class:`~openturns.Function`
            Basis
        indices : sequence of int
            Indices of the basis

        Returns
        -------
        measure : float
            Fitting measure
        """
        return _algo.KFold_run(self, x, y, weight, basis, indices)

    def setK(self, p):
        """
        Accessor to the number of folds.

        Parameters
        ----------
        k : integer
            Number of folds in which the sample is splitted.
        """
        return _algo.KFold_setK(self, p)

    def getK(self):
        """
        Accessor to the number of folds.

        Returns
        -------
        k : integer
            Number of folds in which the sample is splitted.
        """
        return _algo.KFold_getK(self)

    def __init__(self, *args):
        _algo.KFold_swiginit(self, _algo.new_KFold(*args))

    __swig_destroy__ = _algo.delete_KFold


_algo.KFold_swigregister(KFold)

class CorrectedLeaveOneOut(FittingAlgorithmImplementation):
    """
    Corrected leave one out.

    Available constructors:
        CorrectedLeaveOneOut()

    See also
    --------
    FittingAlgorithm, KFold

    Notes
    -----
    CorrectedLeaveOneOut inherits from :class:`~openturns.FittingAlgorithm`.

    This class is not usable because it has sense only whithin the
    :class:`~openturns.FunctionalChaosAlgorithm`.
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
        return _algo.CorrectedLeaveOneOut_getClassName(self)

    def __repr__(self):
        return _algo.CorrectedLeaveOneOut___repr__(self)

    def run(self, x, y, weight, psi, indices):
        """
        Run the algorithm.

        Parameters
        ----------
        x : 2-d sequence of float
            Input sample
        y : 2-d sequence of float
            Output sample
        weight : sequence of float
            Weights associated to the outputs
        psi : sequence of :class:`~openturns.Function`
            Basis
        indices : sequence of int
            Indices of the basis

        Returns
        -------
        measure : float
            Fitting measure
        """
        return _algo.CorrectedLeaveOneOut_run(self, x, y, weight, psi, indices)

    def __init__(self, *args):
        _algo.CorrectedLeaveOneOut_swiginit(self, _algo.new_CorrectedLeaveOneOut(*args))

    __swig_destroy__ = _algo.delete_CorrectedLeaveOneOut


_algo.CorrectedLeaveOneOut_swigregister(CorrectedLeaveOneOut)

class DesignProxy(openturns.common.Object):
    """
    Design matrix cache.

    Available constructors:
        DesignProxy(*x, basis*)

        DesignProxy(*matrix*)

    Parameters
    ----------
    x : :class:`~openturns.Sample`
        Input sample
    psi : sequence of :class:`~openturns.Function`
        Basis
    matrix : 2-d sequence of float
    The design matrix

    Notes
    -----
    Helps to cache evaluations of the design matrix. Can be useful for an iterative
    least squares problem resolution or in interaction with :class:`~openturns.LeastSquaresMethod`
    to select the algorithm used for the resolution of linear least-squares problems.

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
        return _algo.DesignProxy_getClassName(self)

    def __repr__(self):
        return _algo.DesignProxy___repr__(self)

    def getInputSample(self):
        """
        Input sample accessor.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            Input sample.
        """
        return _algo.DesignProxy_getInputSample(self)

    def getBasis(self):
        """
        Accessor to the basis.

        Returns
        -------
        basis : collection of :class:`~openturns.Function`
            Basis.
        """
        return _algo.DesignProxy_getBasis(self)

    def computeDesign(self, indices):
        """
        Build the design matrix.

        Parameters
        ----------
        indices : sequence of int
            Indices of the current basis in the global basis

        Returns
        -------
        psiAk : :class:`~openturns.Matrix`
            The design matrix
        """
        return _algo.DesignProxy_computeDesign(self, indices)

    def setRowFilter(self, rowFilter):
        """
        Row filter accessor.

        Parameters
        ----------
        rowFilter : sequence of int
            Sub-indices in of the sample in the current indices
        """
        return _algo.DesignProxy_setRowFilter(self, rowFilter)

    def getRowFilter(self):
        """
        Row filter accessor.

        Returns
        -------
        rowFilter : :class:`~openturns.Indices`
            Sub-indices in of the sample in the current indices
        """
        return _algo.DesignProxy_getRowFilter(self)

    def hasRowFilter(self):
        """
        Row filter flag accessor.

        Returns
        -------
        hasRowFilter : bool
            Whether sub-indices of the basis are set
        """
        return _algo.DesignProxy_hasRowFilter(self)

    def getSampleSize(self):
        """
        Sample size accessor.

        Returns
        -------
        sampleSize : int
            Size of sample accounting for row filter
        """
        return _algo.DesignProxy_getSampleSize(self)

    def setWeight(self, weight):
        """
        Accessor to the weights.

        Parameters
        ----------
        weight : sequence of float
            Weights on each basis term
        """
        return _algo.DesignProxy_setWeight(self, weight)

    def getWeight(self):
        """
        Accessor to the weights.

        Returns
        -------
        weight : :class:`~openturns.Point`
            Weights on each basis term
        """
        return _algo.DesignProxy_getWeight(self)

    def hasWeight(self):
        """
        Weight flag accessor.

        Returns
        -------
        hasWeight : bool
            Whether weights are set
        """
        return _algo.DesignProxy_hasWeight(self)

    def __init__(self, *args):
        _algo.DesignProxy_swiginit(self, _algo.new_DesignProxy(*args))

    __swig_destroy__ = _algo.delete_DesignProxy


_algo.DesignProxy_swigregister(DesignProxy)

class LeastSquaresMethodImplementation(openturns.common.PersistentObject):
    r"""
    Base class for least square solvers.

    Available constructors:
        LeastSquaresMethod(*proxy, weight, indices*)

        LeastSquaresMethod(*proxy, indices*)

        LeastSquaresMethod(*design*)

    Parameters
    ----------
    proxy : :class:`~openturns.DesignProxy`
        Input sample
    weight : sequence of float
        Output weights
    indices : sequence of int
        Indices allowed in the basis
    design : 2-d sequence of float
        A priori known design matrix

    See also
    --------
    CholeskyMethod, SVDMethod, QRMethod

    Notes
    -----
    Solve the least-squares problem:

    .. math::

        \vect{a} = \argmin_{\vect{b} \in \Rset^P} ||y - \vect{b}^{\intercal} \vect{\Psi}(\vect{U})||^2

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
        return _algo.LeastSquaresMethodImplementation_getClassName(self)

    def __repr__(self):
        return _algo.LeastSquaresMethodImplementation___repr__(self)

    def getInputSample(self):
        """
        Input sample accessor.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            Input sample.
        """
        return _algo.LeastSquaresMethodImplementation_getInputSample(self)

    def getWeight(self):
        """
        Accessor to the weights.

        Returns
        -------
        weight : :class:`~openturns.Point`
            Weights.
        """
        return _algo.LeastSquaresMethodImplementation_getWeight(self)

    def getBasis(self):
        """
        Accessor to the basis.

        Returns
        -------
        basis : collection of :class:`~openturns.Function`
            Basis.
        """
        return _algo.LeastSquaresMethodImplementation_getBasis(self)

    def getCurrentIndices(self):
        """
        Current indices accessor.

        Returns
        -------
        indices : :class:`~openturns.Indices`
            Indices of the current decomposition in the global basis.
        """
        return _algo.LeastSquaresMethodImplementation_getCurrentIndices(self)

    def getInitialIndices(self):
        """
        Initial indices accessor.

        Returns
        -------
        indices : :class:`~openturns.Indices`
            Initial indices of the terms in the global basis.
        """
        return _algo.LeastSquaresMethodImplementation_getInitialIndices(self)

    def solve(self, rhs):
        r"""
        Solve the least-squares problem.

        .. math::

            \vect{a} = \argmin_{\vect{x} \in \Rset^P} ||M\vect{x}-\vect{b}||^2

        Parameters
        ----------
        b : sequence of float
            Second term of the equation

        Returns
        -------
        a : :class:`~openturns.Point`
            The solution.
        """
        return _algo.LeastSquaresMethodImplementation_solve(self, rhs)

    def solveNormal(self, rhs):
        """
        Solve the least-squares problem using normal equation.

        .. math::

            M^T*M*x=M^T*b

        Parameters
        ----------
        b : sequence of float
            Second term of the equation

        Returns
        -------
        x : :class:`~openturns.Point`
            The solution.
        """
        return _algo.LeastSquaresMethodImplementation_solveNormal(self, rhs)

    def getGramInverse(self):
        """
        Get the inverse Gram matrix of input sample.

        .. math::

            G^{-1} = (X^T * X)^{-1}

        Returns
        -------
        c : :class:`~openturns.CovarianceMatrix`
            The inverse Gram matrix.
        """
        return _algo.LeastSquaresMethodImplementation_getGramInverse(self)

    def getH(self):
        """
        Get the projection matrix H.

        .. math::

            H = X * (X^T * X)^{-1} * X^T

        Returns
        -------
        h : :class:`~openturns.SymmetricMatrix`
            The projection matrix H.
        """
        return _algo.LeastSquaresMethodImplementation_getH(self)

    def getHDiag(self):
        """
        Get the diagonal of the projection matrix H.

        .. math::

            H = X * (X^T * X)^{-1} * X^T

        Returns
        -------
        d : :class:`~openturns.Point`
            The diagonal of H.
        """
        return _algo.LeastSquaresMethodImplementation_getHDiag(self)

    def getGramInverseDiag(self):
        """
        Get the diagonal of the inverse Gram matrix.

        .. math::

            diag(G^{-1}) = diag((X^T * X)^{-1})

        Returns
        -------
        d : :class:`~openturns.Point`
            The diagonal of the inverse Gram matrix.
        """
        return _algo.LeastSquaresMethodImplementation_getGramInverseDiag(self)

    def getGramInverseTrace(self):
        """
        Get the trace of the inverse Gram matrix.

        .. math::

            Tr(G^{-1}) = Tr(x^T * x)^{-1}

        Returns
        -------
        x : :class:`~openturns.Scalar`
            The trace of inverse Gram matrix.
        """
        return _algo.LeastSquaresMethodImplementation_getGramInverseTrace(self)

    def update(self, addedIndices, conservedIndices, removedIndices, row=False):
        """
        Update the current decomposition.

        Parameters
        ----------
        addedIndices : sequence of int
            Indices of added basis terms.
        conservedIndices : sequence of int
            Indices of conserved basis terms.
        removedIndices : sequence of int
            Indices of removed basis terms.
        """
        return _algo.LeastSquaresMethodImplementation_update(self, addedIndices, conservedIndices, removedIndices, row)

    def trashDecomposition(self):
        """Drop the current decomposition."""
        return _algo.LeastSquaresMethodImplementation_trashDecomposition(self)

    def computeWeightedDesign(self, whole=False):
        """
        Build the design matrix.

        Parameters
        ----------
        whole : bool, defaults to False
            Whether to use the initial indices instead of the current indices

        Returns
        -------
        psiAk : :class:`~openturns.Matrix`
            The design matrix
        """
        return _algo.LeastSquaresMethodImplementation_computeWeightedDesign(self, whole)

    def __init__(self, *args):
        _algo.LeastSquaresMethodImplementation_swiginit(self, _algo.new_LeastSquaresMethodImplementation(*args))

    __swig_destroy__ = _algo.delete_LeastSquaresMethodImplementation


_algo.LeastSquaresMethodImplementation_swigregister(LeastSquaresMethodImplementation)

class LeastSquaresMethodImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _algo.LeastSquaresMethodImplementationTypedInterfaceObject_swiginit(self, _algo.new_LeastSquaresMethodImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _algo.LeastSquaresMethodImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _algo.LeastSquaresMethodImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _algo.LeastSquaresMethodImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _algo.LeastSquaresMethodImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _algo.LeastSquaresMethodImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _algo.delete_LeastSquaresMethodImplementationTypedInterfaceObject


_algo.LeastSquaresMethodImplementationTypedInterfaceObject_swigregister(LeastSquaresMethodImplementationTypedInterfaceObject)

class LeastSquaresMethod(LeastSquaresMethodImplementationTypedInterfaceObject):
    r"""
    Base class for least square solvers.

    Available constructors:
        LeastSquaresMethod(*proxy, weight, indices*)

        LeastSquaresMethod(*proxy, indices*)

        LeastSquaresMethod(*design*)

    Parameters
    ----------
    proxy : :class:`~openturns.DesignProxy`
        Input sample
    weight : sequence of float
        Output weights
    indices : sequence of int
        Indices allowed in the basis
    design : 2-d sequence of float
        A priori known design matrix

    See also
    --------
    CholeskyMethod, SVDMethod, QRMethod

    Notes
    -----
    Solve the least-squares problem:

    .. math::

        \vect{a} = \argmin_{\vect{b} \in \Rset^P} ||y - \vect{b}^{\intercal} \vect{\Psi}(\vect{U})||^2

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
        return _algo.LeastSquaresMethod_getClassName(self)

    def __repr__(self):
        return _algo.LeastSquaresMethod___repr__(self)

    def __str__(self, *args):
        return _algo.LeastSquaresMethod___str__(self, *args)

    def getInputSample(self):
        """
        Input sample accessor.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            Input sample.
        """
        return _algo.LeastSquaresMethod_getInputSample(self)

    def getWeight(self):
        """
        Accessor to the weights.

        Returns
        -------
        weight : :class:`~openturns.Point`
            Weights.
        """
        return _algo.LeastSquaresMethod_getWeight(self)

    def getBasis(self):
        """
        Accessor to the basis.

        Returns
        -------
        basis : collection of :class:`~openturns.Function`
            Basis.
        """
        return _algo.LeastSquaresMethod_getBasis(self)

    def getCurrentIndices(self):
        """
        Current indices accessor.

        Returns
        -------
        indices : :class:`~openturns.Indices`
            Indices of the current decomposition in the global basis.
        """
        return _algo.LeastSquaresMethod_getCurrentIndices(self)

    def getInitialIndices(self):
        """
        Initial indices accessor.

        Returns
        -------
        indices : :class:`~openturns.Indices`
            Initial indices of the terms in the global basis.
        """
        return _algo.LeastSquaresMethod_getInitialIndices(self)

    def solve(self, rhs):
        r"""
        Solve the least-squares problem.

        .. math::

            \vect{a} = \argmin_{\vect{x} \in \Rset^P} ||M\vect{x}-\vect{b}||^2

        Parameters
        ----------
        b : sequence of float
            Second term of the equation

        Returns
        -------
        a : :class:`~openturns.Point`
            The solution.
        """
        return _algo.LeastSquaresMethod_solve(self, rhs)

    def solveNormal(self, rhs):
        """
        Solve the least-squares problem using normal equation.

        .. math::

            M^T*M*x=M^T*b

        Parameters
        ----------
        b : sequence of float
            Second term of the equation

        Returns
        -------
        x : :class:`~openturns.Point`
            The solution.
        """
        return _algo.LeastSquaresMethod_solveNormal(self, rhs)

    def getHDiag(self):
        """
        Get the diagonal of the projection matrix H.

        .. math::

            H = X * (X^T * X)^{-1} * X^T

        Returns
        -------
        d : :class:`~openturns.Point`
            The diagonal of H.
        """
        return _algo.LeastSquaresMethod_getHDiag(self)

    def getH(self):
        """
        Get the projection matrix H.

        .. math::

            H = X * (X^T * X)^{-1} * X^T

        Returns
        -------
        h : :class:`~openturns.SymmetricMatrix`
            The projection matrix H.
        """
        return _algo.LeastSquaresMethod_getH(self)

    def getGramInverse(self):
        """
        Get the inverse Gram matrix of input sample.

        .. math::

            G^{-1} = (X^T * X)^{-1}

        Returns
        -------
        c : :class:`~openturns.CovarianceMatrix`
            The inverse Gram matrix.
        """
        return _algo.LeastSquaresMethod_getGramInverse(self)

    def getGramInverseDiag(self):
        """
        Get the diagonal of the inverse Gram matrix.

        .. math::

            diag(G^{-1}) = diag((X^T * X)^{-1})

        Returns
        -------
        d : :class:`~openturns.Point`
            The diagonal of the inverse Gram matrix.
        """
        return _algo.LeastSquaresMethod_getGramInverseDiag(self)

    def getGramInverseTrace(self):
        """
        Get the trace of the inverse Gram matrix.

        .. math::

            Tr(G^{-1}) = Tr(x^T * x)^{-1}

        Returns
        -------
        x : :class:`~openturns.Scalar`
            The trace of inverse Gram matrix.
        """
        return _algo.LeastSquaresMethod_getGramInverseTrace(self)

    def update(self, addedIndices, conservedIndices, removedIndices, row=False):
        """
        Update the current decomposition.

        Parameters
        ----------
        addedIndices : sequence of int
            Indices of added basis terms.
        conservedIndices : sequence of int
            Indices of conserved basis terms.
        removedIndices : sequence of int
            Indices of removed basis terms.
        """
        return _algo.LeastSquaresMethod_update(self, addedIndices, conservedIndices, removedIndices, row)

    def computeWeightedDesign(self, whole=False):
        """
        Build the design matrix.

        Parameters
        ----------
        whole : bool, defaults to False
            Whether to use the initial indices instead of the current indices

        Returns
        -------
        psiAk : :class:`~openturns.Matrix`
            The design matrix
        """
        return _algo.LeastSquaresMethod_computeWeightedDesign(self, whole)

    @staticmethod
    def Build(*args):
        """
        Instanciate a decomposition method from its name.

        Parameters
        ----------
        name : str
            The name of the least-squares method
            Values are 'QR', 'SVD', 'Cholesky'
        proxy : :class:`~openturns.DesignProxy`
            Input sample
        weight : sequence of float, optional
            Output weights
        indices : sequence of int
            Indices allowed in the basis
        design : 2-d sequence of float
            A priori known design matrix

        Returns
        -------
        method : :class:`~openturns.LeastSquaresMethod`
            The built method
        """
        return _algo.LeastSquaresMethod_Build(*args)

    def __init__(self, *args):
        _algo.LeastSquaresMethod_swiginit(self, _algo.new_LeastSquaresMethod(*args))

    __swig_destroy__ = _algo.delete_LeastSquaresMethod


_algo.LeastSquaresMethod_swigregister(LeastSquaresMethod)

def LeastSquaresMethod_Build(*args):
    """
    Instanciate a decomposition method from its name.

    Parameters
    ----------
    name : str
        The name of the least-squares method
        Values are 'QR', 'SVD', 'Cholesky'
    proxy : :class:`~openturns.DesignProxy`
        Input sample
    weight : sequence of float, optional
        Output weights
    indices : sequence of int
        Indices allowed in the basis
    design : 2-d sequence of float
        A priori known design matrix

    Returns
    -------
    method : :class:`~openturns.LeastSquaresMethod`
        The built method
    """
    return _algo.LeastSquaresMethod_Build(*args)


class CholeskyMethod(LeastSquaresMethodImplementation):
    """
    Least squares solver using Cholesky decomposition.

    Available constructors:
        CholeskyMethod(*proxy, weight, indices*)

        CholeskyMethod(*proxy, indices*)

        CholeskyMethod(*design*)

    Parameters
    ----------
    proxy : :class:`~openturns.DesignProxy`
        Input sample
    weight : sequence of float
        Output weights
    indices : sequence of int
        Indices allowed in the basis
    design : 2-d sequence of float
        A priori known design matrix

    See also
    --------
    LeastSquaresMethod, SVDMethod, QRMethod

    Examples
    --------
    Solves a linear least squares problem with Cholesky method:

    >>> import openturns as ot
    >>> A = ot.Matrix([[1,1],[1,2],[1,3],[1,4]])
    >>> y = ot.Point([6,5,7,10])
    >>> method = ot.CholeskyMethod(A)
    >>> x = method.solve(y)
    >>> print(x)
    [3.5,1.4]
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
        return _algo.CholeskyMethod_getClassName(self)

    def __repr__(self):
        return _algo.CholeskyMethod___repr__(self)

    def solve(self, rhs):
        r"""
        Solve the least-squares problem.

        .. math::

            \vect{a} = \argmin_{\vect{x} \in \Rset^P} ||M\vect{x}-\vect{b}||^2

        Parameters
        ----------
        b : sequence of float
            Second term of the equation

        Returns
        -------
        a : :class:`~openturns.Point`
            The solution.
        """
        return _algo.CholeskyMethod_solve(self, rhs)

    def solveNormal(self, rhs):
        """
        Solve the least-squares problem using normal equation.

        .. math::

            M^T*M*x=M^T*b

        Parameters
        ----------
        b : sequence of float
            Second term of the equation

        Returns
        -------
        x : :class:`~openturns.Point`
            The solution.
        """
        return _algo.CholeskyMethod_solveNormal(self, rhs)

    def update(self, addedIndices, conservedIndices, removedIndices, row=False):
        """
        Update the current decomposition.

        Parameters
        ----------
        addedIndices : sequence of int
            Indices of added basis terms.
        conservedIndices : sequence of int
            Indices of conserved basis terms.
        removedIndices : sequence of int
            Indices of removed basis terms.
        """
        return _algo.CholeskyMethod_update(self, addedIndices, conservedIndices, removedIndices, row)

    def trashDecomposition(self):
        """Drop the current decomposition."""
        return _algo.CholeskyMethod_trashDecomposition(self)

    def getGramInverse(self):
        """
        Get the inverse Gram matrix of input sample.

        .. math::

            G^{-1} = (X^T * X)^{-1}

        Returns
        -------
        c : :class:`~openturns.CovarianceMatrix`
            The inverse Gram matrix.
        """
        return _algo.CholeskyMethod_getGramInverse(self)

    def getH(self):
        """
        Get the projection matrix H.

        .. math::

            H = X * (X^T * X)^{-1} * X^T

        Returns
        -------
        h : :class:`~openturns.SymmetricMatrix`
            The projection matrix H.
        """
        return _algo.CholeskyMethod_getH(self)

    def getGramInverseDiag(self):
        """
        Get the diagonal of the inverse Gram matrix.

        .. math::

            diag(G^{-1}) = diag((X^T * X)^{-1})

        Returns
        -------
        d : :class:`~openturns.Point`
            The diagonal of the inverse Gram matrix.
        """
        return _algo.CholeskyMethod_getGramInverseDiag(self)

    def getHDiag(self):
        """
        Get the diagonal of the projection matrix H.

        .. math::

            H = X * (X^T * X)^{-1} * X^T

        Returns
        -------
        d : :class:`~openturns.Point`
            The diagonal of H.
        """
        return _algo.CholeskyMethod_getHDiag(self)

    def getGramInverseTrace(self):
        """
        Get the trace of the inverse Gram matrix.

        .. math::

            Tr(G^{-1}) = Tr(x^T * x)^{-1}

        Returns
        -------
        x : :class:`~openturns.Scalar`
            The trace of inverse Gram matrix.
        """
        return _algo.CholeskyMethod_getGramInverseTrace(self)

    def __init__(self, *args):
        _algo.CholeskyMethod_swiginit(self, _algo.new_CholeskyMethod(*args))

    __swig_destroy__ = _algo.delete_CholeskyMethod


_algo.CholeskyMethod_swigregister(CholeskyMethod)

class QRMethod(LeastSquaresMethodImplementation):
    """
    Least squares solver using the QR decomposition.

    Available constructors:
        QRMethod(*proxy, weight, indices*)

        QRMethod(*proxy, indices*)

        QRMethod(*design*)

    Parameters
    ----------
    proxy : :class:`~openturns.DesignProxy`
        Input sample
    weight : sequence of float
        Output weights
    indices : sequence of int
        Indices allowed in the basis
    design : 2-d sequence of float
        A priori known design matrix

    See also
    --------
    LeastSquaresMethod, CholeskyMethod, SVDMethod

    Examples
    --------
    Solves a linear least squares problem with SVD method:

    >>> import openturns as ot
    >>> A = ot.Matrix([[1,1],[1,2],[1,3],[1,4]])
    >>> y = ot.Point([6,5,7,10])
    >>> method = ot.QRMethod(A)
    >>> x = method.solve(y)
    >>> print(x)
    [3.5,1.4]
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
        return _algo.QRMethod_getClassName(self)

    def __repr__(self):
        return _algo.QRMethod___repr__(self)

    def solve(self, rhs):
        r"""
        Solve the least-squares problem.

        .. math::

            \vect{a} = \argmin_{\vect{x} \in \Rset^P} ||M\vect{x}-\vect{b}||^2

        Parameters
        ----------
        b : sequence of float
            Second term of the equation

        Returns
        -------
        a : :class:`~openturns.Point`
            The solution.
        """
        return _algo.QRMethod_solve(self, rhs)

    def solveNormal(self, rhs):
        """
        Solve the least-squares problem using normal equation.

        .. math::

            M^T*M*x=M^T*b

        Parameters
        ----------
        b : sequence of float
            Second term of the equation

        Returns
        -------
        x : :class:`~openturns.Point`
            The solution.
        """
        return _algo.QRMethod_solveNormal(self, rhs)

    def getGramInverse(self):
        """
        Get the inverse Gram matrix of input sample.

        .. math::

            G^{-1} = (X^T * X)^{-1}

        Returns
        -------
        c : :class:`~openturns.CovarianceMatrix`
            The inverse Gram matrix.
        """
        return _algo.QRMethod_getGramInverse(self)

    def getGramInverseDiag(self):
        """
        Get the diagonal of the inverse Gram matrix.

        .. math::

            diag(G^{-1}) = diag((X^T * X)^{-1})

        Returns
        -------
        d : :class:`~openturns.Point`
            The diagonal of the inverse Gram matrix.
        """
        return _algo.QRMethod_getGramInverseDiag(self)

    def getHDiag(self):
        """
        Get the diagonal of the projection matrix H.

        .. math::

            H = X * (X^T * X)^{-1} * X^T

        Returns
        -------
        d : :class:`~openturns.Point`
            The diagonal of H.
        """
        return _algo.QRMethod_getHDiag(self)

    def getH(self):
        """
        Get the projection matrix H.

        .. math::

            H = X * (X^T * X)^{-1} * X^T

        Returns
        -------
        h : :class:`~openturns.SymmetricMatrix`
            The projection matrix H.
        """
        return _algo.QRMethod_getH(self)

    def getGramInverseTrace(self):
        """
        Get the trace of the inverse Gram matrix.

        .. math::

            Tr(G^{-1}) = Tr(x^T * x)^{-1}

        Returns
        -------
        x : :class:`~openturns.Scalar`
            The trace of inverse Gram matrix.
        """
        return _algo.QRMethod_getGramInverseTrace(self)

    def update(self, addedIndices, conservedIndices, removedIndices, row=False):
        """
        Update the current decomposition.

        Parameters
        ----------
        addedIndices : sequence of int
            Indices of added basis terms.
        conservedIndices : sequence of int
            Indices of conserved basis terms.
        removedIndices : sequence of int
            Indices of removed basis terms.
        """
        return _algo.QRMethod_update(self, addedIndices, conservedIndices, removedIndices, row)

    def trashDecomposition(self):
        """Drop the current decomposition."""
        return _algo.QRMethod_trashDecomposition(self)

    def __init__(self, *args):
        _algo.QRMethod_swiginit(self, _algo.new_QRMethod(*args))

    __swig_destroy__ = _algo.delete_QRMethod


_algo.QRMethod_swigregister(QRMethod)

class SVDMethod(LeastSquaresMethodImplementation):
    """
    Least squares solver using SVD decomposition.

    Available constructors:
        SVDMethod(*proxy, weight, indices*)

        SVDMethod(*proxy, indices*)

        SVDMethod(*design*)

    Parameters
    ----------
    proxy : :class:`~openturns.DesignProxy`
        Input sample
    weight : sequence of float
        Output weights
    indices : sequence of int
        Indices allowed in the basis
    design : 2-d sequence of float
        A priori known design matrix

    See also
    --------
    LeastSquaresMethod, CholeskyMethod, QRMethod

    Examples
    --------
    Solves a linear least squares problem with SVD method:

    >>> import openturns as ot
    >>> A = ot.Matrix([[1,1],[1,2],[1,3],[1,4]])
    >>> y = ot.Point([6,5,7,10])
    >>> method = ot.SVDMethod(A)
    >>> x = method.solve(y)
    >>> print(x)
    [3.5,1.4]
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
        return _algo.SVDMethod_getClassName(self)

    def __repr__(self):
        return _algo.SVDMethod___repr__(self)

    def solve(self, rhs):
        r"""
        Solve the least-squares problem.

        .. math::

            \vect{a} = \argmin_{\vect{x} \in \Rset^P} ||M\vect{x}-\vect{b}||^2

        Parameters
        ----------
        b : sequence of float
            Second term of the equation

        Returns
        -------
        a : :class:`~openturns.Point`
            The solution.
        """
        return _algo.SVDMethod_solve(self, rhs)

    def solveNormal(self, rhs):
        """
        Solve the least-squares problem using normal equation.

        .. math::

            M^T*M*x=M^T*b

        Parameters
        ----------
        b : sequence of float
            Second term of the equation

        Returns
        -------
        x : :class:`~openturns.Point`
            The solution.
        """
        return _algo.SVDMethod_solveNormal(self, rhs)

    def getGramInverse(self):
        """
        Get the inverse Gram matrix of input sample.

        .. math::

            G^{-1} = (X^T * X)^{-1}

        Returns
        -------
        c : :class:`~openturns.CovarianceMatrix`
            The inverse Gram matrix.
        """
        return _algo.SVDMethod_getGramInverse(self)

    def getGramInverseDiag(self):
        """
        Get the diagonal of the inverse Gram matrix.

        .. math::

            diag(G^{-1}) = diag((X^T * X)^{-1})

        Returns
        -------
        d : :class:`~openturns.Point`
            The diagonal of the inverse Gram matrix.
        """
        return _algo.SVDMethod_getGramInverseDiag(self)

    def getHDiag(self):
        """
        Get the diagonal of the projection matrix H.

        .. math::

            H = X * (X^T * X)^{-1} * X^T

        Returns
        -------
        d : :class:`~openturns.Point`
            The diagonal of H.
        """
        return _algo.SVDMethod_getHDiag(self)

    def getH(self):
        """
        Get the projection matrix H.

        .. math::

            H = X * (X^T * X)^{-1} * X^T

        Returns
        -------
        h : :class:`~openturns.SymmetricMatrix`
            The projection matrix H.
        """
        return _algo.SVDMethod_getH(self)

    def getGramInverseTrace(self):
        """
        Get the trace of the inverse Gram matrix.

        .. math::

            Tr(G^{-1}) = Tr(x^T * x)^{-1}

        Returns
        -------
        x : :class:`~openturns.Scalar`
            The trace of inverse Gram matrix.
        """
        return _algo.SVDMethod_getGramInverseTrace(self)

    def update(self, addedIndices, conservedIndices, removedIndices, row=False):
        """
        Update the current decomposition.

        Parameters
        ----------
        addedIndices : sequence of int
            Indices of added basis terms.
        conservedIndices : sequence of int
            Indices of conserved basis terms.
        removedIndices : sequence of int
            Indices of removed basis terms.
        """
        return _algo.SVDMethod_update(self, addedIndices, conservedIndices, removedIndices, row)

    def trashDecomposition(self):
        """Drop the current decomposition."""
        return _algo.SVDMethod_trashDecomposition(self)

    def __init__(self, *args):
        _algo.SVDMethod_swiginit(self, _algo.new_SVDMethod(*args))

    __swig_destroy__ = _algo.delete_SVDMethod


_algo.SVDMethod_swigregister(SVDMethod)

class SparseMethod(LeastSquaresMethodImplementation):
    """
    Least squares solver using a sparse representation.

    Available constructors:
        SparseMethod(*method*)

        SparseMethod(*method, basisSequenceFactory, fittingAlgorithm*)

    Parameters
    ----------
    method : :class:`~openturns.LeastSquaresMethod`
        Least squares resolution method
    basisSequenceFactory : :class:`~openturns.BasisSequenceFactory`
        Basis enumeration algorithm
    fittingAlgorithm : :class:`~openturns.FittingAlgorithm`
        Validation algorithm

    See also
    --------
    LeastSquaresMethod
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
        return _algo.SparseMethod_getClassName(self)

    def __repr__(self):
        return _algo.SparseMethod___repr__(self)

    def getInputSample(self):
        """
        Input sample accessor.

        Returns
        -------
        inputSample : :class:`~openturns.Sample`
            Input sample.
        """
        return _algo.SparseMethod_getInputSample(self)

    def getWeight(self):
        """
        Accessor to the weights.

        Returns
        -------
        weight : :class:`~openturns.Point`
            Weights.
        """
        return _algo.SparseMethod_getWeight(self)

    def getBasis(self):
        """
        Accessor to the basis.

        Returns
        -------
        basis : collection of :class:`~openturns.Function`
            Basis.
        """
        return _algo.SparseMethod_getBasis(self)

    def getCurrentIndices(self):
        """
        Current indices accessor.

        Returns
        -------
        indices : :class:`~openturns.Indices`
            Indices of the current decomposition in the global basis.
        """
        return _algo.SparseMethod_getCurrentIndices(self)

    def getInitialIndices(self):
        """
        Initial indices accessor.

        Returns
        -------
        indices : :class:`~openturns.Indices`
            Initial indices of the terms in the global basis.
        """
        return _algo.SparseMethod_getInitialIndices(self)

    def solve(self, rhs):
        r"""
        Solve the least-squares problem.

        .. math::

            \vect{a} = \argmin_{\vect{x} \in \Rset^P} ||M\vect{x}-\vect{b}||^2

        Parameters
        ----------
        b : sequence of float
            Second term of the equation

        Returns
        -------
        a : :class:`~openturns.Point`
            The solution.
        """
        return _algo.SparseMethod_solve(self, rhs)

    def getGramInverse(self):
        """
        Get the inverse Gram matrix of input sample.

        .. math::

            G^{-1} = (X^T * X)^{-1}

        Returns
        -------
        c : :class:`~openturns.CovarianceMatrix`
            The inverse Gram matrix.
        """
        return _algo.SparseMethod_getGramInverse(self)

    def update(self, addedIndices, conservedIndices, removedIndices, row=False):
        """
        Update the current decomposition.

        Parameters
        ----------
        addedIndices : sequence of int
            Indices of added basis terms.
        conservedIndices : sequence of int
            Indices of conserved basis terms.
        removedIndices : sequence of int
            Indices of removed basis terms.
        """
        return _algo.SparseMethod_update(self, addedIndices, conservedIndices, removedIndices, row)

    def trashDecomposition(self):
        """Drop the current decomposition."""
        return _algo.SparseMethod_trashDecomposition(self)

    def computeWeightedDesign(self, whole=False):
        """
        Build the design matrix.

        Parameters
        ----------
        whole : bool, defaults to False
            Whether to use the initial indices instead of the current indices

        Returns
        -------
        psiAk : :class:`~openturns.Matrix`
            The design matrix
        """
        return _algo.SparseMethod_computeWeightedDesign(self, whole)

    def __init__(self, *args):
        _algo.SparseMethod_swiginit(self, _algo.new_SparseMethod(*args))

    __swig_destroy__ = _algo.delete_SparseMethod


_algo.SparseMethod_swigregister(SparseMethod)

class LeastSquaresMetaModelSelection(ApproximationAlgorithmImplementation):
    """
    Least squares metamodel selection factory.

    Adaptative sparse selection, as proposed in [blatman2009]_.

    See also
    --------
    ApproximationAlgorithm, PenalizedLeastSquaresAlgorithm

    Notes
    -----
    The LeastSquaresMetaModelSelection is built from a least squares metamodel
    selection factory.
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
        return _algo.LeastSquaresMetaModelSelection_getClassName(self)

    def __repr__(self):
        return _algo.LeastSquaresMetaModelSelection___repr__(self)

    def setBasisSequenceFactory(self, basisSequenceFactory):
        return _algo.LeastSquaresMetaModelSelection_setBasisSequenceFactory(self, basisSequenceFactory)

    def getBasisSequenceFactory(self):
        return _algo.LeastSquaresMetaModelSelection_getBasisSequenceFactory(self)

    def setFittingAlgorithm(self, fittingAlgorithm):
        return _algo.LeastSquaresMetaModelSelection_setFittingAlgorithm(self, fittingAlgorithm)

    def getFittingAlgorithm(self):
        return _algo.LeastSquaresMetaModelSelection_getFittingAlgorithm(self)

    def run(self, *args):
        """Run the algorithm."""
        return _algo.LeastSquaresMetaModelSelection_run(self, *args)

    def __init__(self, *args):
        _algo.LeastSquaresMetaModelSelection_swiginit(self, _algo.new_LeastSquaresMetaModelSelection(*args))

    __swig_destroy__ = _algo.delete_LeastSquaresMetaModelSelection


_algo.LeastSquaresMetaModelSelection_swigregister(LeastSquaresMetaModelSelection)

class LeastSquaresMetaModelSelectionFactory(ApproximationAlgorithmImplementationFactory):
    """
    Least squares metamodel selection factory.

    Available constructors:
        LeastSquaresMetaModelSelectionFactory()

        LeastSquaresMetaModelSelectionFactory(*basisSeqFac*)

        LeastSquaresMetaModelSelectionFactory(*basisSeqFac, fittingAlgo*)

    Parameters
    ----------
    basisSeqFac : :class:`~openturns.BasisSequenceFactory`
        A basis sequence factory.
    fittingAlgo : :class:`~openturns.FittingAlgorithm`
        A fitting algorithm.

    See also
    --------
    ApproximationAlgorithm, PenalizedLeastSquaresAlgorithmFactory

    Notes
    -----
    Implementation of an approximation algorithm implementation factory which builds
    an :class:`~openturns.ApproximationAlgorithm`.

    This class is not usable because it has sense only whithin the
    :class:`~openturns.FunctionalChaosAlgorithm`.

    Examples
    --------
    >>> import openturns as ot
    >>> basisSequenceFactory = ot.LARS()
    >>> fittingAlgorithm = ot.CorrectedLeaveOneOut()
    >>> approximationAlgorithm = ot.LeastSquaresMetaModelSelectionFactory(
    ...                                     basisSequenceFactory, fittingAlgorithm)
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
        return _algo.LeastSquaresMetaModelSelectionFactory_getClassName(self)

    def getBasisSequenceFactory(self):
        """
        Accessor to the basis sequence factory.

        Returns
        -------
        basis : :class:`~openturns.BasisSequenceFactory`
            Basis sequence factory.
        """
        return _algo.LeastSquaresMetaModelSelectionFactory_getBasisSequenceFactory(self)

    def getFittingAlgorithm(self):
        """
        Accessor to the fitting algorithm.

        Returns
        -------
        algo : :class:`~openturns.FittingAlgorithm`
            Fitting algorithm.
        """
        return _algo.LeastSquaresMetaModelSelectionFactory_getFittingAlgorithm(self)

    def build(self, x, y, weight, psi, indices):
        return _algo.LeastSquaresMetaModelSelectionFactory_build(self, x, y, weight, psi, indices)

    def __repr__(self):
        return _algo.LeastSquaresMetaModelSelectionFactory___repr__(self)

    def __init__(self, *args):
        _algo.LeastSquaresMetaModelSelectionFactory_swiginit(self, _algo.new_LeastSquaresMetaModelSelectionFactory(*args))

    __swig_destroy__ = _algo.delete_LeastSquaresMetaModelSelectionFactory


_algo.LeastSquaresMetaModelSelectionFactory_swigregister(LeastSquaresMetaModelSelectionFactory)

class PenalizedLeastSquaresAlgorithm(ApproximationAlgorithmImplementation):
    r"""
    Penalized least squares algorithm.

    Refer to :ref:`least_squares`.

    Available constructors:
        PenalizedLeastSquaresAlgorithm(*x, y, psi, indices, penalizationFactor=0, useNormal=False*)

        PenalizedLeastSquaresAlgorithm(*x, y, weight, psi, indices, penalizationFactor=0, useNormal=False*)

        PenalizedLeastSquaresAlgorithm(*x, y, weight, psi, indices, penalizationFactor=0, penalizationMatrix, useNormal=False*)

    Parameters
    ----------
    x : :class:`~openturns.Sample`
        Input sample
    y : :class:`~openturns.Sample`
        Output sample
    weight : sequence of float
        Output weights
    psi : sequence of :class:`~openturns.Function`
        Basis
    indices : sequence of int
        Indices allowed in the basis
    penalizationFactor : float, optional
        Penalization factor
    penalizationMatrix : 2-d sequence of float
        Penalization matrix
    useNormal : bool, optional
        Solve the normal equation

    See also
    --------
    ApproximationAlgorithm, LeastSquaresMetaModelSelection

    Notes
    -----
    Solve the least-squares problem:

    .. math::

        \vect{a} = \argmin_{\vect{b} \in \Rset^P} ||y - \vect{b}^{\intercal} \vect{\Psi}(\vect{U})||^2

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
        return _algo.PenalizedLeastSquaresAlgorithm_getClassName(self)

    def __repr__(self):
        return _algo.PenalizedLeastSquaresAlgorithm___repr__(self)

    def run(self):
        """Run the algorithm."""
        return _algo.PenalizedLeastSquaresAlgorithm_run(self)

    def __init__(self, *args):
        _algo.PenalizedLeastSquaresAlgorithm_swiginit(self, _algo.new_PenalizedLeastSquaresAlgorithm(*args))

    __swig_destroy__ = _algo.delete_PenalizedLeastSquaresAlgorithm


_algo.PenalizedLeastSquaresAlgorithm_swigregister(PenalizedLeastSquaresAlgorithm)

class PenalizedLeastSquaresAlgorithmFactory(ApproximationAlgorithmImplementationFactory):
    """
    Penalized least squares algorithm factory.

    Available constructors:
        PenalizedLeastSquaresAlgorithmFactory()

    See also
    --------
    ApproximationAlgorithm, LeastSquaresMetaModelSelectionFactory

    Notes
    -----
    Implementation of an approximation algorithm implementation factory which builds
    an :class:`~openturns.ApproximationAlgorithm`.

    This class is not usable because it has sense only whithin the
    :class:`~openturns.FunctionalChaosAlgorithm`.
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
        return _algo.PenalizedLeastSquaresAlgorithmFactory_getClassName(self)

    def build(self, x, y, weight, psi, indices):
        return _algo.PenalizedLeastSquaresAlgorithmFactory_build(self, x, y, weight, psi, indices)

    def __repr__(self):
        return _algo.PenalizedLeastSquaresAlgorithmFactory___repr__(self)

    def __init__(self, *args):
        _algo.PenalizedLeastSquaresAlgorithmFactory_swiginit(self, _algo.new_PenalizedLeastSquaresAlgorithmFactory(*args))

    __swig_destroy__ = _algo.delete_PenalizedLeastSquaresAlgorithmFactory


_algo.PenalizedLeastSquaresAlgorithmFactory_swigregister(PenalizedLeastSquaresAlgorithmFactory)

class KissFFT(openturns.statistics.FFTImplementation):
    """
    Kiss FFT.

    See also
    --------
    FFT

    Notes
    -----
    The KissFFT class inherits from the :class:`~openturns.FFT` class. The methods
    are the same as the FFT class (there is no additional method). This class
    interacts with the kissfft implemented and return results as OpenTURNS objects
    (:class:`~openturns.ComplexCollection`).
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
        return _algo.KissFFT_getClassName(self)

    def transform(self, *args):
        r"""
        Perform Fast Fourier Transform (fft).

        Parameters
        ----------
        collection : :class:`~openturns.ComplexCollection` or :class:`~openturns.ScalarCollection`, sequence of float
          Data to transform.

        Returns
        -------
        collection : :class:`~openturns.ComplexCollection`
          The data in Fourier domain.

        Notes
        -----
        The Fast Fourier Transform writes as following:

        .. math::

            {\rm y_k} = \sum_{n=0}^{N-1} x_n exp(-2 i \pi \frac{kn}{N})

        where :math:`x` denotes the data to be transformed, of size :math:`N`.

        Examples
        --------
        >>> import openturns as ot
        >>> fft = ot.FFT()
        >>> result = fft.transform(ot.Normal(8).getRealization())

        """
        return _algo.KissFFT_transform(self, *args)

    def inverseTransform(self, *args):
        r"""
        Perform Inverse Fast Fourier Transform (fft).

        Parameters
        ----------
        collection : :class:`~openturns.ComplexCollection` or :class:`~openturns.ScalarCollection`, sequence of float
          Data to transform.

        Returns
        -------
        collection : :class:`~openturns.ComplexCollection`
            The transformed data.

        Notes
        -----
        The Inverse Fast Fourier Transform writes as following:

        .. math::

            {\rm y_k} = \sum_{n=0}^{N-1} \frac{1}{N} x_n exp(2 i \pi \frac{kn}{N})

        where :math:`x` denotes the data, of size :math:`N`, to be transformed.

        Examples
        --------
        >>> import openturns as ot
        >>> fft = ot.FFT()
        >>> collection = ot.ComplexCollection([1+1j,2-0.3j,5-.3j,6+1j,9+8j,16+8j,0.3])
        >>> result = fft.inverseTransform(collection)

        """
        return _algo.KissFFT_inverseTransform(self, *args)

    def transform2D(self, *args):
        r"""
        Perform 2D FFT.

        Parameters
        ----------
        matrix : :class:`~openturns.ComplexMatrix`, :class:`~openturns.Matrix`, 2-d sequence of float
          Data to transform.

        Returns
        -------
        result : :class:`~openturns.ComplexMatrix`
          The data in fourier domain.

        Notes
        -----
        The 2D Fast Fourier Transform writes as following:

        .. math::

            {\rm Z_{k,l}} = \sum_{m=0}^{M-1}\sum_{n=0}^{N-1} X_{m,n} exp(-2 i \pi \frac{km}{M}) exp(-2 i \pi \frac{ln}{N})

        where :math:`X` denotes the data to be transformed with shape (:math:`M`,:math:`N`)

        Examples
        --------
        >>> import openturns as ot
        >>> fft = ot.FFT()
        >>> x = ot.Normal(8).getSample(16)
        >>> result = fft.transform2D(x)

        """
        return _algo.KissFFT_transform2D(self, *args)

    def inverseTransform2D(self, *args):
        r"""
        Perform 2D IFFT.

        Parameters
        ----------
        matrix : :class:`~openturns.ComplexMatrix`, :class:`~openturns.Matrix`, 2-d sequence of float
          Data to transform.

        Returns
        -------
        result : :class:`~openturns.ComplexMatrix`
          The data transformed.

        Notes
        -----
        The 2D Fast Inverse Fourier Transform writes as following:

        .. math::

            {\rm Y_{k,l}} = \frac{1}{M\times N}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1} Z_{m,n} exp(2 i \pi \frac{km}{M}) exp(2 i \pi \frac{ln}{N})

        where :math:`Z` denotes the data to be transformed with shape (:math:`M`,:math:`N`)

        Examples
        --------
        >>> import openturns as ot
        >>> fft = ot.FFT()
        >>> x = ot.Normal(8).getSample(16)
        >>> result = fft.inverseTransform2D(x)

        """
        return _algo.KissFFT_inverseTransform2D(self, *args)

    def transform3D(self, *args):
        r"""
        Perform 3D FFT.

        Parameters
        ----------
        tensor : :class:`~openturns.ComplexTensor` or :class:`~openturns.Tensor` or 3d array
          Data to transform.

        Returns
        -------
        result : :class:`~openturns.ComplexTensor`
          The data in fourier domain.

        Notes
        -----
        The 3D Fast Fourier Transform writes as following:

        .. math::

            {\rm Z_{k,l,r}} = \sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\sum_{p=0}^{P-1} X_{m,n,p} exp(-2 i \pi \frac{km}{M}) exp(-2 i \pi \frac{ln}{N}) exp(-2 i \pi \frac{rp}{P})

        where :math:`X` denotes the data to be transformed with shape (:math:`M`,:math:`N`, :math:`P`)

        Examples
        --------
        >>> import openturns as ot
        >>> fft = ot.FFT()
        >>> x = ot.ComplexTensor(8,8,2)
        >>> y = ot.Normal(8).getSample(8)
        >>> x.setSheet(0,fft.transform2D(y))
        >>> z = ot.Normal(8).getSample(8)
        >>> x.setSheet(1,fft.transform2D(z))
        >>> result = fft.transform3D(x)

        """
        return _algo.KissFFT_transform3D(self, *args)

    def inverseTransform3D(self, *args):
        r"""
        Perform 3D IFFT.

        Parameters
        ----------
        tensor : :class:`~openturns.ComplexTensor` or :class:`~openturns.Tensor` or 3d array
          The data to be transformed.

        Returns
        -------
        result : :class:`~openturns.ComplexTensor`
          The transformed data.

        Notes
        -----
        The 3D Inverse Fast Fourier Transform writes as following:

        .. math::

            {\rm Y_{k,l,r}} = \sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\sum_{p=0}^{P-1} \frac{1}{M\times N \times P} Z_{m,n,p} exp(2 i \pi \frac{km}{M}) exp(2 i \pi \frac{ln}{N}) exp(2 i \pi \frac{rp}{P})

        where :math:`Z` denotes the data to be transformed with shape (:math:`M`, :math:`N`, :math:`P`)

        Examples
        --------
        >>> import openturns as ot
        >>> fft = ot.FFT()
        >>> x = ot.ComplexTensor(8,8,2)
        >>> y = ot.Normal(8).getSample(8)
        >>> x.setSheet(0, fft.transform2D(y))
        >>> z = ot.Normal(8).getSample(8)
        >>> x.setSheet(1, fft.transform2D(z))
        >>> result = fft.inverseTransform3D(x)

        """
        return _algo.KissFFT_inverseTransform3D(self, *args)

    def __repr__(self):
        return _algo.KissFFT___repr__(self)

    def __str__(self, *args):
        return _algo.KissFFT___str__(self, *args)

    def __init__(self, *args):
        _algo.KissFFT_swiginit(self, _algo.new_KissFFT(*args))

    __swig_destroy__ = _algo.delete_KissFFT


_algo.KissFFT_swigregister(KissFFT)

class IntegrationAlgorithmImplementation(openturns.common.PersistentObject):
    """Base class for integration algorithms."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _algo.IntegrationAlgorithmImplementation_getClassName(self)

    def integrate(self, *args):
        """
        Integrate a function on an interval.

        Parameters
        ----------
        function : :class:`~openturns.Function`
            The function to integrate.
        interval : :class:`~openturns.Interval`
            The integration domain.

        Returns
        -------
        value : :class:`~openturns.Point`
            The integral value.
        """
        return _algo.IntegrationAlgorithmImplementation_integrate(self, *args)

    def __repr__(self):
        return _algo.IntegrationAlgorithmImplementation___repr__(self)

    def __str__(self, *args):
        return _algo.IntegrationAlgorithmImplementation___str__(self, *args)

    def __init__(self, *args):
        _algo.IntegrationAlgorithmImplementation_swiginit(self, _algo.new_IntegrationAlgorithmImplementation(*args))

    __swig_destroy__ = _algo.delete_IntegrationAlgorithmImplementation


_algo.IntegrationAlgorithmImplementation_swigregister(IntegrationAlgorithmImplementation)

class IntegrationAlgorithmImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _algo.IntegrationAlgorithmImplementationTypedInterfaceObject_swiginit(self, _algo.new_IntegrationAlgorithmImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _algo.IntegrationAlgorithmImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _algo.IntegrationAlgorithmImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _algo.IntegrationAlgorithmImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _algo.IntegrationAlgorithmImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _algo.IntegrationAlgorithmImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _algo.delete_IntegrationAlgorithmImplementationTypedInterfaceObject


_algo.IntegrationAlgorithmImplementationTypedInterfaceObject_swigregister(IntegrationAlgorithmImplementationTypedInterfaceObject)

class IntegrationAlgorithm(IntegrationAlgorithmImplementationTypedInterfaceObject):
    """Base class for integration algorithms."""
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _algo.IntegrationAlgorithm_getClassName(self)

    def integrate(self, *args):
        """
        Integrate a function on an interval.

        Parameters
        ----------
        function : :class:`~openturns.Function`
            The function to integrate.
        interval : :class:`~openturns.Interval`
            The integration domain.

        Returns
        -------
        value : :class:`~openturns.Point`
            The integral value.
        """
        return _algo.IntegrationAlgorithm_integrate(self, *args)

    def __repr__(self):
        return _algo.IntegrationAlgorithm___repr__(self)

    def __str__(self, *args):
        return _algo.IntegrationAlgorithm___str__(self, *args)

    def __init__(self, *args):
        _algo.IntegrationAlgorithm_swiginit(self, _algo.new_IntegrationAlgorithm(*args))

    __swig_destroy__ = _algo.delete_IntegrationAlgorithm


_algo.IntegrationAlgorithm_swigregister(IntegrationAlgorithm)

class FilonQuadrature(IntegrationAlgorithmImplementation):
    r"""
    Tensorized integration algorithm of Gauss-Legendre.

    Parameters
    ----------
    n : int, :math:`n>0`
        The discretization used by the algorithm. The integration algorithm will
        be regularly discretized by :math:`2n+1` points.
    omega : float
        The default pulsation in the oscillating kernel. Default value is 1.0.
    kind : int, :math:`kind\geq 0`
        The type of oscillating kernel defining the integral, see notes. Default
        value is 0.

    Notes
    -----
    The Filon algorithm enables to approximate the definite integral:

    .. math::

        \int_a^b f(t)w(\omega t)\di{t}

    with :math:`f: \Rset \mapsto \Rset^p`, :math:`a, b\in\Rset`,
    :math:`\omega\in\Rset` and:

    .. math ::

        w(\omega t)=\left\{
        \begin{array}{ll}
          \cos(\omega t) & \mathrm{if}\: kind=0 \\
          \sin(\omega t) & \mathrm{if}\: kind=1 \\
          \exp(i \omega t) & \mathrm{if}\: kind\geq 2
        \end{array}
        \right.

    This algorithm is based on a regular partition of the interval :math:`[a,b]`, the
    function :math:`f` being approximated by a quadratic function on three consecutive
    points. This algorithm provides an approximation of order :math:`\cO(1/\omega^2)`
    when :math:`\omega\rightarrow\infty`. When :math:`w(\omega t)=\exp(i \omega t)`,
    the result is returned as a :class:`~openturns.Point` of dimension 2, the first
    component being the real part of the result and the second component the
    imaginary part.

    Examples
    --------
    Create a Filon algorithm:

    >>> import openturns as ot
    >>> algo = ot.FilonQuadrature(100)
    >>> algo = ot.FilonQuadrature(100, 10.0)
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
        return _algo.FilonQuadrature_getClassName(self)

    def integrate(self, *args):
        r"""
        Evaluation of the integral of :math:`f w` on an interval.

        Available usages:
            integrate(*f, interval*)

            integrate(*f, interval, omega*)

        Parameters
        ----------
        f : :class:`~openturns.Function`, :math:`f: \Rset \mapsto \Rset^p`
            The integrand function.
        omega : float
            The pulsation in the weight function. This value superseeds the value given
            in the constructor.
        interval : :class:`~openturns.Interval`, :math:`interval \in \Rset` 
            The integration domain. 

        Returns
        -------
        value : :class:`~openturns.Point`
            Approximation of the integral. Its dimension is :math:`p` if
            :math:`kind\in\{0,1\}`, otherwise it is :math:`2p` with the :math:`p` first
            components corresponding to the real part of the integral and the remaining
            ones to the imaginary part.

        Examples
        --------
        >>> import openturns as ot
        >>> import math
        >>> f = ot.SymbolicFunction(['t'], ['log(1+t)'])
        >>> a = 0.5
        >>> b = a + 8.0 * math.pi
        >>> n = 100
        >>> omega = 1000.0
        >>> kind = 0
        >>> algoF = ot.FilonQuadrature(n, omega, kind)
        >>> value = algoF.integrate(f, ot.Interval(a, b))
        >>> print(value[0])
        -0.00134...
        >>> kind = 1
        >>> algoF = ot.FilonQuadrature(n, omega, kind)
        >>> value = algoF.integrate(f, ot.Interval(a, b))
        >>> print(value[0])
        0.00254...
        >>> kind = 2
        >>> algoF = ot.FilonQuadrature(n, omega, kind)
        >>> value = algoF.integrate(f, ot.Interval(a, b))
        >>> print(value[0])
        -0.00134...
        >>> print(value[1])
        0.00254...

        """
        return _algo.FilonQuadrature_integrate(self, *args)

    def getN(self):
        """
        Accessor to the discretization of the algorithm.

        Returns
        -------
        n : integer
            The discretization used by the algorithm.
        """
        return _algo.FilonQuadrature_getN(self)

    def setN(self, n):
        """
        Accessor to the discretization of the algorithm.

        Parameters
        ----------
        n : integer, :math:`n>0`
            The discretization used by the algorithm.
        """
        return _algo.FilonQuadrature_setN(self, n)

    def getOmega(self):
        """
        Accessor to the default pulsation.

        Returns
        -------
        omega : float
            The pulsation used in the *integrate* method if not explicitely given.
        """
        return _algo.FilonQuadrature_getOmega(self)

    def setOmega(self, omega):
        """
        Accessor to the default pulsation.

        Parameters
        ----------
        omega : float
            The pulsation used in the *integrate* method if not explicitely given.
        """
        return _algo.FilonQuadrature_setOmega(self, omega)

    def getKind(self):
        """
        Accessor to the kind of oscillating weight defining the integral.

        Returns
        -------
        kind : int
            The oscillating weight function defining the integral, see the notes.
        """
        return _algo.FilonQuadrature_getKind(self)

    def setKind(self, kind):
        """
        Accessor to the kind of oscillating weight defining the integral.

        Parameters
        ----------
        kind : int
            The oscillating weight function defining the integral, see the notes.
        """
        return _algo.FilonQuadrature_setKind(self, kind)

    def __repr__(self):
        return _algo.FilonQuadrature___repr__(self)

    def __str__(self, *args):
        return _algo.FilonQuadrature___str__(self, *args)

    def __init__(self, *args):
        _algo.FilonQuadrature_swiginit(self, _algo.new_FilonQuadrature(*args))

    __swig_destroy__ = _algo.delete_FilonQuadrature


_algo.FilonQuadrature_swigregister(FilonQuadrature)

class GaussKronrodRule(openturns.common.PersistentObject):
    r"""
    Gauss-Kronrod rule used in the integration algorithm.

    Parameters
    ----------
    myGaussKronrodPair : :class:`~openturns.GaussKronrodPair`
        It encodes the selected rule. 

        Available rules: 

        - GaussKronrodRule.G1K3, 
        - GaussKronrodRule.G3K7, 
        - GaussKronrodRule.G7K15, 
        - GaussKronrodRule.G11K23,
        - GaussKronrodRule.G15K31, 
        - GaussKronrodRule.G25K51. 

    Notes
    -----
    The Gauss-Kronrod rules :math:`G_mK_{2m+1}` with  :math:`m=2n+1` enable to build two approximations of the definite integral :math:`\int_{-1}^1 f(t)\di{t}` defined by:

    .. math::

        \int_{-1}^1 f(t)\di{t} \simeq  \omega_0f(0) + \sum_{k=1}^n \omega_k (f(\xi_k)+f(-\xi_k))

    and:

    .. math::

      \int_{-1}^1 f(t)\di{t}\simeq  \alpha_0f(0) + \sum_{k=1}^{m} \alpha_k (f(\zeta_k)+f(-\zeta_k))

    We have :math:`\xi_k>0`,  :math:`\zeta_k>0`, :math:`\zeta_{2j}=\xi_j`, :math:`\omega_k>0` and :math:`\alpha_k>0`.

    The rule :math:`G_mK_{2m+1}` combines a :math:`m`-point Gauss rule and a :math:`(2m+1)`-point Kronrod rule (re-using the :math:`m` nodes of the Gauss method). The nodes are defined on :math:`[-1, 1]` and always contain the node 0 when :math:`m`  is odd. 

    Examples
    --------
    Create an Gauss-Kronrod rule:

    >>> import openturns as ot
    >>> myRule = ot.GaussKronrodRule(ot.GaussKronrodRule.G15K31)
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
        return _algo.GaussKronrodRule_getClassName(self)

    G1K3 = _algo.GaussKronrodRule_G1K3
    G3K7 = _algo.GaussKronrodRule_G3K7
    G7K15 = _algo.GaussKronrodRule_G7K15
    G11K23 = _algo.GaussKronrodRule_G11K23
    G15K31 = _algo.GaussKronrodRule_G15K31
    G25K51 = _algo.GaussKronrodRule_G25K51

    def __repr__(self):
        return _algo.GaussKronrodRule___repr__(self)

    def __str__(self, *args):
        return _algo.GaussKronrodRule___str__(self, *args)

    def getPair(self):
        """
        Accessor to pair definig the rule.

        Returns
        -------
        gkPair : :class:`~openturns.GaussKronrodPair`
            Id of the Gauss-Kronrod rule.
        """
        return _algo.GaussKronrodRule_getPair(self)

    def getOrder(self):
        """
        Accessor to :math:`m` parameter.

        Returns
        -------
        m : int
            The number of points used for the Gauss approximation.
        """
        return _algo.GaussKronrodRule_getOrder(self)

    def getZeroGaussWeight(self):
        r"""
        Accessor to the first Gauss weight.

        Returns
        -------
        zeroKronrodWeight : float
            The  first weight :math:`\omega_0`.

        """
        return _algo.GaussKronrodRule_getZeroGaussWeight(self)

    def getOtherGaussWeights(self):
        r"""
        Accessor to the weights used in the Gauss approximation.

        Returns
        -------
        otherGaussWeights : :class:`~openturns.Point`
            The  weights :math:`(\omega_k)_{1 \leq k \leq n}`
        """
        return _algo.GaussKronrodRule_getOtherGaussWeights(self)

    def getOtherKronrodNodes(self):
        r"""
        Accessor to the positive nodes used in the Gauss-Kronrod approximation.

        Returns
        -------
        otherKronrodNodes : :class:`~openturns.Point`
            The  positive nodes :math:`(\zeta_k)_{1 \leq k \leq m}`
            It contains the positive Gauss nodes as we have :math:`\zeta_{2j}=\xi_j`.

        """
        return _algo.GaussKronrodRule_getOtherKronrodNodes(self)

    def getZeroKronrodWeight(self):
        r"""
        Accessor to the first Kronrod weight.

        Returns
        -------
        zeroKronrodWeight : float
            The  first weight :math:`\alpha_0`.

        """
        return _algo.GaussKronrodRule_getZeroKronrodWeight(self)

    def getOtherKronrodWeights(self):
        r"""
        Accessor to the  positive nodes used in the Gauss-Kronrod approximation.

        Returns
        -------
        otherKronrodWeights : :class:`~openturns.Point`
            The  weights :math:`(\alpha_k)_{1 \leq k \leq m}`.

        """
        return _algo.GaussKronrodRule_getOtherKronrodWeights(self)

    def __init__(self, *args):
        _algo.GaussKronrodRule_swiginit(self, _algo.new_GaussKronrodRule(*args))

    __swig_destroy__ = _algo.delete_GaussKronrodRule


_algo.GaussKronrodRule_swigregister(GaussKronrodRule)

class GaussKronrod(IntegrationAlgorithmImplementation):
    r"""
    Adaptive integration algorithm of Gauss-Kronrod.

    Parameters
    ----------
    maximumSubIntervals : int
        The maximal number of subdivisions of the interval :math:`[a,b]`
    maximumError : float
        The maximal error between Gauss and Kronrod approximations.
    GKRule : :class:`~openturns.GaussKronrodRule`
        The rule that fixes the number of points used in the Gauss and Kronrod approximations. 

    Notes
    -----
    The Gauss-Kronrod algorithm enables to approximate the definite integral:

    .. math::

        \int_{a}^b f(t)\di{t}

    with :math:`f: \Rset \mapsto \Rset^p`, using both approximations : Gauss and Kronrod ones defined by:

    .. math::

        \int_{-1}^1 f(t)\di{t} \simeq  \omega_0f(0) + \sum_{k=1}^n \omega_k (f(\xi_k)+f(-\xi_k))

    and:

    .. math::

      \int_{-1}^1 f(t)\di{t}\simeq  \alpha_0f(0) + \sum_{k=1}^{m} \alpha_k (f(\zeta_k)+f(-\zeta_k))

    where :math:`\xi_k>0`,  :math:`\zeta_k>0`, :math:`\zeta_{2j}=\xi_j`, :math:`\omega_k>0` and :math:`\alpha_k>0`.

    The Gauss-Kronrod algorithm evaluates the integral using the Gauss and the Konrod approximations. If the difference between both approximations is greater that *maximumError*, then the interval :math:`[a,b]` is subdivided into 2 subintervals with the same length. The Gauss-Kronrod algorithm is then applied on both subintervals with the sames rules. The algorithm is iterative until the  difference between both approximations is less that *maximumError*. In that case, the integral on the subinterval is approximated by the Kronrod sum. The subdivision process is limited by *maximumSubIntervals* that imposes the maximum number of subintervals.

    The final integral is the sum of the integrals evaluated on the subintervals.

    Examples
    --------
    Create a Gauss-Kronrod algorithm:

    >>> import openturns as ot
    >>> algo = ot.GaussKronrod(100, 1e-8, ot.GaussKronrodRule(ot.GaussKronrodRule.G11K23))
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
        return _algo.GaussKronrod_getClassName(self)

    def integrate(self, *args):
        r"""
        Evaluation of the integral of :math:`f` on an interval.

        Available usages:
            integrate(*f, interval*)

            integrate(*f, interval, error*)

            integrate(*f, a, b, error, ai, bi, fi, ei*)

        Parameters
        ----------
        f : :class:`~openturns.Function`, :math:`f: \Rset \mapsto \Rset^p`
            The integrand function.
        interval : :class:`~openturns.Interval`, :math:`interval \in \Rset` 
            The integration domain. 
        error : :class:`~openturns.Point`
            The error estimation of the approximation.
        a,b : float 
            Bounds of the integration interval.
        ai, bi, ei : :class:`~openturns.Point`; 
            *ai* is the set of lower bounds of the subintervals; 

            *bi* the corresponding upper bounds; 

            *ei* the associated error estimation. 
        fi : :class:`~openturns.Sample`
            *fi* is the set of :math:`\int_{ai}^{bi} f(t)\di{t}`

        Returns
        -------
        value : :class:`~openturns.Point`
            Approximation of the integral.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x'], ['abs(sin(x))'])
        >>> a = -2.5
        >>> b = 4.5
        >>> algoGK = ot.GaussKronrod(100, 1e-8, ot.GaussKronrodRule(ot.GaussKronrodRule.G11K23))

        Use the high-level usage:

        >>> value = algoGK.integrate(f, ot.Interval(a, b))[0]
        >>> print(value)
        4.590...

        Use the low-level usage:

        >>> error = ot.Point()
        >>> ai = ot.Point()
        >>> bi = ot.Point()
        >>> ei = ot.Point()
        >>> fi = ot.Sample()
        >>> value2 = algoGK.integrate(f, a, b, error, ai, bi, fi, ei)[0]
        >>> print(value2)
        4.590...
        """
        return _algo.GaussKronrod_integrate(self, *args)

    def getMaximumSubIntervals(self):
        """
        Accessor to the maximal  number of subdivisions of :math:`[a,b]`.

        Returns
        -------
        maximumSubIntervals : float, positive
            The maximal number of subdivisions of the interval :math:`[a,b]`.
        """
        return _algo.GaussKronrod_getMaximumSubIntervals(self)

    def setMaximumSubIntervals(self, maximumSubIntervals):
        """
        Set the maximal  number of subdivisions of :math:`[a,b]`.

        Parameters
        ----------
        maximumSubIntervals : float, positive
            The maximal number of subdivisions of the interval :math:`[a,b]`.
        """
        return _algo.GaussKronrod_setMaximumSubIntervals(self, maximumSubIntervals)

    def getMaximumError(self):
        """
        Accessor to the maximal error between Gauss and Kronrod approximations.

        Returns
        -------
        maximumErrorvalue : float, positive
            The maximal error between Gauss and Kronrod approximations.
        """
        return _algo.GaussKronrod_getMaximumError(self)

    def setMaximumError(self, maximumError):
        """
        Set the maximal error between Gauss and Kronrod approximations.

        Parameters
        ----------
        maximumErrorvalue : float, positive
            The maximal error between Gauss and Kronrod approximations.
        """
        return _algo.GaussKronrod_setMaximumError(self, maximumError)

    def getRule(self):
        """
        Accessor to the Gauss-Kronrod rule used in the integration algorithm.

        Returns
        -------
        rule : :class:`~openturns.GaussKronrodRule`
            The Gauss-Kronrod rule used in the integration algorithm.
        """
        return _algo.GaussKronrod_getRule(self)

    def setRule(self, rule):
        """
        Set the Gauss-Kronrod rule used in the integration algorithm.

        Parameters
        ----------
        rule : :class:`~openturns.GaussKronrodRule`
            The Gauss-Kronrod rule used in the integration algorithm.
        """
        return _algo.GaussKronrod_setRule(self, rule)

    def __repr__(self):
        return _algo.GaussKronrod___repr__(self)

    def __str__(self, *args):
        return _algo.GaussKronrod___str__(self, *args)

    def __init__(self, *args):
        _algo.GaussKronrod_swiginit(self, _algo.new_GaussKronrod(*args))

    __swig_destroy__ = _algo.delete_GaussKronrod


_algo.GaussKronrod_swigregister(GaussKronrod)

class GaussLegendre(IntegrationAlgorithmImplementation):
    r"""
    Tensorized integration algorithm of Gauss-Legendre.

    Available constructors:
        GaussLegendre(*dimension=1*)

        GaussLegendre(*discretization*)

    Parameters
    ----------
    dimension : int, :math:`dimension>0`
        The dimension of the functions to integrate. The default discretization is *GaussLegendre-DefaultMarginalIntegrationPointsNumber* in each dimension, see :class:`~openturns.ResourceMap`.
    discretization : sequence of int
        The number of nodes in each dimension. The sequence must be non-empty and must contain only positive values.

    Notes
    -----
    The Gauss-Legendre algorithm enables to approximate the definite integral:

    .. math::

        \int_{\vect{a}}^\vect{b} f(\vect{t})\di{\vect{t}}

    with :math:`f: \Rset^d \mapsto \Rset^p`, :math:`\vect{a}, \vect{b}\in\Rset^d` using a fixed tensorized Gauss-Legendre approximation:

    .. math::

        \int_{\vect{a}}^\vect{b} f(\vect{t})\di{\vect{t}} = \sum_{\vect{n}\in \cN}\left(\prod_{i=1}^d w^{N_i}_{n_i}\right)f(\xi^{N_1}_{n_1},\dots,\xi^{N_d}_{n_d})

    where :math:`\xi^{N_i}_{n_i}` is the :math:`n_i`th node of the :math:`N_i`-points Gauss-Legendre 1D integration rule and :math:`w^{N_i}_{n_i}` the associated weight.

    Examples
    --------
    Create a Gauss-Legendre algorithm:

    >>> import openturns as ot
    >>> algo = ot.GaussLegendre(2)
    >>> algo = ot.GaussLegendre([2, 4, 5])
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
        return _algo.GaussLegendre_getClassName(self)

    def integrate(self, *args):
        r"""
        Evaluation of the integral of :math:`f` on an interval.

        Available usages:
            integrate(*f, interval*)

            integrate(*f, interval, xi*)

        Parameters
        ----------
        f : :class:`~openturns.Function`, :math:`f: \Rset^d \mapsto \Rset^p`
            The integrand function.
        interval : :class:`~openturns.Interval`, :math:`interval \in \Rset^d` 
            The integration domain. 
        xi : :class:`~openturns.Sample`
            The integration nodes.

        Returns
        -------
        value : :class:`~openturns.Point`
            Approximation of the integral.

        Examples
        --------
        >>> import openturns as ot
        >>> f = ot.SymbolicFunction(['x'], ['sin(x)'])
        >>> a = -2.5
        >>> b = 4.5
        >>> algoGL = ot.GaussLegendre([10])
        >>> value = algoGL.integrate(f, ot.Interval(a, b))[0]
        >>> print(value)
        -0.590...

        """
        return _algo.GaussLegendre_integrate(self, *args)

    def integrateWithNodes(self, function, interval):
        return _algo.GaussLegendre_integrateWithNodes(self, function, interval)

    def getDiscretization(self):
        """
        Accessor to the discretization of the tensorized rule.

        Returns
        -------
        discretization : :class:`~openturns.Indices`
            The number of integration point in each dimension.
        """
        return _algo.GaussLegendre_getDiscretization(self)

    def getNodes(self):
        """
        Accessor to the integration nodes.

        Returns
        -------
        nodes : :class:`~openturns.Sample`
            The tensorized Gauss-Legendre integration nodes on :math:`[0,1]^d` where :math:`d>0` is the dimension of the integration algorithm.
        """
        return _algo.GaussLegendre_getNodes(self)

    def getWeights(self):
        """
        Accessor to the integration weights.

        Returns
        -------
        weights : :class:`~openturns.Point`
            The tensorized Gauss-Legendre integration weights on :math:`[0,1]^d` where :math:`d>0` is the dimension of the integration algorithm.
        """
        return _algo.GaussLegendre_getWeights(self)

    def __repr__(self):
        return _algo.GaussLegendre___repr__(self)

    def __str__(self, *args):
        return _algo.GaussLegendre___str__(self, *args)

    def __init__(self, *args):
        _algo.GaussLegendre_swiginit(self, _algo.new_GaussLegendre(*args))

    __swig_destroy__ = _algo.delete_GaussLegendre


_algo.GaussLegendre_swigregister(GaussLegendre)

class IteratedQuadrature(IntegrationAlgorithmImplementation):
    r"""
    Multivariate integration algorithm.

    Parameters
    ----------
    univariateQuadrature : :class:`~openturns.IntegrationAlgorithm`
        By default, the integration algorithm is the Gauss-Kronrod algorithm (:class:`~openturns.GaussKronrod`)  with the following parameters: maximumSubIntervals=32, maximumError= :math:`1e-7` and GKRule = G3K7. 
        Note that the default parametrisation of the :class:`~openturns.GaussKronrod` class leads to a more precise evaluation of the integral but the cost is greater. It is recommended to increase the order of the quadratic rule and the number of sub intervals if the integrand or one of the bound functions is smooth but with many oscillations. 

    Notes
    -----
    This class enables to approximate the following integral:

    .. math::

        I_f = \int_{a}^{b}\, \int_{l_1(x_0)}^{u_1(x_0)}\, \int_{l_2(x_0, x_1)}^{u_2(x_0,x_1)}\, \int_{l_{n-1}(x_0, \dots, x_{n-2})}^{u_{n-1}(x_0, \dots, x_{n-2})} \, f(x_0, \dots, x_{n-1})\di{x_{n-1}}\dots\di{x_0}

    with :math:`f: \Rset^n \mapsto \Rset^p`, :math:`l_k, u_k: \Rset^k \mapsto \Rset` and :math:`n\geq 1`. For :math:`n=1`, there is no bound functions :math:`l_k` and :math:`u_k`.

    Examples
    --------
    Create an iterated quadrature algorithm:

    >>> import openturns as ot
    >>> import math as m
    >>> a = -m.pi
    >>> b = m.pi
    >>> f = ot.SymbolicFunction(['x', 'y'], ['1+cos(x)*sin(y)'])
    >>> l = [ot.SymbolicFunction(['x'], [' 2+cos(x)'])]
    >>> u = [ot.SymbolicFunction(['x'], ['-2-cos(x)'])]

    Draw the graph of the integrand and the bounds:

    >>> g = ot.Graph('Integration nodes', 'x', 'y', True, 'topright')
    >>> g.add(f.draw([a,a],[b,b]))
    >>> curve = l[0].draw(a, b).getDrawable(0)
    >>> curve.setLineWidth(2)
    >>> curve.setColor('red')
    >>> g.add(curve)
    >>> curve = u[0].draw(a, b).getDrawable(0)
    >>> curve.setLineWidth(2)
    >>> curve.setColor('red')
    >>> g.add(curve)

    Evaluate the integral with high precision:

    >>> Iref = ot.IteratedQuadrature(ot.GaussKronrod(100000, 1e-13, ot.GaussKronrodRule(ot.GaussKronrodRule.G11K23))).integrate(f, a, b, l, u)

    Evaluate the integral with the default GaussKronrod algorithm, and get
    evaluation points:

    >>> f = ot.MemoizeFunction(f)
    >>> I1 = ot.IteratedQuadrature(ot.GaussKronrod()).integrate(f, a, b, l, u)
    >>> sample1 = f.getInputHistory()
    >>> print(I1)
    [-25.132...]
    >>> n_evals = sample1.getSize()
    >>> print(n_evals)
    2116
    >>> err = abs(100.0*(1.0-I1[0]/Iref[0]))
    >>> print(err)
    2.2...e-14
    >>> cloud = ot.Cloud(sample1)
    >>> cloud.setPointStyle('fcircle')
    >>> cloud.setColor('green')
    >>> g.add(cloud)
    >>> f.clearHistory()

    Evaluate the integral with the default IteratedQuadrature algorithm:

    >>> I2 = ot.IteratedQuadrature().integrate(f, a, b, l, u)
    >>> sample2 = f.getInputHistory()
    >>> print(I2)
    [-25.132...]
    >>> n_evals = sample2.getSize()
    >>> print(n_evals)
    5236
    >>> err = abs(100.0*(1.0-I2[0]/Iref[0]))
    >>> print(err)
    4.6...e-10
    >>> cloud = ot.Cloud(sample2)
    >>> cloud.setPointStyle('fcircle')
    >>> cloud.setColor('gold')
    >>> g.add(cloud)
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
        return _algo.IteratedQuadrature_getClassName(self)

    def integrate(self, *args):
        r"""
        Evaluation of the integral of :math:`f` on a domain.

        Available usages:
            integrate(*f, interval*)

            integrate(*f, a, b, lowerBoundFunctions, upperBoundFunctions*)

        Parameters
        ----------
        f : :class:`~openturns.Function`, :math:`f: \Rset^n \mapsto \Rset^p`
            The integrand function.
        interval : :class:`~openturns.Interval`, :math:`interval \in \Rset^n` 
            The integration domain. 
        a,b : float 
            Bounds of the integration interval of the first scalar input :math:`x_0`
        lowerBoundFunctions, upperBoundFunctions : list of :class:`~openturns.Function`
            List of :math:`n` functions :math:`(l_0, \dots, l_{n-1})` and :math:`(u_0, \dots, u_{n-1})` where :math:`l_k, u_k: \Rset^k \mapsto \Rset` defining the integration domain as defined above.
            The bound functions can cross each other. 

        Returns
        -------
        value : :class:`~openturns.Point`
            Approximation of the integral.
        """
        return _algo.IteratedQuadrature_integrate(self, *args)

    def __repr__(self):
        return _algo.IteratedQuadrature___repr__(self)

    def __str__(self, *args):
        return _algo.IteratedQuadrature___str__(self, *args)

    def __init__(self, *args):
        _algo.IteratedQuadrature_swiginit(self, _algo.new_IteratedQuadrature(*args))

    __swig_destroy__ = _algo.delete_IteratedQuadrature


_algo.IteratedQuadrature_swigregister(IteratedQuadrature)

class ExpertMixture(openturns.func.EvaluationImplementation):
    r"""
    Expert mixture defining a piecewise function according to a classifier.

    This implements an expert mixture which is a piecewise function :math:`f`
    defined by the collection of functions :math:`(f_i)_{i=1, \ldots, N}` given in
    *basis* and according to a *classifier*:

    .. math::

        f(\vect{x}) &= f_1(\vect{x}) \hspace{1em} \forall \vect{z} \in \text{Class} 1 \\
                    &= f_k(\vect{x}) \hspace{1em} \forall \vect{z} \in \text{Class} k \\
                    &= f_N(\vect{x}) \hspace{1em} \forall \vect{z} \in \text{Class} N

    where the :math:`N` classes are defined by the classifier.

    In supervised mode the classifier partitions the input and output space at once:

    .. math::

        \vect{z} = (\vect{x}, f(\vect{x}))

    whereas in non-supervised mode only the input space is partitioned:

    .. math::

        \vect{z} = \vect{x}

    Parameters
    ----------
    basis : sequence of :class:`~openturns.Function`
        A basis
    classifier : :class:`~openturns.Classifier`
        A classifier
    supervised : bool (default=True)
        In supervised mode, the classifier partitions the space
        of :math:`(\vect(x), f(\vect(x)))` whereas in non-supervised mode the
        classifier only partitions the input space.

    Examples
    --------
    >>> import openturns as ot
    >>> R = ot.CorrelationMatrix(2)
    >>> R[0, 1] = -0.99
    >>> d1 = ot.Normal([-1.0, 1.0], [1.0, 1.0], R)
    >>> R[0, 1] = 0.99
    >>> d2 = ot.Normal([1.0, 1.0], [1.0, 1.0], R)
    >>> distribution = ot.Mixture([d1, d2], [1.0]*2)
    >>> classifier = ot.MixtureClassifier(distribution)
    >>> f1 = ot.SymbolicFunction(['x'], ['-x'])
    >>> f2 = ot.SymbolicFunction(['x'], ['x'])
    >>> experts = [f1, f2]
    >>> evaluation = ot.ExpertMixture(experts, classifier)
    >>> moe = ot.Function(evaluation)
    >>> print(moe([-0.3]))
    [0.3]
    >>> print(moe([0.1]))
    [0.1]

    Notes
    -----
    The number of experts must match the number of classes of the classifier.

    See also
    --------
    Classifier, MixtureClassifier
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
        return _algo.ExpertMixture_getClassName(self)

    def __eq__(self, other):
        return _algo.ExpertMixture___eq__(self, other)

    def __repr__(self):
        return _algo.ExpertMixture___repr__(self)

    def __str__(self, *args):
        return _algo.ExpertMixture___str__(self, *args)

    def __call__(self, *args):
        return _algo.ExpertMixture___call__(self, *args)

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
        return _algo.ExpertMixture_getInputDimension(self)

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
        return _algo.ExpertMixture_getOutputDimension(self)

    def getExperts(self):
        r"""
        Accessor the basis.

        Returns
        -------
        basis : collection of :class:`~openturns.Function`
            The collection of functions :math:`(f_i)_{i=1, \ldots, N}`.
        """
        return _algo.ExpertMixture_getExperts(self)

    def setExperts(self, experts):
        r"""
        Accessor the basis.

        Parameters
        ----------
        basis : :class:`~openturns.Basis`
            The collection of functions :math:`(f_i)_{i=1, \ldots, N}`.
        """
        return _algo.ExpertMixture_setExperts(self, experts)

    def getClassifier(self):
        """
        Accessor the classifier.

        Returns
        -------
        classifier : :class:`~openturns.Classifier`
            The classifier.
        """
        return _algo.ExpertMixture_getClassifier(self)

    def setClassifier(self, classifier):
        """
        Accessor the classifier.

        Parameters
        ----------
        classifier : :class:`~openturns.Classifier`
            The classifier.
        """
        return _algo.ExpertMixture_setClassifier(self, classifier)

    def __init__(self, *args):
        _algo.ExpertMixture_swiginit(self, _algo.new_ExpertMixture(*args))

    __swig_destroy__ = _algo.delete_ExpertMixture


_algo.ExpertMixture_swigregister(ExpertMixture)

class KarhunenLoeveResultImplementation(openturns.common.PersistentObject):
    r"""
    Result structure of a Karhunen Loeve algorithm.

    Available constructors:
        KarhunenLoeveResult(*implementation*)

        KarhunenLoeveResult(*covModel, s, lambda, modes, modesAsProcessSample, projection*)

    Parameters
    ----------
    implementation : :class:`~openturns.KarhunenLoeveResultImplementation`
        A specific implementation.
    covModel : :class:`~openturns.CovarianceModel`
        The covariance model.
    s : float, :math:`\geq0`
        The threshold used to select the most significant eigenmodes, defined in  :class:`~openturns.KarhunenLoeveAlgorithm`.
    lambda : :class:`~openturns.Point`
        The first eigenvalues of the Fredholm problem.
    modes : :class:`~openturns.Basis`
        The first modes  of the Fredholm problem.
    modesAsProcessSample : :class:`~openturns.ProcessSample`
        The values of the modes on the mesh associated to the KarhunenLoeve algorithm.
    projection : :class:`~openturns.Matrix`
        The projection matrix.

    Notes
    -----
    Structure generally created by the method run() of a :class:`~openturns.KarhunenLoeveAlgorithm` and obtained thanks to the method getResult().

    We consider :math:`C:\cD \times \cD \rightarrow  \cS^+_d(\Rset)` a covariance function defined on :math:`\cD \in \Rset^n`, continuous at :math:`\vect{0}`.

    We note :math:`(\lambda_k,  \vect{\varphi}_k)_{1 \leq k \leq K}` the solutions of the Fredholm problem associated to  :math:`C` where *K* is the highest index :math:`K` such that :math:`\lambda_K \geq s \lambda_1`.

    We note :math:`\vect{\lambda}` the eigenvalues sequence and :math:`\vect{\varphi}` the eigenfunctions sequence.

    Then we define the linear projection function :math:`\pi_{ \vect{\lambda}, \vect{\varphi}}` by:

    .. math::
        :label: projection

        \pi_{\vect{\lambda}, \vect{\varphi}}: \left|
          \begin{array}{ccl}
            L^2(\cD, \Rset^d) & \rightarrow & \cS^{\Nset} \\
            f & \mapsto &\left(\dfrac{1}{\sqrt{\lambda_k}}\int_{\cD}f(\vect{t}) \vect{\varphi}_k(\vect{t})\, d\vect{t}\right)_{k \geq 1}
          \end{array}
        \right.

    where :math:`\cS^{\Nset}  = \left \{ (\zeta_k)_{k \geq 1} \in  \Rset^{\Nset} \, | \, \sum_{k=1}^{\infty}\lambda_k \zeta_k^2 < +\infty \right \}`. 

    According to the Karhunen Loeve algorithm, the integral of :eq:`projection` is replaced by a specific weighted and finite sum. Thus, the linear relation :eq:`projection` becomes a relation between fields which allows the following matrix representation: 

    .. math::
        :label: projectionMatrix

        \left|
          \begin{array}{ccl}
             \cM_N \times (\Rset^d)^N & \rightarrow & \Rset^K \\
             F & \mapsto & (\xi_1, \dots, \xi_K) = MF
          \end{array}
        \right.

    where :math:`F = (\vect{t}_i, \vect{v}_i)_{1 \leq i \leq N}` is a :class:`~openturns.Field` and :math:`M`  the *projection matrix*.

    The inverse of :math:`\pi_{\vect{\lambda}, \vect{\varphi}}` is the lift function defined by:

    .. math::
        :label: lift

        \pi_{\vect{\lambda}, \vect{\varphi}}^{-1}: \left|
          \begin{array}{ccl}
             \cS^{\Nset} & \rightarrow & L^2(\cD, \Rset^d)\\
            (\xi_k)_{k \geq 1} & \mapsto & f(.) = \sum_{k \geq 1} \sqrt{\lambda_k}\xi_k \vect{\varphi}_k(.)
          \end{array}
        \right.

    If the function :math:`f(.) = X(\omega_0, .)` where :math:`X` is the centered process which covariance function is associated to the eigenvalues and eigenfunctions :math:`(\vect{\lambda}, \vect{\varphi})`, then the *getEigenValues* method enables to obtain the :math:`K` first eigenvalues of the Karhunen Loeve decomposition of :math:`X` and the method *getModes* enables to get the associated modes.

    Examples
    --------
    >>> import openturns as ot
    >>> N = 256
    >>> mesh = ot.IntervalMesher([N - 1]).build(ot.Interval(-1, 1))
    >>> covariance_X = ot.AbsoluteExponential([1])
    >>> process_X = ot.GaussianProcess(covariance_X, mesh)
    >>> s = 0.001
    >>> algo_X = ot.KarhunenLoeveP1Algorithm(mesh, covariance_X, s)
    >>> algo_X.run()
    >>> result_X = algo_X.getResult()
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
        return _algo.KarhunenLoeveResultImplementation_getClassName(self)

    def getThreshold(self):
        r"""
        Accessor to the limit ratio on eigenvalues.

        Returns
        -------
        s : float, :math:`\geq 0`
            The threshold :math:`s` used to select the most significant eigenmodes, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResultImplementation_getThreshold(self)

    def getCovarianceModel(self):
        """
        Accessor to the covariance model.

        Returns
        -------
        covModel : :class:`~openturns.CovarianceModel`
            The covariance model.
        """
        return _algo.KarhunenLoeveResultImplementation_getCovarianceModel(self)

    def getEigenValues(self):
        r"""
        Accessor to the eigenvalues of the Karhunen Loeve decomposition.

        Returns
        -------
        eigenVal : :class:`~openturns.Point`
            The most significant eigenvalues.

        Notes
        -----
        OpenTURNS truncates the sequence :math:`(\lambda_k,  \vect{\varphi}_k)_{k \geq 1}`  to the most significant terms, selected by the threshold defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResultImplementation_getEigenValues(self)

    def getModes(self):
        r"""
        Get the modes as functions.

        Returns
        -------
        modes : collection of :class:`~openturns.Function`
            The truncated basis :math:`(\vect{\varphi}_k)_{1 \leq k \leq K}`.

        Notes
        -----
        The basis is truncated to :math:`(\vect{\varphi}_k)_{1 \leq k \leq K}` where
        :math:`K`  is determined by the :math:`s`, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResultImplementation_getModes(self)

    def getModesAsProcessSample(self):
        r"""
        Accessor to the modes as a process sample.

        Returns
        -------
        modesAsProcessSample : :class:`~openturns.ProcessSample`
            The values of each mode on a mesh whose vertices were used to discretize the
            Fredholm equation.

        Notes
        -----
        The modes :math:`(\vect{\varphi}_k)_{1 \leq k \leq K}` are evaluated on the vertices of the mesh defining the process sample. The values of the i-th field are the values of the i-th mode on these vertices.

        The mesh corresponds to the discretization points of the integral in :eq:`projection`.
        """
        return _algo.KarhunenLoeveResultImplementation_getModesAsProcessSample(self)

    def getScaledModes(self):
        r"""
        Get the modes as functions scaled by the square-root of the corresponding eigenvalue.

        Returns
        -------
        modes : collection of :class:`~openturns.Function`
            The truncated basis :math:`(\sqrt{\lambda_k}\vect{\varphi}_k)_{1 \leq k \leq K}`.

        Notes
        -----
        The basis is truncated to :math:`(\sqrt{\lambda_k}\vect{\varphi}_k)_{1 \leq k \leq K}`
        where :math:`K` is determined by the :math:`s`, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResultImplementation_getScaledModes(self)

    def getScaledModesAsProcessSample(self):
        r"""
        Accessor to the scaled modes as a process sample.

        Returns
        -------
        modesAsProcessSample : :class:`~openturns.ProcessSample`
            The values of each scaled mode on a mesh whose vertices were used to
            discretize the Fredholm equation.

        Notes
        -----
        The modes :math:`(\vect{\varphi}_k)_{1 \leq k \leq K}` are evaluated on the
        vertices of the mesh defining the process sample. The values of the i-th field
        are the values of the i-th mode on these vertices.

        The mesh corresponds to the discretization points used to discretize the integral 
         :eq:`projection`.
        """
        return _algo.KarhunenLoeveResultImplementation_getScaledModesAsProcessSample(self)

    def getProjectionMatrix(self):
        """
        Accessor to the projection matrix.

        Returns
        -------
        projection : :class:`~openturns.Matrix`
            The  matrix :math:`M` defined in :eq:`projectionMatrix`.
        """
        return _algo.KarhunenLoeveResultImplementation_getProjectionMatrix(self)

    def getMesh(self):
        """
        Accessor to the mesh.

        Returns
        -------
        mesh : :class:`~openturns.Mesh`
            The mesh corresponds to the discretization points of the integral in
            :eq:`projection`.
        """
        return _algo.KarhunenLoeveResultImplementation_getMesh(self)

    def project(self, *args):
        r"""
        Project a function or a field on the eigenmodes basis.

        Available constructors:
            project(*function*)

            project(*functions*)

            project(*values*)

            project(*fieldSample*)

        Parameters
        ----------
        function : :class:`~openturns.Function`
            A function.
        functions : list of :class:`~openturns.Function`
            A list of functions.
        values :  :class:`~openturns.Sample`
            Field values.
        fieldSample :  :class:`~openturns.ProcessSample`
            A collection of fields.

        Returns
        -------
        point : :class:`~openturns.Point`
            The vector :math:`(\alpha_1, \dots, \alpha_K)` of the components of the function or the field in the eigenmodes basis
        sample : :class:`~openturns.Sample`
            The collection of the vectors :math:`(\alpha_1, \dots, \alpha_K)` of the components of the collection of functions or fields in the eigenmodes basis

        Notes
        -----
        The *project* method calculates the projection :eq:`projection` on a function  or a field where only the first :math:`K` elements of the sequences are calculated.
        :math:`K` is determined by the :math:`s`, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.

        Lets note :math:`\cM_{KL}` the mesh coming from the :class:`~openturns.KarhunenLoeveResult` (ie the one contained in the *modesAsSample* :class:`~openturns.ProcessSample`).

        The given values are defined on the input field :math:`\cM_{KL}` and the associated values are directly used for the projection.

        If evaluated from a function, the *project* method evaluates the function on :math:`\cM_{KL}` and uses :eq:`projectionMatrix`. 
        """
        return _algo.KarhunenLoeveResultImplementation_project(self, *args)

    def lift(self, coefficients):
        r"""
        Lift the coefficients into a function.

        Parameters
        ----------
        coef : :class:`~openturns.Point`
            The coefficients :math:`(\xi_1, \dots, \xi_K)`.

        Returns
        -------
        modes : :class:`~openturns.Function`
            The function :math:`f` defined in :eq:`lift`.

        Notes
        -----
        The sum defining :math:`f` is truncated to the first :math:`K` terms, where :math:`K`  is determined by the :math:`s`, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResultImplementation_lift(self, coefficients)

    def liftAsSample(self, coefficients):
        r"""
        Lift the coefficients into a sample.

        Parameters
        ----------
        coef : :class:`~openturns.Point`
            The coefficients :math:`(\xi_1, \dots, \xi_K)`.

        Returns
        -------
        modes : :class:`~openturns.Sample`
            The function :math:`f` defined in :eq:`lift` evaluated on the mesh associated to the discretization of :eq:`projection`.

        Notes
        -----
        The sum defining :math:`f` is truncated to the first :math:`K` terms, where :math:`K` is determined by the :math:`s`, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResultImplementation_liftAsSample(self, coefficients)

    def liftAsField(self, coefficients):
        r"""
        Lift the coefficients into a field.

        Parameters
        ----------
        coef : :class:`~openturns.Point`
            The coefficients :math:`(\xi_1, \dots, \xi_K)`.

        Returns
        -------
        modes : :class:`~openturns.Field`
            The function :math:`f` defined in :eq:`lift` evaluated on the mesh associated to the discretization of :eq:`projection`.

        Notes
        -----
        The sum defining :math:`f` is truncated to the first :math:`K` terms, where :math:`K` is determined by the :math:`s`, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResultImplementation_liftAsField(self, coefficients)

    def __repr__(self):
        return _algo.KarhunenLoeveResultImplementation___repr__(self)

    def __str__(self, *args):
        return _algo.KarhunenLoeveResultImplementation___str__(self, *args)

    def __init__(self, *args):
        _algo.KarhunenLoeveResultImplementation_swiginit(self, _algo.new_KarhunenLoeveResultImplementation(*args))

    __swig_destroy__ = _algo.delete_KarhunenLoeveResultImplementation


_algo.KarhunenLoeveResultImplementation_swigregister(KarhunenLoeveResultImplementation)

class KarhunenLoeveResultImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _algo.KarhunenLoeveResultImplementationTypedInterfaceObject_swiginit(self, _algo.new_KarhunenLoeveResultImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _algo.KarhunenLoeveResultImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _algo.KarhunenLoeveResultImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _algo.KarhunenLoeveResultImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _algo.KarhunenLoeveResultImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _algo.KarhunenLoeveResultImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _algo.delete_KarhunenLoeveResultImplementationTypedInterfaceObject


_algo.KarhunenLoeveResultImplementationTypedInterfaceObject_swigregister(KarhunenLoeveResultImplementationTypedInterfaceObject)

class KarhunenLoeveResult(KarhunenLoeveResultImplementationTypedInterfaceObject):
    r"""
    Result structure of a Karhunen Loeve algorithm.

    Available constructors:
        KarhunenLoeveResult(*implementation*)

        KarhunenLoeveResult(*covModel, s, lambda, modes, modesAsProcessSample, projection*)

    Parameters
    ----------
    implementation : :class:`~openturns.KarhunenLoeveResultImplementation`
        A specific implementation.
    covModel : :class:`~openturns.CovarianceModel`
        The covariance model.
    s : float, :math:`\geq0`
        The threshold used to select the most significant eigenmodes, defined in  :class:`~openturns.KarhunenLoeveAlgorithm`.
    lambda : :class:`~openturns.Point`
        The first eigenvalues of the Fredholm problem.
    modes : :class:`~openturns.Basis`
        The first modes  of the Fredholm problem.
    modesAsProcessSample : :class:`~openturns.ProcessSample`
        The values of the modes on the mesh associated to the KarhunenLoeve algorithm.
    projection : :class:`~openturns.Matrix`
        The projection matrix.

    Notes
    -----
    Structure generally created by the method run() of a :class:`~openturns.KarhunenLoeveAlgorithm` and obtained thanks to the method getResult().

    We consider :math:`C:\cD \times \cD \rightarrow  \cS^+_d(\Rset)` a covariance function defined on :math:`\cD \in \Rset^n`, continuous at :math:`\vect{0}`.

    We note :math:`(\lambda_k,  \vect{\varphi}_k)_{1 \leq k \leq K}` the solutions of the Fredholm problem associated to  :math:`C` where *K* is the highest index :math:`K` such that :math:`\lambda_K \geq s \lambda_1`.

    We note :math:`\vect{\lambda}` the eigenvalues sequence and :math:`\vect{\varphi}` the eigenfunctions sequence.

    Then we define the linear projection function :math:`\pi_{ \vect{\lambda}, \vect{\varphi}}` by:

    .. math::
        :label: projection

        \pi_{\vect{\lambda}, \vect{\varphi}}: \left|
          \begin{array}{ccl}
            L^2(\cD, \Rset^d) & \rightarrow & \cS^{\Nset} \\
            f & \mapsto &\left(\dfrac{1}{\sqrt{\lambda_k}}\int_{\cD}f(\vect{t}) \vect{\varphi}_k(\vect{t})\, d\vect{t}\right)_{k \geq 1}
          \end{array}
        \right.

    where :math:`\cS^{\Nset}  = \left \{ (\zeta_k)_{k \geq 1} \in  \Rset^{\Nset} \, | \, \sum_{k=1}^{\infty}\lambda_k \zeta_k^2 < +\infty \right \}`. 

    According to the Karhunen Loeve algorithm, the integral of :eq:`projection` is replaced by a specific weighted and finite sum. Thus, the linear relation :eq:`projection` becomes a relation between fields which allows the following matrix representation: 

    .. math::
        :label: projectionMatrix

        \left|
          \begin{array}{ccl}
             \cM_N \times (\Rset^d)^N & \rightarrow & \Rset^K \\
             F & \mapsto & (\xi_1, \dots, \xi_K) = MF
          \end{array}
        \right.

    where :math:`F = (\vect{t}_i, \vect{v}_i)_{1 \leq i \leq N}` is a :class:`~openturns.Field` and :math:`M`  the *projection matrix*.

    The inverse of :math:`\pi_{\vect{\lambda}, \vect{\varphi}}` is the lift function defined by:

    .. math::
        :label: lift

        \pi_{\vect{\lambda}, \vect{\varphi}}^{-1}: \left|
          \begin{array}{ccl}
             \cS^{\Nset} & \rightarrow & L^2(\cD, \Rset^d)\\
            (\xi_k)_{k \geq 1} & \mapsto & f(.) = \sum_{k \geq 1} \sqrt{\lambda_k}\xi_k \vect{\varphi}_k(.)
          \end{array}
        \right.

    If the function :math:`f(.) = X(\omega_0, .)` where :math:`X` is the centered process which covariance function is associated to the eigenvalues and eigenfunctions :math:`(\vect{\lambda}, \vect{\varphi})`, then the *getEigenValues* method enables to obtain the :math:`K` first eigenvalues of the Karhunen Loeve decomposition of :math:`X` and the method *getModes* enables to get the associated modes.

    Examples
    --------
    >>> import openturns as ot
    >>> N = 256
    >>> mesh = ot.IntervalMesher([N - 1]).build(ot.Interval(-1, 1))
    >>> covariance_X = ot.AbsoluteExponential([1])
    >>> process_X = ot.GaussianProcess(covariance_X, mesh)
    >>> s = 0.001
    >>> algo_X = ot.KarhunenLoeveP1Algorithm(mesh, covariance_X, s)
    >>> algo_X.run()
    >>> result_X = algo_X.getResult()
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
        return _algo.KarhunenLoeveResult_getClassName(self)

    def getThreshold(self):
        r"""
        Accessor to the limit ratio on eigenvalues.

        Returns
        -------
        s : float, :math:`\geq 0`
            The threshold :math:`s` used to select the most significant eigenmodes, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResult_getThreshold(self)

    def getCovarianceModel(self):
        """
        Accessor to the covariance model.

        Returns
        -------
        covModel : :class:`~openturns.CovarianceModel`
            The covariance model.
        """
        return _algo.KarhunenLoeveResult_getCovarianceModel(self)

    def getEigenValues(self):
        r"""
        Accessor to the eigenvalues of the Karhunen Loeve decomposition.

        Returns
        -------
        eigenVal : :class:`~openturns.Point`
            The most significant eigenvalues.

        Notes
        -----
        OpenTURNS truncates the sequence :math:`(\lambda_k,  \vect{\varphi}_k)_{k \geq 1}`  to the most significant terms, selected by the threshold defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResult_getEigenValues(self)

    def getModes(self):
        r"""
        Get the modes as functions.

        Returns
        -------
        modes : collection of :class:`~openturns.Function`
            The truncated basis :math:`(\vect{\varphi}_k)_{1 \leq k \leq K}`.

        Notes
        -----
        The basis is truncated to :math:`(\vect{\varphi}_k)_{1 \leq k \leq K}` where
        :math:`K`  is determined by the :math:`s`, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResult_getModes(self)

    def getModesAsProcessSample(self):
        r"""
        Accessor to the modes as a process sample.

        Returns
        -------
        modesAsProcessSample : :class:`~openturns.ProcessSample`
            The values of each mode on a mesh whose vertices were used to discretize the
            Fredholm equation.

        Notes
        -----
        The modes :math:`(\vect{\varphi}_k)_{1 \leq k \leq K}` are evaluated on the vertices of the mesh defining the process sample. The values of the i-th field are the values of the i-th mode on these vertices.

        The mesh corresponds to the discretization points of the integral in :eq:`projection`.
        """
        return _algo.KarhunenLoeveResult_getModesAsProcessSample(self)

    def getScaledModes(self):
        r"""
        Get the modes as functions scaled by the square-root of the corresponding eigenvalue.

        Returns
        -------
        modes : collection of :class:`~openturns.Function`
            The truncated basis :math:`(\sqrt{\lambda_k}\vect{\varphi}_k)_{1 \leq k \leq K}`.

        Notes
        -----
        The basis is truncated to :math:`(\sqrt{\lambda_k}\vect{\varphi}_k)_{1 \leq k \leq K}`
        where :math:`K` is determined by the :math:`s`, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResult_getScaledModes(self)

    def getScaledModesAsProcessSample(self):
        r"""
        Accessor to the scaled modes as a process sample.

        Returns
        -------
        modesAsProcessSample : :class:`~openturns.ProcessSample`
            The values of each scaled mode on a mesh whose vertices were used to
            discretize the Fredholm equation.

        Notes
        -----
        The modes :math:`(\vect{\varphi}_k)_{1 \leq k \leq K}` are evaluated on the
        vertices of the mesh defining the process sample. The values of the i-th field
        are the values of the i-th mode on these vertices.

        The mesh corresponds to the discretization points used to discretize the integral 
         :eq:`projection`.
        """
        return _algo.KarhunenLoeveResult_getScaledModesAsProcessSample(self)

    def getProjectionMatrix(self):
        """
        Accessor to the projection matrix.

        Returns
        -------
        projection : :class:`~openturns.Matrix`
            The  matrix :math:`M` defined in :eq:`projectionMatrix`.
        """
        return _algo.KarhunenLoeveResult_getProjectionMatrix(self)

    def getMesh(self):
        """
        Accessor to the mesh.

        Returns
        -------
        mesh : :class:`~openturns.Mesh`
            The mesh corresponds to the discretization points of the integral in
            :eq:`projection`.
        """
        return _algo.KarhunenLoeveResult_getMesh(self)

    def project(self, *args):
        r"""
        Project a function or a field on the eigenmodes basis.

        Available constructors:
            project(*function*)

            project(*functions*)

            project(*values*)

            project(*fieldSample*)

        Parameters
        ----------
        function : :class:`~openturns.Function`
            A function.
        functions : list of :class:`~openturns.Function`
            A list of functions.
        values :  :class:`~openturns.Sample`
            Field values.
        fieldSample :  :class:`~openturns.ProcessSample`
            A collection of fields.

        Returns
        -------
        point : :class:`~openturns.Point`
            The vector :math:`(\alpha_1, \dots, \alpha_K)` of the components of the function or the field in the eigenmodes basis
        sample : :class:`~openturns.Sample`
            The collection of the vectors :math:`(\alpha_1, \dots, \alpha_K)` of the components of the collection of functions or fields in the eigenmodes basis

        Notes
        -----
        The *project* method calculates the projection :eq:`projection` on a function  or a field where only the first :math:`K` elements of the sequences are calculated.
        :math:`K` is determined by the :math:`s`, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.

        Lets note :math:`\cM_{KL}` the mesh coming from the :class:`~openturns.KarhunenLoeveResult` (ie the one contained in the *modesAsSample* :class:`~openturns.ProcessSample`).

        The given values are defined on the input field :math:`\cM_{KL}` and the associated values are directly used for the projection.

        If evaluated from a function, the *project* method evaluates the function on :math:`\cM_{KL}` and uses :eq:`projectionMatrix`. 
        """
        return _algo.KarhunenLoeveResult_project(self, *args)

    def lift(self, coefficients):
        r"""
        Lift the coefficients into a function.

        Parameters
        ----------
        coef : :class:`~openturns.Point`
            The coefficients :math:`(\xi_1, \dots, \xi_K)`.

        Returns
        -------
        modes : :class:`~openturns.Function`
            The function :math:`f` defined in :eq:`lift`.

        Notes
        -----
        The sum defining :math:`f` is truncated to the first :math:`K` terms, where :math:`K`  is determined by the :math:`s`, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResult_lift(self, coefficients)

    def liftAsField(self, coefficients):
        r"""
        Lift the coefficients into a field.

        Parameters
        ----------
        coef : :class:`~openturns.Point`
            The coefficients :math:`(\xi_1, \dots, \xi_K)`.

        Returns
        -------
        modes : :class:`~openturns.Field`
            The function :math:`f` defined in :eq:`lift` evaluated on the mesh associated to the discretization of :eq:`projection`.

        Notes
        -----
        The sum defining :math:`f` is truncated to the first :math:`K` terms, where :math:`K` is determined by the :math:`s`, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResult_liftAsField(self, coefficients)

    def liftAsSample(self, coefficients):
        r"""
        Lift the coefficients into a sample.

        Parameters
        ----------
        coef : :class:`~openturns.Point`
            The coefficients :math:`(\xi_1, \dots, \xi_K)`.

        Returns
        -------
        modes : :class:`~openturns.Sample`
            The function :math:`f` defined in :eq:`lift` evaluated on the mesh associated to the discretization of :eq:`projection`.

        Notes
        -----
        The sum defining :math:`f` is truncated to the first :math:`K` terms, where :math:`K` is determined by the :math:`s`, defined in :class:`~openturns.KarhunenLoeveAlgorithm`.
        """
        return _algo.KarhunenLoeveResult_liftAsSample(self, coefficients)

    def __repr__(self):
        return _algo.KarhunenLoeveResult___repr__(self)

    def __str__(self, *args):
        return _algo.KarhunenLoeveResult___str__(self, *args)

    def __init__(self, *args):
        _algo.KarhunenLoeveResult_swiginit(self, _algo.new_KarhunenLoeveResult(*args))

    __swig_destroy__ = _algo.delete_KarhunenLoeveResult


_algo.KarhunenLoeveResult_swigregister(KarhunenLoeveResult)

class KarhunenLoeveAlgorithmImplementation(openturns.common.PersistentObject):
    r"""
    Base class for Karhunen Loeve algorithms.

    Parameters
    ----------
    covModel : :class:`~openturns.CovarianceModel`
        The covariance model.
    s : float, :math:`\geq0`
        The minimal relative amplitude of the eigenvalues to consider in
        the decomposition wrt the sum of the preceeding eigenvalues. The default value is 0.

    Notes
    -----
    The Karhunen Loeve decomposition enables to build some finite approximations of stochastic processes which are optimal with respect to the norm :math:`L^2`.

    We suppose that :math:`C:\cD \times \cD \rightarrow  \cS^+_d(\Rset)` is a covariance function defined on :math:`\cD \in \Rset^n`, continuous at :math:`\vect{0}`. 

    The class :class:`~openturns.KarhunenLoeveAlgorithm` enables to determine the solutions of the second kind Fredholm equation associated to  :math:`C`, ie to find the :math:`(\lambda_k,  \vect{\varphi}_k)_{k \geq 1}` such that: 

    .. math::
        :label: fredholm

        \int_{\cD} \mat{C}(\vect{s},\vect{t}) \vect{\varphi}_k(\vect{t})\,  d\vect{t} = \lambda_k  \vect{\varphi}_k(\vect{s}) \quad \forall \vect{s} \in \cD

    where :math:`(\lambda_k)_{k \geq 1}` is a nonincreasing sequence of nonnegative values (the **eigenvalues**) and :math:`(\vect{\varphi}_k)_{k \geq 1}` the   associated sequence of **eigenfunctions**, normalized by :math:`\int_{\cD}\|\vect{\varphi}_k(\vect{s})\|^2\di{\vect{s}}=1`. They form an hilbertian basis of :math:`L^2(\cD, \Rset^d)`.

    The Mercer theorem shows that the covariance function  :math:`C` writes:

    .. math::
        :label: covFuncMercer

        \mat{C}(\vect{s},\vect{t}) = \sum_{k=1}^{+\infty} \lambda_k \vect{\varphi}_k(\vect{s}) \Tr{\vect{\varphi}}_k(\vect{t}) \quad \forall (\vect{s}, \vect{t}) \in \cD \times \cD

    The threshold :math:`s` is used in order to select the most significant eigenvalues, ie all the eigenvalues such that (the infinite sum on the right being replaced by the sum of all computed eigenvalues in numerical algoritms): 

    .. math::
        :label: thresholdK

        K = \max \left\{k \in \Nset \, | \, \lambda_k \leq s \sum_{i\geq 1}\lambda_i \right\}

    To solve :eq:`fredholm`, we use the functional basis :math:`(\theta_p)_{1 \leq p \leq P}` of :math:`L^2(\cD, \Rset)` with :math:`P` elements defined on :math:`\cD`. We search the solutions of type:

    .. math::

        \tilde{\vect{\varphi}}_k(\vect{t})=\sum_{p=1}^{P} \vect{\phi}_{pk}\theta_p(\vect{t})

    where :math:`\vect{\phi}_{pk} \in \Rset^d`. We note:

    .. math::

        \begin{align*}
            \vect{\Phi}_k =
            \left(
              \begin{array}{l}
                \vect{\phi}_{1k} \\
                \dots \\
                \vect{\phi}_{Pk}
              \end{array}
            \right) \in \Rset^{Pd}
         \end{align*}

    and :math:`\mat{\vect{\Phi}} = (\vect{\Phi}_1\, |\, \dots \, | \vect{\Phi}_K)` the matrix of the :math:`K` first modes of the Karhunen Loeve decomposition.

    The approximated Fredholm problem writes for all :math:`k \geq 1`:

    .. math::

       \int_{\cD} \mat{C}(\vect{s},\vect{t}) \tilde{\vect{\varphi}}_k(\vect{t})\,  d\vect{t} = \lambda_k   \tilde{\vect{\varphi}}_k(\vect{s}) \quad  \forall \vect{s} \in \cD

    which enables to define the **residual function** :math:`\vect{r}: \cD \rightarrow \Rset^d` defined by

    .. math::
        :label: fredholmApprox

        \vect{r}(\vect{s}) = \int_{\cD} \mat{C}(\vect{s},\vect{t}) \tilde{\vect{\varphi}}_k(\vect{t})\,  d\vect{t} - \lambda_k  \tilde{\vect{\varphi}}_k(\vect{s})

    The Fredholm problem writes:

    .. math::
        :label: pbResidu

        \vect{r}(\vect{s}) = \vect{0} \quad \forall \vect{s} \in \cD

    which is solved either by the **Galerkin** approach or the **collocation** approach.

    The integrals in :eq:`fredholmApprox` can be evaluated with:

        - a :math:`P_1` -approach: see :class:`~openturns.KarhunenLoeveP1Algorithm`,
        - a quadrature approach: see :class:`~openturns.KarhunenLoeveQuadratureAlgorithm`,
        - a singular values decomposition approach: see :class:`~openturns.KarhunenLoeveSVDAlgorithm`.

    See also
    --------
    KarhunenLoeveResult
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
        return _algo.KarhunenLoeveAlgorithmImplementation_getClassName(self)

    def getThreshold(self):
        r"""
        Accessor to the threshold used to select the most significant eigenmodes.

        Returns
        -------
        s : float, positive
            The threshold :math:`s`. 

        Notes
        -----
        OpenTURNS truncates the sequence :math:`(\lambda_k,  \vect{\varphi}_k)_{k \geq 1}`  at the index :math:`K` defined in :eq:`thresholdK`.
        """
        return _algo.KarhunenLoeveAlgorithmImplementation_getThreshold(self)

    def setThreshold(self, threshold):
        r"""
        Accessor to the limit ratio on eigenvalues.

        Parameters
        ----------
        s : float, :math:`\geq 0`
            The threshold :math:`s` defined in :eq:`thresholdK`.
        """
        return _algo.KarhunenLoeveAlgorithmImplementation_setThreshold(self, threshold)

    def getCovarianceModel(self):
        """
        Accessor to the covariance model.

        Returns
        -------
        covModel : :class:`~openturns.CovarianceModel`
            The covariance model.
        """
        return _algo.KarhunenLoeveAlgorithmImplementation_getCovarianceModel(self)

    def setCovarianceModel(self, covariance):
        """
        Accessor to the covariance model.

        Parameters
        ----------
        covModel : :class:`~openturns.CovarianceModel`
            The covariance model.
        """
        return _algo.KarhunenLoeveAlgorithmImplementation_setCovarianceModel(self, covariance)

    def run(self):
        """
        Launch the algorithm.

        Notes
        -----
        It launches the algorithm and creates a :class:`~openturns.KarhunenLoeveResult`,
        structure containing all the results.
        """
        return _algo.KarhunenLoeveAlgorithmImplementation_run(self)

    def getResult(self):
        """
        Get the result structure.

        Returns
        -------
        resKL : :class:`~openturns.KarhunenLoeveResult`
            The structure containing all the results of the Fredholm problem.

        Notes
        -----
        The structure contains all the results of the Fredholm problem.
        """
        return _algo.KarhunenLoeveAlgorithmImplementation_getResult(self)

    def __repr__(self):
        return _algo.KarhunenLoeveAlgorithmImplementation___repr__(self)

    def __str__(self, *args):
        return _algo.KarhunenLoeveAlgorithmImplementation___str__(self, *args)

    def __init__(self, *args):
        _algo.KarhunenLoeveAlgorithmImplementation_swiginit(self, _algo.new_KarhunenLoeveAlgorithmImplementation(*args))

    __swig_destroy__ = _algo.delete_KarhunenLoeveAlgorithmImplementation


_algo.KarhunenLoeveAlgorithmImplementation_swigregister(KarhunenLoeveAlgorithmImplementation)

class KarhunenLoeveAlgorithmImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _algo.KarhunenLoeveAlgorithmImplementationTypedInterfaceObject_swiginit(self, _algo.new_KarhunenLoeveAlgorithmImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _algo.KarhunenLoeveAlgorithmImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _algo.KarhunenLoeveAlgorithmImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _algo.KarhunenLoeveAlgorithmImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _algo.KarhunenLoeveAlgorithmImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _algo.KarhunenLoeveAlgorithmImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _algo.delete_KarhunenLoeveAlgorithmImplementationTypedInterfaceObject


_algo.KarhunenLoeveAlgorithmImplementationTypedInterfaceObject_swigregister(KarhunenLoeveAlgorithmImplementationTypedInterfaceObject)

class KarhunenLoeveAlgorithm(KarhunenLoeveAlgorithmImplementationTypedInterfaceObject):
    r"""
    Base class for Karhunen Loeve algorithms.

    Parameters
    ----------
    covModel : :class:`~openturns.CovarianceModel`
        The covariance model.
    s : float, :math:`\geq0`
        The minimal relative amplitude of the eigenvalues to consider in
        the decomposition wrt the sum of the preceeding eigenvalues. The default value is 0.

    Notes
    -----
    The Karhunen Loeve decomposition enables to build some finite approximations of stochastic processes which are optimal with respect to the norm :math:`L^2`.

    We suppose that :math:`C:\cD \times \cD \rightarrow  \cS^+_d(\Rset)` is a covariance function defined on :math:`\cD \in \Rset^n`, continuous at :math:`\vect{0}`. 

    The class :class:`~openturns.KarhunenLoeveAlgorithm` enables to determine the solutions of the second kind Fredholm equation associated to  :math:`C`, ie to find the :math:`(\lambda_k,  \vect{\varphi}_k)_{k \geq 1}` such that: 

    .. math::
        :label: fredholm

        \int_{\cD} \mat{C}(\vect{s},\vect{t}) \vect{\varphi}_k(\vect{t})\,  d\vect{t} = \lambda_k  \vect{\varphi}_k(\vect{s}) \quad \forall \vect{s} \in \cD

    where :math:`(\lambda_k)_{k \geq 1}` is a nonincreasing sequence of nonnegative values (the **eigenvalues**) and :math:`(\vect{\varphi}_k)_{k \geq 1}` the   associated sequence of **eigenfunctions**, normalized by :math:`\int_{\cD}\|\vect{\varphi}_k(\vect{s})\|^2\di{\vect{s}}=1`. They form an hilbertian basis of :math:`L^2(\cD, \Rset^d)`.

    The Mercer theorem shows that the covariance function  :math:`C` writes:

    .. math::
        :label: covFuncMercer

        \mat{C}(\vect{s},\vect{t}) = \sum_{k=1}^{+\infty} \lambda_k \vect{\varphi}_k(\vect{s}) \Tr{\vect{\varphi}}_k(\vect{t}) \quad \forall (\vect{s}, \vect{t}) \in \cD \times \cD

    The threshold :math:`s` is used in order to select the most significant eigenvalues, ie all the eigenvalues such that (the infinite sum on the right being replaced by the sum of all computed eigenvalues in numerical algoritms): 

    .. math::
        :label: thresholdK

        K = \max \left\{k \in \Nset \, | \, \lambda_k \leq s \sum_{i\geq 1}\lambda_i \right\}

    To solve :eq:`fredholm`, we use the functional basis :math:`(\theta_p)_{1 \leq p \leq P}` of :math:`L^2(\cD, \Rset)` with :math:`P` elements defined on :math:`\cD`. We search the solutions of type:

    .. math::

        \tilde{\vect{\varphi}}_k(\vect{t})=\sum_{p=1}^{P} \vect{\phi}_{pk}\theta_p(\vect{t})

    where :math:`\vect{\phi}_{pk} \in \Rset^d`. We note:

    .. math::

        \begin{align*}
            \vect{\Phi}_k =
            \left(
              \begin{array}{l}
                \vect{\phi}_{1k} \\
                \dots \\
                \vect{\phi}_{Pk}
              \end{array}
            \right) \in \Rset^{Pd}
         \end{align*}

    and :math:`\mat{\vect{\Phi}} = (\vect{\Phi}_1\, |\, \dots \, | \vect{\Phi}_K)` the matrix of the :math:`K` first modes of the Karhunen Loeve decomposition.

    The approximated Fredholm problem writes for all :math:`k \geq 1`:

    .. math::

       \int_{\cD} \mat{C}(\vect{s},\vect{t}) \tilde{\vect{\varphi}}_k(\vect{t})\,  d\vect{t} = \lambda_k   \tilde{\vect{\varphi}}_k(\vect{s}) \quad  \forall \vect{s} \in \cD

    which enables to define the **residual function** :math:`\vect{r}: \cD \rightarrow \Rset^d` defined by

    .. math::
        :label: fredholmApprox

        \vect{r}(\vect{s}) = \int_{\cD} \mat{C}(\vect{s},\vect{t}) \tilde{\vect{\varphi}}_k(\vect{t})\,  d\vect{t} - \lambda_k  \tilde{\vect{\varphi}}_k(\vect{s})

    The Fredholm problem writes:

    .. math::
        :label: pbResidu

        \vect{r}(\vect{s}) = \vect{0} \quad \forall \vect{s} \in \cD

    which is solved either by the **Galerkin** approach or the **collocation** approach.

    The integrals in :eq:`fredholmApprox` can be evaluated with:

        - a :math:`P_1` -approach: see :class:`~openturns.KarhunenLoeveP1Algorithm`,
        - a quadrature approach: see :class:`~openturns.KarhunenLoeveQuadratureAlgorithm`,
        - a singular values decomposition approach: see :class:`~openturns.KarhunenLoeveSVDAlgorithm`.

    See also
    --------
    KarhunenLoeveResult
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
        return _algo.KarhunenLoeveAlgorithm_getClassName(self)

    def getThreshold(self):
        r"""
        Accessor to the threshold used to select the most significant eigenmodes.

        Returns
        -------
        s : float, positive
            The threshold :math:`s`. 

        Notes
        -----
        OpenTURNS truncates the sequence :math:`(\lambda_k,  \vect{\varphi}_k)_{k \geq 1}`  at the index :math:`K` defined in :eq:`thresholdK`.
        """
        return _algo.KarhunenLoeveAlgorithm_getThreshold(self)

    def setThreshold(self, threshold):
        r"""
        Accessor to the limit ratio on eigenvalues.

        Parameters
        ----------
        s : float, :math:`\geq 0`
            The threshold :math:`s` defined in :eq:`thresholdK`.
        """
        return _algo.KarhunenLoeveAlgorithm_setThreshold(self, threshold)

    def getCovarianceModel(self):
        """
        Accessor to the covariance model.

        Returns
        -------
        covModel : :class:`~openturns.CovarianceModel`
            The covariance model.
        """
        return _algo.KarhunenLoeveAlgorithm_getCovarianceModel(self)

    def setCovarianceModel(self, covariance):
        """
        Accessor to the covariance model.

        Parameters
        ----------
        covModel : :class:`~openturns.CovarianceModel`
            The covariance model.
        """
        return _algo.KarhunenLoeveAlgorithm_setCovarianceModel(self, covariance)

    def getResult(self):
        """
        Get the result structure.

        Returns
        -------
        resKL : :class:`~openturns.KarhunenLoeveResult`
            The structure containing all the results of the Fredholm problem.

        Notes
        -----
        The structure contains all the results of the Fredholm problem.
        """
        return _algo.KarhunenLoeveAlgorithm_getResult(self)

    def __repr__(self):
        return _algo.KarhunenLoeveAlgorithm___repr__(self)

    def __str__(self, *args):
        return _algo.KarhunenLoeveAlgorithm___str__(self, *args)

    def run(self):
        """
        Launch the algorithm.

        Notes
        -----
        It launches the algorithm and creates a :class:`~openturns.KarhunenLoeveResult`,
        structure containing all the results.
        """
        return _algo.KarhunenLoeveAlgorithm_run(self)

    def __init__(self, *args):
        _algo.KarhunenLoeveAlgorithm_swiginit(self, _algo.new_KarhunenLoeveAlgorithm(*args))

    __swig_destroy__ = _algo.delete_KarhunenLoeveAlgorithm


_algo.KarhunenLoeveAlgorithm_swigregister(KarhunenLoeveAlgorithm)

class KarhunenLoeveP1Algorithm(KarhunenLoeveAlgorithmImplementation):
    r"""
    Computation of Karhunen-Loeve decomposition using P1 approximation.

    Parameters
    ----------
    mesh : :class:`~openturns.Mesh`
        The mesh :math:`\cD_N` that discretizes the domain :math:`\cD`.
    covariance : :class:`~openturns.CovarianceModel`
        The covariance function to decompose.
    s : float, :math:`\geq0`
        The threshold used to select the most significant eigenmodes, defined in  :class:`~openturns.KarhunenLoeveAlgorithm`.

    Notes
    -----
    The Karhunen-Loeve :math:`P_1` algorithm solves the Fredholm problem  associated to the covariance function :math:`C`: see :class:`~openturns.KarhunenLoeveAlgorithm` to get the notations.

    The Karhunen-Loeve :math:`P_1` approximation uses the :math:`P_1` functional basis :math:`(\theta_p)_{1 \leq p \leq N}` where  :math:`\theta_p: \cD_N \mapsto \Rset` are the basis functions of the :math:`P_1` finite element space associated to :math:`\cD_N`, which vertices are :math:`(\vect{s}_i)_{1 \leq i \leq N}`.

    The covariance function :math:`\mat{C}` is approximated by its :math:`P_1` approximation :math:`\hat{\mat{C}}` on :math:`\cD_N`:

    .. math::

       \hat{\mat{C}}(\vect{s},\vect{t})=\sum_{\vect{s}_i,\vect{s}_j\in\cV_N}\mat{C}(\vect{s}_i,\vect{s}_j)\theta_i(\vect{s})\theta_j(\vect{t}), \quad  \forall \vect{s},\vect{t}\in\cD_N

    The Galerkin approach and the collocation one are equivalent in the :math:`P_1` approach and both lead to the following formulation:

    .. math::

        \mat{C}\, \mat{G}\, \mat{\Phi}  =   \mat{\Phi}\, \mat{\Lambda}

    where :math:`\mat{G} = (G_{ij})_{1\leq i,j \leq N}` with :math:`G_{i\ell}= \int_{\cD} \theta_i(\vect{s})\theta_\ell(\vect{s})\,  d\vect{s}`, :math:`\mat{\Lambda}=diag(\vect{\lambda})`.

    Examples
    --------
    Create a Karhunen-Loeve P1 algorithm:

    >>> import openturns as ot
    >>> mesh = ot.IntervalMesher([10]*2).build(ot.Interval([-1.0]*2, [1.0]*2))
    >>> s = 0.01
    >>> model = ot.AbsoluteExponential([1.0]*2)
    >>> algorithm = ot.KarhunenLoeveP1Algorithm(mesh, model, s)

    Run it!

    >>> algorithm.run()
    >>> result = algorithm.getResult()
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
        return _algo.KarhunenLoeveP1Algorithm_getClassName(self)

    def run(self):
        """
        Computation of the eigenvalues and eigenfunctions values at nodes.

        Notes
        -----
        Runs the algorithm and creates the result structure :class:`~openturns.KarhunenLoeveResult`.
        """
        return _algo.KarhunenLoeveP1Algorithm_run(self)

    def getMesh(self):
        r"""
        Accessor to the mesh.

        Returns
        -------
        mesh : :class:`~openturns.Mesh`
            The mesh :math:`\cD_N` that discretizes the domain :math:`\cD`.
        """
        return _algo.KarhunenLoeveP1Algorithm_getMesh(self)

    def __repr__(self):
        return _algo.KarhunenLoeveP1Algorithm___repr__(self)

    def __str__(self, *args):
        return _algo.KarhunenLoeveP1Algorithm___str__(self, *args)

    def __init__(self, *args):
        _algo.KarhunenLoeveP1Algorithm_swiginit(self, _algo.new_KarhunenLoeveP1Algorithm(*args))

    __swig_destroy__ = _algo.delete_KarhunenLoeveP1Algorithm


_algo.KarhunenLoeveP1Algorithm_swigregister(KarhunenLoeveP1Algorithm)

class KarhunenLoeveProjection(openturns.func.FieldToPointFunctionImplementation):
    """
    Function dedicated to the projection of fields on a Karhunen Loeve basis.

    Parameters
    ----------
    KLResult : :class:`~openturns.KarhunenLoeveResult`
        The result structure created by a :class:`~openturns.KarhunenLoeveAlgorithm`

    Notes
    -----
    The class :class:`~openturns.KarhunenLoeveProjection` is a specific function  :class:`~openturns.FieldToPointFunction` dedicated to the projection of fields on a Karhunen Loeve basis.

    See the documentation of :class:`~openturns.KarhunenLoeveResult` to get information on the projection function.

    The function acts on :class:`~openturns.Fields` or :class:`~openturns.ProcessSample` associated to a :class:`~openturns.Mesh` with an input dimension equal to :math:`n`.
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
        return _algo.KarhunenLoeveProjection_getClassName(self)

    def __eq__(self, other):
        return _algo.KarhunenLoeveProjection___eq__(self, other)

    def __repr__(self):
        return _algo.KarhunenLoeveProjection___repr__(self)

    def __str__(self, *args):
        return _algo.KarhunenLoeveProjection___str__(self, *args)

    def __call__(self, *args):
        return _algo.KarhunenLoeveProjection___call__(self, *args)

    def getMarginal(self, *args):
        r"""
        Get the marginal(s) at given indice(s).

        Parameters
        ----------
        i : int or list of ints, :math:`0 \leq i < d`
            Indice(s) of the marginal(s) to be extracted.
            output vector.

        Returns
        -------
        function : :class:`~openturns.KarhunenLoeveProjection`
            The initial function restricted to the concerned marginal(s) at the indice(s)
            :math:`i`.
        """
        return _algo.KarhunenLoeveProjection_getMarginal(self, *args)

    def __init__(self, *args):
        _algo.KarhunenLoeveProjection_swiginit(self, _algo.new_KarhunenLoeveProjection(*args))

    __swig_destroy__ = _algo.delete_KarhunenLoeveProjection


_algo.KarhunenLoeveProjection_swigregister(KarhunenLoeveProjection)

class KarhunenLoeveLifting(openturns.func.PointToFieldFunctionImplementation):
    """
    Function dedicated to the lift of Karhunen Loeve coefficients into a field.

    Parameters
    ----------
    KLResult : :class:`~openturns.KarhunenLoeveResult`
        The result structure created by a :class:`~openturns.KarhunenLoeveAlgorithm`

    Notes
    -----
    The class :class:`~openturns.KarhunenLoeveLifting` is a specific function  :class:`~openturns.PointToFieldFunction` dedicated to the lift of Karhunen Loeve coefficients into a field.

    See the documentation of :class:`~openturns.KarhunenLoeveResult` to get information on the lift function.

    The function acts on a vector of coefficients (:class:`~openturns.Point`) to create a field associated to the Karhunen Loeve mesh (:class:`~openturns.Mesh`).
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
        return _algo.KarhunenLoeveLifting_getClassName(self)

    def __eq__(self, other):
        return _algo.KarhunenLoeveLifting___eq__(self, other)

    def __repr__(self):
        return _algo.KarhunenLoeveLifting___repr__(self)

    def __str__(self, *args):
        return _algo.KarhunenLoeveLifting___str__(self, *args)

    def __call__(self, *args):
        return _algo.KarhunenLoeveLifting___call__(self, *args)

    def getMarginal(self, *args):
        r"""
        Get the marginal(s) at given indice(s).

        Parameters
        ----------
        i : int or list of ints, :math:`0 \leq i < d`
            Indice(s) of the marginal(s) to be extracted.
            output vector.

        Returns
        -------
        function : :class:`~openturns.KarhunenLoeveLifting`
            The initial function restricted to the concerned marginal(s) at the indice(s)
            :math:`i`.
        """
        return _algo.KarhunenLoeveLifting_getMarginal(self, *args)

    def __init__(self, *args):
        _algo.KarhunenLoeveLifting_swiginit(self, _algo.new_KarhunenLoeveLifting(*args))

    __swig_destroy__ = _algo.delete_KarhunenLoeveLifting


_algo.KarhunenLoeveLifting_swigregister(KarhunenLoeveLifting)

class ApproximationAlgorithmImplementationPointer(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    ptr_ = property(_algo.ApproximationAlgorithmImplementationPointer_ptr__get, _algo.ApproximationAlgorithmImplementationPointer_ptr__set)

    def __init__(self, *args):
        _algo.ApproximationAlgorithmImplementationPointer_swiginit(self, _algo.new_ApproximationAlgorithmImplementationPointer(*args))

    __swig_destroy__ = _algo.delete_ApproximationAlgorithmImplementationPointer

    def reset(self):
        return _algo.ApproximationAlgorithmImplementationPointer_reset(self)

    def __ref__(self, *args):
        return _algo.ApproximationAlgorithmImplementationPointer___ref__(self, *args)

    def __deref__(self, *args):
        return _algo.ApproximationAlgorithmImplementationPointer___deref__(self, *args)

    def isNull(self):
        return _algo.ApproximationAlgorithmImplementationPointer_isNull(self)

    def __nonzero__(self):
        return _algo.ApproximationAlgorithmImplementationPointer___nonzero__(self)

    __bool__ = __nonzero__

    def get(self):
        return _algo.ApproximationAlgorithmImplementationPointer_get(self)

    def getImplementation(self):
        return _algo.ApproximationAlgorithmImplementationPointer_getImplementation(self)

    def unique(self):
        return _algo.ApproximationAlgorithmImplementationPointer_unique(self)

    def use_count(self):
        return _algo.ApproximationAlgorithmImplementationPointer_use_count(self)

    def swap(self, other):
        return _algo.ApproximationAlgorithmImplementationPointer_swap(self, other)

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getClassName(self)

    def getX(self):
        """
        Accessor to the input sample.

        Returns
        -------
        x : :class:`~openturns.Sample`
            Input sample
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getX(self)

    def getY(self):
        """
        Accessor to the output sample.

        Returns
        -------
        y : :class:`~openturns.Sample`
            Input sample
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getY(self)

    def getWeight(self):
        """
        Accessor to the weights.

        Returns
        -------
        weight : :class:`~openturns.Point`
            Output weights
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getWeight(self)

    def getPsi(self):
        """
        Accessor to the basis.

        Returns
        -------
        coefficients : :class:`~openturns.Basis`
            The basis
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getPsi(self)

    def __repr__(self):
        return _algo.ApproximationAlgorithmImplementationPointer___repr__(self)

    def __str__(self, *args):
        return _algo.ApproximationAlgorithmImplementationPointer___str__(self, *args)

    def run(self):
        """Run the algorithm."""
        return _algo.ApproximationAlgorithmImplementationPointer_run(self)

    def getCoefficients(self):
        """
        Accessor to the coefficients.

        Returns
        -------
        coefficients : :class:`~openturns.Point`
            The coefficients
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getCoefficients(self)

    def getResidual(self):
        """
        Accessor to the coefficients.

        Returns
        -------
        coefficients : float
            The residual
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getResidual(self)

    def getRelativeError(self):
        """
        Accessor to the coefficients.

        Returns
        -------
        relativeError : float
            The relative error
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getRelativeError(self)

    def setVerbose(self, verbose):
        """
        Accessor to the verbosity flag.

        Parameters
        ----------
        v : bool
            Enable or disable the verbosity.
        """
        return _algo.ApproximationAlgorithmImplementationPointer_setVerbose(self, verbose)

    def getVerbose(self):
        """
        Accessor to the verbosity flag.

        Returns
        -------
        v : bool.
            Verbosity
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getVerbose(self)

    def __eq__(self, arg2):
        return _algo.ApproximationAlgorithmImplementationPointer___eq__(self, arg2)

    def __ne__(self, other):
        return _algo.ApproximationAlgorithmImplementationPointer___ne__(self, other)

    def getId(self):
        """
        Accessor to the object's id.

        Returns
        -------
        id : int
           Internal unique identifier.
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getId(self)

    def setShadowedId(self, id):
        """
        Accessor to the object's shadowed id.

        Parameters
        ----------
        id : int
            Internal unique identifier.
        """
        return _algo.ApproximationAlgorithmImplementationPointer_setShadowedId(self, id)

    def getShadowedId(self):
        """
        Accessor to the object's shadowed id.

        Returns
        -------
        id : int
            Internal unique identifier.
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getShadowedId(self)

    def setVisibility(self, visible):
        """
        Accessor to the object's visibility state.

        Parameters
        ----------
        visible : bool
            Visibility flag.
        """
        return _algo.ApproximationAlgorithmImplementationPointer_setVisibility(self, visible)

    def getVisibility(self):
        """
        Accessor to the object's visibility state.

        Returns
        -------
        visible : bool
            Visibility flag.
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getVisibility(self)

    def hasName(self):
        """
        Test if the object is named.

        Returns
        -------
        hasName : bool
            True if the name is not empty.
        """
        return _algo.ApproximationAlgorithmImplementationPointer_hasName(self)

    def hasVisibleName(self):
        """
        Test if the object has a distinguishable name.

        Returns
        -------
        hasVisibleName : bool
            True if the name is not empty and not the default one.
        """
        return _algo.ApproximationAlgorithmImplementationPointer_hasVisibleName(self)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _algo.ApproximationAlgorithmImplementationPointer_getName(self)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _algo.ApproximationAlgorithmImplementationPointer_setName(self, name)


_algo.ApproximationAlgorithmImplementationPointer_swigregister(ApproximationAlgorithmImplementationPointer)

class FFTImplementationPointer(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    ptr_ = property(_algo.FFTImplementationPointer_ptr__get, _algo.FFTImplementationPointer_ptr__set)

    def __init__(self, *args):
        _algo.FFTImplementationPointer_swiginit(self, _algo.new_FFTImplementationPointer(*args))

    __swig_destroy__ = _algo.delete_FFTImplementationPointer

    def reset(self):
        return _algo.FFTImplementationPointer_reset(self)

    def __ref__(self, *args):
        return _algo.FFTImplementationPointer___ref__(self, *args)

    def __deref__(self, *args):
        return _algo.FFTImplementationPointer___deref__(self, *args)

    def isNull(self):
        return _algo.FFTImplementationPointer_isNull(self)

    def __nonzero__(self):
        return _algo.FFTImplementationPointer___nonzero__(self)

    __bool__ = __nonzero__

    def get(self):
        return _algo.FFTImplementationPointer_get(self)

    def getImplementation(self):
        return _algo.FFTImplementationPointer_getImplementation(self)

    def unique(self):
        return _algo.FFTImplementationPointer_unique(self)

    def use_count(self):
        return _algo.FFTImplementationPointer_use_count(self)

    def swap(self, other):
        return _algo.FFTImplementationPointer_swap(self, other)

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _algo.FFTImplementationPointer_getClassName(self)

    def transform(self, *args):
        r"""
        Perform Fast Fourier Transform (fft).

        Parameters
        ----------
        collection : :class:`~openturns.ComplexCollection` or :class:`~openturns.ScalarCollection`, sequence of float
          Data to transform.

        Returns
        -------
        collection : :class:`~openturns.ComplexCollection`
          The data in Fourier domain.

        Notes
        -----
        The Fast Fourier Transform writes as following:

        .. math::

            {\rm y_k} = \sum_{n=0}^{N-1} x_n exp(-2 i \pi \frac{kn}{N})

        where :math:`x` denotes the data to be transformed, of size :math:`N`.

        Examples
        --------
        >>> import openturns as ot
        >>> fft = ot.FFT()
        >>> result = fft.transform(ot.Normal(8).getRealization())

        """
        return _algo.FFTImplementationPointer_transform(self, *args)

    def inverseTransform(self, *args):
        r"""
        Perform Inverse Fast Fourier Transform (fft).

        Parameters
        ----------
        collection : :class:`~openturns.ComplexCollection` or :class:`~openturns.ScalarCollection`, sequence of float
          Data to transform.

        Returns
        -------
        collection : :class:`~openturns.ComplexCollection`
            The transformed data.

        Notes
        -----
        The Inverse Fast Fourier Transform writes as following:

        .. math::

            {\rm y_k} = \sum_{n=0}^{N-1} \frac{1}{N} x_n exp(2 i \pi \frac{kn}{N})

        where :math:`x` denotes the data, of size :math:`N`, to be transformed.

        Examples
        --------
        >>> import openturns as ot
        >>> fft = ot.FFT()
        >>> collection = ot.ComplexCollection([1+1j,2-0.3j,5-.3j,6+1j,9+8j,16+8j,0.3])
        >>> result = fft.inverseTransform(collection)

        """
        return _algo.FFTImplementationPointer_inverseTransform(self, *args)

    def transform2D(self, *args):
        r"""
        Perform 2D FFT.

        Parameters
        ----------
        matrix : :class:`~openturns.ComplexMatrix`, :class:`~openturns.Matrix`, 2-d sequence of float
          Data to transform.

        Returns
        -------
        result : :class:`~openturns.ComplexMatrix`
          The data in fourier domain.

        Notes
        -----
        The 2D Fast Fourier Transform writes as following:

        .. math::

            {\rm Z_{k,l}} = \sum_{m=0}^{M-1}\sum_{n=0}^{N-1} X_{m,n} exp(-2 i \pi \frac{km}{M}) exp(-2 i \pi \frac{ln}{N})

        where :math:`X` denotes the data to be transformed with shape (:math:`M`,:math:`N`)

        Examples
        --------
        >>> import openturns as ot
        >>> fft = ot.FFT()
        >>> x = ot.Normal(8).getSample(16)
        >>> result = fft.transform2D(x)

        """
        return _algo.FFTImplementationPointer_transform2D(self, *args)

    def inverseTransform2D(self, *args):
        r"""
        Perform 2D IFFT.

        Parameters
        ----------
        matrix : :class:`~openturns.ComplexMatrix`, :class:`~openturns.Matrix`, 2-d sequence of float
          Data to transform.

        Returns
        -------
        result : :class:`~openturns.ComplexMatrix`
          The data transformed.

        Notes
        -----
        The 2D Fast Inverse Fourier Transform writes as following:

        .. math::

            {\rm Y_{k,l}} = \frac{1}{M\times N}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1} Z_{m,n} exp(2 i \pi \frac{km}{M}) exp(2 i \pi \frac{ln}{N})

        where :math:`Z` denotes the data to be transformed with shape (:math:`M`,:math:`N`)

        Examples
        --------
        >>> import openturns as ot
        >>> fft = ot.FFT()
        >>> x = ot.Normal(8).getSample(16)
        >>> result = fft.inverseTransform2D(x)

        """
        return _algo.FFTImplementationPointer_inverseTransform2D(self, *args)

    def transform3D(self, *args):
        r"""
        Perform 3D FFT.

        Parameters
        ----------
        tensor : :class:`~openturns.ComplexTensor` or :class:`~openturns.Tensor` or 3d array
          Data to transform.

        Returns
        -------
        result : :class:`~openturns.ComplexTensor`
          The data in fourier domain.

        Notes
        -----
        The 3D Fast Fourier Transform writes as following:

        .. math::

            {\rm Z_{k,l,r}} = \sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\sum_{p=0}^{P-1} X_{m,n,p} exp(-2 i \pi \frac{km}{M}) exp(-2 i \pi \frac{ln}{N}) exp(-2 i \pi \frac{rp}{P})

        where :math:`X` denotes the data to be transformed with shape (:math:`M`,:math:`N`, :math:`P`)

        Examples
        --------
        >>> import openturns as ot
        >>> fft = ot.FFT()
        >>> x = ot.ComplexTensor(8,8,2)
        >>> y = ot.Normal(8).getSample(8)
        >>> x.setSheet(0,fft.transform2D(y))
        >>> z = ot.Normal(8).getSample(8)
        >>> x.setSheet(1,fft.transform2D(z))
        >>> result = fft.transform3D(x)

        """
        return _algo.FFTImplementationPointer_transform3D(self, *args)

    def inverseTransform3D(self, *args):
        r"""
        Perform 3D IFFT.

        Parameters
        ----------
        tensor : :class:`~openturns.ComplexTensor` or :class:`~openturns.Tensor` or 3d array
          The data to be transformed.

        Returns
        -------
        result : :class:`~openturns.ComplexTensor`
          The transformed data.

        Notes
        -----
        The 3D Inverse Fast Fourier Transform writes as following:

        .. math::

            {\rm Y_{k,l,r}} = \sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\sum_{p=0}^{P-1} \frac{1}{M\times N \times P} Z_{m,n,p} exp(2 i \pi \frac{km}{M}) exp(2 i \pi \frac{ln}{N}) exp(2 i \pi \frac{rp}{P})

        where :math:`Z` denotes the data to be transformed with shape (:math:`M`, :math:`N`, :math:`P`)

        Examples
        --------
        >>> import openturns as ot
        >>> fft = ot.FFT()
        >>> x = ot.ComplexTensor(8,8,2)
        >>> y = ot.Normal(8).getSample(8)
        >>> x.setSheet(0, fft.transform2D(y))
        >>> z = ot.Normal(8).getSample(8)
        >>> x.setSheet(1, fft.transform2D(z))
        >>> result = fft.inverseTransform3D(x)

        """
        return _algo.FFTImplementationPointer_inverseTransform3D(self, *args)

    def __repr__(self):
        return _algo.FFTImplementationPointer___repr__(self)

    def __str__(self, *args):
        return _algo.FFTImplementationPointer___str__(self, *args)

    def __eq__(self, arg2):
        return _algo.FFTImplementationPointer___eq__(self, arg2)

    def __ne__(self, other):
        return _algo.FFTImplementationPointer___ne__(self, other)

    def getId(self):
        """
        Accessor to the object's id.

        Returns
        -------
        id : int
           Internal unique identifier.
        """
        return _algo.FFTImplementationPointer_getId(self)

    def setShadowedId(self, id):
        """
        Accessor to the object's shadowed id.

        Parameters
        ----------
        id : int
            Internal unique identifier.
        """
        return _algo.FFTImplementationPointer_setShadowedId(self, id)

    def getShadowedId(self):
        """
        Accessor to the object's shadowed id.

        Returns
        -------
        id : int
            Internal unique identifier.
        """
        return _algo.FFTImplementationPointer_getShadowedId(self)

    def setVisibility(self, visible):
        """
        Accessor to the object's visibility state.

        Parameters
        ----------
        visible : bool
            Visibility flag.
        """
        return _algo.FFTImplementationPointer_setVisibility(self, visible)

    def getVisibility(self):
        """
        Accessor to the object's visibility state.

        Returns
        -------
        visible : bool
            Visibility flag.
        """
        return _algo.FFTImplementationPointer_getVisibility(self)

    def hasName(self):
        """
        Test if the object is named.

        Returns
        -------
        hasName : bool
            True if the name is not empty.
        """
        return _algo.FFTImplementationPointer_hasName(self)

    def hasVisibleName(self):
        """
        Test if the object has a distinguishable name.

        Returns
        -------
        hasVisibleName : bool
            True if the name is not empty and not the default one.
        """
        return _algo.FFTImplementationPointer_hasVisibleName(self)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _algo.FFTImplementationPointer_getName(self)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _algo.FFTImplementationPointer_setName(self, name)


_algo.FFTImplementationPointer_swigregister(FFTImplementationPointer)