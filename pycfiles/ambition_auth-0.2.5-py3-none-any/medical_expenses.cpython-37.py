# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/medical_expenses.py
# Compiled at: 2018-07-21 08:49:30
# Size of source mod 2**32: 2221 bytes
import django.forms as forms
from edc_constants.constants import YES, OTHER, NOT_APPLICABLE
from edc_form_validators import FormValidator
from ..constants import WORKING

class MedicalExpensesFormValidator(FormValidator):

    def clean(self):
        subject_costs = self.cleaned_data.get('subject_spent_last_4wks')
        someone_costs = self.cleaned_data.get('someone_spent_last_4wks')
        try:
            total = subject_costs + someone_costs
        except TypeError:
            pass
        else:
            if total != self.cleaned_data.get('total_spent_last_4wks'):
                raise forms.ValidationError({'total_spent_last_4wks': f"Expected '{total}'."})
            self.required_if(WORKING,
              field='activities_missed',
              field_required='time_off_work')
            self.validate_other_specify(field='activities_missed',
              other_specify_field='activities_missed_other',
              other_stored_value=OTHER)
            self.required_if(YES,
              field='loss_of_earnings',
              field_required='earnings_lost_amount')
            if self.cleaned_data.get('form_of_transport'):
                if self.cleaned_data.get('form_of_transport') not in [
                 NOT_APPLICABLE, 'foot', 'bicycle', 'ambulance']:
                    if self.cleaned_data.get('transport_fare') is None:
                        raise forms.ValidationError({'transport_fare': 'This field is required.'})
                if self.cleaned_data.get('form_of_transport') in [
                 NOT_APPLICABLE, 'foot', 'bicycle', 'ambulance']:
                    if self.cleaned_data.get('transport_fare') is not None:
                        raise forms.ValidationError({'transport_fare': 'This field is not required.'})
            self.required_if_true(condition=(self.cleaned_data.get('form_of_transport') != NOT_APPLICABLE),
              field_required='travel_time')
            self.required_if(YES,
              field='private_healthcare',
              field_required='healthcare_insurance')