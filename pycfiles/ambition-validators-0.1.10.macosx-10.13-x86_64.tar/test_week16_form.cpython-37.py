# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/tests/test_week16_form.py
# Compiled at: 2018-01-29 14:27:09
# Size of source mod 2**32: 3211 bytes
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from ..form_validators import Week16FormValidator

class TestWeek16Form(TestCase):

    def test_patient_dead_death_datetime(self):
        cleaned_data = {'patient_alive':NO, 
         'death_datetime':None}
        week16 = Week16FormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, week16.validate)
        cleaned_data = {'patient_alive':NO, 
         'death_datetime':get_utcnow()}
        week16 = Week16FormValidator(cleaned_data=cleaned_data)
        try:
            week16.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e

    def test_patient_alive_activities_help(self):
        cleaned_data = {'patient_alive':YES, 
         'illness_problems':NO, 
         'rankin_score':1, 
         'activities_help':NOT_APPLICABLE}
        week16 = Week16FormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, week16.validate)
        cleaned_data = {'patient_alive':YES, 
         'illness_problems':NO, 
         'rankin_score':1, 
         'activities_help':YES}
        week16 = Week16FormValidator(cleaned_data=cleaned_data)
        try:
            week16.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e

    def test_patient_alive_illness_problems(self):
        cleaned_data = {'patient_alive':YES, 
         'rankin_score':1, 
         'activities_help':YES, 
         'illness_problems':NOT_APPLICABLE}
        week16 = Week16FormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, week16.validate)
        cleaned_data = {'patient_alive':YES, 
         'rankin_score':1, 
         'activities_help':YES, 
         'illness_problems':YES}
        week16 = Week16FormValidator(cleaned_data=cleaned_data)
        try:
            week16.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e

    def test_patient_alive_rankin_score(self):
        cleaned_data = {'patient_alive':YES, 
         'activities_help':YES, 
         'illness_problems':YES, 
         'rankin_score':None}
        week16 = Week16FormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, week16.validate)
        cleaned_data = {'patient_alive':YES, 
         'activities_help':YES, 
         'illness_problems':YES, 
         'rankin_score':'0'}
        week16 = Week16FormValidator(cleaned_data=cleaned_data)
        try:
            week16.validate()
        except forms.ValidationError as e:
            try:
                self.fail(f"ValidationError unexpectedly raised. Got{e}")
            finally:
                e = None
                del e