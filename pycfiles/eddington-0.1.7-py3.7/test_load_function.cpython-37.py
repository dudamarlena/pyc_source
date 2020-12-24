# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/app_util/test_load_function.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 1562 bytes
from unittest import TestCase
from eddington_core import linear, parabolic
from eddington.app_util import load_func

class TestLoadFunc(TestCase):

    def check(self):
        func = load_func(func_name=(self.func_name),
          func_parameters=(self.func_parameters),
          costumed=(self.costumed))
        self.assertEqual((self.expected_func),
          func, msg='Function is different than expected')

    def test_default_is_linear(self):
        self.func_name = None
        self.func_parameters = []
        self.costumed = None
        self.expected_func = linear
        self.check()

    def test_load_from_registry(self):
        self.func_name = 'parabolic'
        self.func_parameters = []
        self.costumed = None
        self.expected_func = parabolic
        self.check()

    def test_costumed(self):
        self.func_name = None
        self.func_parameters = []
        self.costumed = 'a[0] + a[1] * x'
        self.expected_func = parabolic
        func = load_func(func_name=(self.func_name),
          func_parameters=(self.func_parameters),
          costumed=(self.costumed))
        self.assertEqual(2,
          (func.n), msg='Function number of parameters is different than expected')
        self.assertEqual((self.costumed),
          (func.syntax),
          msg='Function syntax is different than expected')
        self.assertEqual(3,
          (func([1, 2], 1)), msg='Function result is different than expected')