# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/test/base.py
# Compiled at: 2019-08-19 15:09:30
"""This module provides basic utilities for usage in any test"""
__docformat__ = 'restructuredtext'
import functools

def insertTest(klass=None, helper_name=None, test_method_name=None, test_method_doc=None, tested_name=None, test_skip=None, **helper_kwargs):
    r"""Decorator that inserts test methods from a helper method that accepts
    arguments.
    `insertTest` provides a very economic API for creating new tests for a given
    class based on a helper method.
    `insertTest` accepts the following arguments:

      - helper_name (str): the name of the helper method. `insertTest` will
                           insert a test method which calls the helper with
                           any the helper_kwargs (see below).
      - test_method_name (str): Optional. Name of the test method to be used.
                                If None given, one will be generated from the
                                tested class and helper names.
      - test_method_doc (str): Optional. The docstring for the inserted test
                               method (this shows in the unit test output).
                               If None given, a default one is generated which
                               includes the input parameters and the helper
                               name.
      - tested_name (str): Optional. The name of the class or feature being
                           tested (if given, it will be used in default method
                           names and docstrings).

      - test_skip (str): Optional. A reason for skipping the test. If None
                         given, the test will not be skipped

      - \*\*helper_kwargs: All remaining keyword arguments are passed to the
                           helper.

    This decorator can be considered a "base" decorator. It is often used to
    create other decorators in which the helper method is pre-set, as in
    the following example::

        isPos = functools.partial(insertTest, helper_name='isPositive')

        @isPos(x=2)
        @isPos(x=10)
        class Foo(unittest.TestCase):
            def isPositive(self, x):
                self.assertTrue(x > 0)

    """
    if klass is None:
        return functools.partial(insertTest, helper_name=helper_name, test_method_name=test_method_name, test_method_doc=test_method_doc, tested_name=tested_name, test_skip=test_skip, **helper_kwargs)
    else:
        if helper_name is None:
            raise ValueError('helper_name argument is not optional')
        if test_method_name is None:
            test_method_name = 'test_'
            if tested_name:
                test_method_name += '%s_' % tested_name
            test_method_name += helper_name
        name, i = test_method_name, 1
        while hasattr(klass, name):
            i += 1
            name = '%s_%i' % (test_method_name, i)

        test_method_name = name
        if test_method_doc is None:
            argsrep = (', ').join([ '%s=%s' % (k, repr(v)) for k, v in helper_kwargs.items()
                                  ])
            if tested_name:
                test_method_doc = 'Testing %s with %s(%s)' % (tested_name,
                 helper_name, argsrep)
            else:
                test_method_doc = 'Testing %s(%s)' % (helper_name, argsrep)

        def newTest(obj):
            helper = getattr(obj, helper_name)
            return helper(**helper_kwargs)

        newTest.__doc__ = test_method_doc
        if test_skip is not None:
            import unittest
            newTest = unittest.skip(test_skip)(newTest)
        setattr(klass, test_method_name, newTest)
        return klass


if __name__ == '__main__':
    import unittest
    isPos = functools.partial(insertTest, helper_name='isPositive')
    isNeg = functools.partial(insertTest, helper_name='isPositive', expected=False)

    @isPos
    @isPos(x=2)
    @isPos(x=10)
    @isPos(x=5)
    @isNeg(x=-1)
    class FooTest(unittest.TestCase):

        def isPositive(self, x=1, expected=True):
            self.assertEqual(x > 0, expected)


    unittest.main(verbosity=2)