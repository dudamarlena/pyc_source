# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/tests/test_education_validator.py
# Compiled at: 2018-03-07 07:42:56
# Size of source mod 2**32: 2088 bytes
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import NO
from ..form_validators import EducationFormValidator

class TestEducationalBackgroundFormValidator(TestCase):

    def test_total_money_spent_error(self):
        cleaned_data = {'education_years':15, 
         'attendance_years':10, 
         'secondary_years':5, 
         'higher_years':10}
        form_validator = EducationFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('education_years', form_validator._errors)

    def test_total_money_spent(self):
        cleaned_data = {'education_years':25, 
         'attendance_years':10, 
         'secondary_years':5, 
         'higher_years':10}
        form_validator = EducationFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e

    def test_attendance_years(self):
        cleaned_data = {'elementary':NO, 
         'attendance_years':1}
        form = EducationFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('attendance_years', form._errors)

    def test_secondary_years(self):
        cleaned_data = {'secondary':NO, 
         'secondary_years':1}
        form = EducationFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('secondary_years', form._errors)

    def test_higher_education(self):
        cleaned_data = {'higher_education':NO, 
         'higher_years':1}
        form = EducationFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('higher_years', form._errors)