# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/medical_expenses_two_detail.py
# Compiled at: 2018-01-29 14:27:09
# Size of source mod 2**32: 1614 bytes
import django.forms as forms
from edc_constants.constants import YES, NOT_APPLICABLE
from edc_form_validators import FormValidator, NOT_REQUIRED_ERROR

class MedicalExpensesTwoDetailFormValidator(FormValidator):

    def clean(self):
        self.validate_other_specify(field='location_care')
        self.only_not_required_if(NOT_APPLICABLE,
          field='transport_form',
          field_required='transport_cost',
          cleaned_data=(self.cleaned_data))
        self.only_not_required_if(NOT_APPLICABLE,
          field='transport_form',
          field_required='transport_duration',
          cleaned_data=(self.cleaned_data))
        self.validate_other_specify(field='care_provider')
        self.required_if(YES,
          field='paid_treatment',
          field_required='paid_treatment_amount')
        self.required_if(YES,
          field='medication_bought',
          field_required='medication_payment')

    def only_not_required_if(self, *responses, field=None, field_required=None, cleaned_data=None):
        if self.cleaned_data.get(field):
            if self.cleaned_data.get(field) in responses:
                if cleaned_data.get(field_required):
                    if cleaned_data.get(field_required) != NOT_APPLICABLE:
                        message = {field_required: 'This field is not required.'}
                        self._errors.update(message)
                        self._error_codes.append(NOT_REQUIRED_ERROR)
                        raise forms.ValidationError(message, code=NOT_REQUIRED_ERROR)