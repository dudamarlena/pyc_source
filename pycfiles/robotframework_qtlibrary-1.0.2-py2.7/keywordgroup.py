# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\QTLibrary\keywords\keywordgroup.py
# Compiled at: 2017-04-20 20:38:18
import sys, inspect
from decorator import decorator

def _run_on_failure_decorator(method, *args, **kwargs):
    self = args[0]
    self._has_run_on_failure = False
    already_in_keyword = getattr(self, '_already_in_keyword', False)
    self._already_in_keyword = True
    try:
        try:
            return method(*args, **kwargs)
        except Exception as err:
            if hasattr(self, '_run_on_failure') and not self._has_run_on_failure:
                self._has_run_on_failure = True
                self._run_on_failure()
            raise

    finally:
        if not already_in_keyword:
            self._already_in_keyword = False
            self._has_run_on_failure = False


class KeywordGroupMetaClass(type):

    def __new__(cls, clsname, bases, dict):
        if decorator:
            for name, method in list(dict.items()):
                if not name.startswith('_') and inspect.isroutine(method):
                    dict[name] = decorator(_run_on_failure_decorator, method)

        return type.__new__(cls, clsname, bases, dict)


class KeywordGroup(object):
    __metaclass__ = KeywordGroupMetaClass