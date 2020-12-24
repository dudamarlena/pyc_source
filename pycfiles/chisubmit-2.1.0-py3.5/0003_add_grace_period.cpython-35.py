# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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