# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /pmc/Work/kolotev/0git/.github/django-enumfield-named-choices/django_enumfield_named_choices/tests/test_validators.py
# Compiled at: 2019-08-20 19:04:03
# Size of source mod 2**32: 1929 bytes
import unittest
from django_enumfield_named_choices.tests.models import BeerStyle, NamedBeerStyle
from django_enumfield_named_choices.validators import validate_available_choice
from django_enumfield_named_choices.exceptions import InvalidStatusOperationError

class ValidatorTest(unittest.TestCase):

    def test_validate_available_choice_1(self):
        """Test passing a value non convertable to an int raises an
        InvalidStatusOperationError
        """
        (self.assertRaises)(InvalidStatusOperationError, validate_available_choice, *(
         BeerStyle, 'Not an int'))

    def test_validate_available_choice_2(self):
        """Test passing an int as a string validation
        """
        self.assertIsNone(validate_available_choice(BeerStyle, '%s' % BeerStyle.LAGER))

    def test_validate_available_choice_3(self):
        """Test passing an int validation
        """
        self.assertIsNone(validate_available_choice(BeerStyle, BeerStyle.LAGER))

    def test_validate_available_choice_4(self):
        """Test passing a Name validation
        """
        self.assertIsNone(validate_available_choice(BeerStyle, BeerStyle.name(BeerStyle.LAGER)))

    def test_validate_available_choice_5(self):
        """Test passing a Name validation
        """
        self.assertIsNone(validate_available_choice(BeerStyle, BeerStyle.value(BeerStyle.LAGER)))

    def test_validate_available_choice_6(self):
        """Test passing a Name validation
        """
        self.assertIsNone(validate_available_choice(NamedBeerStyle, NamedBeerStyle.name(NamedBeerStyle.LAGER)))

    def test_validate_available_choice_7(self):
        """Test passing a Name validation
        """
        self.assertIsNone(validate_available_choice(NamedBeerStyle, NamedBeerStyle.value(NamedBeerStyle.LAGER)))