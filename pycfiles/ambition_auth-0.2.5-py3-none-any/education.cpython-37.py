# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/education.py
# Compiled at: 2018-01-29 14:27:09
# Size of source mod 2**32: 1507 bytes
import django.forms as forms
from edc_form_validators import FormValidator
from edc_constants.constants import YES

class EducationFormValidator(FormValidator):

    def clean(self):
        self.validate_education_years()
        self.required_if(YES,
          field='elementary',
          field_required='attendance_years')
        self.required_if(YES,
          field='secondary',
          field_required='secondary_years')
        self.required_if(YES,
          field='higher_education',
          field_required='higher_years')

    def validate_education_years(self):
        """Raises if the total years of education is not
        the sum of the years spent in primary/secondary/higher.
        """
        attendance_years = self.cleaned_data.get('attendance_years')
        secondary_years = self.cleaned_data.get('secondary_years')
        higher_years = self.cleaned_data.get('higher_years')
        education_years = self.cleaned_data.get('education_years')
        try:
            education_sum = attendance_years + secondary_years + higher_years
        except TypeError:
            pass
        else:
            if education_sum != education_years:
                raise forms.ValidationError({'education_years': f"The total years of education should be the sum of the years spent in primary/secondary/higher.Expected {education_sum}."})