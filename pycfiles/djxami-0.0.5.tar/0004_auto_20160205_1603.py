# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/xacce/addit/Projects/inventory/venv/local/lib/python2.7/site-packages/djxami/migrations/0004_auto_20160205_1603.py
# Compiled at: 2016-02-08 09:41:09
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djxami', '0003_message_stream')]
    operations = [
     migrations.AddField(model_name=b'message', name=b'expires', field=models.DateTimeField(blank=True, null=True)),
     migrations.AddField(model_name=b'message', name=b'permanent', field=models.BooleanField(default=False))]