# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/asserter.py
# Compiled at: 2009-10-07 18:08:46
"""Help hook into asserts, for verbose asserts"""
import sys

class Asserter:
    __module__ = __name__
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        if not self.__shared_state:
            self._reporters = {}

    def _import(self, package_name, class_name):
        return getattr(__import__(package_name), class_name)

    def _make_assert_report(self, Class, method_name):
        if getattr(Class, method_name).__name__ == '_assert_reporting_func':
            return
        variables = eval('Class.%s' % method_name).func_code.co_varnames
        setattr(Class, '_real_function_%s' % method_name, eval('Class.%s' % method_name))
        method = eval('Class._real_function_%s' % method_name)

        def _assert_reporting_func(*args, **kwargs):
            num_free_args = len(variables)
            additional_args = ()
            if kwargs:
                num_free_args -= 1
                additional_args = (kwargs,)
            if len(args) > num_free_args:
                num_free_args -= 1
                additional_args = args[num_free_args:] + additional_args
            varList = zip(variables[1:], args[1:num_free_args] + additional_args)
            test = sys._getframe().f_back.f_locals['self']
            if not self._reporters.get(test):
                return method(*args, **kwargs)
            try:
                method(*args, **kwargs)
            except Exception, e:
                self._reporters[test].addAssert(test, method_name, varList, e)
                raise

            self._reporters[test].addAssert(test, method_name, varList, None)
            return

        setattr(Class, method_name, _assert_reporting_func)

    def set_reporter(self, test, reporter):
        self._reporters[test] = reporter

    def make_asserts_report(self, module_name, class_name, methods_pattern):
        Class = self._import(module_name, class_name)
        from re import match
        for method_name in dir(Class):
            if match(methods_pattern, method_name):
                self._make_assert_report(Class, method_name)


def register_asserter():
    Asserter().make_asserts_report('unittest', 'TestCase', '(^assert)|(^fail[A-Z])|(^fail$)')
    Asserter().make_asserts_report('testoob', 'testing', '^assert')