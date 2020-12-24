# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/onchange.py
# Compiled at: 2007-12-02 16:26:56


def func_onchange(metric):

    def _inner_onchange(func):
        """A decorator that runs a function only when a generic metric changes."""

        def decorated(*args, **kwargs):
            try:
                mresult = metric(*args, **kwargs)
                if decorated._last_metric != mresult:
                    decorated._last_metric = mresult
                    decorated._last_result = func(*args, **kwargs)
            except AttributeError:
                decorated._last_metric = mresult
                decorated._last_result = func(*args, **kwargs)

            return decorated._last_result

        return decorated

    return _inner_onchange


def method_onchange(metric):

    def _inner_onchange(method):
        """A decorator that runs a method only when a generic metric changes."""
        met_name = '_%s_last_metric' % id(method)
        res_name = '_%s_last_result' % id(method)

        def decorated(self, *args, **kwargs):
            try:
                mresult = metric(*args, **kwargs)
                if getattr(decorated, met_name) != mresult:
                    setattr(decorated, met_name, mresult)
                    setattr(decorated, res_name, method(self, *args, **kwargs))
            except AttributeError:
                setattr(decorated, met_name, mresult)
                setattr(decorated, res_name, method(self, *args, **kwargs))

            return getattr(decorated, res_name)

        return decorated

    return _inner_onchange


from salamoia.tests import *
runDocTests()