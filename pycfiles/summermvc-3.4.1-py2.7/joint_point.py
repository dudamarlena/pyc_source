# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/joint_point.py
# Compiled at: 2018-05-30 05:31:20
__authors__ = [
 'Tim Chow']
__all__ = ['JointPoint']
import inspect

class JointPoint(object):
    """连接点对象"""

    def __init__(self, method=None, args=None, kwargs=None):
        self._method = method
        self._args = args
        self._kwargs = kwargs

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        self._method = method

    def get_signature(self):
        if self.method is None:
            return
        else:
            argspec = inspect.getargspec(self.method)
            return (argspec.args, argspec.varargs, argspec.keywords)

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        self._args = args

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, kwargs):
        self._kwargs = kwargs

    def get_arguments(self):
        if self.method is None or self.args is None and self.kwargs is None:
            raise RuntimeError('invalid usage')
        bind_result = {}
        argspec = inspect.getargspec(self.method)
        formal_arguments = argspec.args
        defaults = argspec.defaults
        if defaults is not None:
            defaults = dict(zip(formal_arguments[-1 * len(defaults):], defaults))
        else:
            defaults = dict()
        actual_arguments = list(self.args or [])
        keyword_arguments = self.kwargs or {}
        if len(actual_arguments) > len(formal_arguments):
            if argspec.varargs is None:
                raise ValueError('too many arguments')
            bind_result.update(dict(zip(formal_arguments, actual_arguments[:len(formal_arguments)])))
            bind_result[argspec.varargs] = tuple(actual_arguments[len(formal_arguments):])
            if argspec.keywords is not None:
                for keyword_argument in keyword_arguments:
                    if keyword_argument in formal_arguments:
                        raise ValueError('mutiple value for argument: %s' % keyword_argument)

                bind_result[argspec.keywords] = keyword_arguments
            elif keyword_arguments:
                raise ValueError('there is no keyword arguments')
        else:
            if argspec.varargs is not None:
                bind_result[argspec.varargs] = tuple()
            bind_result.update(dict(zip(formal_arguments[:len(actual_arguments)], actual_arguments)))
            for formal_argument in formal_arguments[len(actual_arguments):]:
                if formal_argument in keyword_arguments:
                    bind_result[formal_argument] = keyword_arguments.pop(formal_argument)
                    continue
                if formal_argument not in defaults:
                    raise ValueError('missing argument: %s' % formal_argument)
                bind_result[formal_argument] = defaults[formal_argument]

            if argspec.keywords is not None:
                for keyword_argument in keyword_arguments:
                    if keyword_argument in formal_arguments[:len(actual_arguments)]:
                        raise ValueError('mutiple value for argument: %s' % keyword_argument)

                bind_result[argspec.keywords] = keyword_arguments
            elif keyword_arguments:
                raise ValueError('there is no keyword arguments')
        return bind_result

    def proceed(self):
        if self.method is None or self.args is None and self.kwargs is None:
            raise RuntimeError('invalid usage')
        return self.method(*(self.args or tuple()), **(self.kwargs or dict()))