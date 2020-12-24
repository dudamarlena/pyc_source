# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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