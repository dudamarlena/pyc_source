# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idohyeon/Projects/motty/motty/app/migrations/0002_auto_20171118_0326.py
# Compiled at: 2017-11-17 22:26:18
# Size of source mod 2**32: 779 bytes
from __future__ import unicode_literals
import datetime
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('app', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='action',
       name='created_at',
       field=models.DateTimeField(default=(datetime.datetime(2017, 11, 18, 3, 26, 17, 805227)))),
     migrations.AlterField(model_name='action',
       name='resource',
       field=models.ForeignKey(blank=True, on_delete=(django.db.models.deletion.CASCADE), related_name='actions', to='app.Resource'))]