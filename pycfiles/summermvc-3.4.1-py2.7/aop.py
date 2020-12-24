# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/decorator/aop.py
# Compiled at: 2018-05-30 07:45:01
__all__ = [
 'aspect', 'get_aspect', 'is_aspect_present',
 'before', 'get_before', 'is_before_present',
 'around', 'get_around', 'is_around_present',
 'after_throwing', 'get_after_throwing', 'is_after_throwing_present',
 'after_returning', 'get_after_returning', 'is_after_returning_present',
 'after', 'get_after', 'is_after_present']
__authors__ = ['Tim Chow']
import inspect, types
from ..reflect import get_declared_fields

def aspect(order):
    if not isinstance(order, int):
        raise ValueError("expect 'int', not %r" % type(order).__name__)

    def _inner(cls):
        if not inspect.isclass(cls):
            raise RuntimeError("expect 'class', not %r" % type(cls).__name__)
        setattr(cls, '__aop_aspect__', order)
        return cls

    return _inner


def get_aspect(cls):
    if not inspect.isclass(cls):
        return None
    else:
        if '__aop_aspect__' not in get_declared_fields(cls, only_names=True):
            return None
        order = getattr(cls, '__aop_aspect__')
        if not isinstance(order, int):
            return None
        return order


def is_aspect_present(cls):
    return get_aspect(cls) is not None


class AdviceFactory(object):
    define_advice_type = '{{ADIVICE_TYPE_PLACEHOLDER}}'
    advice = 'def {{ADIVICE_TYPE_PLACEHOLDER}}(point_cut):\n    def _inner(f):\n        if not isinstance(f, types.FunctionType):\n            raise RuntimeError("expect function type, not %r" % type(f))\n        setattr(f, "__aop_point_cut_{{ADIVICE_TYPE_PLACEHOLDER}}__",\n            point_cut)\n        return f\n    return _inner\n'
    get_advice = 'def get_{{ADIVICE_TYPE_PLACEHOLDER}}(f):\n    if not isinstance(f, types.MethodType):\n        raise RuntimeError("expect method type, not %r" % type(f))\n    if "__aop_point_cut_{{ADIVICE_TYPE_PLACEHOLDER}}__" not in get_declared_fields(f, only_names=True):\n        return None\n    attr_value = getattr(f, \n        "__aop_point_cut_{{ADIVICE_TYPE_PLACEHOLDER}}__")\n    if not isinstance(attr_value, basestring):\n        return None\n    return attr_value\n'
    is_advice_present = 'def is_{{ADIVICE_TYPE_PLACEHOLDER}}_present(f):\n    return get_{{ADIVICE_TYPE_PLACEHOLDER}}(f) is not None\n'

    @classmethod
    def create(cls, advice_type):
        if advice_type not in ('before', 'around', 'after_throwing', 'after_returning',
                               'after'):
            raise ValueError('invalid advice type')
        locals = {}
        exec (
         cls.advice.replace(cls.define_advice_type, advice_type), globals(), locals)
        exec (
         cls.get_advice.replace(cls.define_advice_type, advice_type), globals(), locals)
        exec (
         cls.is_advice_present.replace(cls.define_advice_type, advice_type), globals(), locals)
        return (locals[advice_type], locals[('get_' + advice_type)],
         locals[('is_' + advice_type + '_present')])


before, get_before, is_before_present = AdviceFactory.create('before')
around, get_around, is_around_present = AdviceFactory.create('around')
after, get_after, is_after_present = AdviceFactory.create('after')
after_throwing, get_after_throwing, is_after_throwing_present = AdviceFactory.create('after_throwing')
after_returning, get_after_returning, is_after_returning_present = AdviceFactory.create('after_returning')