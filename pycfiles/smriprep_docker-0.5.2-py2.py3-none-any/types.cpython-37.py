# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/src/smriprep/wrapper/build/lib/python3.7/types.py
# Compiled at: 2019-09-12 11:41:56
# Size of source mod 2**32: 9897 bytes
"""
Define names for built-in types that aren't directly accessible as a builtin.
"""
import sys

def _f():
    pass


FunctionType = type(_f)
LambdaType = type(lambda : None)
CodeType = type(_f.__code__)
MappingProxyType = type(type.__dict__)
SimpleNamespace = type(sys.implementation)

def _g():
    yield 1


GeneratorType = type(_g())

async def _c():
    pass


_c = _c()
CoroutineType = type(_c)
_c.close()

async def _ag():
    yield


_ag = _ag()
AsyncGeneratorType = type(_ag)

class _C:

    def _m(self):
        pass


MethodType = type(_C()._m)
BuiltinFunctionType = type(len)
BuiltinMethodType = type([].append)
WrapperDescriptorType = type(object.__init__)
MethodWrapperType = type(object().__str__)
MethodDescriptorType = type(str.join)
ClassMethodDescriptorType = type(dict.__dict__['fromkeys'])
ModuleType = type(sys)
try:
    raise TypeError
except TypeError:
    tb = sys.exc_info()[2]
    TracebackType = type(tb)
    FrameType = type(tb.tb_frame)
    tb = None
    del tb

GetSetDescriptorType = type(FunctionType.__code__)
MemberDescriptorType = type(FunctionType.__globals__)
del sys
del _f
del _g
del _C
del _c
del _ag

def new_class(name, bases=(), kwds=None, exec_body=None):
    """Create a class object dynamically using the appropriate metaclass."""
    resolved_bases = resolve_bases(bases)
    meta, ns, kwds = prepare_class(name, resolved_bases, kwds)
    if exec_body is not None:
        exec_body(ns)
    if resolved_bases is not bases:
        ns['__orig_bases__'] = bases
    return meta(name, resolved_bases, ns, **kwds)


def resolve_bases(bases):
    """Resolve MRO entries dynamically as specified by PEP 560."""
    new_bases = list(bases)
    updated = False
    shift = 0
    for i, base in enumerate(bases):
        if isinstance(base, type):
            continue
        if not hasattr(base, '__mro_entries__'):
            continue
        new_base = base.__mro_entries__(bases)
        updated = True
        if not isinstance(new_base, tuple):
            raise TypeError('__mro_entries__ must return a tuple')
        else:
            new_bases[i + shift:i + shift + 1] = new_base
            shift += len(new_base) - 1

    if not updated:
        return bases
    return tuple(new_bases)


def prepare_class(name, bases=(), kwds=None):
    """Call the __prepare__ method of the appropriate metaclass.

    Returns (metaclass, namespace, kwds) as a 3-tuple

    *metaclass* is the appropriate metaclass
    *namespace* is the prepared class namespace
    *kwds* is an updated copy of the passed in kwds argument with any
    'metaclass' entry removed. If no kwds argument is passed in, this will
    be an empty dict.
    """
    if kwds is None:
        kwds = {}
    else:
        kwds = dict(kwds)
    if 'metaclass' in kwds:
        meta = kwds.pop('metaclass')
    else:
        if bases:
            meta = type(bases[0])
        else:
            meta = type
    if isinstance(meta, type):
        meta = _calculate_meta(meta, bases)
    elif hasattr(meta, '__prepare__'):
        ns = (meta.__prepare__)(name, bases, **kwds)
    else:
        ns = {}
    return (
     meta, ns, kwds)


def _calculate_meta(meta, bases):
    """Calculate the most derived metaclass."""
    winner = meta
    for base in bases:
        base_meta = type(base)
        if issubclass(winner, base_meta):
            continue
        if issubclass(base_meta, winner):
            winner = base_meta
            continue
        raise TypeError('metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases')

    return winner


class DynamicClassAttribute:
    __doc__ = "Route attribute access on a class to __getattr__.\n\n    This is a descriptor, used to define attributes that act differently when\n    accessed through an instance and through a class.  Instance access remains\n    normal, but access to an attribute through a class will be routed to the\n    class's __getattr__ method; this is done by raising AttributeError.\n\n    This allows one to have properties active on an instance, and have virtual\n    attributes on the class with the same name (see Enum for an example).\n\n    "

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or fget.__doc__
        self.overwrite_doc = doc is None
        self.__isabstractmethod__ = bool(getattr(fget, '__isabstractmethod__', False))

    def __get__(self, instance, ownerclass=None):
        if instance is None:
            if self.__isabstractmethod__:
                return self
            raise AttributeError()
        else:
            if self.fget is None:
                raise AttributeError('unreadable attribute')
        return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(instance)

    def getter(self, fget):
        fdoc = fget.__doc__ if self.overwrite_doc else None
        result = type(self)(fget, self.fset, self.fdel, fdoc or self.__doc__)
        result.overwrite_doc = self.overwrite_doc
        return result

    def setter(self, fset):
        result = type(self)(self.fget, fset, self.fdel, self.__doc__)
        result.overwrite_doc = self.overwrite_doc
        return result

    def deleter(self, fdel):
        result = type(self)(self.fget, self.fset, fdel, self.__doc__)
        result.overwrite_doc = self.overwrite_doc
        return result


class _GeneratorWrapper:

    def __init__(self, gen):
        self._GeneratorWrapper__wrapped = gen
        self._GeneratorWrapper__isgen = gen.__class__ is GeneratorType
        self.__name__ = getattr(gen, '__name__', None)
        self.__qualname__ = getattr(gen, '__qualname__', None)

    def send(self, val):
        return self._GeneratorWrapper__wrapped.send(val)

    def throw(self, tp, *rest):
        return (self._GeneratorWrapper__wrapped.throw)(tp, *rest)

    def close(self):
        return self._GeneratorWrapper__wrapped.close()

    @property
    def gi_code(self):
        return self._GeneratorWrapper__wrapped.gi_code

    @property
    def gi_frame(self):
        return self._GeneratorWrapper__wrapped.gi_frame

    @property
    def gi_running(self):
        return self._GeneratorWrapper__wrapped.gi_running

    @property
    def gi_yieldfrom(self):
        return self._GeneratorWrapper__wrapped.gi_yieldfrom

    cr_code = gi_code
    cr_frame = gi_frame
    cr_running = gi_running
    cr_await = gi_yieldfrom

    def __next__(self):
        return next(self._GeneratorWrapper__wrapped)

    def __iter__(self):
        if self._GeneratorWrapper__isgen:
            return self._GeneratorWrapper__wrapped
        return self

    __await__ = __iter__


def coroutine(func):
    """Convert regular generator function to a coroutine."""
    if not callable(func):
        raise TypeError('types.coroutine() expects a callable')
    elif func.__class__ is FunctionType:
        if getattr(func, '__code__', None).__class__ is CodeType:
            co_flags = func.__code__.co_flags
            if co_flags & 384:
                return func
            if co_flags & 32:
                co = func.__code__
                func.__code__ = CodeType(co.co_argcount, co.co_kwonlyargcount, co.co_nlocals, co.co_stacksize, co.co_flags | 256, co.co_code, co.co_consts, co.co_names, co.co_varnames, co.co_filename, co.co_name, co.co_firstlineno, co.co_lnotab, co.co_freevars, co.co_cellvars)
                return func
    import functools, _collections_abc

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        coro = func(*args, **kwargs)
        if (coro.__class__ is CoroutineType or coro.__class__) is GeneratorType:
            if coro.gi_code.co_flags & 256:
                return coro
        if isinstance(coro, _collections_abc.Generator):
            if not isinstance(coro, _collections_abc.Coroutine):
                return _GeneratorWrapper(coro)
        return coro

    return wrapped


__all__ = [n for n in globals() if n[:1] != '_']