# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/cubepy/axis.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 5915 bytes
import numpy as np

class Axis(object):
    __doc__ = 'A named sequence of values. Can be used as non-indexable axis in Cube.\n    Name is a string. Values are stored in one-dimensional numpy array.\n    '

    def __init__(self, name, values):
        """Initializes Axis object.
        :param name: str
        :param values: sequence of values of the same type, are converted to 1-D numpy array
        :raise: ValueError if values cannot be converted, TypeError if name is not string
        """
        if not isinstance(name, str):
            raise TypeError('type of {} is not str'.format(repr(name)))
        values = np.atleast_1d(values)
        if values.ndim > 1:
            raise ValueError('values must not have more than 1 dimension')
        self._name = name
        self._values = values

    def __repr__(self):
        """Returns textual representation of Axis object. Can be reused by inherited classes.
        :return: str
        """
        return "{}('{}', {})".format(self.__class__.__name__, self._name, self._values)

    def __len__(self):
        """Returns the number of elements in (the length) the axis.
        :return: int
        """
        return len(self._values)

    def __getitem__(self, item):
        """
        :param item:
        :return: a new Axis object
        """
        _newValues = self._values[item]
        if isinstance(_newValues, str):
            _newValues = [
             _newValues]
        else:
            if 'numpy.' in str(type(_newValues)):
                _newValues = _newValues.flatten()
        return self.__class__(self._name, _newValues)

    def __sizeof__(self):
        return self.values.nbytes

    def __eq__(self, other):
        return apply_op(self, other, np.ndarray.__eq__)

    def __ne__(self, other):
        return apply_op(self, other, np.ndarray.__ne__)

    def __lt__(self, other):
        return apply_op(self, other, np.ndarray.__lt__)

    def __le__(self, other):
        return apply_op(self, other, np.ndarray.__le__)

    def __gt__(self, other):
        return apply_op(self, other, np.ndarray.__gt__)

    def __ge__(self, other):
        return apply_op(self, other, np.ndarray.__ge__)

    @property
    def name(self):
        """Returns he name of the axis.
        :return: str
        """
        return self._name

    @property
    def values(self):
        """Returns one-dimensional numpy.ndarray of axis values.
        :return: numpy.ndarray
        """
        return self._values

    def filter(self, values):
        """Filter axis elements which are contained in values. The axis order is preserved.
        :param values: a value or a list, set, tuple or numpy array of values
            the order or values is irrelevant, need not be unique
        :return:
        """
        if isinstance(values, set):
            values = list(values)
        values = np.asarray(values)
        selection = np.in1d(self._values, values)
        return self.__class__(self._name, self._values[selection])

    def like(self, text):
        """Return Cube with  this index and True when elemen contains text
        """
        from pyplan_core.cubepy.cube import Cube
        _vals = []
        for _value in self.values:
            if text in str(_value):
                _vals.append(True)
            else:
                _vals.append(False)

        return Cube([self], _vals)

    def take(self, indices):
        """Analogy to numpy.ndarray.take.
        :return: a new Axis object
        """
        return self.__class__(self._name, self._values.take(indices))

    def compress(self, condition):
        """Analogy to numpy.ndarray.compress.
        :return: a new Axis object
        """
        return self.__class__(self._name, self._values.compress(condition))

    def rename(self, new_name):
        """Returns a new object (of type Axis or the actual derived type) with the new name and the same values.
        :param new_name: str
        :return: new axis (instance of actual derived type)
        """
        return self.__class__(new_name, self._values)

    def sort(self):
        """Sorts the values.
        :return: a new Axis object with sorted values
        """
        return self.__class__(self._name, np.sort(self._values))

    def astype(self, dtype):
        """ change dtype of values of index """
        return self.__class__(self._name, self.values.real.astype(dtype, copy=False))

    def apply(self, func, *args):
        """Applies a function to each element individually and return the new index.
        :param func: function to be applied to values
        :param args: additional optional arguments of func
        :return: new Index  instance

        Examples:
        cube.apply(lambda x: x[0:5] )
        """
        func = np.vectorize(func)
        np_values = func(self.values, *args)
        seripandas = pd.Series(np_values)
        return self.__class__(self._name, seripandas.unique())

    def generateDefinition(self):
        """Generate code for inex definition"""
        np.set_printoptions(threshold=(np.prod(self.values.shape)))
        data = np.array2string((self.values), separator=',').replace('\n', '')
        deff = 'result = cp.index(' + data + ')'
        return deff


def apply_op(a, b, fn, *args):
    from pyplan_core.cubepy.cube import Cube
    if isinstance(a, Axis):
        if isinstance(b, Axis):
            return getattr(Cube([a], a.values), fn.__name__)(Cube([b], b.values))
    if isinstance(a, Axis):
        return Cube([a], fn(a.values, b, *args))
    return Cube([b], fn(b.values, a, *args))