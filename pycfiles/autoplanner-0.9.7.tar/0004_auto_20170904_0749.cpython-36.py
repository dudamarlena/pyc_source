# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/AutoPlanner/autoplanner/migrations/0004_auto_20170904_0749.py
# Compiled at: 2017-09-04 01:49:43
# Size of source mod 2**32: 641 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('autoplanner', '0003_auto_20170903_2337')]
    operations = [
     migrations.AlterField(model_name='organization',
       name='current_schedule',
       field=models.ForeignKey(blank=True, default=None, null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='current_organizations', to='autoplanner.ScheduleRun'))]