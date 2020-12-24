# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/radiology.py
# Compiled at: 2018-01-29 14:27:09
# Size of source mod 2**32: 1707 bytes
from edc_constants.constants import OTHER, YES
from edc_form_validators import FormValidator

class RadiologyFormValidator(FormValidator):

    def clean(self):
        self.required_if(YES,
          field='cxr_done',
          field_required='cxr_date')
        self.required_if(YES,
          field='cxr_done',
          field_required='cxr_type')
        self.m2m_other_specify('infiltrates',
          m2m_field='cxr_type',
          field_other='infiltrate_location')
        self.required_if(YES,
          field='ct_performed',
          field_required='ct_performed_date')
        self.applicable_if(YES,
          field='ct_performed',
          field_applicable='scanned_with_contrast')
        self.applicable_if(YES,
          field='ct_performed',
          field_applicable='brain_imaging_reason')
        self.validate_other_specify(field='brain_imaging_reason',
          other_specify_field='brain_imaging_reason_other',
          other_stored_value=OTHER)
        self.required_if(YES,
          field='ct_performed',
          field_required='are_results_abnormal')
        self.required_if(YES,
          field='are_results_abnormal',
          field_required='abnormal_results_reason')
        self.m2m_other_specify(OTHER,
          m2m_field='abnormal_results_reason',
          field_other='abnormal_results_reason_other')
        self.m2m_other_specify('infarcts',
          m2m_field='abnormal_results_reason',
          field_other='infarcts_location')