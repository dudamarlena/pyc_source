# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/week2.py
# Compiled at: 2018-07-21 08:49:30
# Size of source mod 2**32: 1048 bytes
from edc_constants.constants import YES, OTHER
from edc_form_validators import FormValidator

class Week2FormValidator(FormValidator):

    def clean(self):
        self.required_if(YES,
          field='discharged',
          field_required='discharge_date')
        self.required_if(YES,
          field='discharged',
          field_required='research_discharge_date')
        self.required_if(YES,
          field='died',
          field_required='death_date_time')
        self.m2m_other_specify(OTHER,
          m2m_field='drug_intervention',
          field_other='drug_intervention_other')
        self.m2m_other_specify(OTHER,
          m2m_field='antibiotic',
          field_other='antibiotic_other')
        self.required_if(YES,
          field='blood_received',
          field_required='units')
        self.m2m_other_specify(OTHER,
          m2m_field='medicines',
          field_other='medicine_other')