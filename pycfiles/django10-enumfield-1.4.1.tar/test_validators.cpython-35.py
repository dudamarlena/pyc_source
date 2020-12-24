# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jb/projects/i2biz/misc/django-enumfield/django_enumfield/tests/test_validators.py
# Compiled at: 2017-10-06 05:18:16
# Size of source mod 2**32: 995 bytes
import unittest
from django_enumfield.tests.models import BeerStyle
from django_enumfield.validators import validate_available_choice
from django_enumfield.exceptions import InvalidStatusOperationError

class ValidatorTest(unittest.TestCase):

    def test_validate_available_choice_1(self):
        """Test passing a value non convertable to an int raises an
        InvalidStatusOperationError
        """
        self.assertRaises(InvalidStatusOperationError, validate_available_choice, *(
         BeerStyle, 'Not an int'))

    def test_validate_available_choice_2(self):
        """Test passing an int as a string validation
        """
        self.assertIsNone(validate_available_choice(BeerStyle, '%s' % BeerStyle.LAGER))

    def test_validate_available_choice_3(self):
        """Test passing an int validation
        """
        self.assertIsNone(validate_available_choice(BeerStyle, BeerStyle.LAGER))