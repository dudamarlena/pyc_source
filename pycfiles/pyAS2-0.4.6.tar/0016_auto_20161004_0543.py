# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pyas2/migrations/0016_auto_20161004_0543.py
# Compiled at: 2017-03-06 23:12:21
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0015_auto_20160615_0409')]
    operations = [
     migrations.AlterField(model_name=b'log', name=b'message', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'logs', to=b'pyas2.Message'))]