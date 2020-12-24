# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/test/test_dict.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 6050 bytes
"""
Tests for dict duplicate keys Pyflakes behavior.
"""
from sys import version_info
from pyflakes import messages as m
from pyflakes.test.harness import TestCase, skipIf

class Test(TestCase):

    def test_duplicate_keys(self):
        self.flakes("{'yes': 1, 'yes': 2}", m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    @skipIf(version_info < (3, ), "bytes and strings with same 'value' are not equal in python3")
    def test_duplicate_keys_bytes_vs_unicode_py3(self):
        self.flakes("{b'a': 1, u'a': 2}")

    @skipIf(version_info < (3, ), "bytes and strings with same 'value' are not equal in python3")
    def test_duplicate_values_bytes_vs_unicode_py3(self):
        self.flakes("{1: b'a', 1: u'a'}", m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    @skipIf(version_info >= (3, ), "bytes and strings with same 'value' are equal in python2")
    def test_duplicate_keys_bytes_vs_unicode_py2(self):
        self.flakes("{b'a': 1, u'a': 2}", m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    @skipIf(version_info >= (3, ), "bytes and strings with same 'value' are equal in python2")
    def test_duplicate_values_bytes_vs_unicode_py2(self):
        self.flakes("{1: b'a', 1: u'a'}")

    def test_multiple_duplicate_keys(self):
        self.flakes("{'yes': 1, 'yes': 2, 'no': 2, 'no': 3}", m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    def test_duplicate_keys_in_function(self):
        self.flakes("\n            def f(thing):\n                pass\n            f({'yes': 1, 'yes': 2})\n            ", m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    def test_duplicate_keys_in_lambda(self):
        self.flakes('lambda x: {(0,1): 1, (0,1): 2}', m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    def test_duplicate_keys_tuples(self):
        self.flakes('{(0,1): 1, (0,1): 2}', m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    def test_duplicate_keys_tuples_int_and_float(self):
        self.flakes('{(0,1): 1, (0,1.0): 2}', m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    def test_duplicate_keys_ints(self):
        self.flakes('{1: 1, 1: 2}', m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    def test_duplicate_keys_bools(self):
        self.flakes('{True: 1, True: 2}', m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    def test_duplicate_keys_bools_false(self):
        self.flakes('{False: 1, False: 2}', m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    def test_duplicate_keys_none(self):
        self.flakes('{None: 1, None: 2}', m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    def test_duplicate_variable_keys(self):
        self.flakes('\n            a = 1\n            {a: 1, a: 2}\n            ', m.MultiValueRepeatedKeyVariable, m.MultiValueRepeatedKeyVariable)

    def test_duplicate_variable_values(self):
        self.flakes('\n            a = 1\n            b = 2\n            {1: a, 1: b}\n            ', m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    def test_duplicate_variable_values_same_value(self):
        self.flakes('\n            a = 1\n            b = 1\n            {1: a, 1: b}\n            ', m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    def test_duplicate_key_float_and_int(self):
        """
        These do look like different values, but when it comes to their use as
        keys, they compare as equal and so are actually duplicates.
        The literal dict {1: 1, 1.0: 1} actually becomes {1.0: 1}.
        """
        self.flakes('\n            {1: 1, 1.0: 2}\n            ', m.MultiValueRepeatedKeyLiteral, m.MultiValueRepeatedKeyLiteral)

    def test_no_duplicate_key_error_same_value(self):
        self.flakes("\n        {'yes': 1, 'yes': 1}\n        ")

    def test_no_duplicate_key_errors(self):
        self.flakes("\n        {'yes': 1, 'no': 2}\n        ")

    def test_no_duplicate_keys_tuples_same_first_element(self):
        self.flakes('{(0,1): 1, (0,2): 1}')

    def test_no_duplicate_key_errors_func_call(self):
        self.flakes('\n        def test(thing):\n            pass\n        test({True: 1, None: 2, False: 1})\n        ')

    def test_no_duplicate_key_errors_bool_or_none(self):
        self.flakes('{True: 1, None: 2, False: 1}')

    def test_no_duplicate_key_errors_ints(self):
        self.flakes('\n        {1: 1, 2: 1}\n        ')

    def test_no_duplicate_key_errors_vars(self):
        self.flakes("\n        test = 'yes'\n        rest = 'yes'\n        {test: 1, rest: 2}\n        ")

    def test_no_duplicate_key_errors_tuples(self):
        self.flakes('\n        {(0,1): 1, (0,2): 1}\n        ')

    def test_no_duplicate_key_errors_instance_attributes(self):
        self.flakes('\n        class Test():\n            pass\n        f = Test()\n        f.a = 1\n        {f.a: 1, f.a: 1}\n        ')