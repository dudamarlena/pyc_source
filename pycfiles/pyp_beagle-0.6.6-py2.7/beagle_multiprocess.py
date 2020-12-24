# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyp_beagle/beagle_multiprocess.py
# Compiled at: 2019-07-16 04:25:49
import copy_reg, types

def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    if func_name.startswith('__') and not func_name.endswith('__'):
        cls_name = cls.__name__.lstrip('_')
        func_name = '_' + cls_name + func_name
    return (
     _unpickle_method, (func_name, obj, cls))


def _unpickle_method(func_name, obj, cls):
    for cls in cls.__mro__:
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break

    return func.__get__(obj, cls)


copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)