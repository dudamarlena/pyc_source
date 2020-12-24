# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/sql/tests/test_wrapper.py
# Compiled at: 2007-12-17 11:25:35
"""
Generic Test case for 'iw.sqlalchemy' doctest
"""
__docformat__ = 'restructuredtext'
import unittest
from wrapper import DynamicDecorator

class TestWrapper(unittest.TestCase):
    __module__ = __name__

    def test_ddecorator(self):

        class A(object):
            __module__ = __name__

            def func(self):
                return 1

        def dec(func):

            def func_plus_one(*args, **kw):
                return func(*args, **kw) + 1

            return func_plus_one

        a = DynamicDecorator(A, dec)
        self.assertEquals(a.func(), 2)


def test_suite():
    tests = [
     unittest.makeSuite(TestWrapper)]
    return unittest.TestSuite(tests)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')