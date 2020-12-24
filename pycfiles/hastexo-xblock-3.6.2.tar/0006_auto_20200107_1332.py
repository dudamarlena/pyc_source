# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/florian/git/hastexo-xblock/hastexo/migrations/0006_auto_20200107_1332.py
# Compiled at: 2020-03-13 10:18:41
from __future__ import unicode_literals
from django.db import migrations
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = [
     ('hastexo', '0005_auto_20190811_1555')]
    operations = [
     migrations.AlterField(model_name=b'stack', name=b'hook_events', field=jsonfield.fields.JSONField(default=dict)),
     migrations.RunSQL(b'UPDATE hastexo_stack SET hook_events = \'{}\' WHERE hook_events = \'"null"\';', b'UPDATE hastexo_stack SET hook_events = \'"null"\' WHERE hook_events = \'{}\';'),
     migrations.AlterField(model_name=b'stack', name=b'providers', field=jsonfield.fields.JSONField(default=list)),
     migrations.RunSQL(b'UPDATE hastexo_stack SET providers = \'[]\' WHERE providers = \'"null"\';', b'UPDATE hastexo_stack SET providers = \'"null"\' WHERE providers = \'[]\';'),
     migrations.AlterField(model_name=b'stacklog', name=b'hook_events', field=jsonfield.fields.JSONField(default=dict)),
     migrations.AlterField(model_name=b'stacklog', name=b'providers', field=jsonfield.fields.JSONField(default=list))]