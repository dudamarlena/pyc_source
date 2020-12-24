# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/significant_diagnoses.py
# Compiled at: 2018-01-29 14:27:09
# Size of source mod 2**32: 936 bytes
from edc_constants.constants import OTHER, YES
from edc_form_validators import FormValidator

class SignificantDiagnosesFormValidator(FormValidator):

    def clean(self):
        significant_dx_cls = self.cleaned_data.get('week4') or self.cleaned_data.get('week2') or self.cleaned_data.get('followup')
        self.required_if_true(condition=(significant_dx_cls and significant_dx_cls.other_significant_dx == YES),
          field_required='possible_diagnoses')
        self.required_if(YES,
          field='other_significant_diagnoses',
          field_required='possible_diagnoses')
        self.not_required_if(None,
          field='possible_diagnoses',
          field_required='dx_date')
        self.required_if(OTHER,
          field='possible_diagnoses',
          field_required='dx_other')