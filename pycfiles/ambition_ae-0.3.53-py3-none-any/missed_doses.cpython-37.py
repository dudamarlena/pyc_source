# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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