# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/marcel/Dropbox/marcel/repos/numphy/numphy/core.py
# Compiled at: 2018-05-02 13:47:51
"""
Numphy core implementation.
"""
__all__ = [
 'Wrapper', 'Trace', 'DataProxy',
 'is_numpy', 'is_tensorflow', 'map_struct',
 't', 'HAS_NUMPY', 'HAS_TENSORFLOW']
from copy import deepcopy
from operator import mul
from numphy.util import no_value, is_lazy_iterable
import six, wrapt
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False

try:
    import tensorflow as tf
    HAS_TENSORFLOW = True
except ImportError:
    tf = None
    HAS_TENSORFLOW = False

def is_numpy(obj):
    """
    Returns *True* when *obj* is a numpy object.
    """
    return HAS_NUMPY and type(obj).__module__.split('.', 1)[0] == 'numpy'


def is_tensorflow(obj):
    """
    Returns *True* when *obj* is a tensorflow object.
    """
    return HAS_TENSORFLOW and type(obj).__module__.split('.', 1)[0] == 'tensorflow'


def map_struct(func, struct):
    if is_lazy_iterable(struct):
        struct = list(struct)
    new_struct = (isinstance(struct, tuple) or struct.__class__)() if isinstance(struct, (dict, list, tuple, set)) else []
    if isinstance(struct, (list, tuple)):
        gen = enumerate(struct)
        add = lambda _, value: new_struct.append(value)
    else:
        if isinstance(struct, set):
            gen = enumerate(struct)
            add = lambda _, value: new_struct.add(value)
        else:
            gen = six.iteritems(struct)
            add = lambda key, value: new_struct.__setitem__(key, value)
        for key, value in gen:
            value = map_struct(func, value)
            add(key, value)

        if isinstance(struct, tuple):
            new_struct = struct.__class__(new_struct)
        return new_struct
    if HAS_NUMPY and isinstance(struct, np.ndarray):
        if struct.dtype == 'O':
            n = reduce(mul, struct.shape, 1) if struct.shape else 0
            if n == 0:
                copy = np.array(None, dtype=struct.dtype)
                copy[()] = map_struct(func, struct[()])
            else:
                copy = np.array(n * [None], dtype=struct.dtype)
                for i in range(n):
                    copy[i] = map_struct(func, struct.item(i))

                copy = copy.reshape(struct.shape)
            return copy
        if struct.dtype.names:
            copy = np.array(struct)
            for name in struct.dtype.names:
                copy[name] = map_struct(func, struct[name])

            return copy
    return func(struct)


class Trace(object):

    @classmethod
    def get(cls, trace, struct):
        values = trace.values if isinstance(trace, cls) else cls._make_tuple(trace)
        return cls._get(values, struct)

    @classmethod
    def _get(cls, trace_values, struct):
        if not trace_values:
            return struct
        first, rest = trace_values[0], trace_values[1:]
        return cls.get(rest, struct[first])

    @classmethod
    def set(cls, trace, struct, value):
        values = trace.values if isinstance(trace, cls) else cls._make_tuple(trace)
        return cls._set(values, struct, value)

    @classmethod
    def _set(cls, trace_values, struct, value):
        if not trace_values:
            return value
        first, rest = trace_values[0], trace_values[1:]
        struct[first] = cls._set(rest, struct[first], value)
        return struct

    @classmethod
    def _make_tuple(cls, values):
        if isinstance(values, tuple):
            return values
        return (values,)

    def __init__(self, values=None):
        super(Trace, self).__init__()
        self._values = tuple()
        if values is not None:
            self.values = values
        return

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        if isinstance(values, self.__class__):
            values = values.values
        self._values = self._make_tuple(values)

    def __repr__(self):
        return ('<{} {} at {}>').format(self.__class__.__name__, str(self), hex(id(self)))

    def __str__(self):
        return self.values.__str__()

    def __len__(self):
        return self.values.__len__()

    def __nonzero__(self):
        return len(self) > 0

    def __contains__(self, value):
        return value in self.values

    def __eq__(self, trace):
        values = trace.values if isinstance(trace, self.__class__) else self._make_tuple(trace)
        return self.values == values

    def __getitem__(self, key):
        item = self.values.__getitem__(key)
        if isinstance(key, six.integer_types):
            return item
        return self.__class__(item)

    def __setitem__(self, key, value):
        values = list(self.values)
        try:
            values.__setitem__(key, value)
        except IndexError:
            raise IndexError(('index {} out of range for trace {!r}').format(key, self))
        except TypeError:
            raise TypeError(('trace indices must be integers, not {}').format(type(key).__name__))

        self.values = tuple(values)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return self.__class__(self.values + other.values)

    def __radd__(self, other):
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return self.__class__(other.values + self.values)

    def __iadd__(self, other):
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        self.values = self.values + other.values
        return self

    def __call__(self, struct, value=no_value):
        if value is no_value:
            return self.get(self, struct)
        else:
            return self.set(self, struct, value)


class _TraceFactory(object):

    def __getitem__(self, trace):
        if isinstance(trace, Trace):
            return trace
        return Trace(trace)


t = _TraceFactory()

class DataProxy(wrapt.ObjectProxy):

    def __init__(self, wrapped=None):
        super(DataProxy, self).__init__(wrapped)

    def __repr__(self):
        return self.__wrapped__.__repr__()

    def __call__(self, wrapped=no_value):
        if wrapped is not no_value:
            self.__wrapped__ = wrapped
        return self.__wrapped__


class Wrapper(object):
    __slots__ = [
     '_data_proxy', '_trace', '_attributes']

    @staticmethod
    def _get_data(obj):
        if isinstance(obj, Wrapper):
            return obj.data
        return obj

    def __init__(self, data=None, trace=None, attrs=None):
        super(Wrapper, self).__init__()
        self._data_proxy = DataProxy()
        self._trace = Trace()
        self._attributes = {}
        self.wrap(data)
        self.trace = trace
        if attrs:
            for attr, obj in six.iteritems(attrs):
                self.sub(obj, attr=attr)

    @property
    def data_proxy(self):
        return self._data_proxy

    @data_proxy.setter
    def data_proxy(self, data_proxy):
        if not isinstance(data_proxy, DataProxy):
            data_proxy = DataProxy(data_proxy)
        self._data_proxy = data_proxy

    @property
    def trace(self):
        return self._trace

    @trace.setter
    def trace(self, trace):
        if not isinstance(trace, Trace):
            trace = Trace(trace)
        self._trace = trace

    def update_trace(self, func, recursive=True):
        self.trace = func(self.trace)
        if recursive:
            for wrapper in six.itervalues(self._attributes):
                wrapper.update_trace(func, recursive=recursive)

    @property
    def data(self):
        if self.is_empty():
            return
        else:
            if not self.trace:
                return self.data_proxy()
            else:
                return self.trace(self.data_proxy())

            return

    @data.setter
    def data(self, data):
        if self.is_empty():
            raise Exception('cannot inject data when data proxy is empty')
        if not self.trace:
            self.data_proxy(data)
        else:
            self.trace(self.data_proxy, self._get_data(data))

    def __call__(self, data=no_value):
        if data is not no_value:
            self.data = data
        return self.data

    def __getattr__(self, attr):
        if not hasattr(self, '_attributes') or attr not in self._attributes:
            raise AttributeError(("unknown attribute '{}'").format(attr))
        return self._attributes[attr]

    def __setattr__(self, attr, value):
        if hasattr(self, '_attributes') and attr in self._attributes:
            if isinstance(value, Wrapper):
                self.sub(value, attr=attr)
            else:
                self._attributes[attr].data = value
        else:
            super(Wrapper, self).__setattr__(attr, value)

    def __getitem__(self, trace):
        if not isinstance(trace, Trace):
            trace = Trace(trace)
        if len(trace) != 1:
            msg = '{} objects only support item slicing with one expression, got {!s}'
            raise Exception(msg.format(self.__class__.__name__, trace))
        copy = self.copy(deep=False, inject_trace=trace)
        return copy

    def __setitem__(self, trace, value):
        self.__getitem__(trace).data = value

    def __repr__(self):
        return repr(self.data)

    def __contains__(self, value):
        return value in self.data

    def __nonzero__(self):
        return bool(self.data)

    def __sizeof__(self):
        return self.data.__sizeof__()

    def __len__(self):
        return len(self.data)

    def __array__(self, *args, **kwargs):
        return self.data.__array__(*args, **kwargs)

    def is_empty(self):
        return self.data_proxy() is None

    def is_numpy(self):
        return is_numpy(self.data_proxy())

    def is_tensorflow(self):
        return is_tensorflow(self.data_proxy())

    def wrap(self, data, recursive=True, overwrite=False, _first=True):
        """ wrap(data, recursive=True, overwrite=False)
        """
        if isinstance(data, DataProxy):
            data_proxy = data
        else:
            data_proxy = DataProxy(data)
        if _first or overwrite or self.data_proxy() is None:
            self.data_proxy = data_proxy
        if recursive:
            for wrapper in six.itervalues(self._attributes):
                wrapper.wrap(data_proxy, recursive=recursive, overwrite=overwrite, _first=False)

        return

    def sub(self, obj, attr=None, attrs=None, cls=None, wrap=None):
        if isinstance(obj, self.__class__):
            wrapper = obj
            trace = wrapper.trace
        else:
            if cls is None:
                cls = self.__class__
            wrapper = cls()
            trace = obj
        if attr:
            self._attributes[attr] = wrapper
        if isinstance(wrap, dict):
            wrapper.wrap(self.data_proxy, _first=False, **wrap)
        elif wrap is None and wrapper.is_empty() or wrap:
            wrapper.wrap(self.data_proxy)
        wrapper.trace = self.trace + trace
        if attrs:
            for attr, obj in six.iteritems(attrs):
                wrapper.sub(obj, attr=attr)

        return wrapper

    def copy(self, inject_trace=(), deep=False):
        if not deep:
            data = self.data_proxy
            trace = self.trace + inject_trace
        else:
            data = DataProxy(deepcopy(self.data))
            trace = inject_trace
        attrs = {}
        for attr, wrapper in six.iteritems(self._attributes):
            wrapper = wrapper.copy(deep=False)
            wrapper.trace = wrapper.trace[len(self.trace):]
            attrs[attr] = wrapper

        return self.__class__(data=data, trace=trace, attrs=attrs)

    def __copy__(self):
        return self.copy(deep=False)

    def __deepcopy__(self, memo):
        return self.copy(deep=True)

    def _map_copy(self, func):
        copy = self.copy(deep=True)
        copy.data = map_struct(func, copy.data)
        return copy

    def _map_inplace(self, func):
        self.data = map_struct(func, self.data)
        return self

    def __eq__(self, value):
        return self.data == self._get_data(value)

    def __ne__(self, value):
        return self.data != self._get_data(value)

    def __lt__(self, value):
        return self.data < self._get_data(value)

    def __le__(self, value):
        return self.data <= self._get_data(value)

    def __gt__(self, value):
        return self.data > self._get_data(value)

    def __ge__(self, value):
        return self.data >= self._get_data(value)

    def __pos__(self):
        return self.copy(deep=True)

    def __neg__(self):
        return self * -1

    def __abs__(self):
        return self._map_copy(lambda obj: abs(obj))

    def __invert__(self):
        return self._map_copy(lambda obj: ~obj)

    def __and__(self, value):
        return self._map_copy(lambda obj: obj & value)

    def __rand__(self, value):
        return self._map_copy(lambda obj: value & obj)

    def __iand__(self, value):
        return self._map_inplace(lambda obj: obj & value)

    def __or__(self, value):
        return self._map_copy(lambda obj: obj | value)

    def __ror__(self, value):
        return self._map_copy(lambda obj: value | obj)

    def __ior__(self, value):
        return self._map_inplace(lambda obj: obj | value)

    def __xor__(self, value):
        return self._map_copy(lambda obj: obj ^ value)

    def __rxor__(self, value):
        return self._map_copy(lambda obj: value ^ obj)

    def __ixor__(self, value):
        return self._map_inplace(lambda obj: obj ^ value)

    def __lshift__(self, value):
        return self._map_copy(lambda obj: obj << value)

    def __rlshift__(self, value):
        return self._map_copy(lambda obj: value << obj)

    def __ilshift__(self, value):
        return self._map_inplace(lambda obj: obj << value)

    def __rshift__(self, value):
        return self._map_copy(lambda obj: obj >> value)

    def __rrshift__(self, value):
        return self._map_copy(lambda obj: value >> obj)

    def __irshift__(self, value):
        return self._map_inplace(lambda obj: obj >> value)

    def __add__(self, value):
        return self._map_copy(lambda obj: obj + value)

    def __radd__(self, value):
        return self._map_copy(lambda obj: value + obj)

    def __iadd__(self, value):
        return self._map_inplace(lambda obj: obj + value)

    def __sub__(self, value):
        return self._map_copy(lambda obj: obj - value)

    def __rsub__(self, value):
        return self._map_copy(lambda obj: value - obj)

    def __isub__(self, value):
        return self._map_inplace(lambda obj: obj - value)

    def __mul__(self, value):
        return self._map_copy(lambda obj: obj * value)

    def __rmul__(self, value):
        return self._map_copy(lambda obj: value * obj)

    def __imul__(self, value):
        return self._map_inplace(lambda obj: obj * value)

    def __div__(self, value):
        return self._map_copy(lambda obj: obj / value)

    def __rdiv__(self, value):
        return self._map_copy(lambda obj: value / obj)

    def __idiv__(self, value):
        return self._map_inplace(lambda obj: obj / value)

    def __truediv__(self, value):
        return self._map_copy(lambda obj: obj / value)

    def __rtruediv__(self, value):
        return self._map_copy(lambda obj: value / obj)

    def __itruediv__(self, value):
        return self._map_inplace(lambda obj: obj / value)

    def __floordiv__(self, value):
        return self._map_copy(lambda obj: obj // value)

    def __rfloordiv__(self, value):
        return self._map_copy(lambda obj: value // obj)

    def __ifloordiv__(self, value):
        return self._map_inplace(lambda obj: obj // value)

    def __mod__(self, value):
        return self._map_copy(lambda obj: obj % value)

    def __rmod__(self, value):
        return self._map_copy(lambda obj: value % obj)

    def __imod__(self, value):
        return self._map_inplace(lambda obj: obj % value)

    def __pow__(self, value):
        return self._map_copy(lambda obj: obj ** value)

    def __rpow__(self, value):
        return self._map_copy(lambda obj: value ** obj)

    def __ipow__(self, value):
        return self._map_inplace(lambda obj: obj ** value)