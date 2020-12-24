# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sw_logger/migrations/0004_auto_20180810_1127.py
# Compiled at: 2018-08-14 23:23:05
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sw_logger', '0003_auto_20170624_1913')]
    operations = [
     migrations.AlterModelOptions(name=b'log', options={b'ordering': ('id', )}),
     migrations.AddField(model_name=b'log', name=b'fk_object_id', field=models.IntegerField(db_index=True, null=True)),
     migrations.AlterField(model_name=b'log', name=b'action', field=models.CharField(choices=[('', ''), ('created', 'created'), ('updated', 'updated'), ('deleted', 'deleted'), ('other', 'other')], default=b'', max_length=10))]