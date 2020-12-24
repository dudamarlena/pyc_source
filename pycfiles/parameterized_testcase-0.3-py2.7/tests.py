# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parameterized_testcase/test/tests.py
# Compiled at: 2011-08-19 00:39:38
import unittest
from .. import parameterize

class Echo:

    def test_echo(self):
        return self.param_value


class Llama:

    def test_sound(self):
        return 'A llama says "laga-laga-laga".'


classes = {'Llama': Llama, 'Echo': Echo}
params = {'alpha': {'param_value': 42}, 'beta': {'param_value': 'decay'}}
cases = parameterize([
 Echo, Llama], params)

class Tests(unittest.TestCase):

    def test_count(self):
        """Created proper amount of testcases."""
        self.assertEqual(len(cases), 2 * len(params))

    def test_testcase_subclass(self):
        """Results subclass from TestCase."""
        for case in cases:
            self.assertTrue(issubclass(case, unittest.TestCase))

    def test_custom_baseclass(self):
        """Custom testcase baseclasses are supported.
        """

        class CustomTestCase(object):
            pass

        for case in parameterize([Echo, Llama], params, CustomTestCase):
            self.assertTrue(issubclass(case, CustomTestCase))
            self.assertFalse(issubclass(case, unittest.TestCase))

    def test_subclasses(self):
        """Results subclass from original classes."""
        for case in cases:
            for k, v in classes.items():
                if case.__name__.startswith(k):
                    self.assertTrue(issubclass(case, v))

    def test_param_values(self):
        """Testcases have proper attribute values."""
        for case in cases:
            for set_name, param_set in params.items():
                if case.__name__.endswith(('_{0}').format(set_name)):
                    for k, v in param_set.items():
                        self.assertEqual(getattr(case, k), v)