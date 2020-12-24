# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/missed_doses.py
# Compiled at: 2018-01-29 14:27:09
# Size of source mod 2**32: 575 bytes
from edc_constants.constants import OTHER
from edc_form_validators import FormValidator

class MissedDosesFormValidator(FormValidator):
    field = None
    reason_field = None
    reason_other_field = None
    day_range = None

    def clean(self):
        field_value = self.cleaned_data.get(self.field)
        self.required_if_true(condition=(field_value in self.day_range),
          field_required=(self.reason_field))
        self.required_if(OTHER,
          field=(self.reason_field),
          field_required=(self.reason_other_field))