# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/formish/tests/testish/testish/lib/test_func.py
# Compiled at: 2010-01-04 05:35:21
from testish.lib.base import TestCase
from testish.lib import forms

class TestTogether(TestCase):
    """
    Run all tests in a single browser session.
    """

    def test_func(self):
        for attr in dir(forms):
            if attr.startswith('functest_'):
                getattr(forms, attr)(self)


class TestSeparately(TestCase):
    """
    Run each test in a separate browser session.

    Test methods are dynamically added to this class by replacing the functest_
    prefix with test_ and attaching the method to the class (see below).
    """
    pass


for attr in dir(forms):
    if attr.startswith('functest_'):
        func_name = 'test_%s' % attr[9:]
        func = getattr(forms, attr)
        func.__name__ = func_name
        setattr(TestSeparately, func_name, func)