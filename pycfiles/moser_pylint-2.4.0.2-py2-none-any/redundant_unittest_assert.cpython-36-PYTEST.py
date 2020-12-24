# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/functional/redundant_unittest_assert.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 1307 bytes
"""
http://www.logilab.org/ticket/355
If you are using assertTrue or assertFalse and the first argument is a
constant(like a string), then the assert will always be true. Therefore,
it should emit a warning message.
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest

@unittest.skip("don't run this")
class Tests(unittest.TestCase):

    def test_something(self):
        """ Simple test """
        some_var = 'It should be assertEqual'
        self.assertTrue('I meant assertEqual not assertTrue', some_var)
        self.assertFalse('I meant assertEqual not assertFalse', some_var)
        self.assertTrue(True, some_var)
        self.assertFalse(False, some_var)
        self.assertFalse(None, some_var)
        self.assertTrue(0, some_var)
        self.assertTrue('should be' in some_var, some_var)
        self.assertTrue(some_var, some_var)


@unittest.skip("don't run this")
class RegressionWithArgs(unittest.TestCase):
    __doc__ = "Don't fail if the bound method doesn't have arguments."

    def test(self):
        self.run()