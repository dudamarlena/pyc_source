# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/week16.py
# Compiled at: 2018-01-29 14:27:09
# Size of source mod 2**32: 659 bytes
from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator

class Week16FormValidator(FormValidator):

    def clean(self):
        self.required_if(NO,
          field='patient_alive',
          field_required='death_datetime')
        self.applicable_if(YES,
          field='patient_alive',
          field_applicable='activities_help')
        self.applicable_if(YES,
          field='patient_alive',
          field_applicable='illness_problems')
        self.required_if(YES,
          field='patient_alive',
          field_required='rankin_score')