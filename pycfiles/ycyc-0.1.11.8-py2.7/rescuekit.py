# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/tools/rescuekit.py
# Compiled at: 2016-02-25 04:17:16
import inspect
from ycyc.base.decoratorutils import allow_unbound_method

def init_if_is_class(cls_or_ins):
    if inspect.isclass(cls_or_ins):
        cls_or_ins = cls_or_ins()
    return cls_or_ins


class Rescue(object):

    @allow_unbound_method
    def catch(cls_or_ins, value, exception=Exception):
        self = init_if_is_class(cls_or_ins)
        self.exceptions[exception] = value
        return self

    @allow_unbound_method
    def meet(cls_or_ins, value, wish=None):
        self = init_if_is_class(cls_or_ins)
        self.conversions[wish] = value
        return self

    def __init__(self):
        self.exceptions = {}
        self.conversions = {}

    def call(self, func, *args, **kwg):
        try:
            result = func(*args, **kwg)
            return self.conversions.get(result, result)
        except Exception as err:
            err_typ = type(err)
            if err_typ in self.exceptions:
                return self.exceptions[err_typ]
            for types, val in self.exceptions.items():
                if isinstance(err, types):
                    return val