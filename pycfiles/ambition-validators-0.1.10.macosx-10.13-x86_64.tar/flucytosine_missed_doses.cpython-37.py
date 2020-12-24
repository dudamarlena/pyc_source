# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/form_validators/flucytosine_missed_doses.py
# Compiled at: 2018-01-29 14:27:09
# Size of source mod 2**32: 271 bytes
from .missed_doses import MissedDosesFormValidator

class FlucytosineMissedDosesFormValidator(MissedDosesFormValidator):
    field = 'flucy_day_missed'
    reason_field = 'flucy_missed_reason'
    reason_other_field = 'missed_reason_other'
    day_range = range(1, 15)