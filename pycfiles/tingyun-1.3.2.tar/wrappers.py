# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/packages/wrapt/wrappers.py
# Compiled at: 2016-06-30 06:13:10
import sys, functools, operator, weakref, inspect
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    string_types = (
     str,)
else:
    string_types = (
     basestring,)

def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    return meta('NewBase', bases, {})


class _ObjectProxyMethods(object):

    @property
    def __module__(self):
        return self.__wrapped__.__module__

    @__module__.setter
    def __module__(self, value):
        self.__wrapped__.__module__ = value

    @property
    def __doc__(self):
        return self.__wrapped__.__doc__

    @__doc__.setter
    def __doc__(self, value):
        self.__wrapped__.__doc__ = value

    @property
    def __dict__(self):
        return self.__wrapped__.__dict__

    @property
    def __weakref__(self):
        return self.__wrapped__.__weakref__


class _ObjectProxyMetaType(type):

    def __new__(cls, name, bases, dictionary):
        dictionary.update(vars(_ObjectProxyMethods))
        return type.__new__(cls, name, bases, dictionary)


class ObjectProxy(with_metaclass(_ObjectProxyMetaType)):
    __slots__ = '__wrapped__'

    def __init__(self, wrapped):
        object.__setattr__(self, '__wrapped__', wrapped)
        try:
            object.__setattr__(self, '__qualname__', wrapped.__qualname__)
        except AttributeError:
            pass

    @property
    def __name__(self):
        return self.__wrapped__.__name__

    @__name__.setter
    def __name__(self, value):
        self.__wrapped__.__name__ = value

    @property
    def __class__(self):
        return self.__wrapped__.__class__

    @__class__.setter
    def __class__(self, value):
        self.__wrapped__.__class__ = value

    @property
    def __annotations__(self):
        return self.__wrapped__.__anotations__

    @__annotations__.setter
    def __annotations__(self, value):
        self.__wrapped__.__annotations__ = value

    def __dir__(self):
        return dir(self.__wrapped__)

    def __str__(self):
        return str(self.__wrapped__)

    if PY3:

        def __bytes__(self):
            return bytes(self.__wrapped__)

    def __repr__(self):
        return '<%s at 0x%x for %s at 0x%x>' % (
         type(self).__name__, id(self),
         type(self.__wrapped__).__name__,
         id(self.__wrapped__))

    def __reversed__(self):
        return reversed(self.__wrapped__)

    if PY3:

        def __round__(self):
            return round(self.__wrapped__)

    def __lt__(self, other):
        return self.__wrapped__ < other

    def __le__(self, other):
        return self.__wrapped__ <= other

    def __eq__(self, other):
        return self.__wrapped__ == other

    def __ne__(self, other):
        return self.__wrapped__ != other

    def __gt__(self, other):
        return self.__wrapped__ > other

    def __ge__(self, other):
        return self.__wrapped__ >= other

    def __hash__(self):
        return hash(self.__wrapped__)

    def __nonzero__(self):
        return bool(self.__wrapped__)

    def __bool__(self):
        return bool(self.__wrapped__)

    def __setattr__(self, name, value):
        if name.startswith('_self_'):
            object.__setattr__(self, name, value)
        elif name == '__wrapped__':
            object.__setattr__(self, name, value)
            try:
                object.__delattr__(self, '__qualname__')
            except AttributeError:
                pass

            object.__setattr__(self, name, value)
            try:
                object.__setattr__(self, '__qualname__', value.__qualname__)
            except AttributeError:
                pass

        elif name == '__qualname__':
            setattr(self.__wrapped__, name, value)
            object.__setattr__(self, name, value)
        elif hasattr(type(self), name):
            object.__setattr__(self, name, value)
        else:
            setattr(self.__wrapped__, name, value)

    def __getattr__(self, name):
        if name == '__wrapped__':
            raise ValueError('wrapper has not been initialised')
        return getattr(self.__wrapped__, name)

    def __delattr__(self, name):
        if name.startswith('_self_'):
            object.__delattr__(self, name)
        elif name == '__wrapped__':
            raise TypeError('__wrapped__ must be an object')
        elif name == '__qualname__':
            object.__delattr__(self, name)
            delattr(self.__wrapped__, name)
        elif hasattr(type(self), name):
            object.__delattr__(self, name)
        else:
            delattr(self.__wrapped__, name)

    def __add__(self, other):
        return self.__wrapped__ + other

    def __sub__(self, other):
        return self.__wrapped__ - other

    def __mul__(self, other):
        return self.__wrapped__ * other

    def __div__(self, other):
        return operator.div(self.__wrapped__, other)

    def __truediv__(self, other):
        return operator.truediv(self.__wrapped__, other)

    def __floordiv__(self, other):
        return self.__wrapped__ // other

    def __mod__(self, other):
        return self.__wrapped__ ^ other

    def __divmod__(self, other):
        return divmod(self.__wrapped__, other)

    def __pow__(self, other, *args):
        return pow(self.__wrapped__, other, *args)

    def __lshift__(self, other):
        return self.__wrapped__ << other

    def __rshift__(self, other):
        return self.__wrapped__ >> other

    def __and__(self, other):
        return self.__wrapped__ & other

    def __xor__(self, other):
        return self.__wrapped__ ^ other

    def __or__(self, other):
        return self.__wrapped__ | other

    def __radd__(self, other):
        return other + self.__wrapped__

    def __rsub__(self, other):
        return other - self.__wrapped__

    def __rmul__(self, other):
        return other * self.__wrapped__

    def __rdiv__(self, other):
        return operator.div(other, self.__wrapped__)

    def __rtruediv__(self, other):
        return operator.truediv(other, self.__wrapped__)

    def __rfloordiv__(self, other):
        return other // self.__wrapped__

    def __rmod__(self, other):
        return other % self.__wrapped__

    def __rdivmod__(self, other):
        return divmod(other, self.__wrapped__)

    def __rpow__(self, other, *args):
        return pow(other, self.__wrapped__, *args)

    def __rlshift__(self, other):
        return other << self.__wrapped__

    def __rrshift__(self, other):
        return other >> self.__wrapped__

    def __rand__(self, other):
        return other & self.__wrapped__

    def __rxor__(self, other):
        return other ^ self.__wrapped__

    def __ror__(self, other):
        return other | self.__wrapped__

    def __iadd__(self, other):
        self.__wrapped__ += other
        return self

    def __isub__(self, other):
        self.__wrapped__ -= other
        return self

    def __imul__(self, other):
        self.__wrapped__ *= other
        return self

    def __idiv__(self, other):
        self.__wrapped__ = operator.idiv(self.__wrapped__, other)
        return self

    def __itruediv__(self, other):
        self.__wrapped__ = operator.itruediv(self.__wrapped__, other)
        return self

    def __ifloordiv__(self, other):
        self.__wrapped__ //= other
        return self

    def __imod__(self, other):
        self.__wrapped__ %= other
        return self

    def __ipow__(self, other):
        self.__wrapped__ **= other
        return self

    def __ilshift__(self, other):
        self.__wrapped__ <<= other
        return self

    def __irshift__(self, other):
        self.__wrapped__ >>= other
        return self

    def __iand__(self, other):
        self.__wrapped__ &= other
        return self

    def __ixor__(self, other):
        self.__wrapped__ ^= other
        return self

    def __ior__(self, other):
        self.__wrapped__ |= other
        return self

    def __neg__(self):
        return -self.__wrapped__

    def __pos__(self):
        return +self.__wrapped__

    def __abs__(self):
        return abs(self.__wrapped__)

    def __invert__(self):
        return ~self.__wrapped__

    def __int__(self):
        return int(self.__wrapped__)

    def __long__(self):
        return long(self.__wrapped__)

    def __float__(self):
        return float(self.__wrapped__)

    def __oct__(self):
        return oct(self.__wrapped__)

    def __hex__(self):
        return hex(self.__wrapped__)

    def __index__(self):
        return operator.index(self.__wrapped__)

    def __len__(self):
        return len(self.__wrapped__)

    def __contains__(self, value):
        return value in self.__wrapped__

    def __getitem__(self, key):
        return self.__wrapped__[key]

    def __setitem__(self, key, value):
        self.__wrapped__[key] = value

    def __delitem__(self, key):
        del self.__wrapped__[key]

    def __getslice__(self, i, j):
        return self.__wrapped__[i:j]

    def __setslice__(self, i, j, value):
        self.__wrapped__[i:j] = value

    def __delslice__(self, i, j):
        del self.__wrapped__[i:j]

    def __enter__(self):
        return self.__wrapped__.__enter__()

    def __exit__(self, *args, **kwargs):
        return self.__wrapped__.__exit__(*args, **kwargs)

    def __iter__(self):
        return iter(self.__wrapped__)


class CallableObjectProxy(ObjectProxy):

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)


class _FunctionWrapperBase(ObjectProxy):
    __slots__ = ('_self_instance', '_self_wrapper', '_self_enabled', '_self_binding',
                 '_self_parent')

    def __init__(self, wrapped, instance, wrapper, enabled=None, binding='function', parent=None):
        super(_FunctionWrapperBase, self).__init__(wrapped)
        object.__setattr__(self, '_self_instance', instance)
        object.__setattr__(self, '_self_wrapper', wrapper)
        object.__setattr__(self, '_self_enabled', enabled)
        object.__setattr__(self, '_self_binding', binding)
        object.__setattr__(self, '_self_parent', parent)

    def __get__(self, instance, owner):
        if self._self_parent is None:
            if not inspect.isclass(self.__wrapped__):
                descriptor = self.__wrapped__.__get__(instance, owner)
                return self.__bound_function_wrapper__(descriptor, instance, self._self_wrapper, self._self_enabled, self._self_binding, self)
            return self
        if self._self_instance is None and self._self_binding == 'function':
            descriptor = self._self_parent.__wrapped__.__get__(instance, owner)
            return self._self_parent.__bound_function_wrapper__(descriptor, instance, self._self_wrapper, self._self_enabled, self._self_binding, self._self_parent)
        else:
            return self

    def __call__(self, *args, **kwargs):
        if self._self_enabled is not None:
            if callable(self._self_enabled):
                if not self._self_enabled():
                    return self.__wrapped__(*args, **kwargs)
            elif not self._self_enabled:
                return self.__wrapped__(*args, **kwargs)
        if self._self_binding == 'function':
            if self._self_instance is None:
                instance = getattr(self.__wrapped__, '__self__', None)
                if instance is not None:
                    return self._self_wrapper(self.__wrapped__, instance, args, kwargs)
        return self._self_wrapper(self.__wrapped__, self._self_instance, args, kwargs)


class BoundFunctionWrapper(_FunctionWrapperBase):

    def __call__(self, *args, **kwargs):
        if self._self_enabled is not None:
            if callable(self._self_enabled):
                if not self._self_enabled():
                    return self.__wrapped__(*args, **kwargs)
            elif not self._self_enabled:
                return self.__wrapped__(*args, **kwargs)
        if self._self_binding == 'function':
            if self._self_instance is None:
                if not args:
                    raise TypeError('missing 1 required positional argument')
                instance, args = args[0], args[1:]
                wrapped = functools.partial(self.__wrapped__, instance)
                return self._self_wrapper(wrapped, instance, args, kwargs)
            return self._self_wrapper(self.__wrapped__, self._self_instance, args, kwargs)
        else:
            instance = getattr(self.__wrapped__, '__self__', None)
            return self._self_wrapper(self.__wrapped__, instance, args, kwargs)
            return


class FunctionWrapper(_FunctionWrapperBase):
    __bound_function_wrapper__ = BoundFunctionWrapper

    def __init__(self, wrapped, wrapper, enabled=None):
        if isinstance(wrapped, classmethod):
            binding = 'classmethod'
        elif isinstance(wrapped, staticmethod):
            binding = 'staticmethod'
        elif hasattr(wrapped, '__self__'):
            if inspect.isclass(wrapped.__self__):
                binding = 'classmethod'
            else:
                binding = 'function'
        else:
            binding = 'function'
        super(FunctionWrapper, self).__init__(wrapped, None, wrapper, enabled, binding)
        return


try:
    from ._wrappers import ObjectProxy, CallableObjectProxy, FunctionWrapper, BoundFunctionWrapper, _FunctionWrapperBase
except ImportError:
    pass

def resolve_path(module, name):
    if isinstance(module, string_types):
        __import__(module)
        module = sys.modules[module]
    parent = module
    path = name.split('.')
    attribute = path[0]
    original = getattr(parent, attribute)
    for attribute in path[1:]:
        parent = original
        if inspect.isclass(original):
            for cls in inspect.getmro(original):
                if attribute in vars(original):
                    original = vars(original)[attribute]
                    break
            else:
                original = getattr(original, attribute)

        else:
            original = getattr(original, attribute)

    return (
     parent, attribute, original)


def apply_patch(parent, attribute, replacement):
    setattr(parent, attribute, replacement)


def wrap_object(module, name, factory, args=(), kwargs={}):
    parent, attribute, original = resolve_path(module, name)
    wrapper = factory(original, *args, **kwargs)
    apply_patch(parent, attribute, wrapper)
    return wrapper


class AttributeWrapper(object):

    def __init__(self, attribute, factory, args, kwargs):
        self.attribute = attribute
        self.factory = factory
        self.args = args
        self.kwargs = kwargs

    def __get__(self, instance, owner):
        value = instance.__dict__[self.attribute]
        return self.factory(value, *self.args, **self.kwargs)

    def __set__(self, instance, value):
        instance.__dict__[self.attribute] = value

    def __delete__(self, instance):
        del instance.__dict__[self.attribute]


def wrap_object_attribute(module, name, factory, args=(), kwargs={}):
    path, attribute = name.rsplit('.', 1)
    parent = resolve_path(module, path)[2]
    wrapper = AttributeWrapper(attribute, factory, args, kwargs)
    apply_patch(parent, attribute, wrapper)
    return wrapper


def function_wrapper(wrapper):

    def _wrapper(wrapped, instance, args, kwargs):
        target_wrapped = args[0]
        if instance is None:
            target_wrapper = wrapper
        elif inspect.isclass(instance):
            target_wrapper = wrapper.__get__(None, instance)
        else:
            target_wrapper = wrapper.__get__(instance, type(instance))
        return FunctionWrapper(target_wrapped, target_wrapper)

    return FunctionWrapper(wrapper, _wrapper)


def wrap_function_wrapper(module, name, wrapper):
    return wrap_object(module, name, FunctionWrapper, (wrapper,))


def patch_function_wrapper(module, name):

    def _wrapper(wrapper):
        return wrap_object(module, name, FunctionWrapper, (wrapper,))

    return _wrapper


def transient_function_wrapper(module, name):

    def _decorator(wrapper):

        def _wrapper(wrapped, instance, args, kwargs):
            target_wrapped = args[0]
            if instance is None:
                target_wrapper = wrapper
            elif inspect.isclass(instance):
                target_wrapper = wrapper.__get__(None, instance)
            else:
                target_wrapper = wrapper.__get__(instance, type(instance))

            def _execute(wrapped, instance, args, kwargs):
                parent, attribute, original = resolve_path(module, name)
                replacement = FunctionWrapper(original, target_wrapper)
                setattr(parent, attribute, replacement)
                try:
                    return wrapped(*args, **kwargs)
                finally:
                    setattr(parent, attribute, original)

            return FunctionWrapper(target_wrapped, _execute)

        return FunctionWrapper(wrapper, _wrapper)

    return _decorator


def _weak_function_proxy_callback(ref, proxy, callback):
    if proxy._self_expired:
        return
    else:
        proxy._self_expired = True
        if callback is not None:
            callback(proxy)
        return


class WeakFunctionProxy(ObjectProxy):
    __slots__ = ('_self_expired', '_self_instance')

    def __init__(self, wrapped, callback=None):
        _callback = callback and functools.partial(_weak_function_proxy_callback, proxy=self, callback=callback)
        self._self_expired = False
        try:
            self._self_instance = weakref.ref(wrapped.__self__, _callback)
            super(WeakFunctionProxy, self).__init__(weakref.proxy(wrapped.__func__, _callback))
        except AttributeError:
            self._self_instance = None
            super(WeakFunctionProxy, self).__init__(weakref.proxy(wrapped, _callback))

        return

    def __call__(self, *args, **kwargs):
        instance = self._self_instance and self._self_instance()
        function = self.__wrapped__ and self.__wrapped__
        if instance is None:
            return self.__wrapped__(*args, **kwargs)
        else:
            return function.__get__(instance, type(instance))(*args, **kwargs)