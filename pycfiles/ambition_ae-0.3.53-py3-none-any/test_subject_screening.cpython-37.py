# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/tests/test_subject_screening.py
# Compiled at: 2018-07-21 08:49:31
# Size of source mod 2**32: 2121 bytes
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import MALE, YES, NOT_APPLICABLE, NO, FEMALE
from ..form_validators import SubjectScreeningFormValidator

class TestSubjectScreeningFormValidator(TestCase):

    def test_gender(self):
        options = {'gender':MALE, 
         'pregnancy':YES}
        form_validator = SubjectScreeningFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('pregnancy', form_validator._errors)

    def test_preg_test_date_yes(self):
        options = {'gender':FEMALE, 
         'pregnancy':YES, 
         'preg_test_date':None}
        form_validator = SubjectScreeningFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('preg_test_date', form_validator._errors)

    def test_preg_test_date_no(self):
        options = {'gender':FEMALE, 
         'pregnancy':NO, 
         'preg_test_date':None}
        form_validator = SubjectScreeningFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('preg_test_date', form_validator._errors)

    def test_preg_test_date_NA(self):
        options = {'gender':MALE, 
         'pregnancy':NOT_APPLICABLE, 
         'preg_test_date':get_utcnow}
        form_validator = SubjectScreeningFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('preg_test_date', form_validator._errors)

    def test_gender_male_breast_feeding_invalid(self):
        options = {'gender':MALE, 
         'pregnancy':NOT_APPLICABLE, 
         'breast_feeding':YES}
        form_validator = SubjectScreeningFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('breast_feeding', form_validator._errors)