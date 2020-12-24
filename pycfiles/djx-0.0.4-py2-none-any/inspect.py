# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/inspect.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import absolute_import
import inspect
from django.utils import six

def getargspec(func):
    if six.PY2:
        return inspect.getargspec(func)
    else:
        sig = inspect.signature(func)
        args = [ p.name for p in sig.parameters.values() if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
               ]
        varargs = [ p.name for p in sig.parameters.values() if p.kind == inspect.Parameter.VAR_POSITIONAL
                  ]
        varargs = varargs[0] if varargs else None
        varkw = [ p.name for p in sig.parameters.values() if p.kind == inspect.Parameter.VAR_KEYWORD
                ]
        varkw = varkw[0] if varkw else None
        defaults = [ p.default for p in sig.parameters.values() if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD and p.default is not p.empty
                   ] or None
        return (args, varargs, varkw, defaults)


def get_func_args(func):
    if six.PY2:
        argspec = inspect.getargspec(func)
        return argspec.args[1:]
    sig = inspect.signature(func)
    return [ arg_name for arg_name, param in sig.parameters.items() if param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
           ]


def get_func_full_args(func):
    """
    Return a list of (argument name, default value) tuples. If the argument
    does not have a default value, omit it in the tuple. Arguments such as
    *args and **kwargs are also included.
    """
    if six.PY2:
        argspec = inspect.getargspec(func)
        args = argspec.args[1:]
        defaults = argspec.defaults or []
        no_default = args[:len(args) - len(defaults)]
        with_default = args[len(args) - len(defaults):]
        args = [ (arg,) for arg in no_default ] + zip(with_default, defaults)
        varargs = [('*' + argspec.varargs,)] if argspec.varargs else []
        kwargs = [('**' + argspec.keywords,)] if argspec.keywords else []
        return args + varargs + kwargs
    sig = inspect.signature(func)
    args = []
    for arg_name, param in sig.parameters.items():
        name = arg_name
        if name == 'self':
            continue
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            name = '*' + name
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            name = '**' + name
        if param.default != inspect.Parameter.empty:
            args.append((name, param.default))
        else:
            args.append((name,))

    return args


def func_accepts_kwargs(func):
    if six.PY2:
        try:
            argspec = inspect.getargspec(func)
        except TypeError:
            try:
                argspec = inspect.getargspec(func.__call__)
            except (TypeError, AttributeError):
                argspec = None

        return not argspec or argspec[2] is not None
    else:
        return any(p for p in inspect.signature(func).parameters.values() if p.kind == p.VAR_KEYWORD)


def func_accepts_var_args(func):
    """
    Return True if function 'func' accepts positional arguments *args.
    """
    if six.PY2:
        return inspect.getargspec(func)[1] is not None
    else:
        return any(p for p in inspect.signature(func).parameters.values() if p.kind == p.VAR_POSITIONAL)


def func_has_no_args(func):
    args = inspect.getargspec(func)[0] if six.PY2 else [ p for p in inspect.signature(func).parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD
                                                       ]
    return len(args) == 1


def func_supports_parameter(func, parameter):
    if six.PY3:
        return parameter in inspect.signature(func).parameters
    else:
        args, varargs, varkw, defaults = inspect.getargspec(func)
        return parameter in args