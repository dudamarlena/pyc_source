# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/classes/check.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 1696 bytes
import importlib, inspect, pkgutil
from ..exceptions import CheckError

class Check:
    NUMERIC_TYPES = (
     int, float, complex)
    ASSERTIONS_PACKAGE = 'fluentcheck.assertions_check'

    def _import_assertion_modules(self):
        ass = importlib.import_module(Check.ASSERTIONS_PACKAGE)
        assertion_modules = list()
        for _1, module_name, _2 in pkgutil.iter_modules(ass.__path__):
            assertion_modules.append(importlib.import_module(ass.__name__ + '.' + module_name))

        return assertion_modules

    def __new__(cls, *args, **kwargs):
        assertion_modules = cls._import_assertion_modules(cls)
        instance = super(Check, cls).__new__(cls)
        for module in assertion_modules:
            for item in inspect.getmembers(module, inspect.isfunction):
                func_name = item[0]
                func = item[1]
                bound_method = func.__get__(instance, instance.__class__)
                setattr(instance, func_name, bound_method)

        return instance

    def __init__(self, value):
        self._val = value

    @property
    def value(self):
        return self._val

    def is_none(self):
        try:
            assert self._val is None
            return self
        except AssertionError:
            raise CheckError('{} is not None'.format(self._val))

    def is_not_none(self):
        try:
            assert self._val is not None
            return self
        except AssertionError:
            raise CheckError('{} is None'.format(self._val))