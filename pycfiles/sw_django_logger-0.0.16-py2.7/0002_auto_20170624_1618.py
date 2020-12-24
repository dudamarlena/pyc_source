# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sw_logger/migrations/0002_auto_20170624_1618.py
# Compiled at: 2018-02-07 05:07:39
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sw_logger', '0001_initial')]
    operations = [
     migrations.RemoveField(model_name=b'log', name=b'http_general'),
     migrations.AddField(model_name=b'log', name=b'http_method', field=models.TextField(blank=True)),
     migrations.AddField(model_name=b'log', name=b'http_path', field=models.TextField(blank=True))]