# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/models/observation_alert.py
# Compiled at: 2019-08-13 09:00:38
# Size of source mod 2**32: 396 bytes
from django.db import models
from tom_observations.models import ObservationRecord

class ObservationAlert(models.Model):
    __doc__ = '\n    A model to store an email address with an observation, so that an alert can\n    be issued when there is a change in the observation status\n    '
    observation = models.ForeignKey(ObservationRecord, on_delete=(models.CASCADE))
    email = models.EmailField()