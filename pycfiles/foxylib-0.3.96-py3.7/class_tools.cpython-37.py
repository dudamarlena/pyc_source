# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/native/class_tools.py
# Compiled at: 2019-08-16 19:23:53
# Size of source mod 2**32: 681 bytes
import inspect
from operator import itemgetter as ig
from future.utils import lfilter

class ClassToolkit:

    @classmethod
    def cls2name(cls, clazz):
        return clazz.__name__

    @classmethod
    def cls2name_lower(cls, clazz):
        return cls.cls2name(clazz).lower()


class ModuleToolkit:

    @classmethod
    def module2class_list(cls, module):
        m_list = inspect.getmembers(module, inspect.isclass)
        clazz_list = lfilter(lambda x: x.__module__ == module.__name__, map(ig(1), m_list))
        return clazz_list

    @classmethod
    def x2module(cls, x):
        return x.__module__


cls2name = ClassToolkit.cls2name
module2class_list = ModuleToolkit.module2class_list