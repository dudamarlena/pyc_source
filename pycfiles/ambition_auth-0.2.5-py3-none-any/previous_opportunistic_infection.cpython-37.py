# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/previous_opportunistic_infection.py
# Compiled at: 2018-01-29 14:27:09
# Size of source mod 2**32: 818 bytes
from edc_constants.constants import YES
from edc_form_validators import FormValidator

class PreviousOpportunisticInfectionFormValidator(FormValidator):

    def clean(self):
        condition = self.cleaned_data.get('patient_history') and self.cleaned_data.get('patient_history').previous_oi == YES
        self.required_if_true(condition=condition,
          field_required='previous_non_tb_oi',
          not_required_msg="Cannot fill in this form without any previous opportunistic infections in patient's history form.")
        self.not_required_if(None,
          field='previous_non_tb_oi',
          field_required='previous_non_tb_oi_date')
        self.validate_other_specify(field='previous_non_tb_oi')