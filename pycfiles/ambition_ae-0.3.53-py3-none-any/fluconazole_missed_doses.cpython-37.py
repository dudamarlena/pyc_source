# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/fluconazole_missed_doses.py
# Compiled at: 2018-01-29 14:27:09
# Size of source mod 2**32: 273 bytes
from .missed_doses import MissedDosesFormValidator

class FluconazoleMissedDosesFormValidator(MissedDosesFormValidator):
    field = 'flucon_day_missed'
    reason_field = 'flucon_missed_reason'
    reason_other_field = 'missed_reason_other'
    day_range = range(1, 15)