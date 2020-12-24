# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./pyas2/migrations/0020_auto_20190315_1048.py
# Compiled at: 2019-03-15 06:48:47
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0019_auto_20180127_0509')]
    operations = [
     migrations.AlterField(model_name=b'log', name=b'text', field=models.TextField()),
     migrations.AlterField(model_name=b'mdn', name=b'message_id', field=models.CharField(max_length=250, primary_key=True, serialize=False)),
     migrations.AlterField(model_name=b'message', name=b'adv_status', field=models.TextField(null=True)),
     migrations.AlterField(model_name=b'message', name=b'message_id', field=models.CharField(max_length=250, primary_key=True, serialize=False)),
     migrations.AlterField(model_name=b'payload', name=b'file', field=models.TextField())]