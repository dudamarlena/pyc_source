# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/florian/git/hastexo-xblock/hastexo/migrations/0005_auto_20190811_1555.py
# Compiled at: 2020-03-13 09:19:09
# Size of source mod 2**32: 1647 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = [
     ('hastexo', '0004_auto_20190715_1053')]
    operations = [
     migrations.AddField(model_name='stack', name='hook_events', field=jsonfield.fields.JSONField(default='null')),
     migrations.AddField(model_name='stack', name='hook_script', field=models.CharField(max_length=256, null=True)),
     migrations.AddField(model_name='stack', name='providers', field=jsonfield.fields.JSONField(default='null')),
     migrations.AddField(model_name='stack', name='run', field=models.CharField(blank=True, max_length=50)),
     migrations.AddField(model_name='stacklog', name='hook_events', field=jsonfield.fields.JSONField(default='null')),
     migrations.AddField(model_name='stacklog', name='hook_script', field=models.CharField(max_length=256, null=True)),
     migrations.AddField(model_name='stacklog', name='providers', field=jsonfield.fields.JSONField(default='null')),
     migrations.AddField(model_name='stacklog', name='run', field=models.CharField(blank=True, max_length=50))]