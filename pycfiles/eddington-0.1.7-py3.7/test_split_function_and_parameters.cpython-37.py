# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/app_util/test_split_function_and_parameters.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 1357 bytes
from unittest import TestCase
from eddington.app_util import split_function_and_parameters

class TestSplitFunctionAndParameters(TestCase):

    def check(self):
        func, parameters = split_function_and_parameters(self.function_repr)
        self.assertEqual((self.expected_func),
          func, msg='Function is different than expected')
        self.assertEqual((self.expected_parameters),
          parameters,
          msg='Parameters are different than expected')

    def test_none(self):
        self.function_repr = None
        self.expected_func = None
        self.expected_parameters = []
        self.check()

    def test_empty_list(self):
        self.function_repr = []
        self.expected_func = None
        self.expected_parameters = []
        self.check()

    def test_string(self):
        self.function_repr = 'func'
        self.expected_func = 'func'
        self.expected_parameters = []
        self.check()

    def test_list_with_one_element(self):
        self.function_repr = [
         'func']
        self.expected_func = 'func'
        self.expected_parameters = []
        self.check()

    def test_list_with_multiple_element(self):
        self.function_repr = [
         'func', 1, 'b']
        self.expected_func = 'func'
        self.expected_parameters = [1, 'b']
        self.check()