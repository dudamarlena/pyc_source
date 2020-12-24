# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/follow_up.py
# Compiled at: 2018-07-21 08:49:30
# Size of source mod 2**32: 608 bytes
from edc_constants.constants import YES, OTHER
from edc_form_validators import FormValidator

class FollowUpFormValidator(FormValidator):

    def clean(self):
        self.validate_other_specify(field='fluconazole_dose',
          other_specify_field='fluconazole_dose_other',
          other_stored_value=OTHER)
        self.required_if(YES,
          field='rifampicin_started',
          field_required='rifampicin_start_date')
        self.required_if(YES,
          field='blood_transfusions',
          field_required='blood_transfusions_units')