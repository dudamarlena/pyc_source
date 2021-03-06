# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/function/warmer.py
# Compiled at: 2019-12-17 00:50:39
# Size of source mod 2**32: 1460 bytes
import inspect
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.native.class_tool import module2class_list

class Warmer:

    def __init__(self, module):
        super(Warmer, self).__init__()
        self.module = module
        self.h = {}

    @classmethod
    def _func2key(cls, f):
        return FunctionTool.func2module_qualname(f)

    def add(self, func=None, cond=True, args=None, kwargs=None):
        cls = self.__class__
        _args = args or []
        _kwargs = kwargs or {}

        def wrapper(f):
            if cond:
                k = cls._func2key(f)
                self.h[k] = (_args, _kwargs)
            return f

        if func:
            return wrapper(func)
        return wrapper

    @classmethod
    def _dict2warmup(cls, h, target_list):
        h_k2f = {}
        predicate = lambda x: any([inspect.ismethod(x),
         inspect.isfunction(x)])
        for target in target_list:
            for name, f in inspect.getmembers(target, predicate=predicate):
                k = cls._func2key(f)
                h_k2f[k] = f

        for k, (args, kwargs) in h.items():
            f = h_k2f[k]
            f(*args, **kwargs)

    def warmup(self, target_list=None):
        cls = self.__class__
        if target_list is None:
            target_list = [
             self.module] + module2class_list(self.module)
        cls._dict2warmup(self.h, target_list)