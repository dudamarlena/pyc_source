# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/tests/tests_validators.py
# Compiled at: 2017-01-13 19:06:36
# Size of source mod 2**32: 1669 bytes
from django.test import TestCase
from django.core.exceptions import ValidationError
from billjobs.validators import validate_accounting_number

class ValidateAccountingNumberTestCase(TestCase):
    __doc__ = ' Test accounting number string validator '

    def test_validate_accounting_number_raise_validationError(self):
        """ Test validator raise a ValidationError """
        with self.assertRaises(ValidationError):
            validate_accounting_number('error')

    def test_validate_accounting_number_message(self):
        """ Test validator message content """
        with self.assertRaisesRegexp(ValidationError, 'Accounting number do not begin with 01'):
            validate_accounting_number('error')

    def test_wrong_string_raise_exception(self):
        """ Test string that do not begin with 01 raise exception """
        with self.assertRaises(ValidationError):
            validate_accounting_number('error')
        with self.assertRaises(ValidationError):
            validate_accounting_number('er01ror')
        with self.assertRaises(ValidationError):
            validate_accounting_number('error01')
        with self.assertRaises(ValidationError):
            validate_accounting_number('0error')

    def test_exception_is_not_raised_with_correct_value(self):
        """ Test good input do not raise exception """
        raised = False
        try:
            validate_accounting_number('01error')
        except ValidationError:
            raised = True

        self.assertFalse(raised)