# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bramin/curry.py
# Compiled at: 2019-12-24 06:58:53
# Size of source mod 2**32: 4097 bytes
from typing import Callable
from functools import update_wrapper
from inspect import _empty, Signature, Parameter
from collections import OrderedDict as od
from copy import copy
from ._utils import type_error, is_partial_like, signature

def init_bindings(sig: Signature) -> od:
    bids = od([])
    for n, p in sig.parameters.items():
        if p.kind is Parameter.VAR_POSITIONAL:
            bids[n] = tuple()
        else:
            if p.kind is Parameter.VAR_KEYWORD:
                bids[n] = dict()
            else:
                bids[n] = p.default

    return bids


class curry(object):
    __doc__ = "\n    [NOTE] Now, built-in func only support:\n        map, filter, reduce.\n\n    Basically it's same to toolz.curry,\n    but the argument binding behavior like this is allowed:\n\n    >>> def add(x, y):\n    ...     return x + y\n    >>> curry(add)(x=1)(1)\n    2\n    "

    def __init__(self, func: Callable, *args, **kwargs):
        if not callable(func):
            raise type_error(f"{type(self)}.__init__", callable, type(func))
        else:
            is_p = is_partial_like(func)
            ori_func = func.func if is_p else func
            self.func = ori_func
            sig = signature(ori_func)
            self._params = od(sig.parameters)
            self._bindings = init_bindings(sig)
            if is_p:
                if hasattr(func, '_bindings'):
                    self._bindings.update(func._bindings)
            if is_p:
                self._bind(func.args, func.keywords)
        (self._bind)(*args, **kwargs)
        update_wrapper(self, ori_func)

    def _var_kw_param(self):
        n, p = next(reversed(self._params.items()))
        if p.kind is Parameter.VAR_KEYWORD:
            return n
        else:
            return

    def _bind(self, *args, **kwargs):
        bids = self._bindings
        for val in args:
            for name, p in self._params.items():
                if p.default is not _empty or bids[name] is _empty:
                    bids[name] = val
                    break
                elif p.kind is Parameter.VAR_POSITIONAL:
                    bids[name] = bids[name] + (val,)
                    break

        for name, val in kwargs.items():
            if name in bids:
                bids[name] = val
            else:
                p_varkw = self._var_kw_param()
                if not p_varkw:
                    raise TypeError(f"{self} got an unexpected keyword argument {repr(name)}")
                bids[p_varkw] = copy(bids[p_varkw])
                bids[p_varkw][name] = val

    @property
    def _all_bound(self) -> bool:
        return all([b is not _empty for b in self._bindings.values()])

    @property
    def args(self) -> tuple:
        args_ = []
        for name, p in self._params.items():
            if p.default is not _empty:
                break
            else:
                if self._bindings[name] is _empty:
                    break
                if p.kind is Parameter.VAR_KEYWORD:
                    break
            if p.kind is Parameter.VAR_POSITIONAL:
                args_.extend(self._bindings[name])
            else:
                args_.append(self._bindings[name])

        return tuple(args_)

    @property
    def keywords(self) -> dict:
        kwargs = {}
        for name, p in self._params.items():
            if p.default is _empty:
                if p.kind is not Parameter.VAR_KEYWORD:
                    continue
            if p.kind is Parameter.VAR_KEYWORD:
                kwargs.update(self._bindings[name])
            else:
                kwargs[name] = self._bindings[name]

        return kwargs

    def __call__(self, *args, **kwargs):
        new = (type(self))(self, *args, **kwargs)
        if new._all_bound:
            return (new.func)(*new.args, **new.keywords)
        else:
            return new

    def __repr__(self):
        bound = {n:v for n, v in self._bindings.items() if v is not _empty if v is not _empty}
        b = ', '.join([f"{n}={repr(v)}" for n, v in bound.items()])
        s = f"<curry {self.__name__}{' ' + b if b else ''}>"
        return s