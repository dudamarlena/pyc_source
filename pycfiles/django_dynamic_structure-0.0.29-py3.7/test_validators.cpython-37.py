# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/tests/db/test_validators.py
# Compiled at: 2017-12-05 22:57:16
# Size of source mod 2**32: 1025 bytes
from django.core.exceptions import ValidationError
from django.test import TestCase
from dyn_struct.db import validators

class ParamsValidatorTest(TestCase):

    def test_call(self):
        test_dict = '{"test_key": "test"}'
        params_field = validators.ParamsValidator()
        self.assertIsNone(params_field(test_dict))

    def test_call_with_json_exception(self):
        params_field = validators.ParamsValidator()
        with self.assertRaises(ValidationError) as (ex):
            params_field({'test': 123})
        self.assertIn('Введите корректные JSON данные.', ex.exception)
        self.assertEqual('invalid', ex.exception.code)

    def test_call_with_type_error(self):
        params_field = validators.ParamsValidator()
        with self.assertRaises(ValidationError) as (ex):
            params_field('123')
        self.assertIn('Данные должны иметь вид {"ключ": значение}.', ex.exception)
        self.assertEqual('invalid', ex.exception.code)