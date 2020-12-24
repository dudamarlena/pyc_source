# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/packages/wrapt/decorators.py
# Compiled at: 2016-06-30 06:13:10
"""This module implements decorators for implementing other decorators
as well as some commonly used decorators.

"""
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    string_types = (
     str,)
    import builtins
    exec_ = getattr(builtins, 'exec')
    del builtins
else:
    string_types = (
     basestring,)

    def exec_(_code_, _globs_=None, _locs_=None):
        """Execute code in a namespace."""
        if _globs_ is None:
            frame = sys._getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
        exec 'exec _code_ in _globs_, _locs_'
        return


from functools import partial
from inspect import getargspec, ismethod, isclass, formatargspec
from collections import namedtuple
from threading import Lock, RLock
try:
    from inspect import signature
except ImportError:
    pass

from .wrappers import FunctionWrapper, BoundFunctionWrapper, ObjectProxy, CallableObjectProxy

class _AdapterFunctionCode(CallableObjectProxy):

    def __init__(self, wrapped_code, adapter_code):
        super(_AdapterFunctionCode, self).__init__(wrapped_code)
        self._self_adapter_code = adapter_code

    @property
    def co_argcount(self):
        return self._self_adapter_code.co_argcount

    @property
    def co_code(self):
        return self._self_adapter_code.co_code

    @property
    def co_flags(self):
        return self._self_adapter_code.co_flags

    @property
    def co_kwonlyargcount(self):
        return self._self_adapter_code.co_kwonlyargcount

    @property
    def co_varnames(self):
        return self._self_adapter_code.co_varnames


class _AdapterFunctionSurrogate(CallableObjectProxy):

    def __init__(self, wrapped, adapter):
        super(_AdapterFunctionSurrogate, self).__init__(wrapped)
        self._self_adapter = adapter

    @property
    def __code__(self):
        return _AdapterFunctionCode(self.__wrapped__.__code__, self._self_adapter.__code__)

    @property
    def __defaults__(self):
        return self._self_adapter.__defaults__

    @property
    def __kwdefaults__(self):
        return self._self_adapter.__kwdefaults__

    @property
    def __signature__(self):
        if 'signature' not in globals():
            return self._self_adapter.__signature__
        else:
            return signature(self._self_adapter)

    if PY2:
        func_code = __code__
        func_defaults = __defaults__


class _BoundAdapterWrapper(BoundFunctionWrapper):

    @property
    def __func__(self):
        return _AdapterFunctionSurrogate(self.__wrapped__.__func__, self._self_parent._self_adapter)

    if PY2:
        im_func = __func__


class AdapterWrapper(FunctionWrapper):
    __bound_function_wrapper__ = _BoundAdapterWrapper

    def __init__(self, *args, **kwargs):
        adapter = kwargs.pop('adapter')
        super(AdapterWrapper, self).__init__(*args, **kwargs)
        self._self_surrogate = _AdapterFunctionSurrogate(self.__wrapped__, adapter)
        self._self_adapter = adapter

    @property
    def __code__(self):
        return self._self_surrogate.__code__

    @property
    def __defaults__(self):
        return self._self_surrogate.__defaults__

    @property
    def __kwdefaults__(self):
        return self._self_surrogate.__kwdefaults__

    if PY2:
        func_code = __code__
        func_defaults = __defaults__

    @property
    def __signature__(self):
        return self._self_surrogate.__signature__


class AdapterFactory(object):

    def __call__(self, wrapped):
        raise NotImplementedError()


class DelegatedAdapterFactory(AdapterFactory):

    def __init__(self, factory):
        super(DelegatedAdapterFactory, self).__init__()
        self.factory = factory

    def __call__(self, wrapped):
        return self.factory(wrapped)


adapter_factory = DelegatedAdapterFactory

def decorator(wrapper=None, enabled=None, adapter=None):
    if wrapper is not None:

        def _build(wrapped, wrapper, enabled=None, adapter=None):
            if adapter:
                if isinstance(adapter, AdapterFactory):
                    adapter = adapter(wrapped)
                if not callable(adapter):
                    ns = {}
                    if not isinstance(adapter, string_types):
                        adapter = formatargspec(*adapter)
                    exec_(('def adapter{0}: pass').format(adapter), ns, ns)
                    adapter = ns['adapter']
                return AdapterWrapper(wrapped=wrapped, wrapper=wrapper, enabled=enabled, adapter=adapter)
            return FunctionWrapper(wrapped=wrapped, wrapper=wrapper, enabled=enabled)

        def _wrapper(wrapped, instance, args, kwargs):
            if instance is None and isclass(wrapped) and not args:

                def _capture(target_wrapped):
                    _enabled = enabled
                    if type(_enabled) is bool:
                        if not _enabled:
                            return target_wrapped
                        _enabled = None
                    target_wrapper = wrapped(**kwargs)
                    return _build(target_wrapped, target_wrapper, _enabled, adapter)

                return _capture
            else:
                target_wrapped = args[0]
                _enabled = enabled
                if type(_enabled) is bool:
                    if not _enabled:
                        return target_wrapped
                    _enabled = None
                if instance is None:
                    if isclass(wrapped):
                        target_wrapper = wrapped()
                    else:
                        target_wrapper = wrapper
                elif isclass(instance):
                    target_wrapper = wrapper.__get__(None, instance)
                else:
                    target_wrapper = wrapper.__get__(instance, type(instance))
                return _build(target_wrapped, target_wrapper, _enabled, adapter)

        return _build(wrapper, _wrapper)
    else:
        return partial(decorator, enabled=enabled, adapter=adapter)
        return


def synchronized(wrapped):
    if hasattr(wrapped, 'acquire') and hasattr(wrapped, 'release'):
        lock = wrapped

        @decorator
        def _synchronized(wrapped, instance, args, kwargs):
            with lock:
                return wrapped(*args, **kwargs)

        class _PartialDecorator(CallableObjectProxy):

            def __enter__(self):
                lock.acquire()
                return lock

            def __exit__(self, *args):
                lock.release()

        return _PartialDecorator(wrapped=_synchronized)

    def _synchronized_lock(context):
        lock = vars(context).get('_synchronized_lock', None)
        if lock is None:
            meta_lock = vars(synchronized).setdefault('_synchronized_meta_lock', Lock())
            with meta_lock:
                lock = vars(context).get('_synchronized_lock', None)
                if lock is None:
                    lock = RLock()
                    setattr(context, '_synchronized_lock', lock)
        return lock

    def _synchronized_wrapper(wrapped, instance, args, kwargs):
        with _synchronized_lock(instance or wrapped):
            return wrapped(*args, **kwargs)

    class _FinalDecorator(FunctionWrapper):

        def __enter__(self):
            self._self_lock = _synchronized_lock(self.__wrapped__)
            self._self_lock.acquire()
            return self._self_lock

        def __exit__(self, *args):
            self._self_lock.release()

    return _FinalDecorator(wrapped=wrapped, wrapper=_synchronized_wrapper)