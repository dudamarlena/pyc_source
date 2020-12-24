# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\CODE\VScode\autowork\ymm-automation\ymmuim-library\YmmuimLibrary\keywords\keywordgroup.py
# Compiled at: 2019-07-01 05:54:08
# Size of source mod 2**32: 1037 bytes
import sys, inspect
from six import with_metaclass
try:
    from decorator import decorator
except SyntaxError:
    decorator = None

if sys.platform == 'cli':
    decorator = None

def _run_on_failure_decorator(method, *args, **kwargs):
    try:
        return method(*args, **kwargs)
    except Exception as err:
        try:
            self = args[0]
            if hasattr(self, '_run_on_failure'):
                self._run_on_failure()
            raise err
        finally:
            err = None
            del err


class KeywordGroupMetaClass(type):

    def __new__(cls, clsname, bases, dict):
        if decorator:
            for name, method in dict.items():
                if name.startswith('_') or inspect.isroutine(method):
                    dict[name] = decorator(_run_on_failure_decorator, method)

        return type.__new__(cls, clsname, bases, dict)


class KeywordGroup(with_metaclass(KeywordGroupMetaClass, object)):
    pass