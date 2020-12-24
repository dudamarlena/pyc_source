# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/api/migrations/0007_registration_grading_started.py
# Compiled at: 2017-09-19 13:56:43
# Size of source mod 2**32: 467 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('api', '0006_submission_submitted_by')]
    operations = [
     migrations.AddField(model_name='registration', name='grading_started', field=models.BooleanField(default=False))]