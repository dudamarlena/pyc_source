# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/reflect.py
# Compiled at: 2018-06-03 02:30:54
__all__ = [
 'get_declared_methods', 'get_declared_field', 'get_declared_fields',
 'get_declared_attribute', 'get_declared_attributes']
__authors__ = ['Tim Chow']
import inspect, types

def get_declared_methods(cls, only_names=False):
    u"""返回类中定义的所有实例方法"""
    if not inspect.isclass(cls):
        raise ValueError('expect class')
    for attr_name in vars(cls):
        attr = getattr(cls, attr_name)
        if not isinstance(attr, types.UnboundMethodType):
            continue
        if only_names:
            yield attr_name
        else:
            yield (
             attr_name, attr)


def get_declared_field(obj, field_type, only_names=False):
    u"""返回对象或类中定义的特定类型的所有属性（不包含方法）"""
    if not inspect.isclass(field_type):
        raise StopIteration
    for attr_name, attr_value in vars(obj).iteritems():
        if inspect.isclass(obj) and isinstance(attr_value, types.FunctionType):
            continue
        if not isinstance(attr_value, field_type):
            continue
        if only_names:
            yield attr_name
        else:
            yield (
             attr_name, attr_value)


def get_declared_fields(obj, only_names=False):
    u"""返回对象或类中定义的所有属性（不包含方法）"""
    for attr_name, attr_value in vars(obj).iteritems():
        if inspect.isclass(obj) and isinstance(attr_value, types.FunctionType):
            continue
        if only_names:
            yield attr_name
        else:
            yield (
             attr_name, attr_value)


def get_declared_attribute(obj, attribute_name):
    try:
        if attribute_name in vars(obj):
            return getattr(obj, attribute_name)
    except TypeError:
        pass

    raise ValueError('no attribute named: %s' % attribute_name)


def get_declared_attributes(obj, only_names=False):
    u"""返回对象或类中定义的所有方法和属性"""
    for attr_name, attr_value in vars(obj).iteritems():
        if only_names:
            yield attr_name
        else:
            yield (
             attr_name, attr_value)