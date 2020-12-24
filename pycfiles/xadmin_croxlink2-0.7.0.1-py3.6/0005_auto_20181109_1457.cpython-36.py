# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/xadmin/migrations/0005_auto_20181109_1457.py
# Compiled at: 2018-11-09 01:59:22
# Size of source mod 2**32: 496 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('xadmin', '0004_auto_20180722_1448')]
    operations = [
     migrations.AlterField(model_name='log',
       name='action_flag',
       field=models.CharField(db_index=True, max_length=32, verbose_name='action flag'))]