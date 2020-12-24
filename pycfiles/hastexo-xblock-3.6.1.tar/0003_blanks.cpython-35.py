# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/florian/git/hastexo-xblock/hastexo/migrations/0003_blanks.py
# Compiled at: 2019-08-19 03:16:13
# Size of source mod 2**32: 2596 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('hastexo', '0002_stacklog')]
    operations = [
     migrations.AlterField(model_name='stack', name='error_msg', field=models.CharField(max_length=256, blank=True)),
     migrations.AlterField(model_name='stack', name='key', field=models.TextField(blank=True)),
     migrations.AlterField(model_name='stack', name='launch_task_id', field=models.CharField(max_length=40, blank=True)),
     migrations.AlterField(model_name='stack', name='password', field=models.CharField(max_length=128, blank=True)),
     migrations.AlterField(model_name='stack', name='protocol', field=models.CharField(max_length=32, blank=True)),
     migrations.AlterField(model_name='stack', name='provider', field=models.CharField(max_length=32, blank=True)),
     migrations.AlterField(model_name='stack', name='status', field=models.CharField(db_index=True, max_length=32, blank=True)),
     migrations.AlterField(model_name='stack', name='user', field=models.CharField(max_length=32, blank=True)),
     migrations.AlterField(model_name='stacklog', name='error_msg', field=models.CharField(max_length=256, blank=True)),
     migrations.AlterField(model_name='stacklog', name='launch_task_id', field=models.CharField(max_length=40, blank=True)),
     migrations.AlterField(model_name='stacklog', name='protocol', field=models.CharField(max_length=32, blank=True)),
     migrations.AlterField(model_name='stacklog', name='provider', field=models.CharField(max_length=32, blank=True)),
     migrations.AlterField(model_name='stacklog', name='status', field=models.CharField(db_index=True, max_length=32, blank=True)),
     migrations.AlterField(model_name='stacklog', name='user', field=models.CharField(max_length=32, blank=True))]