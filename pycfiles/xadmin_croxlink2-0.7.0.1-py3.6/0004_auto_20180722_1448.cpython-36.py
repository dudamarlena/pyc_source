# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/xadmin/migrations/0004_auto_20180722_1448.py
# Compiled at: 2018-07-22 02:49:51
# Size of source mod 2**32: 783 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('xadmin', '0003_auto_20160715_0100')]
    operations = [
     migrations.AlterField(model_name='log',
       name='action_time',
       field=models.DateTimeField(db_index=True, default=(django.utils.timezone.now), editable=False, verbose_name='action time')),
     migrations.AlterField(model_name='log',
       name='object_id',
       field=models.CharField(blank=True, db_index=True, max_length=191, null=True, verbose_name='object id'))]