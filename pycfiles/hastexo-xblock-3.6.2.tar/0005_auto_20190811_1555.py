# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/florian/git/hastexo-xblock/hastexo/migrations/0005_auto_20190811_1555.py
# Compiled at: 2020-03-13 09:19:09
from __future__ import unicode_literals
from django.db import migrations, models
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = [
     ('hastexo', '0004_auto_20190715_1053')]
    operations = [
     migrations.AddField(model_name=b'stack', name=b'hook_events', field=jsonfield.fields.JSONField(default=b'null')),
     migrations.AddField(model_name=b'stack', name=b'hook_script', field=models.CharField(max_length=256, null=True)),
     migrations.AddField(model_name=b'stack', name=b'providers', field=jsonfield.fields.JSONField(default=b'null')),
     migrations.AddField(model_name=b'stack', name=b'run', field=models.CharField(blank=True, max_length=50)),
     migrations.AddField(model_name=b'stacklog', name=b'hook_events', field=jsonfield.fields.JSONField(default=b'null')),
     migrations.AddField(model_name=b'stacklog', name=b'hook_script', field=models.CharField(max_length=256, null=True)),
     migrations.AddField(model_name=b'stacklog', name=b'providers', field=jsonfield.fields.JSONField(default=b'null')),
     migrations.AddField(model_name=b'stacklog', name=b'run', field=models.CharField(blank=True, max_length=50))]