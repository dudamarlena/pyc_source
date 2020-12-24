# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/api/migrations/0003_add_grace_period.py
# Compiled at: 2017-04-03 16:34:20
# Size of source mod 2**32: 654 bytes
from __future__ import unicode_literals
import datetime
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('api', '0002_connstr_length')]
    operations = [
     migrations.AddField(model_name='assignment', name='grace_period', field=models.DurationField(default=datetime.timedelta(0))),
     migrations.AddField(model_name='submission', name='in_grace_period', field=models.BooleanField(default=False))]