# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sw_logger/migrations/0005_add_indexes.py
# Compiled at: 2019-04-26 00:00:53
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sw_logger', '0004_auto_20180810_1127')]
    operations = [
     migrations.AlterField(model_name=b'log', name=b'level', field=models.CharField(max_length=10, choices=[('', ''), ('CRITICAL', 'CRITICAL'), ('ERROR', 'ERROR'), ('WARNING', 'WARNING'), ('INFO', 'INFO'), ('DEBUG', 'DEBUG'), ('NOTSET', 'NOTSET')], default=b'NOTSET', db_index=True)),
     migrations.AlterField(model_name=b'log', name=b'created', field=models.DateTimeField(auto_now_add=True, db_index=True))]