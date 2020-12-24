# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/decorator.py
# Compiled at: 2018-07-31 10:42:31
"""
修改类的名字，或者过滤掉不想暴漏的方法

@export("service")
class Service(object):
    @provide(filtered=True)
    def filtered_method(self):
        pass

    def exported_method(self):
        pass
"""
__all__ = [
 'export', 'get_export', 'provide', 'get_provide',
 'run_in_subprocess', 'get_run_in_subprocess']
__authors__ = ['Tim Chow']
import inspect, warnings

def export(name):
    if not isinstance(name, str):
        raise TypeError('expect str, not %s' % type(name).__name__)

    def _inner(cls):
        if not inspect.isclass(cls):
            warnings.warn('expect class, not %s' % type(cls).__name__, RuntimeWarning)
            return cls
        setattr(cls, '__rpc_export__', {'name': name})
        return cls

    return _inner


def get_export(cls):
    if not inspect.isclass(cls):
        warnings.warn('expect class, not %s' % type(cls).__name__, RuntimeWarning)
        return
    else:
        export = getattr(cls, '__rpc_export__', None)
        if export is None or not isinstance(export, dict):
            return
        return export


def provide(name=None, filtered=False):

    def _inner(f):
        if not inspect.isfunction(f) and not inspect.ismethod(f):
            warnings.warn('expect method or function, not %s' % type(f).__name__, RuntimeWarning)
            return f
        else:
            if name is None:
                name = f.__name__
            setattr(f, '__rpc_provide__', {'name': name, 'filtered': filtered})
            return f

    return _inner


def get_provide(f):
    if not inspect.isfunction(f) and not inspect.ismethod(f):
        warnings.warn('expect method or function, not %s' % type(f).__name__, RuntimeWarning)
        return
    else:
        provide = getattr(f, '__rpc_provide__', None)
        if provide is None or not isinstance(provide, dict):
            return
        return provide


def run_in_subprocess(f):
    if not inspect.isfunction(f) and not inspect.ismethod(f):
        warnings.warn('expect method or function, not %s' % type(f).__name__, RuntimeWarning)
        return f
    setattr(f, '__run_in_subprocess__', True)
    return f


def get_run_in_subprocess(f):
    if not inspect.isfunction(f) and not inspect.ismethod(f):
        warnings.warn('expect method or function, not %s' % type(f).__name__, RuntimeWarning)
        return
    else:
        run_in_subprocess = getattr(f, '__run_in_subprocess__', None)
        if not isinstance(run_in_subprocess, bool):
            return
        return run_in_subprocess