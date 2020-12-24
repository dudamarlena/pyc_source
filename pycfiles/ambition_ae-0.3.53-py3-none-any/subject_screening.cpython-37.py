# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/subject_screening.py
# Compiled at: 2018-07-21 08:49:30
# Size of source mod 2**32: 899 bytes
from edc_constants.constants import FEMALE, YES, NO, MALE
from edc_form_validators import FormValidator

class SubjectScreeningFormValidator(FormValidator):

    def clean(self):
        condition = self.cleaned_data.get('gender') == FEMALE and self.cleaned_data.get('pregnancy') in [YES, NO]
        self.required_if_true(condition=condition,
          field_required='preg_test_date')
        self.applicable_if(FEMALE, field='gender', field_applicable='pregnancy')
        self.not_applicable_if(MALE, field='gender', field_applicable='pregnancy')
        self.not_applicable_if(MALE, field='gender', field_applicable='breast_feeding')
        self.required_if(YES,
          field='unsuitable_for_study',
          field_required='reasons_unsuitable')