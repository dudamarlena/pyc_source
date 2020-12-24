# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/florian/git/hastexo-xblock/hastexo/migrations/0003_blanks.py
# Compiled at: 2019-08-19 03:16:13
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('hastexo', '0002_stacklog')]
    operations = [
     migrations.AlterField(model_name=b'stack', name=b'error_msg', field=models.CharField(max_length=256, blank=True)),
     migrations.AlterField(model_name=b'stack', name=b'key', field=models.TextField(blank=True)),
     migrations.AlterField(model_name=b'stack', name=b'launch_task_id', field=models.CharField(max_length=40, blank=True)),
     migrations.AlterField(model_name=b'stack', name=b'password', field=models.CharField(max_length=128, blank=True)),
     migrations.AlterField(model_name=b'stack', name=b'protocol', field=models.CharField(max_length=32, blank=True)),
     migrations.AlterField(model_name=b'stack', name=b'provider', field=models.CharField(max_length=32, blank=True)),
     migrations.AlterField(model_name=b'stack', name=b'status', field=models.CharField(db_index=True, max_length=32, blank=True)),
     migrations.AlterField(model_name=b'stack', name=b'user', field=models.CharField(max_length=32, blank=True)),
     migrations.AlterField(model_name=b'stacklog', name=b'error_msg', field=models.CharField(max_length=256, blank=True)),
     migrations.AlterField(model_name=b'stacklog', name=b'launch_task_id', field=models.CharField(max_length=40, blank=True)),
     migrations.AlterField(model_name=b'stacklog', name=b'protocol', field=models.CharField(max_length=32, blank=True)),
     migrations.AlterField(model_name=b'stacklog', name=b'provider', field=models.CharField(max_length=32, blank=True)),
     migrations.AlterField(model_name=b'stacklog', name=b'status', field=models.CharField(db_index=True, max_length=32, blank=True)),
     migrations.AlterField(model_name=b'stacklog', name=b'user', field=models.CharField(max_length=32, blank=True))]