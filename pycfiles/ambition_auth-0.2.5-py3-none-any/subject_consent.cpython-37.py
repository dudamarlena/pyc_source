# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/subject_consent.py
# Compiled at: 2018-01-29 14:27:09
# Size of source mod 2**32: 2170 bytes
import dateutil.relativedelta as relativedelta
from django import forms
import django.apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import ABNORMAL
from edc_form_validators import FormValidator

class SubjectConsentFormValidator(FormValidator):
    subject_screening_model = 'ambition_screening.subjectscreening'

    def __init__(self, **kwargs):
        (super().__init__)(**kwargs)
        self.dob = self.cleaned_data.get('dob')
        self.consent_datetime = self.cleaned_data.get('consent_datetime')
        self.guardian_name = self.cleaned_data.get('guardian_name')
        self.screening_identifier = self.cleaned_data.get('screening_identifier')

    @property
    def subject_screening_model_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    def clean(self):
        try:
            subject_screening = self.subject_screening_model_cls.objects.get(screening_identifier=(self.screening_identifier))
        except ObjectDoesNotExist:
            raise forms.ValidationError('Complete the "Subject Screening" form before proceeding.',
              code='missing_subject_screening')

        if self.add_form:
            if not self.consent_datetime:
                raise forms.ValidationError({'consent_datetime': 'This field is required.'})
        screening_age_in_years = relativedelta(subject_screening.report_datetime.date(), self.dob).years
        if screening_age_in_years != subject_screening.age_in_years:
            raise forms.ValidationError({'dob': f"Age mismatch. The date of birth entered does not match the age at screening. Expected {subject_screening.age_in_years}. Got {screening_age_in_years}."})
        if subject_screening.mental_status == ABNORMAL:
            if not self.guardian_name:
                raise forms.ValidationError({'guardian_name': f"This field is required. Patient mental status at screening is {subject_screening.mental_status}."})