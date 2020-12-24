# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kohei/anaconda3/lib/python3.5/site-packages/extheano/jit.py
# Compiled at: 2016-04-27 03:31:33
# Size of source mod 2**32: 7561 bytes
"""Classes related to the auto-compilation"""
import copy, inspect, functools, numpy as np, theano, theano.tensor as T
from .nodebuffer import UpdateCollector

class JITCompiler(object):
    __doc__ = 'Decorator for your theano-function\n\n    You can call your theano-function without any explicit instructions to compile it. It takes a\n    while for the first time. Note that the type of arguments will be fixed on\n    the first call.\n\n    Usage:\n        >> f = JITCompiler( lambda x: T.sqrt((x ** 2).mean()) )\n\n        >> f([1., 2.]) # <-- implicit compilation here\n            array(1.5811388300841898)\n\n        >> f([3., 4., 5.]) # <-- pre-compiled function is used\n            array(4.08248290463863)\n    '
    parse = None

    def __init__(self, func, owner=None):
        """Initialize the members given the decorated function"""
        functools.update_wrapper(self, func)
        self.raw_func = func
        self.owner = owner
        self.compiled_func = None

    def __call__(self, *args):
        """Call the compiled function after its compilation """
        if self.compiled_func is None:
            self.compiled_func = Compiler().compile_with_value(self.raw_func, args, self.owner)
        return self.compiled_func(*args)

    def __get__(self, obj, objtype=None):
        """Support decorating instance methods"""
        if obj is not None:
            name = self.raw_func.__name__
            wrapped_func = JITCompiler(self.raw_func, owner=obj)
            setattr(obj, name, wrapped_func)
            return wrapped_func
        if self.owner is None:
            self.owner = objtype
        return self

    def recompile(self):
        """Lazy re-compilation"""
        self.compiled_func = None


class ParsingJITCompiler(JITCompiler):
    __doc__ = 'JITCompiler with a new feature: argument parsing\n\n    Now you can pass keyword arguments to the function\n    '

    def __init__(self, func, owner=None):
        """Initialize the members given the decorated function"""
        functools.update_wrapper(self, func)
        self.rawinfo = FuncInfo(func)
        self.owner = owner
        self.compiled_func = None
        if owner is not None:
            self.rawinfo.remove_first_key()

    def __call__(self, *args, **kwargs):
        """Call the compiled function after its compilation """
        if self.rawinfo.has_default_arg():
            args = self.rawinfo.parse_args_kwargs(*args, **kwargs)
        if self.compiled_func is None:
            self.compiled_func = Compiler().compile_with_value(self.rawinfo.func, args, self.owner)
        return self.compiled_func(*args)

    def __get__(self, obj, objtype=None):
        """Support decorating instance methods"""
        if obj is not None:
            name = self.rawinfo.func.__name__
            wrapped_func = ParsingJITCompiler(self.rawinfo.func, owner=obj)
            setattr(obj, name, wrapped_func)
            return wrapped_func
        if self.owner is None:
            self.owner = objtype
            self.rawinfo.remove_first_key()
        return self


class FuncInfo(object):
    __doc__ = 'Container of a function and its information'

    def __init__(self, func):
        self.func = func
        self.arginfo = self._get_keys_defdict()

    def has_default_arg(self):
        """If there are any arguments with default value or not"""
        return self.arginfo[1] is not None

    def remove_first_key(self):
        """remove the key of the first argument from arginfo"""
        self.arginfo = (
         self.arginfo[0][1:], self.arginfo[1])

    def parse_args_kwargs(self, *args, **kwargs):
        """Parse the arguments with keywords."""
        keys, defdict = self.arginfo
        assigned = keys[:len(args)]
        not_assigned = keys[len(args):]
        for key in kwargs:
            assert key not in assigned
            if not key in keys:
                raise AssertionError

        knowns = dict(defdict, **kwargs)
        parsed_args = args + tuple([knowns[key] for key in not_assigned])
        return parsed_args

    def _get_keys_defdict(self):
        """Get the keys and the default dictionary of the given function's
        arguments
        """
        argspec = inspect.getargspec(self.func)
        keys, defvals = argspec.args, argspec.defaults
        if defvals is None:
            return (keys, None)
        else:
            defvals = list(defvals)
            keys.reverse()
            defvals.reverse()
            defdict = dict(zip(keys, defvals))
            keys.reverse()
            return (keys, defdict)


class Compiler(object):
    __doc__ = 'Compile the theano-function/method just with its arguments and owner\n    '
    default_options = {'on_unused_input': 'warn'}

    def compile_with_value(self, func, args=None, owner=None):
        """Compile the function with array-like objects"""
        if args is None:
            args = []
        theano_args = [self.cast2theano_var(a, 'extheano.jit.Compiler-arg-%d' % i) for a, i in zip(args, range(len(args)))]
        return self.compile_with_symbol(func, theano_args, owner)

    def compile_with_symbol(self, func, theano_args=None, owner=None):
        """Compile the function with theano symbols"""
        if theano_args is None:
            theano_args = []
        upc = UpdateCollector()
        theano_ret = func(*theano_args) if owner is None else func(owner, *theano_args)
        out = copy.copy(self.default_options)
        out['outputs'] = theano_ret
        out['updates'] = upc.extract_updates()
        return theano.function(theano_args, **out)

    def cast2theano_var(self, array_like, name=None):
        """Cast `numpy.ndarray` into `theano.tensor` keeping `dtype` and `ndim`
        compatible
        """
        array = np.asarray(array_like)
        args = (name, array.dtype)
        ndim = array.ndim
        if ndim == 0:
            return T.scalar(*args)
        if ndim == 1:
            return T.vector(*args)
        if ndim == 2:
            return T.matrix(*args)
        if ndim == 3:
            return T.tensor3(*args)
        if ndim == 4:
            return T.tensor4(*args)
        raise ValueError('extheano.jit.Compiler: Unsupported type or shape')


JITCompiler.parse = ParsingJITCompiler